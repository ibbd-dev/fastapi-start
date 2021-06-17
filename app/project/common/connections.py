# -*- coding: utf-8 -*-
#
# mysql，redis等连接函数
# Author: __author__
# Email: __email__
# Created Time: __created_time__
import redis

# redis pool
_redis_pool = None


def init_redis(host: str, port=6379, db=0):
    """配置redis """
    global _redis_pool
    _redis_pool = redis.ConnectionPool(host=host, port=port, db=db)


def get_redis() -> redis.Redis:
    """获取redis操作对象
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接
    """
    # 检查间隔(health_check_interval)的含义:
    # 当连接在health_check_interval秒内没有使用下次使用时需要进行健康检查。
    # 在内部是通过发送ping命令来实现
    r = redis.Redis(connection_pool=_redis_pool, health_check_interval=30)
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
