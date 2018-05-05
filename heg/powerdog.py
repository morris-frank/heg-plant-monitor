from heg import provider
from ratelimit import limits, sleep_and_retry
import datetime
import pandas as pd
import xmlrpc.client

POWERDOG_API_URL = "http://api.power-dog.eu:80/index.php"
POWERDOG_FREQ = 5
POWERDOG_ALLOWANCE = 60


class ProviderPowerdog(provider.Provider):
    def __init__(self, powerdog_id, apikey, freq=POWERDOG_FREQ, **kwargs):
        """
        Arguments:
            powerdog_id {string} -- The id of the powerdog
            apikey {string} -- The apikey

        Keyword Arguments:
            freq {int} -- Frequency of datapoints (default: {POWERDOG_FREQ})
            name {string} -- The name of this project
        """
        super().__init__(freq, **kwargs)
        self.powerdog_id = powerdog_id
        self.apikey = apikey
        self.client = xmlrpc.client.ServerProxy(POWERDOG_API_URL)
        self.powerdog_ids = None
        self.powerdog_inv = None
        self.powerdog_snum = None
        self.load_powerdog_strings()

    def load_powerdog_strings(self):
        """Retrieve all Powerdog IDS, Inverters and number of strings for this apikey.
        """
        powerdogs = self.client.getPowerDogs(self.apikey)['powerdogs']
        self.powerdog_ids = []
        self.powerdog_inv = {}
        self.powerdog_snum = {}
        for powerdog in powerdogs:
            id = powerdog['id']
            inverters = self.client.getInverters(self.apikey, id)['inverters']
            inverter_ids = []
            inverter_snum = []
            for inverter in inverters.values():
                inverter_ids.append(int(inverter['id']))
                inverter_snum.append(int(inverter['Strings']))
            self.powerdog_ids.append(id)
            self.powerdog_inv[id] = inverter_ids
            self.powerdog_snum[id] = inverter_snum

    @sleep_and_retry
    @limits(calls=POWERDOG_ALLOWANCE, period=60)
    def get_day_data(self, date):
        """Returns the energy data for one day

        Arguments:
            date {datetime.date} -- The date to get data for

        Returns:
            pd.Series -- The Energy data in a Series
        """
        powerdog_series = pd.Series(
            index=self.time_range(date), name=self.name)
        powerdog_series = powerdog_series.fillna(0)

        start_ts = int(datetime.datetime(
            date.year, date.month, date.day).timestamp())
        # Timezone aligning for dummies:
        start_ts = start_ts - 2 * 60
        end_ts = start_ts + 86400 - 1
        for inverter_id, n_string in zip(self.powerdog_inv[self.powerdog_id], self.powerdog_snum[self.powerdog_id]):
            for string_id in range(1, n_string + 1):
                string_data = self.client.getStringData(
                    self.apikey, inverter_id, string_id, start_ts, end_ts)
                df = self.process_string_data(string_data)
                powerdog_series += df['PDC']

        # Convert W to kW:
        powerdog_series /= 1000
        # Convert kW to kWh
        powerdog_series *= self.freq / 60

        return powerdog_series

    def process_string_data(self, string_data):
        """Process the energy data of a string

        Arguments:
            string_data {dict} -- The data for one string unchanged from the client

        Returns:
            pd.DataFrame -- The normalized and processed strings data in a DF
        """
        string_data = string_data['datasets']
        df = pd.DataFrame(string_data)
        df = df.T
        df.index = df['TIMESTAMP_LOCAL']
        df.index = df.index.astype('int64')
        df = df.apply(pd.to_numeric, errors='ignore')
        df = self._reindex_day_data(df)
        return df
