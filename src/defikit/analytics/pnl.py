"""PnL tracking (stub)."""


class PnL:
    """Profit and loss tracking utilities."""

    @staticmethod
    def calculate(
        initial_value: float, current_value: float
    ) -> dict[str, float]:
        """Calculate PnL.

        Args:
            initial_value: Initial value
            current_value: Current value

        Returns:
            Dictionary with PnL metrics
        """
        pnl = current_value - initial_value
        pnl_pct = (pnl / initial_value * 100) if initial_value != 0 else 0

        return {
            "pnl": pnl,
            "pnl_pct": pnl_pct,
            "initial_value": initial_value,
            "current_value": current_value,
        }
