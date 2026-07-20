from datetime import datetime

from sqlalchemy import String, DateTime, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
portfolio_assets = Table(
    "portfolio_assets",
    Base.metadata,

    Column(
        "portfolio_id",
        ForeignKey("portfolios.id"),
        primary_key=True
    ),

    Column(
        "asset_id",
        ForeignKey("assets.id"),
        primary_key=True
    )
)

class Portfolio(Base):

    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


    assets = relationship(
        "Asset",
        secondary=portfolio_assets,
        back_populates="portfolios"
    )