from typing import TypedDict, Optional

from modem_client import ModemClient
from modem_gatherers import ModemClientDataGatherer


class PortLanStatistics(TypedDict):
    lan_port: int
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
        num_ports = 4
        data = ModemClientDataGatherer._get_data_array_dict(
            stats, 'LAN Ethernet Statistics Table', num_ports)
        lan_stats_list = []
        for port in range(num_ports):
            port_data = data[port]
            lan_stats_list.append(PortLanStatistics(
                lan_port=port,
                state=ModemClientDataGatherer._get_str_upper_value(
                    port_data, 'State'),
                transmit_speed=ModemClientDataGatherer._get_int_value(
                    port_data, 'Transmit Speed'),
                transmit_packets=ModemClientDataGatherer._get_int_value(
                    port_data, 'Transmit Packets'),
                transmit_bytes=ModemClientDataGatherer._get_int_value(
                    port_data, 'Transmit Bytes'),
                transmit_unicast=ModemClientDataGatherer._get_int_value(
                    port_data, 'Transmit Unicast'),
                transmit_multicast=ModemClientDataGatherer._get_int_value(
                    port_data, 'Transmit Multicast'),
                transmit_dropped=ModemClientDataGatherer._get_int_value(
                    port_data, 'Transmit Dropped'),
                transmit_errors=ModemClientDataGatherer._get_int_value(
                    port_data, 'Transmit Errors'),
                receive_packets=ModemClientDataGatherer._get_int_value(
                    port_data, 'Receive Packets'),
                receive_bytes=ModemClientDataGatherer._get_int_value(
                    port_data, 'Receive Bytes'),
                receive_unicast=ModemClientDataGatherer._get_int_value(
                    port_data, 'Receive Unicast'),
                receive_multicast=ModemClientDataGatherer._get_int_value(
                    port_data, 'Receive Multicast'),
                receive_dropped=ModemClientDataGatherer._get_int_value(
                    port_data, 'Receive Dropped'),
                receive_errors=ModemClientDataGatherer._get_int_value(
                    port_data, 'Receive Errors')
            ))
        return lan_stats_list
