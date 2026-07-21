"""
Docker部署工具模块
提供docker-compose配置修改和容器部署功能
"""

import os
import subprocess
import yaml
from typing import List, Tuple


class DockerDeployError(Exception):
    """Docker部署错误"""
    pass


def parse_ports_from_compose(compose_file_path: str) -> List[str]:
    """
    从docker-compose.yml中解析端口映射
    
    Args:
        compose_file_path: docker-compose.yml文件路径
        
    Returns:
        List[str]: 容器端口列表，如 ["8000", "3306"]
        
    Raises:
        DockerDeployError: 解析失败
    """
    try:
        with open(compose_file_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        container_ports = []
        services = config.get('services', {})
        
        if not services:
            return container_ports
        
        # 假设只有一个service，取第一个
        service_name = list(services.keys())[0]
        service_config = services[service_name]
        
        if 'ports' in service_config:
            ports = service_config['ports']
            for port_def in ports:
                if isinstance(port_def, str):
                    # "8000:8000" 或 "8000" 格式
                    if ':' in port_def:
                        parts = port_def.split(':')
                        container_port = parts[-1].split('/')[0]  # 去除/tcp等协议后缀
                    else:
                        container_port = port_def.split('/')[0]
                    container_ports.append(container_port)
                elif isinstance(port_def, dict):
                    # 长格式 {target: 8000, published: 8000}
                    container_port = str(port_def.get('target', ''))
                    if container_port:
                        container_ports.append(container_port)
        
        return container_ports
        
    except Exception as e:
        raise DockerDeployError(f"解析docker-compose.yml失败: {str(e)}")


def modify_compose_ports(compose_file_path: str, allocated_ports: List[int]) -> List[str]:
    """
    修改docker-compose.yml的端口映射
    
    Args:
        compose_file_path: docker-compose.yml文件路径
        allocated_ports: 分配的宿主机端口列表
        
    Returns:
        List[str]: 端口映射列表，格式 ["27001:8000", "27002:3306"]
        
    Raises:
        DockerDeployError: 修改失败
    """
    try:
        with open(compose_file_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        port_mappings = []
        services = config.get('services', {})
        
        if not services:
            raise DockerDeployError("docker-compose.yml中没有定义services")
        
        # 假设只有一个service
        service_name = list(services.keys())[0]
        service_config = services[service_name]
        
        if 'ports' not in service_config:
            raise DockerDeployError("docker-compose.yml中没有定义ports")
        
        ports = service_config['ports']
        new_ports = []
        
        for i, port_def in enumerate(ports):
            if i >= len(allocated_ports):
                # 端口不够分配（理论上不会发生，因为已经预先分配了）
                break
            
            allocated_port = allocated_ports[i]
            
            # 解析原端口映射
            if isinstance(port_def, str):
                # "8000:8000" 或 "127.0.0.1:8000:8000" 格式
                if ':' in port_def:
                    parts = port_def.split(':')
                    # 取最后一部分作为容器端口
                    container_port = parts[-1]
                else:
                    container_port = port_def
                
                new_mapping = f"{allocated_port}:{container_port}"
                new_ports.append(new_mapping)
                port_mappings.append(new_mapping)
                
            elif isinstance(port_def, dict):
                # 长格式
                container_port = port_def.get('target')
                if container_port:
                    new_ports.append({
                        'target': container_port,
                        'published': allocated_port,
                        'protocol': port_def.get('protocol', 'tcp')
                    })
                    port_mappings.append(f"{allocated_port}:{container_port}")
        
        service_config['ports'] = new_ports
        
        # 移除 container_name 字段，让 Docker Compose 自动生成容器名称
        # 这样可以避免不同用户上传相同容器名称时的冲突
        # 容器名称会自动变成: {project_name}_{service_name}_{index}
        if 'container_name' in service_config:
            del service_config['container_name']
            print(f"已移除 container_name 字段，容器名称将自动生成为: svc_{service_name}_*")
        
        # 移除 volumes 配置，禁止用户服务进行挂载操作（安全考虑）
        if 'volumes' in service_config:
            removed_volumes = service_config['volumes']
            del service_config['volumes']
            print(f"⚠️ 已移除 volumes 配置（安全限制）: {removed_volumes}")
        
        # 移除顶层的 volumes 定义（命名卷声明）
        if 'volumes' in config:
            removed_volume_definitions = list(config['volumes'].keys())
            del config['volumes']
            print(f"⚠️ 已移除顶层 volumes 定义（安全限制）: {removed_volume_definitions}")
        
        # 写回文件
        with open(compose_file_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        
        return port_mappings
        
    except Exception as e:
        if isinstance(e, DockerDeployError):
            raise
        raise DockerDeployError(f"修改docker-compose.yml失败: {str(e)}")


def deploy_service(project_root: str, service_id: str, timeout: int = 600) -> Tuple[bool, str]:
    """
    使用docker-compose部署服务
    
    Args:
        project_root: 项目根目录路径（包含docker-compose.yml）
        service_id: 服务ID
        timeout: 超时时间（秒），默认600秒（10分钟）
        
    Returns:
        Tuple[bool, str]: (是否成功, 错误信息或成功信息)
    """
    compose_file = os.path.join(project_root, 'docker-compose.yml')
    # 使用缩短的project name，避免网络名称过长
    project_name = f"svc_{service_id[:8]}"
    
    if not os.path.exists(compose_file):
        return False, f"docker-compose.yml不存在: {compose_file}"
    
    try:
        # 执行 docker-compose up -d
        result = subprocess.run(
            ['docker-compose', '-f', compose_file, '-p', project_name, 'up', '-d'],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout
            return False, f"docker-compose up 失败: {error_msg}"
        
        # 等待容器启动
        import time
        time.sleep(5)
        
        # 检查容器状态
        check_result = subprocess.run(
            ['docker-compose', '-f', compose_file, '-p', project_name, 'ps'],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # 简单判断：输出中包含 "Up" 表示成功
        if check_result.returncode == 0 and 'Up' in check_result.stdout:
            return True, f"服务部署成功，容器运行中"
        
        return False, f"容器启动失败，状态: {check_result.stdout}"
        
    except subprocess.TimeoutExpired:
        return False, f"docker-compose执行超时（{timeout}秒）"
    except FileNotFoundError:
        return False, "docker-compose命令不存在，请确保已安装docker-compose"
    except Exception as e:
        return False, f"部署异常: {str(e)}"


def stop_and_remove_service(project_root: str, service_id: str) -> bool:
    """
    停止并删除服务容器
    
    Args:
        project_root: 项目根目录路径
        service_id: 服务ID
        
    Returns:
        bool: 是否成功
    """
    compose_file = os.path.join(project_root, 'docker-compose.yml')
    # 使用缩短的project name，与部署时保持一致
    project_name = f"svc_{service_id[:8]}"
    
    if not os.path.exists(compose_file):
        print(f"docker-compose.yml不存在: {compose_file}")
        return False
    
    try:
        result = subprocess.run(
            ['docker-compose', '-f', compose_file, '-p', project_name, 'down', '-v'],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"停止容器失败: {str(e)}")
        return False

