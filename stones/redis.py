
from .base import Base
import itertools
import contextlib


class RedisStore(Base):
    """
    Redis-backed container compatible with Python dicts.
    """

    def __init__(self, redis, key, iterable=tuple(), **kwargs):
        self._redis = redis
        self._key = key
        if iterable or kwargs:
            if self.redis.exists(self.key):
                raise KeyExistsError(self.redis, self.key)
            else:
                self._populate(iterable, **kwargs)

    @property
    def redis(self):
        return self._redis

    @property
    def key(self):
        return self._key

    def close(self):
        self._redis.close()

    def _populate(self, iterable=tuple(), **kwargs):
        hm_set = []
        with contextlib.suppress(AttributeError):
            iterable = iterable.items()
        for key, value in itertools.chain(iterable, kwargs.items()):
            hm_set.append(key)
            hm_set.append(self._encode(value))
        if hm_set:
            self.redis.multi()
            self.redis.hmset(self.key, *hm_set)
            self.redis.exec()

    def get(self, key, default=None):
        return self[key] if key in self else default

    def put(self, key, value, overwrite=False):
        if not overwrite and self.redis.hget(self.key, key):
            return
        self.redis.hset(self.key, key, self._encode(value))

    def delete(self, key):
        return bool(self.redis.hdel(self.key, key))

    def __getitem__(self, key):
        encoded_value = self.redis.hget(self.key, key)
        return self._decode(encoded_value)

    def __setitem__(self, key, value):
        self.redis.hset(self.key, key, self._encode(value))

    __delitem__ = delete

    def __contains__(self, key):
        return bool(self.redis.hexists(self.key, key))

    def __len__(self):
        return self.redis.hlen(self.key)

    def __iter__(self):
        yield from self.redis.hkeys(self.key)

    def __repr__(self):
        items = dict(self.items())
        return self.__class__.__name__ + repr(items)

    def keys(self):
        return self.redis.hkeys(self.key)

    def values(self):
        return [self._decode(val) for val in self.redis.hvals(self.key)]

    def items(self):
        items = self.redis.hgetall(self.key)
        keys = items[::2]
        vals = (self._decode(val) for val in items[1::2])
        return list(zip(keys, vals))

    def update(self, iterable=tuple(), **kwargs):
        """
        Update data in place.
        """
        self._populate(iterable, **kwargs)

    def clear(self):
        """
        Remove all elements from a Redis-backed container.
        """
        self.redis.delete(self.key)
