# -*- coding: utf-8 -*-
#
# 模块路由文件
# Author: __author__
# Created Time: __created_time__
from fastapi import APIRouter
# from fastapi import Depends, HTTPException

router = APIRouter(
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


# 接口样例
"""
@router.get("/")
async def test_api():
    return {'message': 'ok'}
"""