# -*- coding: utf-8 -*-
#
# 模块路由文件
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from fastapi import APIRouter, Path
from fastapi import status, HTTPException
import tempfile
from starlette.responses import FileResponse
import random
import string
from captcha.image import ImageCaptcha
from schema import MessageResp     # 通用schema
from .api import set_captcha

"""
在系统入口main.py文件中加入:
    from captcha_module.router import router as captcha_router
    app.include_router(captcha_router, prefix="/captcha", tags=["验证码"])
"""
router = APIRouter()

# 验证码所有字符
char_all = string.ascii_letters + string.digits


@router.get("/", summary='模块测试API',
            response_model=MessageResp)
async def test_api():
    """模块测试API"""
    return {'message': 'ok'}


@router.get("/image/{token}", summary='生成验证码图像')
async def captcha_image_api(
    token: str = Path(..., regex='^[0-9a-z]+$', title='表单唯一值，用于标识表单',
                      description='表单唯一值，用于标识表单')
):
    """生成验证码图像\n
    表单在生成之前通常会生成一个唯一字符串token，该token值可以用于避免重复提交，也用于请求验证码。\n
    验证码不区分大小写。\n
    该接口返回一个图像文件。
    """
    code = ''.join(random.sample(char_all, 4))
    # print('captcha: ', code)
    if not set_captcha(token, code):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='')
    image = ImageCaptcha().generate_image(code)
    with tempfile.NamedTemporaryFile(mode='w+b', suffix='.png', delete=False) as outfile:
        image.save(outfile)
        return FileResponse(outfile.name, media_type='image/png')
