import json
from pathlib import Path

import requests


FORECAST_API_BASE_URL = "http://localhost:8001/api/v1"
ASSET_API_BASE_URL = "http://localhost:8000/api/v1"
OUTPUT_DIR = Path("frontend/dashboard-ui/public/demo-api")


def export_json(url: str, target: Path, params: dict | None = None):
    response = requests.get(url, params=params)
    response.raise_for_status()

    target.parent.mkdir(parents=True, exist_ok=True)

    target.write_text(
        json.dumps(response.json(), indent=2),
        encoding="utf-8",
    )


def main():
    portfolios_response = requests.get(f"{ASSET_API_BASE_URL}/portfolios")
    portfolios_response.raise_for_status()

    portfolios = portfolios_response.json()
    print(portfolios)
    export_json(
        f"{ASSET_API_BASE_URL}/portfolios",
        OUTPUT_DIR / "portfolios.json",
    )
    for portfolio in portfolios:


        assets_response = requests.get(f"{ASSET_API_BASE_URL}/portfolios/{portfolio['id']}/assets")
        assets_response.raise_for_status()

        assets = assets_response.json()
        print(assets)
        export_json(
            f"{ASSET_API_BASE_URL}/portfolios/{portfolio['id']}/assets",
            OUTPUT_DIR / "portfolios" / str(portfolio['id']) / f"assets.json",
        )

        for asset in assets:
            asset_id = asset["id"]

            print(asset_id)
            latitude = round(float(asset["latitude"]), 2)
            longitude = round(float(asset["longitude"]), 2)

            latitude_str = f"{latitude:.2f}"
            longitude_str = f"{longitude:.2f}"
            export_json(
                f"{FORECAST_API_BASE_URL}/weather-forecasts/",
                OUTPUT_DIR / "weather-forecasts" / f"{latitude_str}_{longitude_str}.json",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "limit": 1,
                },
            )

            export_json(
                f"{FORECAST_API_BASE_URL}/asset-forecasts/{asset_id}",
                OUTPUT_DIR / "asset-forecasts" / f"{asset_id}.json",
            )


if __name__ == "__main__":
    main()