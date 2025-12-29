"""Pytest configuration and fixtures."""

from unittest.mock import AsyncMock

import pytest

from defikit.core import AsyncProvider, DefiKitConfig


@pytest.fixture
def mock_provider():
    """Create a mock async provider."""
    provider = AsyncMock(spec=AsyncProvider)
    provider.get_chain_id = AsyncMock(return_value=1)
    provider.get_block_number = AsyncMock(return_value=18000000)
    provider.get_balance = AsyncMock(return_value=1000000000000000000)  # 1 ETH
    provider.get_gas_price = AsyncMock(return_value=30000000000)  # 30 gwei
    return provider


@pytest.fixture
def config():
    """Create a test configuration."""
    return DefiKitConfig(
        default_rpc_url="https://eth.llamarpc.com",
        max_retries=3,
        request_timeout=30,
    )


@pytest.fixture
def test_addresses():
    """Provide commonly used test addresses."""
    return {
        "zero": "0x0000000000000000000000000000000000000000",
        "weth": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "usdc": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "usdt": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "dai": "0x6B175474E89094C44Da98b954EedeC8992F8dC2",
        "vitalik": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    }
