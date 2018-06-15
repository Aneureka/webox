# -*- coding: utf-8 -*-
"""
redis 相关操作
"""

import redis


_pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)


def get_redis():
    _redis = redis.Redis(connection_pool=_pool)
    return _redis


if __name__ == '__main__':
    r = get_redis()
    r.set('name', 'aaaba')
    print(r.get('access_token'))