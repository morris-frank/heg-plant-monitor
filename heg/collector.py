import heg
import heg.app
import logging
import multiprocessing as mp
from colorama import Fore


class Collector(heg.app.App):
    def __init__(self, arguments=[]):
        """
        Keyword Arguments:
            arguments {list} -- The cli options as a list (default: {[]})
        """
        super().__init__(arguments)

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
            print(Fore.RESET + 'Started plant ' + Fore.YELLOW +
                  plant['name'] + Fore.RESET + ' of project ' + Fore.RED + project['name'])
            provider.save_range_data(
                plant['start'], self.yesterday, self.args.force)
            print(Fore.RESET + 'Finished project ' + Fore.YELLOW +
                  plant['name'] + Fore.RESET + ' of project ' + Fore.RED + project['name'])
        print(Fore.GREEN + 'Finished project ' + Fore.RED + project['name'])

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

    def _provider_discovergy(self, project, plant):
        email = plant['username']
        password = project['apikey']
        name = plant['name']
        return heg.discovergy.ProviderDiscovergy(email, password, name=name)
