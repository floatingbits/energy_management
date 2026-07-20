def test_get_portfolio(
    client
):

    create = client.post(
        "/api/v1/portfolios/",
        json={
            "name": "Solar Portfolio"
        }
    )

    portfolio_id = create.json()["id"]


    response = client.get(
        f"/api/v1/portfolios/{portfolio_id}"
    )


    assert response.status_code == 200

    assert response.json()["id"] == portfolio_id

def test_create_portfolio(
    client
):

    response = client.post(
        "/api/v1/portfolios/",
        json={
            "name": "Wind Portfolio",
            "description": "Nord"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Wind Portfolio"
    assert data["description"] == "Nord"



def test_add_asset_to_portfolio(
    client
):

    portfolio = client.post(
        "/api/v1/portfolios/",
        json={
            "name": "Renewables"
        }
    )

    portfolio_id = portfolio.json()["id"]


    asset = client.post(
        "/api/v1/assets/",
        json={
            "name": "Windpark Nord",
            "asset_type": "WIND",
            "installed_power_kw": 5000,
            "latitude": 53.5,
            "longitude": 10.0
        }
    )

    asset_id = asset.json()["id"]


    response = client.post(
        f"/api/v1/portfolios/{portfolio_id}/assets/{asset_id}"
    )


    assert response.status_code == 201


    data = response.json()

    assert data["id"] == portfolio_id


def test_get_portfolio_assets(
    client
):

    portfolio = client.post(
        "/api/v1/portfolios/",
        json={
            "name": "Mixed Portfolio"
        }
    )

    portfolio_id = portfolio.json()["id"]


    asset = client.post(
        "/api/v1/assets/",
        json={
            "name": "PV Dach",
            "asset_type": "SOLAR",
            "installed_power_kw": 100,
            "latitude": 53.5,
            "longitude": 10.0
        }
    )

    asset_id = asset.json()["id"]


    client.post(
        f"/api/v1/portfolios/{portfolio_id}/assets/{asset_id}"
    )


    response = client.get(
        f"/api/v1/portfolios/{portfolio_id}/assets"
    )


    assert response.status_code == 200

    assets = response.json()

    assert len(assets) == 1
    assert assets[0]["id"] == asset_id