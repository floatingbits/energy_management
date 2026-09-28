from prometheus_client import Gauge, start_http_server


EXPORTER_UP = Gauge(
    "test_exporter_up",
    "Whether the test exporter is running",
)


def main() -> None:
    start_http_server(8000)

    EXPORTER_UP.set(1)

    print("Test exporter listening on :8000")

    # Keep the process alive.
    import time

    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()