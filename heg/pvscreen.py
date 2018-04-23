from heg import provider
import datetime
import zeep
import pandas as pd

# The URL for the pvScreen API
PVSCREEN_API_URL = 'http://pvscreen.de/investor/SolarWebService?wsdl'
# How manny minutes between reported data?
PVSCREEEN_FREQ = 1440


class proivder_pvscreen(provider.provider):
    def __init__(self, locations=[], freq=PVSCREEEN_FREQ):
        self.client = zeep.Client(wsdl=PVSCREEN_API_URL)
        self.freq = freq

        if type(locations) != list:
            locations = [locations]
        self.locations = locations

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

    def get_day_data(self, year, month, day):
        self._day_ts(year, month, day)
        date_format = '{:04d}-{:02d}-{:02d}'.format(year, month, day)
        data = []
        for location in self.locations:
            s = pd.Series(index=self.time_range, name=location)
            s[0] = self._fetch_data(location, date_format)
            data.append(s)
        return data
