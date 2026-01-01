from prometheus_client import CollectorRegistry
from modem_gatherers.home_network_status import HomeNetworkStatusGatherer, PortLanStatistics
from modem_prometheus_mappers import PrometheusModemMapper

class HomeNetworkStatusPrometheusMapper(PrometheusModemMapper):

    def __init__(self, gatherer: HomeNetworkStatusGatherer, registry: CollectorRegistry) -> None:
        super().__init__(gatherer, registry)

    def _map(self, data: list[PortLanStatistics]) -> None:
        labels = self.get_common_labels() + [ 'lan_port' ]
        for port in range(0, len(data)):
            label_values = self.get_common_label_values() + [ data[port]['lan_port'] ]
            for k in data[port]:
                v = data[port][k]
                if k == 'lan_port':
                    continue
                elif k == 'state':
                    if v == 'UP':
                        v = 1
                    else:
                        v = 0
                self._get_or_create_gauge(f'lan_{k}', labels).labels(*label_values).set(v)

