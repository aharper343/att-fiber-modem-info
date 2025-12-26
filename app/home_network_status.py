
from app.modem_gatherers import ModemClientDataGatherer
from app.modem_client import ModemClient
from typing import TypedDict

class PortLanStatistics(TypedDict):
    port: int
    state: str
    transmit_speed: int
    transmit_packets: int
    transmit_bytes: int
    transmit_unicast: int
    transmit_multicast: int
    transmit_dropped: int
    transmit_errors: int
    receive_packets: int
    receive_bytes: int
    receive_unicast: int
    receive_multicast: int
    receive_dropped: int
    receive_errors: int

class LanStatistics(TypedDict):
    lan_statistics: list[PortLanStatistics]

class HomeNetworkStatusGatherer(ModemClientDataGatherer):

    def __init__(self, client: ModemClient):
        super().__init__(client, '/cgi-bin/lanstatistics.ha')

    def _map(self, stats: dict) -> LanStatistics:
        if not stats:
            return None
        stats = stats.get('LAN Ethernet Statistics Table', {})
        if not stats:
            return None
        lan_stats_list = []
        for port in range(len(stats.get('State', []))):
            lan_stats_list.append(PortLanStatistics(
                port=port + 1,
                state=self._to_upper(stats.get('State', [])[port]),
                transmit_speed=self._to_int(stats.get('Transmit Speed', [])[port]),
                transmit_packets=self._to_int(stats.get('Transmit Packets', [])[port]),
                transmit_bytes=self._to_int(stats.get('Transmit Bytes', [])[port]),
                transmit_unicast=self._to_int(stats.get('Transmit Unicast', [])[port]),
                transmit_multicast=self._to_int(stats.get('Transmit Multicast', [])[port]),
                transmit_dropped=self._to_int(stats.get('Transmit Dropped', [])[port]),
                transmit_errors=self._to_int(stats.get('Transmit Errors', [])[port]),
                receive_packets=self._to_int(stats.get('Receive Packets', [])[port]),
                receive_bytes=self._to_int(stats.get('Receive Bytes', [])[port]),
                receive_unicast=self._to_int(stats.get('Receive Unicast', [])[port]),
                receive_multicast=self._to_int(stats.get('Receive Multicast', [])[port]),
                receive_dropped=self._to_int(stats.get('Receive Dropped', [])[port]),
                receive_errors=self._to_int(stats.get('Receive Errors', [])[port])
            ))
        return LanStatistics(lan_statistics=lan_stats_list)
