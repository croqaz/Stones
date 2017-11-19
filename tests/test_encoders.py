
import os
import sys
import pytest
sys.path.insert(1, os.getcwd())
from stones.encoders import encoders


@pytest.fixture(scope='function', params=['noop', 'json', 'pickle', 'cbor', 'msgpack'])
def codec(request):
    return request.param


@pytest.fixture(scope='function', params=[
    b'qwe ASD 123',
    [b'a', b'qwerty'],
    {b'a', b'qwerty'},
    (b'yes', b'no')
])
def value(request):
    return request.param


def test_encode(codec, value):
    if codec == 'cbor' and isinstance(value, tuple):
        return
    txt0 = encoders[codec]['encode'](value)
    txt1 = encoders[codec]['decode'](txt0)
    assert txt1 == value
