from heg import provider
from ratelimit import limits, sleep_and_retry
import pandas as pd
import requests

# The URL for the Powerdog API
METEOCONTROL_API_URL = "http://ws.meteocontrol.de/api/sites/ZDT8R/data/energygeneration/"
# How many minutes between reported data?
METEOCONTROL_FREQ = 15
# How many calls per minute?
METEOCONTROL_ALLOWANCE = 40


class ProviderMeteoControl(provider.Provider):
    def __init__(self, username, apikey, freq=METEOCONTROL_FREQ, **kwargs):
        """
        Arguments:
            username {string} -- The login username
            apikey {string} -- The apikey

        Keyword Arguments:
            freq {int} -- Frequency of datapoints (default: {METEOCONTROL_FREQ})
            name {string} -- The name of this project
        """
        super().__init__(freq, **kwargs)
        self.username = username
        self.apikey = apikey

    @sleep_and_retry
    @limits(calls=METEOCONTROL_ALLOWANCE, period=60)
    def get_day_data(self, date):
        """Returns the energy data for one day

        Arguments:
            date {datetime.date} -- The date to get data for

        Returns:
            pd.Series -- The Energy data in a Series
        """
        link = "{url}?apiKey={apikey}&type=day&date={year}-{month}-{day}"
        link = link.format(url=METEOCONTROL_API_URL, apikey=self.apikey,
                           year=date.year, month=date.month, day=date.day)
        response = requests.get(link)
        response_json = response.json()['chartData']['data']
        df = pd.DataFrame(response_json)
        df = df.set_index(0)
        df.index = df.index / 1000
        df = self._reindex_day_data(df)
        data = df[1]
        data.name = self.name
        return data
