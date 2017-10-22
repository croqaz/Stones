
import os
import sys
import shutil
import pytest
sys.path.insert(1, os.getcwd())
from stones.encoders import *
from stones.base import *
from stones import *


def test_base_store():
    # TypeError: Can't instantiate abstract class BaseStore
    with pytest.raises(TypeError):
        b = BaseStore()
    with pytest.raises(TypeError):
        b = BaseStore('pickle')
    with pytest.raises(EncodeException):
        s = stone('a', value_type=set, encoder=None, encode_decode=None)


def test_default_stone():
    s = stone('a')
    assert s._encode == noop
    assert s._decode == noop
    assert isinstance(s, LevelStore)
    s.clear()
    shutil.rmtree('a.lvl', True)


def test_base_store_encoder_pair():
    s = stone('a', value_type=set, encoder=None, encode_decode=(encode_json, decode_json))
    assert s._encode == encode_json
    assert s._decode == decode_json
    s.clear()
    shutil.rmtree('a.lvl', True)


def test_level_store():
    s = stone('a', 'level', encoder='cbor', value_type=list)
    assert s._encode == encode_cbor
    assert isinstance(s, BaseStore)
    assert isinstance(s, LevelStore)
    s.clear()
    shutil.rmtree('a.lvl', True)


def test_lmdb_store():
    s = stone('a', 'lmdb', encoder='msgpack', value_type=list)
    assert s._encode == encode_msgpack
    assert isinstance(s, BaseStore)
    assert isinstance(s, LmdbStore)
    s.clear()
    shutil.rmtree('a.lmdb', True)
