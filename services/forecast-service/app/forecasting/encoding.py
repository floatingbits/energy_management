import json

DEFAULT_QUANTILES = [5, 50, 95]


def quantile_definition(quantiles=DEFAULT_QUANTILES) -> str:
    """Value type definition for quantile-encoded payloads."""
    return json.dumps({"type": "quantile", "quantiles": list(quantiles)})


def serialize_quantiles(p05, p50, p95) -> str:
    """Serialize a quantile triple into a JSON array payload."""
    return json.dumps([p05, p50, p95])


def parse_quantiles(payload: str):
    """Parse a JSON array payload back into the (p05, p50, p95) triple."""
    values = json.loads(payload)
    p05, p50, p95 = values
    return p05, p50, p95
