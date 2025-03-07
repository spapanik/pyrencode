import pytest

from pyrencode import encode


def test_encode_int_under_max_size() -> None:
    encode.Encoder().encode(2**128)


def test_encode_int_over_max_size() -> None:
    with pytest.raises(OverflowError):
        encode.Encoder().encode(2**256)


def test_encode_custom_class() -> None:
    class CustomClass:
        pass

    obj = CustomClass()
    with pytest.raises(TypeError):
        encode.Encoder().encode(obj)


def test_dumps_wrong_float_bits() -> None:
    with pytest.raises(ValueError, match=r"Float bits \d+ is not 32 or 64"):
        encode.dumps(None, float_bits=128)
