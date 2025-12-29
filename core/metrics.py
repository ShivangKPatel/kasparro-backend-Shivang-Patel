"""Metrics setup (placeholder).

Expose named metrics that other modules expect (ETL_RUNS_TOTAL, ETL_FAILURES_TOTAL)
and keep lower-case aliases for backwards-compatibility.
"""

from prometheus_client import Counter

# Export upper-case names used by ingestion/runner.py
ETL_RUNS_TOTAL = Counter("etl_runs_total", "Number of ETL runs executed")
ETL_FAILURES_TOTAL = Counter("etl_failures_total", "Number of ETL failures")

# Backwards-compatible aliases
etl_runs_total = ETL_RUNS_TOTAL
etl_failures_total = ETL_FAILURES_TOTAL
