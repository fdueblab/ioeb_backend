import uuid

# 生成一个固定的UUID作为服务ID
SERVICE_ID = "5e7f3a1c-e8b2-4a14-9f3c-971d02f46577"

# 模拟服务数据
MOCK_SERVICES = [
    {
        "id": SERVICE_ID,
        "name": "课题一风险识别模型推理微服务",
        "attribute": 1,
        "type": 0,
        "domain": 0,
        "industry": 0,
        "scenario": 1,
        "technology": 1,
        "network": "bridge",
        "port": "0.0.0.0:8000/TCP → 0.0.0.0:80000",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/aml/data",
        "status": 4,
        "number": "512",
        "deleted": 0,
        "create_time": 1617321600000,  # 2021-04-02 00:00:00
        "creator_id": "4291d7da9005377ec9aec4a71ea837f",  # admin用户ID
    }
]

# 模拟服务规范评分数据
MOCK_SERVICE_NORMS = [
    {"id": str(uuid.uuid4()), "service_id": SERVICE_ID, "key": 0, "score": 5},
    {"id": str(uuid.uuid4()), "service_id": SERVICE_ID, "key": 2, "score": 5},
]

# 模拟服务来源信息数据
MOCK_SERVICE_SOURCES = [
    {
        "id": str(uuid.uuid4()),
        "service_id": SERVICE_ID,
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "课题一",
        "ms_introduce": "基于智能体的风险识别算法",
        "company_score": 5,
        "ms_score": 5,
    }
]

# 模拟服务API数据
MOCK_SERVICE_APIS = [
    {
        "id": "api-" + str(uuid.uuid4()),
        "service_id": SERVICE_ID,
        "name": "predict",
        "url": "/api/project1/predict",
        "method": "POST",
        "des": "模型推理接口，基于数据集和参数配置得到风险识别结果",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": False,
    },
    {
        "id": "api-" + str(uuid.uuid4()),
        "service_id": SERVICE_ID,
        "name": "healthCheck",
        "url": "/api/project1/health",
        "method": "GET",
        "des": "判断微服务状态是否正常可用",
        "parameter_type": 0,
        "response_type": 0,
        "is_fake": False,
    },
]

# 存储API ID以便于后续关联参数
API_IDS = {"predict": MOCK_SERVICE_APIS[0]["id"], "healthCheck": MOCK_SERVICE_APIS[1]["id"]}

# 模拟服务API参数数据
MOCK_SERVICE_API_PARAMETERS = [
    {
        "id": str(uuid.uuid4()),
        "api_id": API_IDS["predict"],
        "name": "file",
        "type": "zip file",
        "des": "数据集和参数配置文件的zip压缩包",
    }
]
