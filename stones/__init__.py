# flake8: noqa

from .memory import MemoryStore
from .lmdb import LmdbStore
from .serialize import serializers
from .exceptions import EncoderException


def stone(name, store=MemoryStore, serialize='pickle', dump_load=tuple(), value_type=bytes, options={}):
    """
    Convenience wrapper for returning a Store instance.
    """
    if serialize and serialize not in serializers:
        raise EncoderException('Invalid serializer name "{}"'.format(serialize))
    return store(name, serialize=serialize, dump_load=dump_load, value_type=value_type, **options)
