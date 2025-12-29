# DeFiKit 🚀

A comprehensive, async-first Python DeFi utilities library for EVM chains.

[![CI](https://github.com/jainpr7/defikit/actions/workflows/ci.yml/badge.svg)](https://github.com/jainpr7/defikit/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/defikit.svg)](https://badge.fury.io/py/defikit)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🔄 **Async-first**: All blockchain I/O uses asyncio with sync wrappers available
- 🔗 **Multi-chain**: Support for Ethereum, Arbitrum, Optimism, Base, Polygon, BSC
- 🔀 **DEX Integrations**: Uniswap V2/V3/V4, SushiSwap, Curve, PancakeSwap
- 💰 **Lending Protocols**: Aave V2/V3, Compound V2/V3, Morpho
- 📊 **Price Oracles**: Chainlink, Pyth, Uniswap TWAP, multi-oracle aggregation
- 💼 **Wallet Management**: Hot wallets, Gnosis Safe integration
- 🪙 **Token Operations**: ERC20, ERC721, ERC1155 with batch operations
- 📈 **Analytics**: APY calculations, impermanent loss, PnL tracking, gas analytics
- 🔧 **Utilities**: Multicall, retry logic, event parsing, ABI caching
- 📝 **Type-safe**: Full type annotations with `py.typed` marker
- ⚙️ **Configurable**: Pydantic-based config with env/file support

## Installation

```bash
pip install defikit
```

For development:
```bash
pip install defikit[dev]
```

For documentation:
```bash
pip install defikit[docs]
```

## Quick Start

```python
import asyncio
from defikit import DeFiKit
from defikit.dex.uniswap import UniswapV3
from defikit.oracles import Chainlink

async def main():
    # Initialize with RPC URL
    kit = DeFiKit(rpc_url="https://eth.llamarpc.com")
    
    # Get token info
    usdc = await kit.tokens.get_info("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
    print(f"Token: {usdc.symbol}, Decimals: {usdc.decimals}")
    
    # Get balance
    balance = await kit.tokens.balance_of(
        usdc.address, 
        "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"  # vitalik.eth
    )
    print(f"Balance: {balance.formatted} {usdc.symbol}")
    
    # Get ETH price from Chainlink
    chainlink = Chainlink(kit.provider, chain="ethereum")
    eth_price = await chainlink.get_price("ETH")
    print(f"ETH Price: ${eth_price.value:.2f}")
    
    # Get swap quote from Uniswap V3
    uniswap = UniswapV3(kit.provider, chain="ethereum")
    quote = await uniswap.get_quote(
        token_in="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH
        token_out="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # USDC
        amount_in=kit.tokens.parse_amount("1.0", 18)
    )
    print(f"1 WETH = {quote.amount_out.formatted} USDC")

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

DeFiKit can be configured via environment variables, `.env` files, or programmatically:

```python
from defikit import DeFiKit, DefiKitConfig

# From environment variables (DEFIKIT_ prefix)
kit = DeFiKit()

# From .env file
kit = DeFiKit.from_env_file(".env")

# Programmatically
config = DefiKitConfig(
    default_rpc_url="https://eth.llamarpc.com",
    etherscan_api_key="your-api-key",
    default_slippage_bps=50,  # 0.5%
    max_retries=3
)
kit = DeFiKit(config=config)
```

### Environment Variables

```bash
DEFIKIT_DEFAULT_RPC_URL=https://eth.llamarpc.com
DEFIKIT_ETHERSCAN_API_KEY=your-api-key
DEFIKIT_ALCHEMY_API_KEY=your-api-key
DEFIKIT_INFURA_PROJECT_ID=your-project-id
DEFIKIT_DEFAULT_SLIPPAGE_BPS=50
DEFIKIT_MAX_GAS_PRICE_GWEI=100
```

## Supported Chains

- **Ethereum** (Chain ID: 1)
- **Arbitrum One** (Chain ID: 42161)
- **Optimism** (Chain ID: 10)
- **Base** (Chain ID: 8453)
- **Polygon** (Chain ID: 137)
- **BNB Smart Chain** (Chain ID: 56)

## Core Modules

### Token Operations

```python
# ERC20 operations
balance = await kit.tokens.balance_of(token_address, wallet_address)
await kit.tokens.approve(token_address, spender, amount)
await kit.tokens.transfer(token_address, to, amount)

# Batch balance queries with Multicall
balances = await kit.tokens.get_balances(wallet_address, [usdc, dai, usdt])

# ERC721 NFT operations
nft_balance = await kit.nft.balance_of(nft_address, wallet_address)
owner = await kit.nft.owner_of(nft_address, token_id)

# ERC1155 operations
balance = await kit.multi_token.balance_of(contract, wallet, token_id)
```

### DEX Trading

```python
from defikit.dex.uniswap import UniswapV2, UniswapV3

# Uniswap V2
v2 = UniswapV2(kit.provider, chain="ethereum")
quote = await v2.get_quote(token_in, token_out, amount_in)
tx_data = await v2.swap(quote, recipient, slippage_bps=50)

# Uniswap V3 with fee tiers
v3 = UniswapV3(kit.provider, chain="ethereum")
quote = await v3.get_quote(token_in, token_out, amount_in, fee_tier=3000)
pools = await v3.get_pools(token_a, token_b)

# Smart routing across DEXs
from defikit.dex.router import SmartRouter

router = SmartRouter(kit.provider, chain="ethereum")
best_quote = await router.get_best_quote(token_in, token_out, amount_in)
```

### Lending Protocols

```python
from defikit.lending.aave import AaveV3

aave = AaveV3(kit.provider, chain="ethereum")

# Get markets
markets = await aave.get_markets()
for market in markets:
    print(f"{market.symbol}: Supply APY {market.supply_apy}%, Borrow APY {market.borrow_apy}%")

# Get user position
position = await aave.get_user_position(user_address)
print(f"Health Factor: {position.health_factor}")
print(f"Total Collateral: ${position.total_collateral_usd}")
print(f"Total Debt: ${position.total_debt_usd}")

# Supply and borrow
supply_tx = await aave.supply(usdc_address, amount)
borrow_tx = await aave.borrow(dai_address, amount)
```

### Price Oracles

```python
from defikit.oracles import Chainlink, Pyth, UniswapTWAP, OracleAggregator

# Chainlink
chainlink = Chainlink(kit.provider, chain="ethereum")
eth_price = await chainlink.get_price("ETH", "USD")

# Pyth Network
pyth = Pyth(kit.provider, chain="ethereum")
btc_price = await pyth.get_price("BTC", "USD")

# Uniswap TWAP
twap = UniswapTWAP(kit.provider, chain="ethereum")
weth_usdc_price = await twap.get_twap(weth, usdc, period=3600)

# Multi-oracle aggregator with fallbacks
aggregator = OracleAggregator(kit.provider, chain="ethereum")
aggregator.add_oracle(chainlink)
aggregator.add_oracle(pyth)
aggregator.add_oracle(twap)

price = await aggregator.get_price("ETH", "USD")  # Uses first available
```

### Analytics

```python
from defikit.analytics import APY, ImpermanentLoss, PnL, GasAnalytics

# APY calculations
apy = APY.from_apr(apr=0.05, compound_frequency=365)
apr = APY.to_apr(apy=0.05123)

# Impermanent loss
il = ImpermanentLoss.calculate(
    initial_price=2000,
    current_price=2500,
    initial_amount_a=1.0,
    initial_amount_b=2000
)

# Gas analytics
gas = GasAnalytics(kit.provider)
current_gas = await gas.get_current_gas_price()
estimate = await gas.estimate_gas(tx_params)
```

## Examples

Check out the `examples/` directory for complete, runnable examples:

1. `01_basic_token_info.py` - Get token info and balances
2. `02_swap_tokens.py` - Perform a token swap
3. `03_provide_liquidity.py` - Add liquidity to a pool
4. `04_aave_supply_borrow.py` - Supply and borrow on Aave
5. `05_flash_loan.py` - Execute a flash loan
6. `06_price_monitoring.py` - Monitor prices from oracles
7. `07_portfolio_tracker.py` - Track portfolio across protocols
8. `08_trading_bot.py` - Simple arbitrage bot example

## Development

```bash
# Clone the repository
git clone https://github.com/jainpr7/defikit.git
cd defikit

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check src tests

# Run type checking
mypy src

# Install pre-commit hooks
pre-commit install
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=defikit --cov-report=html

# Run only unit tests
pytest tests/unit/

# Run only integration tests (requires Anvil)
pytest tests/integration/
```

## Documentation

Documentation is built with MkDocs and Material theme:

```bash
pip install -e ".[docs]"
mkdocs serve
```

Visit http://127.0.0.1:8000 to view the documentation locally.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This software is provided "as is", without warranty of any kind. Use at your own risk. Always test thoroughly before using in production with real funds.

## Acknowledgments

- Built with [web3.py](https://github.com/ethereum/web3.py)
- Inspired by the Ethereum and DeFi communities
- Thanks to all contributors

## Support

- 📚 [Documentation](https://github.com/jainpr7/defikit#readme)
- 🐛 [Issue Tracker](https://github.com/jainpr7/defikit/issues)
- 💬 [Discussions](https://github.com/jainpr7/defikit/discussions)

## Roadmap

- [ ] Add more DEX integrations (Balancer, 1inch, 0x)
- [ ] Add staking protocol integrations
- [ ] Add yield aggregator integrations (Yearn, Beefy)
- [ ] Add portfolio management tools
- [ ] Add transaction simulation
- [ ] Add MEV protection
- [ ] Add L2 rollup specific features
- [ ] Add governance participation tools
