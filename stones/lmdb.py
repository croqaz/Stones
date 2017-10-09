
from .base import Base

try:
    import lmdb
except ModuleNotFoundError:
    print('LevelDB store requires PyPi.python.org/pypi/lmdb')
    exit(1)


class LmdbStore(Base):
    """
    LMDB container compatible with Python dicts.
    """

    __slots__ = ('db', 'table')

    def __init__(self, name, table=b''):
        self.db = lmdb.open(name + '.lmdb', max_dbs=9, map_size=8e12)
        self.table = None
        if table:
            self.table = self.db.open_db(table)

    def close(self):
        self.db.close()

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
