"""REST client to the forecast-service."""

import httpx


class ForecastServiceClient:
    """Sync client for selected forecast-service read endpoints."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 15.0,
    ):
        self.base_url = base_url
        self._timeout = timeout


    def get_portfolio_forecast(
        self,
        portfolio_id: int,
    ) -> dict:
        response = httpx.get(
            f"{self.base_url}/portfolio-forecasts/{portfolio_id}",
            timeout=self._timeout,
            follow_redirects=True,
        )

        response.raise_for_status()

        return response.json()

    def get_market_forecasts(
        self,
        market: str,
        variable: str | None = None,
    ) -> list[dict]:
        params = {"market": market}
        if variable is not None:
            params["variable"] = variable

        response = httpx.get(
            f"{self.base_url}/energy-market-forecasts",
            params=params,
            timeout=self._timeout,
            follow_redirects=True,
        )

        response.raise_for_status()

        return response.json()
