from app.database import Base

from em_timeseries.orm import TimeSeriesTimeBaseMixin


class TimeSeriesTimeBase(TimeSeriesTimeBaseMixin, Base):
    pass
