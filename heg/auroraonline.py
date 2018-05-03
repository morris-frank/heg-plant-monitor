from heg import provider
import requests
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# The URL for the Powerdog API
AURORAONLINE_API_URL = "https://auroraonline.abbsolarinverters.com/abb/"
# How manny minutes between reported data?
AURORAONLINE_FREQ = 10


class ProviderAuroraOnline(provider.Provider):
    def __init__(self, username, password, freq=AURORAONLINE_FREQ, **kwargs):
        super().__init__(freq, **kwargs)
        self.username = username
        self.password = password
        self.freq = freq

    def _prepare_session(self, datalogger):
        session = requests.Session()
        # headers = {
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Accept-Language': 'en-US,en;q=0.5',
        #     'Cache-Control': 'no-cache',
        #     'Connection': 'keep-alive',
        #     'Host': 'auroraonline.abbsolarinverters.com',
        #     'Pragma': 'no-cache',
        #     'Upgrade-Insecure-Requests': '1',
        #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'
        # }
        # session.headers.update(headers)

        login_url = AURORAONLINE_API_URL + 'login.php'
        datalogger_url = AURORAONLINE_API_URL + \
            'section.php?sn_datalogger={}'.format(datalogger)

        # YES! it is necassary that we walk the same path through the website as a natural user would do!
        _ = session.post(login_url, data={
            'posted_username': self.username, 'posted_password': self.password},
            verify=False)
        # session.headers.update({'Referer': login_url})
        _ = session.get(
            datalogger_url, allow_redirects=False, verify=False)
        return session

    def get_day_data(self, date):
        pass
