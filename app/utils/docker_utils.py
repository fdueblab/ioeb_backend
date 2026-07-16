"""
Docker部署工具模块
提供docker-compose配置修改和容器部署功能
"""

import os
import subprocess
import time
import yaml
import requests
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


def wait_for_mcp_sse_ready(
    readiness_url: str,
    timeout: int = 120,
    interval: float = 2.0
) -> Tuple[bool, str]:
    """等待 MCP SSE 端点真正开始提供事件流。"""
    deadline = time.monotonic() + timeout
    last_error = "尚未收到有效响应"

    while True:
        try:
            response = requests.get(
                readiness_url,
                stream=True,
                timeout=(3, 5)
            )
            try:
                content_type = response.headers.get('Content-Type', '').lower()
                if response.status_code == 200 and 'text/event-stream' in content_type:
                    message_endpoint = _read_mcp_message_endpoint(response)
                    if message_endpoint:
                        return True, (
                            f"MCP SSE端点已就绪: {readiness_url}，"
                            f"消息端点: {message_endpoint}"
                        )
                    last_error = "SSE连接成功，但未收到MCP endpoint事件"
                else:
                    last_error = (
                        f"HTTP {response.status_code}, "
                        f"Content-Type={content_type or 'unknown'}"
                    )
            finally:
                response.close()
        except requests.RequestException as exc:
            last_error = str(exc)

        if time.monotonic() >= deadline:
            return False, f"等待MCP SSE端点超时（{timeout}秒）: {last_error}"
        time.sleep(interval)


def _read_mcp_message_endpoint(response) -> str:
    """读取 FastMCP 建连后发送的首个 ``endpoint`` SSE 事件。"""
    event_name = ""
    data_lines = []
    for line in response.iter_lines(chunk_size=1, decode_unicode=True):
        if isinstance(line, bytes):
            line = line.decode("utf-8", errors="replace")
        if line == "":
            if event_name == "endpoint" and data_lines:
                endpoint = "\n".join(data_lines).strip()
                if endpoint.startswith("/"):
                    return endpoint
            event_name = ""
            data_lines = []
            continue
        if line.startswith("event:"):
            event_name = line[6:].strip()
        elif line.startswith("data:"):
            data_lines.append(line[5:].lstrip())
    return ""


def _get_compose_logs(
    compose_file: str,
    project_name: str,
    project_root: str
) -> str:
    """读取有限长度的容器日志，便于定位启动失败原因。"""
    try:
        result = subprocess.run(
            [
                'docker-compose', '-f', compose_file, '-p', project_name,
                'logs', '--no-color', '--tail', '100'
            ],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=30
        )
        return (result.stdout or result.stderr or '').strip()
    except Exception as exc:
        return f"读取容器日志失败: {str(exc)}"


def deploy_service(
    project_root: str,
    service_id: str,
    timeout: int = 600,
    readiness_url: str = None,
    readiness_timeout: int = 120
) -> Tuple[bool, str]:
    """
    使用docker-compose部署服务
    
    Args:
        project_root: 项目根目录路径（包含docker-compose.yml）
        service_id: 服务ID
        timeout: 超时时间（秒），默认600秒（10分钟）
        readiness_url: 可选的MCP SSE就绪检查地址
        readiness_timeout: MCP SSE就绪检查超时时间（秒）
        
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
        time.sleep(5)
        
        # 检查容器状态
        check_result = subprocess.run(
            ['docker-compose', '-f', compose_file, '-p', project_name, 'ps'],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # 容器进程必须先处于运行状态
        if check_result.returncode == 0 and 'Up' in check_result.stdout:
            if readiness_url:
                ready, message = wait_for_mcp_sse_ready(
                    readiness_url,
                    timeout=readiness_timeout
                )
                if not ready:
                    logs = _get_compose_logs(compose_file, project_name, project_root)
                    if logs:
                        message = f"{message}\n容器日志:\n{logs}"
                    return False, message
                return True, f"服务部署成功，容器运行中；{message}"
            return True, "服务部署成功，容器运行中"

        logs = _get_compose_logs(compose_file, project_name, project_root)
        return False, f"容器启动失败，状态: {check_result.stdout}\n容器日志:\n{logs}"
        
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
