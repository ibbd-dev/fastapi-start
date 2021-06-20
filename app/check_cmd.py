# -*- coding: utf-8 -*-
#
# 代码风格检查及静态类型检查等
# Author: caiyingyao
# Email: cyy0523xc@gmail.com
# Created Time: 2021-06-20
import os
from .utils import shell
from .utils import flake8_stat


class CodeCheck:
    """代码审查"""

    def mypy(self, path):
        """mypy代码静态类型检查

        Example:
            fas check mypy /path/to/filename.py
        http://mypy-lang.org/
        """
        os.system(f'mypy {path}')

    def flake8(self, path='', ignore: str = '', select: str = '',
               autopep8: bool = False, max_line_length: int = 110):
        """PEP8代码风格审查

        主要使用flake8工具，可以配置忽略哪些问题，或者只审查某些问题。
        对于更加复杂的审查方式，可以直接使用flake8工具进行。
        开启autopep8时，会自动进行fix，使用该操作要小心，相当于执行以下命令:
            autopep8 --select=W293 --in-place path/to/filename.py
        说明：
        1. 问题类型是支持前缀形式的，例如W2则表示所有以W2开头的类型
        2. flake8文档：https://www.osgeo.cn/flake8/
        Examples:
            忽略某些类型：
                fas check flake8 --path=app --ignore E501,W292
            自动fix：
                fas check flake8 --path=src --select W293 --autopep8
        Args:
            path str: 代码目录，默认为当前目录
            ignore str: 可以忽略指定类型, 多种类型则用英文逗号隔开。
            select str: 只检测某些类型，默认不开启该选项。
            autopep8 bool: 是否启用自动修复，默认不启用。只有在select模式下该参数才有效。
            max_line_length int: 每行长度限制，默认值为110
        """
        cmd = ''
        _autopep8 = False
        if select:
            _autopep8 = autopep8
            if type(select) in (tuple, list):
                select = ','.join(select)
            select = f'--select {select}'
            cmd = f'flake8 --max-line-length={max_line_length} {select} {path}'
        elif ignore:
            if type(ignore) in (tuple, list):
                ignore = ','.join(ignore)
            ignore = f'--ignore {ignore}'
            cmd = f'flake8 --max-line-length={max_line_length} {ignore} {path}'
        else:
            cmd = f'flake8 --max-line-length={max_line_length} {path}'

        print(cmd)
        res = shell(cmd).strip()
        if not res:
            return
        if _autopep8:
            # 启用自动修复
            files = set()
            for line in res.strip().split('\n'):
                line = line.strip()
                if line:
                    files.add(line.split(':')[0])
            for path in files:
                auto_cmd = f'autopep8 {select} --in-place {path}'
                print(auto_cmd)
                os.system(auto_cmd)
            return

        print(res)
        print('\n不规范类型统计：')
        data = flake8_stat(res.strip().split('\n'))
        for key, cnt, msg in data:
            print(f"  {key} {cnt}\t{msg}")
        print('汇总：%d' % sum([val[1] for val in data]))
