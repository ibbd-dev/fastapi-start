# -*- coding: utf-8 -*-
#
# 工具函数库
# Author: alex
# Created Time: 2021年06月09日 星期三
import fire
from .settings import VERSION
from .cmd import config, get_config, project_init, module_add, py_file_add, code_check


def version():
    """版本号"""
    print(f'Version: {VERSION}')


def config_get():
    """获取配置信息"""
    cfg = get_config()
    print(cfg)


def main():
    """主入口"""
    fire.Fire({
        'version': version,
        'config': config,
        'config-get': config_get,
        'project-init': project_init,
        'module-add': module_add,
        'file-add': py_file_add,
        'code-check': code_check,
    })


if __name__ == '__main__':
    main()