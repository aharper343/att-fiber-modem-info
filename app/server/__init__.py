import logging
import os

import uvicorn
from fastapi import FastAPI

from exporters import DataExporter


class ServerConfig:
    hostname: str
    port: int

    def __init__(self, hostname: str, port: int):
        self.hostname = hostname
        self.port = port

    @staticmethod
    def from_env():
        hostname = os.getenv('SERVER_HOSTNAME', 'localhost').strip()
        port = int(os.getenv('SERVER_PORT', '8666').strip())
        return ServerConfig(hostname, port)


class Server:

    class RegisteredEndpoint:
        method: str
        uri: str
        media_type: str

        def __init__(self, method, uri, media_type):
            self.method = method
            self.uri = uri
            self.media_type = media_type

    def __init__(self, server_config: ServerConfig, exporters: list[DataExporter]):
        self.logger = logging.getLogger(__name__)
        self.server_config = server_config
        self.app = FastAPI()
        self.exporters = exporters
        endpoints = []
        for exporter in exporters:
            endpoints.append(self._register_exporter_routes(exporter))
        async def registered_endpoint():
            return endpoints
        self.app.add_api_route('/endpoints', registered_endpoint)

    def start(self) -> None:
        uvicorn.run(self.app, host=self.server_config.hostname, port=self.server_config.port)

    def _register_exporter_routes(self, exporter: DataExporter):
        endpoint = exporter.get_export_endpoint()
        response_class = exporter.get_export_endpoint_response_class()
        media_type = response_class.media_type

        self.logger.info(f"Registering route: {endpoint} {media_type} for exporter: {exporter.get_name()}")

        async def exporter_endpoint(e=exporter):
            data = e.export()
            return data

        self.app.add_api_route(endpoint, exporter_endpoint, response_class=response_class)

        return self.RegisteredEndpoint('GET', endpoint, media_type)
