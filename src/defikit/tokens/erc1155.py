"""ERC1155 multi-token utilities (stub)."""

from ..core.provider import AsyncProvider
from ..core.types import Address


class ERC1155:
    """Utility class for interacting with ERC1155 tokens."""

    def __init__(self, token_address: Address, provider: AsyncProvider):
        """Initialize ERC1155 utility.

        Args:
            token_address: Address of the ERC1155 token
            provider: Async provider instance
        """
        self.address = token_address
        self.provider = provider

    async def balance_of(self, account: Address, token_id: int) -> int:
        """Get token balance.

        Args:
            account: Address to check balance of
            token_id: Token ID

        Returns:
            Balance amount
        """
        # TODO: Implement
        raise NotImplementedError("ERC1155 functionality not yet implemented")
