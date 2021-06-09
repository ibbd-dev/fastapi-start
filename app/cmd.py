# -*- coding: utf-8 -*-
#
# 命令
# Author: alex
# Created Time: 2021年06月08日 星期二
import re
import os
from os.path import join
import json
import shutil
from typing import Dict
from .utils import init_pyfile

package_path = os.path.dirname(os.path.realpath(__file__))
config_file = join(package_path, 'config.json')


def config(author: str):
    """配置用户名等信息
    :param author str: 用户名
    """
    with open(config_file, 'w', encoding='utf8', newline='') as f:
        data = {'author': author}
        json.dump(data, f)


def get_config() -> Dict[str, str]:
    if not os.path.isfile(config_file):
        raise Exception("需要先设置用户名，帮助文档:\n    fastapi-start config --help")
    with open(config_file, encoding='utf8') as f:
        data = json.load(f)
    if 'author' not in data or data['author'] == '':
        raise Exception("需要先设置用户名，帮助文档:\n    fastapi-start config --help")
    return data


def project_init(project_name: str, title: str=None, desc: str=""):
    """项目初始化
    :param project_name str: 项目名（目录名）
    :param title str: 项目标题（显示在交互式文档中）
    :param desc str: 项目描述（显示在交互式文档中）
    """
    # 创建项目目录
    name_pattern = '^[a-z0-9\-]{4,20}$'
    if re.match(name_pattern, project_name):
        print("project name check ok")
    else:
        raise Exception(f'project name check error: {name_pattern}')
    if os.path.isdir(project_name):
        raise Exception(f"project name: {project_name} is existed!")
    os.mkdir(project_name)
    if title is None:
        title = project_name
    
    # vscode, gitignore, Dockerfile
    cfg = get_config()
    print('parse vscode settings, Dockerfile and gitignore...')
    os.mkdir(join(project_name, ".vscode"))
    shutil.copyfile(join(package_path, 'data', 'vscode_settings.json'), 
                    join(project_name, ".vscode", "settings.json"))
    shutil.copyfile(join(package_path, 'data', 'gitignore'), 
                    join(project_name, ".gitignone"))
    shutil.copyfile(join(package_path, 'data', 'Dockerfile'), 
                    join(project_name, 'Dockerfile'))
    init_pyfile(join(project_name, 'Dockerfile'), cfg['author'])
    print('--> ok.')

    # 生成md文件
    print('create md file...')
    with open(join(project_name, "README.md"), 'w', encoding='utf8', newline='') as f:
        f.write(f"# {title}\n{desc}")
    with open(join(project_name, "install.md"), 'w', encoding='utf8', newline='') as f:
        f.write(f"# {title}: 安装部署与运维文档")
    print('--> ok.')
    
    # 复制app目录
    print('copy and parse app files...')
    src_path = join(package_path, 'project')
    dst_path = join(project_name, 'app')
    os.mkdir(dst_path)
    with open(join(dst_path, "readme.md"), 'w', encoding='utf8', newline='') as f:
        f.write(f"# {title}\n{desc}")

    for filename in os.listdir(src_path):
        if not filename.endswith('.py'):
            continue
        shutil.copyfile(join(src_path, filename), join(dst_path, filename))
        if not init_pyfile(join(dst_path, filename), cfg['author']):
            raise Exception('init python file error: '+ join(dst_path, filename))
    print('--> ok.')
    print(f'init project: {project_name} ok.')


def module_add(module_name: str):
    """增加模块（应该在项目的app目录下执行）
    :param module_name str: 模块名
    """
    name_pattern = '^[a-z0-9_]{4,20}$'
    if re.match(name_pattern, module_name):
        print("module name check ok")
    else:
        raise Exception(f'module name check error: {name_pattern}')
    if os.path.isdir(module_name):
        raise Exception(f'module name: {module_name} is existed!')
    cfg = get_config()
    project_path = os.path.dirname(os.path.realpath(__file__))

    print('copy and parse app files...')
    src_path = join(project_path, 'module')
    os.mkdir(module_name)
    for filename in os.listdir(src_path):
        if not filename.endswith('.py'):
            continue
        shutil.copyfile(join(src_path, filename), join(module_name, filename))
        if not init_pyfile(join(module_name, filename), cfg['author']):
            raise Exception('init python file error: '+ join(module_name, filename))
    print('--> ok.')
    print(f'init module: {module_name} ok.')

def py_file_add(filename: str):
    """生成Python文件"""
    name_pattern = '^[a-z0-9_\.]{4,20}$'
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
    init_pyfile(filename, cfg['author'])
    print('--> ok.')
    print(f'init filename: {filename} ok.')


def code_check():
    """代码检测"""
    print("该功能正在开发中...")