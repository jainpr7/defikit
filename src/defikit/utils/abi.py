"""ABI loading and caching utilities."""

import json
from pathlib import Path
from typing import Any

from ..core.exceptions import ABIError

# Cache for loaded ABIs
_ABI_CACHE: dict[str, list[dict[str, Any]]] = {}


def get_abi_path(name: str) -> Path:
    """Get the path to an ABI file."""
    abi_dir = Path(__file__).parent.parent / "abis"
    abi_file = abi_dir / f"{name}.json"

    if not abi_file.exists():
        raise ABIError(f"ABI file not found: {name}.json")

    return abi_file


def load_abi(name: str, cache: bool = True) -> list[dict[str, Any]]:
    """Load an ABI from a JSON file.

    Args:
        name: Name of the ABI file (without .json extension)
        cache: Whether to cache the ABI

    Returns:
        The ABI as a list of dictionaries

    Raises:
        ABIError: If the ABI file is not found or invalid
    """
    if cache and name in _ABI_CACHE:
        return _ABI_CACHE[name]

    try:
        abi_path = get_abi_path(name)
        with open(abi_path) as f:
            abi = json.load(f)

        if not isinstance(abi, list):
            raise ABIError(f"Invalid ABI format in {name}.json: expected list")

        if cache:
            _ABI_CACHE[name] = abi

        return abi
    except json.JSONDecodeError as e:
        raise ABIError(f"Failed to parse ABI {name}.json: {str(e)}") from e
    except Exception as e:
        raise ABIError(f"Failed to load ABI {name}.json: {str(e)}") from e


def get_function_abi(
    abi: list[dict[str, Any]], function_name: str
) -> dict[str, Any] | None:
    """Get a specific function from an ABI.

    Args:
        abi: The ABI to search
        function_name: Name of the function

    Returns:
        The function ABI or None if not found
    """
    for item in abi:
        if item.get("type") == "function" and item.get("name") == function_name:
            return item
    return None


def get_event_abi(
    abi: list[dict[str, Any]], event_name: str
) -> dict[str, Any] | None:
    """Get a specific event from an ABI.

    Args:
        abi: The ABI to search
        event_name: Name of the event

    Returns:
        The event ABI or None if not found
    """
    for item in abi:
        if item.get("type") == "event" and item.get("name") == event_name:
            return item
    return None


def clear_abi_cache() -> None:
    """Clear the ABI cache."""
    _ABI_CACHE.clear()
