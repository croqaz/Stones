
#- rev: v1 -
#- hash: OOTXQY -

import itertools
import contextlib
from .base import BaseStore


class MemoryStore(BaseStore):
    """
    Pure memory store.
    """

    __slots__ = ('db', '_name')

    def __init__(self, *args, encoder='noop', encode_decode=tuple(),
            value_type=bytes, iterable=tuple(), **kwargs):
        super().__init__(encoder=encoder, encode_decode=encode_decode, value_type=value_type)
        self.db = {}
        if iterable or kwargs:
            self._populate(iterable, **kwargs)

    def close(self):
        pass


    def _populate(self, iterable=tuple(), **kwargs):
        with contextlib.suppress(AttributeError):
            iterable = iterable.items()
        for key, value in itertools.chain(iterable, kwargs.items()):
            self.db[key] = self._encode(value)


    def get(self, key, default=None):
        encoded_value = self.db.get(key)
        return self._decode(encoded_value) if encoded_value else default

    def put(self, key, value, overwrite=False):
        if not overwrite and self.db.get(key):
            return
        self.db[key] = self._encode(value)

    def delete(self, key):
        del self.db[key]


    def __getitem__(self, key):
        encoded_value = self.db.get(key)
        return self._decode(encoded_value)

    def __setitem__(self, key, value):
        self.db[key] = self._encode(value)

    __delitem__ = delete

    def __contains__(self, key):
        return key in self.db

    def __len__(self):
        return len(self.db)

    def __iter__(self):
        return iter(self.db)

    def __repr__(self):
        return repr(self.db)


    def keys(self):
        return list(self.db.keys())

    def values(self):
        return list(self.db.values())

    def items(self):
        return dict(self.db)

    def clear(self):
        self.db.clear()
