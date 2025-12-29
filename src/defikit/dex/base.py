"""Base DEX interface."""

from abc import ABC, abstractmethod
from typing import Optional

from ..core.types import Address, Quote, Pool


class BaseDEX(ABC):
    """Abstract base class for DEX implementations."""

    @abstractmethod
    async def get_quote(
        self,
        token_in: Address,
        token_out: Address,
        amount_in: int,
        fee_tier: Optional[int] = None,
    ) -> Quote:
        """Get a quote for swapping tokens.

        Args:
            token_in: Input token address
            token_out: Output token address
            amount_in: Input amount
            fee_tier: Fee tier (for DEXs that support it)

        Returns:
            Quote object
        """
        pass

    @abstractmethod
    async def swap(
        self,
        quote: Quote,
        recipient: Address,
        slippage_bps: int = 50,
        deadline: Optional[int] = None,
    ) -> bytes:
        """Build swap transaction calldata.

        Args:
            quote: Quote from get_quote
            recipient: Recipient address
            slippage_bps: Slippage tolerance in basis points
            deadline: Transaction deadline timestamp

        Returns:
            Encoded transaction data
        """
        pass

    @abstractmethod
    async def get_pools(
        self, token_a: Address, token_b: Address
    ) -> list[Pool]:
        """Get available pools for a token pair.

        Args:
            token_a: First token address
            token_b: Second token address

        Returns:
            List of Pool objects
        """
        pass
