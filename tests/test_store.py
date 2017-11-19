
import os
import sys
import shutil
import pytest
sys.path.insert(1, os.getcwd())
from stones import MemoryStore
from common import *


@pytest.fixture(scope='function')
def stor():
    d = MemoryStore()
    repr(d)
    yield d


def test_empty_db(stor):
    check_empty(stor)


def test_get_put(stor):
    check_get_put(stor)


def test_get_set(stor):
    check_get_set(stor)


def test_populate():
    d = MemoryStore(iterable=[(b'a', b'b'), (b'c', b'd')])
    assert len(d) == 2
    assert list(d.items()) == [(b'a', b'b'), (b'c', b'd')]
    d.update({b'a': b'x'})
    assert list(d.items()) == [(b'a', b'x'), (b'c', b'd')]
    d.update([(b'a', b'z')])
    assert list(d.items()) == [(b'a', b'z'), (b'c', b'd')]
    d.clear()
    d.close()
    d.destroy(yes_im_sure=True)


def test_iter(stor):
    check_iter(stor)


def test_delete(stor):
    check_delete(stor)
