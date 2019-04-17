import os
import sys
import pytest
sys.path.insert(1, os.getcwd())
from stones.serialize import *
from stones.base import *
from stones import *


def test_crash_base_store():
    # TypeError: Can't instantiate abstract class BaseStore
    with pytest.raises(TypeError):
        b = BaseStore()
    with pytest.raises(TypeError):
        b = BaseStore('pickle')
    # Invalid serializer name
    with pytest.raises(EncoderException):
        s = stone('a', serialize='xxx')
    # Encoder required for sets, lists, tuples
    with pytest.raises(EncoderException):
        s = stone('a', value_type=set, serialize=None, dump_load=None)
    with pytest.raises(EncoderException):
        s = stone('a', value_type=list, serialize=None, dump_load=None)
    with pytest.raises(EncoderException):
        s = stone('a', value_type=tuple, serialize=None, dump_load=None)


def test_default_stone():
    s = stone('a')
    assert s._encode == encode_pickle
    assert s._decode == decode_pickle
    assert isinstance(s, MemoryStore)


def test_base_store_encoder_pair():
    s = stone('a', value_type=set, serialize=None, dump_load=(encode_json, decode_json))
    assert s._encode == encode_json
    assert s._decode == decode_json


@pytest.fixture(scope='function', params=['json', 'pickle', 'cbor', 'msgpack'])
def codec(request):
    return request.param


def test_serializer(codec):
    s = stone('a', serialize=codec)
    assert s._encode == globals()['encode_' + codec]
    assert isinstance(s, MemoryStore)
    s[b'a'] = b'abc'
    assert s[b'a'] == b'abc'
