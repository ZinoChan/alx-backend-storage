#!/usr/bin/env python3

"""
Implementing an expiring web cache and tracker.
"""

import redis
import requests

redis_connection = redis.Redis()
initial_count = 0


def get_page(url: str) -> str:
    """
    Track how many times a particular
    URL was accessed
    """
    count_key = f"count:{url}"
    cache_key = f"cached:{url}"

    redis_connection.set(cache_key, initial_count)
    response = requests.get(url)
    redis_connection.incr(count_key)
    redis_connection.setex(cache_key, 10, redis_connection.get(cache_key))

    return response.text


if __name__ == "__main__":
    url_to_fetch = 'http://slowwly.robertomurray.co.uk'
    get_page(url_to_fetch)
