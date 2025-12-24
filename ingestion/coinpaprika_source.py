"""CoinPaprika ingestion using the official SDK."""

from coinpaprika import client as Coinpaprika

from services.rate_limiter import rate_limited
from services.backoff import simple_retry


_client = Coinpaprika.Client()


def _fetch() -> list[dict]:
    """Fetch tickers from CoinPaprika via the SDK."""

    with rate_limited():
        # The SDK exposes high-level helpers like `tickers()`.
        return _client.tickers()


def fetch_coinpaprika() -> list[dict]:
    """Public entrypoint used by the ETL runner.

    Wrapped in a simple retry helper for resilience.
    """

    return simple_retry(_fetch)
