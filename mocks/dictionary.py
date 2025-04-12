"""
字典示例数据
"""

import uuid

# 通用字典数据
MOCK_STATUS_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "status",
        "code": "error",
        "text": "容器分配失败",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "status",
        "code": "warning",
        "text": "运行中(未通过测评)",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "status",
        "code": "default",
        "text": "未运行",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "status",
        "code": "error",
        "text": "异常",
        "sort": 4
    },
    {
        "id": str(uuid.uuid4()),
        "category": "status",
        "code": "success",
        "text": "运行中(已通过测评)",
        "sort": 5
    },
    {
        "id": str(uuid.uuid4()),
        "category": "status",
        "code": "processing",
        "text": "部署中",
        "sort": 6
    }
]

MOCK_NORM_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "norm",
        "code": "security",
        "text": "安全性",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "norm",
        "code": "robustness",
        "text": "鲁棒性",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "norm",
        "code": "privacy",
        "text": "隐私性",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "norm",
        "code": "trustworthiness",
        "text": "可信性",
        "sort": 4
    }
]

MOCK_API_TYPE_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "api_type",
        "code": "restful",
        "text": "RESTful API",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "api_type",
        "code": "graphql",
        "text": "GraphQL API",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "api_type",
        "code": "websocket",
        "text": "WebSocket API",
        "sort": 3
    }
]

MOCK_METHOD_TYPE_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "method_type",
        "code": "get",
        "text": "GET",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "method_type",
        "code": "post",
        "text": "POST",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "method_type",
        "code": "put",
        "text": "PUT",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "method_type",
        "code": "delete",
        "text": "DELETE",
        "sort": 4
    }
]

MOCK_IO_TYPE_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "io_type",
        "code": "none",
        "text": "none",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "io_type",
        "code": "string",
        "text": "string",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "io_type",
        "code": "formdata",
        "text": "formData",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "io_type",
        "code": "json",
        "text": "json",
        "sort": 4
    }
]

MOCK_SERVICE_TYPE_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "service_type",
        "code": "atomic",
        "text": "原子微服务",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "service_type",
        "code": "meta",
        "text": "元应用服务",
        "sort": 2
    }
]

MOCK_PERFORMANCE_METRIC_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "performance_metric",
        "code": "recall",
        "text": "查全率",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "performance_metric",
        "code": "precision",
        "text": "查准率",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "performance_metric",
        "code": "computation_efficiency",
        "text": "计算效率",
        "sort": 3
    }
]

MOCK_ATTRIBUTE_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "attribute",
        "code": "non_intelligent",
        "text": "非智能体服务",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "attribute",
        "code": "open_source",
        "text": "开源模型",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "attribute",
        "code": "paid",
        "text": "付费模型",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "attribute",
        "code": "custom",
        "text": "定制模型",
        "sort": 4
    }
]

# 跨境支付AI监测领域
MOCK_AML_INDUSTRY_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "aml_industry",
        "code": "0",
        "text": "金融风控",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aml_industry",
        "code": "1",
        "text": "自贸监管",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aml_industry",
        "code": "2",
        "text": "跨境贸易",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aml_industry",
        "code": "3",
        "text": "跨境电商",
        "sort": 4
    }
]

MOCK_AML_SCENARIO_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "aml_scenario",
        "code": "0",
        "text": "反洗钱",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aml_scenario",
        "code": "1",
        "text": "合规监测",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aml_scenario",
        "code": "2",
        "text": "税务稽查",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aml_scenario",
        "code": "3",
        "text": "业务统计",
        "sort": 4
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aml_scenario",
        "code": "4",
        "text": "信用评估",
        "sort": 5
    }
]

MOCK_AML_TECHNOLOGY_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "aml_technology",
        "code": "0",
        "text": "异常识别",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aml_technology",
        "code": "1",
        "text": "安全计算",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aml_technology",
        "code": "2",
        "text": "技术评测",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aml_technology",
        "code": "3",
        "text": "报告生成",
        "sort": 4
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aml_technology",
        "code": "4",
        "text": "配套技术",
        "sort": 5
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aml_technology",
        "code": "5",
        "text": "关联技术",
        "sort": 6
    }
]

# 无人飞机AI监控领域
MOCK_AIRCRAFT_INDUSTRY_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "aircraft_industry",
        "code": "0",
        "text": "城市治理",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aircraft_industry",
        "code": "1",
        "text": "文旅农林",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aircraft_industry",
        "code": "2",
        "text": "教育培训",
        "sort": 3
    }
]

MOCK_AIRCRAFT_SCENARIO_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "aircraft_scenario",
        "code": "0",
        "text": "应急救援",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aircraft_scenario",
        "code": "1",
        "text": "交通巡逻",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aircraft_scenario",
        "code": "2",
        "text": "低空物流",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aircraft_scenario",
        "code": "3",
        "text": "低空测绘",
        "sort": 4
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aircraft_scenario",
        "code": "4",
        "text": "目标识别",
        "sort": 5
    }
]

MOCK_AIRCRAFT_TECHNOLOGY_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "aircraft_technology",
        "code": "0",
        "text": "线路设计",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aircraft_technology",
        "code": "1",
        "text": "虚拟仿真",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aircraft_technology",
        "code": "2",
        "text": "智能感知",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aircraft_technology",
        "code": "3",
        "text": "远程控制",
        "sort": 4
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aircraft_technology",
        "code": "4",
        "text": "视频分析",
        "sort": 5
    },
    {
        "id": str(uuid.uuid4()),
        "category": "aircraft_technology",
        "code": "5",
        "text": "技术评价",
        "sort": 6
    }
]

# 乡村医疗AI服务领域
MOCK_HEALTH_INDUSTRY_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "health_industry",
        "code": "0",
        "text": "基层医疗卫生",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "health_industry",
        "code": "1",
        "text": "公共卫生管理",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "health_industry",
        "code": "2",
        "text": "医疗设备制造",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "health_industry",
        "code": "3",
        "text": "医疗保险服务",
        "sort": 4
    }
]

MOCK_HEALTH_SCENARIO_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "health_scenario",
        "code": "0",
        "text": "远程会诊支持",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "health_scenario",
        "code": "1",
        "text": "基层疾病筛查",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "health_scenario",
        "code": "2",
        "text": "慢性病管理",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "health_scenario",
        "code": "3",
        "text": "急诊分诊",
        "sort": 4
    },
    {
        "id": str(uuid.uuid4()),
        "category": "health_scenario",
        "code": "4",
        "text": "预防保健",
        "sort": 5
    }
]

MOCK_HEALTH_TECHNOLOGY_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "health_technology",
        "code": "0",
        "text": "计算机视觉",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "health_technology",
        "code": "1",
        "text": "自然语言处理",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "health_technology",
        "code": "2",
        "text": "时序数据分析",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "health_technology",
        "code": "3",
        "text": "强化学习",
        "sort": 4
    },
    {
        "id": str(uuid.uuid4()),
        "category": "health_technology",
        "code": "4",
        "text": "联邦学习",
        "sort": 5
    }
]

# 数字农业AI服务领域
MOCK_AGRICULTURE_INDUSTRY_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "agriculture_industry",
        "code": "0",
        "text": "智慧种植",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "agriculture_industry",
        "code": "1",
        "text": "畜牧养殖",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "agriculture_industry",
        "code": "2",
        "text": "农产品流通",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "agriculture_industry",
        "code": "3",
        "text": "乡村治理",
        "sort": 4
    }
]

MOCK_AGRICULTURE_SCENARIO_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "agriculture_scenario",
        "code": "0",
        "text": "精准播种",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "agriculture_scenario",
        "code": "1",
        "text": "病虫害防治",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "agriculture_scenario",
        "code": "2",
        "text": "智能灌溉",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "agriculture_scenario",
        "code": "3",
        "text": "产量预测",
        "sort": 4
    },
    {
        "id": str(uuid.uuid4()),
        "category": "agriculture_scenario",
        "code": "4",
        "text": "质量溯源",
        "sort": 5
    }
]

MOCK_AGRICULTURE_TECHNOLOGY_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "agriculture_technology",
        "code": "0",
        "text": "计算机视觉",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "agriculture_technology",
        "code": "1",
        "text": "自然语言处理",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "agriculture_technology",
        "code": "2",
        "text": "时序分析与预测",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "agriculture_technology",
        "code": "3",
        "text": "多模态融合",
        "sort": 4
    },
    {
        "id": str(uuid.uuid4()),
        "category": "agriculture_technology",
        "code": "4",
        "text": "联邦学习",
        "sort": 5
    }
]

# 低空飞行AI应用领域
MOCK_EVTOL_INDUSTRY_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "evtol_industry",
        "code": "0",
        "text": "城市空中交通",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "evtol_industry",
        "code": "1",
        "text": "物流配送",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "evtol_industry",
        "code": "2",
        "text": "紧急救援与医疗",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "evtol_industry",
        "code": "3",
        "text": "文旅与低空旅游",
        "sort": 4
    }
]

MOCK_EVTOL_SCENARIO_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "evtol_scenario",
        "code": "0",
        "text": "飞行路径规划",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "evtol_scenario",
        "code": "1",
        "text": "乘客服务与交互",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "evtol_scenario",
        "code": "2",
        "text": "航空器控制",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "evtol_scenario",
        "code": "3",
        "text": "安全监控与维护",
        "sort": 4
    },
    {
        "id": str(uuid.uuid4()),
        "category": "evtol_scenario",
        "code": "4",
        "text": "能源与电池管理",
        "sort": 5
    }
]

MOCK_EVTOL_TECHNOLOGY_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "evtol_technology",
        "code": "0",
        "text": "强化学习",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "evtol_technology",
        "code": "1",
        "text": "计算机视觉",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "evtol_technology",
        "code": "2",
        "text": "多模态融合",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "evtol_technology",
        "code": "3",
        "text": "时序预测",
        "sort": 4
    },
    {
        "id": str(uuid.uuid4()),
        "category": "evtol_technology",
        "code": "4",
        "text": "图搜索算法",
        "sort": 5
    },
    {
        "id": str(uuid.uuid4()),
        "category": "evtol_technology",
        "code": "5",
        "text": "深度学习",
        "sort": 6
    }
]

# 跨境电商AI应用领域
MOCK_ECOMMERCE_INDUSTRY_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "ecommerce_industry",
        "code": "0",
        "text": "跨境营销与广告",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "ecommerce_industry",
        "code": "1",
        "text": "客户服务与沟通",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "ecommerce_industry",
        "code": "2",
        "text": "选品与产品开发",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "ecommerce_industry",
        "code": "3",
        "text": "合规与风险管理",
        "sort": 4
    }
]

MOCK_ECOMMERCE_SCENARIO_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "ecommerce_scenario",
        "code": "0",
        "text": "多语言翻译与本地化",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "ecommerce_scenario",
        "code": "1",
        "text": "智能客服与互动",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "ecommerce_scenario",
        "code": "2",
        "text": "内容生成与优化",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "ecommerce_scenario",
        "code": "3",
        "text": "数据分析与决策支持",
        "sort": 4
    }
]

MOCK_ECOMMERCE_TECHNOLOGY_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "ecommerce_technology",
        "code": "0",
        "text": "自然语言处理",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "ecommerce_technology",
        "code": "1",
        "text": "计算机视觉",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "ecommerce_technology",
        "code": "2",
        "text": "推荐系统",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "ecommerce_technology",
        "code": "3",
        "text": "供应链优化",
        "sort": 4
    },
    {
        "id": str(uuid.uuid4()),
        "category": "ecommerce_technology",
        "code": "4",
        "text": "多模态大模型",
        "sort": 5
    },
    {
        "id": str(uuid.uuid4()),
        "category": "ecommerce_technology",
        "code": "5",
        "text": "深度学习",
        "sort": 6
    }
]

# 家庭陪伴AI应用领域
MOCK_HOME_AI_INDUSTRY_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "home_ai_industry",
        "code": "0",
        "text": "智能家居",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "home_ai_industry",
        "code": "1",
        "text": "健康管理",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "home_ai_industry",
        "code": "2",
        "text": "安防与应急",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "home_ai_industry",
        "code": "3",
        "text": "情感陪伴",
        "sort": 4
    },
    {
        "id": str(uuid.uuid4()),
        "category": "home_ai_industry",
        "code": "4",
        "text": "家务处理",
        "sort": 5
    }
]

MOCK_HOME_AI_SCENARIO_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "home_ai_scenario",
        "code": "0",
        "text": "家务处理场景",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "home_ai_scenario",
        "code": "1",
        "text": "疾病诊断场景",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "home_ai_scenario",
        "code": "2",
        "text": "应急联络场景",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "home_ai_scenario",
        "code": "3",
        "text": "来客接待场景",
        "sort": 4
    },
    {
        "id": str(uuid.uuid4()),
        "category": "home_ai_scenario",
        "code": "4",
        "text": "情感陪伴场景",
        "sort": 5
    }
]

MOCK_HOME_AI_TECHNOLOGY_DICTIONARIES = [
    {
        "id": str(uuid.uuid4()),
        "category": "home_ai_technology",
        "code": "0",
        "text": "计算机视觉",
        "sort": 1
    },
    {
        "id": str(uuid.uuid4()),
        "category": "home_ai_technology",
        "code": "1",
        "text": "自然语言处理",
        "sort": 2
    },
    {
        "id": str(uuid.uuid4()),
        "category": "home_ai_technology",
        "code": "2",
        "text": "强化学习",
        "sort": 3
    },
    {
        "id": str(uuid.uuid4()),
        "category": "home_ai_technology",
        "code": "3",
        "text": "多传感器融合",
        "sort": 4
    },
    {
        "id": str(uuid.uuid4()),
        "category": "home_ai_technology",
        "code": "4",
        "text": "具身智能",
        "sort": 5
    },
    {
        "id": str(uuid.uuid4()),
        "category": "home_ai_technology",
        "code": "5",
        "text": "多模态技术",
        "sort": 6
    }
]

# 合并所有字典数据
MOCK_DICTIONARIES = (
    MOCK_STATUS_DICTIONARIES
    + MOCK_NORM_DICTIONARIES
    + MOCK_API_TYPE_DICTIONARIES
    + MOCK_METHOD_TYPE_DICTIONARIES
    + MOCK_IO_TYPE_DICTIONARIES
    + MOCK_SERVICE_TYPE_DICTIONARIES
    + MOCK_PERFORMANCE_METRIC_DICTIONARIES
    + MOCK_ATTRIBUTE_DICTIONARIES
    + MOCK_AML_INDUSTRY_DICTIONARIES
    + MOCK_AML_SCENARIO_DICTIONARIES
    + MOCK_AML_TECHNOLOGY_DICTIONARIES
    + MOCK_AIRCRAFT_INDUSTRY_DICTIONARIES
    + MOCK_AIRCRAFT_SCENARIO_DICTIONARIES
    + MOCK_AIRCRAFT_TECHNOLOGY_DICTIONARIES
    + MOCK_HEALTH_INDUSTRY_DICTIONARIES
    + MOCK_HEALTH_SCENARIO_DICTIONARIES
    + MOCK_HEALTH_TECHNOLOGY_DICTIONARIES
    + MOCK_AGRICULTURE_INDUSTRY_DICTIONARIES
    + MOCK_AGRICULTURE_SCENARIO_DICTIONARIES
    + MOCK_AGRICULTURE_TECHNOLOGY_DICTIONARIES
    + MOCK_EVTOL_INDUSTRY_DICTIONARIES
    + MOCK_EVTOL_SCENARIO_DICTIONARIES
    + MOCK_EVTOL_TECHNOLOGY_DICTIONARIES
    + MOCK_ECOMMERCE_INDUSTRY_DICTIONARIES
    + MOCK_ECOMMERCE_SCENARIO_DICTIONARIES
    + MOCK_ECOMMERCE_TECHNOLOGY_DICTIONARIES
    + MOCK_HOME_AI_INDUSTRY_DICTIONARIES
    + MOCK_HOME_AI_SCENARIO_DICTIONARIES
    + MOCK_HOME_AI_TECHNOLOGY_DICTIONARIES
)
