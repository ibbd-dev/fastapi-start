# -*- coding: utf-8 -*-
#
# 工具函数库
# Author: alex
# Created Time: 2021年06月08日 星期二
import re
import os
from datetime import datetime
from typing import Dict, Tuple


def init_pyfile(path: str, author: str, email: str, replaces: Dict[str, str] = None) -> bool:
    """初始化单个py文件
    生成作者和日期
    """
    with open(path, encoding='utf8') as f:
        text = f.read()
    today = datetime.now().strftime("%Y-%m-%d")
    text = text.replace('__author__', author)
    text = text.replace('__email__', email)
    text = text.replace('__created_time__', today)
    if replaces is not None:
        for key, val in replaces.items():
            text = text.replace(key, val)

    with open(path, 'w', encoding='utf8', newline='') as f:
        f.write(text)
    return True


def shell(cmd: str, ) -> str:
    """执行命令"""
    return os.popen(cmd).read().strip()


def get_user_from_git() -> Tuple[str, str]:
    """从git中获取用户名和邮箱"""
    username = shell('git config user.name')
    email = shell('git config user.email')
    return username, email


def parse_git_uri(uri) -> Dict[str, str]:
    """解释git的路径
    Args:
        uri str: 格式如git@github.com:group/project.git or https://github.com/group/project
    Returns:
        dict|None {host: "", group: "", project: ""}
    """
    def _parse(host: str, group: str, project: str):
        if ' ' in host or ' ' in group or ' ' in project:
            return None
        if project.endswith('.git'):
            project = project[:-4]
        return {'host': host, 'group': group, 'project': project}

    if uri[:4] == 'git@':
        pattern = "^git@([^\/]+)\:([^\/]+)\/([^\/]+)$"
        matches = re.match(pattern, uri)
        if matches:
            return _parse(*matches.groups())
        return None
    pattern = "^http[s]?\:\/\/([^\/]+)/([^\/]+)/([^\/]+)$"
    matches = re.match(pattern, uri)
    if matches:
        return _parse(*matches.groups())
    return None


if __name__ == '__main__':
    uri = 'git@git.ibbd.net:gf/iot-warning.git'
    data = parse_git_uri(uri)
    assert data['host'] == 'git.ibbd.net'
    assert data['group'] == 'gf'
    assert data['project'] == 'iot-warning'
    uri = 'http://git.ibbd.net/gf/iot-warning.git'
    data = parse_git_uri(uri)
    assert data['host'] == 'git.ibbd.net'
    assert data['group'] == 'gf'
    assert data['project'] == 'iot-warning'