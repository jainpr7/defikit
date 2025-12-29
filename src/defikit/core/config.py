"""Configuration management for DeFiKit."""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DefiKitConfig(BaseSettings):
    """Configuration for DeFiKit with Pydantic validation."""

    model_config = SettingsConfigDict(
        env_prefix="DEFIKIT_", env_file=".env", extra="ignore"
    )

    # RPC Configuration
    default_rpc_url: str = Field(default="https://eth.llamarpc.com")
    rpc_urls: dict[str, str] = Field(default_factory=dict)

    # API Keys
    etherscan_api_key: Optional[str] = None
    alchemy_api_key: Optional[str] = None
    infura_project_id: Optional[str] = None

    # Transaction Settings
    default_slippage_bps: int = 50  # 0.5%
    default_deadline_seconds: int = 1200  # 20 minutes
    max_gas_price_gwei: Optional[float] = None

    # Provider Settings
    request_timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0

    def get_rpc_url(self, chain: str) -> str:
        """Get RPC URL for a specific chain."""
        return self.rpc_urls.get(chain, self.default_rpc_url)
