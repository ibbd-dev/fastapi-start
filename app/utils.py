# -*- coding: utf-8 -*-
#
# 工具函数库
# Author: alex
# Created Time: 2021年06月08日 星期二
import os
from datetime import datetime
from typing import Dict, Tuple


def init_pyfile(path: str, author: str, email: str, replaces: Dict[str, str]=None) -> bool:
    """初始化单个py文件
    生成作者和日期
    """
    with open(path, encoding='utf8') as f:
        text = f.read()
    today = datetime.now().strftime("%Y-%m-%d")
    text = text.replace('__author__', author)
    text = text.replace('__email__', email)
    text = text.replace('__created_time__', today)
    if replaces is not None:
        for key, val in replaces.items():
            text = text.replace(key, val)
        
    with open(path, 'w', encoding='utf8', newline='') as f:
        f.write(text)
    return True


def get_user_from_git() -> Tuple[str, str]:
    """从git中获取用户名和邮箱"""
    username = os.popen('git config user.name').read().strip()
    email = os.popen('git config user.email').read().strip()
    return username, email