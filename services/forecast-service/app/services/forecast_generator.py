from datetime import datetime, timedelta

from app.models.forecast import Forecast


def generate_forecasts(
    asset_id: int
) -> list[Forecast]:

    now = datetime.utcnow()

    forecasts = []

    for hour in range(24):

        forecast = Forecast(
            asset_id=asset_id,
            forecast_time=now + timedelta(hours=hour),
            predicted_power_kw=1000 + hour * 50
        )

        forecasts.append(forecast)

    return forecasts