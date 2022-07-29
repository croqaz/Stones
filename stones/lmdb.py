import shutil
import itertools
import contextlib
from .base import BaseStore

try:
    import lmdb
except ModuleNotFoundError:
    print('LMDB store requires PyPi.python.org/pypi/lmdb')

LMDB_ENVIRONMENT = {'max_dbs': 9, 'map_size': int(8e12)}


class LmdbStore(BaseStore):
    """
    LMDB ‘Lightning’ Database container, compatible with Python dicts.
    Keys and values MUST be byte strings.
    """

    __slots__ = ('db', 'table', '_name')

    def __init__(self,
                 name,
                 table=None,
                 serialize='json',
                 dump_load=tuple(),
                 value_type=bytes,
                 iterable=tuple(),
                 database={},
                 kwargs={}):
        super().__init__(serialize=serialize, dump_load=dump_load, value_type=value_type)
        self._name = name
        self.db = lmdb.open(self._name, **{**LMDB_ENVIRONMENT, **database})
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
                txn.put(key, self._encode(value), dupdata=False)

    # def put_bytes(self, key, raw, dupdata=False, overwrite=False):
    #     """ Inject raw bytes """
    #     if not isinstance(raw, bytes):
    #         raise TypeError('Raw data must be Bytes')
    #     with self.db.begin(write=True, db=self.table) as txn:
    #         txn.put(key, raw, dupdata=dupdata, overwrite=overwrite)

    def get(self, key, default=None):
        with self.db.begin(db=self.table) as txn:
            encoded_value = txn.get(self._enc_key(key), None)
            return self._decode(encoded_value) if encoded_value else default

    def put(self, key, value, overwrite=False):
        enc_key = self._enc_key(key)
        with self.db.begin(write=True, db=self.table) as txn:
            txn.put(enc_key, self._encode(value), overwrite=overwrite, dupdata=False)

    def delete(self, key):
        with self.db.begin(write=True, db=self.table) as txn:
            return txn.delete(self._enc_key(key))

    def __getitem__(self, key):
        with self.db.begin(db=self.table) as txn:
            encoded_value = txn.get(self._enc_key(key))
            return self._decode(encoded_value)

    def __setitem__(self, key, value):
        with self.db.begin(write=True, db=self.table) as txn:
            txn.put(self._enc_key(key), self._encode(value), dupdata=False)

    __delitem__ = delete

    def __contains__(self, key):
        enc_key = self._enc_key(key)
        with self.db.begin(db=self.table) as txn:
            return bool(txn.get(enc_key))

    def __len__(self):
        with self.db.begin(db=self.table) as txn:
            return txn.stat()['entries']

    def __iter__(self):
        with self.db.begin(db=self.table) as txn:
            yield from txn.cursor().iternext(keys=True, values=False)

    def __repr__(self):
        items = dict(self.items())
        return self.__class__.__name__ + repr(items)

    def keys(self):
        with self.db.begin(db=self.table) as txn:
            yield from txn.cursor().iternext(keys=True, values=False)

    def values(self):
        with self.db.begin(db=self.table) as txn:
            for value in txn.cursor().iternext(keys=False, values=True):
                yield self._decode(value)

    def items(self):
        items_list = []
        with self.db.begin(db=self.table) as txn:
            for key, value in txn.cursor().iternext(keys=True, values=True):
                items_list.append((key, self._decode(value)))
        return items_list

    def update(self, iterable=tuple(), **kwargs):
        self._populate(iterable, **kwargs)

    def clear(self):
        with self.db.begin(write=True) as txn:
            txn.drop(self.table, delete=False)

    def destroy(self, yes_im_sure=False):
        if yes_im_sure:
            self.close()
            shutil.rmtree(self._name)
