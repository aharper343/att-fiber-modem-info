import os

import requests
from bs4 import BeautifulSoup


class ModemConfig:
    url: str
    access_code: str

    def __init__(self, url: str, access_code: str):
        self.url = url
        self.access_code = access_code

    @staticmethod
    def from_env():
        return ModemConfig(
            url=os.getenv("MODEM_URL", "http://192.168.1.254"),
            access_code=os.getenv("MODEM_ACCESS_CODE", None)
        )


class ModemClient:

    def __init__(self, config: ModemConfig):
        self.config = config
        self.session = requests.Session()
        self.nonce = None
        self.logged_in = False

    def _fetch(self, path) -> requests.Response:
        full_url = f"{self.config.url}{path}"
        response = self.session.get(full_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        nonce_tag = soup.find('input', {'name': 'nonce'})
        if nonce_tag:
            self.nonce = nonce_tag['value']
        return response

