"""
清理工具模块
提供Docker容器、镜像、网络和服务文件的清理功能
"""

import os
import subprocess
import shutil
from typing import Dict, List


class CleanupError(Exception):
    """清理错误"""
    pass


def get_service_containers() -> List[str]:
    """
    获取所有通过upload功能部署的服务容器ID
    
    Returns:
        List[str]: 容器ID列表
    """
    container_ids = []
    
    try:
        # 获取所有容器，筛选出project名称以svc_开头的
        result = subprocess.run(
            ['docker', 'ps', '-a', '--format', '{{.ID}}:{{.Label "com.docker.compose.project"}}'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                
                parts = line.split(':')
                if len(parts) == 2:
                    container_id, project_name = parts
                    # 筛选出 svc_ 开头的项目
                    if project_name.startswith('svc_'):
                        container_ids.append(container_id)
        
        return container_ids
        
    except Exception as e:
        print(f"获取服务容器失败: {str(e)}")
        return []


def get_service_networks() -> List[str]:
    """
    获取所有服务相关的Docker网络
    
    Returns:
        List[str]: 网络名称列表
    """
    networks = []
    
    try:
        # 获取所有网络
        result = subprocess.run(
            ['docker', 'network', 'ls', '--format', '{{.Name}}'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            for network_name in result.stdout.strip().split('\n'):
                # 筛选出 svc_ 开头的网络
                if network_name.startswith('svc_'):
                    networks.append(network_name)
        
        return networks
        
    except Exception as e:
        print(f"获取服务网络失败: {str(e)}")
        return []


def get_service_images() -> List[str]:
    """
    获取所有服务相关的Docker镜像
    
    Returns:
        List[str]: 镜像ID列表
    """
    image_ids = []
    
    try:
        # 先获取所有 svc_ 开头的容器使用的镜像
        result = subprocess.run(
            ['docker', 'ps', '-a', '--format', '{{.Image}}:{{.Label "com.docker.compose.project"}}'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            service_images = set()
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                
                parts = line.split(':')
                if len(parts) >= 2:
                    image_name = parts[0]
                    project_name = parts[1]
                    
                    if project_name.startswith('svc_'):
                        service_images.add(image_name)
            
            # 获取这些镜像的ID
            for image_name in service_images:
                img_result = subprocess.run(
                    ['docker', 'images', '-q', image_name],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if img_result.returncode == 0 and img_result.stdout.strip():
                    image_ids.append(img_result.stdout.strip())
        
        return image_ids
        
    except Exception as e:
        print(f"获取服务镜像失败: {str(e)}")
        return []


def cleanup_docker_resources(delete_images: bool = False) -> Dict[str, any]:
    """
    清理Docker资源（容器、网络、镜像）
    
    Args:
        delete_images: 是否删除镜像（默认False，因为镜像可能被其他容器使用）
        
    Returns:
        Dict: 清理结果统计
    """
    result = {
        'containers_removed': 0,
        'containers_failed': 0,
        'networks_removed': 0,
        'networks_failed': 0,
        'images_removed': 0,
        'images_failed': 0,
        'errors': []
    }
    
    # 1. 停止并删除容器
    print("🔄 开始清理服务容器...")
    container_ids = get_service_containers()
    print(f"找到 {len(container_ids)} 个服务容器")
    
    for container_id in container_ids:
        try:
            # 停止容器
            subprocess.run(
                ['docker', 'stop', container_id],
                capture_output=True,
                timeout=30
            )
            
            # 删除容器
            rm_result = subprocess.run(
                ['docker', 'rm', '-f', container_id],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if rm_result.returncode == 0:
                result['containers_removed'] += 1
                print(f"✅ 删除容器: {container_id}")
            else:
                result['containers_failed'] += 1
                error_msg = f"删除容器失败 {container_id}: {rm_result.stderr}"
                result['errors'].append(error_msg)
                print(f"❌ {error_msg}")
                
        except Exception as e:
            result['containers_failed'] += 1
            error_msg = f"处理容器失败 {container_id}: {str(e)}"
            result['errors'].append(error_msg)
            print(f"❌ {error_msg}")
    
    # 2. 删除网络
    print("\n🔄 开始清理服务网络...")
    networks = get_service_networks()
    print(f"找到 {len(networks)} 个服务网络")
    
    for network_name in networks:
        try:
            net_result = subprocess.run(
                ['docker', 'network', 'rm', network_name],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if net_result.returncode == 0:
                result['networks_removed'] += 1
                print(f"✅ 删除网络: {network_name}")
            else:
                result['networks_failed'] += 1
                error_msg = f"删除网络失败 {network_name}: {net_result.stderr}"
                result['errors'].append(error_msg)
                print(f"❌ {error_msg}")
                
        except Exception as e:
            result['networks_failed'] += 1
            error_msg = f"处理网络失败 {network_name}: {str(e)}"
            result['errors'].append(error_msg)
            print(f"❌ {error_msg}")
    
    # 3. 删除镜像（可选）
    if delete_images:
        print("\n🔄 开始清理服务镜像...")
        image_ids = get_service_images()
        print(f"找到 {len(image_ids)} 个服务镜像")
        
        for image_id in image_ids:
            try:
                img_result = subprocess.run(
                    ['docker', 'rmi', '-f', image_id],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if img_result.returncode == 0:
                    result['images_removed'] += 1
                    print(f"✅ 删除镜像: {image_id}")
                else:
                    result['images_failed'] += 1
                    error_msg = f"删除镜像失败 {image_id}: {img_result.stderr}"
                    result['errors'].append(error_msg)
                    print(f"❌ {error_msg}")
                    
            except Exception as e:
                result['images_failed'] += 1
                error_msg = f"处理镜像失败 {image_id}: {str(e)}"
                result['errors'].append(error_msg)
                print(f"❌ {error_msg}")
    
    return result


def cleanup_service_files(base_path: str = '/app/data/services') -> Dict[str, any]:
    """
    清理服务文件目录
    
    Args:
        base_path: 服务文件基础路径
        
    Returns:
        Dict: 清理结果
    """
    result = {
        'directories_removed': 0,
        'directories_failed': 0,
        'errors': []
    }
    
    print(f"\n🔄 开始清理服务文件: {base_path}")
    
    if not os.path.exists(base_path):
        print(f"⚠️  服务目录不存在: {base_path}")
        return result
    
    try:
        # 列出所有服务目录
        service_dirs = [d for d in os.listdir(base_path) 
                       if os.path.isdir(os.path.join(base_path, d))]
        
        print(f"找到 {len(service_dirs)} 个服务目录")
        
        for service_dir in service_dirs:
            service_path = os.path.join(base_path, service_dir)
            try:
                shutil.rmtree(service_path)
                result['directories_removed'] += 1
                print(f"✅ 删除目录: {service_dir}")
            except Exception as e:
                result['directories_failed'] += 1
                error_msg = f"删除目录失败 {service_dir}: {str(e)}"
                result['errors'].append(error_msg)
                print(f"❌ {error_msg}")
        
    except Exception as e:
        error_msg = f"清理服务文件失败: {str(e)}"
        result['errors'].append(error_msg)
        print(f"❌ {error_msg}")
    
    return result

