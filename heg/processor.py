from colorama import Fore
from glob import glob
import collections
import datetime
import heg
import heg.app
import logging
import multiprocessing as mp
import os
import pandas as pd

EXPORT_DIR = './export'

class Processor(heg.app.App):
    def __init__(self, arguments=[]):
        """
        Keyword Arguments:
            arguments {list} -- The cli options as a list (default: {[]})
        """
        super().__init__(arguments)

    def process(self):
        for plant_path in glob(EXPORT_DIR + '/*'):
            plant = os.path.basename(plant_path)
            if self.args.no_mp:
                if heg.utils.query_boolean('Process ' + plant + '?'):
                    self.process_plant(plant, self.args.force)
            else:
                _plant_process = mp.Process(
                    target=self.process_plant, args=(plant, self.args.force,))
                _plant_process.start()

    def process_plant(self, plant, overwrite=False):
        plant_path = EXPORT_DIR + '/' + plant
        for year_path in glob(plant_path + '/*'):
            year = os.path.basename(year_path)
            export_file = self.config['aggr_export_path'] + '/' + plant + '/' + year + '/weekly_data.csv'
            os.makedirs(os.path.dirname(export_file), exist_ok=True)
            if not overwrite and os.path.exists(export_file):
                continue
            sums = {}
            for fpath in glob(year_path + '/*/*'):
                datestr = os.path.basename(fpath).split('_')[0]
                date = datetime.datetime.strptime(datestr, '%Y-%m-%d')
                data = pd.read_csv(fpath, index_col=0, header=None)
                sums[date] = data[1].sum()
            sums = collections.OrderedDict(sorted(sums.items()))
            weekly_energy = []
            _week_energy = 0
            first = True
            for dd in sums.items():
                if dd[0].weekday() == 1 and not first:
                    weekly_energy.append(_week_energy)
                    _week_energy = 0
                _week_energy += dd[1]
                first = False
            with open(export_file, 'w') as fp:
                print(Fore.RESET + ' Write weekly data for plant ' +
                      year + ' ' + Fore.YELLOW + plant + Fore.RESET)
                fp.write(','.join([str(e) for e in weekly_energy]))
