"""Data encoding and decoding helpers."""

from typing import Any

from eth_abi import decode, encode
from eth_utils import function_signature_to_4byte_selector, keccak

from ..core.exceptions import EncodingError, DecodingError


def encode_function_data(
    function_signature: str, args: list[Any]
) -> bytes:
    """Encode function call data.

    Args:
        function_signature: Function signature (e.g., "transfer(address,uint256)")
        args: List of arguments to encode

    Returns:
        Encoded function call data

    Raises:
        EncodingError: If encoding fails
    """
    try:
        selector = function_signature_to_4byte_selector(function_signature)

        # Extract types from signature
        types_str = function_signature.split("(")[1].rstrip(")")
        if types_str:
            types = [t.strip() for t in types_str.split(",")]
            encoded_args = encode(types, args)
        else:
            encoded_args = b""

        return selector + encoded_args
    except Exception as e:
        raise EncodingError(f"Failed to encode function data: {str(e)}") from e


def decode_function_result(
    types: list[str], data: bytes
) -> tuple[Any, ...]:
    """Decode function return data.

    Args:
        types: List of return types
        data: Encoded return data

    Returns:
        Decoded values as a tuple

    Raises:
        DecodingError: If decoding fails
    """
    try:
        return decode(types, data)
    except Exception as e:
        raise DecodingError(f"Failed to decode function result: {str(e)}") from e


def encode_packed(types: list[str], values: list[Any]) -> bytes:
    """Encode values using packed encoding (similar to Solidity's abi.encodePacked).

    Args:
        types: List of types
        values: List of values to encode

    Returns:
        Packed encoded data

    Raises:
        EncodingError: If encoding fails
    """
    try:
        # This is a simplified version - full implementation would need more type handling
        result = b""
        for type_str, value in zip(types, values):
            if type_str == "address":
                # Convert address to bytes
                if isinstance(value, str):
                    value = value.lower().replace("0x", "")
                    result += bytes.fromhex(value)
                else:
                    result += value
            elif type_str.startswith("uint") or type_str.startswith("int"):
                # Convert integer to bytes
                size = int(type_str[4:] if type_str.startswith("uint") else type_str[3:]) // 8
                result += value.to_bytes(size, byteorder="big")
            elif type_str == "bytes":
                result += value
            elif type_str.startswith("bytes"):
                size = int(type_str[5:])
                result += value[:size].ljust(size, b"\x00")
            else:
                raise EncodingError(f"Unsupported type for packed encoding: {type_str}")
        return result
    except Exception as e:
        raise EncodingError(f"Failed to encode packed: {str(e)}") from e


def keccak256(data: bytes) -> bytes:
    """Calculate Keccak-256 hash.

    Args:
        data: Data to hash

    Returns:
        32-byte hash
    """
    return keccak(data)


def get_function_selector(function_signature: str) -> bytes:
    """Get the 4-byte function selector.

    Args:
        function_signature: Function signature (e.g., "transfer(address,uint256)")

    Returns:
        4-byte function selector
    """
    return function_signature_to_4byte_selector(function_signature)


def pad_bytes(data: bytes, length: int = 32) -> bytes:
    """Pad bytes to the specified length.

    Args:
        data: Data to pad
        length: Target length

    Returns:
        Padded data
    """
    if len(data) >= length:
        return data
    return data + b"\x00" * (length - len(data))
