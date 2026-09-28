import time

from prometheus_client import start_http_server


from app.bootstrap import create_collectors


PORT = 8000
COLLECTION_INTERVAL = 30


def main() -> None:
    collectors = create_collectors()

    start_http_server(PORT)

    print(f"Test exporter listening on :{PORT}")

    while True:

        for collector in collectors:
            try:
                collector.collect()
            except Exception as exc:
                print(f"Collector error: {exc}")

        time.sleep(COLLECTION_INTERVAL)


if __name__ == "__main__":
    main()