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


def module_action(action: str = 'list', name: str = '', title: str = '', desc: str = ''):
    """模块操作（应该在项目的app目录下执行）

    支持的action操作:
        list: 获取已有可以直接使用的模块列表
        help: 已有模块的帮助文档
        add: 添加一个已经实现的模块
        new: 新建一个全新的模块
    Examples:
        fas module list     # 已经实现的模块列表
        fas module help --name captcha    # 查看模块的帮助文档
    Args:
        action str: 模块操作:
        name str: 模块名（如果后缀不是_module，则会自动加上，减少冲突可能）
        title str: 模块说明文档标题
        desc str: 模块描述
    """
    if not name.endswith('_module'):
        name += '_module'
    if action == 'list':
        module_list()
    elif action == 'help':
        all_modules = module_list(is_return=True)
        if name not in all_modules:
            raise Exception(f'该模块尚未实现: {name}')
        module_help(name)
    elif action == 'add':
        all_modules = module_list(is_return=True)
        if name not in all_modules:
            raise Exception(f'该模块尚未实现: {name}')
        module_new(name, title=title, desc=desc, src_module=name)
    elif action == 'new':
        module_new(name, title=title, desc=desc)
    else:
        raise Exception(f'不支持该操作: {action}')


def module_help(name):
    """模块帮助文档"""
    with open(join(package_path, "project", name, 'README.md'), encoding='utf8') as f:
        help_text = f.read()
    print(help_text)
    help_url = f"https://github.com/ibbd-dev/fastapi-start/tree/main/app/project/{name}"
    print(f"\n\n在线文档地址：\n    {help_url}")


def module_list(is_return=False):
    """获取支持的模块列表"""
    modules = []
    project_path = join(package_path, 'project')
    # print(project_path)
    for module in os.listdir(project_path):
        if module.endswith('_module') and os.path.isdir(join(project_path, module)):
            modules.append(module)
    if is_return:
        return modules
    print('支持的模块列表：')
    for i, module in enumerate(modules):
        print(f"  {i+1}\t{module}")


def module_new(module_name: str, title: str = '', desc: str = '', src_module: str = 'module'):
    """新建模块
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
    if not module_name.endswith('_module'):   # 加上统一的后缀避免冲突
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
