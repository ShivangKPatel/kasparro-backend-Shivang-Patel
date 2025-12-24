"""Simple placeholder rate limiter utilities."""

import time
from contextlib import contextmanager


@contextmanager
def rate_limited():
    """Dummy context manager for rate limiting."""

    # TODO: implement real rate limiting
    yield
    time.sleep(0)
