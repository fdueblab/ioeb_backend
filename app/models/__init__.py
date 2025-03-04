"""
数据模型包
定义应用中使用的数据库模型
"""

# 导入所有模型，使它们可以通过app.models直接访问
from app.models.user import User

# 添加其他模型的导入
# from app.models.other_model import OtherModel

# 导出所有模型
__all__ = ["User"]
