from __future__ import annotations

import struct
from typing import Any, Callable

from pyrencode import constants
from pyrencode.utils import int2byte


def encode_int(obj: int, data_list: list[bytes]) -> None:
    if 0 <= obj < constants.INT_POS_FIXED_COUNT:
        data_list.append(int2byte(constants.INT_POS_FIXED_START + obj))
    elif -constants.INT_NEG_FIXED_COUNT <= obj < 0:
        data_list.append(int2byte(constants.INT_NEG_FIXED_START - 1 - obj))
    elif -constants.INT1_SIZE <= obj < constants.INT1_SIZE:
        data_list.extend((constants.CHR_INT1, struct.pack("!b", obj)))
    elif -constants.INT2_SIZE <= obj < constants.INT2_SIZE:
        data_list.extend((constants.CHR_INT2, struct.pack("!h", obj)))
    elif -constants.INT4_SIZE <= obj < constants.INT4_SIZE:
        data_list.extend((constants.CHR_INT4, struct.pack("!l", obj)))
    elif -constants.INT8_SIZE <= obj < constants.INT8_SIZE:
        data_list.extend((constants.CHR_INT8, struct.pack("!q", obj)))
    else:
        s = bytes(str(obj), "ascii")
        if len(s) >= constants.MAX_INT_LENGTH:
            raise OverflowError("Integer is too long to be rencoded.")

        data_list.extend((constants.CHR_INT, s, constants.CHR_TERM))


def encode_float32(obj: float, data_list: list[bytes]) -> None:
    data_list.extend((constants.CHR_FLOAT32, struct.pack("!f", obj)))


def encode_float64(obj: float, data_list: list[bytes]) -> None:
    data_list.extend((constants.CHR_FLOAT64, struct.pack("!d", obj)))


def encode_bool(obj: bool, data_list: list[bytes]) -> None:
    if obj:
        data_list.append(constants.CHR_TRUE)
    else:
        data_list.append(constants.CHR_FALSE)


def encode_none(_obj: None, data_list: list[bytes]) -> None:
    data_list.append(constants.CHR_NONE)


def encode_bytes(obj: bytes, data_list: list[bytes]) -> None:
    if len(obj) < constants.STR_FIXED_COUNT:
        data_list.extend((int2byte(constants.STR_FIXED_START + len(obj)), obj))
    else:
        string = bytes(str(len(obj)), constants.ASCII)
        data_list.extend((string, b":", obj))


def encode_string(obj: str, data_list: list[bytes]) -> None:
    encode_bytes(obj.encode(constants.UTF8), data_list)


def encode_list(obj: list[Any], data_list: list[bytes]) -> None:
    if len(obj) < constants.LIST_FIXED_COUNT:
        data_list.append(int2byte(constants.LIST_FIXED_START + len(obj)))
        for item in obj:
            encode_func[type(item)](item, data_list)
    else:
        data_list.append(constants.CHR_LIST)
        for item in obj:
            encode_func[type(item)](item, data_list)
        data_list.append(constants.CHR_TERM)


def encode_dict(obj: dict[Any, Any], data_list: list[bytes]) -> None:
    if len(obj) < constants.DICT_FIXED_COUNT:
        data_list.append(int2byte(constants.DICT_FIXED_START + len(obj)))
        for key, value in obj.items():
            encode_func[type(key)](key, data_list)
            encode_func[type(value)](value, data_list)
    else:
        data_list.append(constants.CHR_DICT)
        for key, value in obj.items():
            encode_func[type(key)](key, data_list)
            encode_func[type(value)](value, data_list)
        data_list.append(constants.CHR_TERM)


encode_func: dict[type, Callable[[Any, list[bytes]], None]] = {
    int: encode_int,
    bytes: encode_bytes,
    list: encode_list,
    tuple: encode_list,
    dict: encode_dict,
    type(None): encode_none,
    str: encode_string,
    bool: encode_bool,
}


def dumps(obj: Any, float_bits: int = constants.DEFAULT_FLOAT_BITS) -> bytes:
    if float_bits == 32:
        encode_func[float] = encode_float32
    elif float_bits == 64:
        encode_func[float] = encode_float64
    else:
        raise ValueError(f"Float bits {float_bits} is not 32 or 64")

    data_list: list[bytes] = []
    encode_func[type(obj)](obj, data_list)

    return b"".join(data_list)
