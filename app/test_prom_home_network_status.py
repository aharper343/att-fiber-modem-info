import logging
from modem_client import ModemClient, ModemConfig
from modem_gatherers.home_network_status import HomeNetworkStatusGatherer
from modem_promtheus_exporters.home_network_status_mapper import HomeNetworkStatusPrometheusMapper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    modem_config = ModemConfig.from_env()
    client = ModemClient(modem_config)
    gatherer = HomeNetworkStatusGatherer(client)
    mapper = HomeNetworkStatusPrometheusMapper(gatherer)
    mapper.refresh()
    mapper.refresh()

