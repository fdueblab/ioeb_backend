"""
微服务服务模块
处理微服务相关的业务逻辑
"""

from typing import Dict, List, Optional, Tuple
import threading
import time

from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from app.repositories.service_repository import ServiceRepository
from app.extensions import db


class ServiceServiceError(Exception):
    """微服务服务错误"""


class ServiceService:
    """微服务服务类"""

    def __init__(self):
        """初始化微服务服务"""
        self.service_repository = ServiceRepository()

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
            return [service.to_dict() for service in services]
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
            return [service.to_dict() for service in services]
        except Exception as e:
            raise ServiceServiceError(f"搜索微服务失败: {str(e)}")

    def filter_services(self, **filters) -> List[Dict]:
        """
        根据条件筛选微服务

        Args:
            **filters: 筛选条件，可包括:
                - attribute: 服务属性（支持单个值或多个值列表）
                - type: 服务类型（支持单个值或多个值列表）
                - domain: 领域（支持单个值或多个值列表）
                - industry: 行业（支持单个值或多个值列表）
                - scenario: 场景（支持单个值或多个值列表）
                - technology: 技术（支持单个值或多个值列表）
                - status: 服务状态（支持单个值或多个值列表）

        Returns:
            List[Dict]: 符合条件的微服务列表
        """
        try:
            services = self.service_repository.filter_services(**filters)
            return [service.to_dict() for service in services]
        except Exception as e:
            raise ServiceServiceError(f"筛选微服务失败: {str(e)}")

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
            
            # 先设置状态为部署中
            self.service_repository.update_service_status(service_id, "deploying")
            
            # 获取当前Flask应用实例
            app = current_app._get_current_object()
            
            # 启动异步部署任务
            def deploy_task():
                with app.app_context():
                    try:
                        # 模拟部署过程，延时10秒
                        time.sleep(10)
                        
                        # 部署完成后设置状态为预发布(未测评)
                        self.service_repository.update_service_status(service_id, "pre_release_unrated")
                        print(f"服务 {service_id} 部署成功")
                    except Exception as e:
                        # 如果部署失败，设置状态为错误
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
            if service.status == "not_deployed":
                raise ServiceServiceError("微服务已经处于未部署状态")
            
            # 设置状态为未部署
            success = self.service_repository.update_service_status(service_id, "not_deployed")
            if not success:
                raise ServiceServiceError("停止微服务失败")
            
            return True
        except Exception as e:
            if isinstance(e, ServiceServiceError):
                raise
            raise ServiceServiceError(f"停止微服务失败: {str(e)}")


# 创建单例实例，方便导入使用
service_service = ServiceService() 