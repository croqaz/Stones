
import os
import sys
import shutil
import pytest
sys.path.insert(1, os.getcwd())
from stones.encoders import *
from stones.base import *
from stones import *


def test_crash_base_store():
    # TypeError: Can't instantiate abstract class BaseStore
    with pytest.raises(TypeError):
        b = BaseStore()
    with pytest.raises(TypeError):
        b = BaseStore('pickle')
    # Invalid store name
    with pytest.raises(StoreException):
        s = stone('a', 'xxx')
    # Invalid encoder name
    with pytest.raises(EncodeException):
        s = stone('a', encoder='xxx')
    # Encoder required for sets and lists
    with pytest.raises(EncodeException):
        s = stone('a', value_type=set, encoder=None, encode_decode=None)
    with pytest.raises(EncodeException):
        s = stone('a', value_type=list, encoder=None, encode_decode=None)


def test_default_stone():
    s = stone('a')
    assert s._encode == encode_pickle
    assert s._decode == decode_pickle
    assert isinstance(s, MemoryStore)


def test_base_store_encoder_pair():
    s = stone('a', 'memory', value_type=set, encoder=None, encode_decode=(encode_json, decode_json))
    assert s._encode == encode_json
    assert s._decode == decode_json


@pytest.fixture(scope='function', params=['json', 'pickle', 'cbor', 'msgpack'])
def codec(request):
    return request.param


def test_encoders(codec):
    s = stone('a', 'memory', codec)
    assert s._encode == globals()['encode_' + codec]
    assert isinstance(s, MemoryStore)
    s = stone('a', persistence='memory', encoder=codec)
    assert s._encode == globals()['encode_' + codec]
    assert isinstance(s, MemoryStore)
