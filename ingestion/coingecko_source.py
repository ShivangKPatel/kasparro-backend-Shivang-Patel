import requests
from services.rate_limiter import rate_limited
from services.backoff import retry_with_backoff

BASE_URL = "https://api.coingecko.com/api/v3/coins/markets"

@rate_limited(10, 60)
def _fetch():
    r = requests.get(
        BASE_URL,
        params={
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 50,
            "page": 1
        },
        timeout=10
    )
    r.raise_for_status()
    return r.json()

def fetch_coingecko():
    return retry_with_backoff(_fetch)
