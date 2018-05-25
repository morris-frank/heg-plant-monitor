import heg
import heg.app
import logging
import multiprocessing as mp
from colorama import Fore


class Processor(heg.app.App):
    def __init__(self, arguments=[]):
        """
        Keyword Arguments:
            arguments {list} -- The cli options as a list (default: {[]})
        """
        super().__init__(arguments)

    def process(self):
        if 'projects' not in self.config:
            logging.warn('No projects listed in config.')
        for project in self.config['projects']:
            pass