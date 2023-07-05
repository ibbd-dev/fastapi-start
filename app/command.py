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
from .config_cmd import get_config

# 项目名字规范
name_pattern = '^[a-z][a-z0-9\\-]{2,99}$'


class Project:
    """项目相关操作

    Examples:
        以当前目录为根目录，初始化项目:
            fas project init --title=测试项目 --desc=这是一个测试项目
        在当前目录下创建一个test的项目，并完成初始化
            fas project create test --title=测试项目 --desc=这是一个测试项目
    """

    def init(self, name: str = '', title: str = '', desc: str = ''):
        """以当前目录为根目录，初始化项目

        Examples:
            fas project init --title=测试项目 --desc=这是一个测试项目
        Args:
            name str: 项目名（目录名），如果不传该值，则自动设置为当前目录名
               命名规范：支持小写字母、数字、连接符-等，必须以字母开头
            title str: 项目标题（显示在交互式文档中）
            desc str: 项目描述（显示在交互式文档中）
        """
        if len(name) == 0:
            name = os.path.split(os.getcwd())[-1]
        elif re.match(name_pattern, name):
            print("project name check ok")
        else:
            raise Exception(f'project name check error: "{name_pattern}"，支持小写字母、数字、连接符-等，必须以字母开头，长度限制3-100个字符')
        project_init(name, title=title, desc=desc)

    def create(self, name: str, title: str = '', desc: str = ''):
        """在当前目录下创建一个目录作为项目根目录，并完成初始化

        Examples:
            fas project create test --title=测试项目 --desc=这是一个测试项目
        Args:
            name str: 项目名（目录名），创建成功之后，会在当前目录下创建一个项目目录
            title str: 项目标题（显示在交互式文档中）
            desc str: 项目描述（显示在交互式文档中）
        """
        if re.match(name_pattern, name):
            print("project name check ok")
        else:
            raise Exception(f'project name check error: {name_pattern}')
        # 创建项目目录，并cd到该目录
        os.mkdir(name)
        os.chdir(name)
        project_init(name, title=title, desc=desc)


def project_init(project_name: str, title: str = '', desc: str = ''):
    """项目初始化
    Args:
        project_name str: 项目名（目录名）
        title str: 项目标题（显示在交互式文档中）
        desc str: 项目描述（显示在交互式文档中）
    """
    if len(title) == 0:
        title = project_name
    else:
        title = title.replace('\n', ' ')

    # vscode, gitignore, Dockerfile
    cfg = get_config()
    print('parse vscode settings, Dockerfile, readme and gitignore...')
    os.mkdir(".vscode")
    shutil.copyfile(join(package_path, 'data', 'vscode_settings.json'),
                    join(".vscode", "settings.json"))
    shutil.copyfile(join(package_path, 'data', 'gitignore'), ".gitignore")
    shutil.copyfile(join(package_path, 'data', 'Dockerfile'), 'Dockerfile')
    shutil.copyfile(join(package_path, 'data', 'requirements.txt'), 'requirements.txt')
    init_file('Dockerfile', cfg['author'], cfg['email'])
    shutil.copyfile(join(package_path, 'data', 'README.md'), 'README.md')
    replaces = {'title': title, 'desc': desc}
    init_file('README.md', cfg['author'], cfg['email'], replaces=replaces)
    print('--> ok.')

    # 创建python虚拟环境
    print('正在创建Python虚拟环境......')
    shell('virtualenv venv')
    if not os.path.isdir(join('venv')):
        raise Exception('创建Python虚拟环境不成功')
    else:
        print('Python虚拟环境安装到目录：venv。使用帮助：virtualenv --help')

    # 复制app目录
    print('copy and parse app files...')
    src_path = join(package_path, 'project')
    dst_path = 'app'
    os.mkdir(dst_path)
    for filename in os.listdir(src_path):
        if not filename.endswith(('.py', '.md')):
            continue   # 如果不是py文件或者md文件
        if filename == 'settings.py':
            dst_filename = 'settings-example.py'
        else:
            dst_filename = filename

        shutil.copyfile(join(src_path, filename), join(dst_path, dst_filename))
        if not init_file(join(dst_path, dst_filename), cfg['author'], cfg['email'], replaces=replaces):
            raise Exception('init file error: ' + join(dst_path, dst_filename))

    src_path = join(src_path, 'common')
    dst_path = join(dst_path, 'common')
    os.mkdir(dst_path)
    for filename in os.listdir(src_path):
        if not filename.endswith(('.py', '.md')):
            continue
        shutil.copyfile(join(src_path, filename), join(dst_path, filename))
        if not init_file(join(dst_path, filename), cfg['author'], cfg['email'], replaces=replaces):
            raise Exception('init file error: ' + join(dst_path, filename))

    # 处理静态文件
    src_path = join(package_path, 'project', 'static')
    dst_path = join('app', 'static')
    os.mkdir(dst_path)
    shutil.copy(join(src_path, 'swagger-ui.css'), dst_path)
    shutil.copy(join(src_path, 'swagger-ui-bundle.js'), dst_path)
    print('--> ok.')
    print(f'init project: {project_name} ok.')

    # 介绍使用方式
    print('\nUsage:')
    print('  cd app')
    print('  cp settings-example.py settings.py')
    print('  uvicorn main:app')


def clone(uri):
    """实现git clone的功能，并创建规范的项目目录路径

    执行命令：fas clone https://github.com/group/project
    项目会被保存到：{root-path}/github.com/group/project
    其中跟目录可以使用config命令进行配置。
    Args:
        uri str: 格式如git@github.com:group/project.git or https://github.com/group/project
    """
    data = get_config()
    if 'root_path' not in data or len(data['root_path']) == 0:
        raise Exception('代码根目录尚未配置，请先使用config命令进行配置')
    root_path = data['root_path']
    if not os.path.isdir(root_path):
        raise Exception(f'代码根目录不是有效目录：{root_path}')
    data = parse_git_uri(uri)
    project_path = join(root_path, data['host'], data['group'], data['project'])
    if os.path.isdir(project_path):
        raise Exception(f'项目路径已经存在，确认是否冲突：{project_path}')
    os.makedirs(project_path)
    os.system(f"git clone {uri} {project_path}")
