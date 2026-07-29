from abc import ABC, abstractmethod

from app.weather.timeseries import TimeSeries


class InterpolationStrategy(ABC):

    @abstractmethod
    def interpolate(
        self,
        series: TimeSeries,
        target_timestamps: list,
    ) -> TimeSeries:
        """
        Transformiert eine TimeSeries auf ein neues Zeitraster.
        """
        raise NotImplementedError