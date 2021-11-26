# -*- coding: utf-8 -*-
#
# 配置相关命令
# Author: alex
# Created Time: 2021年06月13日 星期日
from os import mkdir
from os.path import join, isdir, isfile, expanduser
import json
from typing import Dict, Optional
from .utils import get_user_from_git
from .settings import package_path
from .api_config import api_get, api_post, schema_params, schema_resp

# 工具的配置目录
config_path = join(expanduser('~'), '.fastapi-start')
config_file = join(config_path, 'config.json')
if not isdir(config_path):
    mkdir(config_path)


class Config:
    """配置代码根目录等信息
    配置文件的保存目录为: 用户目录/.fastapi-start/

    Examples:
        获取配置信息（author和email直接从git的配置中获取）：
            fas config get
        设置代码根目录（使用clone命令时，需要该目录）：
            fas config set --root-path=/var/www
    """

    def get(self):
        """获取配置变量的信息
        """
        return get_config()

    def set(self, root_path: str = ''):
        """设置配置变量
        Args:
            root_path str: 代码根目录，使用clone命令的时候会在该目录下生成标准的目录路径，如: root_path/github.com/username/project/
        """
        config_set(root_path=root_path)

    def mysql(self, settings_file: Optional[str] = None):
        """MySQL配置常量：把变量加入到对应的settings.py及settings-example.py文件中
        """
        files = [settings_file] if settings_file else ['settings.py', 'settings-example.py']
        exist_files = [f for f in files if isfile(f)]
        if len(exist_files) == 0:
            print(f"对应的配置文件不存在：{files}")
            return
        print(f"存在的配置文件：{exist_files}")

        with open(join(package_path, 'data', 'mysql_cfg.py'), encoding='utf8') as f:
            mysql_cfg = f.read()
        for fname in exist_files:
            print(f'配置写入文件：{fname}')
            with open(fname, 'a+', encoding='utf8') as f:
                f.write(mysql_cfg)

    def gen_api(self, router: str, title: str = '', method: str = 'POST',
                router_file='router.py', schema_file='schema.py'):
        """生成API接口基本代码

        Args:
            method: str, http方法，取值为POST或者GET，默认为POST
        """
        method = method.upper()
        if method not in ('POST', 'GET'):
            print(f"method只能取值：POST or GET")
            return
        # 规范路由样式
        router = router.strip().lower()
        if not router.startswith('/'):
            print(f"router参数必须以/开头: {router}")
            return
        if ' ' in router:
            print(f"router参数不能带有空格: {router}")
            return
        if '_' in router:
            print(f"router参数值不建议使用下划线: {router}")
            print("可以将下划线改成使用/来替代，例如：/a_b => /a/b")
            return
        if not isfile(router_file):
            print(f"{router_file}: router文件不存在")
            return
        if not isfile(schema_file):
            print(f"{schema_file}: schema文件不存在")
            return
        # 生成函数名
        def_name = router.strip('/').replace('/', '_')
        key = ''.join([k.title() for k in def_name.split('_')])
        params_text = schema_params.replace('__key__', key)
        if method == 'GET':
            api_text = api_get.replace('__def__', def_name).replace('__key__', key).replace('__title__', title).replace('__router__', router)
            with open(router_file, 'a+', encoding='utf8') as f:
                f.write(api_text)
            with open(schema_file, 'a+', encoding='utf8') as f:
                f.write(params_text)
            print(f'在文件{router_file}和{schema_file}中生成了相应的代码。')
            return

        # POST
        resp_text = schema_resp.replace('__key__', key)
        api_text = api_post.replace('__def__', def_name).replace('__key__', key).replace('__title__', title).replace('__router__', router)
        with open(router_file, 'a+', encoding='utf8') as f:
            f.write(api_text)
        with open(schema_file, 'a+', encoding='utf8') as f:
            f.write(params_text)
            f.write(resp_text)
        print(f'在文件{router_file}和{schema_file}中生成了相应的代码。')


def config_set(root_path: str = ''):
    """"""
    if isfile(config_file):
        with open(config_file, encoding='utf8') as f:
            data = json.load(f)
    else:
        data = {}

    if root_path:
        if not isdir(root_path):
            raise Exception(f'代码根目录不是有效目录：{root_path}')
        data['root_path'] = root_path
    if data:
        with open(config_file, 'w', encoding='utf8', newline='') as f:
            json.dump(data, f)


def get_config() -> Dict[str, str]:
    """获取配置信息
    用户名及Email从git配置获取
    Returns:
        dict
    """
    author, email = get_user_from_git()
    if not isfile(config_file):
        return {'author': author, 'email': email}
    with open(config_file, encoding='utf8') as f:
        data = json.load(f)
    data['author'], data['email'] = author, email
    return data
