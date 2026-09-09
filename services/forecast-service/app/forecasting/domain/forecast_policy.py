from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class ForecastPeriod:
    start: datetime
    end: datetime


@dataclass(frozen=True)
class ForecastRunRequirement:
    start: datetime
    resolution_seconds: int
    slots: int

class ForecastPolicy:
    def __init__(
        self,
        horizon: timedelta,
        quantization: timedelta,
        resolution: timedelta
    ):
        self.horizon = horizon
        self.quantization = quantization
        self.resolution = resolution

    def required_run(self, now: datetime):
        start = self._quantize(now)


        slots = int(
            self.horizon.total_seconds()
            / self.resolution.total_seconds()
        )
        return ForecastRunRequirement(
            start=start,
            slots=slots,
            resolution_seconds=round(self.resolution.total_seconds())
        )

    def required_period(self, now: datetime) -> ForecastPeriod:
        start = self._quantize(now)

        return ForecastPeriod(
            start=start,
            end=start + self.horizon,
        )

    def _quantize(self, timestamp: datetime) -> datetime:
        seconds = int(timestamp.timestamp())
        quantum = int(self.quantization.total_seconds())

        quantized_seconds = (
            seconds // quantum
        ) * quantum

        return datetime.fromtimestamp(
            quantized_seconds,
            tz=timestamp.tzinfo,
        )