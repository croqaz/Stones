
import itertools
import contextlib
from .base import Base


class RedisStore(Base):
    """
    Redis-backed container compatible with Python dicts.
    Keys and values MUST be byte strings.
    """

    __slots__ = ('redis', 'redis_key')

    def __init__(self, redis, redis_key, encoder='cbor', iterable=tuple(), **kwargs):
        super().__init__(encoder=encoder)
        self.redis = redis
        self.redis_key = redis_key
        if iterable or kwargs:
            self._populate(iterable, **kwargs)

    def close(self):
        self.redis.close()


    def _populate(self, iterable=tuple(), **kwargs):
        hm_set = []
        with contextlib.suppress(AttributeError):
            iterable = iterable.items()
        for key, value in itertools.chain(iterable, kwargs.items()):
            hm_set.append(key)
            hm_set.append(self._encode(value))
        if hm_set:
            self.redis.multi()
            self.redis.hmset(self.redis_key, *hm_set)
            self.redis.exec()


    def get(self, key, default=None):
        return self[key] if key in self else default

    def put(self, key, value, overwrite=False):
        if not overwrite and self.redis.hget(self.redis_key, key):
            return
        self.redis.hset(self.redis_key, key, self._encode(value))

    def delete(self, key):
        return bool(self.redis.hdel(self.redis_key, key))


    def __getitem__(self, key):
        encoded_value = self.redis.hget(self.redis_key, key)
        return self._decode(encoded_value)

    def __setitem__(self, key, value):
        self.redis.hset(self.redis_key, key, self._encode(value))

    __delitem__ = delete


    def __contains__(self, key):
        return bool(self.redis.hexists(self.redis_key, key))

    def __len__(self):
        return self.redis.hlen(self.redis_key)

    def __iter__(self):
        yield from self.redis.hkeys(self.redis_key)

    def __repr__(self):
        items = dict(self.items())
        return self.__class__.__name__ + repr(items)


    def keys(self):
        return self.redis.hkeys(self.redis_key)

    def values(self):
        return [self._decode(val) for val in self.redis.hvals(self.redis_key)]

    def items(self):
        items = self.redis.hgetall(self.redis_key)
        keys = items[::2]
        vals = (self._decode(val) for val in items[1::2])
        return list(zip(keys, vals))


    def update(self, iterable=tuple(), **kwargs):
        self._populate(iterable, **kwargs)

    def clear(self):
        self.redis.delete(self.redis_key)
