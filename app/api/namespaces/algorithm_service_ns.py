import os
import uuid

from flask import current_app, send_file
from flask_restx import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.services.algorithm_service import (
    AlgorithmServiceError,
    cleanup_resources,
    process_algorithm_code,
)

# 创建命名空间
api = Namespace("algorithm_service", description="算法代码微服务化API")

# 定义上传解析器
upload_parser = api.parser()
upload_parser.add_argument(
    "file", location="files", type=FileStorage, required=True, help="算法代码ZIP文件"
)

# 定义错误响应模型
error_response = api.model(
    "ErrorResponse",
    {
        "status": fields.String(description="响应状态", default="fail"),
        "message": fields.String(description="错误消息"),
    },
)

# 定义代码审查响应模型
code_review_response = api.model(
    "CodeReviewResponse",
    {
        "status": fields.String(description="响应状态", default="fail"),
        "message": fields.String(description="错误消息"),
        "review_report": fields.String(description="代码审查报告"),
    },
)


@api.route("")
class AlgorithmServiceGenerator(Resource):
    @api.doc(
        "algorithm_to_service",
        responses={
            200: "算法代码微服务化成功，返回处理后的ZIP文件",
            400: "请求错误",
            500: "服务器错误",
        },
    )
    @api.expect(upload_parser)
    @api.produces(["application/zip"])
    @api.response(400, "Invalid input or Code standards not met", error_response)
    @api.response(422, "Code standards not met", code_review_response)
    @api.response(500, "Processing error", error_response)
    def post(self):
        """
        将算法代码封装为微服务

        接收算法代码的ZIP文件，分析识别主文件，生成微服务框架并返回完整的微服务项目
        """
        args = upload_parser.parse_args()
        file = args["file"]

        # 检查文件名
        if file.filename == "":
            return api.abort(400, "未选择文件")

        # 检查文件类型
        if not self._allowed_file(file.filename):
            return api.abort(400, "不支持的文件类型，仅支持ZIP文件")

        # 创建临时目录，用于存储上传的文件
        temp_file_path = None
        enforce_standards = current_app.config.get("CODE_STANDARDS_STRICT", True)

        try:
            # 保存上传的文件
            upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], str(uuid.uuid4()))
            os.makedirs(upload_dir, exist_ok=True)

            zip_filename = secure_filename(file.filename)
            temp_file_path = os.path.join(upload_dir, zip_filename)
            file.save(temp_file_path)

            # 调用服务层处理算法代码
            output_zip, code_review_issues = process_algorithm_code(
                temp_file_path, enforce_standards
            )

            # 如果代码检查未通过
            if not output_zip and code_review_issues:
                from app.utils.code_checker import generate_code_review_report

                report = generate_code_review_report(code_review_issues)
                return {
                    "status": "fail",
                    "message": "代码规范检查未通过",
                    "review_report": report,
                }, 422

            # 返回生成的ZIP文件
            output_zip_name = f"microservice_{uuid.uuid4().hex}.zip"
            return send_file(
                output_zip,
                as_attachment=True,
                download_name=output_zip_name,
                mimetype="application/zip",
            )

        except AlgorithmServiceError as e:
            return api.abort(400, f"算法微服务化失败: {str(e)}")
        except Exception as e:
            current_app.logger.error(f"处理过程中发生错误: {str(e)}")
            return api.abort(500, f"微服务生成过程中发生错误: {str(e)}")
        finally:
            # 清理临时文件
            if temp_file_path and os.path.exists(temp_file_path):
                cleanup_resources([temp_file_path])

    def _allowed_file(self, filename):
        """检查文件扩展名是否允许"""
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]
        )
