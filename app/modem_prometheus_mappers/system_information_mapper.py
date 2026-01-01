from modem_gatherers.system_information import SystemInformationGatherer, SystemInformation
from modem_prometheus_mappers import PrometheusModemMapper
from prometheus_client import REGISTRY, CollectorRegistry

class SystemInformationPrometheusMapper(PrometheusModemMapper):

    def __init__(self, gatherer: SystemInformationGatherer, registry: CollectorRegistry) -> None:
        super().__init__(gatherer, registry)

    def _map(self, data: SystemInformation) -> None:
        labels = self.get_common_labels() + [
            'manufacturer',
            'model_number',
            'serial_number',
            'mac_address'
        ]
        gauge = self._get_or_create_gauge('uptime_seconds', labels)
        label_values =  self.get_common_label_values() + [
            data['manufacturer'],
            data['model_number'],
            data['serial_number'],
            data['mac_address']
        ]
        value = data['time_since_last_reboot'].total_seconds()
        gauge.labels(*label_values).set(value)
