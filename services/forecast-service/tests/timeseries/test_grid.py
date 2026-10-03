from datetime import datetime, timedelta, timezone

import numpy as np
import pytest

from app.forecasting.enums import ForecastMetric
from app.timeseries.domain import TimeRange
from app.timeseries.grid import (
    aligned_values,
    build_run,
    interpolate_missing,
)

SLOT = timedelta(hours=1)
RANGE = TimeRange(
    start=datetime(2024, 12, 4, 9, 0, tzinfo=timezone.utc),
    end=datetime(2024, 12, 4, 12, 0, tzinfo=timezone.utc),
    resolution=SLOT,
)


def test_aligned_values_offsets_source_onto_target_grid():
    source = build_run(
        ForecastMetric.DAY_AHEAD_ELECTRICITY_PRICE,
        TimeRange(
            start=datetime(2024, 12, 4, 8, 0, tzinfo=timezone.utc),
            end=datetime(2024, 12, 4, 10, 0, tzinfo=timezone.utc),
            resolution=SLOT,
        ),
        [1.0, 2.0, 3.0],
    )

    values = aligned_values(source, RANGE)

    # source covers 08:00..11:00; target grid wants 09:00..12:00,
    # where the last target slot has no source value
    assert values == [2.0, 3.0, None]


def test_aligned_values_rejects_resolution_mismatch():
    source = build_run(
        ForecastMetric.TEMPERATURE,
        TimeRange(start=RANGE.start, end=RANGE.start, resolution=timedelta(minutes=15)),
        [],
    )

    with pytest.raises(ValueError, match="resolution"):
        aligned_values(source, RANGE)


def test_interpolate_missing_fills_gaps():
    values = interpolate_missing([None, 1.0, None, 3.0])

    assert values == pytest.approx([1.0, 1.0, 2.0, 3.0])


def test_interpolate_missing_rejects_all_missing():
    with pytest.raises(ValueError, match="usable"):
        interpolate_missing([None, None])
