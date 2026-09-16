import requests


class PortfolioClient:

    def __init__(
        self,
        base_url: str,
    ):
        self.base_url = base_url


    def get_portfolios(
        self,
    ):

        response = requests.get(
            f"{self.base_url}/portfolios"
        )

        response.raise_for_status()

        return response.json()


    def get_portfolio_assets(
        self,
        portfolio_id: int,
    ):

        response = requests.get(
            f"{self.base_url}/portfolios/{portfolio_id}/assets"
        )

        response.raise_for_status()

        return response.json()
