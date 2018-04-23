from heg import utils
import pandas as pd
import datetime

class provider(object):
    def __init__(self, freq):
        self.freq = freq
        pass

    def _reindex_day_data(self, df):
        """Normalize the data for a the set time_range.
        
        Arguments:
            df {pd.DataFrame | pd.Series} -- The DataFrame or Series to normalize.
        
        Returns:
            pd.DataFrame | pd.Series -- The normalized DataFrame or Series
        """
        df.index = pd.to_datetime(df.index, unit='s')
        df = df.reindex(self.time_range, method='nearest', tolerance='{}min'.format(self.freq))
        df = df.sort_index()
        df = df.fillna(0)
        return df

    def _day_ts(self, year, month, day):
        """Set the timestamps and time range for a specific day. 
        
        Arguments:
            year {int} -- The desired days year [yyyy]
            month {int} -- The desired days month [mm]
            day {int} -- The desired days day number [dd]
        """
        self.start_ts = int(datetime.datetime(year, month, day, tzinfo=datetime.timezone.utc).timestamp())
        self.end_ts = self.start_ts + 86400 - 1
        self.time_range = pd.date_range(start=pd.to_datetime(self.start_ts, unit='s'),
                                        end=pd.to_datetime(self.end_ts, unit='s'),
                                        freq='{}min'.format(self.freq))

    def get_day_data(self, year, month, day):
        """Get the data for this plant for one specific day.
        
        Arguments:
            year {int} -- The desired days year [yyyy]
            month {int} -- The desired days month [mm]
            day {int} -- The desired days day number [dd]
        """
        self._day_ts(year, month, day)