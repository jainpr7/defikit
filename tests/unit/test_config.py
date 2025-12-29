"""Unit tests for configuration."""

from defikit.core import DefiKitConfig


def test_config_defaults():
    """Test configuration default values."""
    config = DefiKitConfig()

    assert config.default_rpc_url == "https://eth.llamarpc.com"
    assert config.default_slippage_bps == 50
    assert config.max_retries == 3
    assert config.request_timeout == 30


def test_config_custom_values():
    """Test configuration with custom values."""
    config = DefiKitConfig(
        default_rpc_url="https://custom.rpc",
        default_slippage_bps=100,
        max_retries=5,
    )

    assert config.default_rpc_url == "https://custom.rpc"
    assert config.default_slippage_bps == 100
    assert config.max_retries == 5


def test_config_get_rpc_url():
    """Test getting RPC URL for a chain."""
    config = DefiKitConfig(
        default_rpc_url="https://eth.llamarpc.com",
        rpc_urls={"arbitrum": "https://arb.llamarpc.com"},
    )

    assert config.get_rpc_url("ethereum") == "https://eth.llamarpc.com"
    assert config.get_rpc_url("arbitrum") == "https://arb.llamarpc.com"
