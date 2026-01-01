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
        self._gatherer = gatherer
        self._name = f'{self.__class__.__name__}({self._gatherer.get_name()})'
        self._logger = getLogger(self._name)

    def export(self):
        value = self._gatherer.gather()
        if type(value) is list:
            return [v._asdict() if hasattr(v, '_asdict') else v for v in value]
        elif hasattr(value, '_asdict'):
            return value._asdict()
        return value

    def get_name(self) -> str:
        return self._name

    def get_export_endpoint(self) -> str:
        return '/gatherer/' + self._normalize_name()

    def get_export_endpoint_response_class(self):
        return JSONResponse

    def _normalize_name(self) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '-', self._gatherer.get_name()).lower().replace('-gatherer', '')

