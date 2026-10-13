"""Decode forecast-service TimeSeriesGroup JSON into shared domain runs."""

from datetime import datetime, timedelta
from em_timeseries.domain import TimeSeries, TimeSeriesValue, TimeSeriesTimeBase
from em_timeseries.encoding import definition_from_payload
from em_timeseries.grid import TimeSeriesRun


def runs_from_group_payload(payload: dict) -> list[TimeSeriesRun]:
    """Turn a TimeSeriesGroupResponse payload into one run per series.

    Slot values missing in the payload come back as all-None entries so
    the run always has exactly `slots` values.
    """
    tb = payload["time_series_time_base"]
    base = TimeSeriesTimeBase(
        start=datetime.fromisoformat(tb["start"]),
        resolution=timedelta(seconds=tb["resolution_seconds"]),
        slots=tb["slots"],
    )

    runs = []
    for series_payload in payload["time_series"]:
        definition = definition_from_payload(series_payload["value_type_definition"])
        arity = definition.arity()
        empty = TimeSeriesValue(values=(None,) * arity)

        ordered = {
            value["slot_index"]: TimeSeriesValue(values=tuple(value["values"]))
            for value in series_payload.get("values", [])
        }
        values = [
            ordered.get(slot_index, empty)
            for slot_index in range(tb["slots"])
        ]

        runs.append(
            TimeSeriesRun(
                base=base,
                series=TimeSeries(
                    metric=series_payload["metric"],
                    values=values,
                    value_definition=definition,
                ),
            ),
        )

    return runs
