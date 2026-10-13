from app.database import Base

from em_timeseries.orm import TimeSeriesValueMixin


class TimeSeriesValue(TimeSeriesValueMixin, Base):
    pass
