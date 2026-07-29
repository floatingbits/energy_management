from sqlalchemy.orm import Session

from app.forecasting.models.forecast_series import ForecastSeries
from app.forecasting.models.forecast_value import ForecastValue
from app.forecasting.models.forecast_run import ForecastRun
from app.weather.models import (
    WeatherForecast, WeatherSource,
)

from app.weather.result import WeatherForecastResult


def create_weather_forecast_run(
    db: Session,
    result: WeatherForecastResult
):
    result_run = result.forecasts[0].run
    run = ForecastRun(
        start=result_run.start,
        slots=result_run.slots,
        resolution_seconds=result_run.resolution.seconds,


    )

    db.add(run)

    db.flush()


    source = WeatherSource(
        model=result.model,
        provider=result.provider,
        version='0.0.1'
    )
    db.add(source)

    db.flush()


    for point in result.forecasts:

        forecast = WeatherForecast(
            forecast_run_id=run.id,
            latitude=point.location.latitude,
            longitude=point.location.longitude,
            source_id=source.id
        )

        db.add(forecast)

        db.flush()


        for series in point.series:

            series_model = ForecastSeries(
                forecast_run_id=run.id,
                metric=series.metric,
            )

            db.add(series_model)
            db.flush()
            for i, value in enumerate(series.values):
                value_model = ForecastValue(
                    series_id=series_model.id,
                    slot_index=i,
                    p05=value.p05,
                    p50=value.p50,
                    p95=value.p95
                )

                db.add(value_model)
                db.flush()


    db.commit()

    return run