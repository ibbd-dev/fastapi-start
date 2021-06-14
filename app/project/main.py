# -*- coding: utf-8 -*-
#
# 全局入口文件
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from fastapi import FastAPI
# from fastapi import Depends
# from fastapi.middleware.cors import CORSMiddleware

from settings import DEBUG
from utils import parse_readme
from schema import VersionResp

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
# from test_module.router import router as test_router
# app.include_router(test_router, prefix="/test", tags=["测试模块"])

# 加载验证码模块
# from captcha_module.api import config as captcha_config
# from captcha_module.router import router as captcha_router
# captcha_config('192.168.1.242')   # 配置redis host
# app.include_router(captcha_router, prefix="/captcha", tags=["验证码模块"])


@app.get("/version", summary='获取系统版本号',
         response_model=VersionResp)
async def version_api():
    """获取系统版本号"""
    return {"version": version}
