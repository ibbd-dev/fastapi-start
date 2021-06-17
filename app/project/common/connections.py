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


def get_redis() -> redis.Redis:
    """获取redis操作对象
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接
    """
    # return redis.Redis(connection_pool=redis_pool)
    r = redis.Redis(connection_pool=redis_pool)
    try:
        yield r
    finally:
        r.close()


if __name__ == '__main__':
    import sys
    init_redis(sys.argv[1])
    r = get_redis()
    r = next(r)
    print(r)
    r.set('key', 'val', 10)
    assert str(r.get('key'), encoding='utf8') == 'val'
