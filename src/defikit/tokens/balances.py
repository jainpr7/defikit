"""Batch balance queries using multicall."""

from eth_abi import decode

from ..core.provider import AsyncProvider
from ..core.types import Address, TokenAmount
from ..utils.encoding import encode_function_data
from ..utils.multicall import Call, Multicall


async def get_balances(
    wallet_address: Address,
    token_addresses: list[Address],
    provider: AsyncProvider,
    multicall_address: Address | None = None,
) -> dict[Address, TokenAmount]:
    """Get balances for multiple tokens in a single call.

    Args:
        wallet_address: Wallet address to check balances for
        token_addresses: List of token addresses
        provider: Async provider instance
        multicall_address: Custom multicall address

    Returns:
        Dictionary mapping token addresses to balances
    """
    multicall = Multicall(provider, multicall_address)

    # Create calls for balanceOf and decimals for each token
    calls = []
    for token in token_addresses:
        # balanceOf call
        balance_calldata = encode_function_data(
            "balanceOf(address)", [wallet_address]
        )
        calls.append(Call(target=token, calldata=balance_calldata, allow_failure=True))

        # decimals call
        decimals_calldata = encode_function_data("decimals()", [])
        calls.append(Call(target=token, calldata=decimals_calldata, allow_failure=True))

    # Execute multicall
    results = await multicall.call(calls)

    # Parse results
    balances = {}
    for i in range(0, len(results), 2):
        token = token_addresses[i // 2]
        balance_result = results[i]
        decimals_result = results[i + 1]

        if balance_result.success and decimals_result.success:
            (balance,) = decode(["uint256"], balance_result.return_data)
            (decimals,) = decode(["uint8"], decimals_result.return_data)
            balances[token] = TokenAmount(raw=balance, decimals=decimals)

    return balances


async def get_eth_and_token_balances(
    wallet_address: Address,
    token_addresses: list[Address],
    provider: AsyncProvider,
    multicall_address: Address | None = None,
) -> dict[str, TokenAmount]:
    """Get ETH and token balances in a single call.

    Args:
        wallet_address: Wallet address to check balances for
        token_addresses: List of token addresses
        provider: Async provider instance
        multicall_address: Custom multicall address

    Returns:
        Dictionary with 'ETH' and token addresses as keys
    """
    # Get ETH balance
    eth_balance = await provider.get_balance(wallet_address)

    # Get token balances
    token_balances = await get_balances(
        wallet_address, token_addresses, provider, multicall_address
    )

    # Combine results
    result = {
        "ETH": TokenAmount(raw=eth_balance, decimals=18),
        **token_balances,
    }

    return result
