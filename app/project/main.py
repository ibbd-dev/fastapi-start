# -*- coding: utf-8 -*-
#
# 全局入口文件
# Author: __author__
# Created Time: __created_time__
from typing import Dict
from fastapi import FastAPI
# from fastapi import Depends
# from fastapi.middleware.cors import CORSMiddleware

from settings import DEBUG
from utils import parse_readme

version = "0.5.0"     # 系统版本号
title, description = parse_readme()
app = FastAPI(
    debug=DEBUG,
    title=title,
    description=description,
    version=version,
    # dependencies=[Depends(get_query_token),
)

# 跨域问题
"""
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""

# 加载模块路由
# app.include_router()


@app.get("/version", summary='获取系统版本号')
async def version_api() -> Dict[str, str]:
    return {"version": version}