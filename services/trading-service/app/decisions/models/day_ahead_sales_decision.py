from datetime import timezone, datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from app.orm.time_series import TimeSeriesGroup


class DayAheadSalesDecision(Base):
    """A day-ahead sales decision: context, provenance and one time series
    group holding the decided values (see the decisions package docstring;
    the TimeSeries structure supports n series, v1 stores exactly one).
    """

    __tablename__ = "day_ahead_sales_decisions"

    id = Column(Integer, primary_key=True)

    portfolio_id = Column(Integer, nullable=False)

    # Market is mocked at portfolio level for the time being ("DE-LU").
    market = Column(String, nullable=False)

    # Delivery window the decision is valid for (start inclusive,
    # end exclusive, time zone as produced).
    delivery_start = Column(DateTime(timezone=True), nullable=False)
    delivery_end = Column(DateTime(timezone=True), nullable=False)

    # Provenance: the strategy that produced the series.
    strategy = Column(String, nullable=False)

    # Provenance: ids of the forecast-service objects the decision was
    # based on (plain ids; foreign objects live in another database).
    based_on_portfolio_forecast_id = Column(Integer, nullable=True)
    based_on_price_forecast_id = Column(Integer, nullable=True)

    # The quantile level of the production forecast the plan settled on,
    # when applicable (=> 5 for the conservative baseline).
    quantile_level = Column(Integer, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    time_series_group_id = Column(
        Integer,
        ForeignKey("time_series_groups.id"),
        nullable=False,
    )

    time_series_group = relationship("TimeSeriesGroup")
