"""
字典示例数据
"""

# 领域分类字典
MOCK_DOMAIN_DICTIONARIES = [
    {
        "category": "domain",
        "code": "aml",
        "text": "跨境支付AI监测",
        "sort": 1
    },
    {
        "category": "domain",
        "code": "aircraft",
        "text": "无人飞机AI监控",
        "sort": 2
    },
    {
        "category": "domain",
        "code": "health",
        "text": "乡村医疗AI应用",
        "sort": 3
    },
    {
        "category": "domain",
        "code": "agriculture",
        "text": "数字农业AI应用",
        "sort": 4
    },
    {
        "category": "domain",
        "code": "evtol",
        "text": "低空飞行AI应用",
        "sort": 5
    },
    {
        "category": "domain",
        "code": "ecommerce",
        "text": "跨境电商AI应用",
        "sort": 6
    },
    {
        "category": "domain",
        "code": "homeAI",
        "text": "家庭陪伴AI应用",
        "sort": 7
    }
]

# 通用字典数据
MOCK_STATUS_DICTIONARIES = [
    {
        "category": "status",
        "code": "not_deployed",
        "text": "未部署",
        "sort": 1
    },
    {
        "category": "status",
        "code": "deploying",
        "text": "部署中",
        "sort": 2
    },
    {
        "category": "status",
        "code": "pre_release_unrated",
        "text": "预发布(未测评)",
        "sort": 3
    },
    {
        "category": "status",
        "code": "pre_release_pending",
        "text": "预发布(待平台测评)",
        "sort": 4
    },
    {
        "category": "status",
        "code": "released",
        "text": "已发布",
        "sort": 5
    },
    {
        "category": "status",
        "code": "error",
        "text": "服务异常",
        "sort": 6
    }
]

MOCK_STATUS_STYLE_DICTIONARIES = [
    {
        "category": "status_style",
        "code": "pre_release_unrated",
        "text": "warning",
        "sort": 1
    },
    {
        "category": "status_style",
        "code": "pre_release_pending",
        "text": "warning",
        "sort": 1
    },
    {
        "category": "status_style",
        "code": "not_deployed",
        "text": "default",
        "sort": 2
    },
    {
        "category": "status_style",
        "code": "error",
        "text": "error",
        "sort": 3
    },
    {
        "category": "status_style",
        "code": "released",
        "text": "success",
        "sort": 4
    },
    {
        "category": "status_style",
        "code": "deploying",
        "text": "processing",
        "sort": 5
    }
]

MOCK_NORM_DICTIONARIES = [
    {
        "category": "norm",
        "code": "safety-fingerprint",
        "text": "安全性-指纹",
        "sort": 1
    },
    {
        "category": "norm",
        "code": "safety-watermark",
        "text": "安全性-水印",
        "sort": 2
    },
    {
        "category": "norm",
        "code": "robustness",
        "text": "鲁棒性",
        "sort": 3
    },
    {
        "category": "norm",
        "code": "fairness",
        "text": "公平性",
        "sort": 4
    },
    {
        "category": "norm",
        "code": "privacy",
        "text": "隐私性",
        "sort": 5
    },
    {
        "category": "norm",
        "code": "explainability",
        "text": "可解释性",
        "sort": 6
    }
]

MOCK_API_TYPE_DICTIONARIES = [
    {
        "category": "api_type",
        "code": "restful",
        "text": "RESTful API",
        "sort": 1
    },
    {
        "category": "api_type",
        "code": "graphql",
        "text": "GraphQL API",
        "sort": 2
    },
    {
        "category": "api_type",
        "code": "websocket",
        "text": "WebSocket API",
        "sort": 3
    }
]

MOCK_METHOD_TYPE_DICTIONARIES = [
    {
        "category": "method_type",
        "code": "get",
        "text": "GET",
        "sort": 1
    },
    {
        "category": "method_type",
        "code": "post",
        "text": "POST",
        "sort": 2
    },
    {
        "category": "method_type",
        "code": "put",
        "text": "PUT",
        "sort": 3
    },
    {
        "category": "method_type",
        "code": "delete",
        "text": "DELETE",
        "sort": 4
    }
]

MOCK_IO_TYPE_DICTIONARIES = [
    {
        "category": "io_type",
        "code": "none",
        "text": "none",
        "sort": 1
    },
    {
        "category": "io_type",
        "code": "string",
        "text": "string",
        "sort": 2
    },
    {
        "category": "io_type",
        "code": "formdata",
        "text": "formData",
        "sort": 3
    },
    {
        "category": "io_type",
        "code": "json",
        "text": "json",
        "sort": 4
    }
]

MOCK_SERVICE_TYPE_DICTIONARIES = [
        {
        "category": "service_type",
        "code": "atomic",
        "text": "原子微服务-REST",
        "sort": 1
    },
    {
        "category": "service_type",
        "code": "meta",
        "text": "元应用服务",
        "sort": 2
    },
    {
        "category": "service_type",
        "code": "atomic_mcp",
        "text": "原子微服务-MCP",
        "sort": 3
    },
    {
        "category": "service_type",
        "code": "generated_algorithm",
        "text": "想定式生成算法",
        "sort": 4
    },
]

MOCK_PERFORMANCE_METRIC_DICTIONARIES = [
    {
        "category": "performance_metric",
        "code": "recall",
        "text": "查全率",
        "sort": 1
    },
    {
        "category": "performance_metric",
        "code": "precision",
        "text": "查准率",
        "sort": 2
    },
    {
        "category": "performance_metric",
        "code": "computation_efficiency",
        "text": "计算效率",
        "sort": 3
    }
]

MOCK_ATTRIBUTE_DICTIONARIES = [
    {
        "category": "attribute",
        "code": "non_intelligent",
        "text": "非智能体服务",
        "sort": 1
    },
    {
        "category": "attribute",
        "code": "open_source",
        "text": "开源模型",
        "sort": 2
    },
    {
        "category": "attribute",
        "code": "paid",
        "text": "付费模型",
        "sort": 3
    },
    {
        "category": "attribute",
        "code": "custom",
        "text": "定制模型",
        "sort": 4
    }
]

# 跨境支付AI监测领域
MOCK_AML_INDUSTRY_DICTIONARIES = [
    {
        "category": "aml_industry",
        "code": "0",
        "text": "金融风控",
        "sort": 1
    },
    {
        "category": "aml_industry",
        "code": "1",
        "text": "自贸监管",
        "sort": 2
    },
    {
        "category": "aml_industry",
        "code": "2",
        "text": "跨境贸易",
        "sort": 3
    },
    {
        "category": "aml_industry",
        "code": "3",
        "text": "跨境电商",
        "sort": 4
    }
]

MOCK_AML_SCENARIO_DICTIONARIES = [
    {
        "category": "aml_scenario",
        "code": "0",
        "text": "反洗钱",
        "sort": 1
    },
    {
        "category": "aml_scenario",
        "code": "1",
        "text": "合规监测",
        "sort": 2
    },
    {
        "category": "aml_scenario",
        "code": "2",
        "text": "税务稽查",
        "sort": 3
    },
    {
        "category": "aml_scenario",
        "code": "3",
        "text": "业务统计",
        "sort": 4
    },
    {
        "category": "aml_scenario",
        "code": "4",
        "text": "信用评估",
        "sort": 5
    }
]

MOCK_AML_TECHNOLOGY_DICTIONARIES = [
    {
        "category": "aml_technology",
        "code": "0",
        "text": "异常识别",
        "sort": 1
    },
    {
        "category": "aml_technology",
        "code": "1",
        "text": "安全计算",
        "sort": 2
    },
    {
        "category": "aml_technology",
        "code": "2",
        "text": "技术评测",
        "sort": 3
    },
    {
        "category": "aml_technology",
        "code": "3",
        "text": "报告生成",
        "sort": 4
    },
    {
        "category": "aml_technology",
        "code": "4",
        "text": "配套技术",
        "sort": 5
    },
    {
        "category": "aml_technology",
        "code": "5",
        "text": "关联技术",
        "sort": 6
    }
]

# 无人飞机AI监控领域
MOCK_AIRCRAFT_INDUSTRY_DICTIONARIES = [
    {
        "category": "aircraft_industry",
        "code": "0",
        "text": "城市治理",
        "sort": 1
    },
    {
        "category": "aircraft_industry",
        "code": "1",
        "text": "文旅农林",
        "sort": 2
    },
    {
        "category": "aircraft_industry",
        "code": "2",
        "text": "教育培训",
        "sort": 3
    }
]

MOCK_AIRCRAFT_SCENARIO_DICTIONARIES = [
    {
        "category": "aircraft_scenario",
        "code": "0",
        "text": "应急救援",
        "sort": 1
    },
    {
        "category": "aircraft_scenario",
        "code": "1",
        "text": "交通巡逻",
        "sort": 2
    },
    {
        "category": "aircraft_scenario",
        "code": "2",
        "text": "低空物流",
        "sort": 3
    },
    {
        "category": "aircraft_scenario",
        "code": "3",
        "text": "低空测绘",
        "sort": 4
    },
    {
        "category": "aircraft_scenario",
        "code": "4",
        "text": "目标识别",
        "sort": 5
    }
]

MOCK_AIRCRAFT_TECHNOLOGY_DICTIONARIES = [
    {
        "category": "aircraft_technology",
        "code": "0",
        "text": "线路设计",
        "sort": 1
    },
    {
        "category": "aircraft_technology",
        "code": "1",
        "text": "虚拟仿真",
        "sort": 2
    },
    {
        "category": "aircraft_technology",
        "code": "2",
        "text": "智能感知",
        "sort": 3
    },
    {
        "category": "aircraft_technology",
        "code": "3",
        "text": "远程控制",
        "sort": 4
    },
    {
        "category": "aircraft_technology",
        "code": "4",
        "text": "视频分析",
        "sort": 5
    },
    {
        "category": "aircraft_technology",
        "code": "5",
        "text": "技术评价",
        "sort": 6
    }
]

# 乡村医疗AI服务领域
MOCK_HEALTH_INDUSTRY_DICTIONARIES = [
    {
        "category": "health_industry",
        "code": "0",
        "text": "基层医疗卫生",
        "sort": 1
    },
    {
        "category": "health_industry",
        "code": "1",
        "text": "公共卫生管理",
        "sort": 2
    },
    {
        "category": "health_industry",
        "code": "2",
        "text": "医疗设备制造",
        "sort": 3
    },
    {
        "category": "health_industry",
        "code": "3",
        "text": "医疗保险服务",
        "sort": 4
    }
]

MOCK_HEALTH_SCENARIO_DICTIONARIES = [
    {
        "category": "health_scenario",
        "code": "0",
        "text": "远程会诊支持",
        "sort": 1
    },
    {
        "category": "health_scenario",
        "code": "1",
        "text": "基层疾病筛查",
        "sort": 2
    },
    {
        "category": "health_scenario",
        "code": "2",
        "text": "慢性病管理",
        "sort": 3
    },
    {
        "category": "health_scenario",
        "code": "3",
        "text": "急诊分诊",
        "sort": 4
    },
    {
        "category": "health_scenario",
        "code": "4",
        "text": "预防保健",
        "sort": 5
    }
]

MOCK_HEALTH_TECHNOLOGY_DICTIONARIES = [
    {
        "category": "health_technology",
        "code": "0",
        "text": "计算机视觉",
        "sort": 1
    },
    {
        "category": "health_technology",
        "code": "1",
        "text": "自然语言处理",
        "sort": 2
    },
    {
        "category": "health_technology",
        "code": "2",
        "text": "时序数据分析",
        "sort": 3
    },
    {
        "category": "health_technology",
        "code": "3",
        "text": "强化学习",
        "sort": 4
    },
    {
        "category": "health_technology",
        "code": "4",
        "text": "联邦学习",
        "sort": 5
    }
]

# 数字农业AI服务领域
MOCK_AGRICULTURE_INDUSTRY_DICTIONARIES = [
    {
        "category": "agriculture_industry",
        "code": "0",
        "text": "智慧种植",
        "sort": 1
    },
    {
        "category": "agriculture_industry",
        "code": "1",
        "text": "畜牧养殖",
        "sort": 2
    },
    {
        "category": "agriculture_industry",
        "code": "2",
        "text": "农产品流通",
        "sort": 3
    },
    {
        "category": "agriculture_industry",
        "code": "3",
        "text": "乡村治理",
        "sort": 4
    }
]

MOCK_AGRICULTURE_SCENARIO_DICTIONARIES = [
    {
        "category": "agriculture_scenario",
        "code": "0",
        "text": "精准播种",
        "sort": 1
    },
    {
        "category": "agriculture_scenario",
        "code": "1",
        "text": "病虫害防治",
        "sort": 2
    },
    {
        "category": "agriculture_scenario",
        "code": "2",
        "text": "智能灌溉",
        "sort": 3
    },
    {
        "category": "agriculture_scenario",
        "code": "3",
        "text": "产量预测",
        "sort": 4
    },
    {
        "category": "agriculture_scenario",
        "code": "4",
        "text": "质量溯源",
        "sort": 5
    }
]

MOCK_AGRICULTURE_TECHNOLOGY_DICTIONARIES = [
    {
        "category": "agriculture_technology",
        "code": "0",
        "text": "计算机视觉",
        "sort": 1
    },
    {
        "category": "agriculture_technology",
        "code": "1",
        "text": "自然语言处理",
        "sort": 2
    },
    {
        "category": "agriculture_technology",
        "code": "2",
        "text": "时序分析与预测",
        "sort": 3
    },
    {
        "category": "agriculture_technology",
        "code": "3",
        "text": "多模态融合",
        "sort": 4
    },
    {
        "category": "agriculture_technology",
        "code": "4",
        "text": "联邦学习",
        "sort": 5
    }
]

# 低空飞行AI应用领域
MOCK_EVTOL_INDUSTRY_DICTIONARIES = [
    {
        "category": "evtol_industry",
        "code": "0",
        "text": "城市空中交通",
        "sort": 1
    },
    {
        "category": "evtol_industry",
        "code": "1",
        "text": "物流配送",
        "sort": 2
    },
    {
        "category": "evtol_industry",
        "code": "2",
        "text": "紧急救援与医疗",
        "sort": 3
    },
    {
        "category": "evtol_industry",
        "code": "3",
        "text": "文旅与低空旅游",
        "sort": 4
    }
]

MOCK_EVTOL_SCENARIO_DICTIONARIES = [
    {
        "category": "evtol_scenario",
        "code": "0",
        "text": "飞行路径规划",
        "sort": 1
    },
    {
        "category": "evtol_scenario",
        "code": "1",
        "text": "乘客服务与交互",
        "sort": 2
    },
    {
        "category": "evtol_scenario",
        "code": "2",
        "text": "航空器控制",
        "sort": 3
    },
    {
        "category": "evtol_scenario",
        "code": "3",
        "text": "安全监控与维护",
        "sort": 4
    },
    {
        "category": "evtol_scenario",
        "code": "4",
        "text": "能源与电池管理",
        "sort": 5
    }
]

MOCK_EVTOL_TECHNOLOGY_DICTIONARIES = [
    {
        "category": "evtol_technology",
        "code": "0",
        "text": "强化学习",
        "sort": 1
    },
    {
        "category": "evtol_technology",
        "code": "1",
        "text": "计算机视觉",
        "sort": 2
    },
    {
        "category": "evtol_technology",
        "code": "2",
        "text": "多模态融合",
        "sort": 3
    },
    {
        "category": "evtol_technology",
        "code": "3",
        "text": "时序预测",
        "sort": 4
    },
    {
        "category": "evtol_technology",
        "code": "4",
        "text": "图搜索算法",
        "sort": 5
    },
    {
        "category": "evtol_technology",
        "code": "5",
        "text": "深度学习",
        "sort": 6
    }
]

# 跨境电商AI应用领域
MOCK_ECOMMERCE_INDUSTRY_DICTIONARIES = [
    {
        "category": "ecommerce_industry",
        "code": "0",
        "text": "跨境营销与广告",
        "sort": 1
    },
    {
        "category": "ecommerce_industry",
        "code": "1",
        "text": "客户服务与沟通",
        "sort": 2
    },
    {
        "category": "ecommerce_industry",
        "code": "2",
        "text": "选品与产品开发",
        "sort": 3
    },
    {
        "category": "ecommerce_industry",
        "code": "3",
        "text": "合规与风险管理",
        "sort": 4
    }
]

MOCK_ECOMMERCE_SCENARIO_DICTIONARIES = [
    {
        "category": "ecommerce_scenario",
        "code": "0",
        "text": "多语言翻译与本地化",
        "sort": 1
    },
    {
        "category": "ecommerce_scenario",
        "code": "1",
        "text": "智能客服与互动",
        "sort": 2
    },
    {
        "category": "ecommerce_scenario",
        "code": "2",
        "text": "内容生成与优化",
        "sort": 3
    },
    {
        "category": "ecommerce_scenario",
        "code": "3",
        "text": "数据分析与决策支持",
        "sort": 4
    }
]

MOCK_ECOMMERCE_TECHNOLOGY_DICTIONARIES = [
    {
        "category": "ecommerce_technology",
        "code": "0",
        "text": "自然语言处理",
        "sort": 1
    },
    {
        "category": "ecommerce_technology",
        "code": "1",
        "text": "计算机视觉",
        "sort": 2
    },
    {
        "category": "ecommerce_technology",
        "code": "2",
        "text": "推荐系统",
        "sort": 3
    },
    {
        "category": "ecommerce_technology",
        "code": "3",
        "text": "供应链优化",
        "sort": 4
    },
    {
        "category": "ecommerce_technology",
        "code": "4",
        "text": "多模态大模型",
        "sort": 5
    },
    {
        "category": "ecommerce_technology",
        "code": "5",
        "text": "深度学习",
        "sort": 6
    }
]

# 家庭陪伴AI应用领域
MOCK_HOMEAI_INDUSTRY_DICTIONARIES = [
    {
        "category": "homeAI_industry",
        "code": "0",
        "text": "智能家居",
        "sort": 1
    },
    {
        "category": "homeAI_industry",
        "code": "1",
        "text": "健康管理",
        "sort": 2
    },
    {
        "category": "homeAI_industry",
        "code": "2",
        "text": "安防与应急",
        "sort": 3
    },
    {
        "category": "homeAI_industry",
        "code": "3",
        "text": "情感陪伴",
        "sort": 4
    },
    {
        "category": "homeAI_industry",
        "code": "4",
        "text": "家务处理",
        "sort": 5
    }
]

MOCK_HOMEAI_SCENARIO_DICTIONARIES = [
    {
        "category": "homeAI_scenario",
        "code": "0",
        "text": "家务处理场景",
        "sort": 1
    },
    {
        "category": "homeAI_scenario",
        "code": "1",
        "text": "疾病诊断场景",
        "sort": 2
    },
    {
        "category": "homeAI_scenario",
        "code": "2",
        "text": "应急联络场景",
        "sort": 3
    },
    {
        "category": "homeAI_scenario",
        "code": "3",
        "text": "来客接待场景",
        "sort": 4
    },
    {
        "category": "homeAI_scenario",
        "code": "4",
        "text": "情感陪伴场景",
        "sort": 5
    }
]

MOCK_HOMEAI_TECHNOLOGY_DICTIONARIES = [
    {
        "category": "homeAI_technology",
        "code": "0",
        "text": "计算机视觉",
        "sort": 1
    },
    {
        "category": "homeAI_technology",
        "code": "1",
        "text": "自然语言处理",
        "sort": 2
    },
    {
        "category": "homeAI_technology",
        "code": "2",
        "text": "强化学习",
        "sort": 3
    },
    {
        "category": "homeAI_technology",
        "code": "3",
        "text": "多传感器融合",
        "sort": 4
    },
    {
        "category": "homeAI_technology",
        "code": "4",
        "text": "具身智能",
        "sort": 5
    },
    {
        "category": "homeAI_technology",
        "code": "5",
        "text": "多模态技术",
        "sort": 6
    }
]

# ==================== 算法类别与特定参数字典 ====================

MOCK_ALGORITHM_CATEGORY_DICTIONARIES = [
    {"category": "algorithm_category", "code": "classification", "text": "分类算法", "sort": 1},
    {"category": "algorithm_category", "code": "detection", "text": "检测算法", "sort": 2},
    {"category": "algorithm_category", "code": "regression", "text": "回归/预测算法", "sort": 3},
    {"category": "algorithm_category", "code": "clustering", "text": "聚类算法", "sort": 4},
    {"category": "algorithm_category", "code": "generation", "text": "生成算法", "sort": 5},
    {"category": "algorithm_category", "code": "recommendation", "text": "推荐算法", "sort": 6},
]

MOCK_ALGO_INPUT_TYPE_DICTIONARIES = [
    {"category": "algo_input_type", "code": "video_url", "text": "视频 URL", "sort": 1},
    {"category": "algo_input_type", "code": "image_url", "text": "图像 URL", "sort": 2},
    {"category": "algo_input_type", "code": "text", "text": "文本", "sort": 3},
    {"category": "algo_input_type", "code": "file_path", "text": "文件路径", "sort": 4},
    {"category": "algo_input_type", "code": "api_response", "text": "API 响应", "sort": 5},
    {"category": "algo_input_type", "code": "binary_data", "text": "二进制数据", "sort": 6},
    {"category": "algo_input_type", "code": "structured_data", "text": "结构化数据", "sort": 7},
    {"category": "algo_input_type", "code": "time_series", "text": "时序数据", "sort": 8},
    {"category": "algo_input_type", "code": "custom", "text": "自定义", "sort": 9},
]

MOCK_ALGO_CONSTRAINT_DICTIONARIES = [
    {"category": "algo_constraint", "code": "no_llm", "text": "不使用 LLM / 大语言模型", "sort": 1},
    {"category": "algo_constraint", "code": "no_training", "text": "不需要训练或微调", "sort": 2},
    {"category": "algo_constraint", "code": "no_gpu", "text": "不需要 GPU", "sort": 3},
    {"category": "algo_constraint", "code": "pretrained_only", "text": "仅使用预训练模型（推理模式）", "sort": 4},
    {"category": "algo_constraint", "code": "rule_based", "text": "纯规则 / 启发式方法", "sort": 5},
    {"category": "algo_constraint", "code": "single_file", "text": "单文件实现", "sort": 6},
]

# --- 分类算法特定参数 ---
MOCK_ALGO_CLASSIFICATION_OUTPUT_TYPE_DICTIONARIES = [
    {"category": "algo_classification_output_type", "code": "classification_label", "text": "分类标签", "sort": 1},
    {"category": "algo_classification_output_type", "code": "confidence_list", "text": "置信度列表", "sort": 2},
    {"category": "algo_classification_output_type", "code": "json_structure", "text": "JSON 结构", "sort": 3},
    {"category": "algo_classification_output_type", "code": "text_report", "text": "文本报告", "sort": 4},
]

# --- 检测算法特定参数 ---
MOCK_ALGO_DETECTION_TARGET_TYPE_DICTIONARIES = [
    {"category": "algo_detection_target_type", "code": "object", "text": "物体检测", "sort": 1},
    {"category": "algo_detection_target_type", "code": "anomaly", "text": "异常值检测", "sort": 2},
    {"category": "algo_detection_target_type", "code": "event", "text": "事件检测", "sort": 3},
    {"category": "algo_detection_target_type", "code": "defect", "text": "缺陷检测", "sort": 4},
    {"category": "algo_detection_target_type", "code": "face", "text": "人脸检测", "sort": 5},
    {"category": "algo_detection_target_type", "code": "text_region", "text": "文本区域检测", "sort": 6},
]

MOCK_ALGO_DETECTION_OUTPUT_FORMAT_DICTIONARIES = [
    {"category": "algo_detection_output_format", "code": "bounding_box", "text": "边界框坐标", "sort": 1},
    {"category": "algo_detection_output_format", "code": "confidence_score", "text": "置信度分数", "sort": 2},
    {"category": "algo_detection_output_format", "code": "anomaly_score", "text": "异常分数", "sort": 3},
    {"category": "algo_detection_output_format", "code": "detection_report", "text": "检测报告", "sort": 4},
]

# --- 回归/预测算法特定参数 ---
MOCK_ALGO_REGRESSION_TIME_GRANULARITY_DICTIONARIES = [
    {"category": "algo_regression_time_granularity", "code": "second", "text": "秒级", "sort": 1},
    {"category": "algo_regression_time_granularity", "code": "minute", "text": "分钟级", "sort": 2},
    {"category": "algo_regression_time_granularity", "code": "hour", "text": "小时级", "sort": 3},
    {"category": "algo_regression_time_granularity", "code": "day", "text": "天级", "sort": 4},
    {"category": "algo_regression_time_granularity", "code": "week", "text": "周级", "sort": 5},
    {"category": "algo_regression_time_granularity", "code": "month", "text": "月级", "sort": 6},
    {"category": "algo_regression_time_granularity", "code": "none", "text": "不涉及时序", "sort": 7},
]

MOCK_ALGO_REGRESSION_METRIC_DICTIONARIES = [
    {"category": "algo_regression_metric", "code": "mae", "text": "MAE", "sort": 1},
    {"category": "algo_regression_metric", "code": "rmse", "text": "RMSE", "sort": 2},
    {"category": "algo_regression_metric", "code": "r2", "text": "R²", "sort": 3},
    {"category": "algo_regression_metric", "code": "mape", "text": "MAPE", "sort": 4},
]

# --- 聚类算法特定参数 ---
MOCK_ALGO_CLUSTERING_METHOD_DICTIONARIES = [
    {"category": "algo_clustering_method", "code": "distance_based", "text": "基于距离", "sort": 1},
    {"category": "algo_clustering_method", "code": "density_based", "text": "基于密度", "sort": 2},
    {"category": "algo_clustering_method", "code": "hierarchical", "text": "基于层次", "sort": 3},
    {"category": "algo_clustering_method", "code": "model_based", "text": "基于模型", "sort": 4},
]

MOCK_ALGO_CLUSTERING_OUTPUT_FORMAT_DICTIONARIES = [
    {"category": "algo_clustering_output_format", "code": "cluster_labels", "text": "簇标签", "sort": 1},
    {"category": "algo_clustering_output_format", "code": "cluster_centers", "text": "聚类中心", "sort": 2},
    {"category": "algo_clustering_output_format", "code": "visualization", "text": "可视化图表", "sort": 3},
    {"category": "algo_clustering_output_format", "code": "cluster_report", "text": "聚类报告", "sort": 4},
]

# --- 生成算法特定参数 ---
MOCK_ALGO_GENERATION_TARGET_TYPE_DICTIONARIES = [
    {"category": "algo_generation_target_type", "code": "text", "text": "文本", "sort": 1},
    {"category": "algo_generation_target_type", "code": "image", "text": "图像", "sort": 2},
    {"category": "algo_generation_target_type", "code": "audio", "text": "音频", "sort": 3},
    {"category": "algo_generation_target_type", "code": "structured_data", "text": "结构化数据", "sort": 4},
    {"category": "algo_generation_target_type", "code": "code", "text": "代码", "sort": 5},
]

MOCK_ALGO_GENERATION_QUALITY_DICTIONARIES = [
    {"category": "algo_generation_quality", "code": "diversity_first", "text": "多样性优先", "sort": 1},
    {"category": "algo_generation_quality", "code": "quality_first", "text": "质量优先", "sort": 2},
    {"category": "algo_generation_quality", "code": "speed_first", "text": "速度优先", "sort": 3},
]

# --- 推荐算法特定参数 ---
MOCK_ALGO_RECOMMENDATION_STRATEGY_DICTIONARIES = [
    {"category": "algo_recommendation_strategy", "code": "collaborative_filtering", "text": "协同过滤", "sort": 1},
    {"category": "algo_recommendation_strategy", "code": "content_based", "text": "基于内容", "sort": 2},
    {"category": "algo_recommendation_strategy", "code": "hybrid", "text": "混合推荐", "sort": 3},
    {"category": "algo_recommendation_strategy", "code": "knowledge_graph", "text": "基于知识图谱", "sort": 4},
]


# 合并所有字典数据
MOCK_DICTIONARIES = (
    MOCK_STATUS_DICTIONARIES
    + MOCK_STATUS_STYLE_DICTIONARIES
    + MOCK_NORM_DICTIONARIES
    + MOCK_API_TYPE_DICTIONARIES
    + MOCK_METHOD_TYPE_DICTIONARIES
    + MOCK_IO_TYPE_DICTIONARIES
    + MOCK_SERVICE_TYPE_DICTIONARIES
    + MOCK_PERFORMANCE_METRIC_DICTIONARIES
    + MOCK_ATTRIBUTE_DICTIONARIES
    + MOCK_DOMAIN_DICTIONARIES
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
    + MOCK_HOMEAI_INDUSTRY_DICTIONARIES
    + MOCK_HOMEAI_SCENARIO_DICTIONARIES
    + MOCK_HOMEAI_TECHNOLOGY_DICTIONARIES
    + MOCK_ALGORITHM_CATEGORY_DICTIONARIES
    + MOCK_ALGO_INPUT_TYPE_DICTIONARIES
    + MOCK_ALGO_CONSTRAINT_DICTIONARIES
    + MOCK_ALGO_CLASSIFICATION_OUTPUT_TYPE_DICTIONARIES
    + MOCK_ALGO_DETECTION_TARGET_TYPE_DICTIONARIES
    + MOCK_ALGO_DETECTION_OUTPUT_FORMAT_DICTIONARIES
    + MOCK_ALGO_REGRESSION_TIME_GRANULARITY_DICTIONARIES
    + MOCK_ALGO_REGRESSION_METRIC_DICTIONARIES
    + MOCK_ALGO_CLUSTERING_METHOD_DICTIONARIES
    + MOCK_ALGO_CLUSTERING_OUTPUT_FORMAT_DICTIONARIES
    + MOCK_ALGO_GENERATION_TARGET_TYPE_DICTIONARIES
    + MOCK_ALGO_GENERATION_QUALITY_DICTIONARIES
    + MOCK_ALGO_RECOMMENDATION_STRATEGY_DICTIONARIES
)
