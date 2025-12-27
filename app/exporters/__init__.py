import re
from abc import ABC, abstractmethod
from logging import getLogger

from fastapi.responses import JSONResponse

from gatherers import DataGatherer


class DataExporter(ABC):

    @abstractmethod
    def export(self):
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_export_endpoint(self) -> str:
        pass

    @abstractmethod
    def get_export_endpoint_response_class(self):
        pass


class DataGathererExporter(DataExporter):

    def __init__(self, gatherer: DataGatherer):
        self.gatherer = gatherer
        self.name = f'{self.__class__.__name__}({self.gatherer.get_name()})'
        self.logger = getLogger(self.name)

    def export(self):
        return self.gatherer.gather()

    def get_name(self) -> str:
        return self.name

    def get_export_endpoint(self) -> str:
        return '/api/' + re.sub(r'(?<!^)(?=[A-Z])', '-', self.gatherer.get_name()).lower().replace('-gatherer', '')

    def get_export_endpoint_response_class(self):
        return JSONResponse

