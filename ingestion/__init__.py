class BaseSource:
    """Base interface for upstream data sources."""

    def fetch_latest(self):  # type: ignore[override]
        raise NotImplementedError

    def fetch_since(self, cursor):  # type: ignore[override]
        raise NotImplementedError
