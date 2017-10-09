
import collections.abc

class Base(collections.abc.MutableMapping):

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]
        self[key] = default
        return default
