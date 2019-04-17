import os
import sys
import pytest
sys.path.insert(1, os.getcwd())
from stones.util import *


def test_ensure_bytes():
    val = b'asd'
    assert ensure_bytes(val) == val
    val = 'asd'
    assert ensure_bytes(val) == val.encode('utf')

    with pytest.raises(TypeError):
        ensure_bytes([])
    with pytest.raises(TypeError):
        ensure_bytes({})
