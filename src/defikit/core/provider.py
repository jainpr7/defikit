"""Async RPC provider wrapper with retry logic."""

import asyncio
from typing import Any

from eth_typing import HexStr
from web3 import AsyncHTTPProvider, AsyncWeb3
from web3.types import BlockIdentifier as Web3BlockIdentifier
from web3.types import TxParams

from .exceptions import ProviderError, TransactionTimeoutError
from .types import Address, BlockIdentifier, TransactionReceipt, Wei


class AsyncProvider:
    """Async wrapper for Web3 provider with retry logic and failover."""

    def __init__(
        self,
        rpc_url: str,
        fallback_urls: list[str] | None = None,
        max_retries: int = 3,
        timeout: int = 30,
        retry_delay: float = 1.0,
    ):
        """Initialize the async provider.

        Args:
            rpc_url: Primary RPC URL
            fallback_urls: List of fallback RPC URLs
            max_retries: Maximum number of retries per request
            timeout: Request timeout in seconds
            retry_delay: Delay between retries in seconds
        """
        self.rpc_url = rpc_url
        self.fallback_urls = fallback_urls or []
        self.max_retries = max_retries
        self.timeout = timeout
        self.retry_delay = retry_delay

        # Initialize primary Web3 instance
        self.w3 = AsyncWeb3(
            AsyncHTTPProvider(rpc_url, request_kwargs={"timeout": timeout})
        )

        # Initialize fallback instances
        self.fallback_w3_instances = [
            AsyncWeb3(AsyncHTTPProvider(url, request_kwargs={"timeout": timeout}))
            for url in self.fallback_urls
        ]

    async def _execute_with_retry(
        self, func: Any, *args: Any, **kwargs: Any
    ) -> Any:
        """Execute a function with retry logic and failover."""
        all_providers = [self.w3] + self.fallback_w3_instances

        for provider_idx, provider in enumerate(all_providers):
            for attempt in range(self.max_retries):
                try:
                    result = await func(provider, *args, **kwargs)
                    return result
                except Exception as e:
                    is_last_attempt = attempt == self.max_retries - 1
                    is_last_provider = provider_idx == len(all_providers) - 1

                    if is_last_attempt and is_last_provider:
                        raise ProviderError(
                            f"All providers failed after {self.max_retries} retries: {str(e)}"
                        ) from e

                    if not is_last_attempt:
                        await asyncio.sleep(self.retry_delay * (2**attempt))

        raise ProviderError("All providers exhausted")

    async def get_chain_id(self) -> int:
        """Get the chain ID."""

        async def _get_chain_id(provider: AsyncWeb3) -> int:
            return await provider.eth.chain_id

        return await self._execute_with_retry(_get_chain_id)

    async def get_block_number(self) -> int:
        """Get the current block number."""

        async def _get_block_number(provider: AsyncWeb3) -> int:
            return await provider.eth.block_number

        return await self._execute_with_retry(_get_block_number)

    async def get_block(
        self, block_identifier: BlockIdentifier = "latest"
    ) -> dict[str, Any]:
        """Get a block by number or identifier."""

        async def _get_block(
            provider: AsyncWeb3, block_id: Web3BlockIdentifier
        ) -> dict[str, Any]:
            return dict(await provider.eth.get_block(block_id))

        return await self._execute_with_retry(_get_block, block_identifier)

    async def get_balance(self, address: Address) -> Wei:
        """Get the ETH balance of an address."""

        async def _get_balance(provider: AsyncWeb3, addr: Address) -> Wei:
            balance = await provider.eth.get_balance(addr)
            return Wei(balance)

        return await self._execute_with_retry(_get_balance, address)

    async def call(
        self, tx: TxParams, block: BlockIdentifier = "latest"
    ) -> bytes:
        """Execute a contract call without creating a transaction."""

        async def _call(
            provider: AsyncWeb3, transaction: TxParams, block_id: Web3BlockIdentifier
        ) -> bytes:
            result = await provider.eth.call(transaction, block_id)
            return bytes(result)

        return await self._execute_with_retry(_call, tx, block)

    async def estimate_gas(self, tx: TxParams) -> int:
        """Estimate gas for a transaction."""

        async def _estimate_gas(provider: AsyncWeb3, transaction: TxParams) -> int:
            return await provider.eth.estimate_gas(transaction)

        return await self._execute_with_retry(_estimate_gas, tx)

    async def get_transaction_count(self, address: Address) -> int:
        """Get the transaction count (nonce) for an address."""

        async def _get_transaction_count(provider: AsyncWeb3, addr: Address) -> int:
            return await provider.eth.get_transaction_count(addr)

        return await self._execute_with_retry(_get_transaction_count, address)

    async def send_raw_transaction(self, raw_tx: bytes) -> HexStr:
        """Send a raw signed transaction."""

        async def _send_raw_transaction(
            provider: AsyncWeb3, raw_transaction: bytes
        ) -> HexStr:
            return await provider.eth.send_raw_transaction(raw_transaction)  # type: ignore[return-value]

        return await self._execute_with_retry(_send_raw_transaction, raw_tx)

    async def get_transaction(self, tx_hash: HexStr) -> dict[str, Any]:
        """Get a transaction by hash."""

        async def _get_transaction(
            provider: AsyncWeb3, hash: HexStr
        ) -> dict[str, Any]:
            return dict(await provider.eth.get_transaction(hash))

        return await self._execute_with_retry(_get_transaction, tx_hash)

    async def get_transaction_receipt(self, tx_hash: HexStr) -> TransactionReceipt:
        """Get a transaction receipt."""

        async def _get_transaction_receipt(
            provider: AsyncWeb3, hash: HexStr
        ) -> TransactionReceipt:
            receipt = await provider.eth.get_transaction_receipt(hash)
            return TransactionReceipt(
                transaction_hash=receipt["transactionHash"].hex(),  # type: ignore[arg-type]
                block_number=receipt["blockNumber"],
                block_hash=receipt["blockHash"].hex(),  # type: ignore[arg-type]
                gas_used=receipt["gasUsed"],
                status=receipt["status"],
                logs=[dict(log) for log in receipt["logs"]],
            )

        return await self._execute_with_retry(_get_transaction_receipt, tx_hash)

    async def wait_for_transaction(
        self, tx_hash: HexStr, timeout: int = 120, poll_latency: float = 0.5
    ) -> TransactionReceipt:
        """Wait for a transaction to be mined."""
        start_time = asyncio.get_event_loop().time()

        while True:
            try:
                receipt = await self.get_transaction_receipt(tx_hash)
                return receipt
            except Exception as e:
                elapsed = asyncio.get_event_loop().time() - start_time
                if elapsed >= timeout:
                    raise TransactionTimeoutError(
                        f"Transaction {tx_hash} not mined after {timeout} seconds"
                    ) from e
                await asyncio.sleep(poll_latency)

    async def get_gas_price(self) -> Wei:
        """Get the current gas price."""

        async def _get_gas_price(provider: AsyncWeb3) -> Wei:
            gas_price = await provider.eth.gas_price
            return Wei(gas_price)

        return await self._execute_with_retry(_get_gas_price)

    async def get_logs(
        self,
        from_block: BlockIdentifier = "latest",
        to_block: BlockIdentifier = "latest",
        address: Address | None = None,
        topics: list[HexStr] | None = None,
    ) -> list[dict[str, Any]]:
        """Get logs matching filter criteria."""

        async def _get_logs(
            provider: AsyncWeb3,
            from_blk: Web3BlockIdentifier,
            to_blk: Web3BlockIdentifier,
            addr: Address | None,
            topic_list: list[HexStr] | None,
        ) -> list[dict[str, Any]]:
            filter_params: dict[str, Any] = {
                "fromBlock": from_blk,
                "toBlock": to_blk,
            }
            if addr:
                filter_params["address"] = addr
            if topic_list:
                filter_params["topics"] = topic_list

            logs = await provider.eth.get_logs(filter_params)  # type: ignore[arg-type]
            return [dict(log) for log in logs]

        return await self._execute_with_retry(
            _get_logs, from_block, to_block, address, topics
        )

    @property
    def eth(self) -> Any:
        """Access to the underlying eth module."""
        return self.w3.eth
