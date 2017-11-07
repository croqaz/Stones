
import os
import sys
import pytest
sys.path.insert(1, os.getcwd())
from stones import DbmStore
from common import *

DB = 'a'

@pytest.fixture(scope='function')
def stor():
    d = DbmStore(DB)
    d.clear()
    repr(d)
    yield d
    d.close()
    d.destroy(True)


def test_empty_db(stor):
    check_empty(stor)


def test_get_put(stor):
    check_get_put(stor)


def test_get_set(stor):
    check_get_set(stor)


def test_populate():
    d = DbmStore(DB, iterable=[(b'a', b'b'), (b'c', b'd')])
    assert len(d) == 2
    assert list(d.items()) == [(b'c', b'd'), (b'a', b'b')]
    d.update({b'a': b'x'})
    assert list(d.items()) == [(b'c', b'd'), (b'a', b'x')]
    d.close()
    d.destroy(True)


def test_iter(stor):
    check_iter(stor)


def test_delete(stor):
    check_delete(stor)
