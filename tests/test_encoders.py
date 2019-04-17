import os
import sys
import pytest
sys.path.insert(1, os.getcwd())
from stones.serialize import serializers


@pytest.fixture(
    scope='function', params=[
        'noop',
        'json',
        'pickle',
        'cbor',
        'msgpack',
    ])
def codec(request):
    return request.param


@pytest.fixture(
    scope='function',
    params=[
        True,
        3.1415,
        b'qwe ASD 123',
        [b'x', b'qwerty'],
        {b'y', b'qwerty'},
        {True, False, None},
        (b'yes', b'no'),
        (True, False, None),
        frozenset([b'q', b'e']),
        {
            b'yes': b'y',
            b'no': b'n',
            b'maybe': 1
        },
    ])
def value(request):
    return request.param


def test_serialize(codec, value):
    txt0 = serializers[codec]['encode'](value)
    txt1 = serializers[codec]['decode'](txt0)
    assert txt1 == value
