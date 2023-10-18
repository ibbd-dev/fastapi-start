# -*- coding: utf-8 -*-
#
# 工具函数库
# Author: alex
# Created Time: 2021年06月09日 星期三
import os

# 版本
# 0.6.7: add virtualenv
# 0.6.8: 优化config命令
# 0.6.10: 优化项目名字的长度限制；允许在已有目录中创建项目
# 0.6.11: 优化项目初始化及创建命令
# 0.7.0: 增加快速从已有数据库或者表中生成模型文件功能
# 0.8.0: 增加http的post和get统一封装，增加logger日志统一封装，优化配置文件
VERSION = "0.8.0"

# 包跟目录
package_path = os.path.dirname(os.path.realpath(__file__))
