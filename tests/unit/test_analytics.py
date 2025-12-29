"""Unit tests for analytics."""

import pytest
from decimal import Decimal

from defikit.analytics import APY, ImpermanentLoss


def test_apr_to_apy():
    """Test APR to APY conversion."""
    # 5% APR compounded daily should be ~5.13% APY
    apy = APY.from_apr(0.05, compound_frequency=365)
    assert abs(apy - Decimal("0.0512")) < Decimal("0.0001")


def test_apy_to_apr():
    """Test APY to APR conversion."""
    apr = APY.to_apr(0.05123, compound_frequency=365)
    assert abs(apr - Decimal("0.05")) < Decimal("0.0001")


def test_impermanent_loss():
    """Test impermanent loss calculation."""
    # Price doubles (2x)
    il = ImpermanentLoss.calculate(
        initial_price=1000,
        current_price=2000,
    )

    # 2x price change should result in ~5.72% IL
    assert abs(il["impermanent_loss_pct"]) > 5
    assert abs(il["impermanent_loss_pct"]) < 6
