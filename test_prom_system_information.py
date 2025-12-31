import logging
from modem_client import ModemClient, ModemConfig
from modem_gatherers.system_information import SystemInformationGatherer
from modem_promtheus_exporters.system_information_mapper import SystemInformationPrometheusMapper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    modem_config = ModemConfig.from_env()
    client = ModemClient(modem_config)
    gatherer = SystemInformationGatherer(client)
    mapper = SystemInformationPrometheusMapper(gatherer)
    mapper.refresh()

