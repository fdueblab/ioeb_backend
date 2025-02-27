# Flask后端项目框架

这是一个基于Flask的后端项目框架，提供了完整的项目结构和基本功能实现。

## 项目结构

```
.
├── app                     # 应用主目录
│   ├── __init__.py         # 应用初始化
│   ├── api                 # API模块
│   │   ├── __init__.py     # API蓝图初始化
│   │   ├── namespaces      # API命名空间
│   │   │   ├── __init__.py
│   │   │   ├── health_ns.py # 健康检查API
│   │   │   ├── user_ns.py   # 用户管理API
│   │   │   └── file_ns.py   # 文件处理API
│   │   └── routes.py       # API路由定义(已迁移到命名空间)
│   ├── extensions.py       # 扩展模块
│   ├── models.py           # 数据库模型
│   └── utils               # 工具函数模块
│       ├── __init__.py
│       ├── file_utils.py   # 文件处理工具
│       └── remote_service.py # 远程服务通信
├── mocks                   # 模拟服务
│   ├── __init__.py
│   ├── remote_service.py   # 模拟远程服务
│   └── run.py              # 启动模拟服务的脚本
├── tests                   # 测试目录
│   ├── __init__.py
│   ├── conftest.py         # 测试配置
│   ├── unit                # 单元测试
│   │   ├── __init__.py
│   │   └── test_file_utils.py
│   ├── integration         # 集成测试
│   │   ├── __init__.py
│   │   └── test_api.py
│   └── functional          # 功能测试
│       ├── __init__.py
│       └── test_file_processing.py
├── config.py               # 配置文件
├── manage.py               # 管理命令
├── requirements.txt        # 依赖列表
├── uploads                 # 上传文件目录
├── static                  # 静态文件
│   └── index.html          # 测试页面
├── wsgi.py                 # 应用入口
└── README.md               # 项目说明
```

## 功能特点

- 模块化设计，便于扩展
- 完整的数据库支持（SQLAlchemy）
- 数据库迁移支持（Flask-Migrate）
- CORS跨域支持
- 环境配置管理
- CLI管理命令
- 文件上传和处理功能
- 远程服务通信模块
- Swagger API文档
- 单元测试、集成测试和功能测试框架

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 环境变量配置

创建`.env`文件并设置以下变量：

```
FLASK_APP=wsgi.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///dev.db
REMOTE_SERVICE_URL=http://your-remote-service.com/api/process
```

### 初始化数据库

```bash
python manage.py create_db  # 创建数据库表
python manage.py seed_db    # 添加示例数据
```

### 运行应用

```bash
python wsgi.py
```

或者使用Flask CLI：

```bash
flask run
```

### 运行模拟服务

```bash
python -m mocks.run
```

### 访问Swagger文档

应用启动后，访问：
```
http://localhost:5000/api/docs
```

## API端点

### 基础API
- **GET /api/health**: 健康检查
- **GET /api/users**: 获取所有用户
- **POST /api/users**: 创建新用户
- **GET /api/users/{id}**: 获取指定用户

### 文件处理API
- **POST /api/process**: 处理ZIP文件
  - 请求: `multipart/form-data` 格式，包含 `file` 字段（ZIP文件）
  - 响应: 处理后的ZIP文件或错误信息

## 文件处理流程

1. 用户上传打包好的ZIP文件到后端
2. 后端创建临时目录，并在临时目录内解压文件
3. 后端分析代码，识别主文件
4. 主文件名称和内容发送给另一个远程服务
5. 远程服务返回生成的相关文件内容
6. 将生成的文件写入当前目录
7. 重新打包为ZIP文件
8. 返回处理后的ZIP文件给前端

## 数据库操作

使用管理命令进行数据库操作：

```bash
python manage.py create_db  # 创建数据库表
python manage.py drop_db    # 删除数据库表
python manage.py seed_db    # 添加示例数据
```

## 测试

### 单元测试

```bash
pytest tests/unit
```

### 集成测试

```bash
pytest tests/integration
```

### 功能测试

```bash
pytest tests/functional
```

### 运行所有测试

```bash
pytest
```

## 部署

待实现 