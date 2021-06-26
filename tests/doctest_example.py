# -*- coding: utf-8 -*-
#
# doctest测试
# Author: caiyingyao
# Email: cyy0523xc@gmail.com
# Created Time: 2021-06-20
"""
# 模块测试
>>> func(10)
20
"""


def func(i: int) -> int:
    """函数测试
    >>> func(10)
    21
    """
    return i * 2


if __name__ == "__main__":
    import doctest
    doctest.testmod()
