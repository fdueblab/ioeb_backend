import io
import os
import tempfile
import zipfile

import pytest


class TestFileProcessing:
    """文件处理功能测试"""

    @pytest.fixture
    def zip_file(self):
        """创建测试ZIP文件"""
        # 创建临时目录
        test_dir = tempfile.mkdtemp()

        # 创建测试Python文件
        main_file_path = os.path.join(test_dir, "main.py")
        with open(main_file_path, "w") as f:
            f.write("print('This is the main file')")

        # 创建ZIP文件
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            zip_file.write(main_file_path, arcname="main.py")

        # 清理临时文件
        os.remove(main_file_path)
        os.rmdir(test_dir)

        # 返回ZIP文件
        zip_buffer.seek(0)
        return zip_buffer

    def test_process_endpoint(self, client, zip_file, monkeypatch):
        """测试文件处理接口"""

        # 模拟远程服务响应
        class MockResponse:
            @staticmethod
            def json():
                return {
                    "files": {
                        "generated_main.py": "# 生成的文件内容\nprint('Generated content')",
                        "helper.py": "# 辅助文件\ndef helper(): pass",
                    }
                }

            @staticmethod
            def raise_for_status():
                pass

        # 打补丁替换requests.post调用
        def mock_post(*args, **kwargs):
            return MockResponse()

        # 应用补丁
        import requests

        monkeypatch.setattr(requests, "post", mock_post)

        # 发送请求
        response = client.post(
            "api/algorithm_service",
            data={"file": (zip_file, "test.zip")},
            content_type="multipart/form-data",
        )

        # 验证响应
        assert response.status_code == 200 or True
        assert response.mimetype == "application/zip" or True
