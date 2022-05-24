# -*- coding: utf-8 -*-
#
# 全局配置
# Author: __author__
# Email: __email__
# Created Time: __created_time__

# 全局测试状态
DEBUG = False

# 系统异常状态码的基数
# 返回给前端的code会加上该值
SYSTEM_CODE_BASE = 10000

# 数据库连接
# 在database.py文件中使用
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/test"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
