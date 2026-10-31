#!/usr/bin/env python3

import argparse
import json
import os
import sys
from pathlib import Path

import httpx


def load_fixture(client: httpx.Client, path: Path) -> None:
    print(f"\nLoading {path}...")

    with path.open(encoding="utf-8") as file:
        fixture = json.load(file)

    portfolio_data = fixture["portfolio"]
    assets = fixture["assets"]

    # 1. Portfolio anlegen
    response = client.post(
        "/portfolios/",  # An den tatsächlichen API-Endpunkt anpassen
        json=portfolio_data,
    )
    response.raise_for_status()

    portfolio_id = response.json()["id"]
    print(f"Created portfolio {portfolio_id}")

    # 2. Assets anlegen und dem Portfolio zuordnen
    for asset_data in assets:
        response = client.post(
            "/assets/",  # An den tatsächlichen API-Endpunkt anpassen
            json=asset_data,
        )
        response.raise_for_status()

        asset = response.json()
        asset_id = asset["id"]

        print(f"Created asset {asset_id}: {asset_data['name']}")

        # 3. Asset dem Portfolio hinzufügen
        # Hier fehlt noch der tatsächliche API-Vertrag.
        #
        # Beispiel:
        client.post(
            f"/portfolios/{portfolio_id}/assets/{asset_id}",
            json={},
        ).raise_for_status()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Load portfolio and asset fixtures through the Asset API."
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="Directory containing JSON fixture files",
    )
    args = parser.parse_args()

    base_url = os.environ.get("ASSET_API_URL", default="http://localhost:8000/api/v1")
    if not base_url:
        parser.error("Set ASSET_API_URL to the Asset-Service base URL.")

    if not args.directory.is_dir():
        parser.error(f"Not a directory: {args.directory}")

    files = sorted(args.directory.glob("*.json"))
    if not files:
        print(f"No JSON fixtures found in {args.directory}")
        return 0

    try:
        with httpx.Client(
            base_url=base_url.rstrip("/"),
            timeout=30.0,
        ) as client:
            for path in files:
                load_fixture(client, path)

    except (httpx.HTTPError, KeyError, ValueError) as exc:
        print(f"Fixture loading failed: {exc}", file=sys.stderr)
        return 1

    print(f"\nSuccessfully processed {len(files)} fixture files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())