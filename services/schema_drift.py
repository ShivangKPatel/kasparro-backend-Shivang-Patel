"""Schema drift detection placeholder."""


def detect_schema_drift(expected: dict, actual: dict) -> dict:
    """Return a simple diff between expected and actual schemas."""
    expected_keys = set(expected.keys())
    actual_keys = set(actual.keys())

    return {
        "missing": list(expected_keys - actual_keys),
        "extra": list(actual_keys - expected_keys),
    }
