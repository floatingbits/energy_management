def test_create_asset(client):

    response = client.post(
        "/api/v1/assets/",
        json={
            "name": "Windpark Nord",
            "asset_type": "WIND",
            "installed_power_kw": 5000,
            "latitude": 53.55,
            "longitude": 9.99
        }
    )


    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Windpark Nord"
    assert data["asset_type"] == "WIND"

def test_get_assets(client):

    client.post(
        "/api/v1/assets/",
        json={
            "name": "Solar Hamburg",
            "asset_type": "SOLAR",
            "installed_power_kw": 2000,
            "latitude": 53.5,
            "longitude": 10.0
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
            "asset_type": "WIND",
            "installed_power_kw": 1000,
            "latitude": 53,
            "longitude": 9
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
            "asset_type": "WIND",
            "installed_power_kw": 1000,
            "latitude": 53,
            "longitude": 9
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
            "asset_type": "WIND",
            "installed_power_kw": 1000,
            "latitude": 53,
            "longitude": 9
        }
    )

    assert len(fake_publisher.events) == 1

    event = fake_publisher.events[0]

    assert event.asset_id == 1
    assert event.asset_type == "WIND"