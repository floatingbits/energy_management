"""Registry-agnostic ORM definitions of the time series tables.

SQLAlchemy binds a declarative mapping to exactly one MetaData/Base, so these
mixin classes carry columns, constraints and relationships but are NOT
declared against any Base. Services attach them to their own declarative
base (their database owns the schema):

    class TimeSeries(TimeSeriesMixin, Base): pass

The relationship strings resolve against the attaching service's Base
registry, so every service must declare all four attached classes
(TimeSeriesGroup, TimeSeries, TimeSeriesTimeBase, TimeSeriesValue).
"""

from datetime import timezone, datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declared_attr, relationship

from em_timeseries.encoding.definitions import DEFAULT_QUANTILE_DEFINITION


class TimeSeriesTimeBaseMixin:

    __tablename__ = "time_series_time_bases"

    id = Column(
        Integer,
        primary_key=True
    )

    start = Column(
        DateTime(timezone=True),
        nullable=False
    )

    resolution_seconds = Column(
        Integer,
        nullable=False
    )

    slots = Column(
        Integer,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )


class TimeSeriesGroupMixin:

    __tablename__ = "time_series_groups"

    id = Column(
        Integer,
        primary_key=True
    )

    time_series_time_base_id = Column(
        Integer,
        ForeignKey(
            "time_series_time_bases.id"
        ),
        nullable=False
    )

    @declared_attr
    def time_series(cls):
        return relationship(
            "TimeSeries",
            back_populates="time_series_group",
            cascade="all, delete-orphan"
        )

    @declared_attr
    def time_series_time_base(cls):
        return relationship(
            "TimeSeriesTimeBase"
        )


class TimeSeriesMixin:

    __tablename__ = "time_series"

    id = Column(
        Integer,
        primary_key=True
    )

    metric = Column(
        String,
        nullable=False
    )

    value_type_definition = Column(
        String,
        nullable=False,
        default=DEFAULT_QUANTILE_DEFINITION.serialize,
    )

    time_series_group_id = Column(
        Integer,
        ForeignKey(
            "time_series_groups.id"
        ),
        nullable=False
    )

    @declared_attr
    def time_series_group(cls):
        return relationship(
            "TimeSeriesGroup",
            back_populates="time_series"
        )

    @declared_attr
    def values(cls):
        return relationship(
            "TimeSeriesValue",
            back_populates="time_series",
            cascade="all, delete-orphan"
        )


class TimeSeriesValueMixin:

    __tablename__ = "time_series_values"

    id = Column(
        Integer,
        primary_key=True
    )

    time_series_id = Column(
        Integer,
        ForeignKey(
            "time_series.id"
        ),
        nullable=False
    )

    slot_index = Column(
        Integer,
        nullable=False
    )

    payload = Column(
        String,
        nullable=False
    )

    value_type = Column(
        String,
        nullable=False,
        default="forecast"
    )

    @declared_attr
    def time_series(cls):
        return relationship(
            "TimeSeries",
            back_populates="values"
        )
