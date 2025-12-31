from datetime import datetime, timedelta
from typing import TypedDict, Optional

from modem_client import ModemClient
from modem_gatherers import ModemClientDataGatherer


class SystemInformation(TypedDict):
    manufacturer: str
    model_number: str
    serial_number: str
    software_version: str
    mac_address: str
    first_use_date: datetime
    time_since_last_reboot: timedelta
    current_date_time: datetime
    datapump_version: str
    hardware_version: str


class SystemInformationGatherer(ModemClientDataGatherer):

    def __init__(self, client: ModemClient):
        super().__init__(client, '/cgi-bin/sysinfo.ha')

    def _map(self, stats: dict) -> Optional[SystemInformation]:
        if not stats:
            return None
        data = ModemClientDataGatherer._get_data_array_dict(
            stats, 'This table includes system information about the device and its software')[0]
        return SystemInformation(
            manufacturer=ModemClientDataGatherer._get_str_value(
                data, "Manufacturer"),
            model_number=ModemClientDataGatherer._get_str_value(
                data, "Model Number"),
            serial_number=ModemClientDataGatherer._get_str_value(
                data, "Serial Number"),
            software_version=ModemClientDataGatherer._get_str_value(
                data, "Software Version"),
            mac_address=ModemClientDataGatherer._get_str_value(
                data, "MAC Address"),
            first_use_date=ModemClientDataGatherer._get_datetime_value(
                data, "First Use Date"),
            time_since_last_reboot=ModemClientDataGatherer._get_timedelta_value(
                data, "Time Since Last Reboot"),
            current_date_time=ModemClientDataGatherer._get_datetime_value(
                data, "Current Date/Time"),
            datapump_version=ModemClientDataGatherer._get_str_value(
                data, "Datapump Version"),
            hardware_version=ModemClientDataGatherer._get_str_value(
                data, "Hardware Version")
        )
