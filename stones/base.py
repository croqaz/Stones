
import collections.abc
import msgpack


class Base(collections.abc.MutableMapping):

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]
        self[key] = default
        return default

    @staticmethod
    def _encode(value):
        encoded = msgpack.packb(value, use_bin_type=True)
        return encoded

    @staticmethod
    def _decode(value):
        decoded = msgpack.unpackb(value)
        return decoded
