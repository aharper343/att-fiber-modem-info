from app.modem_gatherers import ModemClientDataGatherer
from app.modem_client import ModemClient
from typing import TypedDict
from datetime import datetime
from datetime import timedelta

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

    def _map(self, stats: dict) ->SystemInformation:
        if not stats:
            return None
        stats = stats.get('This table includes system information about the device and its software', {})
        if not stats:
            return None
        return SystemInformation(
            manufacturer=self._to_str(stats.get("Manufacturer", [""])[0]),
            model_number=self._to_str(stats.get("Model Number", [""])[0]),
            serial_number=self._to_str(stats.get("Serial Number", [""])[0]),
            software_version=self._to_str(stats.get("Software Version", [""])[0]),
            mac_address=self._to_str(stats.get("MAC Address", [""])[0]),
            first_use_date=self._to_datetime(stats.get("First Use Date", [""])[0]),
            time_since_last_reboot=self._to_timedelta(stats.get("Time Since Last Reboot", [""])[0]),
            current_date_time=self._to_datetime(stats.get("Current Date/Time", [""])[0]),
            datapump_version=self._to_str(stats.get("Datapump Version", [""])[0]),
            hardware_version=self._to_str(stats.get("Hardware Version", [""])[0])
        )
