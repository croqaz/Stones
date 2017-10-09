
import itertools
import contextlib
from .base import Base

try:
    import plyvel
except ModuleNotFoundError:
    print('LevelDB store requires PyPi.python.org/pypi/plyvel')
    exit(1)


class LevelStore(Base):
    """
    LevelDB container compatible with Python dicts.
    Keys and values MUST be byte strings.
    """

    __slots__ = 'db'

    def __init__(self, name, iterable=tuple(), **kwargs):
        super().__init__()
        self.db = plyvel.DB(name + '.lvl', create_if_missing=True)
        if iterable or kwargs:
            self._populate(iterable, **kwargs)

    def close(self):
        self.db.close()


    def _populate(self, iterable=tuple(), **kwargs):
        with contextlib.suppress(AttributeError):
            iterable = iterable.items()
        with self.db.write_batch() as batch:
            for key, value in itertools.chain(iterable, kwargs.items()):
                batch.put(key, value)


    def get(self, key, default=None):
        return self.db.get(key, default)

    def put(self, key, value, overwrite=False):
        if not overwrite and self.db.get(key):
            return
        self.db.put(key, value)

    def delete(self, key):
        return self.db.delete(key)


    def __getitem__(self, key):
        return self.db.get(key)

    def __setitem__(self, key, value):
        return self.db.put(key, value)

    __delitem__ = delete


    def __contains__(self, key):
        return bool(self.db.get(key))

    def __len__(self):
        return len(set(self.db))

    def __iter__(self):
        return self.db.iterator(include_key=True, include_value=False)

    def __repr__(self):
        items = dict(self.items())
        return self.__class__.__name__ + repr(items)


    def items(self):
        items_dict = {}
        for key, value in self.db.iterator(include_key=True, include_value=True):
            items_dict[key] = value
        return items_dict


    def update(self, iterable=tuple(), **kwargs):
        self._populate(iterable, **kwargs)
