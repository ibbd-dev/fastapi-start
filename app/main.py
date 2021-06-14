# -*- coding: utf-8 -*-
#
# 工具函数库
# Author: alex
# Created Time: 2021年06月09日 星期三
import fire
# from typing import Dict
from .settings import VERSION
from .cmd import project_init, code_check
from .cmd import clone
from .config_cmd import config
from .file_cmd import file_create
from .module_cmd import module_action


def version() -> str:
    """版本号"""
    return f'Version: {VERSION}'


def main():
    """主入口"""
    fire.Fire({
        'version': version,
        'clone': clone,            # 替代git clone命令
        'config': config,

        'project-init': project_init,
        'module': module_action,
        'file': file_create,
        'check': code_check,
    })


if __name__ == '__main__':
    main()