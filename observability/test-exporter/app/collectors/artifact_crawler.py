from app.collectors.artifacts import DirectoryArtifactCrawler, CollectedArtifact
from abc import ABC, abstractmethod
from .prometheus.base import Client, ServiceAndFileBasedClientFactory


class ArtifactStrategy(ABC):

    @abstractmethod
    def handle_artifact(
            self,
            artifact: CollectedArtifact
    ) -> None:
        raise NotImplementedError

class PrometheusClientArtifactStrategy(ArtifactStrategy):
    def __init__(self, client_factory: ServiceAndFileBasedClientFactory):
        self.client_factory = client_factory
    def handle_artifact(self, artifact: CollectedArtifact):
        client = self.client_factory.create_client(
            service=artifact.file.parent.name,
            file=artifact.file
        )
        client.export_to_prometheus()

class ArtifactCrawlingCollector:
   # ARTIFACT_NAME = "coverage.xml"

    def __init__(self, artifacts_dir: str, artifact_name: str, artifact_strategy: ArtifactStrategy):
        self._crawler = DirectoryArtifactCrawler(artifacts_dir)
        self.artifact_name = artifact_name
        self.artifact_strategy = artifact_strategy

    def collect(self) -> None:
        for artifact in self._crawler.collect(self.artifact_name):
            self.artifact_strategy.handle_artifact(artifact)



