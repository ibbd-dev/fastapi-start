# FastAPI脚手架：用于系统后端接口项目

## 安装

```sh
easy_install .
```

OR

```sh
# linux
sudo -H pip3 install -r https://github.com/ibbd-dev/fastapi-start/raw/master/requirements.txt
sudo -H pip3 install git+https://github.com/ibbd-dev/fastapi-start.git

# windows
pip install -r https://github.com/ibbd-dev/fastapi-start/raw/master/requirements.txt
pip install git+https://github.com/ibbd-dev/fastapi-start.git
```

## 使用

安装成功之后，会有一个命令`fastapi-start`

```sh
# 初次使用时，首先配置用户名
fastapi-start config caiyy

# 项目初始化
# test是项目名称，可以指定为自己的项目名称
# --title and --desc: 项目的标题及描述
fastapi-start project-init test --title=测试项目 --desc=这是一个测试项目

# 项目代码目录
cd test/app

# 添加一个模块
# test是模块名称，可以设定
# --prefix: 模块的路由前缀
# --tags: 模块的标签（展示在交互式接口文档上）
fastapi-start module-add test --prefix=/test --tags=测试

# 在当前目录增加一个python文件
fastapi-start file-add filename
```

## 基于FastAPI的大中型项目应该具备

- 函数的参数和返回值必须要有明确的参数类型定义。
- 模块应该使用路由进行组织，模块内紧外松。
- 接口必须要有单元测试，部署时可以执行单元测试来验证。
- 交互式文档应该清晰明了，使用者能方便阅读，理解与测试。

## 项目目录结构

```sh
.
├── app
│   ├── __init__.py
│   ├── readme.md                # 接口的描述文档
│   ├── main.py                  # 主入口文件
│   ├── settings.py              # 配置文件
│   ├── dependencies.py          # 
│   ├── exceptions.py            # 异常相关
│   ├── utile.py                 # 通用的工具函数
│   ├── common                   # 公共模块
│   │   ├── __init__.py
│   └── module_name              # 模块目录，每个模块独立成一个目录
│       ├── __init__.py
│       ├── rule.py              # 模块路由文件
│       └── rule_settings.py     # 路由文件配置
├── .vscode                      # vscode配置
│   ├── settings.json
├── .gitignore
├── README.md                    # 项目说明文档
├── install.md                   # 安装部署与运维文档
├── Dockerfile                   # Docker
├── requirements.txt             # 项目依赖包
```

## 脚手架基本功能

- [x] 项目初始化
- [x] 添加模块
- [x] 生成Python文件
- [ ] 规范化检测
