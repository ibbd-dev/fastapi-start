# -*- coding: utf-8 -*-
#
# 命令
# Author: alex
# Created Time: 2021年06月08日 星期二
import re
import os
from os.path import join
import shutil
from .settings import package_path
from .utils import init_file, parse_git_uri, shell
from .utils import flake8_stat
from .config_cmd import get_config


def project_init(project_name: str, title='', desc=''):
    """项目初始化

    Examples:
        fas project-init test --title=测试项目 --desc=这是一个测试项目
    Args:
        project_name str: 项目名（目录名）
        title str: 项目标题（显示在交互式文档中）
        desc str: 项目描述（显示在交互式文档中）
    """
    # 创建项目目录
    name_pattern = '^[a-z0-9\\-]{4,20}$'
    if re.match(name_pattern, project_name):
        print("project name check ok")
    else:
        raise Exception(f'project name check error: {name_pattern}')
    if os.path.isdir(project_name):
        raise Exception(f"project name: {project_name} is existed!")
    os.mkdir(project_name)
    if len(title) == 0:
        title = project_name
    else:
        title = title.replace('\n', ' ')

    # vscode, gitignore, Dockerfile
    cfg = get_config()
    print('parse vscode settings, Dockerfile, readme and gitignore...')
    os.mkdir(join(project_name, ".vscode"))
    shutil.copyfile(join(package_path, 'data', 'vscode_settings.json'),
                    join(project_name, ".vscode", "settings.json"))
    shutil.copyfile(join(package_path, 'data', 'gitignore'),
                    join(project_name, ".gitignone"))
    shutil.copyfile(join(package_path, 'data', 'Dockerfile'),
                    join(project_name, 'Dockerfile'))
    shutil.copyfile(join(package_path, 'data', 'requirements.txt'),
                    join(project_name, 'requirements.txt'))
    init_file(join(project_name, 'Dockerfile'), cfg['author'], cfg['email'])
    shutil.copyfile(join(package_path, 'data', 'README.md'),
                    join(project_name, 'README.md'))
    replaces = {'title': title, 'desc': desc}
    init_file(join(project_name, 'README.md'), cfg['author'], cfg['email'],
              replaces=replaces)
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
        if not init_file(join(dst_path, filename), cfg['author'], cfg['email']):
            raise Exception('init python file error: ' + join(dst_path, filename))

    src_path = join(src_path, 'common')
    dst_path = join(dst_path, 'common')
    os.mkdir(dst_path)
    for filename in os.listdir(src_path):
        if not filename.endswith('.py'):
            continue
        shutil.copyfile(join(src_path, filename), join(dst_path, filename))
        if not init_file(join(dst_path, filename), cfg['author'], cfg['email']):
            raise Exception('init python file error: ' + join(dst_path, filename))
    print('--> ok.')
    print(f'init project: {project_name} ok.')


def module_add(module_name: str):
    """增加模块（应该在项目的app目录下执行）
    Args:
        module_name str: 模块名
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
        if not init_file(join(module_name, filename), cfg['author'], cfg['email']):
            raise Exception('init python file error: ' + join(module_name, filename))
    print('--> ok.')
    print(f'init module: {module_name} ok.')


def clone(uri):
    """实现git clone的功能，并创建规范的项目目录路径
    Args:
        uri str: 格式如git@github.com:group/project.git or https://github.com/group/project
    """
    data = get_config()
    if 'root_path' not in data or len(data['root_path']) == 0:
        raise Exception('代码根目录尚未配置')
    root_path = data['root_path']
    if not os.path.isdir(root_path):
        raise Exception(f'代码根目录不是有效目录：{root_path}')
    data = parse_git_uri(uri)
    project_path = join(root_path, data['host'], data['group'], data['project'])
    if os.path.isdir(project_path):
        raise Exception(f'项目路径已经存在，确认是否冲突：{project_path}')
    os.makedirs(project_path)
    os.system(f"git clone {uri} {project_path}")


def code_check(path='', ignore='W292'):
    """代码风格审查

    主要使用flake8工具，可以配置忽略哪些问题
    Args:
        path str: 代码目录，默认为当前目录
        ignore str: 可以忽略指定类型，默认为W292。多种类型则用英文逗号隔开
    """
    if ignore:
        ignore = f'--ignore {ignore}'
    res = shell(f'flake8 {ignore} {path}')
    print(res)
    print('\n不规范类型统计：')
    data = flake8_stat(res.strip().split('\n'))
    for key, cnt, msg in data:
        print(f"  {key} {cnt}\t{msg}")
