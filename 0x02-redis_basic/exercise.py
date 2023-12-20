#!/usr/bin/env python3
"""Main"""

import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        """init Redis client and flush db"""
    self._redis = redis.Redis()
    self._redis.flashdb()

    def store(data: Union[str, float, bytes, int]) -> str:
        """set data in redis"""
        randKey = str(uuid.uuid4())
        self._redis.set(randKey, data)
        return randKey
