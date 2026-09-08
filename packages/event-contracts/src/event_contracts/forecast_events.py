from typing import Literal

from event_contracts.base import BaseEvent


class AssetForecastCreatedEvent(BaseEvent):
    event_type: Literal["asset_forecast.created"] = "asset_forecast.created"

    forecast_id: int
    asset_id: int


class AssetForecastUpdatedEvent(BaseEvent):
    event_type: Literal["asset_forecast.updated"] = "asset_forecast.updated"

    forecast_id: int
    asset_id: int

class WeatherForecastCreatedEvent(BaseEvent):
    event_type: Literal["weather_forecast.created"] = "weather_forecast.created"

    forecast_id: int


class WeatherForecastUpdatedEvent(BaseEvent):
    event_type: Literal["weather_forecast.updated"] = "weather_forecast.updated"

    forecast_id: int

class PortfolioForecastCreatedEvent(BaseEvent):
    event_type: Literal["portfolio_forecast.created"] = "portfolio_forecast.created"

    forecast_id: int
    portfolio_id: int


class PortfolioForecastUpdatedEvent(BaseEvent):
    event_type: Literal["portfolio_forecast.updated"] = "portfolio_forecast.updated"

    forecast_id: int
    portfolio_id: int
