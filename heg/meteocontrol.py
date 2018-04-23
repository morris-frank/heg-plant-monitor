from heg import provider
import requests
import pandas as pd

# The URL for the Powerdog API
METEOCONTROL_API_URL = "http://ws.meteocontrol.de/api/sites/ZDT8R/data/energygeneration/"
# How manny minutes between reported data?
METEOCONTROL_FREQ = 15

class proivder_meteocontrol(provider.provider):
    def __init__(self, username, apikey, freq=METEOCONTROL_FREQ):
        self.username = username
        self.apikey = apikey
        self.freq = freq

    def get_day_data(self, year, month, day):
        self._day_ts(year, month, day)
        link = "{url}?apiKey={ak}&type=day&date={y}-{m}-{d}"
        link = link.format(url=METEOCONTROL_API_URL, ak=self.apikey, y=year, m=month, d=day)
        response = requests.get(link)
        data = response.json()['chartData']['data']
        df = pd.DataFrame(data)
        df = df.set_index(0)
        df.index = df.index / 1000
        df = self._reindex_day_data(df)
        return df