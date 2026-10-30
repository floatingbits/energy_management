from app.database import Base

from em_timeseries.orm import TimeSeriesGroupMixin


class TimeSeriesGroup(TimeSeriesGroupMixin, Base):
    pass
