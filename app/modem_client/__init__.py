import logging
import os

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, Timeout, ConnectionError
from urllib.parse import urljoin


class ModemConfig:
    url: str
    access_code: str

    def __init__(self, id: str, url: str, access_code: str):
        if not id:
            raise ValueError("id is required")
        if not url:
            raise ValueError("url is required")
        self.id = id
        self.url = url
        self.access_code = access_code

    @staticmethod
    def from_env():
        return ModemConfig(
            id=os.getenv("MODEM_ID", "att"),
            url=os.getenv("MODEM_URL", "http://192.168.1.254"),
            access_code=os.getenv("MODEM_ACCESS_CODE", None)
        )


class ModemClient:

    def __init__(self, config: ModemConfig):
        self.config = config
        self.session = requests.Session()
        self.nonce = None
        self.logged_in = False
        self.logger = logging.getLogger(self.__class__.__name__)

    def _fetch(self, path) -> requests.Response:
        full_url = urljoin(self.config.url, path)
        try:
            response = self.session.get(full_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            nonce_tag = soup.find('input', {'name': 'nonce'})
            if nonce_tag:
                self.nonce = nonce_tag['value']
            return response
        except Timeout:
            self.logger.error(f"Timeout connecting to {full_url}")
            raise
        except ConnectionError as e:
            self.logger.error(f"Connection error to {full_url}: {e}")
            raise
        except RequestException as e:
            self.logger.error(f"Request failed for {full_url}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error fetching {full_url}: {e}")
            raise
