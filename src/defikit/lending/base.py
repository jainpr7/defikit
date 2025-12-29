"""Base lending interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from ..core.types import Address, TokenAmount


@dataclass
class Market:
    """Lending market information."""

    asset: Address
    symbol: str
    supply_apy: Decimal
    borrow_apy: Decimal
    total_supply: TokenAmount
    total_borrow: TokenAmount
    utilization: Decimal
    ltv: Decimal
    liquidation_threshold: Decimal


@dataclass
class UserPosition:
    """User lending position."""

    total_collateral_usd: Decimal
    total_debt_usd: Decimal
    available_borrow_usd: Decimal
    health_factor: Decimal
    supplies: list[dict]
    borrows: list[dict]


class BaseLending(ABC):
    """Abstract base class for lending protocol implementations."""

    @abstractmethod
    async def get_markets(self) -> list[Market]:
        """Get all available markets.

        Returns:
            List of Market objects
        """
        pass

    @abstractmethod
    async def get_user_position(self, user: Address) -> UserPosition:
        """Get user position.

        Args:
            user: User address

        Returns:
            UserPosition object
        """
        pass

    @abstractmethod
    async def supply(
        self,
        asset: Address,
        amount: TokenAmount,
        on_behalf_of: Optional[Address] = None,
    ) -> bytes:
        """Build supply transaction calldata.

        Args:
            asset: Asset address
            amount: Amount to supply
            on_behalf_of: Address to supply on behalf of

        Returns:
            Encoded transaction data
        """
        pass

    @abstractmethod
    async def borrow(
        self,
        asset: Address,
        amount: TokenAmount,
        interest_rate_mode: int = 2,
    ) -> bytes:
        """Build borrow transaction calldata.

        Args:
            asset: Asset address
            amount: Amount to borrow
            interest_rate_mode: Interest rate mode (1=stable, 2=variable)

        Returns:
            Encoded transaction data
        """
        pass
