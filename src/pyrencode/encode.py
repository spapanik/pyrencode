from __future__ import annotations

import struct
from collections.abc import Iterator, Sequence
from typing import Any

from pyrencode import constants
from pyrencode.utils import to_bytes


class Encoder:
    def __init__(self, float_bits: int = constants.DEFAULT_FLOAT_BITS):
        if float_bits not in {32, 64}:
            raise ValueError(f"Float bits {float_bits} is not 32 or 64")
        self.float_bits = float_bits

    def encode(self, obj: Any) -> bytes:
        return b"".join(self.encode_func(obj))

    def encode_func(self, obj: Any) -> Iterator[bytes]:
        if obj is None:
            yield constants.CHR_NONE
        elif obj is True:
            yield constants.CHR_TRUE
        elif obj is False:
            yield constants.CHR_FALSE
        elif isinstance(obj, int):
            yield from self.encode_int(obj)
        elif isinstance(obj, float):
            if self.float_bits == 32:
                yield from self.encode_float32(obj)
            else:
                yield from self.encode_float64(obj)
        elif isinstance(obj, bytes):
            yield from self.encode_bytes(obj)
        elif isinstance(obj, (list, tuple)):
            yield from self.encode_list(obj)
        elif isinstance(obj, dict):
            yield from self.encode_dict(obj)
        elif isinstance(obj, str):
            yield from self.encode_string(obj)
        else:
            raise TypeError(f"Object {obj} cannot be rencoded.")

    @staticmethod
    def encode_int(obj: int) -> Iterator[bytes]:
        if 0 <= obj < constants.INT_POS_FIXED_COUNT:
            yield to_bytes(constants.INT_POS_FIXED_START + obj)
        elif -constants.INT_NEG_FIXED_COUNT <= obj < 0:
            yield to_bytes(constants.INT_NEG_FIXED_START - 1 - obj)
        elif -constants.INT1_SIZE <= obj < constants.INT1_SIZE:
            yield constants.CHR_INT1
            yield struct.pack("!b", obj)
        elif -constants.INT2_SIZE <= obj < constants.INT2_SIZE:
            yield constants.CHR_INT2
            yield struct.pack("!h", obj)
        elif -constants.INT4_SIZE <= obj < constants.INT4_SIZE:
            yield constants.CHR_INT4
            yield struct.pack("!l", obj)
        elif -constants.INT8_SIZE <= obj < constants.INT8_SIZE:
            yield constants.CHR_INT8
            yield struct.pack("!q", obj)
        else:
            yield constants.CHR_INT

            int_as_bytes = bytes(str(obj), "ascii")
            yield int_as_bytes
            if len(int_as_bytes) >= constants.MAX_INT_LENGTH:
                raise OverflowError(f"Integer {obj} is too big to be rencoded.")

            yield constants.CHR_TERM

    @staticmethod
    def encode_float32(obj: float) -> Iterator[bytes]:
        yield constants.CHR_FLOAT32
        yield struct.pack("!f", obj)

    @staticmethod
    def encode_float64(obj: float) -> Iterator[bytes]:
        yield constants.CHR_FLOAT64
        yield struct.pack("!d", obj)

    @staticmethod
    def encode_bytes(obj: bytes) -> Iterator[bytes]:
        if len(obj) < constants.STR_FIXED_COUNT:
            yield to_bytes(constants.STR_FIXED_START + len(obj))
        else:
            yield str(len(obj)).encode()
            yield b":"
        yield obj

    def encode_string(self, obj: str) -> Iterator[bytes]:
        yield from self.encode_bytes(obj.encode())

    def encode_list(self, obj: Sequence[Any]) -> Iterator[bytes]:
        if len(obj) < constants.LIST_FIXED_COUNT:
            yield to_bytes(constants.LIST_FIXED_START + len(obj))
            for item in obj:
                yield from self.encode_func(item)
        else:
            yield constants.CHR_LIST
            for item in obj:
                yield from self.encode_func(item)
            yield constants.CHR_TERM

    def encode_dict(self, obj: dict[Any, Any]) -> Iterator[bytes]:
        if len(obj) < constants.DICT_FIXED_COUNT:
            yield to_bytes(constants.DICT_FIXED_START + len(obj))
            for key, value in obj.items():
                yield from self.encode_func(key)
                yield from self.encode_func(value)
        else:
            yield constants.CHR_DICT
            for key, value in obj.items():
                yield from self.encode_func(key)
                yield from self.encode_func(value)
            yield constants.CHR_TERM


def dumps(obj: Any, float_bits: int = constants.DEFAULT_FLOAT_BITS) -> bytes:
    return Encoder(float_bits).encode(obj)
