from app.database import Base

from em_timeseries.orm import TimeSeriesMixin


class TimeSeries(TimeSeriesMixin, Base):
    pass
