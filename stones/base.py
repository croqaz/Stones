
from collections.abc import MutableMapping
from .encoders import encoders


class Base(MutableMapping):

    def __init__(self, encoder=None, encode_decode=tuple()):
        if encoder and encoder in encoders:
            self._encode = encoders[encoder]['encode']
            self._decode = encoders[encoder]['decode']
        elif encode_decode and len(encode_decode) == 2:
            self._encode, self._decode = encode_decode
        else:
            raise Exception('The store needs an encoder and a decoder')

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]
        self[key] = default
        return default
