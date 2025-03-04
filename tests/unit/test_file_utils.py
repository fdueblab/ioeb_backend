import os
import tempfile

import pytest

from app.utils.file_utils import (
    cleanup,
    create_temp_dir,
    find_main_file,
)


class TestFileUtils:
    """文件工具模块的单元测试"""

    def test_create_temp_dir(self):
        """测试创建临时目录"""
        temp_dir = create_temp_dir()
        assert os.path.exists(temp_dir)
        assert os.path.isdir(temp_dir)
        # 清理
        cleanup(temp_dir)

    def test_find_main_file(self):
        """测试主文件查找功能"""
        # 创建临时测试目录
        test_dir = tempfile.mkdtemp()
        try:
            # 创建测试文件
            main_file = os.path.join(test_dir, "main.py")
            with open(main_file, "w") as f:
                f.write("print('Hello')")

            other_file = os.path.join(test_dir, "other.py")
            with open(other_file, "w") as f:
                f.write("print('Other')")

            # 测试查找主文件
            found_file = find_main_file(test_dir)
            assert found_file == main_file

            # 测试自定义关键词
            found_file = find_main_file(test_dir, keywords=["other"])
            assert found_file == other_file

        finally:
            # 清理测试目录
            cleanup(test_dir)

    @pytest.mark.parametrize("test_dir_exist", [True, False])
    def test_cleanup(self, test_dir_exist):
        """测试清理功能"""
        if test_dir_exist:
            test_dir = tempfile.mkdtemp()
            cleanup(test_dir)
            assert not os.path.exists(test_dir)
        else:
            # 测试清理不存在的目录不会报错
            non_existent_dir = "/tmp/non_existent_dir_12345"
            if os.path.exists(non_existent_dir):
                os.rmdir(non_existent_dir)

            cleanup(non_existent_dir)  # 不应该抛出异常
