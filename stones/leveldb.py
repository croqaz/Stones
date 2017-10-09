
from .base import Base

try:
    import plyvel
except ModuleNotFoundError:
    print('LevelDB store requires PyPi.python.org/pypi/plyvel')
    exit(1)


class LevelStore(Base):

    __slots__ = 'db'

    def __init__(self, name):
        self.db = plyvel.DB(name + '.lvl', create_if_missing=True)

    def close(self):
        self.db.close()

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
