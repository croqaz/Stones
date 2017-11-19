
#- rev: v3 -
#- hash: JHSNSV -

from collections.abc import MutableMapping
from .exceptions import EncodeException
from .encoders import encoders


class BaseStore(MutableMapping):

    __slots__ = ('_type', '_encode', '_decode')

    def __init__(self, encoder=None, encode_decode=tuple(), value_type=bytes):
        self._type = value_type
        if encoder and encoder in encoders:
            self._encode = encoders[encoder]['encode']
            self._decode = encoders[encoder]['decode']
        elif encode_decode and len(encode_decode) == 2:
            self._encode, self._decode = encode_decode
        else:
            raise EncodeException('The store needs an encoder and a decoder')

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]
        self[key] = default
        return default

    def deep_add(self, key, value):
        """
        Add a value in the structure found at key
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
        Remove a value from the structure found at key
        """
        data = self._type(self.get(key, []))
        if hasattr(data, 'discard'):
            data.discard(value)
        elif hasattr(data, 'remove'):
            data.remove(value)
        else:
            raise TypeError(
                'Cannot remove value from a "{}"'.format(type(data)))
        self[key] = data
