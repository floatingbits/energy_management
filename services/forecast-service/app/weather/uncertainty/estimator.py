from typing import Protocol
from datetime import datetime, timezone
import numpy as np

from app.weather.result import WeatherForecastResult, WeatherLocationForecast
from app.forecasting.uncertainty.estimator import UncertaintyEstimator, UncertaintyEstimatorInput


class WeatherUncertaintyEstimator(Protocol):
    def apply(
            self,
            forecast: WeatherForecastResult,
    ) -> WeatherForecastResult:
        ...
    def needs_variables(self) -> list[str]:
        ...


class ComposedWeatherUncertaintyEstimator(WeatherUncertaintyEstimator):
    def __init__(self, variable_estimators: dict[str, UncertaintyEstimator]):
        self.variable_estimators = variable_estimators

    def apply(
            self,
            forecast: WeatherForecastResult,
    ) -> WeatherForecastResult:

        for fc in forecast.forecasts:
            input_values = self.generate_input_values(fc)
            for series in fc.series:
                if series.metric not in self.variable_estimators.keys():
                    # keep "deterministic" values
                    continue
                var_estimator = self.variable_estimators[series.metric]
                estimator_input = UncertaintyEstimatorInput(series.metric, input_values)
                new_values = var_estimator.estimate_uncertain_forecast_values(estimator_input=estimator_input)
                series.values = new_values

        return forecast

    def needs_variables(self) -> list[str]:
        needed_vars = []
        for estimator in self.variable_estimators.values():
            needed_vars += estimator.needs_variables()
        return list(set(needed_vars))

    def generate_input_values(self, forecast: WeatherLocationForecast) -> dict[str, list[float]]:
        result = {}

        num_slots = forecast.run.slots
        #num_slots = len(fc.series[0].values)
        result['latitude'] = np.repeat(forecast.location.latitude, num_slots,0)
        result['longitude'] = np.repeat(forecast.location.longitude, num_slots, 0)
        # TODO: Elevation from forecast
        result['elevation'] = np.repeat(30, num_slots, 0)
        result['day_of_year'] = [forecast.run.timestamp_for_slot(i).timetuple().tm_yday for i in range(0, num_slots)]
        result['hour_of_day'] = [forecast.run.timestamp_for_slot(i).timetuple().tm_hour for i in range(0, num_slots)]
        now = datetime.now(tz=timezone.utc)
        result['forecast_horizon'] = [(forecast.run.timestamp_for_slot(i) - now).total_seconds() for i in range(0, num_slots)]
        for series in forecast.series:
            result[series.metric] = [value.p50 for value in series.values[:num_slots]]

        return result
