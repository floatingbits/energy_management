import lightgbm as lgb

from app.database import SessionLocal
from app.forecasting.enums import ForecastMetric
from app.forecasting.uncertainty.estimator import ModeledUncertaintyEstimator
from app.weather.adapters.default import DefaultWeatherAdapter
from app.weather.open_meteo_mapping import OPEN_METEO_VARIABLES

from app.weather.resolver import WeatherLocationResolver
from app.weather.open_meteo import OpenMeteoProvider
from app.services.weather_service import WeatherService


from app.repositories import weather_repository
from app.weather.uncertainty.estimator import ComposedWeatherUncertaintyEstimator
from app.weather.uncertainty.predictor_model import UncertaintyEstimatorPredictorWrapper


def create_location_resolver():
    return WeatherLocationResolver(
        grid_size=0.1
    )

def create_uncertainty_estimator():
    sub_estimators = {}
    needed_variables = [
        ForecastMetric.TEMPERATURE,
        ForecastMetric.DIRECT_NORMAL_IRRADIANCE,
        ForecastMetric.DIFFUSE_IRRADIANCE,
        ForecastMetric.PRECIPITATION,
        ForecastMetric.WIND_SPEED,
        ForecastMetric.WIND_DIRECTION
    ]
    for var in needed_variables:
        model_dir = '../models/uncertainty/weather/'
        loaded_model_wrappers = {}
        for level in ['p05', 'p50', 'p95']:
            model_file_name = var + '_' + level + '.txt'
            loaded_model = lgb.Booster(model_file=model_dir + model_file_name)
            loaded_model_wrappers[level] = UncertaintyEstimatorPredictorWrapper(needed_variables, loaded_model)

        sub_estimators[var] = ModeledUncertaintyEstimator(loaded_model_wrappers['p05'],
                                                     loaded_model_wrappers['p50'],
                                                     loaded_model_wrappers['p95'])
    return ComposedWeatherUncertaintyEstimator(sub_estimators)

def create_weather_service():

    resolver = create_location_resolver()

    provider = OpenMeteoProvider()

    adapter = DefaultWeatherAdapter(OPEN_METEO_VARIABLES, resolver)
    repository = create_weather_forecast_repository()
    weather_uncertainty_estimator = create_uncertainty_estimator()
    return WeatherService(
        resolver=resolver,
        provider=provider,
        adapter=adapter,
        repository=repository,
        uncertainty_estimator=weather_uncertainty_estimator
    )


def create_weather_forecast_repository():
    db_session = SessionLocal()
    return weather_repository.WeatherRepository(db_session)
