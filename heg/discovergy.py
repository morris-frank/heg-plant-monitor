from heg import provider
from ratelimit import limits, sleep_and_retry
import os
import pandas as pd
import requests
from requests_oauthlib import OAuth1Session
import yaml

# The URL for the Discovergy API
API = 'https://api.discovergy.com/public/v1'
# How manny minutes between reported data?
FREQ = 1440
# How many calls per minute?
ALLOWANCE = 60
# The file to save client secrets
SECRET_FILE = '.discovergy_secret.yaml'


class ProviderDiscovergy(provider.Provider):
    def __init__(self, freq=FREQ, **kwargs):
        """
        Arguments:

        Keyword Arguments:
            freq {int} -- Frequency of datapoints (default: {FREQ})
            name {string} -- The name of this project
        """
        super().__init__(freq, **kwargs)
        self.load_client_secrets()
        self.register_session

    @sleep_and_retry
    @limits(calls=ALLOWANCE, period=60)
    def get_day_data(self, date):
        """Returns the energy data for one day

        Arguments:
            date {datetime.date} -- The date to get data for

        Returns:
            pd.Series -- The Energy data in a Series
        """
        pass

    def register_session(self):
        self.session = OAuth1Session(client_key=self.client_key, client_secret=self.client_secret)

        # Get Oauth token
        uri_request_token = API + '/oauth1/request_token'
        response_request_token = self.session.post(uri_request_token)
        encoded_token = [e.split('=') for e in response_request_token.text.split('&')]
        self.oauth_token = encoded_token[0][1]
        self.oauth_token_secret = encoded_token[1][1]

        # Authorize token
        # uri_auth_token = API + '/oauth1/authorize?oauth_token={token}&email={email}&password={password}'
        # uri_auth_token.format(token=self.oauth_token, email=self.username, password=self.password)

    def load_client_secrets(self):
        """Loads the client secrets from disk. Or requests new ones if there are no.
        """
        # The file to save client secrets
        if not os.path.exists(SECRET_FILE):
            self.register_client()
        with open(SECRET_FILE, 'r') as fp:
            secrets = yaml.load(fp)
        self.client_key = secrets['key']
        self.client_secret = secrets['secret']

    def register_client(self):
        """Register a new client and save the secrets.
        """
        uri = API + '/oauth1/consumer_token'
        app_name = 'HEG-Plant-Collector'
        response = requests.post(uri, data={'client': app_name}).json()
        secrets = {'key': response['key'],
                   'secret': response['secret']}
        with open(SECRET_FILE, 'w') as fp:
            yaml.dump(secrets, fp)
