"""Analytics calculations example.

This example demonstrates DeFiKit's analytics capabilities:
- APY/APR conversions
- Impermanent loss calculations
- P&L tracking
"""

import asyncio
from decimal import Decimal

from defikit.analytics import APY, ImpermanentLoss, PnL


async def main():
    """Main example function."""
    print("=== DeFiKit Analytics Example ===\n")

    # APY/APR Conversions
    print("=== APY/APR Conversions ===")
    apr = Decimal("0.10")  # 10% APR
    apy_daily = APY.from_apr(apr, compound_frequency=365)
    apy_monthly = APY.from_apr(apr, compound_frequency=12)
    print(f"10% APR:")
    print(f"  - Compounded daily: {apy_daily:.4%} APY")
    print(f"  - Compounded monthly: {apy_monthly:.4%} APY")

    # Convert back
    apr_from_apy = APY.to_apr(apy_daily, compound_frequency=365)
    print(f"  - Converted back to APR: {apr_from_apy:.4%}")
    print()

    # Impermanent Loss for different price changes
    print("=== Impermanent Loss Analysis ===")
    price_changes = [0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0]

    print("Price Ratio | Impermanent Loss")
    print("-" * 35)
    for ratio in price_changes:
        il_result = ImpermanentLoss.calculate(
            initial_price=1000,
            current_price=1000 * ratio,
        )
        print(f"{ratio:>7.2f}x    | {il_result['impermanent_loss_pct']:>7.2f}%")
    print()

    # Detailed IL calculation
    print("=== Detailed IL Calculation ===")
    il_detail = ImpermanentLoss.calculate(
        initial_price=2000,
        current_price=3000,
        initial_amount_a=1.0,
        initial_amount_b=2000,
    )
    print(f"Initial price: $2000")
    print(f"Current price: $3000")
    print(f"Impermanent Loss: {il_detail['impermanent_loss_pct']:.2f}%")
    print(f"Hold value: ${il_detail['hold_value']:.2f}")
    print(f"LP value: ${il_detail['lp_value']:.2f}")
    print(f"Difference: ${il_detail['difference']:.2f}")
    print()

    # P&L Tracking
    print("=== P&L Tracking ===")
    pnl = PnL.calculate(initial_value=10000, current_value=12500)
    print(f"Initial Investment: ${pnl['initial_value']:.2f}")
    print(f"Current Value: ${pnl['current_value']:.2f}")
    print(f"Profit/Loss: ${pnl['pnl']:.2f} ({pnl['pnl_pct']:+.2f}%)")

    print("\n=== Example Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
