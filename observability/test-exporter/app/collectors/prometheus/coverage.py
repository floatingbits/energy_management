from pathlib import Path
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from prometheus_client import Gauge

from app.collectors.artifacts import DirectoryArtifactCrawler
from app.collectors.prometheus.base import Client

COVERAGE_PERCENT = Gauge(
    "test_coverage_percent",
    "Test coverage percentage",
    ["service"],
)

COVERAGE_LINES_TOTAL = Gauge(
    "test_coverage_lines_total",
    "Number of executable lines in the coverage report",
    ["service"],
)

COVERAGE_LINES_COVERED = Gauge(
    "test_coverage_lines_covered",
    "Number of covered lines in the coverage report",
    ["service"],
)


class CoverageClient(Client):

    def __init__(self, service: str, coverage_file: Path):
        self.service = service
        self.coverage_file = coverage_file

    def export_to_prometheus(
        self
    ) -> None:
        root = ET.parse(self.coverage_file).getroot()

        line_rate = float(root.attrib["line-rate"])
        lines_total = int(root.attrib["lines-valid"])
        lines_covered = int(root.attrib["lines-covered"])

        COVERAGE_PERCENT.labels(service=self.service).set(
            line_rate * 100
        )

        COVERAGE_LINES_TOTAL.labels(service=self.service).set(
            lines_total
        )

        COVERAGE_LINES_COVERED.labels(service=self.service).set(
            lines_covered
        )
