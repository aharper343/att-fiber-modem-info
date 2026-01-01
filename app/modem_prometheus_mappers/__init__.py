from gatherers import CachingDataGatherer
from modem_gatherers import ModemClientDataGatherer
from prometheus_exporters import PrometheusMapper
from prometheus_client import REGISTRY, CollectorRegistry, Gauge


class PrometheusModemMapper(PrometheusMapper):

    def __init__(self, gatherer: ModemClientDataGatherer, registry: CollectorRegistry):
        super().__init__(gatherer, registry)
        if isinstance(gatherer, CachingDataGatherer):
            real_gatherer = gatherer.get_gatherer()
        else:
            real_gatherer = gatherer
        if not isinstance(real_gatherer, ModemClientDataGatherer):
            raise ValueError(f'gatherer should be a sub-class of ModemClientDataGatherer and is type {type(gatherer)}')
        self._config = real_gatherer.get_client_config()

    def _get_or_create_gauge(self, name: str, labels: list[str]) -> Gauge:
        metric_name = self.get_metric_name(name)
        metric = self.get_registry()._names_to_collectors.get(metric_name, None)
        if metric:
            if isinstance(metric, Gauge):
                # TODO check labels
                return metric
            else:
                raise ValueError(f"Trying to create a Gauge {metric_name}, a metric is already registered with type {type(metric)}")
        if not metric:
            gauge = self._create_gauge(name, labels)
        return gauge

    def _create_gauge(self, name: str, labels: list[str]) -> Gauge:
        metric_name = self.get_metric_name(name)
        metric_desc = self.get_metric_description(name)
        self._logger.debug("Creating Gauge('%s','%s',%s)", metric_name, metric_desc, labels)
        return Gauge(metric_name, metric_desc, labels, registry=self.get_registry())

    def get_registry(self) -> CollectorRegistry:
        return self._registry

    def get_metric_name(self, name) -> str:
        return f"att_modem_{name}"

    def get_metric_description(self, name) -> str:
        return f"AT&T Modem {name.replace('_', ' ')}"

    def get_common_labels(self) -> list[str]:
        return ['modem_id', 'modem_url']

    def get_common_label_values(self) -> list[str]:
        return [ self._config.id, self._config.url ]
