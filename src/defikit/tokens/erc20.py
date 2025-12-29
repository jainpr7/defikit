"""ERC20 token utilities."""

from ..core.contracts import get_contract
from ..core.provider import AsyncProvider
from ..core.types import Address, TokenAmount, TokenInfo, Wei
from ..utils.encoding import encode_function_data


class ERC20:
    """Utility class for interacting with ERC20 tokens."""

    def __init__(self, token_address: Address, provider: AsyncProvider):
        """Initialize ERC20 utility.

        Args:
            token_address: Address of the ERC20 token
            provider: Async provider instance
        """
        self.address = token_address
        self.provider = provider
        self.contract = get_contract(token_address, "erc20", provider)

    async def name(self) -> str:
        """Get token name."""
        return await self.contract.call_function("name")

    async def symbol(self) -> str:
        """Get token symbol."""
        return await self.contract.call_function("symbol")

    async def decimals(self) -> int:
        """Get token decimals."""
        return await self.contract.call_function("decimals")

    async def total_supply(self) -> Wei:
        """Get total token supply."""
        supply = await self.contract.call_function("totalSupply")
        return Wei(supply)

    async def balance_of(self, account: Address) -> TokenAmount:
        """Get token balance of an account.

        Args:
            account: Address to check balance of

        Returns:
            Token balance with decimals
        """
        balance = await self.contract.call_function("balanceOf", account)
        decimals = await self.decimals()
        return TokenAmount(raw=Wei(balance), decimals=decimals)

    async def allowance(self, owner: Address, spender: Address) -> TokenAmount:
        """Get allowance amount.

        Args:
            owner: Token owner address
            spender: Spender address

        Returns:
            Allowance amount with decimals
        """
        allowance_value = await self.contract.call_function("allowance", owner, spender)
        decimals = await self.decimals()
        return TokenAmount(raw=Wei(allowance_value), decimals=decimals)

    def encode_transfer(self, to: Address, amount: Wei) -> bytes:
        """Encode transfer function call.

        Args:
            to: Recipient address
            amount: Amount to transfer (in wei)

        Returns:
            Encoded function call data
        """
        return encode_function_data("transfer(address,uint256)", [to, amount])

    def encode_approve(self, spender: Address, amount: Wei) -> bytes:
        """Encode approve function call.

        Args:
            spender: Spender address
            amount: Amount to approve (in wei)

        Returns:
            Encoded function call data
        """
        return encode_function_data("approve(address,uint256)", [spender, amount])

    def encode_transfer_from(
        self, from_addr: Address, to: Address, amount: Wei
    ) -> bytes:
        """Encode transferFrom function call.

        Args:
            from_addr: Sender address
            to: Recipient address
            amount: Amount to transfer (in wei)

        Returns:
            Encoded function call data
        """
        return encode_function_data(
            "transferFrom(address,address,uint256)", [from_addr, to, amount]
        )

    async def get_info(self) -> TokenInfo:
        """Get comprehensive token information.

        Returns:
            TokenInfo object with name, symbol, decimals, etc.
        """
        name = await self.name()
        symbol = await self.symbol()
        decimals = await self.decimals()
        total_supply = await self.total_supply()

        return TokenInfo(
            address=self.address,
            name=name,
            symbol=symbol,
            decimals=decimals,
            total_supply=total_supply,
        )


async def get_token_info(
    token_address: Address, provider: AsyncProvider
) -> TokenInfo:
    """Get token information.

    Args:
        token_address: Address of the token
        provider: Async provider instance

    Returns:
        TokenInfo object
    """
    token = ERC20(token_address, provider)
    return await token.get_info()


async def get_balance(
    token_address: Address, account: Address, provider: AsyncProvider
) -> TokenAmount:
    """Get token balance of an account.

    Args:
        token_address: Address of the token
        account: Address to check balance of
        provider: Async provider instance

    Returns:
        Token balance
    """
    token = ERC20(token_address, provider)
    return await token.balance_of(account)
