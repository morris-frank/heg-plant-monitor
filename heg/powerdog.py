from heg import provider
import datetime
import pandas as pd
import xmlrpc.client

# The URL for the Powerdog API
POWERDOG_API_URL = "http://api.power-dog.eu:80/index.php"
# How manny minutes between reported data?
POWERDOG_FREQ = 5


class ProviderPowerdog(provider.Provider):
    def __init__(self, username, apikey, freq=POWERDOG_FREQ, **kwargs):
        super().__init__(freq, **kwargs)
        self.username = username
        self.apikey = apikey
        self.client = xmlrpc.client.ServerProxy(POWERDOG_API_URL)
        self.powerdog_ids = None
        self.powerdog_inv = None
        self.powerdog_snum = None
        self.freq = freq

    # Rate limit
    def load_powerdog_strings(self):
        """[summary]
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

    # Rate limit
    def get_powerdog_data(self, id, date):
        powerdog_series = pd.Series(index=self.time_range(date), name=id)

        start_ts = int(date.timestamp())
        end_ts = start_ts + 86400 - 1
        for inverter_id, n_string in zip(self.powerdog_inv[id], self.powerdog_snum[id]):
            for string_id in range(1, n_string + 1):
                string_data = self.client.getStringData(
                    self.apikey, inverter_id, string_id, start_ts, end_ts)
                df = self.process_string_data(string_data)
                powerdog_series += df['PDC']
        return powerdog_series

    def process_string_data(self, string_data):
        """[summary]

        Arguments:
            string_data {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        string_data = string_data['datasets']
        df = pd.DataFrame(string_data)
        df = df.T
        df.index = df.index.astype('int64')
        df = df.apply(pd.to_numeric, errors='ignore')
        df = self._reindex_day_data(df)
        return df

    def get_day_data(self, date):
        if self.powerdog_ids is None:
            self.load_powerdog_strings()
        data = []
        for id in self.powerdog_ids:
            data.append(self.get_powerdog_data(id, date))
        return data
