"""
微服务服务模块
处理微服务相关的业务逻辑
"""

import re
from typing import Dict, List, Optional, Tuple
import threading
import time
import os
import tempfile

from werkzeug.utils import secure_filename

from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.datastructures import FileStorage

from app.repositories.service_repository import ServiceRepository
from app.extensions import db
from app.models.service.upgrade_advice import ServiceUpgradeAdvice
from app.utils.port_utils import allocate_ports, PortAllocationError
from app.utils.zip_utils import extract_and_find_root, cleanup_directory, ZipProcessError
from app.utils.mcp_artifact_utils import load_mcp_artifact_metadata
from app.utils.docker_utils import (
    parse_ports_from_compose,
    modify_compose_ports,
    deploy_service as docker_deploy,
    stop_and_remove_service,
    DockerDeployError
)
from app.utils.cleanup_utils import (
    cleanup_docker_resources,
    cleanup_service_files
)
from app.services.meta_app_config import (
    ARTIFACT_SCHEMA,
    DEPLOYABLE_STATUSES,
    STOPPABLE_STATUSES,
)


class ServiceServiceError(Exception):
    """微服务服务错误"""


class ServiceService:
    """微服务服务类"""

    def __init__(self):
        """初始化微服务服务"""
        self.service_repository = ServiceRepository()

    def _is_deploy_still_active(self, service_id: str) -> bool:
        service = self.service_repository.get_service_by_id(service_id)
        return service is not None and service.status == "deploying"

    def get_all_services(self) -> List[Dict]:
        """
        获取所有微服务

        Returns:
            List[Dict]: 微服务列表，每个微服务以字典形式表示
        """
        try:
            return self.service_repository.get_all_services_with_dict()
        except Exception as e:
            raise ServiceServiceError(f"获取微服务列表失败: {str(e)}")

    def get_service_by_id(self, service_id: str) -> Dict:
        """
        根据ID获取微服务

        Args:
            service_id: 微服务ID

        Returns:
            Dict: 微服务信息字典

        Raises:
            ServiceServiceError: 微服务不存在时抛出
        """
        try:
            service_dict = self.service_repository.get_service_dict_by_id(service_id)
            if not service_dict:
                raise ServiceServiceError(f"微服务ID {service_id} 不存在")
            return service_dict
        except Exception as e:
            if isinstance(e, ServiceServiceError):
                raise
            raise ServiceServiceError(f"获取微服务失败: {str(e)}")

    def get_services_by_ids(self, service_ids: List[str]) -> Tuple[List[Dict], List[str]]:
        """
        根据ID列表批量获取微服务

        Args:
            service_ids: 微服务ID列表

        Returns:
            Tuple[List[Dict], List[str]]: 
                - 第一个元素：成功获取的微服务字典列表，按输入ID顺序返回
                - 第二个元素：不存在的微服务ID列表

        Raises:
            ServiceServiceError: 获取过程中出错
        """
        if not service_ids:
            return [], []
        
        # 去重并保持顺序
        unique_ids = []
        seen = set()
        for service_id in service_ids:
            if service_id not in seen:
                unique_ids.append(service_id)
                seen.add(service_id)
        
        try:
            # 使用仓库层批量获取服务
            services = self.service_repository.get_services_dict_by_ids(unique_ids)
            
            # 找出成功获取的服务ID
            found_ids = {service['id'] for service in services}
            
            # 找出不存在的服务ID
            not_found_ids = [service_id for service_id in unique_ids if service_id not in found_ids]
            
            return services, not_found_ids
        except Exception as e:
            raise ServiceServiceError(f"批量获取微服务失败: {str(e)}")

    def get_services_by_attribute(self, attribute: str) -> List[Dict]:
        """
        根据属性获取微服务列表

        Args:
            attribute: 微服务属性

        Returns:
            List[Dict]: 符合条件的微服务列表
        """
        try:
            services = self.service_repository.find_by_attribute(attribute)
            return [service.to_dict(include_artifact=False) for service in services]
        except Exception as e:
            raise ServiceServiceError(f"查询微服务失败: {str(e)}")

    def create_service(self, service_data: Dict) -> Dict:
        """
        创建新微服务

        Args:
            service_data: 包含微服务信息的字典，应包括:
                - name: 服务名称
                - attribute: 服务属性
                - type: 服务类型
                - domain: 领域
                - industry: 行业
                - scenario: 场景
                - technology: 技术
                - network: 网络类型
                - port: 端口映射
                - volume: 数据卷映射
                - status: 服务状态
                - number: 服务编号
                - norm: 规范评分列表 (可选)
                - source: 来源信息 (可选)
                - apiList: API列表 (可选)

        Returns:
            Dict: 创建的微服务信息

        Raises:
            ServiceServiceError: 创建过程中出错
        """
        if not service_data.get("name"):
            raise ServiceServiceError("服务名称不能为空")

        try:
            # 使用仓库层创建服务及其关联数据
            service = self.service_repository.create_service_with_relations(service_data)
            return service.to_dict()
        except SQLAlchemyError as e:
            raise ServiceServiceError(f"创建微服务失败: {str(e)}")
        except Exception as e:
            raise ServiceServiceError(f"创建微服务过程中出错: {str(e)}")

    def validate_meta_app_prepublish(self, service_data: Dict) -> None:
        apis = service_data.get("apiList")
        if not isinstance(apis, list) or len(apis) != 1 or not isinstance(apis[0], dict):
            raise ServiceServiceError("元应用必须包含且仅包含一个API配置")
        api = apis[0]
        artifact = api.get("metaAppArtifact")
        if not isinstance(artifact, dict):
            raise ServiceServiceError("元应用缺少Artifact")
        if artifact.get("schemaVersion") != ARTIFACT_SCHEMA:
            raise ServiceServiceError("Artifact Schema必须为meta_app_artifact.v1")
        if api.get("metaAppArtifactId") != artifact.get("artifactId"):
            raise ServiceServiceError("Artifact ID不一致")
        if not api.get("simulationBuildId"):
            raise ServiceServiceError("元应用缺少simulationBuildId")
        if not isinstance(api.get("runtimeSpec"), dict):
            raise ServiceServiceError("元应用缺少runtimeSpec")

    def update_service(self, service_id: str, service_data: Dict) -> Dict:
        """
        更新微服务信息

        Args:
            service_id: 微服务ID
            service_data: 更新的微服务数据

        Returns:
            Dict: 更新后的微服务信息

        Raises:
            ServiceServiceError: 更新过程中出错
        """
        try:
            # 检查服务是否存在
            service = self.service_repository.get_service_by_id(service_id)
            if not service:
                raise ServiceServiceError(f"微服务ID {service_id} 不存在")
            target_type = service_data.get("type", service.type)
            if (service.type == "meta") != (target_type == "meta"):
                raise ServiceServiceError("不允许通过更新接口切换元应用类型")
            if service.type == "meta" and "apiList" in service_data:
                apis = service_data["apiList"]
                if not isinstance(apis, list) or len(apis) != 1 or not isinstance(apis[0], dict):
                    raise ServiceServiceError("元应用必须包含且仅包含一个API配置")
            
            # 使用仓库层更新服务及其关联数据
            updated_service = self.service_repository.update_service_with_relations(service_id, service_data)
            return updated_service.to_dict()
        except SQLAlchemyError as e:
            raise ServiceServiceError(f"更新微服务失败: {str(e)}")
        except Exception as e:
            if isinstance(e, ServiceServiceError):
                raise
            raise ServiceServiceError(f"更新微服务过程中出错: {str(e)}")

    def delete_service(self, service_id: str) -> bool:
        """
        删除微服务（软删除）

        Args:
            service_id: 微服务ID

        Returns:
            bool: 是否删除成功

        Raises:
            ServiceServiceError: 删除过程中出错
        """
        try:
            # 检查服务是否存在
            service = self.service_repository.get_service_by_id(service_id)
            if not service:
                raise ServiceServiceError(f"微服务ID {service_id} 不存在")
            
            # 使用仓库层删除服务
            success = self.service_repository.delete_service(service_id)
            if not success:
                raise ServiceServiceError(f"删除微服务失败")
            return True
        except Exception as e:
            if isinstance(e, ServiceServiceError):
                raise
            raise ServiceServiceError(f"删除微服务失败: {str(e)}")

    def search_services(self, keyword: str) -> List[Dict]:
        """
        搜索微服务

        Args:
            keyword: 搜索关键词，匹配服务名称

        Returns:
            List[Dict]: 符合条件的微服务列表
        """
        try:
            services = self.service_repository.search_by_keyword(keyword)
            return [service.to_dict(include_artifact=False) for service in services]
        except Exception as e:
            raise ServiceServiceError(f"搜索微服务失败: {str(e)}")

    @staticmethod
    def _normalize_search_text(value) -> str:
        return str(value or "").strip().lower()

    @classmethod
    def _extract_smart_search_terms(cls, **fields) -> List[str]:
        raw = " ".join(str(fields.get(key) or "") for key in ("name", "description", "role", "function", "requirement"))
        parts = re.split(r"[\s,，;；、。.!！?？/\\|]+", raw)
        terms = []
        seen = set()
        for part in parts:
            term = cls._normalize_search_text(part)
            if term and term not in seen:
                seen.add(term)
                terms.append(term)
        return terms

    @classmethod
    def _build_service_search_text(cls, service) -> Dict[str, str]:
        api_chunks = []
        for api in service.apis or []:
            api_chunks.extend([api.name or "", api.des or ""])
            for tool in api.tools or []:
                api_chunks.extend([tool.name or "", tool.description or ""])

        source = service.source
        source_chunks = []
        if source:
            source_chunks = [
                source.ms_introduce or "",
                source.company_introduce or "",
                source.company_name or "",
            ]

        name = cls._normalize_search_text(service.name)
        description = cls._normalize_search_text(" ".join(source_chunks + api_chunks))
        metadata = cls._normalize_search_text(
            " ".join(
                [
                    service.attribute or "",
                    service.type or "",
                    service.industry or "",
                    service.scenario or "",
                    service.technology or "",
                    service.status or "",
                ]
            )
        )
        return {
            "name": name,
            "description": description,
            "metadata": metadata,
            "all": f"{name} {description} {metadata}",
        }

    @classmethod
    def _score_service_for_smart_search(cls, service, terms: List[str]) -> int:
        text = cls._build_service_search_text(service)
        if not all(term in text["all"] for term in terms):
            return 0
        score = 0
        for term in terms:
            if term in text["name"]:
                score += 8
            if term in text["description"]:
                score += 5
            if term in text["metadata"]:
                score += 3
            score += 1
        return score

    def smart_search(
        self,
        domain: str,
        *,
        name: str = "",
        description: str = "",
        role: str = "",
        function: str = "",
        requirement: str = "",
    ) -> List[Dict]:
        """
        领域内智能检索：将 5 个表单字段拆词后，对现有文本字段做全表模糊匹配。

        说明：role / function / requirement 在库中无独立列，仅作为检索词参与匹配。
        """
        if not domain or not str(domain).strip():
            raise ServiceServiceError("domain 不能为空")
        terms = self._extract_smart_search_terms(
            name=name,
            description=description,
            role=role,
            function=function,
            requirement=requirement,
        )
        if not terms:
            raise ServiceServiceError("请至少填写一个检索条件")

        try:
            services = self.service_repository.list_services_in_domain(str(domain).strip())
            ranked = []
            for service in services:
                score = self._score_service_for_smart_search(service, terms)
                if score > 0:
                    ranked.append((score, service))
            ranked.sort(key=lambda item: (-item[0], -(item[1].create_time or 0)))
            return [service.to_list_dict() for _, service in ranked]
        except ServiceServiceError:
            raise
        except Exception as e:
            raise ServiceServiceError(f"智能检索失败: {str(e)}")

    def filter_services(
        self, page: int = None, page_size: int = None, **filters
    ) -> Dict:
        """
        根据条件筛选微服务（列表视图，可选分页）。

        Args:
            page: 页码（从 1 开始）；与 page_size 同时传入时启用分页
            page_size: 每页条数（最大 100）
            **filters: 筛选条件

        Returns:
            Dict: services, total, page, pageSize
        """
        try:
            services, total = self.service_repository.filter_services(
                page=page, page_size=page_size, **filters
            )
            return {
                "services": [service.to_list_dict() for service in services],
                "total": total,
                "page": page,
                "pageSize": page_size,
            }
        except Exception as e:
            raise ServiceServiceError(f"筛选微服务失败: {str(e)}")

    def get_mcp_options(self, domain: str) -> List[Dict]:
        """仿真构建 MCP 服务选择器：返回含 tools 的精简选项列表。"""
        if not domain or not str(domain).strip():
            raise ServiceServiceError("domain 不能为空")
        try:
            services = self.service_repository.list_mcp_options(str(domain).strip())
            options = []
            for service in services:
                api = service.apis[0] if service.apis else None
                tools = []
                if api and api.tools:
                    for tool in api.tools:
                        item = tool.to_dict()
                        item["des"] = item.get("description") or ""
                        tools.append(item)
                options.append({
                    "id": service.id,
                    "name": service.name,
                    "status": service.status,
                    "des": (api.des if api else "") or "",
                    "url": (api.url if api else "") or "",
                    "method": (api.method if api else "sse") or "sse",
                    "isFake": bool(api.is_fake) if api else False,
                    "tools": tools,
                })
            return options
        except ServiceServiceError:
            raise
        except Exception as e:
            raise ServiceServiceError(f"获取 MCP 服务选项失败: {str(e)}")

    def deploy_service(self, service_id: str) -> bool:
        """
        部署微服务

        Args:
            service_id: 微服务ID

        Returns:
            bool: 是否成功启动部署

        Raises:
            ServiceServiceError: 部署过程中出错
        """
        try:
            # 检查服务是否存在
            service = self.service_repository.get_service_by_id(service_id)
            if not service:
                raise ServiceServiceError(f"微服务ID {service_id} 不存在")
            
            # 检查服务状态是否允许部署
            if service.status == "deploying":
                raise ServiceServiceError("微服务正在部署中，请稍后再试")
            if service.status not in DEPLOYABLE_STATUSES:
                raise ServiceServiceError(f"当前状态 {service.status} 不允许部署")
            
            # 先设置状态为部署中
            self.service_repository.update_service_status(service_id, "deploying")
            service_type = service.type
            
            # 获取当前Flask应用实例
            app = current_app._get_current_object()
            
            # 启动异步部署任务
            def deploy_task():
                with app.app_context():
                    try:
                        # 原型阶段仅模拟部署状态推进
                        time.sleep(current_app.config.get("META_APP_DEPLOY_DELAY_SECONDS", 10))
                        
                        if not self._is_deploy_still_active(service_id):
                            return

                        target_status = (
                            "pre_release_pending"
                            if service_type == "meta"
                            else "pre_release_unrated"
                        )
                        self.service_repository.update_service_status(service_id, target_status)
                        print(f"服务 {service_id} 部署成功")
                    except Exception as e:
                        if self._is_deploy_still_active(service_id):
                            self.service_repository.update_service_status(service_id, "error")
                            print(f"服务 {service_id} 部署失败: {str(e)}")
            
            # 启动后台线程执行部署
            deploy_thread = threading.Thread(target=deploy_task)
            deploy_thread.daemon = True
            deploy_thread.start()
            
            return True
        except Exception as e:
            if isinstance(e, ServiceServiceError):
                raise
            raise ServiceServiceError(f"部署微服务失败: {str(e)}")

    def stop_service(self, service_id: str) -> bool:
        """
        停止微服务

        Args:
            service_id: 微服务ID

        Returns:
            bool: 是否停止成功

        Raises:
            ServiceServiceError: 停止过程中出错
        """
        try:
            # 检查服务是否存在
            service = self.service_repository.get_service_by_id(service_id)
            if not service:
                raise ServiceServiceError(f"微服务ID {service_id} 不存在")
            
            # 检查服务状态是否允许停止
            if service.status not in STOPPABLE_STATUSES:
                raise ServiceServiceError(f"当前状态 {service.status} 不允许停止")
            
            # 设置状态为未部署
            success = self.service_repository.update_service_status(service_id, "not_deployed")
            if not success:
                raise ServiceServiceError("停止微服务失败")
            
            return True
        except Exception as e:
            if isinstance(e, ServiceServiceError):
                raise
            raise ServiceServiceError(f"停止微服务失败: {str(e)}")

    def upload_and_deploy_service(self, zip_file: FileStorage, service_data: Dict) -> Dict:
        """
        上传ZIP文件并部署微服务
        
        这个方法会：
        1. 创建服务记录（状态：deploying）
        2. 保存并解压ZIP文件
        3. 分配可用端口
        4. 修改docker-compose.yml
        5. 异步部署容器
        
        Args:
            zip_file: 上传的ZIP文件
            service_data: 包含微服务信息的字典（与create_service相同）
            
        Returns:
            Dict: 创建的微服务信息
            
        Raises:
            ServiceServiceError: 上传或部署过程中出错
        """
        service_id = None
        service_dir = None
        project_root = None
        
        try:
            # 1. 设置初始状态为"部署中"
            service_data['status'] = 'deploying'
            
            # 2. 创建服务记录
            service = self.service_repository.create_service_with_relations(service_data)
            service_id = service.id
            
            # 3. 获取服务存储基础路径（从环境变量）
            base_path = os.environ.get('SERVICES_BASE_PATH', '/app/data/services')
            service_dir = os.path.join(base_path, service_id)
            os.makedirs(service_dir, exist_ok=True)
            
            # 4. 保存ZIP文件
            zip_path = os.path.join(service_dir, 'uploaded.zip')
            zip_file.save(zip_path)
            
            # 5. 解压ZIP并找到项目根目录
            project_root = extract_and_find_root(zip_path, service_dir)
            print(f"服务 {service_id} 项目根目录: {project_root}")
            
            # 6. 解析docker-compose.yml获取需要的端口数量
            compose_file = os.path.join(project_root, 'docker-compose.yml')
            container_ports = parse_ports_from_compose(compose_file)
            port_count = len(container_ports)
            
            if port_count == 0:
                raise ServiceServiceError("docker-compose.yml中没有定义端口映射")
            
            print(f"服务 {service_id} 需要分配 {port_count} 个端口")
            
            # 7. 分配端口
            port_start = int(os.environ.get('PORT_RANGE_START', '27000'))
            port_end = int(os.environ.get('PORT_RANGE_END', '28000'))
            allocated_ports = allocate_ports(port_count, port_start, port_end)
            print(f"服务 {service_id} 分配端口: {allocated_ports}")
            
            # 8. 修改docker-compose.yml的端口映射
            port_mappings = modify_compose_ports(compose_file, allocated_ports)
            print(f"服务 {service_id} 端口映射: {port_mappings}")
            
            # 9. 更新服务的端口和路径信息
            port_str = ','.join(port_mappings)
            volume_path = os.path.relpath(project_root, base_path)
            
            update_data = {
                'port': port_str,
                'volume': volume_path
            }
            
            # 如果用户没有指定network，则使用生成的网络标识
            # 如果用户指定了network（如bridge），则保留用户的值
            if not service_data.get('network'):
                # 生成缩短的网络标识以适应数据库字段长度限制(50字符)
                network_name = f"svc_{service_id[:8]}"  # 例如: svc_af753698
                update_data['network'] = network_name
            
            self.service_repository.update_service(service_id, update_data)
            
            # 10. 如果用户没有提供apiList，自动生成默认的MCP API
            if not service_data.get('apiList'):
                # 从port_mappings中提取宿主机端口（第一个端口）
                # port_mappings格式: ["27000:8000"]
                host_port = port_mappings[0].split(':')[0]
                
                # 从环境变量获取部署服务的宿主机URL
                service_host_url = os.environ.get('SERVICE_HOST_URL', 'https://fdueblab.cn')
                artifact_metadata = load_mcp_artifact_metadata(project_root)
                endpoint = artifact_metadata['endpoint']
                description = artifact_metadata['description'] or (
                    f'提供{service_data.get("name", "MCP")}功能的MCP服务'
                )
                
                # 生成默认API
                default_api = {
                    'name': f'{service_data.get("name", "MCP")} Server',
                    'url': f'{service_host_url.rstrip("/")}/mcp-proxy/{host_port}{endpoint}',
                    'method': artifact_metadata['method'],
                    'des': description,
                    'parameterType': 1,
                    'responseType': 1,
                    'isFake': False,
                    'exampleMsg': [
                        {
                            'title': 'MCP服务测试示例',
                            'content': '这是一个自动生成的测试消息'
                        }
                    ],
                    'tools': artifact_metadata['tools']
                }
                
                # 更新服务，添加API
                self.service_repository.update_service_with_relations(service_id, {
                    'apiList': [default_api]
                })
                print(f"服务 {service_id} 已自动添加默认API: {default_api['url']}")
            
            # 11. 启动异步部署任务
            app = current_app._get_current_object()
            
            def deploy_task():
                """异步部署任务"""
                with app.app_context():
                    try:
                        print(f"开始部署服务 {service_id}")
                        
                        # 执行docker-compose部署
                        success, message = docker_deploy(project_root, service_id, timeout=600)
                        
                        if not self._is_deploy_still_active(service_id):
                            return

                        if success:
                            # 部署成功，更新状态为预发布(未测评)
                            self.service_repository.update_service_status(
                                service_id, 
                                "pre_release_unrated"
                            )
                            print(f"服务 {service_id} 部署成功: {message}")
                        else:
                            # 部署失败，清理资源
                            print(f"服务 {service_id} 部署失败: {message}")
                            if self._is_deploy_still_active(service_id):
                                self._cleanup_failed_deployment(service_id, project_root, service_dir)
                            
                    except Exception as e:
                        print(f"服务 {service_id} 部署异常: {str(e)}")
                        if self._is_deploy_still_active(service_id):
                            self._cleanup_failed_deployment(service_id, project_root, service_dir)
            
            # 启动后台线程执行部署
            deploy_thread = threading.Thread(target=deploy_task)
            deploy_thread.daemon = True
            deploy_thread.start()
            
            return service.to_dict()
            
        except (PortAllocationError, ZipProcessError, DockerDeployError) as e:
            # 如果在同步阶段失败，立即清理并抛出异常
            if service_id:
                self._cleanup_failed_deployment(service_id, project_root, service_dir)
            raise ServiceServiceError(str(e))
            
        except SQLAlchemyError as e:
            raise ServiceServiceError(f"创建微服务失败: {str(e)}")
            
        except Exception as e:
            if service_id:
                self._cleanup_failed_deployment(service_id, project_root, service_dir)
            raise ServiceServiceError(f"上传部署微服务过程中出错: {str(e)}")
    
    def _cleanup_failed_deployment(self, service_id: str, project_root: str, service_dir: str):
        """
        清理失败的部署资源
        
        Args:
            service_id: 服务ID
            project_root: 项目根目录
            service_dir: 服务存储目录
        """
        try:
            # 更新服务状态为error
            self.service_repository.update_service_status(service_id, "error")
            
            # 停止并删除容器
            if project_root and os.path.exists(project_root):
                stop_and_remove_service(project_root, service_id)
            
            # 删除解压的文件
            if service_dir and os.path.exists(service_dir):
                cleanup_directory(service_dir)
                
            print(f"服务 {service_id} 资源清理完成")
            
        except Exception as e:
            print(f"清理服务 {service_id} 资源失败: {str(e)}")

    def _is_uploaded_service(self, service) -> bool:
        """
        判断服务是否为通过上传功能部署的服务
        
        判断依据（必须同时满足所有条件）：
        1. network字段以 svc_ 开头
        2. volume字段非空（上传服务会有项目路径）
        3. port字段在27000-28000范围内
        
        Args:
            service: Service对象
            
        Returns:
            bool: 是否为上传部署的服务
        """
        # 条件1: network以svc_开头
        has_svc_network = service.network and service.network.startswith('svc_')
        if not has_svc_network:
            return False
        
        # 条件2: volume非空（上传服务会记录项目路径）
        has_volume = service.volume and service.volume.strip()
        if not has_volume:
            return False
        
        # 条件3: port在27000-28000范围内
        has_valid_port = False
        if service.port:
            try:
                # 解析端口映射，格式如 "27001:8000,27002:3306"
                port_start = int(os.environ.get('PORT_RANGE_START', '27000'))
                port_end = int(os.environ.get('PORT_RANGE_END', '28000'))
                
                for port_mapping in service.port.split(','):
                    if ':' in port_mapping:
                        host_port = int(port_mapping.split(':')[0].strip())
                        # 检查是否在27000-28000范围内
                        if port_start <= host_port < port_end:
                            has_valid_port = True
                            break
            except (ValueError, IndexError):
                pass
        
        if not has_valid_port:
            return False
        
        # 所有条件都满足，确认是上传的服务
        return True

    def cleanup_all_uploaded_services(self, delete_images: bool = False) -> Dict:
        """
        清理所有通过上传功能部署的服务
        
        此操作会：
        1. 停止并删除所有以 svc_ 开头的Docker容器
        2. 删除所有以 svc_ 开头的Docker网络
        3. 删除服务镜像（如果 delete_images=True）
        4. 删除所有服务文件
        5. 清空数据库中的服务记录
        
        Args:
            delete_images: 是否删除Docker镜像（默认False）
            
        Returns:
            Dict: 清理结果统计
            
        Raises:
            ServiceServiceError: 清理过程中出错
        """
        try:
            print("=" * 60)
            print("🚨 开始清理所有上传的服务")
            print("=" * 60)
            
            result = {
                'docker': {},
                'files': {},
                'database': {},
                'summary': {}
            }
            
            # 1. 清理Docker资源
            print("\n📦 步骤 1/3: 清理Docker资源...")
            docker_result = cleanup_docker_resources(delete_images=delete_images)
            result['docker'] = docker_result
            
            # 2. 清理服务文件
            print("\n📁 步骤 2/3: 清理服务文件...")
            base_path = os.environ.get('SERVICES_BASE_PATH', '/app/data/services')
            files_result = cleanup_service_files(base_path)
            result['files'] = files_result
            
            # 3. 清理数据库记录
            print("\n🗄️  步骤 3/3: 清理数据库记录...")
            try:
                from app.models.service.service_norm import ServiceNorm
                from app.models.service.service_source import ServiceSource
                from app.models.service.service_api import ServiceApi
                from app.models.service.service_api_parameter import ServiceApiParameter
                from app.models.service.service_api_tool import ServiceApiTool
                
                # 获取所有服务
                all_services = self.service_repository.get_all_services()
                deleted_count = 0
                failed_count = 0
                skipped_count = 0
                
                # 收集需要删除的服务ID
                services_to_delete = []
                for service in all_services:
                    if self._is_uploaded_service(service):
                        services_to_delete.append(service)
                    else:
                        skipped_count += 1
                        print(f"⏭️  跳过非上传服务: {service.name} ({service.id})")
                
                # 批量删除服务及其关联记录
                for service in services_to_delete:
                    try:
                        service_id = service.id
                        service_name = service.name
                        
                        # 手动级联删除关联记录（因为模型中没有配置cascade）
                        # 1. 获取所有API的ID
                        api_ids = [api.id for api in service.apis]
                        
                        # 2. 删除API的参数和工具
                        for api_id in api_ids:
                            ServiceApiParameter.query.filter_by(api_id=api_id).delete()
                            ServiceApiTool.query.filter_by(api_id=api_id).delete()
                        
                        # 3. 删除API
                        ServiceApi.query.filter_by(service_id=service_id).delete()
                        
                        # 4. 删除规范评分
                        ServiceNorm.query.filter_by(service_id=service_id).delete()
                        
                        # 5. 删除来源信息
                        ServiceSource.query.filter_by(service_id=service_id).delete()
                        
                        # 6. 最后删除服务本身
                        db.session.delete(service)
                        
                        # 提交这个服务的删除
                        db.session.commit()
                        
                        deleted_count += 1
                        print(f"✅ 删除上传服务: {service_name} ({service_id})")
                        
                    except Exception as e:
                        db.session.rollback()  # 回滚当前服务的删除
                        failed_count += 1
                        print(f"❌ 删除服务记录失败 {service_id}: {str(e)}")
                
                result['database'] = {
                    'services_deleted': deleted_count,
                    'services_failed': failed_count,
                    'services_skipped': skipped_count
                }
                
                print(f"✅ 删除了 {deleted_count} 条上传服务记录，跳过 {skipped_count} 条其他服务")
                
            except Exception as e:
                db.session.rollback()
                error_msg = f"清理数据库失败: {str(e)}"
                result['database'] = {
                    'error': error_msg
                }
                print(f"❌ {error_msg}")
            
            # 4. 生成总结
            print("\n" + "=" * 60)
            print("📊 清理完成！统计信息：")
            print("=" * 60)
            
            summary = {
                'containers_removed': docker_result.get('containers_removed', 0),
                'networks_removed': docker_result.get('networks_removed', 0),
                'images_removed': docker_result.get('images_removed', 0),
                'directories_removed': files_result.get('directories_removed', 0),
                'database_records_deleted': result['database'].get('services_deleted', 0),
                'total_errors': (
                    docker_result.get('containers_failed', 0) +
                    docker_result.get('networks_failed', 0) +
                    docker_result.get('images_failed', 0) +
                    files_result.get('directories_failed', 0) +
                    result['database'].get('services_failed', 0)
                )
            }
            
            result['summary'] = summary
            
            print(f"  容器删除: {summary['containers_removed']}")
            print(f"  网络删除: {summary['networks_removed']}")
            print(f"  镜像删除: {summary['images_removed']}")
            print(f"  目录删除: {summary['directories_removed']}")
            print(f"  数据库记录删除: {summary['database_records_deleted']}")
            print(f"  错误数量: {summary['total_errors']}")
            print("=" * 60)
            
            return result
            
        except Exception as e:
            raise ServiceServiceError(f"清理所有服务失败: {str(e)}")

    def upload_scenario_generated_algorithm(
        self, py_file: FileStorage, meta: Dict
    ) -> Dict:
        """
        想定式开发：上传生成的 .py 源码并登记为可检索的 Service（type=generated_algorithm）。
        """
        if not py_file or not py_file.filename:
            raise ServiceServiceError("缺少 Python 源码文件")

        raw_name = secure_filename(py_file.filename)
        if not raw_name.lower().endswith(".py"):
            raise ServiceServiceError("仅支持 .py 格式的源码文件")

        py_file.seek(0, 2)
        py_size = py_file.tell()
        py_file.seek(0)
        max_py = 16 * 1024 * 1024
        if py_size > max_py:
            raise ServiceServiceError(f"源码文件过大（最大 {max_py // (1024 * 1024)}MB）")

        name = (meta.get("name") or raw_name.replace(".py", "")).strip()
        if not name:
            raise ServiceServiceError("服务名称不能为空")

        domain = (meta.get("domain") or "aml").strip()
        industry = (meta.get("industry") or "").strip()
        scenario = (meta.get("scenario") or "").strip()
        technology = (meta.get("technology") or "").strip()

        service_data: Dict = {
            "name": name[:100],
            "attribute": (meta.get("attribute") or "custom").strip(),
            "type": "generated_algorithm",
            "domain": domain,
            "industry": industry,
            "scenario": scenario,
            "technology": technology,
            "network": "n/a",
            "port": "n/a",
            "volume": "n/a",
            "status": "not_deployed",
            "number": 0,
            "apiList": [
                {
                    "name": "算法源码",
                    "url": "",
                    "method": "GET",
                    "des": "想定式开发生成的算法源码，通过平台下载接口获取",
                    "parameterType": 0,
                    "responseType": 0,
                    "isFake": False,
                    "responseFileName": raw_name,
                }
            ],
        }
        if meta.get("source") and isinstance(meta["source"], dict):
            service_data["source"] = meta["source"]
        if meta.get("creator_id"):
            service_data["creator_id"] = meta["creator_id"]

        service_id = None
        try:
            service = self.service_repository.create_service_with_relations(
                service_data
            )
            service_id = service.id
            base = current_app.config["UPLOAD_FOLDER"]
            subdir = os.path.join(base, "generated_algorithm", service_id)
            os.makedirs(subdir, exist_ok=True)
            dest_path = os.path.join(subdir, raw_name)
            py_file.seek(0)
            py_file.save(dest_path)
            return service.to_dict()
        except Exception as e:
            if service_id:
                try:
                    self.delete_service(service_id)
                except Exception:
                    pass
            raise ServiceServiceError(f"登记生成算法资源失败: {str(e)}")

    def get_scenario_generated_code_path(self, service_id: str) -> Tuple[str, str]:
        """返回磁盘绝对路径与建议下载文件名（仅 type=generated_algorithm）。"""
        service = self.service_repository.get_service_by_id(service_id)
        if not service or service.deleted:
            raise ServiceServiceError(f"微服务ID {service_id} 不存在")
        if service.type != "generated_algorithm":
            raise ServiceServiceError("该服务不是想定式生成的算法资源")

        apis = self.service_repository.get_service_apis(service_id)
        if not apis:
            raise ServiceServiceError("未找到算法源码记录")

        fn = apis[0].response_file_name
        if not fn:
            raise ServiceServiceError("未配置源码文件名")

        base = current_app.config["UPLOAD_FOLDER"]
        path = os.path.join(base, "generated_algorithm", service_id, secure_filename(fn))
        if not os.path.isfile(path):
            raise ServiceServiceError("源码文件不存在或已被清理")

        return path, fn

    def get_my_services(self, creator_id: str) -> List[Dict]:
        """获取当前用户创建的成果列表（含升级建议）。"""
        if not creator_id:
            return []
        try:
            services = self.service_repository.get_services_by_creator(creator_id)
            service_ids = [item.id for item in services]
            advice_map = {}
            if service_ids:
                rows = ServiceUpgradeAdvice.query.filter(
                    ServiceUpgradeAdvice.service_id.in_(service_ids)
                ).all()
                advice_map = {row.service_id: row.to_dict() for row in rows}

            result = []
            for service in services:
                item = service.to_dict()
                item["upgradeAdvice"] = advice_map.get(service.id)
                result.append(item)
            return result
        except Exception as e:
            raise ServiceServiceError(f"获取我的成果失败: {str(e)}")

    def save_upgrade_advice(
        self, service_id: str, user_id: str, payload: Dict
    ) -> Dict:
        """保存或更新某成果的升级建议。"""
        try:
            service = self.service_repository.get_service_by_id(service_id)
            if not service:
                raise ServiceServiceError(f"微服务ID {service_id} 不存在")
            if service.creator_id != user_id:
                raise ServiceServiceError("无权保存该成果的升级建议")

            leading = str(payload.get("leadingAnalysis") or "").strip()
            auto_suggestion = str(payload.get("autoUpgradeSuggestion") or "").strip()
            manual_suggestion = str(payload.get("manualUpdateSuggestion") or "").strip()
            if not any([leading, auto_suggestion, manual_suggestion]):
                raise ServiceServiceError("升级建议内容不能为空")

            advice = ServiceUpgradeAdvice.query.filter_by(service_id=service_id).first()
            if not advice:
                advice = ServiceUpgradeAdvice(service_id=service_id)
                db.session.add(advice)

            advice.leading_analysis = leading
            advice.auto_upgrade_suggestion = auto_suggestion
            advice.manual_update_suggestion = manual_suggestion
            advice.generator_user_id = user_id
            advice.generated_at = int(time.time() * 1000)
            db.session.commit()
            return advice.to_dict()
        except ServiceServiceError:
            db.session.rollback()
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ServiceServiceError(f"保存升级建议失败: {str(e)}")


# 创建单例实例，方便导入使用
service_service = ServiceService()
