class PortfolioForecastUpdater:

    def __init__(
        self,
        portfolio_forecast_service,
        portfolio_id: int | None,
    ):
        self.portfolio_forecast_service = portfolio_forecast_service
        self.portfolio_id = portfolio_id

    def run(self) -> None:

        if self.portfolio_id is not None:
            self.portfolio_forecast_service.update_portfolio_forecast(
                self.portfolio_id
            )

            return

        self.portfolio_forecast_service.update_all_portfolios()
