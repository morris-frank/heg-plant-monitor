from heg import provider
from ratelimit import limits, sleep_and_retry
import datetime
import pandas as pd
import zeep

# The URL for the pvScreen API
PVSCREEN_API_URL = 'http://pvscreen.de/investor/SolarWebService?wsdl'
# How manny minutes between reported data?
PVSCREEN_FREQ = 1440
# How many calls per minute?
PVSCREEN_ALLOWANCE = 60


class ProviderPVScreen(provider.Provider):
    def __init__(self, location, freq=PVSCREEN_FREQ, **kwargs):
        """
        Arguments:
            location {string} -- The Location (ID)

        Keyword Arguments:
            freq {int} -- Frequency of datapoints (default: {PVSCREEN_FREQ})
            name {string} -- The name of this project
        """
        super().__init__(freq, **kwargs)
        self.client = zeep.Client(wsdl=PVSCREEN_API_URL)
        self.location = location

    @sleep_and_retry
    @limits(calls=PVSCREEN_ALLOWANCE, period=60)
    def get_day_data(self, date):
        """Returns the energy data for one day

        Arguments:
            date {datetime.date} -- The date to get data for

        Returns:
            pd.Series -- The Energy data in a Series
        """
        date_str = '{:04d}-{:02d}-{:02d}'.format(
            date.year, date.month, date.day)

        client_response = self.client.service.getDailyEnergyData(
            locationNames=self.location, startDate=date_str, endDate=date_str)

        s = pd.Series(index=self.time_range(date), name=self.location)
        s[0] = client_response[0]['values'][0]['energy']
        return s
