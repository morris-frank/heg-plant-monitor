from heg import provider
import datetime
import zeep
import pandas as pd
from ratelimit import limits, sleep_and_retry

# The URL for the pvScreen API
PVSCREEN_API_URL = 'http://pvscreen.de/investor/SolarWebService?wsdl'
# How manny minutes between reported data?
PVSCREEEN_FREQ = 1440
# How many calls per minute?
PVSCREEN_ALLOWANCE = 30


class ProviderPVScreen(provider.Provider):
    def __init__(self, location, freq=PVSCREEEN_FREQ, **kwargs):
        super().__init__(freq, **kwargs)
        self.client = zeep.Client(wsdl=PVSCREEN_API_URL)
        self.location = location

    def _fetch_data(self, location, date):
        """Fetch the generated energy for a plant for one day.

        Arguments:
            location {string} -- The location ID (name)
            date {string} -- The yyyy-mm-dd fromatted date

        Returns:
            [float] -- The Energy for this date/location
        """
        response = self.client.service.getDailyEnergyData(
            locationNames=location, startDate=date, endDate=date)
        return response[0]['values'][0]['energy']

    @sleep_and_retry
    @limits(calls=PVSCREEN_ALLOWANCE, period=60)
    def get_day_data(self, date):
        date_format = '{:04d}-{:02d}-{:02d}'.format(
            date.year, date.month, date.day)
        s = pd.Series(index=self.time_range(date), name=self.location)
        s[0] = self._fetch_data(self.location, date_format)
        return s
