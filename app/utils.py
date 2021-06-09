# -*- coding: utf-8 -*-
#
# 工具函数库
# Author: alex
# Created Time: 2021年06月08日 星期二
from datetime import datetime
from typing import Dict


def init_pyfile(path: str, author: str, replaces: Dict[str, str]=None) -> bool:
    """初始化单个py文件
    生成作者和日期
    """
    with open(path, encoding='utf8') as f:
        text = f.read()
    today = datetime.now().strftime("%Y-%m-%d")
    text = text.replace('__author__', author)
    text = text.replace('__created_time__', today)
    if replaces is not None:
        for key, val in replaces.items():
            text = text.replace(key, val)
        
    with open(path, 'w', encoding='utf8') as f:
        f.write(text)
    return True