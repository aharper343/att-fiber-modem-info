import re
from abc import ABC, abstractmethod
from app.gatherers import DataGatherer
from fastapi.responses import JSONResponse
from logging import getLogger

class DataExporter(ABC):

    @abstractmethod
    def export(self):
        pass

    @abstractmethod
    def getName(self) -> str:
        pass

    @abstractmethod
    def getExportEndpoint(self) -> str:
        pass

    @abstractmethod
    def getExportEndpointResponseClass(self):
        pass

class DataGathererExporter(DataExporter):


    def __init__(self, gatherer: DataGatherer):
        self.gatherer = gatherer
        self.name = f'{self.__class__.__name__}({self.gatherer.getName()})'
        self.logger = getLogger(self.name)

    def export(self):
        return self.gatherer.gather()

    def getName(self) -> str:
        return self.name

    def getExportEndpoint(self) -> str:
        return '/api/' + re.sub(r'(?<!^)(?=[A-Z])', '-', self.gatherer.getName()).lower().replace('-gatherer', '')

    def getExportEndpointResponseClass(self):
        return JSONResponse

