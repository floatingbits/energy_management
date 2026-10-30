"""Provider of market price forecasts for decisions."""

from app.decisions.providers.decode import runs_from_group_payload
from app.decisions.providers.forecast_client import ForecastServiceClient
from app.decisions.request import PriceForecastInput

# The forecast-service metric for a market's day-ahead prices.
DAY_AHEAD_ELECTRICITY_PRICE = "day_ahead_electricity_price"


class PriceForecastProvider:
    """Fulfils the PRICE_FORECAST requirement.

    get() returns a PriceForecastInput, or None if unavailable.
    """

    def get(
        self,
        portfolio_id: int,
        market: str,
        window,
    ) -> PriceForecastInput | None:
        raise NotImplementedError


class ForecastServicePriceForecastProvider(PriceForecastProvider):
    """Serves the requirement from the forecast-service's market price
    forecast (v1: latest available forecast for market+variable is chosen
    among the listed rows)."""

    def __init__(
        self,
        client: ForecastServiceClient,
    ):
        self.client = client

    def get(
        self,
        portfolio_id: int,
        market: str,
        window,
    ) -> PriceForecastInput | None:
        forecasts = self.client.get_market_forecasts(
            market=market,
            variable=DAY_AHEAD_ELECTRICITY_PRICE,
        )
        if not forecasts:
            return None

        # The listing is ordered by the router's repository (most recent
        # first in current usage); v1 takes the first candidate.
        payload = forecasts[0]
        runs = runs_from_group_payload(payload["forecast"])
        if not runs:
            return None

        return PriceForecastInput(
            forecast_id=payload["id"],
            run=runs[0],
        )
