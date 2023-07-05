# -*- coding: utf-8 -*-
#
# __desc__
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy import Boolean, CHAR

from ..project.database import Base


class __model_name__(Base):
    __tablename__ = "__table_name__"

    # 常见字段，如果不需要可以自行去掉
    id = Column(Integer, primary_key=True, nullable=False,  index=True, comment="主键ID")
    created_at = Column(DateTime, index=True, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, index=True, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    remark = Column(String(100), nullable=True, default='', comment="备注信息")
