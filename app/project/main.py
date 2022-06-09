# -*- coding: utf-8 -*-
#
# 全局入口文件
# Author: __author__
# Email: __email__
# Created Time: __created_time__
# from fastapi import Depends
# from fastapi.middleware.cors import CORSMiddleware
from settings import DEBUG
from utils import parse_readme
from schema import VersionResp
from exceptions import status, InternalException
from init_app import init_app

# 初始化app
version = "0.5.0"     # 系统版本号
title, description = parse_readme()
app = init_app(version=version, title=title, description=description, debug=DEBUG)

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

# redis连接
# from common.connections import init_redis
# init_redis('192.168.1.242')   # 配置redis host

# 加载模块路由
# from test_module.router import router as test_router
# app.include_router(test_router, prefix="/test", tags=["测试模块"])

# 加载验证码模块
# from captcha_module.router import router as captcha_router
# app.include_router(captcha_router, prefix="/captcha", tags=["验证码模块"])


@app.get("/test/{test_id}", summary='测试接口',
         response_model=VersionResp)
async def test_api(test_id: int):
    """该接口只是用于测试，可以删除"""
    if test_id == 0:
        # 模拟触发某个内部逻辑错误
        raise InternalException(code=status.HTTP_600_ID_NOT_EXISTED,
                                message="id为0")
    return {"aaa": test_id}
