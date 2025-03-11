"""
角色权限数据模型
定义Role_Permissions数据库表结构
"""

from app.extensions import db


class RolePermission(db.Model):
    """RolePermission模型"""

    __tablename__ = "role_permissions"

    # 主键和基本信息
    id = db.Column(db.Integer, primary_key=True, comment="角色权限ID")  # 使用字符串类型的UUID
    role_id = db.Column(db.String(36), db.ForeignKey("roles.id"), nullable=False, comment="角色ID")
    permission_id = db.Column(db.String(36), nullable=False, comment="权限ID")
    permission_name = db.Column(db.String(100), nullable=False, comment="权限名称")
    data_access = db.Column(db.String(36), nullable=True, default="", comment="访问权限")

    # # 添加关系属性（可选）
    # role = db.relationship('Role', backref=db.backref('role_permissions', lazy=True))

    def __init__(self, **kwargs):
        """初始化RolePermission实例"""
        super().__init__(**kwargs)
        if not self.id:
            # 自增
            self.id = db.session.query(db.func.max(RolePermission.id)).scalar() + 1

    def __repr__(self):
        return f"<RolePermission {self.role_id} - {self.permission_id}>"

    def to_dict(self):
        """将模型转换为字典"""
        return {
            "id": self.id,
            "roleId": self.role_id,
            "permissionId": self.permission_id,
            "permissionName": self.permission_name,
            "dataAccess": self.data_access,
        }
