"""ERC721 NFT utilities (stub)."""

from ..core.provider import AsyncProvider
from ..core.types import Address


class ERC721:
    """Utility class for interacting with ERC721 NFTs."""

    def __init__(self, token_address: Address, provider: AsyncProvider):
        """Initialize ERC721 utility.

        Args:
            token_address: Address of the ERC721 token
            provider: Async provider instance
        """
        self.address = token_address
        self.provider = provider

    async def balance_of(self, owner: Address) -> int:
        """Get NFT balance of an owner.

        Args:
            owner: Address to check balance of

        Returns:
            Number of NFTs owned
        """
        # TODO: Implement
        raise NotImplementedError("ERC721 functionality not yet implemented")

    async def owner_of(self, token_id: int) -> Address:
        """Get owner of a specific token ID.

        Args:
            token_id: Token ID

        Returns:
            Owner address
        """
        # TODO: Implement
        raise NotImplementedError("ERC721 functionality not yet implemented")
