import json

import pytest

from app.forecasting.encoding.definitions import (
    DEFAULT_QUANTILE_DEFINITION,
    ScalarDefinition,
    definition_from_payload,
)
from app.forecasting.encoding.serializers import (
    deserialize,
    parser_for,
    serialize_values,
)
from app.forecasting.domain.time_series_value import TimeSeriesValue


def test_quantile_parser_maps_levels_to_ordered_entries():
    value = TimeSeriesValue(values=(12.0, 34.0, 56.0))
    parser = parser_for(DEFAULT_QUANTILE_DEFINITION)

    assert parser.quantile(value, 5) == 12.0
    assert parser.quantile(value, 50) == 34.0
    assert parser.quantile(value, 95) == 56.0


def test_quantile_parser_unknown_level_raises():
    parser = parser_for(DEFAULT_QUANTILE_DEFINITION)
    value = TimeSeriesValue(values=(12.0, 34.0, 56.0))

    with pytest.raises(ValueError):
        parser.quantile(value, 0.5)


def test_padded_missing_entries_deserialize_and_access_as_none():
    parser = parser_for(DEFAULT_QUANTILE_DEFINITION)
    value = parser.parse("[12.0, 34.0, null]")

    assert value.values == (12.0, 34.0, None)
    assert parser.quantile(value, 95) is None


def test_payload_roundtrip_is_definition_ordered_and_length_checked():
    payload = serialize_values((1.0, 2.0, 3.0), DEFAULT_QUANTILE_DEFINITION)
    assert payload == json.dumps([1.0, 2.0, 3.0])
    assert deserialize(payload, DEFAULT_QUANTILE_DEFINITION) == (1.0, 2.0, 3.0)

    with pytest.raises(ValueError):
        serialize_values((1.0, 2.0), DEFAULT_QUANTILE_DEFINITION)
    with pytest.raises(ValueError):
        deserialize("[1.0]", DEFAULT_QUANTILE_DEFINITION)


def test_scalar_parser_is_non_parametric():
    parser = parser_for(ScalarDefinition())
    value = TimeSeriesValue(values=(73.5,))

    assert parser.scalar(value) == 73.5
    assert json.loads(parser.serialize(value)) == [73.5]


def test_parser_factory_rejects_unknown_definition():
    with pytest.raises(ValueError):
        parser_for(object())
