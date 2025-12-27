from typing import TypedDict, Optional

from modem_client import ModemClient
from modem_gatherers import ModemClientDataGatherer


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


class HomeNetworkStatusGatherer(ModemClientDataGatherer):

    def __init__(self, client: ModemClient):
        super().__init__(client, '/cgi-bin/lanstatistics.ha')

    def _map(self, stats: dict) -> Optional[list[PortLanStatistics]]:
        if not stats:
            return None
        stats = stats.get('LAN Ethernet Statistics Table', {})
        if not stats:
            return None
        lan_stats_list = []
        state_list = stats.get('State', [])
        num_ports = len(state_list)
        if num_ports == 0:
            return lan_stats_list

        # Get all required lists and verify they have the same length
        required_fields = [
            'Transmit Speed', 'Transmit Packets', 'Transmit Bytes', 'Transmit Unicast',
            'Transmit Multicast', 'Transmit Dropped', 'Transmit Errors',
            'Receive Packets', 'Receive Bytes', 'Receive Unicast', 'Receive Multicast',
            'Receive Dropped', 'Receive Errors'
        ]

        # Verify all lists have the same length
        for field in required_fields:
            field_list = stats.get(field, [])
            if len(field_list) != num_ports:
                self.logger.warning(f"Field '{field}' has length {len(field_list)}, expected {num_ports}. Skipping port statistics.")
                return lan_stats_list

        for port in range(num_ports):
            lan_stats_list.append(PortLanStatistics(
                port=port + 1,
                state=self._to_upper(state_list[port]),
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
        return lan_stats_list
