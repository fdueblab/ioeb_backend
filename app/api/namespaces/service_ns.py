"""
微服务相关API
提供微服务的增删改查功能
"""

import json
from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage

from app.services.service_service import ServiceServiceError, service_service

# 创建命名空间
api = Namespace("services", description="微服务管理API")

# 定义规范评分模型
norm_model = api.model(
    "Norm",
    {
        "key": fields.String(description="规范类型"),
        "score": fields.Integer(description="评分"),
        "platformChecked": fields.Integer(description="是否经过平台检测：0-否，1-是", default=0)
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

# 定义MCP工具模型
tool_model = api.model(
    "Tool",
    {
        "id": fields.String(description="工具ID"),
        "name": fields.String(description="工具名称"),
        "description": fields.String(description="工具描述")
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
        "parameters": fields.List(fields.Nested(api_parameter_model), description="API参数"),
        # 元应用专用字段
        "subtitle": fields.String(description="元应用副标题(元应用专用)"),
        "services": fields.List(fields.String, description="元应用使用的服务ID列表(元应用专用)"),
        "inputName": fields.String(description="输入名称(元应用专用)"),
        "outputName": fields.String(description="输出名称(元应用专用)"),
        "outputVisualization": fields.Boolean(description="是否可视化输出(元应用专用)"),
        "submitButtonText": fields.String(description="提交按钮文本(元应用专用)"),
        # MCP专用字段
        "tools": fields.List(fields.Raw, description="MCP工具列表(MCP专用)"),
        "exampleMsg": fields.Raw(description="示例消息(MCP专用)")
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
        # REST服务字段
        "apiList": fields.List(fields.Nested(api_model), description="API列表(REST服务使用)"),
        # MCP服务专用字段
        "url": fields.String(description="MCP服务地址(MCP服务使用)"),
        "method": fields.String(description="MCP通信方法(MCP服务使用)"),
        "des": fields.String(description="MCP服务描述(MCP服务使用)"),
        "isFake": fields.Integer(description="是否使用假数据(MCP服务使用)"),
        "tools": fields.List(fields.Nested(tool_model), description="MCP工具列表(MCP服务使用)")
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

# 定义简单响应模型
simple_response = api.model(
    "SimpleResponse",
    {
        "status": fields.String(description="响应状态"),
        "message": fields.String(description="响应消息"),
    },
)

# 定义错误响应模型
error_response = api.model(
    "ErrorResponse",
    {
        "status": fields.String(description="响应状态", default="error"),
        "message": fields.String(description="错误信息")
    }
)

# 定义批量获取请求模型
batch_request_model = api.model(
    "BatchRequest",
    {
        "ids": fields.List(fields.String, required=True, description="服务ID列表", min_items=1, max_items=100)
    }
)

# 定义批量获取响应模型
batch_response_model = api.model(
    "BatchResponse",
    {
        "status": fields.String(description="响应状态"),
        "message": fields.String(description="响应消息"),
        "total": fields.Integer(description="成功获取的记录数"),
        "services": fields.List(fields.Nested(service_model), description="成功获取的微服务列表"),
        "notFound": fields.List(fields.String, description="不存在的服务ID列表")
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


@api.route("/prepublish")
class ServicePublish(Resource):
    @api.doc("prepublish_service")
    @api.expect(service_create_model)
    @api.marshal_with(service_response, code=201)
    @api.response(400, "Invalid input", error_response)
    @api.response(500, "Server error", error_response)
    def post(self):
        """预发布新服务"""
        data = request.get_json()

        if not data:
            return {"status": "error", "message": "缺少请求数据"}, 400

        if not data.get("name"):
            return {"status": "error", "message": "服务名称不能为空"}, 400

        try:
            service = service_service.create_service(data)
        except ServiceServiceError as e:
            return {"status": "error", "message": str(e)}, 400

        try:
            deployed = service_service.deploy_service(service["id"])
        except ServiceServiceError as e:
            return {"status": "error", "message": f"微服务创建成功，但部署失败：{str(e)}"}, 500

        if not deployed:
            return {"status": "error", "message": "微服务创建成功，但部署任务启动失败"}, 500

        return {
            "status": "success",
            "message": "微服务创建成功，部署已启动，正在部署中...",
            "service": service
        }, 201


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
    def post(self, id):
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
        
        所有参数都支持多个值，多个值用逗号(,)分隔。
        
        可用筛选参数及其含义：
        - attribute: 服务属性 (non_intelligent-非智能体服务, open_source-开源模型, paid-付费模型, custom-定制模型)
        - type: 服务类型 (atomic-原子微服务-REST, atomic_mcp-原子微服务-MCP, meta-元应用服务)
        - domain: 领域 (aml-跨境支付AI监测, aircraft-无人飞机AI监控, health-乡村医疗AI服务, agriculture-数字农业AI服务, 
                      evtol-低空飞行AI应用, ecommerce-跨境电商AI应用, homeAI-家庭陪伴AI应用)
        - industry: 行业 (取决于domain，查看对应domain的industry字典)
        - scenario: 场景 (取决于domain，查看对应domain的scenario字典)
        - technology: 技术 (取决于domain，查看对应domain的technology字典)
        - status: 服务状态 (not_deployed-未部署, deploying-部署中, pre_release_unrated-预发布(未测评), pre_release_pending-预发布(待平台测评), released-已发布, error-服务异常)
        
        示例请求：
        GET /api/services/filter?attribute=open_source&domain=aml&status=released
        GET /api/services/filter?attribute=open_source,paid&domain=aml,health&type=atomic,meta
        GET /api/services/filter?status=released,error&domain=aml
    """)
    @api.param("attribute", "服务属性 (non_intelligent-非智能体服务, open_source-开源模型, paid-付费模型, custom-定制模型)，多个值用逗号分隔")
    @api.param("type", "服务类型 (atomic-原子微服务-REST, atomic_mcp-原子微服务-MCP, meta-元应用服务)，多个值用逗号分隔")
    @api.param("domain", "领域 (aml-跨境支付AI监测, aircraft-无人飞机AI监控, health-乡村医疗AI服务, agriculture-数字农业AI服务, evtol-低空飞行AI应用, ecommerce-跨境电商AI应用, homeAI-家庭陪伴AI应用)，多个值用逗号分隔")
    @api.param("industry", "行业 (取决于domain，查看对应domain的industry字典)，多个值用逗号分隔")
    @api.param("scenario", "场景 (取决于domain，查看对应domain的scenario字典)，多个值用逗号分隔")
    @api.param("technology", "技术 (取决于domain，查看对应domain的technology字典)，多个值用逗号分隔")
    @api.param("status", "服务状态 (not_deployed-未部署, deploying-部署中, pre_release_unrated-预发布(未测评), pre_release_pending-预发布(待平台测评), released-已发布, error-服务异常)，多个值用逗号分隔")
    @api.marshal_with(services_response, code=200)
    def get(self):
        """筛选微服务"""
        filters = {}
        valid_filters = ["attribute", "type", "domain", "industry", "scenario", "technology", "status"]
        
        for key in valid_filters:
            value = request.args.get(key)
            # 只处理非空且有实际内容的参数值
            if value is not None and value.strip():
                # 所有参数都支持多个值，用逗号分隔
                # 过滤掉空字符串和只包含空白字符的值
                value_list = [v.strip() for v in value.split(",") if v.strip()]
                if value_list:
                    filters[key] = value_list
        
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


@api.route("/batch")
class ServiceBatch(Resource):
    @api.doc("batch_get_services", description="""
        批量获取微服务接口，通过服务ID列表一次性获取多个服务的信息。
        
        该接口具有以下特点：
        - 支持一次性获取多个服务信息，提高性能
        - 最多支持一次获取100个服务
        - 会返回成功获取的服务列表和不存在的服务ID列表
        - 服务按输入ID的顺序返回
        - 自动去重，重复的ID只会返回一次
        
        请求体示例：
        {
            "ids": ["service-id-1", "service-id-2", "service-id-3"]
        }
        
        响应示例：
        {
            "status": "success",
            "message": "批量获取微服务成功",
            "total": 2,
            "services": [
                {服务1信息},
                {服务2信息}
            ],
            "notFound": ["service-id-3"]
        }
    """)
    @api.expect(batch_request_model)
    @api.marshal_with(batch_response_model, code=200)
    @api.response(400, "Invalid input", error_response)
    @api.response(500, "Server error", error_response)
    def post(self):
        """批量获取微服务"""
        data = request.get_json()

        if not data:
            return {"status": "error", "message": "缺少请求数据"}, 400

        service_ids = data.get("ids")
        if not service_ids:
            return {"status": "error", "message": "服务ID列表不能为空"}, 400

        if not isinstance(service_ids, list):
            return {"status": "error", "message": "服务ID列表必须是数组格式"}, 400

        if len(service_ids) == 0:
            return {"status": "error", "message": "服务ID列表不能为空"}, 400

        if len(service_ids) > 100:
            return {"status": "error", "message": "一次最多只能获取100个服务"}, 400

        # 检查所有ID是否为字符串
        for service_id in service_ids:
            if not isinstance(service_id, str) or not service_id.strip():
                return {"status": "error", "message": "服务ID必须是非空字符串"}, 400

        try:
            services, not_found_ids = service_service.get_services_by_ids(service_ids)
            
            message = "批量获取微服务成功"
            if not_found_ids:
                message += f"，其中{len(not_found_ids)}个服务不存在"
            
            return {
                "status": "success",
                "message": message,
                "total": len(services),
                "services": services,
                "notFound": not_found_ids
            }, 200
        except ServiceServiceError as e:
            return {"status": "error", "message": str(e)}, 500


@api.route("/<string:id>/delete")
@api.param("id", "微服务ID")
@api.response(404, "Service not found", error_response)
class ServiceDeleteResource(Resource):
    @api.doc("delete_service")
    @api.marshal_with(simple_response, code=200)
    @api.response(404, "Service not found", error_response)
    def get(self, id):
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


@api.route("/<string:id>/deploy")
@api.param("id", "微服务ID")
@api.response(404, "Service not found", error_response)
class ServiceDeployResource(Resource):
    @api.doc("deploy_service")
    @api.marshal_with(simple_response, code=200)
    @api.response(404, "Service not found", error_response)
    def get(self, id):
        """部署指定ID的微服务"""
        try:
            result = service_service.deploy_service(id)
            if result:
                return {
                    "status": "success", 
                    "message": "微服务部署已启动，正在部署中..."
                }, 200
            return {"status": "error", "message": "微服务部署失败"}, 500
        except ServiceServiceError as e:
            return {"status": "error", "message": str(e)}, 404


@api.route("/<string:id>/stop")
@api.param("id", "微服务ID")
@api.response(404, "Service not found", error_response)
class ServiceStopResource(Resource):
    @api.doc("stop_service")
    @api.marshal_with(simple_response, code=200)
    @api.response(404, "Service not found", error_response)
    def get(self, id):
        """停止指定ID的微服务"""
        try:
            result = service_service.stop_service(id)
            if result:
                return {
                    "status": "success", 
                    "message": "微服务停止成功"
                }, 200
            return {"status": "error", "message": "微服务停止失败"}, 500
        except ServiceServiceError as e:
            return {"status": "error", "message": str(e)}, 404


# 定义文件上传参数
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='ZIP压缩文件')
upload_parser.add_argument('name', location='form', type=str, required=True, help='服务名称')
upload_parser.add_argument('attribute', location='form', type=str, required=False, help='服务属性')
upload_parser.add_argument('type', location='form', type=str, required=False, help='服务类型')
upload_parser.add_argument('domain', location='form', type=str, required=False, help='领域')
upload_parser.add_argument('industry', location='form', type=str, required=False, help='行业')
upload_parser.add_argument('scenario', location='form', type=str, required=False, help='场景')
upload_parser.add_argument('technology', location='form', type=str, required=False, help='技术')
upload_parser.add_argument('network', location='form', type=str, required=False, help='网络类型')
upload_parser.add_argument('port', location='form', type=str, required=False, help='端口映射')
upload_parser.add_argument('volume', location='form', type=str, required=False, help='数据卷映射')
upload_parser.add_argument('number', location='form', type=int, required=False, help='服务调用次数')
upload_parser.add_argument('norm', location='form', type=str, required=False, help='规范评分JSON字符串')
upload_parser.add_argument('source', location='form', type=str, required=False, help='来源信息JSON字符串')
upload_parser.add_argument('apiList', location='form', type=str, required=False, help='API列表JSON字符串')


@api.route("/upload")
class ServiceUpload(Resource):
    @api.doc("upload_and_deploy_service", description="""
        上传ZIP文件并部署微服务
        
        该接口接收一个ZIP压缩文件和服务元数据，完成以下操作：
        1. 创建服务记录（初始状态：deploying）
        2. 解压ZIP文件并找到项目根目录（包含docker-compose.yml）
        3. 自动分配可用端口（27000-28000范围）
        4. 修改docker-compose.yml中的端口映射
        5. 使用docker-compose部署服务
        6. 根据部署结果更新服务状态（pre_release_unrated/error）
        
        ZIP文件要求：
        - 必须包含docker-compose.yml文件
        - 必须包含Dockerfile文件
        - 结构类似从GitHub下载的代码仓库
        
        表单参数：
        - file: ZIP文件（必需）
        - name: 服务名称（必需）
        - attribute: 服务属性（可选，默认：non_intelligent）
        - type: 服务类型（可选，默认：atomic）
        - domain: 领域（可选，默认：aml）
        - norm: 规范评分（可选，JSON字符串）
        - source: 来源信息（可选，JSON字符串）
        - apiList: API列表（可选，JSON字符串）
        
        注意：
        - 部署是异步进行的，接口会立即返回
        - 可通过查询服务接口获取最新状态
        - 端口会自动分配，无需手动指定
    """)
    @api.expect(upload_parser)
    @api.marshal_with(service_response, code=201)
    @api.response(400, "Invalid input", error_response)
    @api.response(500, "Server error", error_response)
    def post(self):
        """上传ZIP文件并部署微服务"""
        args = upload_parser.parse_args()
        
        # 获取ZIP文件
        zip_file = args['file']
        if not zip_file:
            return {"status": "error", "message": "缺少ZIP文件"}, 400
        
        # 验证文件类型
        if not zip_file.filename.endswith('.zip'):
            return {"status": "error", "message": "只支持ZIP格式的压缩文件"}, 400
        
        # 验证文件大小（100MB限制）
        zip_file.seek(0, 2)  # 移到文件末尾
        file_size = zip_file.tell()
        zip_file.seek(0)  # 重置到开头
        
        max_size = 100 * 1024 * 1024  # 100MB
        if file_size > max_size:
            return {"status": "error", "message": f"文件大小超过限制（最大100MB）"}, 400
        
        # 构建服务数据
        service_data = {
            'name': args['name']
        }
        
        # 添加可选字段
        optional_fields = ['attribute', 'type', 'domain', 'industry', 'scenario', 
                          'technology', 'network', 'port', 'volume', 'number']
        for field in optional_fields:
            if args.get(field):
                service_data[field] = args[field]
        
        # 解析JSON字符串字段
        try:
            if args.get('norm'):
                service_data['norm'] = json.loads(args['norm'])
            if args.get('source'):
                service_data['source'] = json.loads(args['source'])
            if args.get('apiList'):
                service_data['apiList'] = json.loads(args['apiList'])
        except json.JSONDecodeError as e:
            return {"status": "error", "message": f"JSON格式错误: {str(e)}"}, 400
        
        # 调用服务层处理
        try:
            service = service_service.upload_and_deploy_service(zip_file, service_data)
            return {
                "status": "success",
                "message": "微服务上传成功，正在部署中...",
                "service": service
            }, 201
        except ServiceServiceError as e:
            return {"status": "error", "message": str(e)}, 400


# 定义清理响应模型
cleanup_response = api.model(
    "CleanupResponse",
    {
        "status": fields.String(description="响应状态"),
        "message": fields.String(description="响应消息"),
        "summary": fields.Raw(description="清理统计信息"),
        "details": fields.Raw(description="详细清理结果")
    }
)


@api.route("/cleanup/all")
class ServiceCleanupAll(Resource):
    @api.doc("cleanup_all_services", description="""
        清理所有通过上传功能部署的服务
        
        ⚠️ **危险操作！** 此接口会：
        1. 停止并删除所有以 svc_ 开头的Docker容器
        2. 删除所有以 svc_ 开头的Docker网络
        3. 删除所有服务文件（/data/ioeb_services）
        4. **清空数据库中的所有服务记录**
        5. 可选：删除服务使用的Docker镜像
        
        此操作**不可逆**，请谨慎使用！
        
        建议使用场景：
        - 测试环境清理
        - 开发环境重置
        - 批量删除所有上传的服务
        
        Query参数：
        - delete_images: 是否删除Docker镜像（默认false）
        - confirm: 必须传入"yes"才能执行（安全确认）
        
        示例：
        DELETE /api/services/cleanup/all?confirm=yes&delete_images=false
    """)
    @api.param("confirm", "确认删除（必须为'yes'）", required=True, type=str)
    @api.param("delete_images", "是否删除Docker镜像（默认false）", required=False, type=bool, default=False)
    @api.marshal_with(cleanup_response, code=200)
    @api.response(400, "Invalid input", error_response)
    @api.response(403, "Confirmation required", error_response)
    @api.response(500, "Server error", error_response)
    def delete(self):
        """清理所有上传的服务（危险操作）"""
        # 安全确认
        confirm = request.args.get('confirm', '').lower()
        if confirm != 'yes':
            return {
                "status": "error",
                "message": "请通过 confirm=yes 参数确认此危险操作"
            }, 403
        
        # 是否删除镜像
        delete_images = request.args.get('delete_images', 'false').lower() == 'true'
        
        try:
            # 执行清理
            result = service_service.cleanup_all_uploaded_services(delete_images=delete_images)
            
            summary = result.get('summary', {})
            
            message = (
                f"清理完成！"
                f"容器: {summary.get('containers_removed', 0)}, "
                f"网络: {summary.get('networks_removed', 0)}, "
                f"镜像: {summary.get('images_removed', 0)}, "
                f"目录: {summary.get('directories_removed', 0)}, "
                f"数据库记录: {summary.get('database_records_deleted', 0)}"
            )
            
            if summary.get('total_errors', 0) > 0:
                message += f" (有 {summary['total_errors']} 个错误)"
            
            return {
                "status": "success",
                "message": message,
                "summary": summary,
                "details": result
            }, 200
            
        except ServiceServiceError as e:
            return {"status": "error", "message": str(e)}, 500 