import logging

from exporters import DataGathererExporter
from gatherers import CachingDataGatherer
from modem_client import ModemClient, ModemConfig
from modem_gatherers.broadband_status import BroadbandStatusGatherer
from modem_gatherers.home_network_status import HomeNetworkStatusGatherer
from modem_gatherers.system_information import SystemInformationGatherer
from server import Server, ServerConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main():
    # Start Prometheus metrics server
    modem_config = ModemConfig.from_env()
    client = ModemClient(modem_config)
    gathers = [SystemInformationGatherer(client), BroadbandStatusGatherer(client), HomeNetworkStatusGatherer(client)]
    cached_gathers = map(lambda g: CachingDataGatherer(g), gathers)
    exporters = list(map(lambda g: DataGathererExporter(g), cached_gathers))
    server_config = ServerConfig.from_env()
    server = Server(server_config, exporters)
    server.start()


if __name__ == "__main__":
    main()
