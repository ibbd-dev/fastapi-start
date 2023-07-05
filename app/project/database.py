# -*- coding: utf-8 -*-
#
# 数据库基础文件
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import SQLALCHEMY_DATABASE_URL

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/test"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# check_same_thread: 这个是sqlite的参数
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
