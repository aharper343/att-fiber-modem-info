import logging
from app.server import Server, ServerConfig
from app.modem_client import ModemConfig, ModemClient
from app.home_network_status import HomeNetworkStatusGatherer
from app.system_information import SystemInformationGatherer
from app.broadband_status import BroadbandStatusGatherer
from app.gatherers import CachingDataGatherer
from app.exporters import DataGathererExporter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    # Start Prometheus metrics server
    modem_config = ModemConfig.from_env()
    client = ModemClient(modem_config)
    gathers = [SystemInformationGatherer(client), BroadbandStatusGatherer(client), HomeNetworkStatusGatherer(client)]
    cached_gathers = map(lambda g: CachingDataGatherer(g), gathers)

    exporters = map(lambda g: DataGathererExporter(g), gathers)

    server_config = ServerConfig.from_env()
    server = Server(server_config, exporters)
    server.start()


if __name__ == "__main__":
    main()
