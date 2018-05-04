from heg import utils
import datetime
import logging
import os
import pandas as pd


class Provider(object):
    def __init__(self, freq, name='unnamed'):
        self.freq = freq
        self.name = name

    def _reindex_day_data(self, df):
        """Normalize the data for a the set time_range.

        Arguments:
            df {pd.DataFrame | pd.Series} -- The DataFrame or Series to normalize.

        Returns:
            pd.DataFrame | pd.Series -- The normalized DataFrame or Series
        """
        df.index = pd.to_datetime(df.index, unit='s')
        date = datetime.date(
            df.index[0].year, df.index[0].month, df.index[0].day)
        df = df.reindex(self.time_range(date), method='nearest',
                        tolerance='{}min'.format(self.freq))
        df = df.sort_index()
        df = df.fillna(0)
        return df

    def time_range(self, date):
        start = datetime.datetime(date.year, date.month, date.day)
        stop = start + datetime.timedelta(days=1) - \
            datetime.timedelta(seconds=1)
        return pd.date_range(start=start, end=stop, freq='{}min'.format(self.freq))

    def get_day_data(self, date):
        """Get the data for this plant for one specific day.

        Arguments:
            date {datetime.date} -- The desired day

            pd.Series | list(pd.Series) -- A list of Series of data or just a single one
        """
        data = pd.Series(self.time_range)
        return data

    def save_path(self, date):
        name_slug = utils.slugify(self.name)
        dir_path = 'export/{name}/{year}/{month}/'.format(
            name=name_slug, year=date.year, month=date.month)
        filename = '{year}-{month}-{day}_{name}.csv'.format(
            name=name_slug, year=date.year, month=date.month, day=date.day)
        return '{}{}'.format(dir_path, filename)

    def save_range_data(self, start_date, stop_date, overwrite=False):
        logging.debug('Starting saving data for {name} between {start} and {end}.'.format(
            name=self.name, start=start_date, end=stop_date))
        for date in utils.daterange(start_date, stop_date):
            if overwrite or not os.path.exists(self.save_path(date)):
                self.save_day_data(date)

    def save_day_data(self, date):
        logging.debug(
            'Getting day data for {name} on the {date}'.format(name=self.name, date=date))
        data = self.get_day_data(date)
        self.save_data(data)

    def save_data(self, data):
        save_path = self.save_path(data.index[0])
        logging.debug('Saving {fp}'.format(fp=save_path))
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        data.to_csv(save_path)
