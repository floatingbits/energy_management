from abc import ABC, abstractmethod
from pathlib import Path

class Client(ABC):

    @abstractmethod
    def export_to_prometheus(
            self
    ) -> None:
        raise NotImplementedError

class ServiceAndFileBasedClientFactory(ABC):
    @abstractmethod
    def create_client(
            self,
            service: str,
            file: Path
    ) -> Client:
        raise NotImplementedError