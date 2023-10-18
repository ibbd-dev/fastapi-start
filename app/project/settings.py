# -*- coding: utf-8 -*-
#
# 全局配置，不能定义settings_base中没有的变量
# Author: __author__
# Email: __email__
# Created Time: __created_time__

# 通常配置变量中，和基础配置文件中的值不一致时，才需要移到这里进行重新定义
# 在这里重新定义的变量，会覆盖基础配置文件中的值
from settings_base import *

# 缓存基础配置文件中的变量名
__local_keys__ = set(locals().keys())

# 全局测试状态
DEBUG = False

# 数据库连接
# 在database.py文件中使用
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/test"

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# 校验是否配置异常，避免配置过程中不慎搞错了变量名
__new_locals__ = set(locals().keys())
__new_locals__.remove('__local_keys__')
if len(__new_locals__) != len(__local_keys__):
    __keys = __new_locals__.difference(__local_keys__)
    raise Exception(f'{", ".join(__keys)}: 这些配置变量不在基础配置文件 settings_base.py 中')
