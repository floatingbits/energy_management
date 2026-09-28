from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

"""Artifacts are files that test runs write as results, e.g. coverage.xml or
pytest.xml. They are organized in one directory per service within the shared
test artifacts volume:

    /test-artifacts/<service>/<artifact-file>

The collection strategy is composed of two steps:

1. A service-agnostic directory crawler that searches the artifacts directory
   for files and reports in which directory each found file lives.
2. A by-service collection strategy (the collectors) that assigns a service
   name to a file it has collected. It knows that the directory name from the
   naive directory crawler is the service name.
"""


@dataclass
class CollectedArtifact:
    """One artifact file """
    file: Path


class DirectoryArtifactCrawler:
    """Service-agnostic crawler that searches service directories for files."""

    def __init__(self, artifacts_dir: str | Path):
        self.artifacts_dir = Path(artifacts_dir)

    def collect(self, artifact_name: str) -> Iterator[CollectedArtifact]:
        for directory in self._directories():
            artifact_file = directory / artifact_name

            if artifact_file.is_file():
                yield CollectedArtifact(
                    file=artifact_file,
                )

    def _directories(self) -> Iterator[Path]:
        for entry in self.artifacts_dir.iterdir():
            if entry.is_dir():
                yield entry
