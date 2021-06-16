# -*- coding: utf-8 -*-
#
# 配置相关命令
# Author: alex
# Created Time: 2021年06月13日 星期日
import os
from os.path import join
import json
from typing import Dict
from .settings import package_path
from .utils import get_user_from_git

config_file = join(package_path, 'config.json')


class Config:
    """配置author, email，代码根目录等信息

    Examples:
        获取配置信息（如果没有设置author或者email，则自动从git中获取）:
            fas config get
        设置代码根目录（使用clone命令时，需要该目录）：
            fas config set --root-path=/var/www
    """

    def get(self):
        """获取配置变量的信息
        """
        return get_config()

    def set(self, author: str = '', email: str = '', root_path: str = ''):
        """设置配置变量
        Args:
            author str: 用户名，如果不设置则从git命令中获取
            email str: email，如果不设置则从git命令中获取
            root_path str: 代码根目录，使用clone命令的时候会在该目录下生成标准的目录路径，如: root_path/github.com/username/project/
        """
        config_set(author=author, email=email, root_path=root_path)


def config_set(author: str = '', email: str = '', root_path: str = ''):
    """"""
    if os.path.isfile(config_file):
        with open(config_file, encoding='utf8') as f:
            data = json.load(f)
    else:
        data = {}
    if author:
        data['author'] = author
    if email:
        data['email'] = email
    if root_path:
        if not os.path.isdir(root_path):
            raise Exception(f'代码根目录不是有效目录：{root_path}')
        data['root_path'] = root_path
    if data:
        with open(config_file, 'w', encoding='utf8', newline='') as f:
            json.dump(data, f)


def get_config() -> Dict[str, str]:
    """获取配置信息
    Returns:
        dict
    """
    if not os.path.isfile(config_file):
        author, email = get_user_from_git()
        if author == '':
            raise Exception("需要先设置用户名，帮助文档:\n    fastapi-start config --help")
        return {'author': author, 'email': email}
    with open(config_file, encoding='utf8') as f:
        data = json.load(f)
    if 'author' not in data or data['author'] == '':
        data['author'], data['email'] = get_user_from_git()
    return data
