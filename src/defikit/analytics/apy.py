"""APY and APR calculation utilities."""

from decimal import Decimal
from typing import Union


def apr_to_apy(apr: Union[float, Decimal], compound_frequency: int = 365) -> Decimal:
    """Convert APR to APY.

    Args:
        apr: Annual Percentage Rate (as decimal, e.g., 0.05 for 5%)
        compound_frequency: Number of times interest compounds per year

    Returns:
        Annual Percentage Yield as Decimal
    """
    apr_decimal = Decimal(str(apr))
    frequency = Decimal(str(compound_frequency))

    # APY = (1 + APR/n)^n - 1
    apy = (1 + apr_decimal / frequency) ** frequency - 1
    return apy


def apy_to_apr(apy: Union[float, Decimal], compound_frequency: int = 365) -> Decimal:
    """Convert APY to APR.

    Args:
        apy: Annual Percentage Yield (as decimal, e.g., 0.05123 for 5.123%)
        compound_frequency: Number of times interest compounds per year

    Returns:
        Annual Percentage Rate as Decimal
    """
    apy_decimal = Decimal(str(apy))
    frequency = Decimal(str(compound_frequency))

    # APR = n * ((1 + APY)^(1/n) - 1)
    apr = frequency * ((1 + apy_decimal) ** (1 / frequency) - 1)
    return apr


def calculate_apy(
    principal: Union[float, Decimal],
    interest_earned: Union[float, Decimal],
    period_days: int = 365,
) -> Decimal:
    """Calculate APY from principal and interest earned.

    Args:
        principal: Initial principal amount
        interest_earned: Interest earned over the period
        period_days: Number of days in the period

    Returns:
        APY as Decimal
    """
    principal_decimal = Decimal(str(principal))
    interest_decimal = Decimal(str(interest_earned))
    days = Decimal(str(period_days))

    # Calculate return rate for the period
    period_return = interest_decimal / principal_decimal

    # Annualize it
    periods_per_year = Decimal("365") / days
    apy = (1 + period_return) ** periods_per_year - 1

    return apy


class APY:
    """APY calculation utilities."""

    @staticmethod
    def from_apr(
        apr: Union[float, Decimal], compound_frequency: int = 365
    ) -> Decimal:
        """Convert APR to APY."""
        return apr_to_apy(apr, compound_frequency)

    @staticmethod
    def to_apr(apy: Union[float, Decimal], compound_frequency: int = 365) -> Decimal:
        """Convert APY to APR."""
        return apy_to_apr(apy, compound_frequency)

    @staticmethod
    def calculate(
        principal: Union[float, Decimal],
        interest_earned: Union[float, Decimal],
        period_days: int = 365,
    ) -> Decimal:
        """Calculate APY from principal and interest."""
        return calculate_apy(principal, interest_earned, period_days)
