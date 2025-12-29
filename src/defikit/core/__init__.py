"""Core module for DeFiKit."""

from .config import DefiKitConfig
from .chain import ChainConfig, CHAINS, get_chain, get_chain_by_id
from .provider import AsyncProvider
from .contracts import Contract, get_contract
from .types import (
    Address,
    Wei,
    BlockIdentifier,
    TokenAmount,
    TokenInfo,
    Price,
    Quote,
    Pool,
    Transaction,
    TransactionReceipt,
)
from .exceptions import (
    DeFiKitError,
    ConfigurationError,
    ProviderError,
    ChainNotSupportedError,
    ContractError,
    TokenError,
    InsufficientBalanceError,
    InsufficientAllowanceError,
    DEXError,
    InsufficientLiquidityError,
    SlippageExceededError,
    LendingError,
    InsufficientCollateralError,
    HealthFactorTooLowError,
    OracleError,
    StalePriceError,
    WalletError,
    TransactionError,
    TransactionRevertedError,
    TransactionTimeoutError,
    ABIError,
    EncodingError,
    DecodingError,
)

__all__ = [
    # Config
    "DefiKitConfig",
    # Chain
    "ChainConfig",
    "CHAINS",
    "get_chain",
    "get_chain_by_id",
    # Provider
    "AsyncProvider",
    # Contracts
    "Contract",
    "get_contract",
    # Types
    "Address",
    "Wei",
    "BlockIdentifier",
    "TokenAmount",
    "TokenInfo",
    "Price",
    "Quote",
    "Pool",
    "Transaction",
    "TransactionReceipt",
    # Exceptions
    "DeFiKitError",
    "ConfigurationError",
    "ProviderError",
    "ChainNotSupportedError",
    "ContractError",
    "TokenError",
    "InsufficientBalanceError",
    "InsufficientAllowanceError",
    "DEXError",
    "InsufficientLiquidityError",
    "SlippageExceededError",
    "LendingError",
    "InsufficientCollateralError",
    "HealthFactorTooLowError",
    "OracleError",
    "StalePriceError",
    "WalletError",
    "TransactionError",
    "TransactionRevertedError",
    "TransactionTimeoutError",
    "ABIError",
    "EncodingError",
    "DecodingError",
]
