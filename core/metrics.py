"""Metrics setup (placeholder)."""

from prometheus_client import Counter

etl_runs_total = Counter("etl_runs_total", "Number of ETL runs executed")
