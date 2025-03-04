import os
import uuid

from flask import current_app, send_file
from flask_restx import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.utils.code_checker import check_code_standards, generate_code_review_report
from app.utils.file_utils import (
    cleanup,
    create_temp_dir,
    create_zip,
    extract_zip,
    find_main_file,
)
from app.utils.remote_service import RemoteServiceError, send_file_to_remote_service

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

        # 创建临时目录和变量，用于后续清理
        temp_dirs = []
        temp_files = []
        output_zip = None

        try:
            # 1. 保存上传的文件
            upload_dir = create_temp_dir()
            temp_dirs.append(upload_dir)

            zip_filename = secure_filename(file.filename)
            zip_path = os.path.join(upload_dir, zip_filename)
            file.save(zip_path)
            temp_files.append(zip_path)

            # 2. 创建解压目录并解压文件
            extract_dir = create_temp_dir()
            temp_dirs.append(extract_dir)
            extract_zip(zip_path, extract_dir)

            # 3. 查找主文件
            main_file_path = find_main_file(extract_dir)
            if not main_file_path:
                return api.abort(400, "无法识别主算法文件")

            # 读取主文件内容
            with open(main_file_path, "r", encoding="utf-8") as f:
                main_file_content = f.read()

            # 3.1 对主文件进行代码规范审查
            if current_app.config.get("CODE_STANDARDS_CHECK", True):
                passed, issues = check_code_standards(main_file_content)

                # 生成报告
                report = generate_code_review_report(issues)

                # 如果未通过且处于严格模式，则拒绝处理
                if not passed and current_app.config.get("CODE_STANDARDS_STRICT", False):
                    return {
                        "status": "fail",
                        "message": "代码规范检查未通过",
                        "review_report": report,
                    }, 422  # 422 Unprocessable Entity 更适合表示内容验证失败

            # 4. 发送主文件到远程服务
            generated_files = send_file_to_remote_service(main_file_path, main_file_content)

            # 5. 将生成的文件写入解压目录
            for filename, content in generated_files.items():
                # 确保文件名安全
                safe_filename = secure_filename(filename)
                output_path = os.path.join(extract_dir, safe_filename)

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(content)

            # 6. 重新打包为ZIP文件
            result_dir = create_temp_dir()
            temp_dirs.append(result_dir)

            output_zip_name = f"microservice_{uuid.uuid4().hex}.zip"
            output_zip = os.path.join(result_dir, output_zip_name)
            create_zip(extract_dir, output_zip)

            # 7. 返回处理后的文件
            return send_file(
                output_zip,
                as_attachment=True,
                download_name=output_zip_name,
                mimetype="application/zip",
            )

        except RemoteServiceError as e:
            return api.abort(500, f"远程服务错误: {str(e)}")
        except Exception as e:
            return api.abort(500, f"微服务生成过程中发生错误: {str(e)}")
        finally:
            # 清理临时文件和目录，但不清理output_zip所在的目录
            for temp_dir in temp_dirs:
                # 跳过包含输出ZIP文件的目录
                if output_zip and os.path.commonpath([temp_dir]) == os.path.commonpath(
                    [os.path.dirname(output_zip)]
                ):
                    continue
                try:
                    cleanup(temp_dir)
                except Exception as e:
                    current_app.logger.warning(f"清理临时目录时出错: {str(e)}")

            for temp_file in temp_files:
                try:
                    cleanup(temp_file)
                except Exception as e:
                    current_app.logger.warning(f"清理临时文件时出错: {str(e)}")

    def _allowed_file(self, filename):
        """检查文件扩展名是否允许"""
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]
        )
