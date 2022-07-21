# -*- coding: utf-8 -*-
#
# 接口单元测试脚本（使用pytest）
#     sudo docker exec -ti container_name pytest __module_name__/router_test.py
#
# Author: __author__
# Email: __email__
# Created Time: __created_time__
import os
import sys
run_path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, run_path)
print("运行目录:", run_path)


def test_api():
    """单元测试代码"""
    assert 1 == 1
