from gatherers import CachingDataGatherer
from exporters import DataGathererExporter
from modem_gatherers import ModemClientDataGatherer
from urllib.parse import urljoin, quote

class ModemDataGathererExporter(DataGathererExporter):

    def __init__(self, gatherer: ModemClientDataGatherer):
        super().__init__(gatherer)
        real_gatherer = gatherer
        if issubclass(gatherer.__class__, CachingDataGatherer):
            real_gatherer = gatherer.get_gatherer()
        if not issubclass(real_gatherer.__class__, ModemClientDataGatherer):
            raise ValueError('Not a subclass')
        self.modem_id = real_gatherer.get_client_config().id

    def get_export_endpoint(self) -> str:
        base = urljoin('/modems/', f'{quote(self.modem_id)}/')
        return urljoin(base, self._normalize_name())

