
#- rev: v1 -
#- hash: VB7D8L -

import os
import dbm
from .memory import MemoryStore


class DbmStore(MemoryStore):
    """
    Shelve persistent, dictionary-like object.
    """

    __slots__ = ('db', '_name')

    def __init__(self, name, encoder='pickle', encode_decode=tuple(),
            value_type=bytes, iterable=tuple(), **kwargs):
        super().__init__(encoder=encoder, encode_decode=encode_decode, value_type=value_type)
        self._name = name + '.dbm'
        self.db = dbm.open(self._name, 'c')
        if iterable or kwargs:
            self._populate(iterable, **kwargs)

    def close(self):
        self.db.close()


    def __iter__(self):
        return iter(self.db.keys())

    def values(self):
        data = (self._decode(self.db[k]) for k in self.db.keys())
        return list(data)

    def items(self):
        data = ((k, self._decode(self.db[k])) for k in self.db.keys())
        return list(data)


    def clear(self):
        # FIXME: Really delete?
        for key in self.db.keys():
            self.db[key] = None

    def destroy(self, yes_im_sure=False):
        if yes_im_sure:
            self.close()
            os.remove(self._name)
