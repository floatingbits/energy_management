from datetime import timedelta

from app.asset_forecast.calculators.pv_forecast_calculator import (
    PvForecastCalculator,
)
from app.asset_forecast.domain.pv_asset_context import PvAssetContext

from app.asset_forecast.domain.pv_forecast import PvForecastInput

from app.forecasting.enums import ForecastMetric
from app.forecasting.domain.forecast_series import ForecastSeries
from app.forecasting.domain.forecast_value import ForecastValue
from app.weather.result import WeatherLocationForecast


class PvAssetForecastGenerator:

    def __init__(
        self,
        forecast_calculator: PvForecastCalculator,
    ):
        self.forecast_calculator = forecast_calculator


    def generate(
        self,
        asset: PvAssetContext,
            weather_forecast: WeatherLocationForecast,
    ) -> ForecastSeries:

        run = weather_forecast.run

        dni_series = self._get_series(
            weather_forecast,
            ForecastMetric.DIRECT_NORMAL_IRRADIANCE,
        )

        diffuse_series = self._get_series(
            weather_forecast,
            ForecastMetric.DIFFUSE_IRRADIANCE,
        )

        values = []

        for slot_index in range(run.slots):

            timestamp = (
                run.start
                +
                timedelta(
                    seconds=slot_index * run.resolution.total_seconds()
                )
            )

            result = self.forecast_calculator.calculate(
                PvForecastInput(
                    timestamp=timestamp,

                    latitude=asset.latitude,
                    longitude=asset.longitude,

                    direct_normal_irradiance=(
                        dni_series.values[slot_index].p50
                    ),

                    diffuse_radiation=(
                        diffuse_series.values[slot_index].p50
                    ),

                    panel_geometry=(
                        asset.panel_geometry
                    ),

                    pv_configuration=(
                        asset.pv_configuration
                    ),
                )
            )

            values.append(
                ForecastValue(
                    p50=result.active_power_kw,
                )
            )


        return ForecastSeries(
            metric=ForecastMetric.ACTIVE_POWER,
            values=values,
        )


    def _get_series(
        self,
        weather_forecast: WeatherLocationForecast,
        metric: ForecastMetric,
    ):

        return next(
            series
            for series in weather_forecast.series
            if series.metric == metric
        )