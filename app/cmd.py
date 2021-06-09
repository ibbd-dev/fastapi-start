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
    """配置"""
    with open(config_file, 'w', encoding='utf8') as f:
        data = {'author': author}
        json.dump(data, f)


def get_config() -> Dict[str, str]:
    with open(config_file, encoding='utf8') as f:
        data = json.load(f)
    if 'author' not in data:
        data['author'] = ''
    return data


def project_init(project_name: str, title: str=None, desc: str=""):
    """项目初始化"""
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
    
    # vscode
    print('parse vscode settings and gitignore...')
    os.mkdir(join(project_name, ".vscode"))
    shutil.copy(join(package_path, 'data', 'vscode_settings.json'), 
                join(project_name, ".vscode"))
    shutil.copy(join(package_path, 'data', 'gitignore'), 
                join(project_name, ".gitignone"))
    print('--> ok.')

    # 生成md文件
    print('create md file...')
    with open(join(project_name, "README.md"), 'w', encoding='utf8') as f:
        f.write(f"# {title}\n{desc}")
    with open(join(project_name, "install.md"), 'w', encoding='utf8') as f:
        f.write(f"# {title}: 安装部署与运维文档")
    print('--> ok.')
    
    # 复制app目录
    cfg = get_config()
    print('copy and parse app files...')
    shutil.copy(join(package_path, 'app'), project_name)
    for filename in os.listdir(join(project_name, "app")):
        if not filename.endswith('.py'):
            continue
        if not init_pyfile(join(project_name, 'app', filename), cfg['author']):
            raise Exception('init python file error: '+ join('app', filename))
    print('--> ok.')
    print(f'init project: {project_name} ok.')


def module_add(module_name: str, prefix: str=None, tags: str=None):
    """增加模块"""
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
    shutil.copy(join(project_path, 'module'), module_name)
    for filename in os.listdir(module_name):
        if not filename.endswith('.py'):
            continue
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
    shutil.copy(join(src_path, 'data', 'example.py'), filename)
    cfg = get_config()
    init_pyfile(filename, cfg['author'])
    print('--> ok.')
    print(f'init filename: {filename} ok.')


def code_check():
    """代码检测"""
    print("该功能正在开发中...")