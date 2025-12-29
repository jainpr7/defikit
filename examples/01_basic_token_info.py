"""Basic token information example.

This example demonstrates how to:
- Initialize DeFiKit
- Get token information (name, symbol, decimals)
- Calculate token amounts with decimals
- Work with different chains
"""

import asyncio
from decimal import Decimal

from defikit import DeFiKit
from defikit.core.types import TokenAmount, Wei


async def main():
    """Main example function."""
    print("=== DeFiKit Basic Token Info Example ===\n")

    # Initialize DeFiKit for Ethereum mainnet
    print("Initializing DeFiKit for Ethereum...")
    kit = DeFiKit(
        rpc_url="https://eth.llamarpc.com",
        chain="ethereum"
    )
    print(f"Connected to: {kit.chain.name} (Chain ID: {kit.chain.chain_id})")
    print(f"Native token: {kit.chain.native_token}\n")

    # Example 1: Working with TokenAmount
    print("=== Example 1: TokenAmount ===")
    # Create a token amount from raw wei value
    amount = TokenAmount(raw=Wei(1500000), decimals=6)
    print(f"Raw: {amount.raw} wei")
    print(f"Formatted: {amount.formatted} USDC")

    # Create token amount from formatted value
    amount2 = TokenAmount.from_formatted("2.5", decimals=18)
    print(f"2.5 ETH = {amount2.raw} wei\n")

    # Example 2: Display chain information
    print("=== Example 2: Chain Configuration ===")
    print(f"Explorer: {kit.chain.explorer_url}")
    print(f"Block time: {kit.chain.block_time}s")
    print(f"Multicall3: {kit.chain.multicall3}")
    print(f"WETH: {kit.chain.weth}")
    if kit.chain.usdc:
        print(f"USDC: {kit.chain.usdc}")
    print()

    # Example 3: APY calculations
    print("=== Example 3: APY Calculations ===")
    from defikit.analytics import APY

    apr = Decimal("0.05")  # 5% APR
    apy = APY.from_apr(apr, compound_frequency=365)
    print(f"5% APR compounded daily = {apy:.4%} APY")

    # Example 4: Impermanent Loss
    print("\n=== Example 4: Impermanent Loss ===")
    from defikit.analytics import ImpermanentLoss

    il_result = ImpermanentLoss.calculate(
        initial_price=2000,  # Initial ETH price
        current_price=2500,  # Current ETH price
    )
    print(f"IL for 25% price increase: {il_result['impermanent_loss_pct']:.2f}%")

    print("\n=== Example Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
