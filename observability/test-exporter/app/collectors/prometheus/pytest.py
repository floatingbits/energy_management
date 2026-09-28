from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

from prometheus_client import Gauge


from app.collectors.prometheus.base import Client

TESTS_TOTAL = Gauge(
    "test_tests_total",
    "Total number of tests in the pytest report",
    ["service"],
)

TESTS_PASSED = Gauge(
    "test_tests_passed",
    "Number of passed tests in the pytest report",
    ["service"],
)

TESTS_FAILED = Gauge(
    "test_tests_failed",
    "Number of failed and errored tests in the pytest report",
    ["service"],
)

TESTS_SKIPPED = Gauge(
    "test_tests_skipped",
    "Number of skipped tests in the pytest report",
    ["service"],
)

TESTS_LAST_RUN_TIMESTAMP = Gauge(
    "test_last_run_timestamp",
    "Unix timestamp of the last test run",
    ["service"],
)


class PytestClient(Client):

    def __init__(self, service: str, pytest_file: Path):
        self.service = service
        self.pytest_file = pytest_file



    def export_to_prometheus(
        self
    ) -> None:
        root = ET.parse(self.pytest_file).getroot()

        tests_total = 0
        tests_failed = 0
        tests_skipped = 0
        last_run_timestamp = 0.0

        for testsuite in root.iter("testsuite"):
            tests_total += int(testsuite.attrib.get("tests", 0))
            tests_failed += int(testsuite.attrib.get("errors", 0))
            tests_failed += int(testsuite.attrib.get("failures", 0))
            tests_skipped += int(testsuite.attrib.get("skipped", 0))

            timestamp = testsuite.attrib.get("timestamp")

            if timestamp:
                last_run_timestamp = max(
                    last_run_timestamp,
                    datetime.fromisoformat(timestamp).timestamp(),
                )

        TESTS_TOTAL.labels(service=self.service).set(tests_total)
        TESTS_FAILED.labels(service=self.service).set(tests_failed)
        TESTS_SKIPPED.labels(service=self.service).set(tests_skipped)

        TESTS_PASSED.labels(service=self.service).set(
            tests_total - tests_failed - tests_skipped
        )

        if last_run_timestamp:
            TESTS_LAST_RUN_TIMESTAMP.labels(service=self.service).set(
                last_run_timestamp
            )
