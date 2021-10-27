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


class Module:
    """模块操作（应该在项目的app目录下执行）

    模块类型有两种：
    1. 一种是内置模块：已经开发好的模块，可以使用add命令添加
    2. 另一种是全新模块，使用new命令生成，会自动生成模块的基本目录结构及其文件模板
    Examples:
        fas module list     # 已经实现的模块列表
        fas module help captcha    # 查看模块的帮助文档
    """

    def list(self):
        """获取已有可以直接使用的模块列表
        """
        module_list()

    def help(self, name: str):
        """查看内置模块的帮助文档
        Args:
            name str: 模块名（如果后缀不是_module，则会自动加上，减少冲突可能）
        """
        if not name.endswith('_module'):
            name += '_module'
        all_modules = module_list(is_return=True)
        if name not in all_modules:
            raise Exception(f'该模块尚未实现: {name}')
        module_help(name)

    def add(self, name: str, title: str = '', desc: str = ''):
        """添加一个内置模块

        可以先使用list命令查看有哪些内置模块
        Args:
            name str: 模块名（如果后缀不是_module，则会自动加上，减少冲突可能）
            title str: 模块说明文档标题
            desc str: 模块描述
        """
        if not name.endswith('_module'):
            name += '_module'
        all_modules = module_list(is_return=True)
        if name not in all_modules:
            raise Exception(f'该模块尚未实现: {name}')
        module_new(name, title=title, desc=desc, src_module=name)

    def new(self, name: str, title: str = '', desc: str = ''):
        """新建一个全新的模块
        Args:
            name str: 模块名（如果后缀不是_module，则会自动加上，减少冲突可能）
            title str: 模块说明文档标题
            desc str: 模块描述
        """
        if not name.endswith('_module'):
            name += '_module'
        module_new(name, title=title, desc=desc)


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
    if module_name.endswith('_module'):
        module_name = module_name[:-len('_module')]
    print(f'init module: {module_name} ok.')
    print('\n在入口文件(main.py)中加入引用代码：')
    print(f'from {module_name}_module.router import router as {module_name}_router')
    print(f'app.include_router({module_name}_router, prefix="/{module_name}", tags=["{title}"])')
