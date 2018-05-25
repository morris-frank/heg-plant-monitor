import argparse
import datetime
import logging
import yamale

DEFAULT_CONFIG = 'config.yaml'


class App(object):
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