# -*- coding: utf-8 -*-
#
# 模块相关命令
# Author: caiyingyao
# Email: cyy0523xc@gmail.com
# Created Time: 2021-06-14
import re
import os
from os.path import join
import shutil
from .settings import package_path
from .utils import init_file
from .config_cmd import get_config


def module_action(action: str = 'get', module_name: str = '', title: str = '', desc: str = ''):
    """模块操作（应该在项目的app目录下执行）

    支持的action操作:
        get: 默认，获取已有可以直接使用的模块列表
        add: 添加一个已经实现的模块
        new: 新建一个全新的模块
    Args:
        action str: 模块操作:
        module_name str: 模块名（如果后缀不是_module，则会自动加上，减少冲突可能）
        title str: 模块说明文档标题
        desc str: 模块描述
    """
    if not module_name.endswith('_module'):
        module_name += '_module'
    if action == 'get':
        module_get()
    elif action == 'add':
        all_modules = module_get(is_return=True)
        if module_name not in all_modules:
            raise Exception(f'该模块尚未实现: {module_name}')
        module_new(module_name, title=title, desc=desc, src_module=module_name)
    elif action == 'new':
        module_new(module_name, title=title, desc=desc)
    else:
        raise Exception(f'不支持该操作: {action}')


def module_get(is_return=False):
    """获取支持的模块列表"""
    modules = []
    project_path = join(package_path, 'project')
    for module in os.listdir(project_path):
        if module.endswith('_module') and os.path.isdir(join(project_path, module)):
            modules.append(module)
    if is_return:
        return modules
    print('支持的模块列表：')
    for i, module in enumerate(modules):
        print(f"  {i+1}\t{module}")


def module_new(module_name: str, title: str = '', desc: str = '', src_module: str = 'module'):
    """新建模块（应该在项目的app目录下执行）
    Args:
        module_name str: 模块名（如果后缀不是_module，则会自动加上，减少冲突可能）
        title str: 模块说明文档标题
        desc str: 模块描述
    """
    name_pattern = '^[a-z0-9_]{3,30}$'
    if re.match(name_pattern, module_name):
        print("module name check ok")
    else:
        raise Exception(f'module name check error: {name_pattern}')
    if module_name.endswith('_module'):   # 加上统一的后缀避免冲突
        module_name = f'{module_name}_module'

    if os.path.isdir(module_name):
        raise Exception(f'module name: {module_name} is existed!')
    cfg = get_config()
    replaces = {'title': title if title else module_name, 'desc': desc}
    project_path = os.path.dirname(os.path.realpath(__file__))

    print('copy and parse app files...')
    src_path = join(project_path, 'project', src_module)
    os.mkdir(module_name)
    for filename in os.listdir(src_path):
        if not filename.endswith(('.py', '.md')):
            continue
        shutil.copyfile(join(src_path, filename), join(module_name, filename))
        if not init_file(join(module_name, filename), cfg['author'], cfg['email'], replaces=replaces):
            raise Exception('init file error: ' + join(module_name, filename))
    print('--> ok.')
    print(f'init module: {module_name} ok.')
