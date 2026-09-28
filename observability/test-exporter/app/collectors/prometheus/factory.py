from pathlib import Path

from app.collectors.prometheus.base import ServiceAndFileBasedClientFactory, Client
from .coverage import CoverageClient
from .pytest import PytestClient
class CoverageClientFactory(ServiceAndFileBasedClientFactory):
    def create_client(
            self,
            service: str,
            file: Path
    ) -> Client:
        return CoverageClient(service, file)

class PytestClientFactory(ServiceAndFileBasedClientFactory):
    def create_client(
            self,
            service: str,
            file: Path
    ) -> Client:
        return PytestClient(service, file)
