# -*- coding: utf-8 -*-
#
# 异常信息
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from fastapi import status
from fastapi.responses import JSONResponse
from .settings import SYSTEM_CODE_BASE

# 状态码基数应该符合这两个条件
assert SYSTEM_CODE_BASE >= 1000
assert SYSTEM_CODE_BASE % 1000 == 0


class ErrorResponse(JSONResponse):
    """接口异常响应类型
    异常时可以指定一个状态，这个状态码应该尽量重用http标准的状态码，
    对于超过范围的值，可以定义到600到999的范围，大于等于600的时候，
    在响应时会自动重置为500.
    响应给前端的异常信息结构(假设SYSTEM_CODE_BASE的值为1000)：
    Example1:
    {
        "code": 1401,
        "message": "这是自定义错误信息"
    }
    这时http响应的状态码应该时401
    Example2:
    {
        "code": 1602,
        "message": "这是自定义错误信息"
    }
    这时http响应的状态码应该时500（大于等于600时自动重置为500）

    其中：
    code值是完整的异常状态码，message是异常描述信息。
    """
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
