"""Base oracle interface."""

from abc import ABC, abstractmethod

from ..core.types import Address, Price


class BaseOracle(ABC):
    """Abstract base class for oracle implementations."""

    @abstractmethod
    async def get_price(
        self, asset: Address, quote_currency: str = "USD"
    ) -> Price:
        """Get price for an asset.

        Args:
            asset: Asset address or symbol
            quote_currency: Quote currency

        Returns:
            Price object
        """
        pass

    @abstractmethod
    async def get_prices(
        self, assets: list[Address], quote_currency: str = "USD"
    ) -> dict[Address, Price]:
        """Get prices for multiple assets.

        Args:
            assets: List of asset addresses
            quote_currency: Quote currency

        Returns:
            Dictionary mapping addresses to prices
        """
        pass

    def is_stale(self, price: Price, max_age_seconds: int = 3600) -> bool:
        """Check if a price is stale.

        Args:
            price: Price object
            max_age_seconds: Maximum age in seconds

        Returns:
            True if stale, False otherwise
        """
        import time

        return (int(time.time()) - price.timestamp) > max_age_seconds
