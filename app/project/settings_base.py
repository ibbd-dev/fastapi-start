# -*- coding: utf-8 -*-
#
# 基础配置文件，该文件应该只被settings.py引用
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from pathlib import Path

# 全局测试状态
DEBUG = False

# 版本号
VERSION = "v0.1.0"

# 系统异常状态码的基数
# 返回给前端的code会加上该值
SYSTEM_CODE_BASE = 10000

# 数据库连接
# 在database.py文件中使用
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/test"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# 配置日志目录
# 项目跟目录
ROOT_PATH = Path(__file__).absolute().parent

# 日志文件根目录
LOG_ROOT_PATH = ROOT_PATH.joinpath("logs")

# 用于追踪的请求ID字段
REQUEST_ID_KEY = "x-request-id"
