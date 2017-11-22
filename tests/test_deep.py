
import os
import sys
import shutil
import pytest
sys.path.insert(1, os.getcwd())
from stones import *


@pytest.fixture(scope='function', params=[list, set])
def deep(request):
    return request.param


def test_deep_operations(deep):
    s = stone(name='a', value_type=deep)

    s[b'deep'] = deep()
    assert isinstance(s[b'deep'], deep)
    assert len(s[b'deep']) == 0

    s.deep_add(b'deep', b'a')
    s.deep_add(b'deep', b'x')
    assert len(s[b'deep']) == 2
    s.deep_add(b'deep', b'a')

    if deep == set:
        assert len(s[b'deep']) == 2
        s.deep_remove(b'deep', b'x')
        assert len(s[b'deep']) == 1

    elif deep == list:
        assert len(s[b'deep']) == 3
        s.deep_remove(b'deep', b'x')
        assert len(s[b'deep']) == 2

    s.clear()
    s.close()
    s.destroy(yes_im_sure=True)


def test_crash_deep():
    s = stone(name='a', value_type=frozenset)

    s[b'deep'] = frozenset([1])
    assert isinstance(s[b'deep'], frozenset)
    assert len(s[b'deep']) == 1

    with pytest.raises(TypeError):
        s.deep_add(b'deep', b'a')

    with pytest.raises(TypeError):
        s.deep_remove(b'deep', b'a')
