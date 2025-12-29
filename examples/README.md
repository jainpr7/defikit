# DeFiKit Examples

This directory contains example scripts demonstrating various features of DeFiKit.

## Running the Examples

Make sure you have installed DeFiKit:

```bash
pip install defikit
# OR for development
pip install -e ".[dev]"
```

Then run any example:

```bash
python examples/01_basic_token_info.py
python examples/02_analytics.py
```

## Available Examples

### 01_basic_token_info.py
Demonstrates basic functionality:
- Initializing DeFiKit
- Working with TokenAmount types
- Accessing chain configuration
- Basic analytics (APY, IL)

### 02_analytics.py
Shows analytics capabilities:
- APY/APR conversions
- Impermanent loss calculations
- P&L tracking

## More Examples Coming Soon

Additional examples are planned for:
- Token operations (balance checks, transfers)
- DEX trading (quotes, swaps)
- Lending protocols (supply, borrow)
- Price oracles
- Portfolio tracking
- Trading bots

## Note on RPC URLs

These examples use public RPC endpoints which may have rate limits. For production use, consider:
- Using a paid RPC provider (Alchemy, Infura, etc.)
- Setting up your own node
- Using environment variables for configuration

Example with environment variables:

```bash
export DEFIKIT_DEFAULT_RPC_URL="your-rpc-url"
export DEFIKIT_ALCHEMY_API_KEY="your-api-key"
python examples/01_basic_token_info.py
```
