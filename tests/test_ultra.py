
import os
import sys
import shutil
import pytest
sys.path.insert(1, os.getcwd())
from stones.base import BaseStore
from stones import *


def test_base_store():
    with pytest.raises(TypeError):
        b = BaseStore('pickle')


def test_default_ultra_store():
    s = stone('a')
    assert s._encode == encoders['pickle']['encode']
    assert s._decode == encoders['pickle']['decode']
    assert isinstance(s, LevelStore)
    s.clear()
    s.close()
    shutil.rmtree('a.lvl', True)


def test_ultra_level_store():
    s = stone('a', 'level', 'cbor')
    assert isinstance(s, BaseStore)
    assert isinstance(s, UltraStore)
    assert isinstance(s, LevelStore)
    s.clear()
    s.close()
    shutil.rmtree('a.lvl', True)


def test_ultra_lmdb_store():
    s = stone('a', 'lmdb', 'cbor')
    assert isinstance(s, BaseStore)
    assert isinstance(s, UltraStore)
    assert isinstance(s, LmdbStore)
    s.clear()
    s.close()
    shutil.rmtree('a.lmdb', True)
