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
from .utils import init_pyfile, get_user_from_git, parse_git_uri

package_path = os.path.dirname(os.path.realpath(__file__))
config_file = join(package_path, 'config.json')


def config(set: bool = False, author: str = None, email: str = None, root_path: str = None):
    """配置author, email，代码根目录等信息
    Args:
        set bool: 默认该命令是get
        author str: 用户名，如果不设置则从git命令中获取（set命令时有效）
        email str: email，如果不设置则从git命令中获取（set命令时有效）
        root_path str: 代码根目录，使用clone命令的时候会在该目录下生成标准的目录路径，如：root_path/github.com/username/project/（set命令时有效）
    """
    if not set:
        return get_config()

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


def project_init(project_name: str, title: str = '', desc: str = ''):
    """项目初始化
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
    print('parse vscode settings, Dockerfile and gitignore...')
    os.mkdir(join(project_name, ".vscode"))
    shutil.copyfile(join(package_path, 'data', 'vscode_settings.json'), 
                    join(project_name, ".vscode", "settings.json"))
    shutil.copyfile(join(package_path, 'data', 'gitignore'), 
                    join(project_name, ".gitignone"))
    shutil.copyfile(join(package_path, 'data', 'Dockerfile'), 
                    join(project_name, 'Dockerfile'))
    shutil.copyfile(join(package_path, 'data', 'requirements.txt'), 
                    join(project_name, 'requirements.txt'))
    init_pyfile(join(project_name, 'Dockerfile'), cfg['author'], cfg['email'])
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
        if not init_pyfile(join(dst_path, filename), cfg['author'], cfg['email']):
            raise Exception('init python file error: ' + join(dst_path, filename))

    src_path = join(src_path, 'common')
    dst_path = join(dst_path, 'common')
    os.mkdir(dst_path)
    for filename in os.listdir(src_path):
        if not filename.endswith('.py'):
            continue
        shutil.copyfile(join(src_path, filename), join(dst_path, filename))
        if not init_pyfile(join(dst_path, filename), cfg['author'], cfg['email']):
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
        if not init_pyfile(join(module_name, filename), cfg['author'], cfg['email']):
            raise Exception('init python file error: ' + join(module_name, filename))
    print('--> ok.')
    print(f'init module: {module_name} ok.')


def py_file_add(filename: str, desc: str = ''):
    """生成Python文件
    Args:
        filename str: 文件名（若不以.py结尾，则会自动加上）
        desc str: 描述信息
    """
    name_pattern = '^[a-z0-9_\\.]{4,20}$'
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
    replaces = {'__desc__': desc.replace('\n', '\n# ')}
    init_pyfile(filename, cfg['author'], cfg['email'], replaces=replaces)
    print('--> ok.')
    print(f'init filename: {filename} ok.')


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


def code_check(path: str = '', tool: str = 'flake8'):
    """代码检测，目前支持的工具：flake8
    忽略最后缺少空行的W292
    Args:
        path str: 代码目录，默认为当前目录
        tool str: 使用的代码审查工具，默认为flake8
    """
    if tool == 'flake8':
        if path:
            os.system(f'flake8 --ignore W292 {path}')
        else:
            os.system('flake8 --ignore W292')
    else:
        raise Exception(f"不支持该工具: {tool}")
