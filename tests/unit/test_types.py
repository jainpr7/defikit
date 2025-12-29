"""Unit tests for types."""

import pytest
from decimal import Decimal

from defikit.core.types import TokenAmount, Wei


def test_token_amount_formatted():
    """Test TokenAmount formatted property."""
    amount = TokenAmount(raw=Wei(1000000), decimals=6)
    assert amount.formatted == Decimal("1.0")

    amount = TokenAmount(raw=Wei(1500000), decimals=6)
    assert amount.formatted == Decimal("1.5")


def test_token_amount_from_formatted():
    """Test TokenAmount.from_formatted()."""
    amount = TokenAmount.from_formatted("1.5", decimals=6)
    assert amount.raw == 1500000
    assert amount.decimals == 6

    amount = TokenAmount.from_formatted(2.5, decimals=18)
    assert amount.raw == 2500000000000000000
    assert amount.decimals == 18


def test_token_amount_str():
    """Test TokenAmount string representation."""
    amount = TokenAmount(raw=Wei(1500000), decimals=6)
    assert str(amount) == "1.5"
