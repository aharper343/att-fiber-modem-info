import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from urllib.parse import urljoin

import uvicorn

from exporters import DataExporter


class ServerConfig:
    hostname: str
    port: int

    def __init__(self, hostname: str, port: int):
        if not hostname:
            raise ValueError("hostname is required")
        if port is None or port < 1 or port > 65535:
            raise ValueError("port must be between 1 and 65535")
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
        self._endpoints = endpoints

    def export(self):
        return self._endpoints

    def get_name(self) -> str:
        return self.__class__.__name__

    def get_export_endpoint(self) -> str:
        return '/endpoints'

    def get_export_endpoint_response_class(self):
        return JSONResponse

class HealthDataExporter(DataExporter):
    def __init__(self, exporters: list[DataExporter]):
        self._exporters = exporters

    def export(self):
        return {
            "status": "UP",
            "exporters": len(self._exporters)
        }

    def get_name(self) -> str:
        return self.__class__.__name__

    def get_export_endpoint(self) -> str:
        return '/health'

    def get_export_endpoint_response_class(self):
        return JSONResponse


class Server:

    def __init__(self, server_config: ServerConfig, exporters: list[DataExporter]):
        self._logger = logging.getLogger(__name__)
        self._server_config = server_config
        self._app = FastAPI()
        self._exporters = exporters.copy()
        endpoints = []
        self._exporters.append(EndpointDataExporter(endpoints))
        self._exporters.append(HealthDataExporter(self._exporters))
        for exporter in self._exporters:
            endpoints.append(self._register_exporter_routes(exporter))

    def start(self) -> None:
        uvicorn.run(self._app, host=self._server_config.hostname, port=self._server_config.port)

    def _register_exporter_routes(self, exporter: DataExporter):
        endpoint = exporter.get_export_endpoint()
        response_class = exporter.get_export_endpoint_response_class()
        media_type = response_class.media_type

        self._logger.info(f"Registering route: {endpoint} {media_type} for exporter: {exporter.get_name()}")
        
        async def exporter_endpoint():
            try:
                data = exporter.export()
                return data
            except Exception as exc:
                self._logger.error(f"Error exporting data from {exporter.get_name()}: {exc}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Error retrieving data: {str(exc)}") from exc
        
        self._app.add_api_route(endpoint, exporter_endpoint, response_class=response_class)

        return RegisteredEndpoint('GET', urljoin(self._server_config.address, endpoint), media_type)



