import logging
from abc import abstractmethod
from datetime import datetime, timedelta
from logging import getLogger
from typing import Optional

from bs4 import BeautifulSoup

from gatherers import DataGatherer
from modem_client import ModemClient


class ModemClientDataGatherer(DataGatherer):

    def __init__(self, client: ModemClient, uri: str, requires_login: bool = False):
        self._client = client
        self._uri = uri
        self._requires_login = requires_login
        self._logger = getLogger(self.__class__.__name__)

    def gather(self):
        try:
            response = self._client._fetch(self._uri)
            stats = self._parse_html(response.text)
            if not stats:
                raise ValueError('No statistics found')
            data = self._map(stats)
            self._logger.debug(f"Data -> {data}")
            return data
        except Exception as e:
            self._logger.error(f"Error gathering data from {self._uri}: {e}", exc_info=True)
            raise

    def get_client_config(self):
        return self._client.config

    @abstractmethod
    def _map(self, stats: dict):
        pass

    def _parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return self._parse_soup(soup)

    def _parse_soup(self, soup):
        stats = {}
        # Find all tables and iterate rows to find known labels
        tables = soup.find_all('table')
        for table in tables:
            summary = table.get('summary', '')
            self._logger.debug(f"Parsing table with summary: {summary}")
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['td', 'th'])
                if not cols:
                    continue

                # First column is usually the label
                label = cols[0].get_text(strip=True)
                if not label:
                    continue
                # Subsequent columns are values for Line 1, Line 2, etc.
                values = [c.get_text(strip=True) for c in cols[1:]]
                if not values:
                    continue
                if summary:
                    if summary not in stats:
                        stats[summary] = {}
                    data = stats[summary]
                    level = f'{summary}.'
                else:
                    data = stats
                    level = ''
                if label in data:
                    self._logger.warning(
                        f"Duplicate label found: {level}{label}, overwriting previous values.")
                data[label] = values
                self._logger.debug(f"Found {level}{label} -> {values}")
        return stats

    @staticmethod
    def _get_str_value(data: dict, label: str, required: bool = True, default: str = None) -> Optional[str]:
        value = data.get(label)
        if value:
            value = str(value).strip()
        if value:
            return value
        if required:
            raise ValueError(f"Missing required value: {label}")
        return default

    @staticmethod
    def _get_str_upper_value(data: dict, label: str, required: bool = True, default: str = None) -> Optional[str]:
        value = ModemClientDataGatherer._get_str_value(
            data, label, required, default)
        if value:
            return value.upper()
        return default

    @staticmethod
    def _get_str_lower_value(data: dict, label: str, required: bool = True, default: str = None) -> Optional[str]:
        value = ModemClientDataGatherer._get_str_value(
            data, label, required, default)
        if value:
            return value.lower()
        return default

    @staticmethod
    def _get_int_value(data: dict, label: str, required: bool = True, default: int = None) -> Optional[int]:
        value = ModemClientDataGatherer._get_str_value(data, label, False)
        if value:
            return int(value)
        if required:
            raise ValueError(f"Missing required value: {label}")
        return default

    @staticmethod
    def _get_datetime_value(data: dict, label: str, required: bool = True, default: datetime = None) -> Optional[datetime]:
        value = ModemClientDataGatherer._get_str_value(data, label, False)
        if value:
            if 'T' in value and '-' in value and ':' in value:
                return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
            elif ' ' in value and '/' in value and ':' in value:
                return datetime.strptime(value, "%Y/%m/%d %H:%M:%S")
            else:
                raise ValueError(
                    f"Not datetime converter for {label} with value {value}")
        if required:
            raise ValueError(f"Missing required value: {label}")
        return default

    @staticmethod
    def _get_timedelta_value(data: dict, label: str, required: bool = True, default: timedelta = None) -> Optional[timedelta]:
        value = ModemClientDataGatherer._get_str_value(data, label, False)
        if value:
            split = value.split(':')
            if len(split) <= 4:
                match tuple(map(float, split)):
                    case (days, hours, minutes, seconds):
                        return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
                    case (hours, minutes, seconds):
                        return timedelta(hours=hours, minutes=minutes, seconds=seconds)
                    case (minutes, seconds):
                        return timedelta(minutes=minutes, seconds=seconds)
                    case (seconds,):
                        return timedelta(seconds=seconds)
            raise ValueError(
                f"Not timedelta converter for {label} with value {value}")
        if required:
            raise ValueError(f"Missing required value: {label}")
        return default

    @staticmethod
    def _get_data_array_dict(data: dict, label: str, size: int = 1) -> list[dict]:
        if (not data) or label not in data:
            raise ValueError(f"Missing required value: {label}")
        stats = data[label]
        arr = []
        for k in stats:
            r = stats[k]
            for i in range(0, len(r)):
                if len(arr) <= i:
                    arr.append({})
                arr[i][k] = r[i]
        if len(arr) != size:
            raise ValueError(
                f'Value at label {label} has length {len(arr)} but was expecting {size}')
        return arr
