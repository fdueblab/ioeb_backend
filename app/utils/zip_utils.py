"""
ZIP文件处理工具模块
提供ZIP文件解压和项目根目录查找功能
"""

import os
import zipfile
import shutil
from typing import Optional


class ZipProcessError(Exception):
    """ZIP处理错误"""
    pass


def extract_and_find_root(zip_path: str, extract_to: str) -> str:
    """
    解压ZIP文件并找到包含docker-compose.yml的项目根目录
    
    Args:
        zip_path: ZIP文件路径
        extract_to: 解压目标目录
        
    Returns:
        str: 项目根目录的绝对路径
        
    Raises:
        ZipProcessError: 解压失败或找不到必需文件
    """
    # 确保目标目录存在
    os.makedirs(extract_to, exist_ok=True)
    
    try:
        # 解压ZIP
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 安全检查：防止路径遍历攻击
            for name in zip_ref.namelist():
                # 检查是否包含危险路径
                if name.startswith('/') or '..' in name:
                    raise ZipProcessError(f"ZIP文件包含不安全的路径: {name}")
            
            # 解压所有文件
            zip_ref.extractall(extract_to)
        
        # 查找包含 docker-compose.yml 的目录
        project_root = find_docker_compose_dir(extract_to)
        
        if not project_root:
            raise ZipProcessError("ZIP文件中未找到 docker-compose.yml")
        
        return project_root
        
    except zipfile.BadZipFile:
        raise ZipProcessError("无效的ZIP文件")
    except Exception as e:
        if isinstance(e, ZipProcessError):
            raise
        raise ZipProcessError(f"解压ZIP文件失败: {str(e)}")


def find_docker_compose_dir(base_path: str) -> Optional[str]:
    """
    在指定路径下查找包含 docker-compose.yml 的目录
    
    Args:
        base_path: 基础搜索路径
        
    Returns:
        Optional[str]: 找到的目录路径，未找到返回None
    """
    for root, dirs, files in os.walk(base_path):
        if 'docker-compose.yml' in files:
            return root
    return None


def cleanup_directory(directory: str) -> bool:
    """
    清理指定目录
    
    Args:
        directory: 要删除的目录路径
        
    Returns:
        bool: 是否成功删除
    """
    try:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            return True
        return False
    except Exception as e:
        print(f"清理目录失败 {directory}: {str(e)}")
        return False


def get_zip_root_folder_name(zip_path: str) -> Optional[str]:
    """
    获取ZIP文件解压后的根文件夹名称（不实际解压）
    
    Args:
        zip_path: ZIP文件路径
        
    Returns:
        Optional[str]: 根文件夹名称，如果无法确定则返回None
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 获取所有文件名
            names = zip_ref.namelist()
            if not names:
                return None
            
            # 找到第一级目录
            first_name = names[0]
            if '/' in first_name:
                return first_name.split('/')[0]
            
            return None
    except Exception:
        return None

