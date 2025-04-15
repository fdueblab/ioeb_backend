"""
字典数据模型
定义系统字典表结构
"""

from app.extensions import db


class Dictionary(db.Model):
    """Dictionary模型"""

    __tablename__ = "dictionaries"

    # 主键和基本信息
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="字典ID")
    category = db.Column(db.String(50), nullable=False, comment="字典类别")
    code = db.Column(db.String(50), nullable=False, comment="字典编码")
    text = db.Column(db.String(100), nullable=False, comment="字典文本")
    sort = db.Column(db.Integer, nullable=False, default=0, comment="排序号")
    memo = db.Column(db.String(200), nullable=True, comment="备注")

    def __repr__(self):
        return f"<Dictionary {self.category}:{self.code}>"

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "code": self.code,
            "text": self.text,
            "sort": self.sort,
            "memo": self.memo
        }
