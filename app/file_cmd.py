# -*- coding: utf-8 -*-
#
# 文件命令
# Author: alex
# Created Time: 2021年06月13日 星期日
import re
import os
import shutil
from os.path import join
from .settings import package_path
from .utils import init_file
from .config_cmd import get_config


class File:
    """文件操作(生成规范格式的Python文档，readme文档等)

    Examples:
        生成Python文件:
            fas file python test --desc=这是测试文件
        生成Readme文件:
            fas file readme --title=测试标题 --desc=测试描述
    """

    def python(self, filename: str, desc: str = ''):
        """生成规范格式的Python文件
        Args:
            filename str: 文件名（会自动加上后缀.py）
            desc str: 文件描述信息
        """
        python_create(filename, desc)

    def readme(self, title: str = '', desc: str = ''):
        """生成规范的readme文件
        Args:
            title str: readme文件标题
            desc str: 描述信息
        """
        readme_create(title, desc)


def readme_create(title: str, desc: str):
    """readme文件"""
    filename = 'README.md'
    if os.path.isfile(filename):
        raise Exception(f"file name: {filename} is existed!")
    shutil.copyfile(join(package_path, 'data', filename), filename)
    cfg = get_config()
    replaces = {'title': title, 'desc': desc}
    init_file(filename, cfg['author'], cfg['email'], replaces=replaces)
    print(f'create {filename} ok.')


def python_create(filename: str, desc: str):
    """python文件创建"""
    name_pattern = '^[a-z0-9_\\.]{3,20}$'
    if re.match(name_pattern, filename):
        print("file name check ok")
    else:
        raise Exception(f'file name check error: {name_pattern}')
    if not filename.endswith('.py'):
        filename += '.py'
    if os.path.isfile(filename):
        raise Exception(f"file name: {filename} is existed!")

    print('create file...')
    src_path = os.path.dirname(os.path.realpath(__file__))
    shutil.copyfile(join(src_path, 'data', 'example.py'), filename)
    cfg = get_config()
    replaces = {'desc': desc.replace('\n', '\n# ')}
    init_file(filename, cfg['author'], cfg['email'], replaces=replaces)
    print('--> ok.')
    print(f'init filename: {filename} ok.')
