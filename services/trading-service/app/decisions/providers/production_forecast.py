"""Provider of production forecasts (portfolio level) for decisions."""

from app.decisions.providers.decode import runs_from_group_payload
from app.decisions.providers.forecast_client import ForecastServiceClient
from app.decisions.request import ProductionForecastInput


class ProductionForecastProvider:
    """Fulfils the PRODUCTION_FORECAST requirement.

    get() returns a ProductionForecastInput, or None if unavailable.
    """

    def get(
        self,
        portfolio_id: int,
        market: str,
        window,
    ) -> ProductionForecastInput | None:
        raise NotImplementedError


class ForecastServiceProductionForecastProvider(ProductionForecastProvider):
    """Serves the requirement from the forecast-service's latest portfolio
    forecast (v1: no windowed endpoint yet — the run is fetched whole and
    mapped to the delivery window by the alignment module)."""

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
    ) -> ProductionForecastInput | None:
        payload = self.client.get_portfolio_forecast(portfolio_id)
        runs = runs_from_group_payload(payload["forecast"])
        if not runs:
            return None
        return ProductionForecastInput(
            forecast_id=payload["id"],
            run=runs[0],
        )
