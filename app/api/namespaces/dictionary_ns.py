"""
字典相关API
提供字典的增删改查功能
"""

from flask import request
from flask_restx import Namespace, Resource, fields

from app.services.dictionary_service import DictionaryServiceError, dictionary_service

# 创建命名空间
api = Namespace("dictionaries", description="字典管理API")

# 定义字典模型
dictionary_model = api.model(
    "Dictionary",
    {
        "id": fields.String(description="字典ID"),
        "category": fields.String(required=True, description="字典类别"),
        "code": fields.String(required=True, description="字典编码"),
        "text": fields.String(required=True, description="字典文本"),
        "sort": fields.Integer(description="排序号"),
        "memo": fields.String(description="备注")
    }
)

# 定义创建字典请求模型
dictionary_create_model = api.model(
    "DictionaryCreate",
    {
        "category": fields.String(required=True, description="字典类别"),
        "code": fields.String(required=True, description="字典编码"),
        "text": fields.String(required=True, description="字典文本"),
        "sort": fields.Integer(description="排序号"),
        "memo": fields.String(description="备注")
    }
)

# 定义字典响应模型
dictionary_response = api.model(
    "DictionaryResponse",
    {
        "status": fields.String(description="响应状态"),
        "message": fields.String(description="响应消息"),
        "dictionary": fields.Nested(dictionary_model, description="字典信息")
    }
)

# 定义字典列表响应模型
dictionaries_response = api.model(
    "DictionariesResponse",
    {
        "status": fields.String(description="响应状态"),
        "message": fields.String(description="响应消息"),
        "total": fields.Integer(description="总记录数"),
        "dictionaries": fields.List(fields.Nested(dictionary_model), description="字典列表")
    }
)

# 定义字典分组响应模型
grouped_dictionaries_response = api.model(
    "GroupedDictionariesResponse",
    {
        "status": fields.String(description="响应状态"),
        "message": fields.String(description="响应消息"),
        "dictionaries": fields.Raw(description="按类别分组的字典数据")
    }
)


@api.route("/all")
class AllDictionaries(Resource):
    """所有字典资源"""

    @api.doc("获取所有字典")
    @api.response(200, "Success", grouped_dictionaries_response)
    def get(self):
        """获取所有字典，按类别分组"""
        try:
            dictionaries = dictionary_service.get_all_dictionaries()
            return {
                "status": "success",
                "message": "获取所有字典成功",
                "dictionaries": dictionaries
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }, 500


@api.route("/<string:category>")
class DictionaryList(Resource):
    """字典列表资源"""

    @api.doc("获取字典列表")
    @api.response(200, "Success", dictionaries_response)
    def get(self, category):
        """获取指定类别的字典列表"""
        try:
            dictionaries = dictionary_service.get_by_category(category)
            return {
                "status": "success",
                "message": "获取字典列表成功",
                "total": len(dictionaries),
                "dictionaries": dictionaries
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }, 500

    @api.doc("创建字典")
    @api.expect(dictionary_create_model)
    @api.response(201, "Success", dictionary_response)
    def post(self, category):
        """创建字典"""
        try:
            data = request.json
            dictionary = dictionary_service.create(
                category=category,
                code=data["code"],
                text=data["text"],
                sort=data.get("sort", 0),
                memo=data.get("memo")
            )
            return {
                "status": "success",
                "message": "创建字典成功",
                "dictionary": dictionary
            }, 201
        except DictionaryServiceError as e:
            return {
                "status": "error",
                "message": str(e)
            }, 400
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }, 500


@api.route("/<string:category>/<string:code>")
class Dictionary(Resource):
    """字典资源"""

    @api.doc("获取字典")
    @api.response(200, "Success", dictionary_response)
    def get(self, category, code):
        """获取字典"""
        try:
            dictionary = dictionary_service.get_by_code(category, code)
            if not dictionary:
                return {
                    "status": "error",
                    "message": "字典不存在"
                }, 404
            return {
                "status": "success",
                "message": "获取字典成功",
                "dictionary": dictionary
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }, 500

    @api.doc("更新字典")
    @api.expect(dictionary_create_model)
    @api.response(200, "Success", dictionary_response)
    def post(self, category, code):
        """更新字典"""
        try:
            data = request.json
            dictionary = dictionary_service.update(
                category=category,
                code=code,
                text=data["text"],
                sort=data.get("sort"),
                memo=data.get("memo")
            )
            return {
                "status": "success",
                "message": "更新字典成功",
                "dictionary": dictionary
            }
        except DictionaryServiceError as e:
            return {
                "status": "error",
                "message": str(e)
            }, 400
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }, 500

    @api.doc("删除字典")
    @api.response(200, "Success")
    def delete(self, category, code):
        """删除字典"""
        try:
            dictionary_service.delete(category, code)
            return {
                "status": "success",
                "message": "删除字典成功"
            }
        except DictionaryServiceError as e:
            return {
                "status": "error",
                "message": str(e)
            }, 400
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }, 500 