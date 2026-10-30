"""Provider interface for storage context (battery state).

No real storage data exists yet; the provider interface and the
"unavailable" placeholder implementation are in place so strategies can
declare the storage requirement now.
"""


class StorageContextProvider:

    def get(
        self,
        portfolio_id: int,
        market: str,
        window,
    ):
        """Return a storage context for the window, or None if unavailable."""


class StorageContextUnavailableProvider(StorageContextProvider):

    def get(
        self,
        portfolio_id: int,
        market: str,
        window,
    ):
        return None
