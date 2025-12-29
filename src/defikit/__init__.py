"""Main DeFiKit class."""

from .core import AsyncProvider, DefiKitConfig, get_chain
from .tokens import get_balance, get_balances, get_token_info


class DeFiKit:
    """Main DeFiKit class for interacting with DeFi protocols."""

    def __init__(
        self,
        rpc_url: str | None = None,
        config: DefiKitConfig | None = None,
        chain: str = "ethereum",
    ):
        """Initialize DeFiKit.

        Args:
            rpc_url: RPC URL (overrides config if provided)
            config: Configuration object
            chain: Chain name (default: ethereum)
        """
        if config is None:
            config = DefiKitConfig()

        if rpc_url is not None:
            config.default_rpc_url = rpc_url

        self.config = config
        self.chain = get_chain(chain)

        # Initialize provider
        self.provider = AsyncProvider(
            rpc_url=config.default_rpc_url,
            fallback_urls=list(config.rpc_urls.values()) if config.rpc_urls else None,
            max_retries=config.max_retries,
            timeout=config.request_timeout,
            retry_delay=config.retry_delay,
        )

    @classmethod
    def from_env_file(cls, env_file: str = ".env", chain: str = "ethereum") -> "DeFiKit":
        """Create DeFiKit instance from environment file.

        Args:
            env_file: Path to .env file
            chain: Chain name

        Returns:
            DeFiKit instance
        """
        # Note: pydantic-settings handles .env files automatically via env_file in model_config
        # For now, use default config which will read from .env
        config = DefiKitConfig()
        return cls(config=config, chain=chain)

    async def get_token_info(self, token_address: str):
        """Get token information.

        Args:
            token_address: Token address

        Returns:
            TokenInfo object
        """
        return await get_token_info(token_address, self.provider)

    async def get_balance(self, token_address: str, account: str):
        """Get token balance.

        Args:
            token_address: Token address
            account: Account address

        Returns:
            Token balance
        """
        return await get_balance(token_address, account, self.provider)

    async def get_balances(self, account: str, token_addresses: list[str]):
        """Get multiple token balances.

        Args:
            account: Account address
            token_addresses: List of token addresses

        Returns:
            Dictionary of balances
        """
        return await get_balances(account, token_addresses, self.provider)
