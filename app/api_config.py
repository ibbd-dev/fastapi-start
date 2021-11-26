# 路由中的配置

api_post = \
'''
from .schema import __key__Resp, __key__Params

@router.post("__router__", summary="__title__",
             response_model=__key__Resp)
async def api___def__(
    params: __key__Params
):
    """__title__
    """
    return
'''

api_get = \
'''
from .schema import __key__Resp

@router.get("__router__", summary="__title__",
            response_model=__key__Resp)
async def api___def__():
    """__title__
    """
    return
'''

schema_params = \
'''
class __key__Params(BaseModel):
    test: str = Field(..., example='', title='')
'''

schema_resp = \
'''
class __key__Resp(BaseModel):
    test: str = Field(..., example='', title='')
'''
