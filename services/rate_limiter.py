"""Rate limiter utilities.

Supports two usage patterns:
1. Decorator: @rate_limited(max_calls, period)
2. Context manager: with rate_limited(): ...
"""

import time
import threading
from contextlib import contextmanager
from functools import wraps
from typing import Callable, TypeVar

T = TypeVar("T")

# Simple token-bucket state (thread-safe)
_lock = threading.Lock()
_tokens: dict[str, list] = {}  # bucket_id -> [tokens, last_refill_time]


def _get_bucket(bucket_id: str, max_tokens: int, refill_period: float) -> bool:
    """Try to consume a token. Returns True if allowed, False if rate-limited."""
    now = time.time()
    with _lock:
        if bucket_id not in _tokens:
            _tokens[bucket_id] = [max_tokens, now]
        tokens, last_refill = _tokens[bucket_id]
        # Refill tokens based on elapsed time
        elapsed = now - last_refill
        refill_amount = int(elapsed / refill_period * max_tokens)
        tokens = min(max_tokens, tokens + refill_amount)
        _tokens[bucket_id][1] = now
        if tokens > 0:
            _tokens[bucket_id][0] = tokens - 1
            return True
        return False


def rate_limited(max_calls: int = 10, period: float = 60.0):
    """Decorator or context-manager factory for rate limiting.

    Usage as decorator:
        @rate_limited(10, 60)
        def my_func(): ...

    Usage as context manager:
        with rate_limited():
            do_something()
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        bucket_id = f"{func.__module__}.{func.__name__}"

        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            # Wait until we can proceed
            while not _get_bucket(bucket_id, max_calls, period):
                time.sleep(0.1)
            return func(*args, **kwargs)
        return wrapper

    # If called with no args (as context manager), return a simple context manager
    if callable(max_calls):
        # rate_limited was used without parentheses as @rate_limited
        func = max_calls
        bucket_id = f"{func.__module__}.{func.__name__}"

        @wraps(func)
        def wrapper(*args, **kwargs):
            while not _get_bucket(bucket_id, 10, 60.0):
                time.sleep(0.1)
            return func(*args, **kwargs)
        return wrapper

    return decorator


@contextmanager
def rate_limited_context(max_calls: int = 10, period: float = 60.0):
    """Context manager version of rate limiting."""
    bucket_id = "context_manager_default"
    while not _get_bucket(bucket_id, max_calls, period):
        time.sleep(0.1)
    yield
