from app.enums import AssetType


WIND_CONFIG = {"hub_height_m": 100.0, "rotor_diameter_m": 80.0}

PV_CONFIG = {
    "panel_area_m2": 50.0,
    "efficiency": 0.2,
    "tilt_deg": 30.0,
    "azimuth_deg": 180.0,
}


def test_create_asset(client):

    response = client.post(
        "/api/v1/assets/",
        json={
            "name": "Windpark Nord",
            "asset_type": AssetType.WIND,
            "installed_power_kw": 5000,
            "latitude": 53.55,
            "longitude": 9.99,
            "configuration": WIND_CONFIG
        }
    )


    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Windpark Nord"
    assert data["asset_type"] == AssetType.WIND.value
    assert data["configuration"] == WIND_CONFIG

def test_get_assets(client):

    client.post(
        "/api/v1/assets/",
        json={
            "name": "Solar Hamburg",
            "asset_type": AssetType.SOLAR,
            "installed_power_kw": 2000,
            "latitude": 53.5,
            "longitude": 10.0,
            "configuration": PV_CONFIG
        }
    )


    response = client.get(
        "/api/v1/assets/"
    )


    assert response.status_code == 200

    assets = response.json()

    assert len(assets) == 1


def test_update_asset(client):

    create = client.post(
        "/api/v1/assets/",
        json={
            "name": "Old Name",
            "asset_type": AssetType.WIND,
            "installed_power_kw": 1000,
            "latitude": 53,
            "longitude": 9,
            "configuration": WIND_CONFIG
        }
    )


    asset_id = create.json()["id"]


    response = client.put(
        f"/api/v1/assets/{asset_id}",
        json={
            "name": "New Name"
        }
    )


    assert response.status_code == 200

    assert response.json()["name"] == "New Name"


def test_delete_asset(client):

    create = client.post(
        "/api/v1/assets/",
        json={
            "name": "Delete Me",
            "asset_type": AssetType.WIND,
            "installed_power_kw": 1000,
            "latitude": 53,
            "longitude": 9,
            "configuration": WIND_CONFIG
        }
    )


    asset_id = create.json()["id"]


    response = client.delete(
        f"/api/v1/assets/{asset_id}"
    )


    assert response.status_code == 204


    response = client.get(
        f"/api/v1/assets/{asset_id}"
    )


    assert response.status_code == 404


def test_create_asset_publishes_event(client, fake_publisher):

    client.post(
        "/api/v1/assets/",
        json={
            "name": "Delete Me",
            "asset_type": AssetType.WIND,
            "installed_power_kw": 1000,
            "latitude": 53,
            "longitude": 9,
            "configuration": WIND_CONFIG
        }
    )

    assert len(fake_publisher.events) == 1

    event = fake_publisher.events[0]

    assert event.asset_id == 1
    assert event.asset_type == AssetType.WIND
