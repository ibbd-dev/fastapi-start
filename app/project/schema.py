# -*- coding: utf-8 -*-
#
# 通用schema
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from pydantic import BaseModel, Field


class MessageResp(BaseModel):
    message: str = Field(..., title='提示信息', description='提示信息')


class VersionResp(BaseModel):
    version: str = Field(..., title='版本信息', description='版本信息')