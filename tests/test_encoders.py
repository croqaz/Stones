
import os
import sys
import pytest
sys.path.insert(1, os.getcwd())
from stones.encoders import encoders


@pytest.fixture(scope='function', params=[
    b'qwe ASD 123',
    [b'a', b'qwerty'],
    {b'a', b'qwerty'},
    # (b'yes', b'no')
])
def value(request):
    return request.param


def test_encode_pickle(value):
    txt0 = encoders['pickle']['encode'](value)
    txt1 = encoders['pickle']['decode'](txt0)
    assert txt1 == value


def test_encode_json(value):
    txt0 = encoders['json']['encode'](value)
    txt1 = encoders['json']['decode'](txt0)
    assert txt1 == value


def test_encode_cbor(value):
    txt0 = encoders['cbor']['encode'](value)
    txt1 = encoders['cbor']['decode'](txt0)
    assert txt1 == value


def test_encode_msgpack(value):
    txt0 = encoders['msgpack']['encode'](value)
    txt1 = encoders['msgpack']['decode'](txt0)
    assert txt1 == value
