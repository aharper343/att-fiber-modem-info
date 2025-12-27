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
    primary_dns_name: str
    secondary_dns: str
    secondary_dns_name: str
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
    primary_dns: str
    secondary_dns: str
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
    receive_packets: int
    transmit_packets: int
    receive_bytes: int
    transmit_bytes: int
    receive_discards: int
    transmit_discards: int
    receive_errors: int
    transmit_errors: int


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
        if not stats:
            return None
        return BroadbandStatus(
            broadband_wan_information=self._map_broadband_wan_information(stats.get('Summary of the most important WAN information', {})),
            ethernet_statistics=self._map_ethernet_statistics(stats.get('Ethernet Statistics Table', {})),
            ipv6_information=self._map_ipv6_information(stats.get('IPv6 Table', {})),
            ipv4_statistics=self._map_ethernet_ipv4_statistics(stats.get('Ethernet IPv4 Statistics Table', {})),
            ipv6_statistics=self._map_ethernet_ipv6_statistics(stats.get('IPv6 Statistics Table', {}))
        )

    def _map_broadband_wan_information(self, stats: dict) -> Optional[BroadbandWanInformation]:
        if not stats:
            return None
        return BroadbandWanInformation(
            connection_source=self._to_upper(stats.get("Broadband Connection Source", [""])[0]),
            connection=self._to_upper(stats.get("Broadband Connection", [""])[0]),
            network_type=self._to_upper(stats.get("Broadband Network Type", [""])[0]),
            ipv4_address=self._to_str(stats.get("Broadband IPv4 Address", [""])[0]),
            gateway_ipv4_address=self._to_str(stats.get("Gateway IPv4 Address", [""])[0]),
            mac_address=self._to_lower(stats.get("MAC Address", [""])[0]),
            primary_dns=self._to_str(stats.get("Primary DNS", [""])[0]),
            primary_dns_name=self._to_str(stats.get("Primary DNS Name", [""])[0]),
            secondary_dns=self._to_str(stats.get("Secondary DNS", [""])[0]),
            secondary_dns_name=self._to_str(stats.get("Secondary DNS Name", [""])[0]),
            mtu=self._to_int(stats.get("MTU", [""])[0])
        )

    def _map_ethernet_statistics(self, stats: dict) -> Optional[EthernetStatistics]:
        if not stats:
            return None
        return EthernetStatistics(
            line_state=self._to_upper(stats.get("Line State", [""])[0]),
            current_speed_mbps=self._to_int(stats.get("Current Speed (Mbps)", [""])[0]),
            duplex_mode=self._to_upper(stats.get("Current Duplex", [""])[0])
        )

    def _map_ipv6_information(self, stats: dict) -> Optional[IPv6Information]:
        if not stats:
            return None
        return IPv6Information(
             status=self._to_upper(stats.get("Status", [""])[0]),
             service_type=self._to_upper(stats.get("Service Type", [""])[0]),
             global_unicast_ipv6_address=self._to_str(stats.get("Global Unicast IPv6 Address", [""])[0]),
             link_local_address=self._to_str(stats.get("Link Local Address", [""])[0]),
             default_ipv6_gateway_address=self._to_str(stats.get("Default IPv6 Gateway Address", [""])[0]),
             primary_dns=self._to_str(stats.get("Primary DNS", [""])[0]),
             secondary_dns=self._to_str(stats.get("Secondary DNS", [""])[0]),
             mtu=self._to_int(stats.get("MTU", [""])[0])
        )

    def _map_ethernet_ipv4_statistics(self, stats: dict) -> Optional[EthernetIPv4Statistics]:
        if not stats:
            return None
        return EthernetIPv4Statistics(
            receive_packets=self._to_int(stats.get("Receive Packets", [""])[0]),
            transmit_packets=self._to_int(stats.get("Transmit Packets", [""])[0]),
            receive_bytes=self._to_int(stats.get("Receive Bytes", [""])[0]),
            transmit_bytes=self._to_int(stats.get("Transmit Bytes", [""])[0]),
            receive_unicast=self._to_int(stats.get("Receive Unicast", [""])[0]),
            transmit_unicast=self._to_int(stats.get("Transmit Unicast", [""])[0]),
            receive_multicast=self._to_int(stats.get("Receive Multicast", [""])[0]),
            transmit_multicast=self._to_int(stats.get("Transmit Multicast", [""])[0]),
            receive_drops=self._to_int(stats.get("Receive Drops", [""])[0]),
            transmit_drops=self._to_int(stats.get("Transmit Drops", [""])[0]),
            receive_errors=self._to_int(stats.get("Receive Errors", [""])[0]),
            transmit_errors=self._to_int(stats.get("Transmit Errors", [""])[0]),
            collisions=self._to_int(stats.get("Collisions", [""])[0])
        )

    def _map_ethernet_ipv6_statistics(self, stats: dict) -> Optional[EthernetIPv6Statistics]:
        if not stats:
            return None
        return EthernetIPv6Statistics(
            receive_packets=self._to_int(stats.get("Receive Packets", [""])[0]),
            transmit_packets=self._to_int(stats.get("Transmit Packets", [""])[0]),
            receive_bytes=self._to_int(stats.get("Receive Bytes", [""])[0]),
            transmit_bytes=self._to_int(stats.get("Transmit Bytes", [""])[0]),
            receive_discards=self._to_int(stats.get("Receive Discards", [""])[0]),
            transmit_discards=self._to_int(stats.get("Transmit Discards", [""])[0]),
            receive_errors=self._to_int(stats.get("Receive Errors", [""])[0]),
            transmit_errors=self._to_int(stats.get("Transmit Errors", [""])[0])
        )
