from heg import provider
from ratelimit import limits, sleep_and_retry
import pandas as pd

# The URL for the Discovergy API
DISCOVERGY_API_URL = '1.1.1.1'
# How manny minutes between reported data?
DISCOVERGY_FREQ = 1440
# How many calls per minute?
DISCOVERGY_ALLOWANCE = 60


class ProviderDiscovergy(provider.Provider):
    def __init__(self, freq=DISCOVERGY_FREQ, **kwargs):
        """
        Arguments:

        Keyword Arguments:
            freq {int} -- Frequency of datapoints (default: {DISCOVERGY_FREQ})
            name {string} -- The name of this project
        """
        super().__init__(freq, **kwargs)

    @sleep_and_retry
    @limits(calls=DISCOVERGY_ALLOWANCE, period=60)
    def get_day_data(self, date):
        """Returns the energy data for one day

        Arguments:
            date {datetime.date} -- The date to get data for

        Returns:
            pd.Series -- The Energy data in a Series
        """
        pass