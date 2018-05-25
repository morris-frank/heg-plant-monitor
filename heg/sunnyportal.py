from heg import provider
from ratelimit import limits, sleep_and_retry
import pandas as pd
import requests

# The URL for the SolarLog API
HOST = 'https://www.sunnyportal.com'
# How manny minutes between reported data?
FREQ = 5
# How many calls per minute?
ALLOWANCE = 60

class ProviderSolarLog(provider.Provider):
    def __init__(self, username, password, freq=FREQ, **kwargs):
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
        pass
    
    def _prepare_session(self):
        pass