"""Provider interface for grid constraints.

No grid capacity data exists yet; the interface and the "unavailable"
placeholder follow the storage context pattern.
"""


class GridConstraintsProvider:

    def get(
        self,
        portfolio_id: int,
        market: str,
        window,
    ):
        """Return grid constraints for the window, or None if unavailable."""


class GridConstraintsUnavailableProvider(GridConstraintsProvider):

    def get(
        self,
        portfolio_id: int,
        market: str,
        window,
    ):
        return None
