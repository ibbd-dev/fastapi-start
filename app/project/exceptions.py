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
from fastapi import FastAPI
from fastapi import status as fastapiStatus, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from traceback import format_exc
from typing import Any
from settings import SYSTEM_CODE_BASE

# 状态码基数应该符合这两个条件
assert SYSTEM_CODE_BASE >= 1000
assert SYSTEM_CODE_BASE % 1000 == 0


def init_exception(app: FastAPI):
    """初始化异常处理"""
    def get_detail(msg: str) -> str:
        return '\n'.join(msg.strip().split('\n')[-3:])

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
        """捕获所有其他的异常
        """
        msg = format_exc()
        print(msg, flush=True)
        return ErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            message='内部异常', detail=get_detail(msg))

    @app.exception_handler(KeyError)
    async def keyerror_handler(request, exc: KeyError):
        """捕获所有其他的异常"""
        msg = format_exc()
        print(msg, flush=True)
        return ErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            message='内部异常', detail=get_detail(msg))

    @app.exception_handler(ValueError)
    async def valueerror_handler(request, exc: ValueError):
        """捕获所有其他的异常"""
        msg = format_exc()
        print(msg, flush=True)
        return ErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            message='内部异常', detail=get_detail(msg))


class status:
    """自定义异常状态码常量，尽量重用http状态码
    """
    # 4XX: 来自客户端错误的响应
    HTTP_400_BAD_REQUEST = fastapiStatus.HTTP_400_BAD_REQUEST
    HTTP_401_UNAUTHORIZED = fastapiStatus.HTTP_401_UNAUTHORIZED
    HTTP_403_FORBIDDEN = fastapiStatus.HTTP_403_FORBIDDEN
    HTTP_404_NOT_FOUND = fastapiStatus.HTTP_404_NOT_FOUND
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
    data = [{'code': status.__dict__[key] + SYSTEM_CODE_BASE,
             'message': messages[status.__dict__[key]]}
            for key in status.__dict__ if key.startswith('HTTP_')]
    data = sorted(data, key=lambda x: x['code'])
    # print(data, flush=True)
    # TODO 在这里可以获取上游服务的状态值
    return data


class BaseException(HTTPException):
    """自定义异常基类
    程序内部抛出的异常应该给予该基类
    异常都使用这个类型或者其子类进行抛出，会被统一进行处理和响应。
    对于嵌套的异常处理，如果捕获到这个类型的，则直接raise即可，其他的异常则可以进行进一步的处理。
    """
    def __init__(self, code: int, message: str = None, detail: Any = None) -> None:
        """
        :param code 必须是在在status中定义好的值
        :param message 异常信息，通常可以展示给前端用户看
        :param detail 详细异常信息，通常是用于开发排查问题
        """
        self.code = code
        self.message = message if message else messages[code]
        status_code = code if code < 600 else fastapiStatus.HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__(status_code, detail)

    def __str__(self) -> str:
        return f"code={self.code} message={self.message}\n detail={self.detail}"


class InternalException(BaseException):
    """内部错误异常
    异常时通常使用该类型进行raise
    """
    pass


class ErrorResponse(JSONResponse):
    """接口异常响应类型
    通常只需要在中间件捕获异常的时候使用。
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
        :param code 响应状态码，正常取值0-999，若该值与1000的余数大于等于600，则http code会自动重置为500。若该值大于等于1000，则该值可能来自上游接口
        :param message 异常信息，通常是用于展示给用户。如果该值为空，则会默认为code值对应的异常信息
        :param detail 详细的异常信息，通常用于开发者排除定位问题使用
        """
        if code >= 1000:    # 指定的code值，可能来自上游服务的异常
            super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             content={"code": code, 'message': message, 'detail': detail})
            return
        # http的状态码大于600会报错，超过600响应为内部错误
        status_code = code if code < 600 else status.HTTP_500_INTERNAL_SERVER_ERROR
        message = messages[code] if message is None else message
        super().__init__(status_code=status_code,
                         content={"code": SYSTEM_CODE_BASE + code,
                                  'message': message, 'detail': detail})


if __name__ == "__main__":
    resp = ErrorResponse(status.HTTP_403_FORBIDDEN, message='接口请求参数错误')
    print(resp.body)
    resp = ErrorResponse(status.HTTP_600_ID_NOT_EXISTED)
    print(resp.body)
