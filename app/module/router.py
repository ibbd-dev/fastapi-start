# -*- coding: utf-8 -*-
#
# 模块路由文件
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from typing import Dict
from fastapi import APIRouter
# from fastapi import Depends, HTTPException

router = APIRouter(
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.get("/")
async def test_api() -> Dict[str, str]:
    """模块测试API"""
    return {'message': 'ok'}