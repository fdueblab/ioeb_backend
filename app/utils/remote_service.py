import json
import os

import requests
from flask import current_app


class RemoteServiceError(Exception):
    """远程服务错误"""


def send_file_to_remote_service(file_path, file_content):
    """
    发送文件到远程服务并获取生成的文件

    Args:
        file_path (str): 文件路径
        file_content (str): 文件内容

    Returns:
        dict: 包含生成文件内容的字典
        格式: {
            'file1.py': '文件1内容',
            'file2.py': '文件2内容',
            ...
        }

    Raises:
        RemoteServiceError: 远程服务通信错误
    """
    try:
        # 获取远程服务的URL（从配置中读取）
        remote_service_url = current_app.config.get(
            "REMOTE_SERVICE_URL", "http://example.com/api/process"
        )

        # 准备请求数据
        payload = {"file_name": os.path.basename(file_path), "file_content": file_content}

        # 发送请求到远程服务
        response = requests.post(
            remote_service_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30,  # 30秒超时
        )

        # 检查响应状态
        response.raise_for_status()

        # 解析响应数据
        result = response.json()

        if "error" in result:
            raise RemoteServiceError(f"远程服务错误: {result['error']}")

        if "files" not in result:
            raise RemoteServiceError("远程服务返回的数据格式错误: 缺少'files'字段")

        return result["files"]

    except requests.RequestException as e:
        raise RemoteServiceError(f"远程服务通信错误: {str(e)}")
    except json.JSONDecodeError:
        raise RemoteServiceError("远程服务返回的数据不是有效的JSON格式")
    except Exception as e:
        raise RemoteServiceError(f"与远程服务通信时发生未知错误: {str(e)}")
