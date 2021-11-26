# __title__

本项目使用[`fastapi-start`](https://github.com/ibbd-dev/fastapi-start)工具进行初始化，该工具的帮助可以使用命令：`fas --help`。

__desc__

## 1. 功能介绍

## 2. 安装与部署

部署前需要先复制配置文件：

```sh
cd app/
cp settings-example.py settings.py

# 根据实际情况修改配置文件
vim settings.py
```

## 3. fas工具使用说明

```sh
# 添加一个模块
# test是模块名称，可以设定
fas module new --name=test

# 添加模块之后，要使模块生效，需要手动在app/main.py文件中注册该路由
# prefix: 该参数定义路由的前缀，每个模块的路由前缀必须是唯一的
from test_module.router import router as test_router
app.include_router(test_router, prefix="/test", tags=["测试模块"])

# 在当前目录增加一个test.py文件
# python是文件类型，test是文件名
fas file python test
```

fas也支持一些内置模块：

```sh
# 支持的内置模块列表
fas module list

# 查看某内置模块的帮助文档
fas module help captcha
```

## 4. 附录

## 5. 项目相关人员

- __author__
