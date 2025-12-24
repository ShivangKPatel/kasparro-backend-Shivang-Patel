"""Retry / backoff helpers (placeholder)."""

import time
from typing import Callable, TypeVar

T = TypeVar("T")


def simple_retry(func: Callable[[], T], retries: int = 3, delay: float = 1.0) -> T:
    for attempt in range(retries):
        try:
            return func()
        except Exception:  # noqa: BLE001
            if attempt == retries - 1:
                raise
            time.sleep(delay)
