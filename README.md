# FastAPI脚手架：用于系统后端接口项目

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

- [ ] 项目初始化
- [ ] 添加模块
- [ ] 生成Python文件
- [ ] 规范化检测
