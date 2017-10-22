
# flake8: noqa
from .leveldb import LevelStore
from .lmdb import LmdbStore
from .redis import RedisStore

from .encoders import encoders
from .exceptions import StoreException
from .exceptions import EncodeException


def stone(name, persistence='level', encoder='pickle', encode_decode=tuple(),
        value_type=bytes, options={}):
    if encoder and encoder not in encoders:
        raise EncodeException(f'Invalid encoder name "{encoder}"')
    store_name = f'{persistence.title()}Store'
    if store_name not in globals():
        raise StoreException(f'Invalid store name "{store_name}"')
    stor = globals()[store_name]
    return stor(name, encoder=encoder, encode_decode=encode_decode,
        value_type=value_type, **options)
