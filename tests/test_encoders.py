
import os
import sys
import pytest
sys.path.insert(1, os.getcwd())
from stones.serialize import serializers


@pytest.fixture(scope='function', params=['noop', 'json', 'pickle', 'cbor', 'msgpack'])
def codec(request):
    return request.param


@pytest.fixture(scope='function', params=[
    b'qwe ASD 123',
    [b'x', b'qwerty'],
    {b'y', b'qwerty'},
    (b'yes', b'no'),
    {b'yes': b'y', b'no': b'n'},
    # {b's': {b'a', b'b'}, b'f': frozendict([b'a', b'b'])} # Doesn't work yet
])
def value(request):
    return request.param


def test_serialize(codec, value):
    txt0 = serializers[codec]['encode'](value)
    txt1 = serializers[codec]['decode'](txt0)
    assert txt1 == value
