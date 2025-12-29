"""Custom exception hierarchy for DeFiKit."""


class DeFiKitError(Exception):
    """Base exception for all DeFiKit errors."""

    pass


class ConfigurationError(DeFiKitError):
    """Raised when there is a configuration error."""

    pass


class ProviderError(DeFiKitError):
    """Raised when there is an error with the RPC provider."""

    pass


class ChainNotSupportedError(DeFiKitError):
    """Raised when a chain is not supported."""

    pass


class ContractError(DeFiKitError):
    """Raised when there is an error with a contract interaction."""

    pass


class TokenError(DeFiKitError):
    """Raised when there is an error with token operations."""

    pass


class InsufficientBalanceError(TokenError):
    """Raised when an account has insufficient balance."""

    pass


class InsufficientAllowanceError(TokenError):
    """Raised when an account has insufficient allowance."""

    pass


class DEXError(DeFiKitError):
    """Raised when there is an error with DEX operations."""

    pass


class InsufficientLiquidityError(DEXError):
    """Raised when there is insufficient liquidity for a swap."""

    pass


class SlippageExceededError(DEXError):
    """Raised when slippage exceeds tolerance."""

    pass


class LendingError(DeFiKitError):
    """Raised when there is an error with lending protocol operations."""

    pass


class InsufficientCollateralError(LendingError):
    """Raised when there is insufficient collateral."""

    pass


class HealthFactorTooLowError(LendingError):
    """Raised when health factor is too low for an operation."""

    pass


class OracleError(DeFiKitError):
    """Raised when there is an error with price oracle operations."""

    pass


class StalePriceError(OracleError):
    """Raised when a price is stale."""

    pass


class WalletError(DeFiKitError):
    """Raised when there is an error with wallet operations."""

    pass


class TransactionError(DeFiKitError):
    """Raised when there is an error with transaction operations."""

    pass


class TransactionRevertedError(TransactionError):
    """Raised when a transaction reverts."""

    pass


class TransactionTimeoutError(TransactionError):
    """Raised when a transaction times out."""

    pass


class ABIError(DeFiKitError):
    """Raised when there is an error with ABI operations."""

    pass


class EncodingError(DeFiKitError):
    """Raised when there is an error encoding data."""

    pass


class DecodingError(DeFiKitError):
    """Raised when there is an error decoding data."""

    pass
