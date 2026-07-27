from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class WeatherForecastRun(Base):

    __tablename__ = "weather_forecast_runs"

    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    provider: Mapped[str] = mapped_column(
        String(50)
    )

    model: Mapped[str] = mapped_column(
        String(50)
    )

    forecasts = relationship(
        "WeatherForecast",
        back_populates="forecast_run",
        cascade="all, delete-orphan"
    )


class WeatherForecast(Base):

    __tablename__ = "weather_forecasts"

    id: Mapped[int] = mapped_column(primary_key=True)

    weather_forecast_run_id: Mapped[int] = mapped_column(
        ForeignKey("weather_forecast_runs.id")
    )

    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    forecast_run = relationship(
        "WeatherForecastRun",
        back_populates="forecasts"
    )

    variables = relationship(
        "WeatherForecastValue",
        back_populates="forecast",
        cascade="all, delete-orphan"
    )

class WeatherForecastValue(Base):

    __tablename__ = "weather_variables"

    id: Mapped[int] = mapped_column(primary_key=True)

    forecast_id: Mapped[int] = mapped_column(
        ForeignKey("weather_forecasts.id")
    )

    variable: Mapped[str] = mapped_column(
        String(50)
    )

    p05: Mapped[float] = mapped_column(Float)
    p50: Mapped[float] = mapped_column(Float)
    p95: Mapped[float] = mapped_column(Float)


    forecast = relationship(
        "WeatherForecast",
        back_populates="variables"
    )