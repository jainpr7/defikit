"""Contract loading and ABI caching."""

from typing import Any, Optional

from web3 import AsyncWeb3

from ..core.provider import AsyncProvider
from ..core.types import Address
from .abi import load_abi


class Contract:
    """Wrapper for interacting with smart contracts."""

    def __init__(
        self,
        address: Address,
        abi: list[dict[str, Any]],
        provider: AsyncProvider,
    ):
        """Initialize contract.

        Args:
            address: Contract address
            abi: Contract ABI
            provider: Async provider instance
        """
        self.address = address
        self.abi = abi
        self.provider = provider
        self._w3_contract = provider.w3.eth.contract(address=address, abi=abi)

    @classmethod
    def from_abi_name(
        cls, address: Address, abi_name: str, provider: AsyncProvider
    ) -> "Contract":
        """Create a contract from a bundled ABI.

        Args:
            address: Contract address
            abi_name: Name of the ABI file (without .json)
            provider: Async provider instance

        Returns:
            Contract instance
        """
        abi = load_abi(abi_name)
        return cls(address, abi, provider)

    async def call_function(
        self,
        function_name: str,
        *args: Any,
        block: str = "latest",
        **kwargs: Any,
    ) -> Any:
        """Call a contract function.

        Args:
            function_name: Name of the function to call
            *args: Positional arguments for the function
            block: Block identifier
            **kwargs: Keyword arguments for the function

        Returns:
            Function return value
        """
        function = self._w3_contract.functions[function_name]
        return await function(*args, **kwargs).call(block_identifier=block)

    def encode_function_data(
        self,
        function_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> bytes:
        """Encode function call data.

        Args:
            function_name: Name of the function
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function

        Returns:
            Encoded function call data
        """
        function = self._w3_contract.functions[function_name]
        return function(*args, **kwargs).build_transaction({"to": self.address})["data"]

    async def estimate_gas(
        self,
        function_name: str,
        *args: Any,
        from_address: Optional[Address] = None,
        **kwargs: Any,
    ) -> int:
        """Estimate gas for a function call.

        Args:
            function_name: Name of the function
            *args: Positional arguments for the function
            from_address: Address to simulate the call from
            **kwargs: Keyword arguments for the function

        Returns:
            Estimated gas
        """
        function = self._w3_contract.functions[function_name]
        tx_params = {"to": self.address}
        if from_address:
            tx_params["from"] = from_address

        return await function(*args, **kwargs).estimate_gas(tx_params)


def get_contract(
    address: Address, abi_name: str, provider: AsyncProvider
) -> Contract:
    """Get a contract instance.

    Args:
        address: Contract address
        abi_name: Name of the ABI file
        provider: Async provider instance

    Returns:
        Contract instance
    """
    return Contract.from_abi_name(address, abi_name, provider)
