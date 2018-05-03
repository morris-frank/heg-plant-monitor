from heg import provider
import requests
import pandas as pd
from ratelimit import limits, sleep_and_retry

# The URL for the Powerdog API
METEOCONTROL_API_URL = "http://ws.meteocontrol.de/api/sites/ZDT8R/data/energygeneration/"
# How many minutes between reported data?
METEOCONTROL_FREQ = 15
# How many calls per minute?
METEOCONTROL_ALLOWANCE = 40

class ProviderMeteoControl(provider.Provider):
    def __init__(self, username, apikey, freq=METEOCONTROL_FREQ, **kwargs):
        super().__init__(freq, **kwargs)
        self.username = username
        self.apikey = apikey

    @sleep_and_retry
    @limits(calls=METEOCONTROL_ALLOWANCE, period=60)
    def get_day_data(self, date):
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
