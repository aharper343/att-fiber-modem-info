import logging
import re
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from logging import getLogger


class DataGatherer(ABC):

    @abstractmethod
    def gather(self):
        pass

    def get_name(self) -> str:
        return self.__class__.__name__


class CachingDataGatherer(DataGatherer):

    def __init__(self, gatherer: DataGatherer, cache_duration: timedelta = timedelta(minutes=5)):
        self.gatherer = gatherer
        self.cache_duration = cache_duration
        self.logger = getLogger(self.__class__.__name__)
        self.cache = None
        self.last_update = None

    def gather(self):
        if self.cache is None or (self.last_update is not None and datetime.now() - self.last_update > self.cache_duration):
            self.logger.info("Cache expired or empty, gathering new data.")
            self.cache = self.gatherer.gather()
            self.last_update = datetime.now()
        else:
            self.logger.info("Returning cached data.")
        return self.cache

    def get_name(self) -> str:
        return self.gatherer.get_name()

