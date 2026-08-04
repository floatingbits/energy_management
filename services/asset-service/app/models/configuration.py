from sqlalchemy import Float
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database import Base


class PvConfiguration(Base):

    __tablename__ = "pv_asset_configurations"

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id"),
        primary_key=True,
    )

    panel_area_m2: Mapped[float] = mapped_column(Float)

    efficiency: Mapped[float] = mapped_column(Float)

    tilt_deg: Mapped[float] = mapped_column(Float)

    azimuth_deg: Mapped[float] = mapped_column(Float)

    asset = relationship(
        "Asset",
        back_populates="pv_configuration",
    )


class WindConfiguration(Base):

    __tablename__ = "wind_asset_configurations"

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id"),
        primary_key=True,
    )

    hub_height_m: Mapped[float] = mapped_column(Float)

    rotor_diameter_m: Mapped[float] = mapped_column(Float)

    asset = relationship(
        "Asset",
        back_populates="wind_configuration",
    )


class BatteryConfiguration(Base):

    __tablename__ = "battery_asset_configurations"

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id"),
        primary_key=True,
    )

    capacity_kwh: Mapped[float] = mapped_column(Float)

    max_charge_kw: Mapped[float] = mapped_column(Float)

    max_discharge_kw: Mapped[float] = mapped_column(Float)

    asset = relationship(
        "Asset",
        back_populates="battery_configuration",
    )