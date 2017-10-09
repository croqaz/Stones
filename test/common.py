
def check_empty(stor):
    assert len(stor) == 0
    # Empty store
    assert stor.get(b'a') is None
    assert stor.get(b'x') is None
    # Default values for any key
    assert stor.get(b'a', False) is False
    assert stor.get(b'x', False) is False


def check_get_put(stor):

    stor.setdefault(b'a', b'a')
    # Key doesn't exist, create it
    assert len(stor) == 1
    assert stor.get(b'a') == b'a'

    stor.put(b'a', b'aa')
    # Value not changed
    assert stor.get(b'a') == b'a'

    stor.put(b'a', b'aa', overwrite=True)
    # Overwrite old value
    assert len(stor) == 1
    assert stor.get(b'a') == b'aa'
    assert stor.get(b'a', False) == b'aa'

    stor.put(b'x', b'xxx')

    assert len(stor) == 2
    assert stor.get(b'x') == b'xxx'
    assert stor.get(b'x', False) == b'xxx'


def check_get_set(stor):

    stor[b'a'] = b'a'

    assert len(stor) == 1
    assert stor[b'a'] == b'a'

    stor[b'a'] = b'aaa'

    assert len(stor) == 1
    assert stor[b'a'] == b'aaa'

    stor[b'x'] = b'xx'

    assert len(stor) == 2
    assert stor[b'x'] == b'xx'


def check_iter(stor):

    stor.update({b'a': b'aaa', b'x': b'xxx'})
    assert len(stor) == 2

    stor.update([(b'n', b'123'), (b'm', b'987')])
    assert len(stor) == 4

    assert sorted(x for x in stor) == [b'a', b'm', b'n', b'x']


def check_delete(stor):

    stor.put(b'a', b'abc')
    assert len(stor) == 1

    stor.delete(b'a')
    assert len(stor) == 0

    stor[b'x'] = b'xyz'
    assert len(stor) == 1

    del stor[b'x']
    assert len(stor) == 0

    assert stor.get(b'a') is None
    assert stor.get(b'x') is None
