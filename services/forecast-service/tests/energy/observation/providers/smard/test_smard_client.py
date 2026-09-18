import responses

from app.energy.observation.providers.smard.client import SmardClient


@responses.activate
def test_get_index_returns_timestamps():
    responses.add(
        responses.GET,
        SmardClient.API_URL + "/410/DE/index_quarterhour.json",
        json={
            "timestamps": [1733305200000, 1733312400000],
        },
        status=200,
    )

    client = SmardClient()

    timestamps = client.get_index("410", "DE", "quarterhour")

    assert timestamps == [1733305200000, 1733312400000]


@responses.activate
def test_get_timeseries_returns_series():
    responses.add(
        responses.GET,
        SmardClient.API_URL + "/410/DE/410_DE_quarterhour_1733305200000.json",
        json={
            "timestamps": [1733305200000, 1733306100000],
            "meta": "a",
            "series": [
                [1733305200000, 50000.0],
                [1733306100000, None],
            ],
        },
        status=200,
    )

    client = SmardClient()

    timeseries = client.get_timeseries("410", "DE", "quarterhour", 1733305200000)

    assert timeseries == [
        [1733305200000, 50000.0],
        [1733306100000, None],
    ]
