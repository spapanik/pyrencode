import pytest

from pyrencode import encode


def test_encode_int_under_max_size() -> None:
    encode.Encoder().encode(2**128)


def test_encode_int_over_max_size() -> None:
    with pytest.raises(OverflowError):
        encode.Encoder().encode(2**256)


def test_dumps_wrong_float_bits() -> None:
    with pytest.raises(ValueError):
        encode.dumps(None, float_bits=128)
