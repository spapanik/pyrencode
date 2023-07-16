from __future__ import annotations

import struct
from string import digits
from typing import Any

from pyrencode import constants

string_bytes = {digit.encode() for digit in digits}


class Decoder:
    def __init__(self, *, decode_utf8: bool = constants.DECODE_UTF8):
        self.decode_utf8 = decode_utf8

    def decode(self, bytes_obj: bytes) -> Any:
        try:
            obj, end_position = self._decode(bytes_obj)
        except (IndexError, KeyError, OverflowError) as exc:
            raise ValueError from exc
        if end_position != len(bytes_obj):
            raise ValueError(f"extra data: {bytes_obj[end_position:]!r}")
        return obj

    def _decode(self, bytes_obj: bytes, cursor: int = 0) -> tuple[Any, int]:
        type_byte = bytes_obj[cursor : cursor + 1]
        if type_byte == constants.CHR_NONE:
            return None, cursor + 1
        if type_byte == constants.CHR_TRUE:
            return True, cursor + 1
        if type_byte == constants.CHR_FALSE:
            return False, cursor + 1
        if type_byte == constants.CHR_INT:
            return self.decode_int(bytes_obj, cursor)
        if type_byte == constants.CHR_INT1:
            return self.decode_int1(bytes_obj, cursor)
        if type_byte == constants.CHR_INT2:
            return self.decode_int2(bytes_obj, cursor)
        if type_byte == constants.CHR_INT4:
            return self.decode_int3(bytes_obj, cursor)
        if type_byte == constants.CHR_INT8:
            return self.decode_int4(bytes_obj, cursor)
        if type_byte == constants.CHR_FLOAT32:
            return self.decode_float32(bytes_obj, cursor)
        if type_byte == constants.CHR_FLOAT64:
            return self.decode_float64(bytes_obj, cursor)
        if type_byte in string_bytes:
            return self.decode_string(bytes_obj, cursor)
        if type_byte == constants.CHR_LIST:
            return self.decode_list(bytes_obj, cursor)
        if type_byte == constants.CHR_DICT:
            return self.decode_dict(bytes_obj, cursor)

        order = ord(type_byte)
        if constants.INT_POS_FIXED_START <= order <= constants.INT_POS_FIXED_END:
            return self.decode_fixed_length_positive_integer(bytes_obj, cursor)
        if constants.INT_NEG_FIXED_START <= order <= constants.INT_NEG_FIXED_END:
            return self.decode_fixed_length_negative_integer(bytes_obj, cursor)
        if constants.STR_FIXED_START <= order <= constants.STR_FIXED_END:
            return self.decode_fixed_length_string(bytes_obj, cursor)
        if constants.LIST_FIXED_START <= order <= constants.LIST_FIXED_END:
            return self.decode_fixed_length_list(bytes_obj, cursor)
        if constants.DICT_FIXED_START <= order <= constants.DICT_FIXED_END:
            return self.decode_fixed_length_dict(bytes_obj, cursor)

        raise ValueError(f"unknown type byte: {type_byte!r}")

    def _decode_string(
        self, bytes_obj: bytes, cursor: int, length: int
    ) -> tuple[str | bytes, int]:
        new_cursor = cursor + length
        string = bytes_obj[cursor:new_cursor]
        if self.decode_utf8:
            return string.decode("utf8"), new_cursor

        return string, new_cursor

    @staticmethod
    def decode_int(bytes_obj: bytes, cursor: int) -> tuple[int, int]:
        cursor += 1
        new_cursor = bytes_obj.index(constants.CHR_TERM, cursor)
        if new_cursor - cursor >= constants.MAX_INT_LENGTH:
            raise OverflowError("int exceeds maximum length")
        n = int(bytes_obj[cursor:new_cursor])
        if bytes_obj[cursor : cursor + 1] == b"-":
            if bytes_obj[cursor + 1 : cursor + 2] == b"0":
                raise ValueError("negative zero in int")
        elif bytes_obj[cursor : cursor + 1] == b"0" and new_cursor != cursor + 1:
            raise ValueError("leading zero in int")

        return n, new_cursor + 1

    @staticmethod
    def decode_int1(bytes_obj: bytes, cursor: int) -> tuple[int, int]:
        cursor += 1
        new_cursor = cursor + 1
        return struct.unpack("!b", bytes_obj[cursor:new_cursor])[0], new_cursor

    @staticmethod
    def decode_int2(bytes_obj: bytes, cursor: int) -> tuple[int, int]:
        cursor += 1
        new_cursor = cursor + 2
        return struct.unpack("!h", bytes_obj[cursor:new_cursor])[0], new_cursor

    @staticmethod
    def decode_int3(bytes_obj: bytes, cursor: int) -> tuple[int, int]:
        cursor += 1
        new_cursor = cursor + 4
        return struct.unpack("!l", bytes_obj[cursor:new_cursor])[0], new_cursor

    @staticmethod
    def decode_int4(bytes_obj: bytes, cursor: int) -> tuple[int, int]:
        cursor += 1
        new_cursor = cursor + 8
        return struct.unpack("!q", bytes_obj[cursor:new_cursor])[0], new_cursor

    @staticmethod
    def decode_float32(bytes_obj: bytes, cursor: int) -> tuple[float, int]:
        cursor += 1
        new_cursor = cursor + 4
        return struct.unpack("!f", bytes_obj[cursor:new_cursor])[0], new_cursor

    @staticmethod
    def decode_float64(bytes_obj: bytes, cursor: int) -> tuple[float, int]:
        cursor += 1
        new_cursor = cursor + 8
        return struct.unpack("!d", bytes_obj[cursor:new_cursor])[0], new_cursor

    def decode_string(self, bytes_obj: bytes, cursor: int) -> tuple[str | bytes, int]:
        colon = bytes_obj.index(b":", cursor)
        if bytes_obj[cursor : cursor + 1] == b"0" and colon != cursor + 1:
            raise ValueError("leading zero in string length")

        length = int(bytes_obj[cursor:colon])
        return self._decode_string(bytes_obj, colon + 1, length)

    def decode_list(self, bytes_obj: bytes, cursor: int) -> tuple[tuple[Any, ...], int]:
        output = []
        cursor += 1
        while bytes_obj[cursor : cursor + 1] != constants.CHR_TERM:
            value, cursor = self._decode(bytes_obj, cursor)
            output.append(value)
        return tuple(output), cursor + 1

    def decode_dict(self, bytes_obj: bytes, cursor: int) -> tuple[dict[Any, Any], int]:
        output = {}
        cursor += 1
        while bytes_obj[cursor : cursor + 1] != constants.CHR_TERM:
            key, cursor = self._decode(bytes_obj, cursor)
            output[key], cursor = self._decode(bytes_obj, cursor)
        return output, cursor + 1

    @staticmethod
    def decode_fixed_length_positive_integer(
        bytes_obj: bytes, cursor: int
    ) -> tuple[int, int]:
        return bytes_obj[cursor], cursor + 1

    @staticmethod
    def decode_fixed_length_negative_integer(
        bytes_obj: bytes, cursor: int
    ) -> tuple[int, int]:
        return constants.INT_NEG_FIXED_START - bytes_obj[cursor] - 1, cursor + 1

    def decode_fixed_length_string(
        self, bytes_obj: bytes, cursor: int
    ) -> tuple[str | bytes, int]:
        length = bytes_obj[cursor] - constants.STR_FIXED_START
        return self._decode_string(bytes_obj, cursor + 1, length)

    def decode_fixed_length_list(
        self, bytes_obj: bytes, cursor: int
    ) -> tuple[tuple[Any, ...], int]:
        length = bytes_obj[cursor] - constants.LIST_FIXED_START
        output = []
        cursor += 1
        for _ in range(length):
            value, cursor = self._decode(bytes_obj, cursor)
            output.append(value)
        return tuple(output), cursor

    def decode_fixed_length_dict(
        self, bytes_obj: bytes, cursor: int
    ) -> tuple[dict[Any, Any], int]:
        length = bytes_obj[cursor] - constants.DICT_FIXED_START
        output = {}
        cursor += 1
        for _ in range(length):
            key, cursor = self._decode(bytes_obj, cursor)
            output[key], cursor = self._decode(bytes_obj, cursor)
        return output, cursor


def loads(bytes_obj: bytes, *, decode_utf8: bool = False) -> Any:
    return Decoder(decode_utf8=decode_utf8).decode(bytes_obj)
