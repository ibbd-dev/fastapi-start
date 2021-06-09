# -*- coding: utf-8 -*-
#
# 工具函数库
# Author: alex
# Created Time: 2021年06月08日 星期二
from datetime import datetime


def init_pyfile(path: str, author: str) -> bool:
    """初始化单个py文件
    生成作者和日期
    """
    with open(path, encoding='utf8') as f:
        text = f.read()
    today = datetime.strftime("%Y-%m-%d")
    text.replace('__author__', author)
    text.replace('__created_time__', today)
    with open(path, 'w', encoding='utf8') as f:
        f.write(text)
    return True