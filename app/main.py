import logging

from modem_promtheus_exporters.home_network_status_mapper import HomeNetworkStatusPrometheusMapper
from modem_promtheus_exporters.system_information_mapper import SystemInformationPrometheusMapper
from modem_promtheus_exporters.broadband_status_mapper import BroadbandStatusPrometheusMapper
from prometheus_client import REGISTRY

from prometheus_exporters import PrometheusExporter
from modem_exporters import ModemDataGathererExporter
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

    registry = REGISTRY
    
    modem_config = ModemConfig.from_env()
    client = ModemClient(modem_config)
    gathers = [SystemInformationGatherer(client), HomeNetworkStatusGatherer(client), BroadbandStatusGatherer(client)]
    cached_gathers = list(map(lambda g: CachingDataGatherer(g), gathers))
    mappers = [ SystemInformationPrometheusMapper(cached_gathers[0], registry), 
                HomeNetworkStatusPrometheusMapper(cached_gathers[1], registry),
                BroadbandStatusPrometheusMapper(cached_gathers[2], registry)]
    exporters = list(map(lambda cg: ModemDataGathererExporter(cg), cached_gathers))
    exporters.append(PrometheusExporter(mappers, registry))        
    server_config = ServerConfig.from_env()
    server = Server(server_config, exporters)
    server.start()


if __name__ == "__main__":
    main()
