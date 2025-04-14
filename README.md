# ioeb项目后端

这是一个基于Flask的后端项目框架，提供了完整的项目结构和基本功能实现。

## 项目结构

```
.
├── app                     # 应用主目录
│   ├── __init__.py         # 应用初始化
│   ├── api                 # API层 - 处理HTTP请求和响应
│   │   ├── __init__.py     # API蓝图初始化
│   │   ├── namespaces      # API命名空间
│   │   │   ├── __init__.py
│   │   │   ├── health_ns.py        # 健康检查API
│   │   │   ├── user_ns.py          # 用户管理API
│   │   │   ├── service_ns.py       # 微服务管理API
│   │   │   └── algorithm_service_ns.py  # 算法微服务化API
│   │   └── routes.py       # API路由定义(已迁移到命名空间)
│   ├── services            # 服务层 - 处理业务逻辑
│   │   ├── __init__.py     # 服务层初始化
│   │   ├── user_service.py # 用户服务
│   │   ├── service_service.py # 微服务管理服务
│   │   └── algorithm_service.py # 算法微服务生成服务
│   ├── repositories        # 数据访问层 - 处理数据持久化
│   │   ├── __init__.py     # 数据访问层初始化
│   │   ├── base_repository.py # 基础数据访问仓库
│   │   ├── user_repository.py  # 用户数据访问仓库
│   │   └── service_repository.py  # 微服务数据访问仓库
│   ├── models              # 数据模型定义
│   │   ├── __init__.py
│   │   ├── user            # 用户相关模型
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── role.py
│   │   │   ├── role_permission.py
│   │   │   └── user_tokens.py
│   │   └── service         # 微服务相关模型
│   │       ├── __init__.py
│   │       ├── service.py
│   │       ├── service_norm.py
│   │       ├── service_source.py
│   │       ├── service_api.py
│   │       └── service_api_parameter.py
│   ├── extensions.py       # 扩展模块
│   └── utils               # 工具函数模块
│       ├── __init__.py
│       ├── file_utils.py   # 文件处理工具
│       ├── code_checker.py # 代码规范检查工具
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
├── nginx                   # Nginx配置
│   └── conf.d              # Nginx配置文件目录
│       └── app.conf        # 应用Nginx配置
├── Dockerfile              # Docker构建文件
├── docker-compose.yml      # Docker Compose配置
├── .github                 # GitHub集成
│   └── workflows           # GitHub Actions工作流
│       └── ci-cd.yml       # CI/CD工作流配置
├── wsgi.py                 # 应用入口
└── README.md               # 项目说明
```

## 功能特点

- 模块化设计，便于扩展
- 三层架构（API层、服务层、数据访问层）
- 完整的数据库支持（SQLAlchemy）
- 数据库迁移支持（Flask-Migrate）
- CORS跨域支持
- 环境配置管理
- CLI管理命令
- 微服务管理功能（增删改查、搜索、筛选）
- 算法代码微服务化功能
- 代码规范自动检查
- 远程服务通信模块
- Swagger API文档
- Docker部署支持
- CI/CD集成
- 单元测试、集成测试和功能测试框架

## 架构设计

本项目采用完整的三层架构设计：

1. **API层（Controllers）**：处理HTTP请求和响应，参数校验，不包含业务逻辑
2. **服务层（Services）**：处理所有业务逻辑，是应用程序的核心
3. **数据访问层（Repositories）**：处理数据持久化，包括数据库操作

### API层

API层位于`app/api/namespaces`目录，主要负责：
- 处理HTTP请求和响应
- 输入验证和参数校验
- 路由和端点定义
- 响应格式化和错误处理

### 服务层

服务层位于`app/services`目录，包含所有业务逻辑处理代码。主要服务包括：

- **用户服务（UserService）**：处理用户注册、认证、查询等
- **微服务管理服务（ServiceService）**：处理微服务的增删改查、搜索、筛选等
- **算法微服务生成服务（AlgorithmService）**：处理算法代码的微服务化逻辑

### 数据访问层

数据访问层位于`app/repositories`目录，专门处理数据库操作和持久化逻辑：

- **基础仓库（BaseRepository）**：提供通用的CRUD操作
- **用户仓库（UserRepository）**：处理用户表的特定数据访问操作
- **微服务仓库（ServiceRepository）**：处理微服务相关表的数据访问操作

数据访问层通过泛型和依赖注入的方式设计，便于扩展和测试。

### 分层架构的优势

- **关注点分离**：每一层只关注自己的职责，代码更清晰
- **可测试性**：各层可以独立测试，不依赖其他层的实现
- **可替换性**：底层实现可以替换而不影响上层代码
- **可维护性**：各层职责明确，便于维护和扩展
- **代码复用**：通用逻辑可以在各层之间复用

## 数据模型设计

### 用户相关模型
- **User**：用户基本信息
- **Role**：角色信息
- **RolePermission**：角色权限关系
- **UserToken**：用户令牌信息

### 微服务相关模型
- **Service**：微服务基本信息
- **ServiceNorm**：服务规范评分
- **ServiceSource**：服务来源信息
- **ServiceApi**：服务API信息
- **ServiceApiParameter**：API参数信息

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 环境变量配置

创建`.env`文件并设置以下变量：

```
FLASK_APP=wsgi.py
FLASK_DEBUG=1
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

目前线上版本的API可通过访问[在线版本的Swagger文档](http://fdueblab.cn:5000/api/docs)查看

## 算法微服务化流程

1. 用户上传打包好的算法代码ZIP文件到后端
2. 后端创建临时目录，并在临时目录内解压文件
3. 后端分析代码，识别主算法文件
4. 对主算法文件进行代码规范检查（包括函数封装、Google风格注释、类型注解）
5. 将主算法文件名称和内容发送给微服务生成服务
6. 微服务生成服务返回生成的微服务框架文件
7. 将生成的文件写入当前目录
8. 重新打包为ZIP文件
9. 返回生成的微服务项目ZIP文件给前端

## 微服务管理功能

微服务管理功能提供了对微服务的全生命周期管理，包括：

1. **微服务创建**：创建新的微服务，包括基本信息、规范评分、来源信息和API定义
2. **微服务查询**：按ID查询、关键词搜索或条件筛选微服务
3. **微服务更新**：更新微服务的各项信息，包括关联数据
4. **微服务删除**：软删除微服务（将deleted字段标记为1）

微服务相关数据表包括：
- `services`: 存储微服务基本信息
- `service_norms`: 存储微服务规范评分
- `service_sources`: 存储微服务来源信息
- `service_apis`: 存储微服务API信息
- `service_api_parameters`: 存储API参数信息

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
