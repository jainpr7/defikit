"""Gas analytics and estimation (stub)."""

from ..core.provider import AsyncProvider
from ..core.types import Wei


class GasAnalytics:
    """Gas analytics utilities."""

    def __init__(self, provider: AsyncProvider):
        """Initialize gas analytics.

        Args:
            provider: Async provider instance
        """
        self.provider = provider

    async def get_current_gas_price(self) -> Wei:
        """Get current gas price.

        Returns:
            Current gas price in wei
        """
        return await self.provider.get_gas_price()

    async def estimate_gas(self, tx_params: dict) -> int:  # type: ignore[type-arg]
        """Estimate gas for a transaction.

        Args:
            tx_params: Transaction parameters

        Returns:
            Estimated gas
        """
        return await self.provider.estimate_gas(tx_params)  # type: ignore[arg-type]
