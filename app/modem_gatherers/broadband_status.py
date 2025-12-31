from typing import TypedDict, Optional

from modem_client import ModemClient
from modem_gatherers import ModemClientDataGatherer


class BroadbandWanInformation(TypedDict):
    connection_source: str
    connection: str
    network_type: str
    ipv4_address: str
    gateway_ipv4_address: str
    mac_address: str
    primary_dns: str
    primary_dns_name: Optional[str]
    secondary_dns: str
    secondary_dns_name: Optional[str]
    mtu: int


class EthernetStatistics(TypedDict):
    line_state: str
    current_speed_mbps: int
    duplex_mode: str


class IPv6Information(TypedDict):
    status: str
    service_type: str
    global_unicast_ipv6_address: str
    link_local_address: str
    default_ipv6_gateway_address: str
    primary_dns: Optional[str]
    secondary_dns: Optional[str]
    mtu: int


class EthernetIPv4Statistics(TypedDict):
    receive_packets: int
    transmit_packets: int
    receive_bytes: int
    transmit_bytes: int
    receive_unicast: int
    transmit_unicast: int
    receive_multicast: int
    transmit_multicast: int
    receive_drops: int
    transmit_drops: int
    receive_errors: int
    transmit_errors: int
    collisions: int


class EthernetIPv6Statistics(TypedDict):
    receive_packets: Optional[int]
    transmit_packets: Optional[int]
    receive_bytes: Optional[int]
    transmit_bytes: Optional[int]
    receive_discards: Optional[int]
    transmit_discards: Optional[int]
    receive_errors: Optional[int]
    transmit_errors: Optional[int]


class BroadbandStatus(TypedDict):
    broadband_wan_information: BroadbandWanInformation
    ethernet_statistics: EthernetStatistics
    ipv6_information: IPv6Information
    ipv4_statistics: EthernetIPv4Statistics
    ipv6_statistics: EthernetIPv6Statistics


class BroadbandStatusGatherer(ModemClientDataGatherer):

    def __init__(self, client: ModemClient):
        super().__init__(client, '/cgi-bin/broadbandstatistics.ha')

    def _map(self, stats: dict) -> Optional[BroadbandStatus]:
        return BroadbandStatus(
            broadband_wan_information=self._map_broadband_wan_information(
                stats),
            ethernet_statistics=self._map_ethernet_statistics(stats),
            ipv6_information=self._map_ipv6_information(stats),
            ipv4_statistics=self._map_ethernet_ipv4_statistics(stats),
            ipv6_statistics=self._map_ethernet_ipv6_statistics(stats)
        )

    def _map_broadband_wan_information(self, stats: dict) -> Optional[BroadbandWanInformation]:
        data = ModemClientDataGatherer._get_data_array_dict(stats, 'Summary of the most important WAN information')[0]
        return BroadbandWanInformation(
            connection_source=ModemClientDataGatherer._get_str_upper_value(
                data, 'Broadband Connection Source'),
            connection=ModemClientDataGatherer._get_str_upper_value(
                data, 'Broadband Connection'),
            network_type=ModemClientDataGatherer._get_str_upper_value(
                data, 'Broadband Network Type'),
            ipv4_address=ModemClientDataGatherer._get_str_lower_value(
                data, 'Broadband IPv4 Address'),
            gateway_ipv4_address=ModemClientDataGatherer._get_str_lower_value(
                data, 'Gateway IPv4 Address'),
            mac_address=ModemClientDataGatherer._get_str_lower_value(
                data, 'MAC Address'),
            primary_dns=ModemClientDataGatherer._get_str_value(
                data, 'Primary DNS'),
            primary_dns_name=ModemClientDataGatherer._get_str_value(
                data, 'Primary DNS Name', False),
            secondary_dns=ModemClientDataGatherer._get_str_value(
                data, 'Secondary DNS'),
            secondary_dns_name=ModemClientDataGatherer._get_str_value(
                data, 'Secondary DNS Name', False),
            mtu=ModemClientDataGatherer._get_int_value(data, 'MTU')
        )

    def _map_ethernet_statistics(self, stats: dict) -> Optional[EthernetStatistics]:
        data = ModemClientDataGatherer._get_data_array_dict(stats, 'Ethernet Statistics Table')[0]
        return EthernetStatistics(
            line_state=ModemClientDataGatherer._get_str_upper_value(
                data, 'Line State'),
            current_speed_mbps=ModemClientDataGatherer._get_int_value(
                data, 'Current Speed (Mbps)'),
            duplex_mode=ModemClientDataGatherer._get_str_upper_value(
                data, 'Current Duplex')
        )

    def _map_ipv6_information(self, stats: dict) -> Optional[IPv6Information]:
        data = ModemClientDataGatherer._get_data_array_dict(stats, 'IPv6 Table')[0]
        return IPv6Information(
            status=ModemClientDataGatherer._get_str_upper_value(
                data, 'Status'),
            service_type=ModemClientDataGatherer._get_str_upper_value(
                data, 'Service Type'),
            global_unicast_ipv6_address=ModemClientDataGatherer._get_str_lower_value(
                data, 'Global Unicast IPv6 Address'),
            link_local_address=ModemClientDataGatherer._get_str_lower_value(
                data, 'Link Local Address'),
            default_ipv6_gateway_address=ModemClientDataGatherer._get_str_lower_value(
                data, 'Default IPv6 Gateway Address'),
            primary_dns=ModemClientDataGatherer._get_str_lower_value(
                data, 'Primary DNS', False),
            secondary_dns=ModemClientDataGatherer._get_str_lower_value(
                data, 'Secondary DNS', False),
            mtu=ModemClientDataGatherer._get_int_value(data, 'MTU'))

    def _map_ethernet_ipv4_statistics(self, stats: dict) -> Optional[EthernetIPv4Statistics]:
        data = ModemClientDataGatherer._get_data_array_dict(stats, 'Ethernet IPv4 Statistics Table')[0]
        return EthernetIPv4Statistics(
            receive_packets=ModemClientDataGatherer._get_int_value(
                data, 'Receive Packets'),
            transmit_packets=ModemClientDataGatherer._get_int_value(
                data, 'Transmit Packets'),
            receive_bytes=ModemClientDataGatherer._get_int_value(
                data, 'Receive Bytes'),
            transmit_bytes=ModemClientDataGatherer._get_int_value(
                data, 'Transmit Bytes'),
            receive_unicast=ModemClientDataGatherer._get_int_value(
                data, 'Receive Unicast'),
            transmit_unicast=ModemClientDataGatherer._get_int_value(
                data, 'Transmit Unicast'),
            receive_multicast=ModemClientDataGatherer._get_int_value(
                data, 'Receive Multicast'),
            transmit_multicast=ModemClientDataGatherer._get_int_value(
                data, 'Transmit Multicast'),
            receive_drops=ModemClientDataGatherer._get_int_value(
                data, 'Receive Drops'),
            transmit_drops=ModemClientDataGatherer._get_int_value(
                data, 'Transmit Drops'),
            receive_errors=ModemClientDataGatherer._get_int_value(
                data, 'Receive Errors'),
            transmit_errors=ModemClientDataGatherer._get_int_value(
                data, 'Transmit Errors'),
            collisions=ModemClientDataGatherer._get_int_value(
                data, 'Collisions')
        )

    def _map_ethernet_ipv6_statistics(self, stats: dict) -> Optional[EthernetIPv6Statistics]:
        data = ModemClientDataGatherer._get_data_array_dict(stats, 'IPv6 Statistics Table')[0]
        return EthernetIPv6Statistics(
            receive_packets=ModemClientDataGatherer._get_int_value(
                data, 'Receive Packets', False),
            transmit_packets=ModemClientDataGatherer._get_int_value(
                data, 'Transmit Packets', False),
            receive_bytes=ModemClientDataGatherer._get_int_value(
                data, 'Receive Bytes', False),
            transmit_bytes=ModemClientDataGatherer._get_int_value(
                data, 'Transmit Bytes', False),
            receive_discards=ModemClientDataGatherer._get_int_value(
                data, 'Receive Discards', False),
            transmit_discards=ModemClientDataGatherer._get_int_value(
                data, 'Transmit Discards', False),
            receive_errors=ModemClientDataGatherer._get_int_value(
                data, 'Receive Errors', False),
            transmit_errors=ModemClientDataGatherer._get_int_value(
                data, 'Transmit Errors', False)
        )
