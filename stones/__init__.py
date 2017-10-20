
# flake8: noqa
from .leveldb import LevelStore
from .lmdb import LmdbStore
from .redis import RedisStore
from .ultra import UltraStore

from .encoders import encoders
from .exceptions import StoreException
from .exceptions import EncodeException


def stone(name, persistence='level', encoder='pickle'):
    if encoder not in encoders:
        raise EncodeException(f'Invalid encoder name "{encoder}"')
    store_name = f'{persistence.title()}Store'
    if store_name not in globals():
        raise StoreException(f'Invalid store name "{store_name}"')
    stor = type('Stone', (UltraStore, globals()[store_name]), {})
    return stor(name, encoder=encoder)
