from flask import Blueprint
from flask_restx import Api

from app.api.namespaces.algorithm_service_ns import api as algorithm_service_ns
from app.api.namespaces.health_ns import api as health_ns
from app.api.namespaces.user_ns import api as user_ns

# 创建蓝图
api_bp = Blueprint("api", __name__)

# 创建API
api = Api(
    api_bp,
    version="1.0",
    title="算法微服务化 API",
    description="算法代码微服务化和用户管理API接口",
    doc="/docs",  # 将Swagger文档设置在/api/docs路径下
    # 自定义Swagger UI样式
    specs_route="/docs/",
)

# 注册命名空间
api.add_namespace(health_ns)
api.add_namespace(user_ns)
api.add_namespace(algorithm_service_ns)
