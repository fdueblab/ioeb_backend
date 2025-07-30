"""
密码加密工具
提供密码加密和验证功能
"""

import hashlib


def hash_password(password: str) -> str:
    """
    使用SHA256对密码进行加密
    
    Args:
        password: 明文密码
        
    Returns:
        str: SHA256加密后的密码哈希值
    """
    if not password:
        raise ValueError("密码不能为空")
    
    # 使用SHA256进行加密
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    """
    验证密码是否正确
    
    Args:
        password: 明文密码
        hashed_password: 数据库中存储的加密密码
        
    Returns:
        bool: 密码是否匹配
    """
    if not password or not hashed_password:
        return False
    
    # 对输入的密码进行加密，然后与存储的哈希值比较
    return hash_password(password) == hashed_password 