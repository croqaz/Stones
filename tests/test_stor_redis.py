
import os
import sys
import pytest
from pyredis import Client

sys.path.insert(1, os.getcwd())
from stones import RedisStore
from common import *

STORE_KEY = 'a'
redis = Client(host='127.0.0.1', port=6379, database=0)
redis.ping()


@pytest.fixture(scope='function')
def stor():
    d = RedisStore(redis, STORE_KEY)
    d.clear()
    yield d
    d.clear()


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