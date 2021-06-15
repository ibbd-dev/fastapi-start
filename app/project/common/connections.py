# -*- coding: utf-8 -*-
#
# mysql，redis等连接函数
# Author: __author__
# Email: __email__
# Created Time: __created_time__
import redis

# redis pool
redis_pool = None


def init_redis(host: str, port=6379, db=0):
    """配置redis """
    global redis_pool
    redis_pool = redis.ConnectionPool(host=host, port=port, db=db)


def get_redis():
    """获取redis操作对象"""
    return redis.Redis(connection_pool=redis_pool)


if __name__ == '__main__':
    import sys
    init_redis(sys.argv[1])
    r = get_redis()
    r.set('key', 'val', 10)
    assert str(r.get('key'), encoding='utf8') == 'val'
