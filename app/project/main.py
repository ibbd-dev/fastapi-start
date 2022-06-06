# -*- coding: utf-8 -*-
#
# 全局入口文件
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from traceback import format_exc
# from fastapi import Depends
# from fastapi.middleware.cors import CORSMiddleware

from settings import DEBUG
from utils import parse_readme
from schema import VersionResp, StatusCodeResp
from exceptions import get_status, status, ErrorResponse, InternalException, BaseException

version = "0.5.0"     # 系统版本号
title, description = parse_readme()
app = FastAPI(
    debug=DEBUG,
    title=title,
    description=description,
    version=version,
    docs_url=None,      # 关闭原有的文档地址
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

# *****************************************************
# 解决接口文档的静态文件问题
# *****************************************************
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - 接口文档",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

# *****************************************************


# redis连接
# from common.connections import init_redis
# init_redis('192.168.1.242')   # 配置redis host

# 加载模块路由
# from test_module.router import router as test_router
# app.include_router(test_router, prefix="/test", tags=["测试模块"])

# 加载验证码模块
# from captcha_module.router import router as captcha_router
# app.include_router(captcha_router, prefix="/captcha", tags=["验证码模块"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: Exception):
    """请求参数异常"""
    return ErrorResponse(status.HTTP_400_BAD_REQUEST, message='请求参数校验不通过', detail=str(exc))


@app.exception_handler(ValidationError)
async def resp_validation_exception_handler(request, exc: Exception):
    """响应值参数校验异常"""
    return ErrorResponse(status.HTTP_403_FORBIDDEN, message='响应参数校验不通过', detail=str(exc))


@app.exception_handler(BaseException)
async def base_exception_handler(request, exc: BaseException):
    """捕获自定义异常"""
    # 把异常的详细信息打印到控制台，也可以在此实现将日志写入到对应的文件系统等
    print(format_exc(), flush=True)
    return ErrorResponse(exc.code, message=exc.message, detail=exc.detail)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """捕获FastAPI异常"""
    print(format_exc(), flush=True)
    return ErrorResponse(exc.status_code, message=str(exc.detail), detail=exc.detail)


@app.exception_handler(Exception)
async def allexception_handler(request, exc: Exception):
    """捕获所有其他的异常"""
    print(format_exc(), flush=True)
    return ErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR,
                         message='内部异常', detail=str(exc))


@app.get("/version", summary='获取系统版本号',
         response_model=VersionResp)
async def version_api():
    """获取系统版本号"""
    return {"version": version}


@app.get("/status/code", summary='获取接口的异常状态码及说明',
         response_model=List[StatusCodeResp])
async def status_code_api():
    """获取系统的异常状态值及相应的说明\n
    该接口通常用于开发阶段，用于查询各个状态值及其意义
    """
    return get_status()


@app.get("/test/{test_id}", summary='测试接口',
         response_model=VersionResp)
async def test_api(test_id: int):
    """该接口只是用于测试，可以删除"""
    if test_id == 0:
        # 模拟触发某个内部逻辑错误
        raise InternalException(code=status.HTTP_600_ID_NOT_EXISTED,
                                message="id为0")
    return {"aaa": version}
