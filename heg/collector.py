import argparse
import datetime
import heg
import logging
import multiprocessing as mp
import yamale

DEFAULT_CONFIG = 'config.yaml'


class Collector(object):
    def __init__(self, arguments=[]):
        """
        Keyword Arguments:
            arguments {list} -- The cli options as a list (default: {[]})
        """
        self.parse_arguments(arguments)
        self.load_config(self.args.config)
        self.yesterday = datetime.date.today() - datetime.timedelta(days=1)

    def parse_arguments(self, arguments):
        """Parses cli options/arguments given as a list. 

        Arguments:
            arguments {list} -- The cli options/list
        """
        parser = argparse.ArgumentParser(description='HEG data collector')
        parser.add_argument(
            '-v', '--verbose', action='store_true', help='Make output more verbose.')
        parser.add_argument(
            '-f', '--force', '--overwrite', action='store_true', help='Overwrite all existing data.')
        parser.add_argument('--no-mp', action='store_true',
                            help='Don\'t do multiprocessing')
        parser.add_argument('-c', '--config', default=DEFAULT_CONFIG,
                            type=str, help='The config file to use.')

        self.args = parser.parse_args(arguments)

        if self.args.verbose:
            logging.basicConfig(level=logging.DEBUG)

    def load_config(self, filepath, schemapath='config.schema.yaml'):
        """Load the config file and validate against the schema

        Arguments:
            filepath {str} -- The path to the config file

        Keyword Arguments:
            schemapath {str} -- The path to the schema file (default: {'config.schema.yaml'})
        """
        schema = yamale.make_schema(schemapath)
        data = yamale.make_data(filepath)
        data = yamale.validate(schema, data)
        self.config = data[0]

    def collect(self):
        """Collect and save ALL THA DATA FOR ALL THA PROJECTS.
        """
        if 'projects' not in self.config:
            logging.warn('No projects listed in config.')
        for project in self.config['projects']:
            if self.args.no_mp:
                if heg.utils.query_boolean('Collect {name}?'.format(name=project['name'])):
                    self.collect_project(project)
            else:
                _project_process = mp.Process(
                    target=self.collect_project, args=(project,))
                _project_process.start()

    def collect_project(self, project):
        """Collect and save all the data for one project

        Arguments:
            project {dict} -- The config dict for the project
        """
        collector_functions = {
            'auroraonline': self._provider_auroraonline,
            'meteocontrol': self._provider_meteocontrol,
            'powerdog': self._provider_powerdog,
            'pvscreen': self._provider_pvscreen,
            'solarlog': self._provider_solarlog,
            'discovergy': self._provider_discovergy
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
        powerdog_id = plant['username']
        apikey = project['apikey']
        name = plant['name']
        return heg.powerdog.ProviderPowerdog(powerdog_id, apikey, name=name)

    def _provider_pvscreen(self, project, plant):
        location = plant['username']
        name = plant['name']
        return heg.pvscreen.ProviderPVScreen(location, name=name)

    def _provider_solarlog(self, project, plant):
        username = plant['username']
        password = project['apikey']
        name = plant['name']
        return heg.solarlog.ProviderSolarLog(username, password, name=name)

    def _provider_discovergy(self, project, plant)
        email = plant['username']
        password = project['apikey']
        name = plant['name']
        return heg.discovergy.ProviderDiscovergy(email, password, name=name)
