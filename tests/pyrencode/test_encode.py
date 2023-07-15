import pytest

from pyrencode import encode


def test_encode_int_under_max_size() -> None:
    encode.encode_int(2**128, [])


def test_encode_int_over_max_size() -> None:
    pytest.raises(OverflowError, encode.encode_int, 2**256, [])


def test_dumps_wrong_float_bits() -> None:
    pytest.raises(ValueError, encode.dumps, None, float_bits=128)
