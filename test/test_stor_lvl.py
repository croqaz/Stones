
import os
import sys
import shutil
import pytest
sys.path.insert(1, os.getcwd())
from stones import LevelStore
from common import *


@pytest.fixture(scope='function')
def stor():
    DB = 'a'
    shutil.rmtree(DB + '.lvl', True)
    d = LevelStore(DB)
    yield d
    d.close()
    shutil.rmtree(DB + '.lvl', True)


def test_empty_db(stor):
    check_empty(stor)


def test_get_put(stor):
    check_get_put(stor)


def test_get_set(stor):
    check_get_set(stor)


def test_iter(stor):
    check_iter(stor)


def test_delete(stor):
    check_delete(stor)