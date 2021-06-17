# -*- coding: utf-8 -*-
#
# API接口调用
# Author: caiyingyao
# Email: cyy0523xc@gmail.com
# Created Time: 2021-06-16
# redis连接在公共模块里
from redis import Redis

# 验证码配置
cfg = {
    'prefix': 'ctc',   # redis key前缀
    'expire': 5 * 60,    # 过期时间
}


def config(expire=5 * 60, prefix='ctc'):
    """配置redis
    Args:
        expire int: 过期秒数
        prefix str: 验证码key前缀
    """
    global cfg
    cfg['expire'] = expire
    cfg['prefix'] = prefix


def check_code(redis: Redis, token: str, code: str) -> bool:
    """校验验证码"""
    token = f"{cfg['prefix']}_{token}"
    code = code.lower().strip()
    saved_code = redis.get(token)
    if saved_code is None:
        return False
    redis.delete(token)   # 验证码只能用一次
    saved_code = str(saved_code, encoding='utf8')
    # print(f'{saved_code} == {code}')
    return saved_code == code


def set_captcha(redis: Redis, token: str, code: str):
    """设置验证码"""
    token = f"{cfg['prefix']}_{token}"
    code = code.lower()
    return redis.set(token, code, ex=cfg['expire'])


if __name__ == '__main__':
    # python api.py 192.168.1.242
    import sys
    import os
    sys.path.insert(0, os.path.split(sys.path[0])[0])

    from common.connections import init_redis, get_redis
    init_redis(host=sys.argv[1])
    redis = next(get_redis())

    code = '23kf'
    set_captcha(redis, 'test', code)
    assert check_code(redis, 'test', 'test') is False
    assert check_code(redis, 'test', code) is False

    set_captcha(redis, 'test', code)
    assert check_code(redis, 'test', code) is True
    assert check_code(redis, 'test', code) is False
