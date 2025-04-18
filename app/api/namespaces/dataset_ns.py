"""
数据集相关API
提供数据集的增删改查功能
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage

from app.services.dataset_service import DatasetServiceError, dataset_service

# 创建命名空间
api = Namespace("datasets", description="数据集管理API")

# 定义数据集模型
dataset_model = api.model(
    "Dataset",
    {
        "id": fields.String(description="数据集ID"),
        "name": fields.String(required=True, description="数据集名称"),
        "description": fields.String(description="数据集描述"),
        "fileKey": fields.String(description="COS对象键"),
        "fileName": fields.String(description="原始文件名"),
        "fileSize": fields.Integer(description="文件大小(字节)"),
        "fileType": fields.String(description="文件类型"),
        "fileExtension": fields.String(description="文件扩展名"),
        "metadata": fields.Raw(
            description="元数据"
        ),  # 注意：这里保持metadata名称与前端保持一致，实际对应数据库中的meta_data字段
        "tags": fields.List(fields.String, description="标签"),
        "status": fields.String(description="状态"),
        "createTime": fields.Integer(description="创建时间戳"),
        "updateTime": fields.Integer(description="更新时间戳"),
        "creatorId": fields.String(description="创建者ID"),
    },
)

# 定义创建数据集请求模型
dataset_create_model = api.model(
    "DatasetCreate",
    {
        "name": fields.String(required=True, description="数据集名称"),
        "description": fields.String(description="数据集描述"),
        "tags": fields.List(fields.String, description="标签"),
        "metadata": fields.Raw(description="元数据"),  # 注意：这里保持metadata名称与前端保持一致
    },
)

# 定义更新数据集请求模型
dataset_update_model = api.model(
    "DatasetUpdate",
    {
        "name": fields.String(description="数据集名称"),
        "description": fields.String(description="数据集描述"),
        "tags": fields.List(fields.String, description="标签"),
        "metadata": fields.Raw(description="元数据"),  # 注意：这里保持metadata名称与前端保持一致
        "status": fields.String(description="状态"),
    },
)

# 定义数据集响应模型
dataset_response = api.model(
    "DatasetResponse",
    {
        "status": fields.String(description="响应状态"),
        "message": fields.String(description="响应消息"),
        "dataset": fields.Nested(dataset_model, description="数据集信息"),
    },
)

# 定义数据集列表响应模型
datasets_response = api.model(
    "DatasetsResponse",
    {
        "status": fields.String(description="响应状态"),
        "message": fields.String(description="响应消息"),
        "total": fields.Integer(description="总记录数"),
        "datasets": fields.List(fields.Nested(dataset_model), description="数据集列表"),
    },
)

# 定义URL响应模型
url_response = api.model(
    "UrlResponse",
    {
        "status": fields.String(description="响应状态"),
        "message": fields.String(description="响应消息"),
        "url": fields.String(description="下载URL"),
    },
)

# 定义错误响应模型
error_response = api.model(
    "ErrorResponse",
    {
        "status": fields.String(description="响应状态", default="error"),
        "message": fields.String(description="错误信息"),
    },
)

# 文件上传解析器
upload_parser = api.parser()
upload_parser.add_argument(
    "file", location="files", type=FileStorage, required=True, help="数据集文件"
)
upload_parser.add_argument("name", type=str, required=True, help="数据集名称")
upload_parser.add_argument("description", type=str, required=False, help="数据集描述")
upload_parser.add_argument("tags", type=str, required=False, help="标签，多个标签用逗号分隔")
upload_parser.add_argument("metadata", type=str, required=False, help="元数据，JSON格式字符串")


@api.route("")
class DatasetList(Resource):
    @api.doc("list_datasets")
    @api.marshal_with(datasets_response, code=200)
    def get(self):
        """获取所有数据集"""
        try:
            datasets = dataset_service.get_all_datasets()
            return {
                "status": "success",
                "message": "获取数据集列表成功",
                "total": len(datasets),
                "datasets": datasets,
            }, 200
        except DatasetServiceError as e:
            return {"status": "error", "message": str(e)}, 500

    @api.doc("create_dataset")
    @api.expect(upload_parser)
    @api.marshal_with(dataset_response, code=201)
    @api.response(400, "Invalid input", error_response)
    @api.response(500, "Server error", error_response)
    def post(self):
        """上传文件创建新数据集"""
        args = upload_parser.parse_args()
        file = args.get("file")
        name = args.get("name")
        description = args.get("description")

        # 处理标签
        tags = []
        if args.get("tags"):
            tags = [tag.strip() for tag in args.get("tags").split(",") if tag.strip()]

        # 处理元数据
        metadata = {}
        if args.get("metadata"):
            try:
                import json

                metadata = json.loads(args.get("metadata"))
            except json.JSONDecodeError:
                return {"status": "error", "message": "元数据格式错误，应为有效的JSON字符串"}, 400

        if not file:
            return {"status": "error", "message": "缺少文件"}, 400

        if not name:
            return {"status": "error", "message": "数据集名称不能为空"}, 400

        try:
            dataset = dataset_service.create_dataset_from_file(
                file=file,
                name=name,
                description=description,
                tags=tags,
                metadata=metadata,
                creator_id=None,  # 可以从认证信息中获取
            )
            return {"status": "success", "message": "数据集创建成功", "dataset": dataset}, 201
        except DatasetServiceError as e:
            return {"status": "error", "message": str(e)}, 400


@api.route("/<string:id>")
@api.param("id", "数据集ID")
class DatasetDetail(Resource):
    @api.doc("get_dataset")
    @api.marshal_with(dataset_response, code=200)
    @api.response(404, "Dataset not found", error_response)
    def get(self, id):
        """获取指定ID的数据集"""
        try:
            dataset = dataset_service.get_dataset_by_id(id)
            return {"status": "success", "message": "获取数据集成功", "dataset": dataset}, 200
        except DatasetServiceError as e:
            return {"status": "error", "message": str(e)}, 404

    @api.doc("update_dataset")
    @api.expect(dataset_update_model)
    @api.marshal_with(dataset_response, code=200)
    @api.response(400, "Invalid input", error_response)
    @api.response(404, "Dataset not found", error_response)
    @api.response(500, "Server error", error_response)
    def put(self, id):
        """更新指定ID的数据集"""
        data = request.get_json()

        if not data:
            return {"status": "error", "message": "缺少请求数据"}, 400

        try:
            dataset = dataset_service.update_dataset(id, data)
            return {"status": "success", "message": "数据集更新成功", "dataset": dataset}, 200
        except DatasetServiceError as e:
            if "不存在" in str(e):
                return {"status": "error", "message": str(e)}, 404
            return {"status": "error", "message": str(e)}, 400

    @api.doc("delete_dataset")
    @api.response(200, "Success")
    @api.response(404, "Dataset not found", error_response)
    @api.response(500, "Server error", error_response)
    def delete(self, id):
        """删除指定ID的数据集"""
        try:
            # 获取查询参数
            delete_file = request.args.get("delete_file", "true").lower() == "true"

            dataset_service.delete_dataset(id, delete_file=delete_file)
            return {"status": "success", "message": "数据集删除成功"}, 200
        except DatasetServiceError as e:
            if "不存在" in str(e):
                return {"status": "error", "message": str(e)}, 404
            return {"status": "error", "message": str(e)}, 500


@api.route("/<string:id>/download-url")
@api.param("id", "数据集ID")
class DatasetDownloadUrl(Resource):
    @api.doc("get_dataset_download_url")
    @api.marshal_with(url_response, code=200)
    @api.response(404, "Dataset not found", error_response)
    @api.response(500, "Server error", error_response)
    def get(self, id):
        """获取数据集文件的下载URL"""
        try:
            # 获取查询参数
            expired = request.args.get("expired", 3600)
            try:
                expired = int(expired)
            except ValueError:
                expired = 3600

            url = dataset_service.get_dataset_download_url(id, expired=expired)
            return {"status": "success", "message": "获取下载URL成功", "url": url}, 200
        except DatasetServiceError as e:
            if "不存在" in str(e):
                return {"status": "error", "message": str(e)}, 404
            return {"status": "error", "message": str(e)}, 500


@api.route("/search")
class DatasetSearch(Resource):
    @api.doc("search_datasets")
    @api.param("keyword", "搜索关键词")
    @api.marshal_with(datasets_response, code=200)
    def get(self):
        """搜索数据集"""
        keyword = request.args.get("keyword", "")
        try:
            datasets = dataset_service.search_datasets(keyword)
            return {
                "status": "success",
                "message": "搜索数据集成功",
                "total": len(datasets),
                "datasets": datasets,
            }, 200
        except DatasetServiceError as e:
            return {"status": "error", "message": str(e)}, 500


@api.route("/filter")
class DatasetFilter(Resource):
    @api.doc("filter_datasets")
    @api.param("status", "状态 (active-可用, archived-已归档, deleted-已删除)")
    @api.param(
        "file_type",
        "文件类型 (image-图片, audio-音频, video-视频, document-文档, archive-压缩文件, other-其他)",
    )
    @api.param("file_extension", "文件扩展名")
    @api.param("tags", "标签，多个标签用逗号分隔")
    @api.marshal_with(datasets_response, code=200)
    def get(self):
        """筛选数据集"""
        filters = {}

        # 处理状态
        status = request.args.get("status")
        if status:
            filters["status"] = status

        # 处理文件类型
        file_type = request.args.get("file_type")
        if file_type:
            filters["file_type"] = file_type

        # 处理文件扩展名
        file_extension = request.args.get("file_extension")
        if file_extension:
            filters["file_extension"] = file_extension

        # 处理标签
        tags = request.args.get("tags")
        if tags:
            filters["tags"] = [tag.strip() for tag in tags.split(",") if tag.strip()]

        try:
            datasets = dataset_service.filter_datasets(**filters)
            return {
                "status": "success",
                "message": "筛选数据集成功",
                "total": len(datasets),
                "datasets": datasets,
            }, 200
        except DatasetServiceError as e:
            return {"status": "error", "message": str(e)}, 500
