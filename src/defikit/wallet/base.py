"""Base wallet interface."""

from abc import ABC, abstractmethod
from typing import Optional

from ..core.types import Address, Transaction


class BaseWallet(ABC):
    """Abstract base class for wallet implementations."""

    @abstractmethod
    async def get_address(self) -> Address:
        """Get wallet address.

        Returns:
            Wallet address
        """
        pass

    @abstractmethod
    async def sign_transaction(self, tx: Transaction) -> bytes:
        """Sign a transaction.

        Args:
            tx: Transaction to sign

        Returns:
            Signed transaction bytes
        """
        pass

    @abstractmethod
    async def send_transaction(self, tx: Transaction) -> str:
        """Sign and send a transaction.

        Args:
            tx: Transaction to send

        Returns:
            Transaction hash
        """
        pass
