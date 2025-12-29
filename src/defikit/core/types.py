"""Common types for DeFiKit."""

from dataclasses import dataclass
from decimal import Decimal
from typing import NewType

from eth_typing import ChecksumAddress, HexStr

# Type aliases
Address = NewType("Address", ChecksumAddress)
Wei = NewType("Wei", int)
BlockIdentifier = int | str | HexStr


@dataclass
class TokenAmount:
    """Represents a token amount with its decimals."""

    raw: Wei
    decimals: int

    @property
    def formatted(self) -> Decimal:
        """Return the formatted amount as a Decimal."""
        return Decimal(self.raw) / Decimal(10**self.decimals)

    @classmethod
    def from_formatted(
        cls, amount: str | float | Decimal, decimals: int
    ) -> "TokenAmount":
        """Create a TokenAmount from a formatted amount."""
        raw = int(Decimal(str(amount)) * Decimal(10**decimals))
        return cls(raw=Wei(raw), decimals=decimals)

    def __str__(self) -> str:
        return f"{self.formatted}"

    def __repr__(self) -> str:
        return f"TokenAmount(raw={self.raw}, decimals={self.decimals}, formatted={self.formatted})"


@dataclass
class TokenInfo:
    """Information about a token."""

    address: Address
    name: str
    symbol: str
    decimals: int
    total_supply: Wei | None = None


@dataclass
class Price:
    """Represents a price from an oracle."""

    value: Decimal
    quote_currency: str
    timestamp: int
    source: str

    def __str__(self) -> str:
        return f"{self.value} {self.quote_currency}"


@dataclass
class Quote:
    """Represents a DEX swap quote."""

    token_in: Address
    token_out: Address
    amount_in: TokenAmount
    amount_out: TokenAmount
    price_impact: Decimal
    route: list[Address]
    gas_estimate: int | None = None

    @property
    def price(self) -> Decimal:
        """Calculate the price of token_out in terms of token_in."""
        if self.amount_in.formatted == 0:
            return Decimal(0)
        return self.amount_out.formatted / self.amount_in.formatted

    def __str__(self) -> str:
        return f"Quote({self.amount_in} -> {self.amount_out}, impact={self.price_impact}%)"


@dataclass
class Pool:
    """Represents a liquidity pool."""

    address: Address
    token0: Address
    token1: Address
    reserve0: TokenAmount
    reserve1: TokenAmount
    fee_tier: int | None = None

    @property
    def price_token0(self) -> Decimal:
        """Price of token0 in terms of token1."""
        if self.reserve0.formatted == 0:
            return Decimal(0)
        return self.reserve1.formatted / self.reserve0.formatted

    @property
    def price_token1(self) -> Decimal:
        """Price of token1 in terms of token0."""
        if self.reserve1.formatted == 0:
            return Decimal(0)
        return self.reserve0.formatted / self.reserve1.formatted


@dataclass
class Transaction:
    """Represents a transaction."""

    to: Address
    data: bytes
    value: Wei = Wei(0)
    gas: int | None = None
    gas_price: Wei | None = None
    nonce: int | None = None


@dataclass
class TransactionReceipt:
    """Represents a transaction receipt."""

    transaction_hash: HexStr
    block_number: int
    block_hash: HexStr
    gas_used: int
    status: int
    logs: list[dict]

    @property
    def success(self) -> bool:
        """Check if the transaction was successful."""
        return self.status == 1
