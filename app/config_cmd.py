# -*- coding: utf-8 -*-
#
# 配置相关命令
# Author: alex
# Created Time: 2021年06月13日 星期日
from os import mkdir
from os.path import join, isdir, isfile, expanduser
import json
from typing import Dict
# from .settings import package_path
from .utils import get_user_from_git

# 工具的配置目录
config_path = join(expanduser('~'), '.fastapi-start')
config_file = join(config_path, 'config.json')
if not isdir(config_path):
    mkdir(config_path)


class Config:
    """配置代码根目录等信息
    配置文件的保存目录为: 用户目录/.fastapi-start/

    Examples:
        获取配置信息（author和email直接从git的配置中获取）：
            fas config get
        设置代码根目录（使用clone命令时，需要该目录）：
            fas config set --root-path=/var/www
    """

    def get(self):
        """获取配置变量的信息
        """
        return get_config()

    def set(self, root_path: str = ''):
        """设置配置变量
        Args:
            root_path str: 代码根目录，使用clone命令的时候会在该目录下生成标准的目录路径，如: root_path/github.com/username/project/
        """
        config_set(root_path=root_path)


def config_set(root_path: str = ''):
    """"""
    if isfile(config_file):
        with open(config_file, encoding='utf8') as f:
            data = json.load(f)
    else:
        data = {}

    if root_path:
        if not isdir(root_path):
            raise Exception(f'代码根目录不是有效目录：{root_path}')
        data['root_path'] = root_path
    if data:
        with open(config_file, 'w', encoding='utf8', newline='') as f:
            json.dump(data, f)


def get_config() -> Dict[str, str]:
    """获取配置信息
    用户名及Email从git配置获取
    Returns:
        dict
    """
    author, email = get_user_from_git()
    if not isfile(config_file):
        return {'author': author, 'email': email}
    with open(config_file, encoding='utf8') as f:
        data = json.load(f)
    data['author'], data['email'] = author, email
    return data
