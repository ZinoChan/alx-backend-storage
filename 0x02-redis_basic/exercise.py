#!/usr/bin/env python3
"""Main"""

import redis
import uuid
from typing import Union, Callable, Optional, List
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


def call_history(method: Callable):
    """Call history"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        method_name = method.__qualname__

        input_key = f'{method_name}:inputs'
        output_key = f'{method_name}:outputs'

        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))

        return result

    return wrapper


def replay(redis_instance: redis.Redis, method: Callable) -> List[str]:
    """Replay history"""
    method_name = method.__qualname__

    input_key = f'{method_name}:inputs'
    output_key = f'{method_name}:outputs'

    input_history = redis_instance.lrange(input_key, 0, -1)
    output_history = redis_instance.lrange(output_key, 0, -1)

    history = []
    for i, (input_data, output_data) in enumerate(zip(input_history, output_history)):
        history.append({
            'Call Number': i + 1,
            'Input': input_data.decode('utf-8'),
            'Output': output_data.decode('utf-8')
        })

    return history


class Cache:
    """declare cache class"""

    def __init__(self):
        """init Redis client and flush db"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
