from heg import provider
from ratelimit import limits, sleep_and_retry
import pandas as pd
import ftplib

# The URL for the SolarLog API
API = 'home9.solarlog-web.de'
# How manny minutes between reported data?
FREQ = 5
# How many calls per minute?
ALLOWANCE = 60
# The file to cache ftp requests in
CACHE_FILE = '.solarlog.cache'


class ProviderSolarLog(provider.Provider):
    def __init__(self, username, password, freq=FREQ, **kwargs):
        """
        Arguments:

        Keyword Arguments:
            freq {int} -- Frequency of datapoints (default: {FREQ})
            name {string} -- The name of this project
        """
        super().__init__(freq, **kwargs)
        self.username = username
        self.password = password

    @sleep_and_retry
    @limits(calls=ALLOWANCE, period=60)
    def get_day_data(self, date):
        """Returns the energy data for one day

        Arguments:
            date {datetime.date} -- The date to get data for

        Returns:
            pd.Series -- The Energy data in a Series
        """
        # The name of the file on the ftp server:
        remote_filename = 'min' + date.strftime('%y%m%d') + '.js'

        # Retrieve file for this day from ftp server:
        try:
            ftp = ftplib.FTP(API)
            ftp.login(user=self.username, passwd=self.password)
            ftp.retrbinary('RETR {}'.format(remote_filename),
                        open(CACHE_FILE, 'wb').write)
            ftp.quit()
        except:
            return self._empty_day_data(date)

        # Parse file:
        data = []
        with open(CACHE_FILE, 'r') as f:
            for line in f:
                if len(line) < 50:
                    continue
                line = line[9:-2].split('|')
                time = line[0]
                energy = 0.0
                for datum in line[1:-1]:
                    inv_energy = datum.split(';')[0]
                    energy += float(inv_energy)
                data.append([time, energy])

        if len(data) == 0:
            return self._empty_day_data(date)
        df = pd.DataFrame(data)
        df = df.set_index(0)
        df.index = pd.to_datetime(df.index, dayfirst=True)
        df = self._reindex_day_data(df)
        # W to kW:
        df /= 1000
        # kW to kWh:
        df *= FREQ / 60

        series = df[1]
        series.name = self.name
        return series
