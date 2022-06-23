# -*- coding: utf-8 -*-
#
#
# Author: caiyingyao
# Email: cyy0523xc@gmail.com
# Created Time: 2022-06-09
from typing import List
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

from schema import VersionResp, StatusCodeResp
from exceptions import get_status
from exceptions import init_exception


def init_app(version='1.0', title='接口文档', description='描述文档', debug=False) -> FastAPI:
    """初始化app"""
    # *****************************************************
    # 解决接口文档的静态文件问题
    # *****************************************************
    app = FastAPI(
        debug=debug,
        title=title,
        description=description,
        version=version,
        docs_url=None,      # 关闭原有的文档地址
        responses={'default': {"description": "异常相应值见文档说明"}},
    )
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

    # 初始化异常处理
    init_exception(app)

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

    return app
