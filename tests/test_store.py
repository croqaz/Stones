import os
import sys
import pytest
sys.path.insert(1, os.getcwd())
from stones import MemoryStore
from stones import LmdbStore
from common import *


@pytest.fixture(scope='function',
                params=[
                    lambda: MemoryStore(serialize='json'),
                    lambda: MemoryStore(serialize='json'),
                    lambda: MemoryStore(serialize='pickle'),
                    lambda: LmdbStore('test1', serialize='json'),
                    lambda: LmdbStore('test2', serialize='pickle'),
                ])
def stor(request):
    m = request.param()
    print(repr(m))
    yield m
    m.destroy(yes_im_sure=True)


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
