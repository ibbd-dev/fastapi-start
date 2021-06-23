# FastAPI脚手架：用于系统后端接口项目

该工具主要用于协助规范FastAPI项目的目录及代码风格等。工具目标：

- 规范FastAPI后端接口项目开发。
- 提升后端​开发效率，减少重复工作。
- 增加不同项目间共享模块开发的可能性​。

## 1. 功能介绍

- [x] 项目初始化
- [x] 添加模块
- [x] 生成Python文件
- [x] 代码风格检测
- [x] 代码静态类型检测
- [ ] 覆盖率工具
- [x] 替代git clone命令的clone命令，并生成标准化的目录路径

### 1.1 内置模块列表

- [x] 验证码
- [ ] 用户管理

## 2. 安装说明

```sh
# 推荐安装方式
# linux
sudo -H pip3 install -r https://github.com/ibbd-dev/fastapi-start/raw/main/requirements.txt
sudo -H pip3 install git+https://github.com/ibbd-dev/fastapi-start.git

# windows
pip install -r https://github.com/ibbd-dev/fastapi-start/raw/main/requirements.txt
pip install git+https://github.com/ibbd-dev/fastapi-start.git
```

OR

```sh
# 源码安装
git clone https://github.com/ibbd-dev/fastapi-start
cd fastapi-start
pip install -r requiresment.txt
easy_install .
```

## 3. 使用说明

安装成功之后，会有两个命令

- `fastapi-start`: 完整命令
- `fas`: 简单命令（完整命令的别名），实现功能和完整命令一样

日常使用简单命令即可。

### 3.1 项目日常使用

```sh
# 项目初始化
# test是项目名称，可以指定为自己的项目名称
# --title and --desc: 项目的标题及描述
fas project-init test --title=测试项目 --desc=这是一个测试项目

# 项目根目录
# 项目代码目录
cd test/app

# 启动http服务
uvicorn main:app --reload --host 0.0.0.0
# 在浏览器打开：http://127.0.0.1:8000/docs#/
# 查看接口文档

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

### 3.2 帮助文档

```sh
# 显示所有帮助文档
fas --help

# 某个命令的帮助文档
fas project-init --help

# 查看版本号
fas version

# 如果不设置，则自动使用git中的配置user.name及user.email
fas config set --author=caiyy --email=caiyy@ibbd.net
# 设置git clone命令的根目录
fas config set --root-path=/var/www/src

# 可以查看配置信息
fas config get

# clone项目
# 项目会自动保存到规范化的目录中：{root-path}/git.ibbd.net/gf/iot-warning
# root-path就是前面设置的配置： fas config set --root-path=/var/www/src
fas clone git@git.ibbd.net:gf/iot-warning.git

# 在当前目录生成README.md
fas file readme --title=测试标题 --desc=描述信息
```

### 3.3 代码审查

```sh
# 帮助文档
fas check --help

# 审查当前目录
fas check flake8 --help
fas check flake8

# 审查指定目录（假设app是项目代码所在目录）
fas check flake8 app

# 对于某种类型的问题，可以启用自动修正，如：
fas check flake8 --path app --select=W292 --autopep8 
# 不过使用自动修正时要注意检查比较

# 代码静态风格检测
fas check mypy --help
fas check mypy /path/to/filename.py
```

使用说明：

- 风格审查使用的工具是`flake8`，直接使用也一样。
- 并不是所有不规范的地方都应该修复，例如行代码过长的问题，如果不是很离谱，则可以不处理（当然，最好还是处理）。

## 4. FastAPI项目开发

编码风格遵循[PEP8]((https://alvinzhu.xyz/2017/10/07/python-pep-8/))，接口风格参考[RESTFul](https://mp.weixin.qq.com/s/EOzkOlhrT4pvWIyJ_kfcqw)。

重要规则说明：

- 使用4个空格缩进，换行符使用`\n`（vscode编辑器需要配置为LF，而不是CRLF）
- 文件统一使用UTF-8编码
- 接口响应的异常类型使用HTTP的状态码
- HTTP方法的使用场景：
  - GET: 获取数据
  - DELETE: 删除数据
  - PUT: 修改数据
  - POST: 增加数据和复杂查询
- 函数的输入输出的参数类型需要明确的类型定义，粒度到最基础的简单类型，如布尔值，整型，浮点型，字符串等。对于复杂类型，则应该进一步细化：

```python
from typing import Tuple, List, Dict, Set

# 元组
Tuple[int, str, int]  # 三个元素的元组

# 列表
List[int]    # 元素类型为int的列表

# 字典
Dict[str, int]    # key类型为str，value类型为int

# 集合（和列表类型）
Set[int]
```

参考[Python类型编程](https://mp.weixin.qq.com/s/N_AfjCWg_gcQzqs22KEgVA)

- 在FastAPI中则尽量不要定义字典的输入输出，而是使用继承于`BaseModel`的类结构，可以详细定义每个字段的schema。

### 4.1 基于FastAPI的大中型项目应该具备

- 函数的参数和返回值必须要有明确的参数类型定义。
- 模块应该使用路由进行组织，模块内紧外松。
- 接口必须要有单元测试，部署时可以执行单元测试来验证。
- 交互式文档应该清晰明了，使用者能方便阅读，理解与测试。

### 4.2 项目目录结构

```sh
.
├── app
│   ├── __init__.py
│   ├── readme.md                # 接口的描述文档
│   ├── main.py                  # 主入口文件
│   ├── schema.py                # 通用schema
│   ├── settings.py              # 配置文件
│   ├── dependencies.py          # 
│   ├── exceptions.py            # 异常相关
│   ├── utile.py                 # 通用的工具函数
│   ├── common                   # 公共模块
│   |   ├── __init__.py
│   │   └── connections.py       # redis, mysql等连接公共函数
│   └── module_name              # 模块目录，每个模块独立成一个目录
│       ├── __init__.py
│       ├── README.md            # 模块说明文件
│       ├── router.py            # 模块路由文件
│       ├── schema.py            # 模块的schema
│       └── requirements.txt     # 模块依赖项
├── .vscode                      # vscode配置
│   └── settings.json
├── .gitignore
├── README.md                    # 项目说明文档
├── Dockerfile                   # Docker
└── requirements.txt             # 项目依赖包
```

模块的路由及其配置文件直接放到模块目录下，而不是将所有路由配置独立到一个目录。

### 4.3 内置模块

内置模块，可以使用命令进行快捷添加。

```sh
# module命令帮助文档
fas module --help

# 查看module命令的子命令的帮助文档
fas module add --help

# 支持的模块列表
fas module list

# 查看某内置模块的帮助文档
fas module help captcha

# 添加内置模块
fas module add captcha
```

#### 4.3.1 验证码模块

[使用文档](/app/project/captcha_module/README.md)

### 4.4 注意事项

- 模块下还可以嵌套子模块，不断套娃，但是不建议这么干，这会让系统变得过于复杂；

## 5. Python编码规范

- [PEP8规范](https://alvinzhu.xyz/2017/10/07/python-pep-8/)
- [Google的开源项目风格指南](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_style_rules/)
- [RESTFul](https://mp.weixin.qq.com/s/EOzkOlhrT4pvWIyJ_kfcqw)
- [Python类型编程](https://mp.weixin.qq.com/s/N_AfjCWg_gcQzqs22KEgVA)
