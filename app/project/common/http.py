# -*- coding: utf-8 -*-
#
# 网络请求接口封装
# Author: __author__
# Email: __email__
# Created Time: __created_time__
import requests
from traceback import format_exc

from settings import REQUEST_ID_KEY
from exceptions import InternalException, status
from common.logger import logger, TraceID


def post(*args, retry: int = 2, **kwargs) -> requests.Response:
    """基于requests.post实现
    Args:
        retry (int, optional): 超时导致的失败重试的次数. Defaults to 2.
    Returns:
        requests.Response: _description_
    """
    return _do_req(requests.post, *args, retry=retry, **kwargs)


def get(*args, retry: int = 2, **kwargs) -> requests.Response:
    """基于requests.get实现
    Args:
        retry (int, optional): 超时导致的失败重试的次数. Defaults to 2.
    Returns:
        requests.Response: _description_
    """
    return _do_req(requests.get, *args, retry=retry, **kwargs)


def _do_req(method, *args, retry: int = 2, **kwargs):
    # 设置用于全链路追踪的ID
    if "headers" in kwargs:    # 存在头信息
        if REQUEST_ID_KEY not in kwargs["headers"]:
            kwargs['headers'][REQUEST_ID_KEY] = TraceID.get_trace_id()
    else:
        kwargs['headers'] = {
            REQUEST_ID_KEY: TraceID.get_trace_id(),
        }

    while retry >= 0:
        retry -= 1
        try:
            resp: requests.Response = method(*args, **kwargs)
            break
        except requests.exceptions.Timeout as e:    # 超时异常需要进行重试
            if retry < 0:
                logger.error(f"{method.__name__}超时异常 : {args} : retry = {retry} : {e}")
                raise InternalException(status.HTTP_504_GATEWAY_TIMEOUT, message=f"{method.__name__}上游服务请求超时: {args}", detail=e)
            logger.warning(f"{method.__name__}超时异常 : {args} : retry = {retry} : {e}")
            continue
        except Exception as e:
            msg = str(e)
            logger.error(f"{method.__name__}请求异常 : {args} : retry = {retry} : {msg}\n{format_exc()}")
            oom_err = _check_oom(msg, method.__name__, *args)
            if oom_err:   # 超内存或显存异常
                raise oom_err
            # 其他的异常
            raise InternalException(status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"{method.__name__}上游服务请求异常: {args}", detail=msg)

    if resp.status_code != 200:
        oom_err = _check_oom(resp.text, method.__name__, *args)
        if oom_err:   # 超内存或显存异常
            logger.error(f"{oom_err}: {resp.text}")
            raise oom_err
        # 其他的异常
    return resp


def _check_oom(msg: str, *args):
    """判断是否为OOM异常
    超显存或内存的异常信息，重试可能会成功，但是如果任务比较耗时的话，则可能会导致其他任务阻塞
    # 版本1
    ResourceExhaustedError:
    OutofmemoryerroronGPU0.Cannotallocate1.819336GBmemoryonGPU0,9.243896GBmemoryhasbeenallocatedandavailablememoryisonly1.517273GB.
    PleasecheckwhetherthereisanyotherprocessusingGPU0.
    1.Ifyes,pleasestopthem,orstartPaddlePaddleonanotherGPU.
    2.Ifno,pleasedecreasethebatchsizeofyourmodel. ...
    # 版本2
    Traceback(mostrecentcalllast):
    ...ResourceExhaustedError:
    OutofmemoryerroronGPU0.Cannotallocate2.181519GBmemoryonGPU0,8.634033GBmemoryhasbeenallocatedandavailablememoryisonly2.124084GB.
    PleasecheckwhetherthereisanyotherprocessusingGPU0.
    1.Ifyes,pleasestopthem,orstartPaddlePaddleonanotherGPU.
    2.Ifno,pleasedecreasethebatchsizeofyourmodel.
    Iftheabovewaysdonotsolvetheoutofmemoryproblem,youcantrytouseCUDAmanagedmemory.Thecommandis`exportFLAGS_use_cuda_managed_memory=false`. ...
    Args:
        msg (str): 通常是异常信息字符串
        *args: 需要记录到异常信息的参数
    """
    if 'Outofmemory' in msg or 'Out of memory' in msg:
        if "GPU" in msg:
            err_msg = f"上游服务请求时, GPU超出显存导致错误: {args}"
        else:
            err_msg = f"上游服务请求时，超出内存导致错误: {args}"
        raise InternalException(status.HTTP_504_GATEWAY_TIMEOUT, message=err_msg)
    return None
