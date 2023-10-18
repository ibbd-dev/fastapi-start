# -*- coding: utf-8 -*-
#
# 统一日志
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from uuid import uuid4
from pathlib import Path
from loguru import logger
from contextvars import ContextVar

from settings import LOG_ROOT_PATH

# 业务使用的ID，如任务ID/批量任务ID/大文件id等
# celery任务也可以通过业务ID进行关联
_trace_id: ContextVar[str] = ContextVar('x_trace_id', default="")           # 业务追踪ID
# 使用任务request_id来实现全链路日志追踪，通常Rest接口才有这个
_x_request_id: ContextVar[str] = ContextVar('x_request_id', default="")     # 请求ID


class TraceID:
    """全链路追踪ID
    可以在日志文件中，根据ID过滤相应的日志，方便定位问题所在
    用于追踪的ID分成两类：
    1. 请求ID：以一次请求会话为生命周期，新的请求会产生新的ID；
    2. 追踪ID：通常是具体的业务ID，通常一个业务操作可能不止一个请求，而是有多个请求，这时通过业务ID就能将这些日志都过滤出来
    """
    @staticmethod
    def set(req_id: str) -> ContextVar[str]:
        """设置请求ID，外部需要的时候，可以调用该方法设置
        Returns:
            ContextVar[str]: _description_
        """
        if not req_id:
            req_id = uuid4().hex
        _x_request_id.set(req_id)
        return _x_request_id

    @staticmethod
    def set_trace(id: str, title: str = "trace") -> ContextVar[str]:
        """设置追踪ID
        Returns:
            ContextVar[str]: _description_
        """
        if id:
            id = f"{title}:{id}"
            _trace_id.set(id)
            return _trace_id
        _trace_id.set(id)
        return _trace_id

    @staticmethod
    def init(trace: dict):
        """该方法通常和get搭配使用，如进入子进程前调用get方法获取trace字典，进入子进程之后，再调用该初始化方法
        Args:
            trace (dict): _description_
        Returns:
            _type_: _description_
        """
        trace_id_msg = f"{trace['trace_title']}:{trace['trace_id']}"
        _trace_id.set(trace_id_msg)
        _x_request_id.set(trace['req_id'])

    @staticmethod
    def get() -> dict:
        """获取trace id
        Returns:
            dict: _description_
        """
        trace_msg = _trace_id.get()
        trace_title, trace_id = '', ''
        if trace_msg:
            trace_title, trace_id = trace_msg.split(':')
        return {
            'req_id': _x_request_id.get(),
            'trace_id': trace_id,
            'trace_title': trace_title,
        }

    @staticmethod
    def get_trace_id() -> str:
        trace_msg = _trace_id.get()
        trace_id = ''
        if trace_msg:
            trace_id = trace_msg.split(':')[-1]
        return trace_id

    @staticmethod
    def get_req_id() -> str:
        return _x_request_id.get(),


def _logger_filter(record):
    record['trace_msg'] = f"{_x_request_id.get()} | {_trace_id.get()}"
    return record['trace_msg']


log_path_root = Path(LOG_ROOT_PATH)
if not log_path_root.is_dir():
    log_path_root.mkdir()

# 每次重启会生成新的日志
log_path_info = log_path_root.joinpath('info-{time:YYYYMMDD}.log')
log_path_warning = log_path_root.joinpath(f'warning.log')
log_path_error = log_path_root.joinpath(f'error.log')
"""
https://cloud.tencent.com/developer/article/1849382
backtrace (bool, optional) : 格式化的异常跟踪是否应该向上扩展，超出捕获点，以显示生成错误的完整堆栈跟踪。
diagnose  (bool, optional) : 异常跟踪是否应该显示变量值以简化调试。在生产中，这应该设置为“False”，以避免泄漏敏感数据。
"""
params = {
    "rotation": "50 MB", "encoding": 'utf-8', "enqueue": True, "backtrace": True,  # "compression": "gzip",
    "filter": _logger_filter,
    "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {trace_msg} | {name}:{function}:{line} - {message}",
}
params_info = {
    "rotation": "daily", "encoding": 'utf-8', "enqueue": True, "backtrace": True,  # "compression": "gzip",
    "filter": _logger_filter,
    "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {trace_msg} | {name}:{function}:{line} - {message}",
}
logger.remove()
logger.add(log_path_info, level='INFO', retention='90 days', **params_info)
logger.add(log_path_warning, level='WARNING', **params)
logger.add(log_path_error, level='ERROR', **params)
