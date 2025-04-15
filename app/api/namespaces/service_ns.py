"""
微服务相关API
提供微服务的增删改查功能
"""

from flask import request
from flask_restx import Namespace, Resource, fields

from app.services.service_service import ServiceServiceError, service_service

# 创建命名空间
api = Namespace("services", description="微服务管理API")

# 定义规范评分模型
norm_model = api.model(
    "Norm",
    {
        "key": fields.String(description="规范类型"),
        "score": fields.Integer(description="评分")
    }
)

# 定义来源信息模型
source_model = api.model(
    "Source",
    {
        "popoverTitle": fields.String(description="弹出框标题"),
        "companyName": fields.String(description="公司名称"),
        "companyAddress": fields.String(description="公司地址"),
        "companyContact": fields.String(description="公司联系方式"),
        "companyIntroduce": fields.String(description="公司介绍"),
        "msIntroduce": fields.String(description="微服务介绍"),
        "companyScore": fields.Integer(description="公司评分"),
        "msScore": fields.Integer(description="微服务评分")
    }
)

# 定义API参数模型
api_parameter_model = api.model(
    "ApiParameter",
    {
        "name": fields.String(description="参数名称"),
        "type": fields.String(description="参数类型"),
        "des": fields.String(description="参数描述")
    }
)

# 定义API模型
api_model = api.model(
    "Api",
    {
        "name": fields.String(description="API名称"),
        "url": fields.String(description="API地址"),
        "method": fields.String(description="请求方法"),
        "des": fields.String(description="API描述"),
        "parameterType": fields.Integer(description="参数类型"),
        "responseType": fields.Integer(description="响应类型"),
        "isFake": fields.Boolean(description="是否为模拟数据"),
        "response": fields.Raw(description="模拟响应数据"),
        "responseFileName": fields.String(description="响应文件名"),
        "parameters": fields.List(fields.Nested(api_parameter_model), description="API参数")
    }
)

# 定义微服务模型
service_model = api.model(
    "Service",
    {
        "id": fields.String(description="服务ID"),
        "name": fields.String(required=True, description="服务名称"),
        "attribute": fields.String(description="服务属性"),
        "type": fields.String(description="服务类型"),
        "domain": fields.String(description="领域"),
        "industry": fields.String(description="行业"),
        "scenario": fields.String(description="场景"),
        "technology": fields.String(description="技术"),
        "network": fields.String(description="网络类型"),
        "port": fields.String(description="端口映射"),
        "volume": fields.String(description="数据卷映射"),
        "status": fields.String(description="服务状态"),
        "number": fields.Integer(description="服务调用次数"),
        "deleted": fields.Integer(description="是否删除"),
        "createTime": fields.Integer(description="创建时间"),
        "creatorId": fields.String(description="创建者ID"),
        "norm": fields.List(fields.Nested(norm_model), description="规范评分"),
        "source": fields.Nested(source_model, description="来源信息"),
        "apiList": fields.List(fields.Nested(api_model), description="API列表")
    }
)

# 定义创建微服务请求模型
service_create_model = api.model(
    "ServiceCreate",
    {
        "name": fields.String(required=True, description="服务名称"),
        "attribute": fields.String(description="服务属性"),
        "type": fields.String(description="服务类型"),
        "domain": fields.String(description="领域"),
        "industry": fields.String(description="行业"),
        "scenario": fields.String(description="场景"),
        "technology": fields.String(description="技术"),
        "network": fields.String(description="网络类型"),
        "port": fields.String(description="端口映射"),
        "volume": fields.String(description="数据卷映射"),
        "status": fields.String(description="服务状态"),
        "number": fields.Integer(description="服务调用次数", default=0),
        "norm": fields.List(fields.Nested(norm_model), description="规范评分"),
        "source": fields.Nested(source_model, description="来源信息"),
        "apiList": fields.List(fields.Nested(api_model), description="API列表")
    }
)

# 定义微服务响应模型
service_response = api.model(
    "ServiceResponse",
    {
        "status": fields.String(description="响应状态"),
        "message": fields.String(description="响应消息"),
        "service": fields.Nested(service_model, description="微服务信息")
    }
)

# 定义微服务列表响应模型
services_response = api.model(
    "ServicesResponse",
    {
        "status": fields.String(description="响应状态"),
        "message": fields.String(description="响应消息"),
        "total": fields.Integer(description="总记录数"),
        "services": fields.List(fields.Nested(service_model), description="微服务列表")
    }
)

# 定义错误响应模型
error_response = api.model(
    "ErrorResponse",
    {
        "status": fields.String(description="响应状态", default="error"),
        "message": fields.String(description="错误信息")
    }
)


@api.route("")
class ServiceList(Resource):
    @api.doc("list_services")
    @api.marshal_with(services_response, code=200)
    def get(self):
        """获取所有微服务"""
        try:
            services = service_service.get_all_services()
            return {
                "status": "success",
                "message": "获取微服务列表成功",
                "total": len(services),
                "services": services
            }, 200
        except ServiceServiceError as e:
            return {"status": "error", "message": str(e)}, 500

    @api.doc("create_service")
    @api.expect(service_create_model)
    @api.marshal_with(service_response, code=201)
    @api.response(400, "Invalid input", error_response)
    @api.response(500, "Server error", error_response)
    def post(self):
        """创建新微服务"""
        data = request.get_json()

        if not data:
            return {"status": "error", "message": "缺少请求数据"}, 400

        if not data.get("name"):
            return {"status": "error", "message": "服务名称不能为空"}, 400

        try:
            service = service_service.create_service(data)
            return {
                "status": "success", 
                "message": "微服务创建成功", 
                "service": service
            }, 201
        except ServiceServiceError as e:
            return {"status": "error", "message": str(e)}, 400


@api.route("/<string:id>")
@api.param("id", "微服务ID")
@api.response(404, "Service not found", error_response)
class ServiceResource(Resource):
    @api.doc("get_service")
    @api.marshal_with(service_response, code=200)
    def get(self, id):
        """获取指定ID的微服务"""
        try:
            service = service_service.get_service_by_id(id)
            return {
                "status": "success", 
                "message": "获取微服务成功", 
                "service": service
            }, 200
        except ServiceServiceError as e:
            return {"status": "error", "message": str(e)}, 404

    @api.doc("update_service")
    @api.expect(service_create_model)
    @api.marshal_with(service_response, code=200)
    @api.response(400, "Invalid input", error_response)
    @api.response(404, "Service not found", error_response)
    @api.response(500, "Server error", error_response)
    def put(self, id):
        """更新指定ID的微服务"""
        data = request.get_json()

        if not data:
            return {"status": "error", "message": "缺少请求数据"}, 400

        try:
            service = service_service.update_service(id, data)
            return {
                "status": "success", 
                "message": "微服务更新成功", 
                "service": service
            }, 200
        except ServiceServiceError as e:
            if "不存在" in str(e):
                return {"status": "error", "message": str(e)}, 404
            return {"status": "error", "message": str(e)}, 400

    @api.doc("delete_service")
    @api.response(200, "Service deleted")
    @api.response(404, "Service not found", error_response)
    def delete(self, id):
        """删除指定ID的微服务"""
        try:
            result = service_service.delete_service(id)
            if result:
                return {
                    "status": "success", 
                    "message": "微服务删除成功"
                }, 200
            return {"status": "error", "message": "微服务删除失败"}, 500
        except ServiceServiceError as e:
            return {"status": "error", "message": str(e)}, 404


@api.route("/search")
class ServiceSearch(Resource):
    @api.doc("search_services")
    @api.param("keyword", "搜索关键词")
    @api.marshal_with(services_response, code=200)
    def get(self):
        """搜索微服务"""
        keyword = request.args.get("keyword", "")
        try:
            services = service_service.search_services(keyword)
            return {
                "status": "success",
                "message": "搜索微服务成功",
                "total": len(services),
                "services": services
            }, 200
        except ServiceServiceError as e:
            return {"status": "error", "message": str(e)}, 500


@api.route("/filter")
class ServiceFilter(Resource):
    @api.doc("filter_services", description="""
        筛选微服务接口，可以组合多个条件进行筛选。
        
        可用筛选参数及其含义：
        - attribute: 服务属性 (non_intelligent-非智能体服务, open_source-开源模型, paid-付费模型, custom-定制模型)
          可以指定多个attribute值，用逗号(,)分隔
        - type: 服务类型 (atomic-原子微服务, meta-元应用服务)
        - domain: 领域 (aml-跨境支付AI监测, aircraft-无人飞机AI监控, health-乡村医疗AI服务, agriculture-数字农业AI服务, 
                      evtol-低空飞行AI应用, ecommerce-跨境电商AI应用, homeAI-家庭陪伴AI应用)
        - industry: 行业 (取决于domain，查看对应domain的industry字典)
        - scenario: 场景 (取决于domain，查看对应domain的scenario字典)
        - technology: 技术 (取决于domain，查看对应domain的technology字典)
        - status: 服务状态 (error-容器分配失败/异常, warning-运行中(未通过测评), default-未运行, 
                         success-运行中(已通过测评), processing-部署中)
        
        示例请求：
        GET /api/services/filter?attribute=open_source&domain=aml&status=success
        GET /api/services/filter?attribute=open_source,paid&domain=aml
    """)
    @api.param("attribute", "服务属性 (non_intelligent-非智能体服务, open_source-开源模型, paid-付费模型, custom-定制模型)，多个值用逗号分隔")
    @api.param("type", "服务类型 (atomic-原子微服务, meta-元应用服务)")
    @api.param("domain", "领域 (aml-跨境支付AI监测, aircraft-无人飞机AI监控, health-乡村医疗AI服务, agriculture-数字农业AI服务, evtol-低空飞行AI应用, ecommerce-跨境电商AI应用, homeAI-家庭陪伴AI应用)")
    @api.param("industry", "行业 (取决于domain，查看对应domain的industry字典)")
    @api.param("scenario", "场景 (取决于domain，查看对应domain的scenario字典)")
    @api.param("technology", "技术 (取决于domain，查看对应domain的technology字典)")
    @api.param("status", "服务状态 (error-容器分配失败/异常, warning-运行中(未通过测评), default-未运行, success-运行中(已通过测评), processing-部署中)")
    @api.marshal_with(services_response, code=200)
    def get(self):
        """筛选微服务"""
        filters = {}
        valid_filters = ["attribute", "type", "domain", "industry", "scenario", "technology", "status"]
        
        for key in valid_filters:
            value = request.args.get(key)
            if value is not None:
                # attribute为列表
                if key == "attribute":
                    filters[key] = value.split(",")
                else:
                    filters[key] = value
        
        try:
            services = service_service.filter_services(**filters)
            return {
                "status": "success",
                "message": "筛选微服务成功",
                "total": len(services),
                "services": services
            }, 200
        except ServiceServiceError as e:
            return {"status": "error", "message": str(e)}, 500 