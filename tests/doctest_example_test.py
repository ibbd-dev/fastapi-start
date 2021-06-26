# -*- coding: utf-8 -*-
#
# pytest单元测试
# Author: caiyingyao
# Email: cyy0523xc@gmail.com
# Created Time: 2021-06-26
import pytest
from .doctest_example import func


def test_func():
    assert func(10) == 20
    assert func(20) == 40


@pytest.mark.parametrize("args, expected", [([10], 20), ([20], 30)])
def test_func2(args, expected):
    assert func(*args) == expected


test_data = [
    (func, [10], {}, 20), 
    (func, [20], {}, 30)
]


@pytest.mark.parametrize("action, args, kwargs, expected", test_data)
def test_func3(action, args, kwargs, expected):
    assert action(*args, **kwargs) == expected
