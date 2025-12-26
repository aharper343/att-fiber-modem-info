import logging
from abc import abstractmethod
from bs4 import BeautifulSoup
from logging import getLogger
from datetime import timedelta
from datetime import datetime
from app.gatherers import DataGatherer
from app.modem_client import ModemClient



class ModemClientDataGatherer(DataGatherer):

    def __init__(self, client: ModemClient, uri: str, requires_login: bool = False):
        self.client = client
        self.uri = uri
        self.requires_login = requires_login
        self.logger = getLogger(self.__class__.__name__)

    def gather(self):
        response = self.client._fetch(self.uri)
        stats = self._parse_html(response.text)
        if not stats:
            self.logger.warning("No stats found.")
            return None
        data = self._map(stats)
        self.logger.info(f"Data -> {data}")
        return data

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
            self.logger.debug(f"Parsing table with summary: {summary}")
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
                if label in stats:
                    self.logger.warning(f"Duplicate label found: {level}{label}, overwriting previous values.")
                data[label] = values
                self.logger.debug(f"Found {level}{label} -> {values}")
        return stats
    
    def _to_int(self, value: str) -> int:
        if not value:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0
        
    def _to_str(self, value: str) -> str:
        if not value:
            return None
        return str(value).strip()
    
    def _to_lower(self, value: str) -> str:
        if not value:
            return None
        return str(value).lower().strip()

    def _to_upper(self, value: str) -> str:
        if not value:
            return None
        return str(value).upper().strip()
    
    def _to_datetime(self, value: str):
        value = self._to_str(value)
        if not value:
            return None
        if 'T' in value and '-' in value and ':' in value:
            try:
                return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                logger.warning(f"Unable to parse datetime from value: {value}")
                return None
        elif ' ' in value and '/' in value and ':' in value:
            try:
                return datetime.strptime(value, "%Y/%m/%d %H:%M:%S")
            except ValueError:
                logger.warning(f"Unable to parse datetime from value: {value}")
                return None
        logger.warning(f"Unable to parse datetime from value: {value}")
        return None
    
        
    def _to_timedelta(self, value: str) -> timedelta:
        if not value:
            return None
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
        logger.warning(f"Unable to parse timedelta from value: {value}")
        return None
