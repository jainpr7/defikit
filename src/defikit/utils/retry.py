"""Async retry logic with exponential backoff."""

import asyncio
from typing import Any, Callable, Optional, TypeVar

T = TypeVar("T")


async def async_retry(
    func: Callable[..., Any],
    *args: Any,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    exponential_base: float = 2.0,
    max_delay: Optional[float] = None,
    exceptions: tuple[type[Exception], ...] = (Exception,),
    **kwargs: Any,
) -> T:
    """Retry an async function with exponential backoff.

    Args:
        func: Async function to retry
        *args: Positional arguments for the function
        max_retries: Maximum number of retries
        initial_delay: Initial delay between retries in seconds
        exponential_base: Base for exponential backoff
        max_delay: Maximum delay between retries
        exceptions: Tuple of exceptions to catch and retry
        **kwargs: Keyword arguments for the function

    Returns:
        The result of the function

    Raises:
        The last exception if all retries fail
    """
    last_exception: Optional[Exception] = None

    for attempt in range(max_retries + 1):
        try:
            return await func(*args, **kwargs)
        except exceptions as e:
            last_exception = e
            if attempt == max_retries:
                raise

            delay = initial_delay * (exponential_base**attempt)
            if max_delay is not None:
                delay = min(delay, max_delay)

            await asyncio.sleep(delay)

    # This should never be reached, but helps with type checking
    if last_exception:
        raise last_exception
    raise RuntimeError("Unexpected state in async_retry")


class RetryConfig:
    """Configuration for retry behavior."""

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        exponential_base: float = 2.0,
        max_delay: Optional[float] = None,
        exceptions: tuple[type[Exception], ...] = (Exception,),
    ):
        """Initialize retry configuration.

        Args:
            max_retries: Maximum number of retries
            initial_delay: Initial delay between retries in seconds
            exponential_base: Base for exponential backoff
            max_delay: Maximum delay between retries
            exceptions: Tuple of exceptions to catch and retry
        """
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.exponential_base = exponential_base
        self.max_delay = max_delay
        self.exceptions = exceptions

    async def retry(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> T:
        """Retry a function with this configuration."""
        return await async_retry(
            func,
            *args,
            max_retries=self.max_retries,
            initial_delay=self.initial_delay,
            exponential_base=self.exponential_base,
            max_delay=self.max_delay,
            exceptions=self.exceptions,
            **kwargs,
        )
