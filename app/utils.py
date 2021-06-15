# -*- coding: utf-8 -*-
#
# 工具函数库
# Author: alex
# Created Time: 2021年06月08日 星期二
import re
import os
from datetime import datetime
from typing import Dict, Tuple, List


def init_file(path: str, author: str, email: str, replaces: Dict[str, str] = {}) -> bool:
    """初始化单个文件（主要时模板变量替换）
    生成作者和日期
    Args:
        replaces 格式{'title': title}
    """
    with open(path, encoding='utf8') as f:
        text = f.read()
    replaces['author'] = author
    replaces['email'] = email
    replaces['created_time'] = datetime.now().strftime("%Y-%m-%d")
    for key, val in replaces.items():
        text = text.replace(f'__{key}__', val)

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

    p = '([^\\/]+)'
    if uri[:4] == 'git@':
        # pattern = "^git@([^\/]+)\:([^\/]+)\/([^\/]+)$"
        pattern = f"^git@{p}:{p}\\/{p}$"
        matches = re.match(pattern, uri)
        if matches:
            return _parse(*matches.groups())
        return None
    # pattern = "^http[s]?\:\/\/([^\/]+)/([^\/]+)/([^\/]+)$"
    pattern = f"^http[s]?://{p}/{p}/{p}$"
    print(pattern)
    matches = re.match(pattern, uri)
    if matches:
        return _parse(*matches.groups())
    return None


def flake8_stat(texts: List[str]) -> List[Tuple[str, int, str]]:
    """flake8审查结果统计
    Args:
        texts 格式如：
            app/utils.py:46:80: E501 line too long (88 > 79 characters)
            app/utils.py:58:28: W605 invalid escape sequence
    Returns:
        List[List[str, int, str]] 如：['W605', 3, "invalid escape sequence"]，第二个值为统计值
    """
    data = {}
    pattern = '^.+?: ([A-X]\\d+) ([^\\(]+)'
    for text in texts:
        matches = re.match(pattern, text.strip())
        if matches:
            _type, _msg = matches.groups()
            if _type not in data:
                data[_type] = {'cnt': 0, 'msg': _msg.strip()}
            data[_type]['cnt'] += 1

    data = [(key, val['cnt'], val['msg']) for key, val in data.items()]
    data = sorted(data, key=lambda x: x[1], reverse=True)
    return data


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

    # flake8结果统计
    text = [
        "app/cmd.py:101:78: W291 trailing whitespace",
        "app/cmd.py:104:1: W293 blank line contains whitespace",
        "app/cmd.py:110:80: E501 line too long (82 > 79 characters)",
        "app/utils.py:46:80: E501 line too long (88 > 79 characters)",
        "app/utils.py:58:28: W605 invalid escape sequence '\\/'",
    ]
    data = flake8_stat(text)
    print(data)
    assert data[0][:2] == ('E501', 2)
