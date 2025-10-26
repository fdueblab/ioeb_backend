"""
端口分配工具模块
提供端口可用性检测和分配功能
"""

import subprocess
import threading
from typing import List, Set

# 端口分配锁，防止并发冲突
_port_lock = threading.Lock()


class PortAllocationError(Exception):
    """端口分配错误"""
    pass


def get_used_ports_from_docker() -> Set[int]:
    """
    从Docker容器获取已占用的端口
    
    Returns:
        Set[int]: 已占用的端口集合
    """
    used_ports = set()
    
    try:
        # 获取所有容器的端口映射
        result = subprocess.run(
            ['docker', 'ps', '-a', '--format', '{{.Ports}}'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            # 解析输出，格式如: 0.0.0.0:27001->8000/tcp, :::27001->8000/tcp
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                
                # 分割多个端口映射
                for mapping in line.split(','):
                    mapping = mapping.strip()
                    if '->' in mapping:
                        # 提取宿主机端口
                        host_part = mapping.split('->')[0].strip()
                        if ':' in host_part:
                            port_str = host_part.split(':')[-1]
                            try:
                                port = int(port_str)
                                used_ports.add(port)
                            except ValueError:
                                continue
    except Exception as e:
        print(f"获取Docker端口信息失败: {str(e)}")
    
    return used_ports


def is_port_available(port: int) -> bool:
    """
    检测端口是否可用
    
    Args:
        port: 端口号
        
    Returns:
        bool: 端口是否可用
    """
    used_ports = get_used_ports_from_docker()
    return port not in used_ports


def allocate_ports(count: int, start_port: int = 27000, end_port: int = 28000) -> List[int]:
    """
    分配可用端口（线程安全）
    
    Args:
        count: 需要分配的端口数量
        start_port: 起始端口（默认27000）
        end_port: 结束端口（默认28000）
        
    Returns:
        List[int]: 分配的端口列表
        
    Raises:
        PortAllocationError: 无法分配足够的端口
    """
    with _port_lock:
        allocated = []
        used_ports = get_used_ports_from_docker()
        
        current_port = start_port
        while len(allocated) < count and current_port < end_port:
            if current_port not in used_ports:
                allocated.append(current_port)
            current_port += 1
        
        if len(allocated) < count:
            raise PortAllocationError(
                f"无法分配 {count} 个端口，范围 {start_port}-{end_port}，"
                f"已占用端口: {sorted(list(used_ports))}"
            )
        
        return allocated

