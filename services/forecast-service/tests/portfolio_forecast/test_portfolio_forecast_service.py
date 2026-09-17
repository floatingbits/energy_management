from unittest.mock import Mock

import pytest

from app.portfolio_forecast.aggregators.naive import (
    NaivePortfolioAggregator,
)
from app.portfolio_forecast.service import (
    PortfolioForecastService,
    MisalignedAssetForecastsError,
    MissingAssetForecastError,
)


def _make_asset_forecast(
    asset_id: int,
    start="2026-09-09T00:00:00+00:00",
    resolution_seconds=3600,
    slots=24,
    p05=1.0,
    p50=2.0,
    p95=3.0,
    based_on_revision=1,
):

    value = Mock()
    value.p05 = p05
    value.p50 = p50
    value.p95 = p95

    series = Mock()
    series.values = [
        Mock(slot_index=index, p05=p05, p50=p50, p95=p95)
        for index in range(slots)
    ]

    run = Mock()
    run.start = start
    run.resolution_seconds = resolution_seconds
    run.slots = slots

    forecast = Mock()
    forecast.time_series_time_base = run
    forecast.time_series = [series]

    asset_forecast = Mock()
    asset_forecast.asset_id = asset_id
    asset_forecast.based_on_revision = based_on_revision
    asset_forecast.forecast = forecast

    return asset_forecast


def test_update_portfolio_forecast_aggregates_and_persists():

    portfolio_client = Mock()
    portfolio_client.get_portfolio_assets.return_value = [
        {"id": 1},
        {"id": 2},
    ]

    asset_forecast_repository = Mock()
    asset_forecast_repository.get_latest_asset_forecast.side_effect = [
        _make_asset_forecast(1),
        _make_asset_forecast(2, p05=10.0, p50=20.0, p95=30.0),
    ]

    portfolio_forecast_repository = Mock()

    service = PortfolioForecastService(
        portfolio_client=portfolio_client,
        portfolio_forecast_repository=portfolio_forecast_repository,
        asset_forecast_repository=asset_forecast_repository,
        aggregator=NaivePortfolioAggregator(),
    )

    service.update_portfolio_forecast(42)

    kwargs = portfolio_forecast_repository.save.call_args.kwargs

    assert kwargs["portfolio_id"] == 42
    assert kwargs["aggregation_model"] == "naive"
    assert kwargs["based_on_revision"] == 1

    values = kwargs["series"].values

    assert values[0].p50 == 22.0
    assert values[0].p05 == 11.0
    assert values[0].p95 == 33.0


def test_update_portfolio_forecast_raises_on_misaligned_runs():

    portfolio_client = Mock()
    portfolio_client.get_portfolio_assets.return_value = [
        {"id": 1},
        {"id": 2},
    ]

    asset_forecast_repository = Mock()
    asset_forecast_repository.get_latest_asset_forecast.side_effect = [
        _make_asset_forecast(1),
        _make_asset_forecast(2, slots=48),
    ]

    service = PortfolioForecastService(
        portfolio_client=portfolio_client,
        portfolio_forecast_repository=Mock(),
        asset_forecast_repository=asset_forecast_repository,
        aggregator=NaivePortfolioAggregator(),
    )

    with pytest.raises(MisalignedAssetForecastsError):
        service.update_portfolio_forecast(42)


def test_update_portfolio_forecast_raises_on_missing_forecast():

    portfolio_client = Mock()
    portfolio_client.get_portfolio_assets.return_value = [
        {"id": 1},
    ]

    asset_forecast_repository = Mock()
    asset_forecast_repository.get_latest_asset_forecast.return_value = (
        None
    )

    service = PortfolioForecastService(
        portfolio_client=portfolio_client,
        portfolio_forecast_repository=Mock(),
        asset_forecast_repository=asset_forecast_repository,
        aggregator=NaivePortfolioAggregator(),
    )

    with pytest.raises(MissingAssetForecastError):
        service.update_portfolio_forecast(42)
