"""Approval management utilities (stub)."""

from ..core.provider import AsyncProvider
from ..core.types import Address, Wei


async def approve_token(
    token_address: Address,
    spender: Address,
    amount: Wei,
    provider: AsyncProvider,
) -> bytes:
    """Approve token spending.

    Args:
        token_address: Address of the token
        spender: Address to approve
        amount: Amount to approve
        provider: Async provider instance

    Returns:
        Encoded transaction data
    """
    # TODO: Implement
    raise NotImplementedError("Approval functionality not yet implemented")
