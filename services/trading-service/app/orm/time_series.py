"""The shared time series tables, attached to this service's own database."""

from app.database import Base

from em_timeseries.orm import (
    TimeSeriesGroupMixin,
    TimeSeriesMixin,
    TimeSeriesTimeBaseMixin,
    TimeSeriesValueMixin,
)


class TimeSeriesGroup(TimeSeriesGroupMixin, Base):
    pass


class TimeSeriesTimeBase(TimeSeriesTimeBaseMixin, Base):
    pass


class TimeSeries(TimeSeriesMixin, Base):
    pass


class TimeSeriesValue(TimeSeriesValueMixin, Base):
    pass
