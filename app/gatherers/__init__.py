from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from logging import getLogger
from cachetools import TTLCache, cached

class DataGatherer(ABC):

    @abstractmethod
    def gather(self):
        pass

    def get_name(self) -> str:
        return self.__class__.__name__


class CachingDataGatherer(DataGatherer):

    def __init__(self, gatherer: DataGatherer, cache_duration: timedelta = timedelta(minutes=5)):
        self._gatherer = gatherer
        self._cache = TTLCache(maxsize=1, ttl=cache_duration.seconds)
        self._logger = getLogger(self.__class__.__name__)
        self._logger.info("Initialized CachingDataGatherer with cache_duration=%s", cache_duration)

    def gather(self):
        key = self.get_name()
        value = self._cache.get(key, None)
        if not value:
            self._logger.info('Cache expired for gatherer %s', key)
            value = self._gatherer.gather()
            self._cache[key] = value
        else:
            self._logger.info('Using cached value for gatherer %s', key)
        return value

    def get_name(self) -> str:
        return self._gatherer.get_name()

    def get_gatherer(self) -> DataGatherer:
        return self._gatherer
                
