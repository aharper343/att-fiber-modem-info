import logging
import os

from prometheus_client import make_asgi_app, make_wsgi_app
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from urllib.parse import urljoin

import uvicorn

from exporters import DataExporter


class ServerConfig:
    hostname: str
    port: int

    def __init__(self, hostname: str, port: int):
        self.hostname = hostname
        self.port = port
        self.address = f"http://{hostname}:{port}"

    @staticmethod
    def from_env():
        hostname = os.getenv('SERVER_HOSTNAME', '0.0.0.0').strip()
        port = int(os.getenv('SERVER_PORT', '8666').strip())
        return ServerConfig(hostname, port)


class RegisteredEndpoint:
    method: str
    uri: str
    media_type: str

    def __init__(self, method, uri, media_type):
        self.method = method
        self.uri = uri
        self.media_type = media_type

class EndpointDataExporter(DataExporter):

    def __init__(self, endpoints: list[RegisteredEndpoint]):
        self.endpoints = endpoints

    def export(self):
        return self.endpoints

    def get_name(self) -> str:
        return self.__class__.__name__

    def get_export_endpoint(self) -> str:
        return '/endpoints'

    def get_export_endpoint_response_class(self):
        return JSONResponse

class HealthDataExporter(DataExporter):
    def __init__(self, exporters: list[DataExporter]):
        self.exporters = exporters

    def export(self):
        return {
            "status": "UP",
            "exporters": len(self.exporters)
        }

    def get_name(self) -> str:
        return self.__class__.__name__

    def get_export_endpoint(self) -> str:
        return '/health'

    def get_export_endpoint_response_class(self):
        return JSONResponse


class Server:

    def __init__(self, server_config: ServerConfig, exporters: list[DataExporter]):
        self.logger = logging.getLogger(__name__)
        self.server_config = server_config
        self.app = FastAPI()
        self.exporters = exporters.copy()
        endpoints = []
        self.exporters.append(EndpointDataExporter(endpoints))
        self.exporters.append(HealthDataExporter(self.exporters))
        for exporter in self.exporters:
            endpoints.append(self._register_exporter_routes(exporter))

    def start(self) -> None:
        uvicorn.run(self.app, host=self.server_config.hostname, port=self.server_config.port)

    def _register_exporter_routes(self, exporter: DataExporter):
        endpoint = exporter.get_export_endpoint()
        response_class = exporter.get_export_endpoint_response_class()
        media_type = response_class.media_type

        self.logger.info(f"Registering route: {endpoint} {media_type} for exporter: {exporter.get_name()}")
        make_asgi_app
# async
        async def exporter_endpoint():
            try:
                data = exporter.export()
                return data
            except Exception as exc:
                self.logger.error(f"Error exporting data from {e.get_name()}: {exc}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Error retrieving data: {str(exc)}") from exc
        
        self.app.add_api_route(endpoint, exporter_endpoint, response_class=response_class)

        return RegisteredEndpoint('GET', urljoin(self.server_config.address, endpoint), media_type)



