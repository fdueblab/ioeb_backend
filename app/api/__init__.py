"""
API包
定义应用中使用的API接口
"""

from flask import Blueprint
from flask_cors import CORS
from flask_restx import Api

from app.api.namespaces.auth_ns import api as auth_ns
from app.api.namespaces.dataset_ns import api as dataset_ns
from app.api.namespaces.dictionary_ns import api as dictionary_ns
from app.api.namespaces.health_ns import api as health_ns
from app.api.namespaces.service_ns import api as service_ns
from app.api.namespaces.user_ns import api as user_ns

# 创建蓝图
api_bp = Blueprint("api", __name__)

CORS(api_bp, resources={r"/*": {"origins": "*"}})

# 创建API
api = Api(
    api_bp,
    version="1.0",
    title="ioeb项目后端 API",
    description="ioeb项目后端 API接口",
    doc="/docs",  # 将Swagger文档设置在/api/docs路径下
    # 自定义Swagger UI样式
    specs_route="/docs/",
)

# 注册命名空间
api.add_namespace(health_ns)
api.add_namespace(user_ns)
api.add_namespace(service_ns)
api.add_namespace(auth_ns, path="/auth")  # 添加认证命名空间
api.add_namespace(dictionary_ns, path="/dictionaries")
api.add_namespace(dataset_ns, path="/datasets")  # 添加数据集命名空间
