#!/usr/bin/env python3
"""Main"""

import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """declare cache class"""

    def __init__(self):
        """init Redis client and flush db"""
        self._redis = redis.Redis()
        self._redis.flashdb()

    def store(self, data: Union[str, float, bytes, int]) -> str:
        """set data in redis"""
        randKey = str(uuid.uuid4())
        self._redis.set(randKey, data)
        return randKey

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, float, bytes, int]:
        value = self._redis.get(key)
        if value:
            value = fn(value)
        return value

    def get_str(self, key: str):
        """Get data as str"""
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str):
        return self.get(key, fn=int)
