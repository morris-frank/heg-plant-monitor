from heg import provider
from ratelimit import limits, sleep_and_retry
import pandas as pd

# The URL for the SolarLog API
SOLARLOG_API_URL = '1.1.1.1'
# How manny minutes between reported data?
SOLARLOG_FREQ = 1440
# How many calls per minute?
SOLARLOG_ALLOWANCE = 60


class ProviderSolarLog(provider.Provider):
    def __init__(self, freq=SOLARLOG_FREQ, **kwargs):
        """
        Arguments:

        Keyword Arguments:
            freq {int} -- Frequency of datapoints (default: {SOLARLOG_FREQ})
            name {string} -- The name of this project
        """
        super().__init__(freq, **kwargs)

    @sleep_and_retry
    @limits(calls=SOLARLOG_ALLOWANCE, period=60)
    def get_day_data(self, date):
        """Returns the energy data for one day

        Arguments:
            date {datetime.date} -- The date to get data for

        Returns:
            pd.Series -- The Energy data in a Series
        """
        pass