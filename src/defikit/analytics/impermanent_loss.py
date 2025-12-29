"""Impermanent loss calculation."""

from decimal import Decimal


def calculate_impermanent_loss(
    initial_price: float | Decimal,
    current_price: float | Decimal,
) -> Decimal:
    """Calculate impermanent loss percentage.

    Args:
        initial_price: Initial price ratio
        current_price: Current price ratio

    Returns:
        Impermanent loss as a decimal (e.g., 0.0557 for 5.57% loss)
    """
    initial = Decimal(str(initial_price))
    current = Decimal(str(current_price))

    # Calculate price ratio change
    price_ratio = current / initial
    sqrt_ratio = price_ratio.sqrt()

    # IL = 2 * sqrt(ratio) / (1 + ratio) - 1
    il = 2 * sqrt_ratio / (1 + price_ratio) - 1

    return il


class ImpermanentLoss:
    """Impermanent loss calculation utilities."""

    @staticmethod
    def calculate(
        initial_price: float | Decimal,
        current_price: float | Decimal,
        initial_amount_a: float | Decimal = 1.0,
        initial_amount_b: float | Decimal = 1.0,
    ) -> dict[str, Decimal]:
        """Calculate impermanent loss with detailed breakdown.

        Args:
            initial_price: Initial price of token A in terms of token B
            current_price: Current price of token A in terms of token B
            initial_amount_a: Initial amount of token A
            initial_amount_b: Initial amount of token B

        Returns:
            Dictionary with IL percentage and value comparisons
        """
        il_pct = calculate_impermanent_loss(initial_price, current_price)

        initial_a = Decimal(str(initial_amount_a))
        initial_b = Decimal(str(initial_amount_b))
        curr_price = Decimal(str(current_price))

        # Calculate what would have happened if just holding
        hold_value = initial_a * curr_price + initial_b

        # Calculate actual LP value
        # Using constant product formula: k = x * y
        k = initial_a * initial_b
        current_a = (k / curr_price).sqrt()
        current_b = (k * curr_price).sqrt()
        lp_value = current_a * curr_price + current_b

        return {
            "impermanent_loss_pct": il_pct * 100,  # As percentage
            "hold_value": hold_value,
            "lp_value": lp_value,
            "difference": lp_value - hold_value,
        }
