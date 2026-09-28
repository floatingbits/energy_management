from app.collectors.artifact_crawler import ArtifactCrawlingCollector, PrometheusClientArtifactStrategy
from app.collectors.prometheus.factory import CoverageClientFactory, PytestClientFactory

ARTIFACTS_DIR = "/test-artifacts"

def create_collectors():
    coverage_strategy = PrometheusClientArtifactStrategy(CoverageClientFactory())
    pytest_strategy = PrometheusClientArtifactStrategy(PytestClientFactory())
    return [
        ArtifactCrawlingCollector(ARTIFACTS_DIR, "coverage.xml", coverage_strategy),
        ArtifactCrawlingCollector(ARTIFACTS_DIR, "pytest.xml", pytest_strategy),
    ]