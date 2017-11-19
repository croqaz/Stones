
# flake8: noqa

from .memory import MemoryStore
from .encoders import encoders
from .exceptions import StoreException
from .exceptions import EncodeException


def stone(name, store=MemoryStore, encoder='pickle', encode_decode=tuple(),
          value_type=bytes, options={}):
    if encoder and encoder not in encoders:
        raise EncodeException('Invalid encoder name "{}"'.format(encoder))
    return store(name, encoder=encoder, encode_decode=encode_decode,
                 value_type=value_type, **options)
