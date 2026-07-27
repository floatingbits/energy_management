from sqlalchemy.orm import Session

from app.weather.models import (
    WeatherForecastRun,
    WeatherForecast,
    WeatherVariable
)

from app.schemas.weather import WeatherForecastResult


def create_weather_forecast_run(
    db: Session,
    result: WeatherForecastResult
):

    run = WeatherForecastRun(
        provider=result.provider,
        model=result.model
    )

    db.add(run)

    db.flush()


    for point in result.forecasts:

        forecast = WeatherForecast(
            weather_forecast_run_id=run.id,
            latitude=point.latitude,
            longitude=point.longitude,
            period_start=point.period_start,
            period_end=point.period_end
        )

        db.add(forecast)

        db.flush()


        for variable in point.variables:

            weather_variable = WeatherVariable(
                weather_forecast_id=forecast.id,
                variable=variable.variable,
                p05=variable.p05,
                p50=variable.p50,
                p95=variable.p95
            )

            db.add(weather_variable)


    db.commit()

    return run