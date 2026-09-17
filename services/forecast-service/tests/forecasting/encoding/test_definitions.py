import json

import pytest

from app.forecasting.encoding.definitions import (
    DEFAULT_QUANTILE_DEFINITION,
    DEFAULT_QUANTILES,
    ScalarDefinition,
    QuantileDefinition,
    definition_from_payload,
)


def test_default_definition_matching_current_payload():
    assert DEFAULT_QUANTILES == (5.0, 50.0, 95.0)
    assert DEFAULT_QUANTILE_DEFINITION.serialize() == json.dumps(
        {"type": "quantile", "quantiles": [5, 50, 95]}
    )
    assert DEFAULT_QUANTILE_DEFINITION.arity() == 3


def test_quantile_definition_stores_percent_levels():
    definition = QuantileDefinition([10, 50, 100])
    assert definition.has(10)
    assert definition.index(50) == 1
    assert not definition.has(0.5)


def test_quantile_definition_sorts_levels():
    definition = QuantileDefinition([95, 5, 50])
    assert definition.quantiles == (5.0, 50.0, 95.0)


def test_serialized_and_parsed_definition_roundtrip():
    definition = QuantileDefinition([10, 25, 50, 90])
    assert definition_from_payload(definition.serialize()) == definition


def test_scalar_definition_roundtrip():
    definition = definition_from_payload(ScalarDefinition().serialize())
    assert definition == ScalarDefinition()
    assert definition.arity() == 1


def test_unknown_definition_type_rejected():
    with pytest.raises(ValueError):
        definition_from_payload(json.dumps({"type": "weird"}))
