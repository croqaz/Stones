from collections.abc import MutableMapping
from .exceptions import EncoderException
from .serialize import serializers


class BaseStore(MutableMapping):
    """
    The Store represents storage for any key-value pair.

    This is an abstract class and should not be used directly.
    """

    __slots__ = ('_type', '_encode', '_decode')

    def __init__(self, serialize=None, dump_load=tuple(), value_type=bytes):
        self._type = value_type
        if serialize and serialize in serializers:
            self._encode = serializers[serialize]['encode']
            self._decode = serializers[serialize]['decode']
        elif dump_load and len(dump_load) == 2:
            self._encode, self._decode = dump_load
        else:
            raise EncoderException('The store needs an encoder and a decoder')

    def _enc_key(self, k):
        if isinstance(k, str):
            return k.encode('utf8')
        return k

    def get(self, key):
        raise NotImplementedError

    def put(self, key, value):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def destroy(self, yes_im_sure=False):
        raise NotImplementedError

    def setdefault(self, key, default=None):
        """
        If key is in the dictionary, return its value.
        If not, insert key with a value of default and return default.
        """
        if key in self:
            return self[key]
        self[key] = default
        return default

    def deep_add(self, key, value):
        """
        Add a value in the deep structure found at key.
        The deep structure can be a list, or a set.
        """
        data = self._type(self.get(key, []))
        if hasattr(data, 'add'):
            data.add(value)
        elif hasattr(data, 'append'):
            data.append(value)
        else:
            raise TypeError('Cannot add value in a "{}"'.format(type(data)))
        self[key] = data

    def deep_remove(self, key, value):
        """
        Remove a value from the deep structure found at key.
        The deep structure can be a list, or a set.
        """
        data = self._type(self.get(key, []))
        if hasattr(data, 'discard'):
            data.discard(value)
        elif hasattr(data, 'remove'):
            data.remove(value)
        else:
            raise TypeError('Cannot del value from a "{}"'.format(type(data)))
        self[key] = data
