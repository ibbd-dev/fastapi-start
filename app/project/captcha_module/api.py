# -*- coding: utf-8 -*-
#
# API接口调用
# Author: __author__
# Email: __email__
# Created Time: __created_time__
import redis

# redis配置
cfg = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'prefix': 'ctc',   # redis key前缀
    'expire': 5 * 60,    # 过期时间
}
# redis pool
pool = None


def config(host: str, port=6379, expire=5 * 60, db=0, prefix='ctc'):
    """配置redis
    Args:
        expire int: 过期秒数
        prefix str: 验证码key前缀
    """
    global cfg, pool
    cfg['host'] = host
    cfg['port'] = port
    cfg['db'] = db
    cfg['expire'] = expire
    cfg['prefix'] = prefix
    pool = redis.ConnectionPool(host=host, port=port, db=db)


def check_code(token: str, code: str) -> bool:
    """校验验证码"""
    token = f"{cfg['prefix']}_{token}"
    code = code.lower().strip()
    saved_code = _redis().get(token)
    if saved_code is None:
        return False
    _redis().delete(token)   # 验证码只能用一次
    saved_code = str(saved_code, encoding='utf8')
    # print(f'{saved_code} == {code}')
    return saved_code == code


def set_captcha(token: str, code: str):
    """设置验证码"""
    token = f"{cfg['prefix']}_{token}"
    code = code.lower()
    return _redis().set(token, code, ex=cfg['expire'])


def _redis():
    return redis.Redis(connection_pool=pool)


if __name__ == '__main__':
    import sys
    config(host=sys.argv[1])

    code = '23kf'
    set_captcha('test', code)
    assert check_code('test', 'test') is False
    assert check_code('test', code) is False

    set_captcha('test', code)
    assert check_code('test', code) is True
    assert check_code('test', code) is False