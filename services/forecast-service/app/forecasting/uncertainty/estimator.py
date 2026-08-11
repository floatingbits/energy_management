

from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.forecasting.domain.forecast_value import ForecastValue
from app.forecasting.enums import ForecastMetric
from app.weather.uncertainty.predictor_model import UncertaintyEstimatorPredictorWrapper


@dataclass
class UncertaintyEstimatorInput:
    output_var:str
    input_values: dict[str,list[float]]


class UncertaintyEstimator(ABC):
    @abstractmethod
    def estimate_uncertain_forecast_values(self,estimator_input: UncertaintyEstimatorInput) -> list[ForecastValue]:
        pass

    def needs_variables(self) -> list[str]:
        return []

class TrivialUncertaintyEstimator(UncertaintyEstimator):

    def estimate_uncertain_forecast_values(self,estimator_input: UncertaintyEstimatorInput) -> list[ForecastValue]:
        return [
            ForecastValue.deterministic(value)
            for value in estimator_input.input_values[estimator_input.output_var]
        ]

class ModeledUncertaintyEstimator(UncertaintyEstimator):
    def __init__(self,
                 model_p05: UncertaintyEstimatorPredictorWrapper,
                 model_p50: UncertaintyEstimatorPredictorWrapper,
                 model_p95: UncertaintyEstimatorPredictorWrapper):
        self.model_p05 = model_p05
        self.model_p50 = model_p50
        self.model_p95 = model_p95

    def estimate_uncertain_forecast_values(self,estimator_input: UncertaintyEstimatorInput) -> list[ForecastValue]:

        p05 = self.model_p05.predict(estimator_input.input_values)
        p50 = self.model_p50.predict(estimator_input.input_values)
        p95 = self.model_p95.predict(estimator_input.input_values)

        return [
            ForecastValue.probabilistic(
                p05=val05,
                p50=val50,
                p95=val95
            )
            for val05, val50, val95 in zip(p05, p50, p95)
        ]

    def needs_variables(self) -> list[str]:
        return list(set(self.model_p05.needed_variables + self.model_p50.needed_variables + self.model_p95.needed_variables))

