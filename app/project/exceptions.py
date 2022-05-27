# -*- coding: utf-8 -*-
#
# 异常处理相关常量及工具函数等
# 1. 每一个抛出的异常都应该有对应的状态值及默认的异常信息
# 2. 每一个抛出的异常都应该继承自BaseException，这个异常会在接口层进行捕获
# 3. 异常的响应时统一的使用ErrorResponse
#
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from fastapi import status as fastapiStatus, HTTPException
from fastapi.responses import JSONResponse
from typing import Any
from settings import SYSTEM_CODE_BASE

# 状态码基数应该符合这两个条件
assert SYSTEM_CODE_BASE >= 1000
assert SYSTEM_CODE_BASE % 1000 == 0


class status:
    """自定义异常状态码常量，尽量重用http状态码
    """
    # 4XX: 来自客户端错误的响应
    HTTP_400_BAD_REQUEST = fastapiStatus.HTTP_400_BAD_REQUEST
    HTTP_401_UNAUTHORIZED = fastapiStatus.HTTP_401_UNAUTHORIZED
    HTTP_403_FORBIDDEN = fastapiStatus.HTTP_403_FORBIDDEN
    HTTP_404_NOT_FOUND = fastapiStatus.HTTP_404_NOT_FOUND
    HTTP_422_UNPROCESSABLE_ENTITY = fastapiStatus.HTTP_422_UNPROCESSABLE_ENTITY
    # 5XX：来自服务器端错误的响应
    HTTP_500_INTERNAL_SERVER_ERROR = fastapiStatus.HTTP_500_INTERNAL_SERVER_ERROR
    HTTP_504_GATEWAY_TIMEOUT = fastapiStatus.HTTP_504_GATEWAY_TIMEOUT
    # 自定义常量值应该取值在600-999
    HTTP_600_ID_NOT_EXISTED = 600    # 示例

# 状态码对应的异常信息(默认)
messages = {
    # 4XX
    status.HTTP_400_BAD_REQUEST: '请求参数校验不通过',
    status.HTTP_401_UNAUTHORIZED: '权限校验不通过',
    status.HTTP_403_FORBIDDEN: '响应参数校验不通过',
    status.HTTP_404_NOT_FOUND: '请求的资源不存在',
    # 5XX
    status.HTTP_500_INTERNAL_SERVER_ERROR: '服务器内部错误',
    status.HTTP_504_GATEWAY_TIMEOUT: '请求上游服务时超时',
    # 600-999
    status.HTTP_600_ID_NOT_EXISTED: '请求ID不存在',
}


def get_status():
    """获取接口状态值列表"""
    data = [{'code': status.__dict__[key],
             'message': messages[status.__dict__[key]]}
            for key in status.__dict__ if key.startswith('HTTP_')]
    data = sorted(data, key=lambda x: x['code'])
    print(data, flush=True)
    # TODO 在这里可以获取上游服务的状态值
    return data


class BaseException(HTTPException):
    """自定义异常基类
    程序内部抛出的异常应该给予该基类
    """
    def __init__(self, code: int, message: str, detail: Any = None) -> None:
        self.code = code
        self.message = message
        status_code = code if code < 600 else fastapiStatus.HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__(status_code, detail)

    def __str__(self) -> str:
        return f"code={self.code} message={self.message}\n detail={self.detail}"


class InternalException(BaseException):
    """内部错误异常"""
    pass


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
    def __init__(self, code: int, message: str = None, detail: Any = None) -> None:
        """
        :param code 响应状态码，取值0-999，若该值大于等于600，则http code会自动重置为500
        :param message 异常信息，如果该值为空，则会默认为code值对应的异常信息
        :param detail 详细的异常信息，通常用于开发者排除定位问题使用
        """
        assert 0 <= code < 1000
        # http的状态码大于600会报错，超过600响应为内部错误
        status_code = code if code < 600 else status.HTTP_500_INTERNAL_SERVER_ERROR
        if message is None:
            message = messages[code]
        super().__init__(status_code=status_code,
                         content={"code": SYSTEM_CODE_BASE + code,
                                  'message': message, 'detail': detail})


if __name__ == "__main__":
    resp = ErrorResponse(status.HTTP_403_FORBIDDEN, message='接口请求参数错误')
    print(resp.body)
    resp = ErrorResponse(status.HTTP_600_ID_NOT_EXISTED)
    print(resp.body)
