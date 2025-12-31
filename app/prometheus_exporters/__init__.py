import logging
from abc import ABC, abstractmethod

from fastapi.responses import PlainTextResponse
from prometheus_client import REGISTRY, CollectorRegistry, generate_latest
from gatherers import DataGatherer
from exporters import DataExporter


class PrometheusMapper(ABC):

    def __init__(self, gatherer: DataGatherer, registry: CollectorRegistry):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._gatherer = gatherer
        self._registry = registry

    def refresh(self) -> None:
        data = self._gatherer.gather()
        self._map(data)

    @abstractmethod
    def _map(self, data) -> None:
        pass

class PrometheusExporter(DataExporter):

    def __init__(self, mappers: list[PrometheusMapper] = [], registry: CollectorRegistry = REGISTRY):
        self._name = self.__class__.__name__
        self._logger = logging.getLogger(self._name)
        self._mappers = mappers
        self._registry = registry

    def export(self):
        for m in self._mappers:
            m.refresh()
        res = generate_latest(self._registry)
        return res

    def get_name(self) -> str:
        return self._name

    def get_export_endpoint(self) -> str:
        return '/metrics'

    def get_export_endpoint_response_class(self):
        return PlainTextResponse

