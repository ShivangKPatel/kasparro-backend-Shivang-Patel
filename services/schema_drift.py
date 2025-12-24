"""Schema drift detection placeholder."""


def detect_schema_drift(expected: dict, actual: dict) -> dict:
    """Return a simple diff between expected and actual schemas."""

    return {
        "missing": [k for k in expected.keys() - actual.keys()],
        "extra": [k for k in actual.keys() - expected.keys()],
    }
