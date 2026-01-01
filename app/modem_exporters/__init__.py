from gatherers import CachingDataGatherer
from exporters import DataGathererExporter
from modem_gatherers import ModemClientDataGatherer
from urllib.parse import urljoin, quote

class ModemDataGathererExporter(DataGathererExporter):

    def __init__(self, gatherer: ModemClientDataGatherer):
        super().__init__(gatherer)
        real_gatherer = gatherer
        if isinstance(gatherer, CachingDataGatherer):
            real_gatherer = gatherer.get_gatherer()
        if not isinstance(real_gatherer, ModemClientDataGatherer):
            raise ValueError('Not a subclass')
        self._modem_id = real_gatherer.get_client_config().id

    def get_export_endpoint(self) -> str:
        base = urljoin('/modems/', f'{quote(self._modem_id)}/')
        return urljoin(base, self._normalize_name())

