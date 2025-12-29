"""Event parsing and streaming utilities."""

from dataclasses import dataclass
from typing import Any, Optional

from eth_abi import decode
from eth_typing import HexStr
from eth_utils import event_abi_to_log_topic

from ..core.provider import AsyncProvider
from ..core.types import Address, BlockIdentifier


@dataclass
class Event:
    """Represents a decoded event."""

    name: str
    address: Address
    block_number: int
    transaction_hash: HexStr
    log_index: int
    args: dict[str, Any]
    raw_log: dict[str, Any]


def decode_event(
    event_abi: dict[str, Any], log: dict[str, Any]
) -> Event:
    """Decode an event log.

    Args:
        event_abi: The event ABI
        log: The raw log data

    Returns:
        Decoded event
    """
    # Get indexed and non-indexed inputs
    indexed_inputs = [inp for inp in event_abi["inputs"] if inp.get("indexed", False)]
    non_indexed_inputs = [inp for inp in event_abi["inputs"] if not inp.get("indexed", False)]

    # Decode indexed parameters from topics (skip first topic which is event signature)
    indexed_args = {}
    for i, inp in enumerate(indexed_inputs):
        topic_index = i + 1  # +1 because topics[0] is the event signature
        if topic_index < len(log["topics"]):
            topic_data = bytes.fromhex(log["topics"][topic_index].hex()[2:])
            # For indexed parameters, decode them
            if inp["type"] in ["address", "uint256", "int256", "bool", "bytes32"]:
                (value,) = decode([inp["type"]], topic_data)
                indexed_args[inp["name"]] = value
            else:
                # For complex types, the topic is the hash
                indexed_args[inp["name"]] = topic_data

    # Decode non-indexed parameters from data
    non_indexed_args = {}
    if non_indexed_inputs and log["data"] != "0x":
        data = bytes.fromhex(log["data"][2:] if log["data"].startswith("0x") else log["data"])
        types = [inp["type"] for inp in non_indexed_inputs]
        decoded = decode(types, data)
        for inp, value in zip(non_indexed_inputs, decoded):
            non_indexed_args[inp["name"]] = value

    # Combine all arguments
    args = {**indexed_args, **non_indexed_args}

    return Event(
        name=event_abi["name"],
        address=Address(log["address"]),
        block_number=log["blockNumber"],
        transaction_hash=log["transactionHash"].hex() if hasattr(log["transactionHash"], "hex") else log["transactionHash"],
        log_index=log["logIndex"],
        args=args,
        raw_log=log,
    )


async def get_events(
    provider: AsyncProvider,
    event_abi: dict[str, Any],
    from_block: BlockIdentifier = "latest",
    to_block: BlockIdentifier = "latest",
    address: Optional[Address] = None,
) -> list[Event]:
    """Get events matching the event ABI.

    Args:
        provider: Async provider instance
        event_abi: The event ABI
        from_block: Starting block
        to_block: Ending block
        address: Filter by contract address

    Returns:
        List of decoded events
    """
    # Get event signature topic
    event_topic = event_abi_to_log_topic(event_abi)

    # Get logs
    logs = await provider.get_logs(
        from_block=from_block,
        to_block=to_block,
        address=address,
        topics=[event_topic.hex()],
    )

    # Decode events
    return [decode_event(event_abi, log) for log in logs]


class EventStream:
    """Stream events in real-time."""

    def __init__(
        self,
        provider: AsyncProvider,
        event_abi: dict[str, Any],
        address: Optional[Address] = None,
        poll_interval: float = 1.0,
    ):
        """Initialize event stream.

        Args:
            provider: Async provider instance
            event_abi: The event ABI
            address: Filter by contract address
            poll_interval: Polling interval in seconds
        """
        self.provider = provider
        self.event_abi = event_abi
        self.address = address
        self.poll_interval = poll_interval
        self.last_block: Optional[int] = None

    async def __aiter__(self) -> "EventStream":
        """Async iterator initialization."""
        return self

    async def __anext__(self) -> list[Event]:
        """Get next batch of events."""
        import asyncio

        # Wait for poll interval
        await asyncio.sleep(self.poll_interval)

        # Get current block
        current_block = await self.provider.get_block_number()

        # Determine from_block
        from_block = self.last_block + 1 if self.last_block is not None else current_block

        # Get events
        events = await get_events(
            self.provider,
            self.event_abi,
            from_block=from_block,
            to_block=current_block,
            address=self.address,
        )

        # Update last block
        self.last_block = current_block

        return events
