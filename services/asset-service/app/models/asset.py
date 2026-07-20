from datetime import datetime, timezone

from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.portfolio import portfolio_assets
from app.database import Base


class Asset(Base):

    __tablename__ = "assets"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )


    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )


    asset_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )


    installed_power_kw: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )


    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )


    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )


    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="ACTIVE"
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )


    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    portfolios = relationship(
        "Portfolio",
        secondary=portfolio_assets,
        back_populates="assets"
    )