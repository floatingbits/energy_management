from datetime import datetime

from sqlalchemy import Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Forecast(Base):

    __tablename__ = "forecasts"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    asset_id: Mapped[int] = mapped_column(
        Integer,
        index=True
    )

    forecast_time: Mapped[datetime] = mapped_column(
        DateTime,
        index=True
    )

    predicted_power_kw: Mapped[float] = mapped_column(
        Float
    )