"""REST client to the asset-service, portfolios only."""

import httpx


class PortfolioClient:

    def __init__(
        self,
        base_url: str,
        timeout: float = 15.0,
    ):
        self.base_url = base_url
        self._timeout = timeout

    def get_portfolios(self) -> list[dict]:
        response = httpx.get(
            f"{self.base_url}/portfolios",
            timeout=self._timeout,
            follow_redirects=True,
        )

        response.raise_for_status()

        return response.json()
