from datetime import timedelta

from app.forecasting.enums import ForecastMetric
from app.portfolio_forecast.aggregators.aggregator import (
    PortfolioAggregator,
)
from app.portfolio_forecast.domain.timeslice import (
    TimesliceValues,
)
from app.forecasting.domain.forecast_run import ForecastRun
from app.forecasting.domain.forecast_series import ForecastSeries
from app.forecasting.domain.forecast_value import ForecastValue
from app.repositories.asset_forecast_repository import AssetForecastRepository
from app.repositories.portfolio_forecast_repository import PortfolioForecastRepository


class MisalignedAssetForecastsError(Exception):
    """
    Die neuesten Asset-Forecasts der Portfolio-Assets passen
    nicht zusammen (unterschiedlicher Start, Auflösung oder
    Slot-Anzahl).
    """
    pass


class MissingAssetForecastError(Exception):
    """
    Für mindestens ein Asset des Portfolios existiert
    (noch) kein Asset-Forecast.
    """
    pass


class PortfolioForecastService:
    """
    Orchestriert die Aggregation eines Portfolio-Forecasts.

    Lädt die jeweils neuesten Asset-Forecasts der
    Portfolio-Assets, prüft deren horizontale Ausrichtung,
    überlässt je Zeitscheibe die eigentliche Mathematik dem
    PortfolioAggregator und persistiert das Ergebnis.

    Frische- und Requirement-Logik leben bewusst nicht hier:
    Dieses Objekt wird aufgerufen, wenn Asset-Forecasts
    aktualisiert wurden, und nimmt die Inputs so, wie sie sind.
    """

    def __init__(
        self,
        portfolio_client,
        portfolio_forecast_repository: PortfolioForecastRepository,
        asset_forecast_repository: AssetForecastRepository,
        aggregator: PortfolioAggregator,
    ):
        self.portfolio_client = portfolio_client
        self.portfolio_forecast_repository = portfolio_forecast_repository
        self.asset_forecast_repository = asset_forecast_repository
        self.aggregator = aggregator

    def update_portfolio_forecast(
        self,
        portfolio_id: int,
    ) -> None:

        assets = self.portfolio_client.get_portfolio_assets(portfolio_id)

        asset_ids = [asset["id"] for asset in assets]

        if not asset_ids:
            return

        asset_forecasts = []

        for asset_id in asset_ids:

            asset_forecast = (
                self.asset_forecast_repository.get_latest_asset_forecast(
                    asset_id
                )
            )

            # Bis eine Frische-/Requirement-Logik auf dieser Seite
            # existiert, gilt: ohne Asset-Forecast für alle Assets
            # kein Portfolio-Forecast.
            if asset_forecast is None:
                raise MissingAssetForecastError(
                    f"No asset forecast for asset {asset_id} "
                    f"of portfolio {portfolio_id}."
                )

            asset_forecasts.append(asset_forecast)

        self._check_alignment(asset_forecasts)

        # Alignment ist geprüft, daher genügt die Referenz-Run der
        # Asset-Forecasts als Vorlage für den Portfolio-Forecast.
        reference_run = asset_forecasts[0].forecast.forecast_run

        forecast_run = ForecastRun(
            start=reference_run.start,
            resolution=timedelta(seconds=reference_run.resolution_seconds),
            slots=reference_run.slots,
        )

        series = self._aggregate(
            asset_forecasts=asset_forecasts,
            slot_count=reference_run.slots,
        )

        self.portfolio_forecast_repository.save(
            portfolio_id=portfolio_id,
            forecast_run=forecast_run,
            series=series,
            aggregation_model=self.aggregator.get_name(),
            based_on_revision=max(
                asset_forecast.based_on_revision
                for asset_forecast in asset_forecasts
            ),
        )

    def update_all_portfolios(
        self,
    ) -> None:

        portfolios = self.portfolio_client.get_portfolios()

        for portfolio in portfolios:
            self.update_portfolio_forecast(portfolio["id"])

    def update_affected_portfolios(
        self,
        affected_asset_ids: list[int],
    ) -> None:
        """
        Bestimmt die Portfolios, die mindestens eines der
        betroffenen Assets enthalten, und aktualisiert deren
        Portfolio-Forecast.
        """

        affected_asset_ids = set(affected_asset_ids)

        portfolios = self.portfolio_client.get_portfolios()

        for portfolio in portfolios:

            assets = self.portfolio_client.get_portfolio_assets(
                portfolio["id"]
            )

            portfolio_asset_ids = {asset["id"] for asset in assets}

            if not affected_asset_ids & portfolio_asset_ids:
                continue

            self.update_portfolio_forecast(portfolio["id"])

    def _check_alignment(
        self,
        asset_forecasts,
    ) -> None:

        first = asset_forecasts[0].forecast.forecast_run

        for asset_forecast in asset_forecasts:

            run = asset_forecast.forecast.forecast_run

            if (
                run.start != first.start
                or run.slots != first.slots
                or run.resolution_seconds != first.resolution_seconds
            ):
                raise MisalignedAssetForecastsError(
                    "Latest asset forecasts are not aligned: "
                    f"(start={run.start}, slots={run.slots}, "
                    f"resolution={run.resolution_seconds}) vs. "
                    f"(start={first.start}, slots={first.slots}, "
                    f"resolution={first.resolution_seconds})."
                )

    def _aggregate(
        self,
        asset_forecasts,
        slot_count: int,
    ) -> ForecastSeries:

        # Quantile je Asset je Slot indexieren, damit die
        # Slot-Reihenfolge nicht von der Persistenz abhängt.
        values_by_asset = {
            asset_forecast.asset_id: (
                self._quantiles_by_slot(asset_forecast)
            )
            for asset_forecast in asset_forecasts
        }

        aggregated_values = []

        for slot_index in range(slot_count):

            timeslice_values = [
                TimesliceValues(
                    asset_id=asset_id,
                    p05=quantiles[slot_index].p05,
                    p50=quantiles[slot_index].p50,
                    p95=quantiles[slot_index].p95,
                )
                for asset_id, quantiles in values_by_asset.items()
            ]

            aggregated = self.aggregator.aggregate(timeslice_values)

            aggregated_values.append(
                ForecastValue.probabilistic(
                    p05=aggregated.p05,
                    p50=aggregated.p50,
                    p95=aggregated.p95,
                )
            )

        return ForecastSeries(
            metric=ForecastMetric.ACTIVE_POWER,
            values=aggregated_values
        )

    @staticmethod
    def _quantiles_by_slot(
        asset_forecast,
    ) -> dict[int, ForecastValue]:

        series = asset_forecast.forecast.series[0]

        return {
            value.slot_index: value
            for value in series.values
        }
