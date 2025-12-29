"""Chain definitions and registry."""

from dataclasses import dataclass
from typing import Optional

from .exceptions import ChainNotSupportedError
from .types import Address


@dataclass
class ChainConfig:
    """Configuration for a blockchain network."""

    chain_id: int
    name: str
    native_token: str
    native_decimals: int = 18
    block_time: float = 12.0
    explorer_url: str = ""

    # Core addresses
    multicall3: Address
    weth: Address

    # DEX addresses
    uniswap_v2_router: Optional[Address] = None
    uniswap_v2_factory: Optional[Address] = None
    uniswap_v3_router: Optional[Address] = None
    uniswap_v3_factory: Optional[Address] = None
    uniswap_v3_quoter: Optional[Address] = None
    sushiswap_router: Optional[Address] = None

    # Lending addresses
    aave_v3_pool: Optional[Address] = None
    aave_v3_pool_data_provider: Optional[Address] = None
    compound_v3_usdc: Optional[Address] = None

    # Common tokens
    usdc: Optional[Address] = None
    usdt: Optional[Address] = None
    dai: Optional[Address] = None


# Chain registry
CHAINS: dict[str, ChainConfig] = {
    "ethereum": ChainConfig(
        chain_id=1,
        name="Ethereum",
        native_token="ETH",
        explorer_url="https://etherscan.io",
        multicall3=Address("0xcA11bde05977b3631167028862bE2a173976CA11"),
        weth=Address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"),
        uniswap_v2_router=Address("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"),
        uniswap_v2_factory=Address("0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"),
        uniswap_v3_router=Address("0xE592427A0AEce92De3Edee1F18E0157C05861564"),
        uniswap_v3_factory=Address("0x1F98431c8aD98523631AE4a59f267346ea31F984"),
        uniswap_v3_quoter=Address("0x61fFE014bA17989E743c5F6cB21bF9697530B21e"),
        aave_v3_pool=Address("0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"),
        usdc=Address("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"),
        usdt=Address("0xdAC17F958D2ee523a2206206994597C13D831ec7"),
        dai=Address("0x6B175474E89094C44Da98b954EedeC8992F8dC2"),
    ),
    "arbitrum": ChainConfig(
        chain_id=42161,
        name="Arbitrum One",
        native_token="ETH",
        block_time=0.25,
        explorer_url="https://arbiscan.io",
        multicall3=Address("0xcA11bde05977b3631167028862bE2a173976CA11"),
        weth=Address("0x82aF49447D8a07e3bd95BD0d56f35241523fBab1"),
        uniswap_v3_router=Address("0xE592427A0AEce92De3Edee1F18E0157C05861564"),
        uniswap_v3_factory=Address("0x1F98431c8aD98523631AE4a59f267346ea31F984"),
        aave_v3_pool=Address("0x794a61358D6845594F94dc1DB02A252b5b4814aD"),
        usdc=Address("0xaf88d065e77c8cC2239327C5EDb3A432268e5831"),
    ),
    "base": ChainConfig(
        chain_id=8453,
        name="Base",
        native_token="ETH",
        block_time=2.0,
        explorer_url="https://basescan.org",
        multicall3=Address("0xcA11bde05977b3631167028862bE2a173976CA11"),
        weth=Address("0x4200000000000000000000000000000000000006"),
        uniswap_v3_router=Address("0x2626664c2603336E57B271c5C0b26F421741e481"),
        uniswap_v3_factory=Address("0x33128a8fC17869897dcE68Ed026d694621f6FDfD"),
        aave_v3_pool=Address("0xA238Dd80C259a72e81d7e4664a9801593F98d1c5"),
        usdc=Address("0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"),
    ),
    "polygon": ChainConfig(
        chain_id=137,
        name="Polygon",
        native_token="MATIC",
        block_time=2.0,
        explorer_url="https://polygonscan.com",
        multicall3=Address("0xcA11bde05977b3631167028862bE2a173976CA11"),
        weth=Address("0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"),  # WMATIC
        uniswap_v3_router=Address("0xE592427A0AEce92De3Edee1F18E0157C05861564"),
        uniswap_v3_factory=Address("0x1F98431c8aD98523631AE4a59f267346ea31F984"),
        aave_v3_pool=Address("0x794a61358D6845594F94dc1DB02A252b5b4814aD"),
        usdc=Address("0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359"),
    ),
    "optimism": ChainConfig(
        chain_id=10,
        name="Optimism",
        native_token="ETH",
        block_time=2.0,
        explorer_url="https://optimistic.etherscan.io",
        multicall3=Address("0xcA11bde05977b3631167028862bE2a173976CA11"),
        weth=Address("0x4200000000000000000000000000000000000006"),
        uniswap_v3_router=Address("0xE592427A0AEce92De3Edee1F18E0157C05861564"),
        aave_v3_pool=Address("0x794a61358D6845594F94dc1DB02A252b5b4814aD"),
        usdc=Address("0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85"),
    ),
    "bsc": ChainConfig(
        chain_id=56,
        name="BNB Smart Chain",
        native_token="BNB",
        block_time=3.0,
        explorer_url="https://bscscan.com",
        multicall3=Address("0xcA11bde05977b3631167028862bE2a173976CA11"),
        weth=Address("0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"),  # WBNB
        usdc=Address("0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"),
    ),
}


def get_chain(chain: str) -> ChainConfig:
    """Get chain configuration by name."""
    chain_lower = chain.lower()
    if chain_lower not in CHAINS:
        raise ChainNotSupportedError(f"Chain '{chain}' is not supported")
    return CHAINS[chain_lower]


def get_chain_by_id(chain_id: int) -> ChainConfig:
    """Get chain configuration by chain ID."""
    for chain in CHAINS.values():
        if chain.chain_id == chain_id:
            return chain
    raise ChainNotSupportedError(f"Chain ID {chain_id} is not supported")
