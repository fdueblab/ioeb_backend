"""
微服务数据仓库模块
提供对微服务数据模型的基础操作接口
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Union

from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models import Service, ServiceNorm, ServiceSource, ServiceApi, ServiceApiParameter


class ServiceRepository:
    """微服务数据仓库"""

    def get_all_services(self) -> List[Service]:
        """
        获取所有微服务

        Returns:
            List[Service]: 微服务对象列表
        """
        return Service.query.filter_by(deleted=0).all()
    
    def get_all_services_with_dict(self) -> List[Dict]:
        """
        获取所有微服务的字典表示

        Returns:
            List[Dict]: 微服务字典列表
        """
        services = self.get_all_services()
        return [service.to_dict() for service in services]
    
    def get_service_by_id(self, service_id: str) -> Optional[Service]:
        """
        根据ID获取微服务

        Args:
            service_id: 微服务ID

        Returns:
            Optional[Service]: 微服务对象，如果不存在则返回None
        """
        return Service.query.filter_by(id=service_id, deleted=0).first()
    
    def get_service_dict_by_id(self, service_id: str) -> Optional[Dict]:
        """
        根据ID获取微服务的字典表示

        Args:
            service_id: 微服务ID

        Returns:
            Optional[Dict]: 微服务字典，如果不存在则返回None
        """
        service = self.get_service_by_id(service_id)
        return service.to_dict() if service else None
    
    def find_by_name(self, name: str) -> Optional[Service]:
        """
        根据名称查找微服务

        Args:
            name: 微服务名称

        Returns:
            Optional[Service]: 微服务对象，如果不存在则返回None
        """
        return Service.query.filter_by(name=name, deleted=0).first()
    
    def find_by_attribute(self, attribute: str) -> List[Service]:
        """
        根据属性查找微服务

        Args:
            attribute: 微服务属性

        Returns:
            List[Service]: 微服务对象列表
        """
        return Service.query.filter_by(attribute=attribute, deleted=0).all()
    
    def search_by_keyword(self, keyword: str) -> List[Service]:
        """
        根据关键词搜索微服务

        Args:
            keyword: 搜索关键词，匹配服务名称

        Returns:
            List[Service]: 符合条件的微服务对象列表
        """
        return Service.query.filter(
            Service.name.like(f"%{keyword}%"),
            Service.deleted == 0
        ).all()
    
    def create_service(self, service_data: Dict) -> Service:
        """
        创建新微服务

        Args:
            service_data: 包含微服务基本信息的字典

        Returns:
            Service: 创建的微服务对象
        """
        service = Service(**service_data)
        db.session.add(service)
        db.session.commit()
        return service
    
    def create_service_with_relations(self, service_data: Dict) -> Service:
        """
        创建微服务及其关联数据（规范评分、来源信息、API）

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
            Service: 创建的微服务对象

        Raises:
            SQLAlchemyError: 数据库操作错误
        """
        try:
            # 开始数据库事务
            service_id = str(uuid.uuid4())
            current_time = int(datetime.now().timestamp() * 1000)  # 毫秒时间戳

            # 创建服务基本信息
            service = Service(
                id=service_id,
                name=service_data.get("name"),
                attribute=str(service_data.get("attribute", "non_intelligent")),
                type=str(service_data.get("type", "atomic")),
                domain=str(service_data.get("domain", "")),
                industry=str(service_data.get("industry", "")),
                scenario=str(service_data.get("scenario", "")),
                technology=str(service_data.get("technology", "")),
                network=service_data.get("network", "bridge"),
                port=service_data.get("port", ""),
                volume=service_data.get("volume", ""),
                status=str(service_data.get("status", "default")),
                number=service_data.get("number", "0"),
                create_time=current_time,
                creator_id=service_data.get("creator_id", "")
            )
            db.session.add(service)
            
            # 添加规范评分
            if "norm" in service_data and isinstance(service_data["norm"], list):
                for norm_data in service_data["norm"]:
                    norm = ServiceNorm(
                        id=str(uuid.uuid4()),
                        service_id=service_id,
                        key=str(norm_data.get("key", "")),
                        score=norm_data.get("score", 0)
                    )
                    db.session.add(norm)
            
            # 添加来源信息
            if "source" in service_data and isinstance(service_data["source"], dict):
                source_data = service_data["source"]
                source = ServiceSource(
                    id=str(uuid.uuid4()),
                    service_id=service_id,
                    popover_title=source_data.get("popoverTitle", ""),
                    company_name=source_data.get("companyName", ""),
                    company_address=source_data.get("companyAddress", ""),
                    company_contact=source_data.get("companyContact", ""),
                    company_introduce=source_data.get("companyIntroduce", ""),
                    ms_introduce=source_data.get("msIntroduce", ""),
                    company_score=source_data.get("companyScore", 0),
                    ms_score=source_data.get("msScore", 0)
                )
                db.session.add(source)
            
            # 添加API信息
            if "apiList" in service_data and isinstance(service_data["apiList"], list):
                for api_data in service_data["apiList"]:
                    api_id = str(uuid.uuid4())
                    
                    # 处理可能的JSON字符串响应
                    response = None
                    if api_data.get("response"):
                        if isinstance(api_data["response"], dict):
                            response = json.dumps(api_data["response"])
                        else:
                            response = api_data["response"]
                    
                    api = ServiceApi(
                        id=api_id,
                        service_id=service_id,
                        name=api_data.get("name", ""),
                        url=api_data.get("url", ""),
                        method=api_data.get("method", "GET"),
                        des=api_data.get("des", ""),
                        parameter_type=api_data.get("parameterType", 0),
                        response_type=api_data.get("responseType", 0),
                        is_fake=api_data.get("isFake", False),
                        response=response,
                        response_file_name=api_data.get("responseFileName")
                    )
                    db.session.add(api)
                    
                    # 添加API参数
                    if "parameters" in api_data and isinstance(api_data["parameters"], list):
                        for param_data in api_data["parameters"]:
                            param = ServiceApiParameter(
                                id=str(uuid.uuid4()),
                                api_id=api_id,
                                name=param_data.get("name", ""),
                                type=param_data.get("type", ""),
                                des=param_data.get("des", "")
                            )
                            db.session.add(param)
            
            # 提交事务
            db.session.commit()
            return service
        except Exception as e:
            db.session.rollback()
            raise e
    
    def update_service(self, service_id: str, service_data: Dict) -> Optional[Service]:
        """
        更新微服务信息

        Args:
            service_id: 微服务ID
            service_data: 更新的微服务数据

        Returns:
            Optional[Service]: 更新后的微服务对象，如果不存在则返回None
        """
        service = self.get_service_by_id(service_id)
        if not service:
            return None
        
        for key, value in service_data.items():
            if hasattr(service, key):
                setattr(service, key, value)
        
        db.session.commit()
        return service
    
    def update_service_with_relations(self, service_id: str, service_data: Dict) -> Optional[Service]:
        """
        更新微服务及其关联数据（规范评分、来源信息、API）

        Args:
            service_id: 微服务ID
            service_data: 更新的微服务数据

        Returns:
            Optional[Service]: 更新后的微服务对象，如果不存在则返回None

        Raises:
            SQLAlchemyError: 数据库操作错误
        """
        try:
            service = self.get_service_by_id(service_id)
            if not service:
                return None
            
            # 更新服务基本信息
            for key, value in service_data.items():
                if key in ["name", "attribute", "type", "domain", "industry", 
                         "scenario", "technology", "network", "port", 
                         "volume", "status", "number"]:
                    if key in ["attribute", "type", "domain", "industry", "scenario", "technology", "status"] and value is not None:
                        value = str(value)
                    setattr(service, key, value)
            
            # 更新规范评分
            if "norm" in service_data and isinstance(service_data["norm"], list):
                # 删除现有的规范评分
                ServiceNorm.query.filter_by(service_id=service_id).delete()
                
                # 添加新的规范评分
                for norm_data in service_data["norm"]:
                    norm = ServiceNorm(
                        id=str(uuid.uuid4()),
                        service_id=service_id,
                        key=str(norm_data.get("key", "")),
                        score=norm_data.get("score", 0)
                    )
                    db.session.add(norm)
            
            # 更新来源信息
            if "source" in service_data and isinstance(service_data["source"], dict):
                # 删除现有的来源信息
                ServiceSource.query.filter_by(service_id=service_id).delete()
                
                # 添加新的来源信息
                source_data = service_data["source"]
                source = ServiceSource(
                    id=str(uuid.uuid4()),
                    service_id=service_id,
                    popover_title=source_data.get("popoverTitle", ""),
                    company_name=source_data.get("companyName", ""),
                    company_address=source_data.get("companyAddress", ""),
                    company_contact=source_data.get("companyContact", ""),
                    company_introduce=source_data.get("companyIntroduce", ""),
                    ms_introduce=source_data.get("msIntroduce", ""),
                    company_score=source_data.get("companyScore", 0),
                    ms_score=source_data.get("msScore", 0)
                )
                db.session.add(source)
            
            # 更新API信息
            if "apiList" in service_data and isinstance(service_data["apiList"], list):
                # 获取现有API的ID
                existing_apis = ServiceApi.query.filter_by(service_id=service_id).all()
                existing_api_ids = [api.id for api in existing_apis]
                
                # 删除相关的参数
                for api_id in existing_api_ids:
                    ServiceApiParameter.query.filter_by(api_id=api_id).delete()
                
                # 删除API
                ServiceApi.query.filter_by(service_id=service_id).delete()
                
                # 添加新的API
                for api_data in service_data["apiList"]:
                    api_id = str(uuid.uuid4())
                    
                    # 处理可能的JSON字符串响应
                    response = None
                    if api_data.get("response"):
                        if isinstance(api_data["response"], dict):
                            response = json.dumps(api_data["response"])
                        else:
                            response = api_data["response"]
                    
                    api = ServiceApi(
                        id=api_id,
                        service_id=service_id,
                        name=api_data.get("name", ""),
                        url=api_data.get("url", ""),
                        method=api_data.get("method", "GET"),
                        des=api_data.get("des", ""),
                        parameter_type=api_data.get("parameterType", 0),
                        response_type=api_data.get("responseType", 0),
                        is_fake=api_data.get("isFake", False),
                        response=response,
                        response_file_name=api_data.get("responseFileName")
                    )
                    db.session.add(api)
                    
                    # 添加API参数
                    if "parameters" in api_data and isinstance(api_data["parameters"], list):
                        for param_data in api_data["parameters"]:
                            param = ServiceApiParameter(
                                id=str(uuid.uuid4()),
                                api_id=api_id,
                                name=param_data.get("name", ""),
                                type=param_data.get("type", ""),
                                des=param_data.get("des", "")
                            )
                            db.session.add(param)
            
            # 提交事务
            db.session.commit()
            return service
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete_service(self, service_id: str) -> bool:
        """
        删除微服务（软删除）

        Args:
            service_id: 微服务ID

        Returns:
            bool: 是否删除成功
        """
        service = self.get_service_by_id(service_id)
        if not service:
            return False
        
        service.deleted = 1
        db.session.commit()
        return True
    
    def filter_services(self, **filters) -> List[Service]:
        """
        根据条件筛选微服务

        Args:
            **filters: 筛选条件，可包括:
                - attribute: 服务属性
                - type: 服务类型
                - domain: 领域
                - industry: 行业
                - scenario: 场景
                - technology: 技术
                - status: 服务状态

        Returns:
            List[Service]: 符合条件的微服务对象列表
        """
        query = Service.query.filter_by(deleted=0)
        
        # 应用筛选条件
        valid_filters = ["attribute", "type", "domain", "industry", "scenario", "technology", "status"]
        for key, value in filters.items():
            if key in valid_filters and value is not None:
                # 确保所有值都是字符串类型
                if not isinstance(value, str):
                    value = str(value)
                query = query.filter(getattr(Service, key) == value)
        
        return query.all()
    
    def get_service_norms(self, service_id: str) -> List[ServiceNorm]:
        """
        获取微服务的规范评分列表

        Args:
            service_id: 微服务ID

        Returns:
            List[ServiceNorm]: 规范评分对象列表
        """
        return ServiceNorm.query.filter_by(service_id=service_id).all()
    
    def get_service_source(self, service_id: str) -> Optional[ServiceSource]:
        """
        获取微服务的来源信息

        Args:
            service_id: 微服务ID

        Returns:
            Optional[ServiceSource]: 来源信息对象，如果不存在则返回None
        """
        return ServiceSource.query.filter_by(service_id=service_id).first()
    
    def get_service_apis(self, service_id: str) -> List[ServiceApi]:
        """
        获取微服务的API列表

        Args:
            service_id: 微服务ID

        Returns:
            List[ServiceApi]: API对象列表
        """
        return ServiceApi.query.filter_by(service_id=service_id).all()
    
    def get_api_parameters(self, api_id: str) -> List[ServiceApiParameter]:
        """
        获取API的参数列表

        Args:
            api_id: API ID

        Returns:
            List[ServiceApiParameter]: 参数对象列表
        """
        return ServiceApiParameter.query.filter_by(api_id=api_id).all()


# 创建单例实例，方便导入使用
service_repository = ServiceRepository() 