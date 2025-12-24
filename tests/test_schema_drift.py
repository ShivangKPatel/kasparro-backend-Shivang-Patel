from services.schema_drift import detect_schema_drift


def test_schema_drift_placeholder() -> None:
    diff = detect_schema_drift({"a": 1}, {"a": 1})
    assert diff["missing"] == []
    assert diff["extra"] == []
