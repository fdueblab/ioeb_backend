"""
服务API工具模型
定义服务API工具表结构(用于MCP服务)
"""

from app.extensions import db


class ServiceApiTool(db.Model):
    """服务API工具模型"""

    __tablename__ = "service_api_tools"

    id = db.Column(db.String(36), primary_key=True, comment="工具ID")
    api_id = db.Column(db.String(36), db.ForeignKey("service_apis.id"), nullable=False, comment="关联的API ID")
    name = db.Column(db.String(100), nullable=False, comment="工具名称")
    description = db.Column(db.Text, nullable=True, comment="工具描述")

    def to_dict(self):
        """将模型转换为字典"""
        result = {
            "name": self.name,
        }
        
        # 兼容两种描述字段名
        if self.description:
            result["description"] = self.description
            result["des"] = self.description
            
        return result 