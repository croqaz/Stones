import itertools
import contextlib
from .base import BaseStore


class MemoryStore(BaseStore):
    """
    Pure memory store.
    Inspired from builtin collections.UserDict.
    """

    __slots__ = ('db',)

    def __init__(self,
                 *arg,
                 serialize='noop',
                 dump_load=tuple(),
                 value_type=bytes,
                 iterable=tuple(),
                 kwargs={}):
        super().__init__(serialize=serialize, dump_load=dump_load, value_type=value_type)
        self.db = {}
        if iterable or kwargs:
            self._populate(iterable, **kwargs)

    def _populate(self, iterable=tuple(), **kwargs):
        with contextlib.suppress(AttributeError):
            iterable = iterable.items()
        for key, value in itertools.chain(iterable, kwargs.items()):
            self.db[key] = self._encode(value)

    def get(self, key, default=None):
        encoded_value = self.db.get(key)
        return self._decode(encoded_value) if encoded_value else default

    def put(self, key, value, overwrite=True):
        if not overwrite and self.db.get(key):
            return
        self.db[key] = self._encode(value)

    def delete(self, key):
        del self.db[key]

    __getitem__ = get

    __setitem__ = put

    __delitem__ = delete

    def __contains__(self, key):
        return key in self.db

    def __len__(self):
        return len(self.db)

    def __iter__(self):
        return iter(self.db)

    def __repr__(self):
        return self.__class__.__name__ + repr(self.db)

    def keys(self):
        return list(self.db.keys())

    def values(self):
        return list(self.db.values())

    def items(self):
        return self.db.items()

    def update(self, iterable=tuple(), **kwargs):
        self._populate(iterable, **kwargs)

    def close(self):
        pass

    def clear(self):
        self.db.clear()

    def destroy(self, yes_im_sure=False):
        if yes_im_sure:
            self.db.clear()
