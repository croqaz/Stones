
import os
import sys
import shutil
import pytest
sys.path.insert(1, os.getcwd())
from stones import LmdbStore
from common import *


@pytest.fixture(scope='function')
def stor():
    DB = 'a'
    d = LmdbStore(DB)
    d.clear()
    yield d
    d.close()
    shutil.rmtree(DB + '.lmdb', True)


def test_empty_db(stor):
    check_empty(stor)


def test_get_put(stor):
    check_get_put(stor)


def test_get_set(stor):
    check_get_set(stor)


def test_populate():
    DB = 'a'
    d = LmdbStore(DB, iterable=[(b'a', b'b'), (b'c', b'd')])
    assert len(d) == 2
    assert d.items() == {b'a': b'b', b'c': b'd'}
    d.close()
    shutil.rmtree(DB + '.lmdb', True)


def test_iter(stor):
    check_iter(stor)


def test_delete(stor):
    check_delete(stor)
