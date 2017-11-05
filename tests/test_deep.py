
import os
import sys
import shutil
import pytest
sys.path.insert(1, os.getcwd())
from stones import *


@pytest.fixture(scope='function', params=['level', 'lmdb', 'memory'])
def stor(request):
    return request.param


def cleanup(stor):
    stor.clear()
    stor.close()
    shutil.rmtree('a.lvl', True)
    shutil.rmtree('a.lmdb', True)


def test_deep_list(stor):
    s = stone('a', stor, value_type=list)

    s[b'li'] = []
    assert isinstance(s[b'li'], list)
    assert len(s[b'li']) == 0

    s.list_append(b'li', b'a')
    s.list_append(b'li', b'x')
    s.list_append(b'li', b'a')
    assert len(s[b'li']) == 3

    s.list_remove(b'li', b'x')
    assert len(s[b'li']) == 2

    with pytest.raises(TypeError):
        s.set_add(b'li', b'a')

    with pytest.raises(TypeError):
        s.set_remove(b'li', b'a')

    cleanup(s)


def test_deep_set(stor):
    s = stone('a', stor, value_type=set)

    s[b'set'] = set()
    assert isinstance(s[b'set'], set)
    assert len(s[b'set']) == 0

    s.set_add(b'set', b'a')
    s.set_add(b'set', b'x')
    s.set_add(b'set', b'a')
    assert len(s[b'set']) == 2

    s.set_remove(b'set', b'x')
    assert len(s[b'set']) == 1

    with pytest.raises(TypeError):
        s.list_append(b'set', b'a')

    with pytest.raises(TypeError):
        s.list_remove(b'set', b'a')

    cleanup(s)
