from prometheus_client import CollectorRegistry
from modem_gatherers.broadband_status import BroadbandStatus, EthernetIPv4Statistics, BroadbandStatusGatherer
from modem_promtheus_exporters import PrometheusModemMapper

class BroadbandStatusPrometheusMapper(PrometheusModemMapper):

    def __init__(self, gatherer: BroadbandStatusGatherer, registry: CollectorRegistry) -> None:
        super().__init__(gatherer, registry)

    def _map(self, data: BroadbandStatus) -> None:
        labels = self.get_common_labels()
        label_values = self.get_common_label_values()
        self._map_part('wan_ipv4', data['ipv4_statistics'], labels, label_values)
        self._map_part('wan_ipv6', data['ipv6_statistics'], labels, label_values)

    def _map_part(self, prefix: str, data: any, labels: list[str], label_values: list[str]) -> None:
        for k in data:
            v = data[k]
            if v is None:
                self._logger.warning('Skipping key with no value %s.%s', prefix, k)
            else:
                self._get_or_create_gauge(f'{prefix}_{k}', labels).labels(*label_values).set(v)
