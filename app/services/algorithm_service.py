"""
算法微服务生成服务
负责处理算法代码的微服务化逻辑
"""

import os
import shutil
from typing import Dict, List, Tuple, Union

from flask import current_app

from app.utils.code_checker import (
    CodeStandardIssue,
    check_code_standards,
)
from app.utils.file_utils import (
    cleanup,
    create_temp_dir,
    create_zip,
    extract_zip,
    find_main_file,
)
from app.utils.remote_service import RemoteServiceError, send_file_to_remote_service


class AlgorithmServiceError(Exception):
    """算法服务处理错误"""


def process_algorithm_code(
    file_path: str, enforce_standards: bool = True
) -> Tuple[str, Union[Dict, List[CodeStandardIssue]]]:
    """
    处理算法代码，转换为微服务

    Args:
        file_path: 上传的ZIP文件路径
        enforce_standards: 是否强制执行代码规范检查

    Returns:
        Tuple[str, Union[Dict, List[CodeStandardIssue]]]:
            - 处理后的ZIP文件路径
            - 如果成功，返回空字典；如果代码规范检查失败，返回问题列表

    Raises:
        AlgorithmServiceError: 处理过程中发生错误
    """
    # 创建工作目录
    temp_dir = create_temp_dir()
    processed_file_path = None
    code_review_issues = []

    try:
        # 解压文件
        extract_path = extract_zip(file_path, temp_dir)

        # 识别主算法文件
        main_file = find_main_file(extract_path)
        if not main_file:
            raise AlgorithmServiceError("找不到主算法文件")

        # 读取主文件内容
        with open(main_file, "r", encoding="utf-8") as f:
            main_file_content = f.read()

        # 进行代码规范检查
        if current_app.config.get("CODE_STANDARDS_CHECK", True):
            standards_passed, issues = check_code_standards(main_file_content)
            code_review_issues = issues

            # 如果启用严格模式且代码规范检查失败，则返回错误
            if (
                enforce_standards
                and not standards_passed
                and current_app.config.get("CODE_STANDARDS_STRICT", True)
            ):
                return "", code_review_issues

        # 发送到远程服务处理
        try:
            response = send_file_to_remote_service(os.path.basename(main_file), main_file_content)
        except RemoteServiceError as e:
            raise AlgorithmServiceError(f"远程服务处理失败: {str(e)}")

        # 将返回的文件内容写入当前目录
        for file_name, content in response.get("files", {}).items():
            file_path = os.path.join(extract_path, file_name)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

        # 创建ZIP文件
        processed_file_path = create_zip(extract_path)

        return processed_file_path, {}

    except Exception as e:
        if isinstance(e, AlgorithmServiceError):
            raise
        raise AlgorithmServiceError(f"处理算法代码时出错: {str(e)}")
    finally:
        # 延迟清理临时目录和处理后的文件
        # 确保处理完成后再清理，防止文件访问冲突
        try:
            # 不清理最终生成的ZIP文件
            if processed_file_path and os.path.exists(temp_dir):
                # 删除临时目录，但保留生成的ZIP文件
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            current_app.logger.warning(f"清理临时文件失败: {temp_dir}")


def cleanup_resources(file_paths: List[str]) -> None:
    """
    清理资源文件

    Args:
        file_paths: 要清理的文件路径列表
    """
    for path in file_paths:
        if path and os.path.exists(path):
            try:
                cleanup(path)
            except Exception as e:
                current_app.logger.warning(f"清理文件失败: {path}, 错误: {str(e)}")
