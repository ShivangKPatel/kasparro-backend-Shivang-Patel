"""Retry / backoff helpers.

Exports two helpers used across the codebase:
- `simple_retry(func, retries, delay)` — fixed-delay retry for simple SDK calls
- `retry_with_backoff(func, retries, base_delay, factor)` — exponential backoff wrapper

Both accept a callable with no arguments and return its result or re-raise the final
exception after the allotted retries.
"""

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


def retry_with_backoff(func: Callable[[], T], retries: int = 5, base_delay: float = 0.5, factor: float = 2.0) -> T:
    """Call `func()` with exponential backoff retries.

    Args:
        func: callable taking no arguments.
        retries: number of attempts (including the first).
        base_delay: initial delay in seconds.
        factor: multiplier applied each retry (exponential growth).

    Returns:
        The return value of `func()` on success.

    Raises:
        The last exception raised by `func()` if all retries fail.
    """
    delay = base_delay
    for attempt in range(retries):
        try:
            return func()
        except Exception:  # noqa: BLE001
            if attempt == retries - 1:
                raise
            time.sleep(delay)
            delay *= factor
