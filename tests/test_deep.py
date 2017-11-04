
import os
import sys
import shutil
import pytest
sys.path.insert(1, os.getcwd())
from stones import *


def test_deep_list():
    s = stone('a', value_type=list)

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

    s.clear()
    s.close()
    shutil.rmtree('a.lvl', True)


def test_deep_set():
    s = stone('a', value_type=set)

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

    s.clear()
    s.close()
    shutil.rmtree('a.lvl', True)
