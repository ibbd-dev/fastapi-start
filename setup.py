  
# -*- coding: utf-8 -*-
#
# 安装程序
# Author: alex
# Created Time: 2018年04月02日 星期一 17时29分45秒
import os
from distutils.core import setup

def read(rel_path):
    # type: (str) -> str
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path), encoding='utf8') as fp:
        return fp.read()


def get_version(rel_path):
    # type: (str) -> str
    for line in read(rel_path).splitlines():
        if line.startswith("VERSION"):
            # VERSION = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


LONG_DESCRIPTION = """
使用：

- 完整命令：fastapi-start
- 缩写命令：fas

包含功能：

- [x] 项目初始化
- [x] 添加模块
- [x] 生成Python文件
- [x] git路径规范
- [x] 编码风格审查
""".strip()

SHORT_DESCRIPTION = """FastAPI脚手架""".strip()

DEPENDENCIES = [
    'fire',
]

VERSION = get_version('app/settings.py')
URL = 'https://github.com/ibbd-dev/python-fastapi-start'
setup(
    name='fastapi_start',
    version=VERSION,
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,

    author='Alex Cai',
    author_email='cyy0523xc@gmail.com',
    license='Apache Software License',

    keywords='fastapi',
    packages=['fastapi_start'],
    package_dir={'fastapi_start': 'app'},
    package_data={'fastapi_start': [
                                    os.path.join('data', '*'),
                                    os.path.join('project', '*'),
                                    os.path.join('project', 'common', '*'),
                                    os.path.join('project', 'module', '*'),
                                    os.path.join('project', 'captcha_module', '*'),
                                    ]},
    entry_points={      # 安装命令
        "console_scripts": [
            "fastapi-start=fastapi_start.main:main",
            # 命令别名
            "fas=fastapi_start.main:main",
        ],
    },
    python_requires=">=3.6",
)