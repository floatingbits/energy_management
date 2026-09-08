from app.bootstrap.workers import (
    create_asset_forecast_worker,
)


def main():
    worker = create_asset_forecast_worker()
    worker.run()


if __name__ == "__main__":
    main()