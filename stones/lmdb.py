
import itertools
import contextlib
from .base import Base

try:
    import lmdb
except ModuleNotFoundError:
    print('LevelDB store requires PyPi.python.org/pypi/lmdb')
    exit(1)


class LmdbStore(Base):
    """
    LMDB ‘Lightning’ Database container, compatible with Python dicts.
    Keys and values MUST be byte strings.
    """

    __slots__ = ('db', 'table')

    def __init__(self, name, table=None, iterable=tuple(), **kwargs):
        super().__init__()
        self.db = lmdb.open(name + '.lmdb', max_dbs=9, map_size=8e12)
        self.table = self.db.open_db(table)
        if iterable or kwargs:
            self._populate(iterable, **kwargs)

    def close(self):
        self.db.close()


    def _populate(self, iterable=tuple(), **kwargs):
        with contextlib.suppress(AttributeError):
            iterable = iterable.items()
        with self.db.begin(write=True, db=self.table) as txn:
            for key, value in itertools.chain(iterable, kwargs.items()):
                txn.put(key, value, dupdata=False)


    def get(self, key, default=None):
        with self.db.begin(db=self.table) as txn:
            return txn.get(key, default)

    def put(self, key, value, overwrite=False):
        with self.db.begin(write=True, db=self.table) as txn:
            txn.put(key, value, dupdata=False, overwrite=overwrite)

    def delete(self, key):
        with self.db.begin(write=True, db=self.table) as txn:
            return txn.delete(key)


    def __getitem__(self, key):
        with self.db.begin(db=self.table) as txn:
            return txn.get(key)

    def __setitem__(self, key, value):
        with self.db.begin(write=True, db=self.table) as txn:
            txn.put(key, value, dupdata=False)

    __delitem__ = delete


    def __contains__(self, key):
        with self.db.begin(db=self.table) as txn:
            return bool(txn.get(key))

    def __len__(self):
        with self.db.begin(db=self.table) as txn:
            return txn.stat()['entries']

    def __iter__(self):
        with self.db.begin(db=self.table) as txn:
            yield from txn.cursor().iternext(keys=True, values=False)

    def __repr__(self):
        items = dict(self.items())
        return self.__class__.__name__ + repr(items)


    def items(self):
        items_dict = {}
        with self.db.begin(db=self.table) as txn:
            for key, value in txn.cursor().iternext(keys=True, values=True):
                items_dict[key] = value
        return items_dict


    def update(self, iterable=tuple(), **kwargs):
        self._populate(iterable, **kwargs)

    def clear(self):
        with self.db.begin(write=True) as txn:
            txn.drop(self.table, delete=False)
