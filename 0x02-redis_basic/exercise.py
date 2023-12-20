#!/usr/bin/env python3
"""Main"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count how many times methods of Cache class are called"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrap the decorated"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """declare cache class"""

    def __init__(self):
        """init Redis client and flush db"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, float, bytes, int]) -> str:
        """set data in redis"""
        randKey = str(uuid.uuid4())
        self._redis.set(randKey, data)
        return randKey

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, float, bytes, int]:
        value = self._redis.get(key)
        if value:
            value = fn(value)
        return value

    def get_str(self, key: str):
        """Get data as str"""
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str):
        return self.get(key, fn=int)
