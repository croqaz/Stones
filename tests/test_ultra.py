
import os
import sys
import shutil
import pytest
sys.path.insert(1, os.getcwd())
from stones import stone
from stones.base import BaseStore
from stones.ultra import UltraStore


def test_base_store():
    with pytest.raises(TypeError):
        b = BaseStore('pickle')


def test_ultra_level_store():
    s = stone('a', 'level', 'cbor')
    assert isinstance(s, BaseStore)
    assert isinstance(s, UltraStore)
    s.clear()
    s.close()
    shutil.rmtree('a.lvl', True)


def test_ultra_lmdb_store():
    s = stone('a', 'lmdb', 'cbor')
    assert isinstance(s, BaseStore)
    assert isinstance(s, UltraStore)
    s.clear()
    s.close()
    shutil.rmtree('a.lmdb', True)
