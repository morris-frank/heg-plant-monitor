import argparse
import datetime
import heg
import logging
import multiprocessing as mp
import yamale
import yaml

DEFAULT_CONFIG = 'config.yaml'


class Collector(object):
    def __init__(self, arguments=[]):
        self.parse_arguments(arguments)
        self.load_config(self.args.config)
        self.yesterday = datetime.date.today() - datetime.timedelta(days=1)

    def parse_arguments(self, arguments):
        parser = argparse.ArgumentParser(description='HEG data collector')
        parser.add_argument(
            '-v', '--verbose', action='store_true', help='Make output more verbose.')
        parser.add_argument(
            '-f', '--force', '--overwrite', action='store_true', help='Overwrite all existing data.')
        parser.add_argument('-c', '--config', default=DEFAULT_CONFIG,
                            type=str, help='The config file to use.')

        self.args = parser.parse_args(arguments)

        if self.args.verbose:
            logging.basicConfig(level=logging.DEBUG)

    def load_config(self, filepath, schemapath='config.schema.yaml'):
        schema = yamale.make_schema(schemapath)
        data = yamale.make_data(filepath)
        data = yamale.validate(schema, data)
        self.config = data[0]

    def collect(self):
        if 'projects' not in self.config:
            logging.warn('No projects listed in config.')
        for project in self.config['projects']:
            _project_process = mp.Process(target=self.collect_project, args=(project,))
            _project_process.start()

    def collect_project(self, project):
        collector_functions = {
            'auroraonline': self._provider_auroraonline,
            'meteocontrol': self._provider_meteocontrol,
            'powerdog': self._provider_powerdog,
            'pvscreen': self._provider_pvscreen
        }

        if project['provider'] not in collector_functions:
            logging.error('Given Provider for {name} is not valid!'.format(
                name=project['name']))

        _collect = collector_functions[project['provider']]
        for plant in project['plants']:
            provider = _collect(project, plant)
            provider.save_range_data(
                plant['start'], self.yesterday, self.args.force)

    def _provider_auroraonline(self, project, plant):
        pass

    def _provider_meteocontrol(self, project, plant):
        username = plant['username']
        apikey = project['apikey']
        name = plant['name']
        return heg.meteocontrol.ProviderMeteoControl(username, apikey, name=name)

    def _provider_powerdog(self, project, plant):
        pass

    def _provider_pvscreen(self, project, plant):
        location = plant['username']
        name = plant['name']
        return heg.pvscreen.ProviderPVScreen(location, name=name)
