"""Batch RPC calls using Multicall3."""

from dataclasses import dataclass
from typing import cast

from eth_abi import decode
from eth_typing import ChecksumAddress

from ..core.provider import AsyncProvider
from ..core.types import Address
from .abi import load_abi
from .encoding import encode_function_data


@dataclass
class Call:
    """Represents a call in a multicall batch."""

    target: Address
    calldata: bytes
    allow_failure: bool = False


@dataclass
class CallResult:
    """Result of a multicall call."""

    success: bool
    return_data: bytes


class Multicall:
    """Utility for batching multiple contract calls into a single RPC request."""

    MULTICALL3_ADDRESS = Address(cast(ChecksumAddress, "0xcA11bde05977b3631167028862bE2a173976CA11"))

    def __init__(self, provider: AsyncProvider, multicall_address: Address | None = None):
        """Initialize Multicall.

        Args:
            provider: Async provider instance
            multicall_address: Custom Multicall3 address (uses default if None)
        """
        self.provider = provider
        self.multicall_address = multicall_address or self.MULTICALL3_ADDRESS
        self.abi = load_abi("multicall3")

    async def call(self, calls: list[Call]) -> list[CallResult]:
        """Execute multiple calls in a single RPC request.

        Args:
            calls: List of calls to execute

        Returns:
            List of call results
        """
        # Prepare calls data
        calls_data = [
            (call.target, call.allow_failure, call.calldata) for call in calls
        ]

        # Encode the aggregate3 function call
        calldata = encode_function_data(
            "aggregate3((address,bool,bytes)[])",
            [calls_data]
        )

        # Execute the multicall
        result_data = await self.provider.call(
            {
                "to": self.multicall_address,
                "data": calldata,
            }
        )

        # Decode results
        # aggregate3 returns (bool success, bytes returnData)[]
        (results,) = decode(
            ["(bool,bytes)[]"],
            result_data
        )

        return [
            CallResult(success=success, return_data=return_data)
            for success, return_data in results
        ]

    async def aggregate(self, calls: list[Call]) -> list[bytes]:
        """Execute calls and return only successful results.

        Args:
            calls: List of calls to execute

        Returns:
            List of return data from successful calls

        Raises:
            Exception: If any call fails when allow_failure is False
        """
        results = await self.call(calls)

        return_data = []
        for i, result in enumerate(results):
            if not result.success and not calls[i].allow_failure:
                raise Exception(f"Multicall: Call {i} failed")
            if result.success:
                return_data.append(result.return_data)

        return return_data

    async def try_aggregate(
        self, calls: list[Call], require_success: bool = False
    ) -> list[CallResult]:
        """Execute calls with optional failure handling.

        Args:
            calls: List of calls to execute
            require_success: If True, revert if any call fails

        Returns:
            List of call results
        """
        # Prepare calls data
        calls_data = [(call.target, call.calldata) for call in calls]

        # Encode the tryAggregate function call
        calldata = encode_function_data(
            "tryAggregate(bool,(address,bytes)[])",
            [require_success, calls_data]
        )

        # Execute the multicall
        result_data = await self.provider.call(
            {
                "to": self.multicall_address,
                "data": calldata,
            }
        )

        # Decode results
        (results,) = decode(
            ["(bool,bytes)[]"],
            result_data
        )

        return [
            CallResult(success=success, return_data=return_data)
            for success, return_data in results
        ]


async def batch_call(
    provider: AsyncProvider,
    calls: list[tuple[Address, bytes]],
    multicall_address: Address | None = None,
) -> list[bytes]:
    """Convenience function for batch calling.

    Args:
        provider: Async provider instance
        calls: List of (target, calldata) tuples
        multicall_address: Custom Multicall3 address

    Returns:
        List of return data
    """
    multicall = Multicall(provider, multicall_address)
    call_objects = [Call(target=target, calldata=calldata) for target, calldata in calls]
    return await multicall.aggregate(call_objects)
