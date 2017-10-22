
from collections.abc import MutableMapping
from .exceptions import EncodeException
from .encoders import encoders


class BaseStore(MutableMapping):

    __slots__ = ('_type', '_encode', '_decode')

    def __init__(self, encoder=None, encode_decode=tuple(), value_type=bytes):
        self._type = value_type
        if value_type == bytes:
            self._encode = encoders['noop']['encode']
            self._decode = encoders['noop']['encode']
        else:
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


    def set_add(self, key, value):
        """
        Add a value in the set found at key
        """
        if self._type != set:
            raise TypeError('Value type must be set')
        kset = set(self.get(key, set()))
        kset.add(value)
        self[key] = kset


    def set_remove(self, key, value):
        """
        Remove a value from the set found at key
        """
        if self._type != set:
            raise TypeError('Value type must be set')
        kset = set(self.get(key, set()))
        kset.discard(value)
        self[key] = kset


    def list_append(self, key, value):
        """
        Add a value in the list found at key
        """
        if self._type != list:
            raise TypeError('Value type must be list')
        klist = list(self.get(key, []))
        klist.append(value)
        self[key] = klist


    def list_remove(self, key, value):
        """
        Remove a value from the list found at key
        """
        if self._type != list:
            raise TypeError('Value type must be list')
        klist = list(self.get(key, []))
        klist.remove(value)
        self[key] = klist
