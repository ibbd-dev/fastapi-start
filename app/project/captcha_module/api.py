# -*- coding: utf-8 -*-
#
# API接口调用
# Author: __author__
# Email: __email__
# Created Time: __created_time__
# redis连接在公共模块里
from common.connections import get_redis

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


def check_code(token: str, code: str) -> bool:
    """校验验证码"""
    token = f"{cfg['prefix']}_{token}"
    code = code.lower().strip()
    saved_code = get_redis().get(token)
    if saved_code is None:
        return False
    get_redis().delete(token)   # 验证码只能用一次
    saved_code = str(saved_code, encoding='utf8')
    # print(f'{saved_code} == {code}')
    return saved_code == code


def set_captcha(token: str, code: str):
    """设置验证码"""
    token = f"{cfg['prefix']}_{token}"
    code = code.lower()
    return get_redis().set(token, code, ex=cfg['expire'])


if __name__ == '__main__':
    import sys
    from common.connections import init_redis
    init_redis(host=sys.argv[1])

    code = '23kf'
    set_captcha('test', code)
    assert check_code('test', 'test') is False
    assert check_code('test', code) is False

    set_captcha('test', code)
    assert check_code('test', code) is True
    assert check_code('test', code) is False
