# -*- coding: utf-8 -*-
#
# 命令
# Author: alex
# Created Time: 2021年06月08日 星期二
import re
import os
from os.path import join
import shutil
from utils import init_pyfile

package_path = os.path.dirname(os.path.realpath(__file__))


def project_init(project_name: str, author: str="", 
                 title: str=None, desc: str=""):
    """项目初始化"""
    # 创建项目目录
    if re.match('^[a-z0-9\-]{4,20}$', project_name):
        print("project name check ok")
    else:
        raise Exception('project name check error')
    os.mkdir(project_name)
    if title is None:
        title = project_name
    
    # vscode
    os.mkdir(join(project_name, ".vscode"))
    shutil.copy(join(package_path, 'data', 'vscode_settings.json'), 
                join(project_name, ".vscode"))
    shutil.copy(join(package_path, 'data', 'gitignore'), 
                join(project_name, ".gitignone"))

    # 生成md文件
    with open(join(project_name, "README.md"), 'w', encoding='utf8') as f:
        f.write(f"# {title}\n{desc}")
    with open(join(project_name, "install.md"), 'w', encoding='utf8') as f:
        f.write(f"# {title}: 安装部署与运维文档")
    
    # 复制app目录
    shutil.copy(join(package_path, 'app'), project_name)
    for filename in os.listdir(join(project_name, "app")):
        if not filename.endswith('.py'):
            continue
        if not init_pyfile(join(project_name, 'app', filename), author):
            raise Exception('init python file error: '+)


def module_add(module_name: str, prefix: str=None, tags: str=None):
    """增加模块"""


def py_file_add(filename: str):
    """生成Python文件"""


def code_check():
    """代码检测"""