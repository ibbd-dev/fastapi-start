# -*- coding: utf-8 -*-
#
# 异常信息
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from fastapi import status
from fastapi.responses import JSONResponse
from settings import SYSTEM_CODE_BASE

# 状态码基数应该符合这两个条件
assert SYSTEM_CODE_BASE >= 1000
assert SYSTEM_CODE_BASE % 1000 == 0


class ErrorResponse(JSONResponse):
    """接口异常响应类型"""
    def __init__(self, code: int, message: str) -> None:
        """
        :param code 响应状态码，取值0-999，若该值大于等于600，则http code会自动重置为500
        :param message 异常信息
        """
        assert 0 <= code < 1000
        # http的状态码大于600会报错，超过600响应为内部错误
        status_code = code if code < 600 else status.HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__(status_code=status_code,
                         content={"code": SYSTEM_CODE_BASE + code, 'message': message})
