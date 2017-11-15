
import os
import sys
import shutil
import pytest
sys.path.insert(1, os.getcwd())
from stones import *


@pytest.fixture(scope='function', params=['level', 'lmdb', 'dbm', 'memory'])
def stor(request):
    return request.param


@pytest.fixture(scope='function', params=[list, set])
def deep(request):
    return request.param


def cleanup(stor):
    stor.clear()
    stor.close()
    stor.destroy(yes_im_sure=True)


def test_deep_operations(stor, deep):

    s = stone('a', stor, value_type=deep)

    s[b'deep'] = deep()
    assert isinstance(s[b'deep'], deep)
    assert len(s[b'deep']) == 0

    s.deep_add(b'deep', b'a')
    s.deep_add(b'deep', b'x')
    assert len(s[b'deep']) == 2
    s.deep_add(b'deep', b'a')

    if isinstance(deep, set):
        assert len(s[b'deep']) == 2

    if isinstance(deep, list):
        assert len(s[b'deep']) == 3
        s.deep_remove(b'deep', b'x')
        assert len(s[b'deep']) == 2

    cleanup(s)
