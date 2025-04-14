API_IDS = {
    "predict": "e04e0165-3b18-4d54-ae38-659d04f8aef5",
    "healthCheck": "b90b04e2-2ca9-493c-b165-82d1b7f90574",
    "train": "fb9e80f7-9aad-4ee5-a620-131decf37bec",
    "getReportData": "2df635e5-4281-4cbf-832f-006175c6a1ad",
    "sendReport": "590017b7-fa60-4d07-a7e9-d668b32e033b",
    "generateReport": "eebfb433-46e7-477a-9abb-057ef90daacd",
    "preprocess": "b4f21aaa-6280-49b4-8db6-b8d7e4561df2",
    "evaluate": "f49b20ec-dfab-4ca7-a462-fa2c07a5f919",
    "visualize": "0a92bf34-5b57-497f-b5d2-6facadda0469",
    "generate-report": "c8f9b07b-b7bb-47e9-ade9-17937dda65c3",
    "nl2gql": "78a9058c-affa-4af2-9ec5-af12e5eef50d",
    "safety-fingerprint": "e59e68c3-3d03-4e36-b6ce-71673b261005",
    "技术评测元应用": "d5475ad3-d6ce-437c-bfc5-c1e3e8639301",
    "无人机智能投递": "83ed1e7d-3be4-4e15-b23f-44df74d59e35",
    "calculate": "c35b0b2c-2b11-4279-914e-e6e751f8e00a",
    "diagnose": "37dc651e-1559-44b9-8fbf-a23e96b41b23",
    "analyze": "c3b1cfa6-9c0a-49d4-86ed-99c9ce5319bd",
    "alert": "dc1b1514-f05a-449a-ae67-84143636d1a1",
    "transcribe": "eb71aac4-245e-42ef-9f45-a15febac7054",
    "allocate": "11850741-9979-4a5b-ae18-75dd8b2199e6",
    "乡村医疗AI辅助诊断元应用": "199c0645-a55f-45ff-a09c-5e535e091534",
    "农村公共卫生监测元应用": "17043d06-188f-4909-b32d-cbbbb7680a64",
    "analyzeImage": "4b71974a-2d65-412a-b25d-13c0924d1abb",
    "identifyDisease": "3d939529-0043-4b2f-a906-2dc5714dc84d",
    "getIrrigationPlan": "0f5179d4-3bc7-4c0e-9bac-cb2a97c5386e",
    "predictYield": "fa339134-1472-4421-bed3-2e516ef14156",
    "智慧农业综合管理元应用": "8a4765d9-a024-473d-bd01-6cefc07d2081",
    "pathPlanner": "f7b3a3a6-ae2a-4e0a-9764-6ab98605d592",
    "environmentPerception": "bcb8d724-5b02-4729-b61f-d36e4802eaa1",
    "obstacleDetection": "a22ff83e-009e-40ea-a658-5300d6d25e11",
    "flightController": "2f6e70a5-ff4a-4bae-be66-b7adf0d4d47c",
    "batteryManager": "36ef2f7e-3dab-479c-a6fb-a04dcc04e54c",
    "energyOptimizer": "ec3fc278-2d77-4c52-a5e9-55a7c2ab9536",
    "safetyMonitor": "3417f66a-dffb-449e-94f2-32634e6c0675",
    "eVTOL智能飞行控制元应用": "3c7df4ef-609b-4353-af9e-ee6e8ddc752e",
    "translateContent": "16741c61-7457-4ba5-a8e5-1eb84ab9b8c0",
    "generateDescription": "0c242c60-e1d2-417f-9385-f4c7c90140c7",
    "analyzeTrend": "85c17132-3534-4a85-9845-fd55dfb81989",
    "predictSales": "a93fe785-e984-4c95-9f09-3cc6f052834e",
    "跨境电商智能营销元应用": "7369ae9e-780f-4d19-9a21-f138dda5b9a6",
    "objectDetection": "628f8e15-1139-42d2-9057-3baa6cb592e2",
    "spatialMapping": "cb618d37-f215-44b8-a7b7-8346147b901b",
    "naturalLanguageUnderstanding": "e5fcbf58-80bb-4b52-a606-5a80296e0c8e",
    "emotionRecognition": "225ea76e-44a5-486c-94cc-58e15e5b4606",
    "vitalSignsMonitor": "e4562ca9-bb85-424f-8c30-68c16b2a3e94",
    "abnormalBehaviorDetection": "9e0d6410-4fb5-408f-9eb8-1b5473809b42",
    "taskPlanner": "7295b267-8a30-4675-a73e-652ecd94f786",
    "pathPlanning": "87c2c1d3-4339-47b1-bcf8-7a74ecfbcec6",
    "家庭智能助手元应用": "20474c78-8753-4508-bc99-d7f56a11b1c6",
}

# MOCK_SERVICES 数据
MOCK_SERVICES = [
    {
        "id": "8438c51b-4f31-4f44-91b1-f805ff4f5b39",
        "name": "课题一风险识别模型推理微服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "aml",
        "industry": "0",
        "scenario": "1",
        "technology": "1",
        "network": "bridge",
        "port": "0.0.0.0:8000/TCP → 0.0.0.0:80000",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/aml/data",
        "status": "success",
        "number": 512,
        "deleted": 0,
        "create_time": 1744631575306,
        "creator_id": ""
    },
    {
        "id": "924dc60b-4866-45f2-bd19-f98af257cf6c",
        "name": "课题二多方安全计算模型推理微服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "aml",
        "industry": "0",
        "scenario": "1",
        "technology": "1",
        "network": "bridge",
        "port": "0.0.0.0:8000/TCP → 0.0.0.0:80000",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/aml/data",
        "status": "success",
        "number": 512,
        "deleted": 0,
        "create_time": 1744631575306,
        "creator_id": ""
    },
    {
        "id": "c27fe536-7ac5-413a-84ca-09b6fe218659",
        "name": "技术评测微服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "aml",
        "industry": "1",
        "scenario": "2",
        "technology": "2",
        "network": "bridge",
        "port": "0.0.0.0:8001/TCP → 0.0.0.0:80001",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/aml/data",
        "status": "error",
        "number": 8192,
        "deleted": 0,
        "create_time": 1744631575306,
        "creator_id": ""
    },
    {
        "id": "ea1f0266-ed60-47f7-a29a-717ab0ce0b46",
        "name": "样例报告生成微服务",
        "attribute": "non_intelligent",
        "type": "atomic",
        "domain": "aml",
        "industry": "2",
        "scenario": "3",
        "technology": "3",
        "network": "bridge",
        "port": "0.0.0.0:8002/TCP → 0.0.0.0:80002",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/aml/data",
        "status": "warning",
        "number": 2330,
        "deleted": 0,
        "create_time": 1744631575306,
        "creator_id": ""
    },
    {
        "id": "1da6516e-c61f-43c8-adca-91fa0ab2d2ac",
        "name": "信用评估微服务",
        "attribute": "paid",
        "type": "atomic",
        "domain": "aml",
        "industry": "3",
        "scenario": "4",
        "technology": "4",
        "network": "bridge",
        "port": "0.0.0.0:8003/TCP → 0.0.0.0:80003",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/aml/data",
        "status": "default",
        "number": 2342,
        "deleted": 0,
        "create_time": 1744631575306,
        "creator_id": ""
    },
    {
        "id": "61ddfb7b-aa8e-47e7-a84d-bbb3b546052c",
        "name": "异常识别微服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "aml",
        "industry": "0",
        "scenario": "0",
        "technology": "0",
        "network": "bridge",
        "port": "0.0.0.0:8004/TCP → 0.0.0.0:80004",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/aml/data",
        "status": "error",
        "number": 0,
        "deleted": 0,
        "create_time": 1744631575306,
        "creator_id": ""
    },
    {
        "id": "42320ee0-39b3-4180-8231-77b951a16997",
        "name": "课题三金融风险报告生成微服务",
        "attribute": "paid",
        "type": "atomic",
        "domain": "aml",
        "industry": "3",
        "scenario": "4",
        "technology": "4",
        "network": "bridge",
        "port": "0.0.0.0:8005/TCP → 0.0.0.0:80005",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/aml/data",
        "status": "success",
        "number": 2342,
        "deleted": 0,
        "create_time": 1744631575306,
        "creator_id": ""
    },
    {
        "id": "f6ac8879-e20c-4109-bddc-069e5f9dd458",
        "name": "课题四模型评测-安全性指纹微服务",
        "attribute": "paid",
        "type": "atomic",
        "domain": "aml",
        "industry": "3",
        "scenario": "4",
        "technology": "4",
        "network": "bridge",
        "port": "0.0.0.0:8006/TCP → 0.0.0.0:80006",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/aml/data",
        "status": "success",
        "number": 2342,
        "deleted": 0,
        "create_time": 1744631575306,
        "creator_id": ""
    },
    {
        "id": "b48f8cb6-415b-4374-9ac1-e3287d484c79",
        "name": "技术评测元应用",
        "attribute": "custom",
        "type": "meta",
        "domain": "aml",
        "industry": "1",
        "scenario": "2",
        "technology": "4",
        "network": "bridge",
        "port": "0.0.0.0:1020/TCP → 0.0.0.0:10020",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/aml/metaApp",
        "status": "warning",
        "number": 2342,
        "deleted": 0,
        "create_time": 1744631575306,
        "creator_id": ""
    },
    {
        "id": "80f1735f-552f-4b24-95e9-606f70abe445",
        "name": "无人机虚拟仿真微服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "aircraft",
        "industry": "0",
        "scenario": "0",
        "technology": "1",
        "network": "bridge",
        "port": "0.0.0.0:8080/TCP → 0.0.0.0:80080",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/aircraft/data",
        "status": "success",
        "number": 2342,
        "deleted": 0,
        "create_time": 1744631575309,
        "creator_id": ""
    },
    {
        "id": "240add7d-f94c-48fe-a8a8-d33b328f66a8",
        "name": "无人机低空测绘微服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "aircraft",
        "industry": "1",
        "scenario": "3",
        "technology": "2",
        "network": "bridge",
        "port": "0.0.0.0:8081/TCP → 0.0.0.0:80081",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/aircraft/data",
        "status": "error",
        "number": 2342,
        "deleted": 0,
        "create_time": 1744631575309,
        "creator_id": ""
    },
    {
        "id": "6a594b3e-301c-4fd0-9143-03361b398ab7",
        "name": "无人机目标识别微服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "aircraft",
        "industry": "2",
        "scenario": "4",
        "technology": "2",
        "network": "bridge",
        "port": "0.0.0.0:8082/TCP → 0.0.0.0:80082",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/aircraft/data",
        "status": "error",
        "number": 2342,
        "deleted": 0,
        "create_time": 1744631575309,
        "creator_id": ""
    },
    {
        "id": "e28e52fa-5b85-4f3a-9497-aa88316fb0c6",
        "name": "无人机远程控制微服务",
        "attribute": "non_intelligent",
        "type": "atomic",
        "domain": "aircraft",
        "industry": "0",
        "scenario": "1",
        "technology": "3",
        "network": "bridge",
        "port": "0.0.0.0:8083/TCP → 0.0.0.0:80083",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/aircraft/data",
        "status": "default",
        "number": 2342,
        "deleted": 0,
        "create_time": 1744631575309,
        "creator_id": ""
    },
    {
        "id": "5914386c-9ea5-4695-8262-119ca4659257",
        "name": "无人机视频分析微服务",
        "attribute": "paid",
        "type": "atomic",
        "domain": "aircraft",
        "industry": "1",
        "scenario": "2",
        "technology": "4",
        "network": "bridge",
        "port": "0.0.0.0:8084/TCP → 0.0.0.0:80084",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/aircraft/data",
        "status": "warning",
        "number": 2342,
        "deleted": 0,
        "create_time": 1744631575309,
        "creator_id": ""
    },
    {
        "id": "2a971817-12df-412c-982b-0773e5ca757e",
        "name": "无人机智能投递",
        "attribute": "custom",
        "type": "meta",
        "domain": "aircraft",
        "industry": "1",
        "scenario": "2",
        "technology": "4",
        "network": "bridge",
        "port": "0.0.0.0:8084/TCP → 0.0.0.0:80084",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/aircraft/data",
        "status": "warning",
        "number": 2342,
        "deleted": 0,
        "create_time": 1744631575309,
        "creator_id": ""
    },
    {
        "id": "7c0a984a-90e6-40f7-bd1b-76b559e6dd5a",
        "name": "肝移植患者利奈唑胺给药方案优化微服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "health",
        "industry": "0",
        "scenario": "1",
        "technology": "1",
        "network": "bridge",
        "port": "0.0.0.0:8000/TCP → 0.0.0.0:80000",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/aml/data",
        "status": "success",
        "number": 512,
        "deleted": 0,
        "create_time": 1744631575315,
        "creator_id": ""
    },
    {
        "id": "2d73797c-09a9-4960-88f0-88252affb06a",
        "name": "基层医疗影像辅助诊断微服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "health",
        "industry": "0",
        "scenario": "1",
        "technology": "0",
        "network": "bridge",
        "port": "0.0.0.0:8100/TCP → 0.0.0.0:81000",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/health/data",
        "status": "success",
        "number": 256,
        "deleted": 0,
        "create_time": 1744631575315,
        "creator_id": ""
    },
    {
        "id": "6fd78779-3663-4929-88c3-e250b8ccef41",
        "name": "慢性病管理监测微服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "health",
        "industry": "0",
        "scenario": "2",
        "technology": "2",
        "network": "bridge",
        "port": "0.0.0.0:8101/TCP → 0.0.0.0:81001",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/health/data",
        "status": "success",
        "number": 128,
        "deleted": 0,
        "create_time": 1744631575315,
        "creator_id": ""
    },
    {
        "id": "b55a50bf-a123-4a47-81e1-7104eb979440",
        "name": "方言语音识别转写微服务",
        "attribute": "paid",
        "type": "atomic",
        "domain": "aircraft",
        "industry": "0",
        "scenario": "0",
        "technology": "1",
        "network": "bridge",
        "port": "0.0.0.0:8102/TCP → 0.0.0.0:81002",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/health/data",
        "status": "success",
        "number": 384,
        "deleted": 0,
        "create_time": 1744631575315,
        "creator_id": ""
    },
    {
        "id": "6d758804-6de8-4fa7-9a31-4b3e8d8241c3",
        "name": "乡村医疗资源调度微服务",
        "attribute": "non_intelligent",
        "type": "atomic",
        "domain": "health",
        "industry": "1",
        "scenario": "3",
        "technology": "3",
        "network": "bridge",
        "port": "0.0.0.0:8103/TCP → 0.0.0.0:81003",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/health/data",
        "status": "error",
        "number": 192,
        "deleted": 0,
        "create_time": 1744631575315,
        "creator_id": ""
    },
    {
        "id": "522f944a-2a1c-4ef3-a4e8-7ebde3fccc1c",
        "name": "流行病预测分析微服务",
        "attribute": "paid",
        "type": "atomic",
        "domain": "agriculture",
        "industry": "1",
        "scenario": "4",
        "technology": "2",
        "network": "bridge",
        "port": "0.0.0.0:8104/TCP → 0.0.0.0:81004",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/health/data",
        "status": "success",
        "number": 512,
        "deleted": 0,
        "create_time": 1744631575315,
        "creator_id": ""
    },
    {
        "id": "f4ab84fd-fda9-4bdf-a840-0718f2417dbe",
        "name": "乡村医疗AI辅助诊断元应用",
        "attribute": "custom",
        "type": "meta",
        "domain": "health",
        "industry": "0",
        "scenario": "1",
        "technology": "0",
        "network": "bridge",
        "port": "0.0.0.0:8120/TCP → 0.0.0.0:81020",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/health/metaApp",
        "status": "warning",
        "number": 1024,
        "deleted": 0,
        "create_time": 1744631575315,
        "creator_id": ""
    },
    {
        "id": "93314394-b92d-4e42-9ec2-b0f3cd436f39",
        "name": "农村公共卫生监测元应用",
        "attribute": "custom",
        "type": "meta",
        "domain": "health",
        "industry": "1",
        "scenario": "4",
        "technology": "2",
        "network": "bridge",
        "port": "0.0.0.0:8121/TCP → 0.0.0.0:81021",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/health/metaApp",
        "status": "warning",
        "number": 768,
        "deleted": 0,
        "create_time": 1744631575315,
        "creator_id": ""
    },
    {
        "id": "9d780c5e-8cac-4139-9753-0801c038d775",
        "name": "农作物图像分析服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "agriculture",
        "industry": "4",
        "scenario": "0",
        "technology": "计算机视觉（智慧种植/精准播种）",
        "network": "bridge",
        "port": "0.0.0.0:8010/TCP → 0.0.0.0:8010",
        "volume": "/var/opt/gitlab/mnt/user → /appdata/agriculture/data",
        "status": "success",
        "number": 512,
        "deleted": 0,
        "create_time": 1744631575320,
        "creator_id": ""
    },
    {
        "id": "462e0a2c-a502-4adb-8a0b-ed9fd2cc9332",
        "name": "病虫害识别与防治服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "agriculture",
        "industry": "4",
        "scenario": "1",
        "technology": "计算机视觉（智慧种植/病虫害防治）",
        "network": "bridge",
        "port": "0.0.0.0:8011/TCP → 0.0.0.0:8011",
        "volume": "/var/opt/gitlab/mnt/user → /appdata/agriculture/data",
        "status": "success",
        "number": 512,
        "deleted": 0,
        "create_time": 1744631575320,
        "creator_id": ""
    },
    {
        "id": "45e0f736-c6c2-4f5d-922f-81c9a70c0c05",
        "name": "智能灌溉决策服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "agriculture",
        "industry": "4",
        "scenario": "2",
        "technology": "时序分析与预测（智慧种植/智能灌溉）",
        "network": "bridge",
        "port": "0.0.0.0:8012/TCP → 0.0.0.0:8012",
        "volume": "/var/opt/gitlab/mnt/user → /appdata/agriculture/data",
        "status": "success",
        "number": 512,
        "deleted": 0,
        "create_time": 1744631575320,
        "creator_id": ""
    },
    {
        "id": "8995db1a-eeb8-42af-97c1-32e5a4a73c6a",
        "name": "农作物产量预测服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "agriculture",
        "industry": "4",
        "scenario": "3",
        "technology": "时序分析与预测（智慧种植/产量预测）",
        "network": "bridge",
        "port": "0.0.0.0:8013/TCP → 0.0.0.0:8013",
        "volume": "/var/opt/gitlab/mnt/user → /appdata/agriculture/data",
        "status": "success",
        "number": 512,
        "deleted": 0,
        "create_time": 1744631575320,
        "creator_id": ""
    },
    {
        "id": "e8b0b89f-aa4e-4a24-b12d-b68a5ed660d7",
        "name": "智慧农业综合管理元应用",
        "attribute": "paid",
        "type": "meta",
        "domain": "agriculture",
        "industry": "4",
        "scenario": "4",
        "technology": "计算机视觉、时序分析与预测、多模态融合（智慧种植/精准播种、病虫害防治、智能灌溉、产量预测）",
        "network": "host",
        "port": "0.0.0.0:9010/TCP → 0.0.0.0:9010",
        "volume": "/var/opt/gitlab/mnt/user → /appdata/agriculture/meta",
        "status": "success",
        "number": 512,
        "deleted": 0,
        "create_time": 1744631575320,
        "creator_id": ""
    },
    {
        "id": "4e988dd8-ffbf-4714-baca-3ae60b8a007c",
        "name": "飞行路径规划微服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "evtol",
        "industry": "0",
        "scenario": "0",
        "technology": "0",
        "network": "bridge",
        "port": "0.0.0.0:8200/TCP → 0.0.0.0:82000",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/evtol/data",
        "status": "success",
        "number": 256,
        "deleted": 0,
        "create_time": 1744631575325,
        "creator_id": ""
    },
    {
        "id": "4577e627-156b-4061-9da1-3a1ae14418db",
        "name": "环境感知微服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "evtol",
        "industry": "0",
        "scenario": "3",
        "technology": "1",
        "network": "bridge",
        "port": "0.0.0.0:8201/TCP → 0.0.0.0:82001",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/evtol/data",
        "status": "success",
        "number": 512,
        "deleted": 0,
        "create_time": 1744631575325,
        "creator_id": ""
    },
    {
        "id": "aaed9501-1085-41de-878c-aa106a35cc76",
        "name": "飞行控制微服务",
        "attribute": "non_intelligent",
        "type": "atomic",
        "domain": "evtol",
        "industry": "0",
        "scenario": "2",
        "technology": "0",
        "network": "bridge",
        "port": "0.0.0.0:8202/TCP → 0.0.0.0:82002",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/evtol/data",
        "status": "success",
        "number": 256,
        "deleted": 0,
        "create_time": 1744631575325,
        "creator_id": ""
    },
    {
        "id": "ddf3ad0f-3311-4b0f-8780-3e883e8618aa",
        "name": "能源管理微服务",
        "attribute": "paid",
        "type": "atomic",
        "domain": "evtol",
        "industry": "0",
        "scenario": "4",
        "technology": "3",
        "network": "bridge",
        "port": "0.0.0.0:8203/TCP → 0.0.0.0:82003",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/evtol/data",
        "status": "success",
        "number": 128,
        "deleted": 0,
        "create_time": 1744631575325,
        "creator_id": ""
    },
    {
        "id": "bf06c54b-0953-44ed-a1f1-53b56d569010",
        "name": "安全监控微服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "evtol",
        "industry": "2",
        "scenario": "3",
        "technology": "4",
        "network": "bridge",
        "port": "0.0.0.0:8204/TCP → 0.0.0.0:82004",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/evtol/data",
        "status": "success",
        "number": 384,
        "deleted": 0,
        "create_time": 1744631575325,
        "creator_id": ""
    },
    {
        "id": "8189e54b-ae51-43b6-bf25-7e5391288e3c",
        "name": "eVTOL智能飞行控制元应用",
        "attribute": "open_source",
        "type": "meta",
        "domain": "evtol",
        "industry": "0",
        "scenario": "0",
        "technology": "0",
        "network": "bridge",
        "port": "0.0.0.0:8220/TCP → 0.0.0.0:82200",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/evtol/metaApp",
        "status": "success",
        "number": 1024,
        "deleted": 0,
        "create_time": 1744631575325,
        "creator_id": ""
    },
    {
        "id": "64d4710f-e820-4900-b0a1-659ae8871b97",
        "name": "多语言内容生成微服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "ecommerce",
        "industry": "0",
        "scenario": "0",
        "technology": "0",
        "network": "bridge",
        "port": "0.0.0.0:8500/TCP → 0.0.0.0:85000",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/ecommerce/data",
        "status": "success",
        "number": 256,
        "deleted": 0,
        "create_time": 1744631575328,
        "creator_id": ""
    },
    {
        "id": "3e846e2c-5c43-4eda-be49-b279cfd68b49",
        "name": "市场分析微服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "ecommerce",
        "industry": "0",
        "scenario": "3",
        "technology": "3",
        "network": "bridge",
        "port": "0.0.0.0:8501/TCP → 0.0.0.0:85001",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/ecommerce/data",
        "status": "success",
        "number": 384,
        "deleted": 0,
        "create_time": 1744631575328,
        "creator_id": ""
    },
    {
        "id": "f043882c-acbe-4737-99d7-5de8bbb3beae",
        "name": "跨境电商智能营销元应用",
        "attribute": "open_source",
        "type": "meta",
        "domain": "ecommerce",
        "industry": "0",
        "scenario": "0",
        "technology": "0",
        "network": "bridge",
        "port": "0.0.0.0:8600/TCP → 0.0.0.0:86000",
        "volume": "/var/opt/gitlab/mnt/user  →  /appdata/ecommerce/meta",
        "status": "success",
        "number": 512,
        "deleted": 0,
        "create_time": 1744631575328,
        "creator_id": ""
    },
    {
        "id": "6f29852e-b8e0-44fe-b7f7-8aacb871e4d3",
        "name": "环境感知微服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "homeAI",
        "industry": "0",
        "scenario": "0",
        "technology": "0",
        "network": 5,
        "port": 4,
        "volume": 4,
        "status": "success",
        "number": 5,
        "deleted": 0,
        "create_time": 1744631575332,
        "creator_id": ""
    },
    {
        "id": "078d857f-5f86-48d7-aafb-7f07f74de318",
        "name": "智能对话微服务",
        "attribute": "paid",
        "type": "atomic",
        "domain": "homeAI",
        "industry": "0",
        "scenario": "0",
        "technology": "1",
        "network": 4,
        "port": 3,
        "volume": 5,
        "status": "success",
        "number": 6,
        "deleted": 0,
        "create_time": 1744631575333,
        "creator_id": ""
    },
    {
        "id": "300ece69-b80f-4c78-8865-fbda3760aee8",
        "name": "健康监测微服务",
        "attribute": "open_source",
        "type": "atomic",
        "domain": "homeAI",
        "industry": "1",
        "scenario": "1",
        "technology": "3",
        "network": 3,
        "port": 3,
        "volume": 4,
        "status": "success",
        "number": 4,
        "deleted": 0,
        "create_time": 1744631575333,
        "creator_id": ""
    },
    {
        "id": "257154b3-77b8-4ce6-a3c9-c560a60ce10d",
        "name": "家务辅助微服务",
        "attribute": "non_intelligent",
        "type": "atomic",
        "domain": "aml",
        "industry": "4",
        "scenario": "0",
        "technology": "2",
        "network": 4,
        "port": 3,
        "volume": 3,
        "status": "success",
        "number": 3,
        "deleted": 0,
        "create_time": 1744631575333,
        "creator_id": ""
    },
    {
        "id": "0ef523dd-ee18-40bb-a588-d8097f197806",
        "name": "家庭智能助手元应用",
        "attribute": "open_source",
        "type": "meta",
        "domain": "homeAI",
        "industry": "0",
        "scenario": "4",
        "technology": "5",
        "network": 5,
        "port": 5,
        "volume": 5,
        "status": "success",
        "number": 1,
        "deleted": 0,
        "create_time": 1744631575333,
        "creator_id": ""
    },
]

# MOCK_SERVICE_NORMS 数据
MOCK_SERVICE_NORMS = [
    {
        "id": "562f800c-e81e-43ea-876c-3b39e25ebd7c",
        "service_id": "8438c51b-4f31-4f44-91b1-f805ff4f5b39",
        "key": "security",
        "score": 5
    },
    {
        "id": "873bc766-d4aa-47de-9d3d-62167dc5ffb9",
        "service_id": "8438c51b-4f31-4f44-91b1-f805ff4f5b39",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "d84f12f8-8ca2-412d-8990-907295ce78f2",
        "service_id": "924dc60b-4866-45f2-bd19-f98af257cf6c",
        "key": "security",
        "score": 5
    },
    {
        "id": "ad46d72f-455a-49b7-a010-51179d69609c",
        "service_id": "924dc60b-4866-45f2-bd19-f98af257cf6c",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "1d1ff24b-53fe-4f27-8c43-8b39e98ae86f",
        "service_id": "c27fe536-7ac5-413a-84ca-09b6fe218659",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "964a2b38-33ba-4de7-870c-681e56afdfa3",
        "service_id": "c27fe536-7ac5-413a-84ca-09b6fe218659",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "83c4b647-d82f-42c1-8ac7-e1eadc867268",
        "service_id": "ea1f0266-ed60-47f7-a29a-717ab0ce0b46",
        "key": "security",
        "score": 5
    },
    {
        "id": "db4f35e2-6c72-44c3-b46b-71a7da4eb9cc",
        "service_id": "ea1f0266-ed60-47f7-a29a-717ab0ce0b46",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "f474e95c-a8af-4746-be6f-b7d4ed889142",
        "service_id": "ea1f0266-ed60-47f7-a29a-717ab0ce0b46",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "de58a9ad-b1c7-4b3d-959d-1ac54ab25e1a",
        "service_id": "1da6516e-c61f-43c8-adca-91fa0ab2d2ac",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "1f0dc778-7756-4bb8-afd2-950cab7130b9",
        "service_id": "1da6516e-c61f-43c8-adca-91fa0ab2d2ac",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "341d9cb3-46ed-4b8a-88a5-1e04c2716dc4",
        "service_id": "1da6516e-c61f-43c8-adca-91fa0ab2d2ac",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "5bf7a3d1-5e82-4280-a1fb-ea3e885a5217",
        "service_id": "61ddfb7b-aa8e-47e7-a84d-bbb3b546052c",
        "key": "security",
        "score": 5
    },
    {
        "id": "dc3e63a5-681e-4f55-b141-82b62876fc09",
        "service_id": "61ddfb7b-aa8e-47e7-a84d-bbb3b546052c",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "09e26330-0b32-464b-af7c-810a5b6e3992",
        "service_id": "61ddfb7b-aa8e-47e7-a84d-bbb3b546052c",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "3cd94095-f80b-41c9-aa0f-1407fdb384da",
        "service_id": "42320ee0-39b3-4180-8231-77b951a16997",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "cb4a8a02-5fdb-42e7-a0e4-a7625902db9e",
        "service_id": "42320ee0-39b3-4180-8231-77b951a16997",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "919b2711-8919-4976-89e8-d622c8e1ddeb",
        "service_id": "42320ee0-39b3-4180-8231-77b951a16997",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "dd736242-002d-4cab-a602-0670c1392586",
        "service_id": "f6ac8879-e20c-4109-bddc-069e5f9dd458",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "32f40d51-9f06-4c4a-a043-960440bb064e",
        "service_id": "f6ac8879-e20c-4109-bddc-069e5f9dd458",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "3b9a8c2f-29be-4fd1-aa6f-932cf041a695",
        "service_id": "f6ac8879-e20c-4109-bddc-069e5f9dd458",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "32d8bf2e-daee-498c-b9ec-b5a6e59b5aca",
        "service_id": "b48f8cb6-415b-4374-9ac1-e3287d484c79",
        "key": "security",
        "score": 5
    },
    {
        "id": "0fad569d-c277-4baf-85c2-85f735ae2b91",
        "service_id": "b48f8cb6-415b-4374-9ac1-e3287d484c79",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "614c880c-0c10-458b-b4fd-b5de1fa64079",
        "service_id": "b48f8cb6-415b-4374-9ac1-e3287d484c79",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "2b32517f-cb26-42f3-83fc-2696d88da3a5",
        "service_id": "b48f8cb6-415b-4374-9ac1-e3287d484c79",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "963ebc77-1743-4d0d-957b-c4503c3ef429",
        "service_id": "80f1735f-552f-4b24-95e9-606f70abe445",
        "key": "security",
        "score": 5
    },
    {
        "id": "ebe54fb8-30f8-4208-8a61-5309a2fad795",
        "service_id": "80f1735f-552f-4b24-95e9-606f70abe445",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "df3559e7-dab5-4069-aa96-eede4ce6801d",
        "service_id": "80f1735f-552f-4b24-95e9-606f70abe445",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "cfd3acbf-da89-4108-8150-c59cd2343194",
        "service_id": "240add7d-f94c-48fe-a8a8-d33b328f66a8",
        "key": "security",
        "score": 5
    },
    {
        "id": "0bb8de76-6694-45da-94e2-12185a157d4c",
        "service_id": "240add7d-f94c-48fe-a8a8-d33b328f66a8",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "169da35e-e9b4-4d95-ace0-cb16fa756e32",
        "service_id": "6a594b3e-301c-4fd0-9143-03361b398ab7",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "f95d35bf-90e8-4b6f-9406-bd1b66bee3d5",
        "service_id": "6a594b3e-301c-4fd0-9143-03361b398ab7",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "394625be-48a1-4f34-bc42-6d48671d41cd",
        "service_id": "e28e52fa-5b85-4f3a-9497-aa88316fb0c6",
        "key": "security",
        "score": 5
    },
    {
        "id": "ab5add5b-4ef8-4797-a6c4-88f69e966ae1",
        "service_id": "e28e52fa-5b85-4f3a-9497-aa88316fb0c6",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "f36bd416-302f-4658-9bb7-74344fc76301",
        "service_id": "e28e52fa-5b85-4f3a-9497-aa88316fb0c6",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "d09508d2-31d2-44aa-9b59-fbd54eab05d6",
        "service_id": "5914386c-9ea5-4695-8262-119ca4659257",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "0c7aba93-8e79-4597-8ae4-d3494bea815c",
        "service_id": "5914386c-9ea5-4695-8262-119ca4659257",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "b4b6dc6b-53c4-4bff-aac4-7c3097c6238e",
        "service_id": "5914386c-9ea5-4695-8262-119ca4659257",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "8d4c1cae-126c-4348-9791-08a8cf08c98d",
        "service_id": "2a971817-12df-412c-982b-0773e5ca757e",
        "key": "security",
        "score": 5
    },
    {
        "id": "e065cb7b-4fdf-4f14-b7ff-8db08e2a9102",
        "service_id": "2a971817-12df-412c-982b-0773e5ca757e",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "71e82205-cc89-463a-95e5-3445f74537f1",
        "service_id": "2a971817-12df-412c-982b-0773e5ca757e",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "1b75248b-3ccb-4eee-a5b6-6cc97037bcfa",
        "service_id": "2a971817-12df-412c-982b-0773e5ca757e",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "29837ad7-55c8-4912-8e85-dcb170efd936",
        "service_id": "7c0a984a-90e6-40f7-bd1b-76b559e6dd5a",
        "key": "security",
        "score": 5
    },
    {
        "id": "1451b13e-3c20-43fe-b8fb-f90ee5ed1c5f",
        "service_id": "7c0a984a-90e6-40f7-bd1b-76b559e6dd5a",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "ed7a1cd7-055e-4ba8-b1cf-8c058b7e832b",
        "service_id": "2d73797c-09a9-4960-88f0-88252affb06a",
        "key": "security",
        "score": 5
    },
    {
        "id": "07fc80ee-02b4-4a0f-b6e4-f00d0c34a37e",
        "service_id": "2d73797c-09a9-4960-88f0-88252affb06a",
        "key": "privacy",
        "score": 4
    },
    {
        "id": "3ead520a-57c3-41a0-926a-531f17b1b982",
        "service_id": "6fd78779-3663-4929-88c3-e250b8ccef41",
        "key": "robustness",
        "score": 4
    },
    {
        "id": "89ef2d8b-5da0-4732-8bb9-6b5c7fd84030",
        "service_id": "6fd78779-3663-4929-88c3-e250b8ccef41",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "b5ea998e-8cef-4d86-b415-d45b862908fa",
        "service_id": "b55a50bf-a123-4a47-81e1-7104eb979440",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "77536a28-17c7-45c6-ae05-518f509272df",
        "service_id": "b55a50bf-a123-4a47-81e1-7104eb979440",
        "key": "privacy",
        "score": 4
    },
    {
        "id": "ede9e3dd-0a31-4ceb-a673-7e97512873d9",
        "service_id": "6d758804-6de8-4fa7-9a31-4b3e8d8241c3",
        "key": "security",
        "score": 4
    },
    {
        "id": "6fecfc25-eea8-4b74-95a3-ea9e77fbad7a",
        "service_id": "6d758804-6de8-4fa7-9a31-4b3e8d8241c3",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "c749efbb-257a-472b-9239-9698b3682ac3",
        "service_id": "522f944a-2a1c-4ef3-a4e8-7ebde3fccc1c",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "867cc64a-8958-4fc6-b0b4-16bf8a776ca0",
        "service_id": "522f944a-2a1c-4ef3-a4e8-7ebde3fccc1c",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "6ce295ad-2c87-4be4-be68-c30195d42364",
        "service_id": "f4ab84fd-fda9-4bdf-a840-0718f2417dbe",
        "key": "security",
        "score": 5
    },
    {
        "id": "acd28d23-3b41-4104-bb01-3c38880f39a8",
        "service_id": "f4ab84fd-fda9-4bdf-a840-0718f2417dbe",
        "key": "robustness",
        "score": 4
    },
    {
        "id": "3bbdc284-8506-451f-bc05-b2c16b946b42",
        "service_id": "f4ab84fd-fda9-4bdf-a840-0718f2417dbe",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "5e1a311b-b5e5-4b4e-ab6f-1dbc04aab0ce",
        "service_id": "f4ab84fd-fda9-4bdf-a840-0718f2417dbe",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "55a43f7d-97c4-40c7-8be7-12683d25039f",
        "service_id": "93314394-b92d-4e42-9ec2-b0f3cd436f39",
        "key": "security",
        "score": 4
    },
    {
        "id": "6e412986-9667-4f51-81b9-bfdd3dce3363",
        "service_id": "93314394-b92d-4e42-9ec2-b0f3cd436f39",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "498f1d2d-2244-48f9-b184-94e2adfca28d",
        "service_id": "93314394-b92d-4e42-9ec2-b0f3cd436f39",
        "key": "privacy",
        "score": 4
    },
    {
        "id": "7e1f12ba-b468-430a-b8c5-ffa4a02977ce",
        "service_id": "93314394-b92d-4e42-9ec2-b0f3cd436f39",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "4ebceb77-6bca-457b-abcc-f84d30e7fa48",
        "service_id": "9d780c5e-8cac-4139-9753-0801c038d775",
        "key": "security",
        "score": 5
    },
    {
        "id": "38176276-ac33-455d-906b-ca41649118d9",
        "service_id": "9d780c5e-8cac-4139-9753-0801c038d775",
        "key": "privacy",
        "score": 4
    },
    {
        "id": "9e1bdcd7-e421-43e1-920a-ef6950e25d6b",
        "service_id": "462e0a2c-a502-4adb-8a0b-ed9fd2cc9332",
        "key": "security",
        "score": 5
    },
    {
        "id": "2733a17b-e9e6-4295-aafc-afa5b8bfbee2",
        "service_id": "462e0a2c-a502-4adb-8a0b-ed9fd2cc9332",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "39d56887-23b9-46ae-b9f9-addcd69a5073",
        "service_id": "45e0f736-c6c2-4f5d-922f-81c9a70c0c05",
        "key": "security",
        "score": 4
    },
    {
        "id": "4c42a9d9-5d79-4182-a0ba-d9ad4c0e3f3e",
        "service_id": "45e0f736-c6c2-4f5d-922f-81c9a70c0c05",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "69b7ae50-2c96-4bb3-9626-4ac67dfac714",
        "service_id": "8995db1a-eeb8-42af-97c1-32e5a4a73c6a",
        "key": "security",
        "score": 4
    },
    {
        "id": "c20f1a13-c324-43a3-a04a-faa964222a9c",
        "service_id": "8995db1a-eeb8-42af-97c1-32e5a4a73c6a",
        "key": "privacy",
        "score": 4
    },
    {
        "id": "9d396a03-c658-4ca1-b1bf-a690500906b6",
        "service_id": "e8b0b89f-aa4e-4a24-b12d-b68a5ed660d7",
        "key": "security",
        "score": 5
    },
    {
        "id": "b50d48af-c9d5-4634-bd7f-ba00def28775",
        "service_id": "e8b0b89f-aa4e-4a24-b12d-b68a5ed660d7",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "237ef2c2-58b1-4c9d-bdbb-ab7b2004c04f",
        "service_id": "4e988dd8-ffbf-4714-baca-3ae60b8a007c",
        "key": "security",
        "score": 5
    },
    {
        "id": "8783a394-892d-46d1-a604-d44b186cc199",
        "service_id": "4e988dd8-ffbf-4714-baca-3ae60b8a007c",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "e2f36865-98ce-423b-9b8b-b085fc6ff928",
        "service_id": "4577e627-156b-4061-9da1-3a1ae14418db",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "dc871c27-da3b-48a6-910c-e8c0948dfa24",
        "service_id": "4577e627-156b-4061-9da1-3a1ae14418db",
        "key": "trustworthiness",
        "score": 4
    },
    {
        "id": "39555099-8b87-404d-b5c6-a0bf476fba94",
        "service_id": "aaed9501-1085-41de-878c-aa106a35cc76",
        "key": "security",
        "score": 5
    },
    {
        "id": "dd215b00-0631-4ba6-8ae1-cad7cd0686e6",
        "service_id": "aaed9501-1085-41de-878c-aa106a35cc76",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "9219efa1-9e8e-49be-85dc-98e23782f0ae",
        "service_id": "aaed9501-1085-41de-878c-aa106a35cc76",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "db752e5b-c789-45a1-b34f-d5dc4e581d3c",
        "service_id": "ddf3ad0f-3311-4b0f-8780-3e883e8618aa",
        "key": "security",
        "score": 4
    },
    {
        "id": "54b9910e-dcec-47d0-a853-4759713bb358",
        "service_id": "ddf3ad0f-3311-4b0f-8780-3e883e8618aa",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "cbc47bd2-1baa-44cb-8656-e94dd780d10a",
        "service_id": "bf06c54b-0953-44ed-a1f1-53b56d569010",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "03201d10-d4b3-42c7-8386-f900471e6835",
        "service_id": "bf06c54b-0953-44ed-a1f1-53b56d569010",
        "key": "privacy",
        "score": 4
    },
    {
        "id": "46b3a0ac-be17-41aa-a558-e45a6aaffcdf",
        "service_id": "bf06c54b-0953-44ed-a1f1-53b56d569010",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "e4d125b7-319c-4907-88a3-0f849b11c3f7",
        "service_id": "8189e54b-ae51-43b6-bf25-7e5391288e3c",
        "key": "security",
        "score": 5
    },
    {
        "id": "7cd11b7f-eac8-4f32-8afd-427837cbf253",
        "service_id": "8189e54b-ae51-43b6-bf25-7e5391288e3c",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "c3cbfae4-2fef-43fb-b068-456b518d88bd",
        "service_id": "8189e54b-ae51-43b6-bf25-7e5391288e3c",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "8df24852-afb7-475a-b9fe-597f4d42b4b0",
        "service_id": "8189e54b-ae51-43b6-bf25-7e5391288e3c",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "a16fd11e-dade-4b67-a533-bc735fc9643e",
        "service_id": "64d4710f-e820-4900-b0a1-659ae8871b97",
        "key": "security",
        "score": 5
    },
    {
        "id": "a3d428e8-f7e9-4ab5-ab8f-a960bdceeb80",
        "service_id": "64d4710f-e820-4900-b0a1-659ae8871b97",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "7cf4cfba-ef54-46c3-938f-cc4f36ca1aa1",
        "service_id": "64d4710f-e820-4900-b0a1-659ae8871b97",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "bf0d846b-506d-4a42-ba83-203b990ca608",
        "service_id": "64d4710f-e820-4900-b0a1-659ae8871b97",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "b1a029e9-74c4-4144-b8a6-0049aa00e53d",
        "service_id": "3e846e2c-5c43-4eda-be49-b279cfd68b49",
        "key": "security",
        "score": 5
    },
    {
        "id": "ab72aec4-f44c-42b2-b555-e9bbdd15f6a2",
        "service_id": "3e846e2c-5c43-4eda-be49-b279cfd68b49",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "05cad1b2-56d9-493a-909f-3a12a9639c3d",
        "service_id": "3e846e2c-5c43-4eda-be49-b279cfd68b49",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "abd7afe4-4fda-43e4-b7b5-32861685a718",
        "service_id": "f043882c-acbe-4737-99d7-5de8bbb3beae",
        "key": "security",
        "score": 5
    },
    {
        "id": "aeb5b5d9-082e-42ed-9a04-e58d8233a6de",
        "service_id": "f043882c-acbe-4737-99d7-5de8bbb3beae",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "338a2425-3507-4662-8495-dbffd3a27f78",
        "service_id": "f043882c-acbe-4737-99d7-5de8bbb3beae",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "6bed02be-5655-4284-a197-9c688f4ae0ca",
        "service_id": "6f29852e-b8e0-44fe-b7f7-8aacb871e4d3",
        "key": "security",
        "score": 5
    },
    {
        "id": "f9fa91d1-9e58-42ee-b49c-d82cc4052db4",
        "service_id": "6f29852e-b8e0-44fe-b7f7-8aacb871e4d3",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "08085ab6-0ee7-4703-a115-d54bdae41fcb",
        "service_id": "6f29852e-b8e0-44fe-b7f7-8aacb871e4d3",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "04b6846a-b84a-4555-ae4e-7bf6390a499a",
        "service_id": "6f29852e-b8e0-44fe-b7f7-8aacb871e4d3",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "d876b9a6-996b-49e2-b95f-4a7b3a558eae",
        "service_id": "078d857f-5f86-48d7-aafb-7f07f74de318",
        "key": "security",
        "score": 5
    },
    {
        "id": "2f069575-b029-4cfc-a9d6-b0147ef3e866",
        "service_id": "078d857f-5f86-48d7-aafb-7f07f74de318",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "4948e583-fb29-4d36-8819-8ec0b3d12a7f",
        "service_id": "078d857f-5f86-48d7-aafb-7f07f74de318",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "f6f2b675-2427-4830-a803-49a72c4ee533",
        "service_id": "078d857f-5f86-48d7-aafb-7f07f74de318",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "b70a5835-24c8-4b83-b329-48b4b6316951",
        "service_id": "300ece69-b80f-4c78-8865-fbda3760aee8",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "cbc1b1f2-1142-4395-8561-c9e3424b0ae6",
        "service_id": "300ece69-b80f-4c78-8865-fbda3760aee8",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "19aa175d-d55f-4134-a9b8-6d3788f6d71d",
        "service_id": "300ece69-b80f-4c78-8865-fbda3760aee8",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "3ad10d98-4b75-436d-aac3-457c703556c2",
        "service_id": "257154b3-77b8-4ce6-a3c9-c560a60ce10d",
        "key": "security",
        "score": 5
    },
    {
        "id": "93b1dc8b-9373-4da4-a98c-0bea1abd3984",
        "service_id": "257154b3-77b8-4ce6-a3c9-c560a60ce10d",
        "key": "privacy",
        "score": 5
    },
    {
        "id": "143b4209-8e7d-4394-bdf4-083c346a9f37",
        "service_id": "257154b3-77b8-4ce6-a3c9-c560a60ce10d",
        "key": "trustworthiness",
        "score": 5
    },
    {
        "id": "19dbbc4a-f315-4658-a4db-8f3f2d4f0fa9",
        "service_id": "0ef523dd-ee18-40bb-a588-d8097f197806",
        "key": "security",
        "score": 5
    },
    {
        "id": "0ffe4c17-442a-44f9-bc85-8cda3af4f52d",
        "service_id": "0ef523dd-ee18-40bb-a588-d8097f197806",
        "key": "robustness",
        "score": 5
    },
    {
        "id": "3999b9ce-e1c4-461d-aa50-e1fe38fd5730",
        "service_id": "0ef523dd-ee18-40bb-a588-d8097f197806",
        "key": "privacy",
        "score": 5
    },
]

# MOCK_SERVICE_SOURCES 数据
MOCK_SERVICE_SOURCES = [
    {
        "id": "cbd20041-e716-401c-8204-fa4374394483",
        "service_id": "8438c51b-4f31-4f44-91b1-f805ff4f5b39",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "课题一",
        "ms_introduce": "基于智能体的风险识别算法",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "68898486-7609-4937-990a-cd758696cade",
        "service_id": "924dc60b-4866-45f2-bd19-f98af257cf6c",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "课题二",
        "ms_introduce": "基于多方安全计算的风险识别算法",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "85119606-d8de-480a-9c24-95938e8b8f63",
        "service_id": "c27fe536-7ac5-413a-84ca-09b6fe218659",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "课题五",
        "ms_introduce": "课题五样例服务",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "60df9a9d-1f7f-4fde-ac92-436275c8b261",
        "service_id": "ea1f0266-ed60-47f7-a29a-717ab0ce0b46",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "课题一",
        "ms_introduce": "简易版报告生成",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "9fd9c5ea-12d2-4568-87fc-1802fc7a7ef6",
        "service_id": "1da6516e-c61f-43c8-adca-91fa0ab2d2ac",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "课题五",
        "ms_introduce": "课题五样例服务",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "c4c3f27a-17ba-4696-b616-db1f91f8de04",
        "service_id": "61ddfb7b-aa8e-47e7-a84d-bbb3b546052c",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "课题五",
        "ms_introduce": "课题五AI技术中台上传、发布算法样例服务",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "157989f5-9116-48ec-b980-b6ffaaba99a3",
        "service_id": "42320ee0-39b3-4180-8231-77b951a16997",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "课题三",
        "ms_introduce": "金融风险报告生成",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "8e6243f4-d725-4759-8fa9-53daca2cdfe8",
        "service_id": "f6ac8879-e20c-4109-bddc-069e5f9dd458",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "课题四",
        "ms_introduce": "安全性指纹测评算法",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "768f2a6b-0392-4056-9b65-4b0e455ff082",
        "service_id": "b48f8cb6-415b-4374-9ac1-e3287d484c79",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "课题五",
        "ms_introduce": "用于跨境支付的风险评估和报告生成的元应用样例",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "d6227148-624f-4ee3-92a3-8718f9532677",
        "service_id": "80f1735f-552f-4b24-95e9-606f70abe445",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "课题五",
        "ms_introduce": "基于智能体的无人机虚拟仿真微服务",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "d79e463e-eb60-497f-8fff-8678d471fea3",
        "service_id": "240add7d-f94c-48fe-a8a8-d33b328f66a8",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "无人机AI应用课题",
        "ms_introduce": "基于智能体的无人机低空测绘微服务",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "01de86cb-005d-4f10-8655-172d0bda13f7",
        "service_id": "6a594b3e-301c-4fd0-9143-03361b398ab7",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "无人机AI应用课题",
        "ms_introduce": "基于智能体的无人机目标识别微服务",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "c3aea589-9d58-455b-b9c0-9438ebbea1e5",
        "service_id": "e28e52fa-5b85-4f3a-9497-aa88316fb0c6",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "无人机AI应用课题",
        "ms_introduce": "基于智能体的无人机远程控制微服务",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "4a75f939-1a3e-41de-8b0a-2012962fdaf0",
        "service_id": "5914386c-9ea5-4695-8262-119ca4659257",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "无人机AI应用课题",
        "ms_introduce": "基于智能体的无人机视频分析微服务",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "c880ca65-f08e-4f3e-a3cf-b6a23fe5bea8",
        "service_id": "2a971817-12df-412c-982b-0773e5ca757e",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "",
        "ms_introduce": "针对跨境贸易支付监管的误检率高、效率低问题，本课题旨在研究新的监管方法和机制，支持新时代的监管体系构建。基于高性能分布式图数据库和FIDO客户认证，通过高性能图分析算法优化规则驱动的跨境支付监管，确保数据真实性并实现高并发事中监管。",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "48ad06de-a0ee-43a1-969a-82d6abc79dc5",
        "service_id": "7c0a984a-90e6-40f7-bd1b-76b559e6dd5a",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "药学院临床药学系",
        "ms_introduce": "基于群体药动学模型的肝移植患者利奈唑胺给药方案优化",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "c08900ab-0590-4a0c-b280-6c603f41718b",
        "service_id": "2d73797c-09a9-4960-88f0-88252affb06a",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "乡村医疗AI应用课题",
        "ms_introduce": "基于轻量化模型的医疗影像辅助诊断服务",
        "company_score": 5,
        "ms_score": 4
    },
    {
        "id": "94007962-6705-481f-acff-6f78a3058240",
        "service_id": "6fd78779-3663-4929-88c3-e250b8ccef41",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "乡村医疗AI应用课题",
        "ms_introduce": "基于物联网和AI的慢性病监测服务",
        "company_score": 4,
        "ms_score": 5
    },
    {
        "id": "7da15d7c-08c2-4178-a994-437eb7f97937",
        "service_id": "b55a50bf-a123-4a47-81e1-7104eb979440",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "乡村医疗AI应用课题",
        "ms_introduce": "农村方言语音识别转写服务",
        "company_score": 4,
        "ms_score": 5
    },
    {
        "id": "f242f738-7d42-46d2-93d8-8d2a3f62760d",
        "service_id": "6d758804-6de8-4fa7-9a31-4b3e8d8241c3",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "乡村医疗AI应用课题",
        "ms_introduce": "基于强化学习的医疗资源优化调度服务",
        "company_score": 5,
        "ms_score": 4
    },
    {
        "id": "8968e95b-1ec9-4bdc-a1a5-faa193f0aeb3",
        "service_id": "522f944a-2a1c-4ef3-a4e8-7ebde3fccc1c",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "乡村医疗AI应用课题",
        "ms_introduce": "基于时序数据分析的流行病预测服务",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "4db030b4-4ba7-44e4-9b13-19e2df478dd5",
        "service_id": "f4ab84fd-fda9-4bdf-a840-0718f2417dbe",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "乡村医疗AI应用课题",
        "ms_introduce": "针对基层医疗机构的AI辅助诊断元应用，整合了医学影像处理和方言语音识别功能",
        "company_score": 5,
        "ms_score": 4
    },
    {
        "id": "a5c8c487-92bf-483e-98f3-e504f7745e8e",
        "service_id": "93314394-b92d-4e42-9ec2-b0f3cd436f39",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "乡村医疗AI应用课题",
        "ms_introduce": "农村地区公共卫生监测元应用，整合流行病预测和医疗资源调度功能",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "8c664d6c-f0d5-4ba5-8096-b2f7f84147de",
        "service_id": "9d780c5e-8cac-4139-9753-0801c038d775",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "数字农业AI应用课题",
        "ms_introduce": "基于计算机视觉的农作物生长状态智能分析服务",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "f59c2de0-48a6-46c9-b4e4-894ea0ccbac0",
        "service_id": "462e0a2c-a502-4adb-8a0b-ed9fd2cc9332",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "数字农业AI应用课题",
        "ms_introduce": "基于深度学习的病虫害智能识别与防治系统",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "4abaaf60-137a-415d-a7ea-9205a9957310",
        "service_id": "45e0f736-c6c2-4f5d-922f-81c9a70c0c05",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "数字农业AI应用课题",
        "ms_introduce": "基于时序分析的农田智能灌溉决策系统",
        "company_score": 5,
        "ms_score": 4
    },
    {
        "id": "8f0b66ad-838a-4d99-b59f-1ba0be771e6d",
        "service_id": "8995db1a-eeb8-42af-97c1-32e5a4a73c6a",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "数字农业AI应用课题",
        "ms_introduce": "基于机器学习的农作物产量预测服务",
        "company_score": 5,
        "ms_score": 4
    },
    {
        "id": "71028d2d-08f1-429c-9474-b2034bb85b08",
        "service_id": "e8b0b89f-aa4e-4a24-b12d-b68a5ed660d7",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "数字农业AI应用课题",
        "ms_introduce": "基于多代理系统的智慧农业综合管理平台",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "3b790768-0849-4239-ae84-289d6b8f2881",
        "service_id": "4e988dd8-ffbf-4714-baca-3ae60b8a007c",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "低空飞行（eVTOL）AI应用课题",
        "ms_introduce": "基于强化学习的飞行路径规划服务",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "d32081ef-da96-485b-8140-6af58e277946",
        "service_id": "4577e627-156b-4061-9da1-3a1ae14418db",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "低空飞行（eVTOL）AI应用课题",
        "ms_introduce": "基于计算机视觉和多传感器融合的环境感知服务",
        "company_score": 5,
        "ms_score": 4
    },
    {
        "id": "b87de6c7-6cc1-43b8-8432-b420085a2e9a",
        "service_id": "aaed9501-1085-41de-878c-aa106a35cc76",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "低空飞行（eVTOL）AI应用课题",
        "ms_introduce": "基于PID控制算法的飞行姿态控制服务",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "02ade03d-a440-4518-995c-62cda1adfe75",
        "service_id": "ddf3ad0f-3311-4b0f-8780-3e883e8618aa",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "低空飞行（eVTOL）AI应用课题",
        "ms_introduce": "基于时序预测的电池能源管理服务",
        "company_score": 4,
        "ms_score": 5
    },
    {
        "id": "95ffec86-d265-4349-b4b6-2dbba525481e",
        "service_id": "bf06c54b-0953-44ed-a1f1-53b56d569010",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "低空飞行（eVTOL）AI应用课题",
        "ms_introduce": "基于异常检测算法的飞行安全监控服务",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "6ea48704-5007-42cf-b901-48bb2dcfc743",
        "service_id": "8189e54b-ae51-43b6-bf25-7e5391288e3c",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "低空飞行（eVTOL）AI应用课题",
        "ms_introduce": "集成了路径规划、环境感知和飞行控制的综合元应用",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "cbe60308-3372-46af-b55c-38c132e12c44",
        "service_id": "64d4710f-e820-4900-b0a1-659ae8871b97",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "跨境电商AI应用课题",
        "ms_introduce": "垂域多语言生成大模型",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "b4325f5c-7fb1-447d-a62d-619c24f9530a",
        "service_id": "3e846e2c-5c43-4eda-be49-b279cfd68b49",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "跨境电商AI应用课题",
        "ms_introduce": "基于智能体的市场分析算法",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "bf6603f4-1883-4d36-9043-98b8d6f5b36e",
        "service_id": "f043882c-acbe-4737-99d7-5de8bbb3beae",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "跨境电商AI应用课题",
        "ms_introduce": "基于智能体的风险识别算法",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "5f636f68-e16c-474c-8eb1-b19ac0e3b277",
        "service_id": "6f29852e-b8e0-44fe-b7f7-8aacb871e4d3",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "家庭智能助手AI应用课题",
        "ms_introduce": "基于智能体的环境感知算法",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "3fa69edc-e227-4a93-8820-17291812f215",
        "service_id": "078d857f-5f86-48d7-aafb-7f07f74de318",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "家庭智能助手AI应用课题",
        "ms_introduce": "基于多模态情感识别算法",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "345ab401-9e09-4d43-972f-b7c14036caa0",
        "service_id": "300ece69-b80f-4c78-8865-fbda3760aee8",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "家庭智能助手AI应用课题",
        "ms_introduce": "基于多模态情感识别算法",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "34997535-05d0-49ed-9427-f685ad193ae7",
        "service_id": "257154b3-77b8-4ce6-a3c9-c560a60ce10d",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "家庭智能助手AI应用课题",
        "ms_introduce": "基于强化学习的任务规划算法",
        "company_score": 5,
        "ms_score": 5
    },
    {
        "id": "267c724e-88e4-4b12-9053-dce7c2bdbedf",
        "service_id": "0ef523dd-ee18-40bb-a588-d8097f197806",
        "popover_title": "可信云技术服务溯源",
        "company_name": "复旦大学课题组",
        "company_address": "上海市杨浦区邯郸路220号",
        "company_contact": "021-65642222",
        "company_introduce": "家庭智能助手AI应用课题",
        "ms_introduce": "家庭智能助手",
        "company_score": 5,
        "ms_score": 5
    },
]

# MOCK_SERVICE_APIS 数据
MOCK_SERVICE_APIS = [
    {
        "id": "e04e0165-3b18-4d54-ae38-659d04f8aef5",
        "service_id": "8438c51b-4f31-4f44-91b1-f805ff4f5b39",
        "name": "predict",
        "url": "/api/project1/predict",
        "method": "POST",
        "des": "模型推理接口，基于数据集和参数配置得到风险识别结果",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 0,
        "response": None
    },
    {
        "id": "b90b04e2-2ca9-493c-b165-82d1b7f90574",
        "service_id": "8438c51b-4f31-4f44-91b1-f805ff4f5b39",
        "name": "healthCheck",
        "url": "/api/project1/health",
        "method": "GET",
        "des": "判断微服务状态是否正常可用",
        "parameter_type": 0,
        "response_type": 0,
        "is_fake": 0,
        "response": None
    },
    {
        "id": "e04e0165-3b18-4d54-ae38-659d04f8aef5",
        "service_id": "924dc60b-4866-45f2-bd19-f98af257cf6c",
        "name": "predict",
        "url": "/api/project2/predict",
        "method": "POST",
        "des": "模型推理接口，基于数据集和参数配置得到风险识别结果",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 0,
        "response": None
    },
    {
        "id": "b90b04e2-2ca9-493c-b165-82d1b7f90574",
        "service_id": "924dc60b-4866-45f2-bd19-f98af257cf6c",
        "name": "healthCheck",
        "url": "/api/project2/health",
        "method": "GET",
        "des": "判断微服务状态是否正常可用",
        "parameter_type": 0,
        "response_type": 0,
        "is_fake": 0,
        "response": None
    },
    {
        "id": "fb9e80f7-9aad-4ee5-a620-131decf37bec",
        "service_id": "c27fe536-7ac5-413a-84ca-09b6fe218659",
        "name": "train",
        "url": "https://myApiServer.com/technical-assessment/train",
        "method": "POST",
        "des": "",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u8bad\\u7ec3\\u5b8c\\u6210!\", \"data\": {\"modelId\": \"2\", \"modelName\": \"model2\", \"modelVersion\": \"1.0\", \"modelPath\": \"/appdata/aml/model/model2.pkl\"}}"
    },
    {
        "id": "e04e0165-3b18-4d54-ae38-659d04f8aef5",
        "service_id": "c27fe536-7ac5-413a-84ca-09b6fe218659",
        "name": "predict",
        "url": "https://myApiServer.com/technical-assessment/predict",
        "method": "POST",
        "des": "",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u9884\\u6d4b\\u6210\\u529f\\uff01\", \"data\": {\"predictResult\": \"predict result list\"}}"
    },
    {
        "id": "2df635e5-4281-4cbf-832f-006175c6a1ad",
        "service_id": "ea1f0266-ed60-47f7-a29a-717ab0ce0b46",
        "name": "getReportData",
        "url": "https://myApiServer.com/report/get",
        "method": "GET",
        "des": "",
        "parameter_type": 1,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u83b7\\u53d6\\u6210\\u529f!\", \"data\": {\"result\": \"\\u57fa\\u4e8e\\u56fe\\u795e\\u7ecf\\u7f51\\u7edc\\u7684\\u8de8\\u5883\\u8d38\\u6613\\u652f\\u4ed8\\u76d1\\u6d4b\\u6a21\\u578b\\u7684\\u63a8\\u7406\\u7ed3\\u679c\\u5df2\\u7ecf\\u4ea7\\u751f\\u3002\\u6a21\\u578b\\u5728\\u6570\\u636e\\u96c6\\u4e0a\\u7684\\u8868\\u73b0\\u5982\\u4e0b\\uff1a\\n    \\n    \\u5728100\\u4e2a\\u8282\\u70b9\\u4e2d\\uff0c\\u670993\\u4e2a\\u8282\\u70b9\\u88ab\\u5224\\u5b9a\\u4e3a\\u7c7b\\u522b0\\uff0c7\\u4e2a\\u8282\\u70b9\\u88ab\\u5224\\u5b9a\\u4e3a\\u7c7b\\u522b2\\u3002\\u5177\\u4f53\\u7ed3\\u679c\\u5982\\u4e0b\\uff1a\\n    \\n    - \\u7c7b\\u522b0\\uff1a\\u8282\\u70b91\\uff0c\\u8282\\u70b92\\uff0c\\u8282\\u70b93\\uff0c\\u8282\\u70b94\\uff0c\\u8282\\u70b99\\uff0c\\u8282\\u70b910\\uff0c\\u8282\\u70b911\\uff0c\\u8282\\u70b912\\uff0c\\u8282\\u70b913\\uff0c\\u8282\\u70b914\\uff0c\\u8282\\u70b915\\uff0c\\u8282\\u70b916\\uff0c\\u8282\\u70b917\\uff0c\\u8282\\u70b9\\n    18\\uff0c\\u8282\\u70b919\\uff0c\\u8282\\u70b920\\uff0c\\u8282\\u70b921\\uff0c\\u8282\\u70b922\\uff0c\\u8282\\u70b923\\uff0c\\u8282\\u70b924\\uff0c\\u8282\\u70b925\\uff0c\\u8282\\u70b926\\uff0c\\u8282\\u70b927\\uff0c\\u8282\\u70b928\\uff0c\\u8282\\u70b929\\uff0c\\u8282\\u70b930\\uff0c\\u8282\\u70b931\\uff0c\\u8282\\u70b9\\n    32\\uff0c\\u8282\\u70b933\\uff0c\\u8282\\u70b934\\uff0c\\u8282\\u70b935\\uff0c\\u8282\\u70b936\\uff0c\\u8282\\u70b937\\uff0c\\u8282\\u70b938\\uff0c\\u8282\\u70b939\\uff0c\\u8282\\u70b940\\uff0c\\u8282\\u70b941\\uff0c\\u8282\\u70b942\\uff0c\\u8282\\u70b943\\uff0c\\u8282\\u70b944\\uff0c\\u8282\\u70b945\\uff0c\\u8282\\u70b9\\n    46\\uff0c\\u8282\\u70b947\\uff0c\\u8282\\u70b948\\uff0c\\u8282\\u70b949\\uff0c\\u8282\\u70b950\\uff0c\\u8282\\u70b951\\uff0c\\u8282\\u70b952\\uff0c\\u8282\\u70b953\\uff0c\\u8282\\u70b954\\uff0c\\u8282\\u70b955\\uff0c\\u8282\\u70b956\\uff0c\\u8282\\u70b957\\uff0c\\u8282\\u70b958\\uff0c\\u8282\\u70b959\\uff0c\\u8282\\u70b9\\n    60\\uff0c\\u8282\\u70b961\\uff0c\\u8282\\u70b962\\uff0c\\u8282\\u70b963\\uff0c\\u8282\\u70b965\\uff0c\\u8282\\u70b966\\uff0c\\u8282\\u70b967\\uff0c\\u8282\\u70b968\\uff0c\\u8282\\u70b969\\uff0c\\u8282\\u70b970\\uff0c\\u8282\\u70b971\\uff0c\\u8282\\u70b972\\uff0c\\u8282\\u70b973\\uff0c\\u8282\\u70b974\\uff0c\\u8282\\u70b9\\n    75\\uff0c\\u8282\\u70b976\\uff0c\\u8282\\u70b977\\uff0c\\u8282\\u70b978\\uff0c\\u8282\\u70b979\\uff0c\\u8282\\u70b980\\uff0c\\u8282\\u70b981\\uff0c\\u8282\\u70b982\\uff0c\\u8282\\u70b983\\uff0c\\u8282\\u70b984\\uff0c\\u8282\\u70b985\\uff0c\\u8282\\u70b986\\uff0c\\u8282\\u70b987\\uff0c\\u8282\\u70b988\\uff0c\\u8282\\u70b9\\n    89\\uff0c\\u8282\\u70b990\\uff0c\\u8282\\u70b991\\uff0c\\u8282\\u70b992\\uff0c\\u8282\\u70b993\\uff0c\\u8282\\u70b994\\uff0c\\u8282\\u70b995\\uff0c\\u8282\\u70b996\\u3002\\n    \\n    - \\u7c7b\\u522b2\\uff1a\\u8282\\u70b90\\uff0c\\u8282\\u70b95\\uff0c\\u8282\\u70b96\\uff0c\\u8282\\u70b97\\uff0c\\u8282\\u70b98\\uff0c\\u8282\\u70b964\\uff0c\\u8282\\u70b997\\uff0c\\u8282\\u70b998\\uff0c\\u8282\\u70b999\\u3002\\n    \\n    \\u603b\\u7ed3\\uff0c\\u5927\\u591a\\u6570\\u8282\\u70b9\\uff0893%\\uff09\\u88ab\\u5206\\u7c7b\\u4e3a\\u7c7b\\u522b0\\uff0c\\u800c\\u8f83\\u5c0f\\u7684\\u90e8\\u5206\\uff087%\\uff09\\u88ab\\u5206\\u7c7b\\u4e3a\\u7c7b\\u522b2\\u3002\\u8fd9\\u53ef\\u80fd\\u53cd\\u6620\\u4e86\\u5728\\u8bad\\u7ec3\\u96c6\\u4e2d\\u7c7b\\u522b0\\u7684\\u6837\\u672c\\u6570\\u91cf\\u66f4\\u591a\\n    \\uff0c\\u6a21\\u578b\\u5728\\u8bc6\\u522b\\u7c7b\\u522b0\\u7684\\u80fd\\u529b\\u4e0a\\u8868\\u73b0\\u5f97\\u66f4\\u597d\\u3002\\u540c\\u65f6\\uff0c\\u6a21\\u578b\\u5bf9\\u4e8e\\u7c7b\\u522b2\\u7684\\u8bc6\\u522b\\u4e5f\\u6709\\u4e00\\u5b9a\\u7684\\u80fd\\u529b\\u3002\"}}"
    },
    {
        "id": "590017b7-fa60-4d07-a7e9-d668b32e033b",
        "service_id": "ea1f0266-ed60-47f7-a29a-717ab0ce0b46",
        "name": "sendReport",
        "url": "https://myApiServer.com/report/send",
        "method": "GET",
        "des": "",
        "parameter_type": 1,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u53d1\\u9001\\u6210\\u529f\\uff01\", \"data\": {\"reportId\": \"1\"}}"
    },
    {
        "id": "eebfb433-46e7-477a-9abb-057ef90daacd",
        "service_id": "ea1f0266-ed60-47f7-a29a-717ab0ce0b46",
        "name": "generateReport",
        "url": "https://myApiServer.com/report-generation/generate",
        "method": "POST",
        "des": "报告生成接口样例",
        "parameter_type": 3,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u751f\\u6210\\u6210\\u529f\\uff01\", \"data\": {\"reportPath\": \"/appdata/aml/report/report1.pdf\"}}"
    },
    {
        "id": "fb9e80f7-9aad-4ee5-a620-131decf37bec",
        "service_id": "1da6516e-c61f-43c8-adca-91fa0ab2d2ac",
        "name": "train",
        "url": "https://myApiServer.com/credit-assessment/train",
        "method": "POST",
        "des": "",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u8bad\\u7ec3\\u5b8c\\u6210!\", \"data\": {\"modelId\": \"4\", \"modelName\": \"model4\", \"modelVersion\": \"1.0\", \"modelPath\": \"/appdata/aml/model/model3.pkl\"}}"
    },
    {
        "id": "e04e0165-3b18-4d54-ae38-659d04f8aef5",
        "service_id": "1da6516e-c61f-43c8-adca-91fa0ab2d2ac",
        "name": "predict",
        "url": "https://myApiServer.com/credit-assessment/predict",
        "method": "POST",
        "des": "",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u9884\\u6d4b\\u6210\\u529f\\uff01\", \"data\": {\"predictResult\": \"predict result list\"}}"
    },
    {
        "id": "b4f21aaa-6280-49b4-8db6-b8d7e4561df2",
        "service_id": "61ddfb7b-aa8e-47e7-a84d-bbb3b546052c",
        "name": "preprocess",
        "url": "https://myApiServer.com/anomaly-detection/preprocess",
        "method": "POST",
        "des": "",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u9884\\u5904\\u7406\\u6210\\u529f!\", \"data\": {\"modelId\": \"4\", \"modelName\": \"model4\", \"modelVersion\": \"1.0\", \"modelPath\": \"/appdata/aml/data/data4.pkl\"}}"
    },
    {
        "id": "fb9e80f7-9aad-4ee5-a620-131decf37bec",
        "service_id": "61ddfb7b-aa8e-47e7-a84d-bbb3b546052c",
        "name": "train",
        "url": "https://myApiServer.com/anomaly-detection/train",
        "method": "POST",
        "des": "",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u8bad\\u7ec3\\u5b8c\\u6210!\", \"data\": {\"modelId\": \"4\", \"modelName\": \"model4\", \"modelVersion\": \"1.0\", \"modelPath\": \"/appdata/aml/model/model4.pkl\"}}"
    },
    {
        "id": "e04e0165-3b18-4d54-ae38-659d04f8aef5",
        "service_id": "61ddfb7b-aa8e-47e7-a84d-bbb3b546052c",
        "name": "predict",
        "url": "https://myApiServer.com/anomaly-detection/predict",
        "method": "POST",
        "des": "",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u9884\\u6d4b\\u6210\\u529f\\uff01\", \"data\": {\"predictResult\": \"predict result list\"}}"
    },
    {
        "id": "f49b20ec-dfab-4ca7-a462-fa2c07a5f919",
        "service_id": "61ddfb7b-aa8e-47e7-a84d-bbb3b546052c",
        "name": "evaluate",
        "url": "https://myApiServer.com/anomaly-detection/evaluate",
        "method": "POST",
        "des": "",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u8bc4\\u4f30\\u6210\\u529f\\uff01\", \"data\": {\"evaluateResult\": \"evaluate result list\"}}"
    },
    {
        "id": "0a92bf34-5b57-497f-b5d2-6facadda0469",
        "service_id": "61ddfb7b-aa8e-47e7-a84d-bbb3b546052c",
        "name": "visualize",
        "url": "https://myApiServer.com/anomaly-detection/visualize",
        "method": "POST",
        "des": "",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u53ef\\u89c6\\u5316\\u6210\\u529f\\uff01\", \"data\": {\"visualizeResult\": \"visualize result list\"}}"
    },
    {
        "id": "c8f9b07b-b7bb-47e9-ade9-17937dda65c3",
        "service_id": "42320ee0-39b3-4180-8231-77b951a16997",
        "name": "generate-report",
        "url": "/api/project3/generate-report",
        "method": "GET",
        "des": "根据自然语言需求生成风险评估报告",
        "parameter_type": 1,
        "response_type": 2,
        "is_fake": 0,
        "response": None
    },
    {
        "id": "78a9058c-affa-4af2-9ec5-af12e5eef50d",
        "service_id": "42320ee0-39b3-4180-8231-77b951a16997",
        "name": "nl2gql",
        "url": "/api/project3/nl2gql",
        "method": "GET",
        "des": "根据自然语言需求生成gql语句并得到查询结果",
        "parameter_type": 1,
        "response_type": 1,
        "is_fake": 0,
        "response": None
    },
    {
        "id": "b90b04e2-2ca9-493c-b165-82d1b7f90574",
        "service_id": "42320ee0-39b3-4180-8231-77b951a16997",
        "name": "healthCheck",
        "url": "/api/project3/health",
        "method": "GET",
        "des": "判断微服务状态是否正常可用",
        "parameter_type": 0,
        "response_type": 0,
        "is_fake": 0,
        "response": None
    },
    {
        "id": "e59e68c3-3d03-4e36-b6ce-71673b261005",
        "service_id": "f6ac8879-e20c-4109-bddc-069e5f9dd458",
        "name": "safety-fingerprint",
        "url": "/api/project4/safety/safety-fingerprint",
        "method": "POST",
        "des": "",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 0,
        "response": None
    },
    {
        "id": "b90b04e2-2ca9-493c-b165-82d1b7f90574",
        "service_id": "f6ac8879-e20c-4109-bddc-069e5f9dd458",
        "name": "healthCheck",
        "url": "/api/project4/safety/health",
        "method": "GET",
        "des": "",
        "parameter_type": 0,
        "response_type": 0,
        "is_fake": 0,
        "response": None
    },
    {
        "id": "d5475ad3-d6ce-437c-bfc5-c1e3e8639301",
        "service_id": "b48f8cb6-415b-4374-9ac1-e3287d484c79",
        "name": "技术评测元应用",
        "url": "https://myApiServer.com/metaApp",
        "method": "POST",
        "des": "",
        "parameter_type": 3,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u8bc4\\u6d4b\\u5b8c\\u6bd5\\uff01\", \"data\": {\"securityResult\": \"5.0\", \"robustnessResult\": \"5.0\", \"privacyResult\": \"5.0\", \"credibilityResult\": \"5.0\"}}"
    },
    {
        "id": "83ed1e7d-3be4-4e15-b23f-44df74d59e35",
        "service_id": "2a971817-12df-412c-982b-0773e5ca757e",
        "name": "无人机智能投递",
        "url": "https://myApiServer.com/air/target",
        "method": "POST",
        "des": "",
        "parameter_type": 3,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u4efb\\u52a1\\u5df2\\u5f00\\u59cb\"}"
    },
    {
        "id": "c35b0b2c-2b11-4279-914e-e6e751f8e00a",
        "service_id": "7c0a984a-90e6-40f7-bd1b-76b559e6dd5a",
        "name": "calculate",
        "url": "/api/linezolid/calculate",
        "method": "POST",
        "des": "根据患者的基本信息计算推荐的利奈唑胺给药剂量",
        "parameter_type": 3,
        "response_type": 1,
        "is_fake": 0,
        "response": None
    },
    {
        "id": "b90b04e2-2ca9-493c-b165-82d1b7f90574",
        "service_id": "7c0a984a-90e6-40f7-bd1b-76b559e6dd5a",
        "name": "healthCheck",
        "url": "/api/linezolid/health",
        "method": "GET",
        "des": "判断微服务状态是否正常可用",
        "parameter_type": 0,
        "response_type": 0,
        "is_fake": 0,
        "response": None
    },
    {
        "id": "37dc651e-1559-44b9-8fbf-a23e96b41b23",
        "service_id": "2d73797c-09a9-4960-88f0-88252affb06a",
        "name": "diagnose",
        "url": "https://myApiServer.com/health/diagnose",
        "method": "POST",
        "des": "模型推理接口，基于医学影像数据进行辅助诊断",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u8bca\\u65ad\\u5b8c\\u6210\\uff01\", \"data\": {\"diagnosisResult\": \"\\u9ad8\\u5ea6\\u7591\\u4f3c\\u80ba\\u90e8\\u611f\\u67d3\\uff0c\\u5efa\\u8bae\\u8fdb\\u4e00\\u6b65\\u68c0\\u67e5\", \"confidence\": 0.89, \"annotations\": {\"regions\": [{\"x\": 120, \"y\": 150, \"width\": 50, \"height\": 40}, {\"x\": 200, \"y\": 180, \"width\": 30, \"height\": 25}], \"type\": \"\\u5f02\\u5e38\\u533a\\u57df\"}}}"
    },
    {
        "id": "b90b04e2-2ca9-493c-b165-82d1b7f90574",
        "service_id": "2d73797c-09a9-4960-88f0-88252affb06a",
        "name": "healthCheck",
        "url": "https://myApiServer.com/health/health",
        "method": "GET",
        "des": "判断微服务状态是否正常可用",
        "parameter_type": 0,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u670d\\u52a1\\u8fd0\\u884c\\u6b63\\u5e38\", \"data\": {\"status\": \"healthy\", \"uptime\": \"72h 15m\"}}"
    },
    {
        "id": "c3b1cfa6-9c0a-49d4-86ed-99c9ce5319bd",
        "service_id": "6fd78779-3663-4929-88c3-e250b8ccef41",
        "name": "analyze",
        "url": "https://myApiServer.com/health/monitor/analyze",
        "method": "POST",
        "des": "分析健康数据并提供管理建议",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u5206\\u6790\\u5b8c\\u6210\\uff01\", \"data\": {\"patientStatus\": \"\\u8840\\u7cd6\\u6c34\\u5e73\\u6ce2\\u52a8\\u8f83\\u5927\", \"riskLevel\": \"\\u4e2d\\u7b49\", \"recommendations\": [\"\\u589e\\u52a0\\u9910\\u540e30\\u5206\\u949f\\u6d4b\\u91cf\\u9891\\u7387\", \"\\u8c03\\u6574\\u80f0\\u5c9b\\u7d20\\u7528\\u91cf\", \"\\u6bcf\\u65e530\\u5206\\u949f\\u4f4e\\u5f3a\\u5ea6\\u8fd0\\u52a8\"], \"nextCheckupDate\": \"2023-06-15\"}}"
    },
    {
        "id": "dc1b1514-f05a-449a-ae67-84143636d1a1",
        "service_id": "6fd78779-3663-4929-88c3-e250b8ccef41",
        "name": "alert",
        "url": "https://myApiServer.com/health/monitor/alert",
        "method": "POST",
        "des": "设置健康预警阈值和通知",
        "parameter_type": 2,
        "response_type": 0,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u9884\\u8b66\\u8bbe\\u7f6e\\u6210\\u529f\\uff01\", \"data\": {\"alertId\": \"12345\", \"thresholds\": {\"bloodPressureHigh\": \"140/90\", \"bloodPressureLow\": \"90/60\", \"bloodSugarHigh\": \"11.1\", \"bloodSugarLow\": \"3.9\"}, \"notificationChannels\": [\"SMS\", \"App\", \"Family\"]}}"
    },
    {
        "id": "eb71aac4-245e-42ef-9f45-a15febac7054",
        "service_id": "b55a50bf-a123-4a47-81e1-7104eb979440",
        "name": "transcribe",
        "url": "https://myApiServer.com/health/voice/transcribe",
        "method": "POST",
        "des": "将方言语音转写为标准文字",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u8f6c\\u5199\\u6210\\u529f\\uff01\", \"data\": {\"originalDialect\": \"\\u56db\\u5ddd\\u65b9\\u8a00\", \"standardText\": \"\\u6211\\u6700\\u8fd1\\u611f\\u89c9\\u8eab\\u4f53\\u4e0d\\u592a\\u8212\\u670d\\uff0c\\u5934\\u6655\\u5934\\u75db\\uff0c\\u60f3\\u6302\\u53f7\\u770b\\u533b\\u751f\", \"confidence\": 0.92, \"duration\": \"15\\u79d2\", \"medicalTerms\": [{\"term\": \"\\u5934\\u6655\", \"standard\": true}, {\"term\": \"\\u5934\\u75db\", \"standard\": true}]}}"
    },
    {
        "id": "11850741-9979-4a5b-ae18-75dd8b2199e6",
        "service_id": "6d758804-6de8-4fa7-9a31-4b3e8d8241c3",
        "name": "allocate",
        "url": "https://myApiServer.com/health/resource/allocate",
        "method": "POST",
        "des": "根据急诊情况优化医疗资源调度",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u8d44\\u6e90\\u8c03\\u5ea6\\u5b8c\\u6210\\uff01\", \"data\": {\"emergencyLevel\": \"\\u4e2d\\u5ea6\\u7d27\\u6025\", \"allocatedResources\": [{\"type\": \"\\u6551\\u62a4\\u8f66\", \"eta\": \"15\\u5206\\u949f\", \"distance\": \"8.5\\u516c\\u91cc\"}, {\"type\": \"\\u6025\\u8bca\\u533b\\u5e08\", \"status\": \"\\u5f85\\u547d\", \"specialty\": \"\\u5185\\u79d1\"}], \"nearestHospital\": {\"name\": \"\\u53bf\\u4eba\\u6c11\\u533b\\u9662\", \"distance\": \"12\\u516c\\u91cc\", \"availableBeds\": 3, \"specialtyAvailable\": [\"\\u5185\\u79d1\", \"\\u5916\\u79d1\", \"\\u6025\\u8bca\"]}, \"alternativeFacilities\": [{\"name\": \"\\u9547\\u536b\\u751f\\u9662\", \"distance\": \"3\\u516c\\u91cc\", \"capabilities\": \"\\u57fa\\u7840\\u5904\\u7406\"}]}}"
    },
    {
        "id": "e04e0165-3b18-4d54-ae38-659d04f8aef5",
        "service_id": "522f944a-2a1c-4ef3-a4e8-7ebde3fccc1c",
        "name": "predict",
        "url": "https://myApiServer.com/health/epidemic/predict",
        "method": "POST",
        "des": "分析历史数据预测流行病发展趋势",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u9884\\u6d4b\\u5206\\u6790\\u5b8c\\u6210\\uff01\", \"data\": {\"diseaseName\": \"\\u5b63\\u8282\\u6027\\u6d41\\u611f\", \"riskLevel\": \"\\u9ad8\", \"predictedPeakTime\": \"2023\\u5e7412\\u6708\\u4e0a\\u65ec\", \"affectedAreas\": [{\"name\": \"\\u6653\\u5e84\\u6751\", \"riskLevel\": \"\\u6781\\u9ad8\", \"population\": 1200}, {\"name\": \"\\u6cb3\\u897f\\u9547\", \"riskLevel\": \"\\u9ad8\", \"population\": 5000}, {\"name\": \"\\u4e1c\\u6797\\u53bf\", \"riskLevel\": \"\\u4e2d\", \"population\": 32000}], \"preventionRecommendations\": [\"\\u63d0\\u524d\\u4e24\\u5468\\u5f00\\u59cb\\u75ab\\u82d7\\u63a5\\u79cd\", \"\\u52a0\\u5f3a\\u5b66\\u6821\\u548c\\u516c\\u5171\\u573a\\u6240\\u6d88\\u6bd2\", \"\\u51c6\\u5907\\u5145\\u8db3\\u533b\\u7597\\u7269\\u8d44\"], \"predictionAccuracy\": \"85%\"}}"
    },
    {
        "id": "199c0645-a55f-45ff-a09c-5e535e091534",
        "service_id": "f4ab84fd-fda9-4bdf-a840-0718f2417dbe",
        "name": "乡村医疗AI辅助诊断元应用",
        "url": "https://myApiServer.com/health/metaApp",
        "method": "POST",
        "des": "",
        "parameter_type": 3,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u8bca\\u65ad\\u5b8c\\u6210\\uff01\", \"data\": {\"patientInfo\": {\"age\": 65, \"gender\": \"\\u7537\", \"symptoms\": [\"\\u80f8\\u95f7\", \"\\u54b3\\u55fd\", \"\\u53d1\\u70ed\"], \"medicalHistory\": \"\\u9ad8\\u8840\\u538b\\uff0c2\\u578b\\u7cd6\\u5c3f\\u75c5\"}, \"diagnosisResult\": {\"primaryDiagnosis\": \"\\u80ba\\u90e8\\u611f\\u67d3\", \"confidence\": 0.92, \"alternativeDiagnosis\": [\"\\u6162\\u6027\\u652f\\u6c14\\u7ba1\\u708e\", \"\\u80ba\\u6c14\\u80bf\"], \"riskLevel\": \"\\u4e2d\\u9ad8\\u98ce\\u9669\"}, \"recommendations\": [\"\\u5efa\\u8bae\\u8fdb\\u884c\\u6297\\u751f\\u7d20\\u6cbb\\u7597\", \"\\u5bc6\\u5207\\u76d1\\u6d4b\\u8840\\u6c27\\u6c34\\u5e73\", \"\\u4e00\\u5468\\u540e\\u590d\\u67e5\"], \"referralNeeded\": true, \"referToSpecialist\": \"\\u547c\\u5438\\u79d1\\u4e13\\u5bb6\"}}"
    },
    {
        "id": "17043d06-188f-4909-b32d-cbbbb7680a64",
        "service_id": "93314394-b92d-4e42-9ec2-b0f3cd436f39",
        "name": "农村公共卫生监测元应用",
        "url": "https://myApiServer.com/health/publicHealth/monitor",
        "method": "POST",
        "des": "",
        "parameter_type": 3,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u5206\\u6790\\u5b8c\\u6210\\uff01\", \"data\": {\"regionOverview\": {\"name\": \"\\u4e1c\\u6797\\u53bf\\u53ca\\u5468\\u8fb9\\u4e61\\u9547\", \"population\": 120000, \"medicalFacilities\": 15, \"healthcareWorkers\": 230}, \"epidemicStatus\": {\"currentOutbreaks\": [{\"disease\": \"\\u5b63\\u8282\\u6027\\u6d41\\u611f\", \"cases\": 325, \"trend\": \"\\u4e0a\\u5347\"}, {\"disease\": \"\\u624b\\u8db3\\u53e3\\u75c5\", \"cases\": 48, \"trend\": \"\\u7a33\\u5b9a\"}], \"predictions\": [{\"disease\": \"\\u5b63\\u8282\\u6027\\u6d41\\u611f\", \"peakTime\": \"2023\\u5e7412\\u6708\\u4e0a\\u65ec\", \"estimatedCases\": 500}, {\"disease\": \"\\u8179\\u6cfb\", \"peakTime\": \"2023\\u5e747\\u6708\", \"estimatedCases\": 200}]}, \"resourceAllocation\": {\"criticalShortages\": [\"\\u513f\\u79d1\\u533b\\u751f\", \"\\u547c\\u5438\\u79d1\\u4e13\\u5bb6\"], \"recommendedDistribution\": [{\"resource\": \"\\u6d41\\u611f\\u75ab\\u82d7\", \"allocateTo\": [\"\\u6cb3\\u897f\\u9547\", \"\\u6653\\u5e84\\u6751\"], \"quantity\": 2000}, {\"resource\": \"\\u9632\\u62a4\\u53e3\\u7f69\", \"allocateTo\": [\"\\u6240\\u6709\\u5b66\\u6821\", \"\\u517b\\u8001\\u9662\"], \"quantity\": 10000}]}, \"preventionActions\": [\"\\u52a0\\u5f3a\\u5b66\\u6821\\u6668\\u68c0\", \"\\u63d0\\u524d\\u542f\\u52a8\\u75ab\\u82d7\\u63a5\\u79cd\\u8ba1\\u5212\", \"\\u519c\\u6751\\u533b\\u751f\\u57f9\\u8bad\"]}}"
    },
    {
        "id": "4b71974a-2d65-412a-b25d-13c0924d1abb",
        "service_id": "9d780c5e-8cac-4139-9753-0801c038d775",
        "name": "analyzeImage",
        "url": "https://myApiServer.com/agriculture/image/analyze",
        "method": "POST",
        "des": "分析农作物图像，识别生长状态",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u5206\\u6790\\u6210\\u529f\", \"data\": {\"status\": \"healthy\", \"growthStage\": \"flowering\", \"confidence\": 0.95, \"estimatedHarvestDate\": \"2023-09-15\", \"recommendations\": [\"\\u9002\\u91cf\\u6d47\\u6c34\", \"\\u589e\\u52a0\\u5149\\u7167\", \"\\u9632\\u6cbb\\u767d\\u7c89\\u75c5\"], \"nutritionStatus\": {\"nitrogen\": \"\\u9002\\u5b9c\", \"phosphorus\": \"\\u504f\\u4f4e\", \"potassium\": \"\\u9002\\u5b9c\"}}}"
    },
    {
        "id": "b90b04e2-2ca9-493c-b165-82d1b7f90574",
        "service_id": "9d780c5e-8cac-4139-9753-0801c038d775",
        "name": "healthCheck",
        "url": "https://myApiServer.com/agriculture/health",
        "method": "GET",
        "des": "健康检查接口",
        "parameter_type": 0,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u670d\\u52a1\\u6b63\\u5e38\", \"data\": {\"status\": \"running\", \"uptime\": \"65d 12h 37m\", \"version\": \"2.3.5\", \"memoryUsage\": \"45%\", \"cpuUsage\": \"12%\"}}"
    },
    {
        "id": "3d939529-0043-4b2f-a906-2dc5714dc84d",
        "service_id": "462e0a2c-a502-4adb-8a0b-ed9fd2cc9332",
        "name": "identifyDisease",
        "url": "https://myApiServer.com/agriculture/disease/identify",
        "method": "POST",
        "des": "识别农作物病虫害",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u8bc6\\u522b\\u6210\\u529f\", \"data\": {\"disease\": \"\\u7a3b\\u761f\\u75c5\", \"confidence\": 0.92, \"severity\": \"\\u4e2d\\u5ea6\", \"affectedArea\": \"30%\", \"treatment\": [\"\\u55b7\\u6d12\\u6740\\u83cc\\u5242\", \"\\u589e\\u52a0\\u901a\\u98ce\"], \"preventionMeasures\": [\"\\u52a0\\u5f3a\\u7530\\u95f4\\u7ba1\\u7406\", \"\\u9009\\u62e9\\u6297\\u75c5\\u54c1\\u79cd\"], \"spreadRisk\": \"\\u9ad8\", \"economicImpact\": \"\\u4ea7\\u91cf\\u53ef\\u80fd\\u964d\\u4f4e15-20%\"}}"
    },
    {
        "id": "b90b04e2-2ca9-493c-b165-82d1b7f90574",
        "service_id": "462e0a2c-a502-4adb-8a0b-ed9fd2cc9332",
        "name": "healthCheck",
        "url": "https://myApiServer.com/agriculture/disease/health",
        "method": "GET",
        "des": "健康检查接口",
        "parameter_type": 0,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u670d\\u52a1\\u6b63\\u5e38\", \"data\": {\"status\": \"running\", \"uptime\": \"42d 5h 18m\", \"version\": \"1.8.2\", \"memoryUsage\": \"38%\", \"cpuUsage\": \"5%\"}}"
    },
    {
        "id": "0f5179d4-3bc7-4c0e-9bac-cb2a97c5386e",
        "service_id": "45e0f736-c6c2-4f5d-922f-81c9a70c0c05",
        "name": "getIrrigationPlan",
        "url": "https://myApiServer.com/agriculture/irrigation/plan",
        "method": "POST",
        "des": "获取智能灌溉计划",
        "parameter_type": 1,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u704c\\u6e89\\u8ba1\\u5212\\u751f\\u6210\\u6210\\u529f\", \"data\": {\"shouldIrrigate\": true, \"recommendedAmount\": 30, \"unit\": \"\\u7acb\\u65b9\\u7c73/\\u4ea9\", \"timing\": \"\\u4eca\\u65e5\\u508d\\u665a\", \"reason\": \"\\u571f\\u58e4\\u6e7f\\u5ea6\\u4f4e\\u4e8e\\u4f5c\\u7269\\u9700\\u6c42\", \"waterSavings\": \"\\u7ea625%\\uff08\\u4e0e\\u4f20\\u7edf\\u704c\\u6e89\\u76f8\\u6bd4\\uff09\", \"nextAssessment\": \"3\\u5929\\u540e\", \"weatherForecast\": \"\\u672a\\u67653\\u5929\\u65e0\\u6709\\u6548\\u964d\\u6c34\", \"irrigationZones\": [{\"zone\": \"A\", \"priority\": \"\\u9ad8\", \"amount\": 35}, {\"zone\": \"B\", \"priority\": \"\\u4e2d\", \"amount\": 30}, {\"zone\": \"C\", \"priority\": \"\\u4f4e\", \"amount\": 25}]}}"
    },
    {
        "id": "b90b04e2-2ca9-493c-b165-82d1b7f90574",
        "service_id": "45e0f736-c6c2-4f5d-922f-81c9a70c0c05",
        "name": "healthCheck",
        "url": "https://myApiServer.com/agriculture/irrigation/health",
        "method": "GET",
        "des": "健康检查接口",
        "parameter_type": 0,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u670d\\u52a1\\u6b63\\u5e38\", \"data\": {\"status\": \"running\", \"uptime\": \"28d 9h 42m\", \"version\": \"3.1.0\", \"memoryUsage\": \"32%\", \"cpuUsage\": \"8%\"}}"
    },
    {
        "id": "fa339134-1472-4421-bed3-2e516ef14156",
        "service_id": "8995db1a-eeb8-42af-97c1-32e5a4a73c6a",
        "name": "predictYield",
        "url": "https://myApiServer.com/agriculture/yield/predict",
        "method": "POST",
        "des": "预测农作物产量",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u4ea7\\u91cf\\u9884\\u6d4b\\u5b8c\\u6210\", \"data\": {\"predictedYield\": 550, \"unit\": \"\\u516c\\u65a4/\\u4ea9\", \"confidenceInterval\": [520, 580], \"harvestDate\": \"2023-10-05\\u81f32023-10-15\", \"comparisonWithLastYear\": \"+5.2%\", \"factors\": [{\"name\": \"\\u6c14\\u5019\\u6761\\u4ef6\", \"impact\": \"\\u6b63\\u9762\", \"description\": \"\\u4eca\\u5e74\\u964d\\u6c34\\u91cf\\u9002\\u5b9c\"}, {\"name\": \"\\u571f\\u58e4\\u72b6\\u51b5\", \"impact\": \"\\u4e2d\\u6027\", \"description\": \"\\u571f\\u58e4\\u80a5\\u529b\\u9002\\u4e2d\"}, {\"name\": \"\\u75c5\\u866b\\u5bb3\\u98ce\\u9669\", \"impact\": \"\\u8d1f\\u9762\", \"description\": \"\\u7a3b\\u98de\\u8671\\u98ce\\u9669\\u589e\\u52a0\"}], \"recommendations\": [\"\\u4f18\\u5316\\u65bd\\u80a5\\u65b9\\u6848\\u53ef\\u80fd\\u8fdb\\u4e00\\u6b65\\u63d0\\u9ad8\\u4ea7\\u91cf\", \"\\u6ce8\\u610f\\u9632\\u6cbb\\u7a3b\\u98de\\u8671\", \"\\u9002\\u5f53\\u5ef6\\u957f\\u704c\\u6e89\\u5468\\u671f\"]}}"
    },
    {
        "id": "b90b04e2-2ca9-493c-b165-82d1b7f90574",
        "service_id": "8995db1a-eeb8-42af-97c1-32e5a4a73c6a",
        "name": "healthCheck",
        "url": "https://myApiServer.com/agriculture/yield/health",
        "method": "GET",
        "des": "健康检查接口",
        "parameter_type": 0,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u670d\\u52a1\\u6b63\\u5e38\", \"data\": {\"status\": \"running\", \"uptime\": \"15d 22h 55m\", \"version\": \"2.0.4\", \"memoryUsage\": \"41%\", \"cpuUsage\": \"7%\"}}"
    },
    {
        "id": "8a4765d9-a024-473d-bd01-6cefc07d2081",
        "service_id": "e8b0b89f-aa4e-4a24-b12d-b68a5ed660d7",
        "name": "智慧农业综合管理元应用",
        "url": "https://myApiServer.com/agriculture/metaApp",
        "method": "POST",
        "des": "",
        "parameter_type": 3,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u5206\\u6790\\u5b8c\\u6210\", \"data\": {\"predictedYield\": 550, \"unit\": \"\\u516c\\u65a4/\\u4ea9\", \"confidenceInterval\": [520, 580], \"harvestDate\": \"2023-10-05\\u81f32023-10-15\", \"comparisonWithLastYear\": \"+5.2%\", \"factors\": [{\"name\": \"\\u6c14\\u5019\\u6761\\u4ef6\", \"impact\": \"\\u6b63\\u9762\", \"description\": \"\\u4eca\\u5e74\\u964d\\u6c34\\u91cf\\u9002\\u5b9c\"}, {\"name\": \"\\u571f\\u58e4\\u72b6\\u51b5\", \"impact\": \"\\u4e2d\\u6027\", \"description\": \"\\u571f\\u58e4\\u80a5\\u529b\\u9002\\u4e2d\"}, {\"name\": \"\\u75c5\\u866b\\u5bb3\\u98ce\\u9669\", \"impact\": \"\\u8d1f\\u9762\", \"description\": \"\\u7a3b\\u98de\\u8671\\u98ce\\u9669\\u589e\\u52a0\"}], \"recommendations\": [\"\\u4f18\\u5316\\u65bd\\u80a5\\u65b9\\u6848\\u53ef\\u80fd\\u8fdb\\u4e00\\u6b65\\u63d0\\u9ad8\\u4ea7\\u91cf\", \"\\u6ce8\\u610f\\u9632\\u6cbb\\u7a3b\\u98de\\u8671\", \"\\u9002\\u5f53\\u5ef6\\u957f\\u704c\\u6e89\\u5468\\u671f\"]}}"
    },
    {
        "id": "f7b3a3a6-ae2a-4e0a-9764-6ab98605d592",
        "service_id": "4e988dd8-ffbf-4714-baca-3ae60b8a007c",
        "name": "pathPlanner",
        "url": "https://myApiServer.com/evtol/path/plan",
        "method": "POST",
        "des": "规划飞行路径，避开障碍物",
        "parameter_type": 3,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u8def\\u5f84\\u89c4\\u5212\\u6210\\u529f\\uff01\", \"data\": {\"pathPoints\": [{\"lat\": 31.2304, \"lng\": 121.4737, \"altitude\": 120}, {\"lat\": 31.2324, \"lng\": 121.4757, \"altitude\": 150}, {\"lat\": 31.2354, \"lng\": 121.4787, \"altitude\": 150}, {\"lat\": 31.2384, \"lng\": 121.4817, \"altitude\": 120}], \"estimatedTime\": \"15\\u5206\\u949f\", \"distance\": \"12.5\\u516c\\u91cc\", \"energyConsumption\": \"30%\", \"weatherRisk\": \"\\u4f4e\", \"noFlyZonesAvoided\": 3}}"
    },
    {
        "id": "bcb8d724-5b02-4729-b61f-d36e4802eaa1",
        "service_id": "4577e627-156b-4061-9da1-3a1ae14418db",
        "name": "environmentPerception",
        "url": "https://myApiServer.com/evtol/perception",
        "method": "POST",
        "des": "感知周围环境，识别障碍物和导航信息",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u73af\\u5883\\u611f\\u77e5\\u5b8c\\u6210\\uff01\", \"data\": {\"detectedObjects\": [{\"type\": \"\\u5efa\\u7b51\\u7269\", \"distance\": 120, \"direction\": \"\\u4e1c\\u5317\", \"height\": 80}, {\"type\": \"\\u7535\\u7ebf\", \"distance\": 50, \"direction\": \"\\u6b63\\u524d\\u65b9\", \"height\": 30}, {\"type\": \"\\u5176\\u4ed6\\u98de\\u884c\\u5668\", \"distance\": 500, \"direction\": \"\\u897f\", \"height\": 150, \"velocity\": {\"speed\": 40, \"heading\": 90}}], \"weatherConditions\": {\"visibility\": \"\\u826f\\u597d\", \"windSpeed\": \"5\\u7c73/\\u79d2\", \"windDirection\": \"\\u897f\\u5317\", \"precipitation\": \"\\u65e0\"}, \"terrainFeatures\": {\"slope\": \"\\u5e73\\u5766\", \"elevation\": \"\\u6d77\\u62d435\\u7c73\", \"surfaceType\": \"\\u57ce\\u5e02\\u5efa\\u7b51\\u533a\"}, \"confidenceScore\": 0.92}}"
    },
    {
        "id": "a22ff83e-009e-40ea-a658-5300d6d25e11",
        "service_id": "4577e627-156b-4061-9da1-3a1ae14418db",
        "name": "obstacleDetection",
        "url": "https://myApiServer.com/evtol/obstacle",
        "method": "POST",
        "des": "检测障碍物并提供避险建议",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u969c\\u788d\\u7269\\u68c0\\u6d4b\\u5b8c\\u6210\\uff01\", \"data\": {\"obstaclesDetected\": true, \"obstacleCount\": 3, \"criticalObstacles\": 1, \"emergencyAction\": \"\\u5411\\u53f3\\u504f\\u822a15\\u5ea6\", \"timeToImpact\": \"8.5\\u79d2\"}}"
    },
    {
        "id": "2f6e70a5-ff4a-4bae-be66-b7adf0d4d47c",
        "service_id": "aaed9501-1085-41de-878c-aa106a35cc76",
        "name": "flightController",
        "url": "https://myApiServer.com/evtol/control",
        "method": "POST",
        "des": "控制飞行姿态和动作",
        "parameter_type": 3,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u63a7\\u5236\\u547d\\u4ee4\\u5df2\\u6267\\u884c\\uff01\", \"data\": {\"commandStatus\": \"executed\", \"currentAttitude\": {\"pitch\": 5, \"roll\": 0, \"yaw\": 270}, \"currentAltitude\": 150, \"currentSpeed\": 70, \"flightMode\": \"cruise\", \"stability\": \"\\u4f18\\u79c0\", \"responseTime\": \"0.05\\u79d2\"}}"
    },
    {
        "id": "36ef2f7e-3dab-479c-a6fb-a04dcc04e54c",
        "service_id": "ddf3ad0f-3311-4b0f-8780-3e883e8618aa",
        "name": "batteryManager",
        "url": "https://myApiServer.com/evtol/battery",
        "method": "POST",
        "des": "管理电池能源使用",
        "parameter_type": 3,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u80fd\\u6e90\\u5206\\u6790\\u5b8c\\u6210\\uff01\", \"data\": {\"currentCharge\": \"72%\", \"estimatedRemaining\": \"38\\u5206\\u949f\", \"rangeRemaining\": \"45\\u516c\\u91cc\", \"dischargeCurve\": [{\"time\": 0, \"charge\": 72}, {\"time\": 10, \"charge\": 65}, {\"time\": 20, \"charge\": 58}, {\"time\": 30, \"charge\": 50}], \"recommendations\": [\"\\u964d\\u4f4e\\u98de\\u884c\\u9ad8\\u5ea6\\u53ef\\u5ef6\\u957f\\u7eed\\u822a\\u65f6\\u95f4\", \"\\u51cf\\u5c11\\u6025\\u52a0\\u901f\\u4ee5\\u4f18\\u5316\\u80fd\\u6e90\\u4f7f\\u7528\"], \"criticalLevel\": false, \"optimalSpeed\": 65}}"
    },
    {
        "id": "ec3fc278-2d77-4c52-a5e9-55a7c2ab9536",
        "service_id": "ddf3ad0f-3311-4b0f-8780-3e883e8618aa",
        "name": "energyOptimizer",
        "url": "https://myApiServer.com/evtol/energy/optimize",
        "method": "POST",
        "des": "优化能源使用策略",
        "parameter_type": 3,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u80fd\\u6e90\\u4f18\\u5316\\u5b8c\\u6210\\uff01\", \"data\": {\"optimizedProfile\": {\"climbRate\": \"3\\u7c73/\\u79d2\", \"cruiseSpeed\": \"65\\u516c\\u91cc/\\u5c0f\\u65f6\", \"descentRate\": \"2\\u7c73/\\u79d2\"}, \"energySavings\": \"12%\", \"extendedRange\": \"8\\u516c\\u91cc\", \"batteryHealthImpact\": \"\\u79ef\\u6781\", \"implementationDifficulty\": \"\\u4f4e\"}}"
    },
    {
        "id": "3417f66a-dffb-449e-94f2-32634e6c0675",
        "service_id": "bf06c54b-0953-44ed-a1f1-53b56d569010",
        "name": "safetyMonitor",
        "url": "https://myApiServer.com/evtol/safety",
        "method": "POST",
        "des": "监控飞行安全状态",
        "parameter_type": 3,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u5b89\\u5168\\u72b6\\u6001\\u8bc4\\u4f30\\u5b8c\\u6210\\uff01\", \"data\": {\"overallStatus\": \"\\u6b63\\u5e38\", \"safetyScore\": 95, \"anomalies\": [{\"component\": \"\\u5de6\\u4fa7\\u87ba\\u65cb\\u6868\", \"severity\": \"\\u4f4e\", \"action\": \"\\u7ee7\\u7eed\\u76d1\\u63a7\"}], \"systemChecks\": {\"propulsion\": \"Pass\", \"navigation\": \"Pass\", \"communication\": \"Pass\", \"powertrain\": \"Pass\"}, \"redundancyStatus\": {\"primary\": \"\\u6b63\\u5e38\", \"secondary\": \"\\u51c6\\u5907\\u5c31\\u7eea\"}, \"recommendedActions\": []}}"
    },
    {
        "id": "3c7df4ef-609b-4353-af9e-ee6e8ddc752e",
        "service_id": "8189e54b-ae51-43b6-bf25-7e5391288e3c",
        "name": "eVTOL智能飞行控制元应用",
        "url": "https://myApiServer.com/evtol/metaApp",
        "method": "POST",
        "des": "",
        "parameter_type": 3,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u4efb\\u52a1\\u6267\\u884c\\u5b8c\\u6210\\uff01\", \"data\": {\"missionStatus\": \"\\u5b8c\\u6210\", \"flightPath\": [{\"lat\": 31.2304, \"lng\": 121.4737, \"alt\": 120, \"time\": \"14:30:00\"}, {\"lat\": 31.2324, \"lng\": 121.4757, \"alt\": 150, \"time\": \"14:35:00\"}, {\"lat\": 31.2354, \"lng\": 121.4787, \"alt\": 150, \"time\": \"14:40:00\"}, {\"lat\": 31.2384, \"lng\": 121.4817, \"alt\": 120, \"time\": \"14:45:00\"}], \"batteryUsed\": \"28%\", \"obstaclesAvoided\": 5, \"weatherConditions\": \"\\u826f\\u597d\", \"totalFlightTime\": \"15\\u5206\\u949f\", \"safetyIncidents\": 0, \"recommendations\": [\"\\u5b9a\\u671f\\u68c0\\u67e5\\u5de6\\u4fa7\\u87ba\\u65cb\\u6868\", \"\\u66f4\\u65b0\\u57ce\\u533a\\u9ad8\\u5c42\\u5efa\\u7b51\\u6570\\u636e\"]}}"
    },
    {
        "id": "16741c61-7457-4ba5-a8e5-1eb84ab9b8c0",
        "service_id": "64d4710f-e820-4900-b0a1-659ae8871b97",
        "name": "translateContent",
        "url": "https://myApiServer.com/ecommerce/translate",
        "method": "POST",
        "des": "将产品描述翻译成多种语言",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u7ffb\\u8bd1\\u6210\\u529f\\uff01\", \"data\": {\"translations\": {\"en\": \"Product description in English\", \"es\": \"Descripci\\u00f3n del producto en espa\\u00f1ol\", \"fr\": \"Description du produit en fran\\u00e7ais\"}}}"
    },
    {
        "id": "0c242c60-e1d2-417f-9385-f4c7c90140c7",
        "service_id": "64d4710f-e820-4900-b0a1-659ae8871b97",
        "name": "generateDescription",
        "url": "https://myApiServer.com/ecommerce/generate",
        "method": "POST",
        "des": "根据产品特性生成营销文案",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u751f\\u6210\\u6210\\u529f\\uff01\", \"data\": {\"marketingText\": \"Generated marketing content based on product features\"}}"
    },
    {
        "id": "85c17132-3534-4a85-9845-fd55dfb81989",
        "service_id": "3e846e2c-5c43-4eda-be49-b279cfd68b49",
        "name": "analyzeTrend",
        "url": "https://myApiServer.com/ecommerce/analyze",
        "method": "POST",
        "des": "分析市场趋势及竞品情况",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u5206\\u6790\\u5b8c\\u6210\\uff01\", \"data\": {\"trends\": [\"\\u5317\\u7f8e\\u533a\\u57df\\u9500\\u91cf\\u589e\\u957f15%\", \"\\u6b27\\u6d32\\u5e02\\u573a\\u7ade\\u4e89\\u52a0\\u5267\"], \"recommendations\": [\"\\u589e\\u52a0\\u5e7f\\u544a\\u6295\\u653e\", \"\\u8c03\\u6574\\u5b9a\\u4ef7\\u7b56\\u7565\"]}}"
    },
    {
        "id": "a93fe785-e984-4c95-9f09-3cc6f052834e",
        "service_id": "3e846e2c-5c43-4eda-be49-b279cfd68b49",
        "name": "predictSales",
        "url": "https://myApiServer.com/ecommerce/predict",
        "method": "POST",
        "des": "预测产品销量及趋势",
        "parameter_type": 2,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u9884\\u6d4b\\u5b8c\\u6210\\uff01\", \"data\": {\"predictedSales\": [125, 142, 156, 168, 172], \"trend\": \"\\u4e0a\\u5347\", \"confidence\": 0.85}}"
    },
    {
        "id": "7369ae9e-780f-4d19-9a21-f138dda5b9a6",
        "service_id": "f043882c-acbe-4737-99d7-5de8bbb3beae",
        "name": "跨境电商智能营销元应用",
        "url": "https://myApiServer.com/ecommerce/metaApp",
        "method": "POST",
        "des": "执行跨境电商全渠道营销活动",
        "parameter_type": 3,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"code\": 200, \"message\": \"\\u8425\\u9500\\u8ba1\\u5212\\u751f\\u6210\\u6210\\u529f\\uff01\", \"data\": {\"marketingPlan\": {\"channels\": [\"social\", \"email\", \"search\"], \"schedule\": {\"startDate\": \"2023-07-01\", \"endDate\": \"2023-07-31\"}, \"budget\": {\"total\": 5000, \"allocation\": {\"social\": 2500, \"email\": 1000, \"search\": 1500}}}}}"
    },
    {
        "id": "628f8e15-1139-42d2-9057-3baa6cb592e2",
        "service_id": "6f29852e-b8e0-44fe-b7f7-8aacb871e4d3",
        "name": "objectDetection",
        "url": "",
        "method": "GET",
        "des": "",
        "parameter_type": 0,
        "response_type": 0,
        "is_fake": 0,
        "response": "{\"name\": \"detectedObjects\", \"description\": \"\\u68c0\\u6d4b\\u5230\\u7684\\u7269\\u4f53\\u5217\\u8868\", \"type\": \"array\"}"
    },
    {
        "id": "cb618d37-f215-44b8-a7b7-8346147b901b",
        "service_id": "6f29852e-b8e0-44fe-b7f7-8aacb871e4d3",
        "name": "spatialMapping",
        "url": "",
        "method": "GET",
        "des": "",
        "parameter_type": 0,
        "response_type": 0,
        "is_fake": 0,
        "response": "{\"name\": \"spatialMap\", \"description\": \"3D\\u7a7a\\u95f4\\u5730\\u56fe\", \"type\": \"object\"}"
    },
    {
        "id": "e5fcbf58-80bb-4b52-a606-5a80296e0c8e",
        "service_id": "078d857f-5f86-48d7-aafb-7f07f74de318",
        "name": "naturalLanguageUnderstanding",
        "url": "",
        "method": "GET",
        "des": "",
        "parameter_type": 0,
        "response_type": 0,
        "is_fake": 0,
        "response": "{\"name\": \"understanding\", \"description\": \"\\u7406\\u89e3\\u7ed3\\u679c\", \"type\": \"object\"}"
    },
    {
        "id": "225ea76e-44a5-486c-94cc-58e15e5b4606",
        "service_id": "078d857f-5f86-48d7-aafb-7f07f74de318",
        "name": "emotionRecognition",
        "url": "",
        "method": "GET",
        "des": "",
        "parameter_type": 0,
        "response_type": 0,
        "is_fake": 0,
        "response": "{\"name\": \"emotionState\", \"description\": \"\\u60c5\\u7eea\\u72b6\\u6001\\u5206\\u6790\", \"type\": \"object\"}"
    },
    {
        "id": "e4562ca9-bb85-424f-8c30-68c16b2a3e94",
        "service_id": "300ece69-b80f-4c78-8865-fbda3760aee8",
        "name": "vitalSignsMonitor",
        "url": "",
        "method": "GET",
        "des": "",
        "parameter_type": 0,
        "response_type": 0,
        "is_fake": 0,
        "response": "{\"name\": \"vitalSigns\", \"description\": \"\\u751f\\u547d\\u4f53\\u5f81\\u5206\\u6790\\u7ed3\\u679c\", \"type\": \"object\"}"
    },
    {
        "id": "9e0d6410-4fb5-408f-9eb8-1b5473809b42",
        "service_id": "300ece69-b80f-4c78-8865-fbda3760aee8",
        "name": "abnormalBehaviorDetection",
        "url": "",
        "method": "GET",
        "des": "",
        "parameter_type": 0,
        "response_type": 0,
        "is_fake": 0,
        "response": "{\"name\": \"anomalyReport\", \"description\": \"\\u5f02\\u5e38\\u884c\\u4e3a\\u62a5\\u544a\", \"type\": \"object\"}"
    },
    {
        "id": "7295b267-8a30-4675-a73e-652ecd94f786",
        "service_id": "257154b3-77b8-4ce6-a3c9-c560a60ce10d",
        "name": "taskPlanner",
        "url": "",
        "method": "GET",
        "des": "",
        "parameter_type": 0,
        "response_type": 0,
        "is_fake": 0,
        "response": "{\"name\": \"taskPlan\", \"description\": \"\\u4efb\\u52a1\\u6267\\u884c\\u8ba1\\u5212\", \"type\": \"object\"}"
    },
    {
        "id": "87c2c1d3-4339-47b1-bcf8-7a74ecfbcec6",
        "service_id": "257154b3-77b8-4ce6-a3c9-c560a60ce10d",
        "name": "pathPlanning",
        "url": "",
        "method": "GET",
        "des": "",
        "parameter_type": 0,
        "response_type": 0,
        "is_fake": 0,
        "response": "{\"name\": \"path\", \"description\": \"\\u89c4\\u5212\\u8def\\u5f84\", \"type\": \"array\"}"
    },
    {
        "id": "20474c78-8753-4508-bc99-d7f56a11b1c6",
        "service_id": "0ef523dd-ee18-40bb-a588-d8097f197806",
        "name": "家庭智能助手元应用",
        "url": "https://myApiServer.com/evtol/metaApp",
        "method": "POST",
        "des": "",
        "parameter_type": 3,
        "response_type": 1,
        "is_fake": 1,
        "response": "{\"name\": \"assistantResponse\", \"description\": \"\\u52a9\\u624b\\u6267\\u884c\\u7ed3\\u679c\", \"type\": \"object\"}"
    },
]

# MOCK_SERVICE_API_PARAMETERS 数据
MOCK_SERVICE_API_PARAMETERS = [
    {
        "id": "680a53ba-a9c8-44b3-89e6-1154a938b600",
        "api_id": "e04e0165-3b18-4d54-ae38-659d04f8aef5",
        "name": "file",
        "type": "zip file",
        "des": "数据集和参数配置文件的zip压缩包"
    },
    {
        "id": "0a8da2a9-241d-44a8-a7b2-3c28f4098f39",
        "api_id": "e04e0165-3b18-4d54-ae38-659d04f8aef5",
        "name": "file",
        "type": "zip file",
        "des": "数据集和参数配置文件的zip压缩包"
    },
    {
        "id": "971949cc-0b89-4ebc-8ca3-e724c829a6bd",
        "api_id": "2df635e5-4281-4cbf-832f-006175c6a1ad",
        "name": "reportId",
        "type": "int",
        "des": ""
    },
    {
        "id": "e0d2788d-88df-43ef-b08a-1e0699ed9eed",
        "api_id": "590017b7-fa60-4d07-a7e9-d668b32e033b",
        "name": "reportId",
        "type": "int",
        "des": ""
    },
    {
        "id": "154f634a-5250-4131-9dbc-988958445012",
        "api_id": "eebfb433-46e7-477a-9abb-057ef90daacd",
        "name": "reportData",
        "type": "string",
        "des": "用于生成报告的数据"
    },
    {
        "id": "4f938071-15ba-469e-81a6-d5a427ea2f56",
        "api_id": "c8f9b07b-b7bb-47e9-ade9-17937dda65c3",
        "name": "query",
        "type": "string",
        "des": "用自然语言描述想要生成的报告"
    },
    {
        "id": "c27182e7-c9a4-4628-9bb5-ea42f2f4259d",
        "api_id": "78a9058c-affa-4af2-9ec5-af12e5eef50d",
        "name": "query",
        "type": "string",
        "des": "用自然语言描述查询需求"
    },
    {
        "id": "6782b166-8da1-47fb-bcf1-71fd5bfd3f7b",
        "api_id": "e59e68c3-3d03-4e36-b6ce-71673b261005",
        "name": "file",
        "type": "file",
        "des": "数据集和配置文件的zip压缩包"
    },
    {
        "id": "b8fcc8ba-555c-4ff0-90e8-6036f31dfa28",
        "api_id": "e59e68c3-3d03-4e36-b6ce-71673b261005",
        "name": "model_name",
        "type": "string",
        "des": "模型名称，目前只支持HattenGCN"
    },
    {
        "id": "f623dd1a-c3e1-47d7-860b-84183d4596f6",
        "api_id": "c35b0b2c-2b11-4279-914e-e6e751f8e00a",
        "name": "sex",
        "type": "int",
        "des": "性别，0表示女性，1表示男性"
    },
    {
        "id": "348385c3-8697-4d92-95db-bead1d56e261",
        "api_id": "c35b0b2c-2b11-4279-914e-e6e751f8e00a",
        "name": "age",
        "type": "int",
        "des": "年龄，必须为整数"
    },
    {
        "id": "8e29d9f3-8e2c-4fd8-a6d3-36dd20613ba3",
        "api_id": "c35b0b2c-2b11-4279-914e-e6e751f8e00a",
        "name": "height",
        "type": "int",
        "des": "身高，单位cm，必须为整数"
    },
    {
        "id": "edb0bbb5-ef30-47f4-bcec-94a0a2bfe7e5",
        "api_id": "c35b0b2c-2b11-4279-914e-e6e751f8e00a",
        "name": "weight",
        "type": "int",
        "des": "体重，单位kg，必须为整数"
    },
    {
        "id": "3d3073e5-982a-4327-badd-3382c2c6b05e",
        "api_id": "c35b0b2c-2b11-4279-914e-e6e751f8e00a",
        "name": "scr",
        "type": "float",
        "des": "血清肌酐，单位umol/L，必须为浮点数"
    },
    {
        "id": "5c9f3f06-1adc-45d2-824e-35e046798c78",
        "api_id": "c35b0b2c-2b11-4279-914e-e6e751f8e00a",
        "name": "tb",
        "type": "float",
        "des": "总胆红素，单位umol/L，必须为浮点数"
    },
    {
        "id": "63265eac-a2b4-4943-a8a0-14459cdc1dce",
        "api_id": "c35b0b2c-2b11-4279-914e-e6e751f8e00a",
        "name": "auc_range",
        "type": "array",
        "des": "目标24小时药时曲线AUC范围，单位umol/L，必须为数组，数组长度为2，第一个元素为下限，第二个元素为上限"
    },
    {
        "id": "bbe7cd35-88e4-4f72-8885-0b7f05552bc4",
        "api_id": "37dc651e-1559-44b9-8fbf-a23e96b41b23",
        "name": "file",
        "type": "image file",
        "des": "医学影像文件（支持CT、X光、超声等图像）"
    },
    {
        "id": "d9447e8c-6339-4eb3-b004-9f73b2478453",
        "api_id": "c3b1cfa6-9c0a-49d4-86ed-99c9ce5319bd",
        "name": "data",
        "type": "json",
        "des": "来自可穿戴设备和家用医疗设备的健康数据"
    },
    {
        "id": "78d40a80-1b83-48d9-8ddd-05d13c7969eb",
        "api_id": "eb71aac4-245e-42ef-9f45-a15febac7054",
        "name": "audio",
        "type": "audio file",
        "des": "语音文件（支持方言）"
    },
    {
        "id": "e7595f9c-96ca-492c-8cca-d7f8776ec930",
        "api_id": "11850741-9979-4a5b-ae18-75dd8b2199e6",
        "name": "data",
        "type": "json",
        "des": "急诊信息和可用资源数据"
    },
    {
        "id": "af8c4fe5-0074-4fa0-8812-8777a38fbeae",
        "api_id": "e04e0165-3b18-4d54-ae38-659d04f8aef5",
        "name": "data",
        "type": "json",
        "des": "历史疫情数据和环境因素"
    },
    {
        "id": "9dd6be31-06bb-45cf-9804-c62cf390b079",
        "api_id": "4b71974a-2d65-412a-b25d-13c0924d1abb",
        "name": "image",
        "type": "file",
        "des": "农作物图像文件"
    },
    {
        "id": "1c4f2915-b870-4dcd-9162-42ac03220f26",
        "api_id": "4b71974a-2d65-412a-b25d-13c0924d1abb",
        "name": "cropType",
        "type": "string",
        "des": "作物类型，如不提供则自动识别"
    },
    {
        "id": "1dd0b287-351e-4798-838f-211b132f0fc3",
        "api_id": "3d939529-0043-4b2f-a906-2dc5714dc84d",
        "name": "image",
        "type": "file",
        "des": "病害部位图像"
    },
    {
        "id": "3aed8b48-bc8b-46e2-be57-c39b3773a420",
        "api_id": "3d939529-0043-4b2f-a906-2dc5714dc84d",
        "name": "cropType",
        "type": "string",
        "des": "作物类型"
    },
    {
        "id": "56383009-1f6b-45b4-a281-0a2a6ada07fc",
        "api_id": "0f5179d4-3bc7-4c0e-9bac-cb2a97c5386e",
        "name": "soilMoisture",
        "type": "number",
        "des": "土壤湿度百分比"
    },
    {
        "id": "06972077-e129-49af-820c-87f4448984c4",
        "api_id": "0f5179d4-3bc7-4c0e-9bac-cb2a97c5386e",
        "name": "cropType",
        "type": "string",
        "des": "作物类型"
    },
    {
        "id": "e76e3298-022a-4c12-9fe5-5b9dc38308dd",
        "api_id": "0f5179d4-3bc7-4c0e-9bac-cb2a97c5386e",
        "name": "growthStage",
        "type": "string",
        "des": "生长阶段"
    },
    {
        "id": "d119533d-f79c-4e12-8f87-88970831151c",
        "api_id": "0f5179d4-3bc7-4c0e-9bac-cb2a97c5386e",
        "name": "fieldSize",
        "type": "number",
        "des": "田地面积(亩)"
    },
    {
        "id": "a6499c2e-e952-4d5d-8c69-de8381cba9cf",
        "api_id": "fa339134-1472-4421-bed3-2e516ef14156",
        "name": "cropType",
        "type": "string",
        "des": "作物类型"
    },
    {
        "id": "51e9fe3c-0de8-400e-8ee1-40c2e80d3ed6",
        "api_id": "fa339134-1472-4421-bed3-2e516ef14156",
        "name": "plantingDate",
        "type": "string",
        "des": "播种日期(YYYY-MM-DD)"
    },
    {
        "id": "a5482b94-a2b3-4134-bf62-4bf0cbf79ffe",
        "api_id": "fa339134-1472-4421-bed3-2e516ef14156",
        "name": "fieldSize",
        "type": "number",
        "des": "田地面积(亩)"
    },
    {
        "id": "a8b1a5b5-a57f-4d1d-a12e-1136c38181ee",
        "api_id": "fa339134-1472-4421-bed3-2e516ef14156",
        "name": "historicalData",
        "type": "file",
        "des": "历史产量数据(CSV)"
    },
    {
        "id": "e713a017-9787-4e0f-9a09-54e8c40c5a22",
        "api_id": "f7b3a3a6-ae2a-4e0a-9764-6ab98605d592",
        "name": "data",
        "type": "json",
        "des": "包含起点终点和环境数据的JSON"
    },
    {
        "id": "d58cfb50-fdc4-497b-90b0-6162a5daa855",
        "api_id": "bcb8d724-5b02-4729-b61f-d36e4802eaa1",
        "name": "sensorData",
        "type": "multimodal",
        "des": "来自多种传感器的数据"
    },
    {
        "id": "f57b508e-8ab4-4f4f-ad27-3e0c1635a276",
        "api_id": "2f6e70a5-ff4a-4bae-be66-b7adf0d4d47c",
        "name": "controlCommand",
        "type": "json",
        "des": "飞行控制命令"
    },
    {
        "id": "398064e6-1628-47a2-8672-97c933a21c72",
        "api_id": "36ef2f7e-3dab-479c-a6fb-a04dcc04e54c",
        "name": "flightData",
        "type": "json",
        "des": "飞行数据和电池状态"
    },
    {
        "id": "da1c7014-2601-4a5f-ab27-2715f81480c4",
        "api_id": "3417f66a-dffb-449e-94f2-32634e6c0675",
        "name": "systemStatus",
        "type": "json",
        "des": "系统状态数据"
    },
    {
        "id": "4c0c1862-cba1-40fd-b0be-1ef3e85f59fa",
        "api_id": "16741c61-7457-4ba5-a8e5-1eb84ab9b8c0",
        "name": "productData",
        "type": "object",
        "des": "产品详细信息"
    },
    {
        "id": "5c79f149-7339-4c33-8669-c3cba1209731",
        "api_id": "16741c61-7457-4ba5-a8e5-1eb84ab9b8c0",
        "name": "targetLanguages",
        "type": "array",
        "des": "目标语言列表"
    },
    {
        "id": "4878ee3d-d588-46cf-b4a5-cf2c09671d5f",
        "api_id": "0c242c60-e1d2-417f-9385-f4c7c90140c7",
        "name": "productFeatures",
        "type": "array",
        "des": "产品特性列表"
    },
    {
        "id": "99db845a-8c63-4961-ad55-242a6dcb2da2",
        "api_id": "0c242c60-e1d2-417f-9385-f4c7c90140c7",
        "name": "targetMarket",
        "type": "string",
        "des": "目标市场"
    },
    {
        "id": "20d24775-c31a-4fc7-b770-5946cc9d5cc1",
        "api_id": "0c242c60-e1d2-417f-9385-f4c7c90140c7",
        "name": "tone",
        "type": "string",
        "des": "文案风格"
    },
    {
        "id": "39b21694-6e62-44e6-abe0-11395acb4fca",
        "api_id": "85c17132-3534-4a85-9845-fd55dfb81989",
        "name": "productCategory",
        "type": "string",
        "des": "产品类别"
    },
    {
        "id": "c67fd499-c3bb-4f95-b574-53c12c419273",
        "api_id": "85c17132-3534-4a85-9845-fd55dfb81989",
        "name": "targetMarkets",
        "type": "array",
        "des": "目标市场列表"
    },
    {
        "id": "45322124-aeec-422b-966c-380465838e9c",
        "api_id": "85c17132-3534-4a85-9845-fd55dfb81989",
        "name": "timeRange",
        "type": "object",
        "des": "分析时间范围"
    },
    {
        "id": "b7416a7d-d422-4646-8d7d-56a02babfb66",
        "api_id": "a93fe785-e984-4c95-9f09-3cc6f052834e",
        "name": "productId",
        "type": "string",
        "des": "产品ID"
    },
    {
        "id": "6eca97a0-4fec-438b-b68f-6ace3e87ceb2",
        "api_id": "a93fe785-e984-4c95-9f09-3cc6f052834e",
        "name": "historicalData",
        "type": "array",
        "des": "历史销售数据"
    },
    {
        "id": "7c42b58b-b317-4653-aead-de0d3b827429",
        "api_id": "a93fe785-e984-4c95-9f09-3cc6f052834e",
        "name": "predictionPeriod",
        "type": "number",
        "des": "预测周期（天）"
    },
    {
        "id": "32f217d2-710c-4289-9867-0c9efc6229ac",
        "api_id": "7369ae9e-780f-4d19-9a21-f138dda5b9a6",
        "name": "campaignDetails",
        "type": "object",
        "des": "营销活动详情"
    },
    {
        "id": "0039ce0e-d822-47d4-a5a1-f4b393c88ca5",
        "api_id": "7369ae9e-780f-4d19-9a21-f138dda5b9a6",
        "name": "productData",
        "type": "object",
        "des": "产品数据"
    },
    {
        "id": "639c09e5-f359-43c8-b2ca-20e75602121b",
        "api_id": "7369ae9e-780f-4d19-9a21-f138dda5b9a6",
        "name": "targetMarkets",
        "type": "array",
        "des": "目标市场列表"
    },
    {
        "id": "c36c1494-572b-4cc7-b8da-6963de4a5138",
        "api_id": "7369ae9e-780f-4d19-9a21-f138dda5b9a6",
        "name": "budget",
        "type": "object",
        "des": "预算配置"
    },
    {
        "id": "65c2c888-d7f4-40b2-bf36-dd5cb674f6b4",
        "api_id": "628f8e15-1139-42d2-9057-3baa6cb592e2",
        "name": "imageData",
        "type": "object",
        "des": ""
    },
    {
        "id": "1c6b1243-ec12-4505-9937-43114652aa7e",
        "api_id": "628f8e15-1139-42d2-9057-3baa6cb592e2",
        "name": "detectionThreshold",
        "type": "number",
        "des": ""
    },
    {
        "id": "93ba50f0-161e-428e-970b-8c0995f343c9",
        "api_id": "cb618d37-f215-44b8-a7b7-8346147b901b",
        "name": "depthData",
        "type": "array",
        "des": ""
    },
    {
        "id": "f9007980-f3f1-49b8-80d0-0a958a31bb86",
        "api_id": "cb618d37-f215-44b8-a7b7-8346147b901b",
        "name": "resolution",
        "type": "number",
        "des": ""
    },
    {
        "id": "3a0b6f80-8645-4a92-bd9f-93f894971c68",
        "api_id": "e5fcbf58-80bb-4b52-a606-5a80296e0c8e",
        "name": "text",
        "type": "string",
        "des": ""
    },
    {
        "id": "ab1e4343-c205-4ad2-8fbf-dddf2bfc5882",
        "api_id": "e5fcbf58-80bb-4b52-a606-5a80296e0c8e",
        "name": "context",
        "type": "object",
        "des": ""
    },
    {
        "id": "421ac775-f4d2-4075-8c8d-c21aa7e16f50",
        "api_id": "225ea76e-44a5-486c-94cc-58e15e5b4606",
        "name": "audioData",
        "type": "binary",
        "des": ""
    },
    {
        "id": "49f95d97-a648-4372-9da5-7d160829070c",
        "api_id": "225ea76e-44a5-486c-94cc-58e15e5b4606",
        "name": "facialImage",
        "type": "binary",
        "des": ""
    },
    {
        "id": "1a0b3944-3055-48ac-8ef5-9d060cd22784",
        "api_id": "e4562ca9-bb85-424f-8c30-68c16b2a3e94",
        "name": "sensorData",
        "type": "object",
        "des": ""
    },
    {
        "id": "d8b06934-c12d-43a8-9e14-852d50c15f7e",
        "api_id": "e4562ca9-bb85-424f-8c30-68c16b2a3e94",
        "name": "userProfile",
        "type": "object",
        "des": ""
    },
    {
        "id": "053ed462-25da-46cf-a085-78cf9f8a922c",
        "api_id": "9e0d6410-4fb5-408f-9eb8-1b5473809b42",
        "name": "behaviorData",
        "type": "array",
        "des": ""
    },
    {
        "id": "92be94dc-3bf9-4bdd-9328-9c29ead2f958",
        "api_id": "9e0d6410-4fb5-408f-9eb8-1b5473809b42",
        "name": "baseline",
        "type": "object",
        "des": ""
    },
    {
        "id": "849e1dda-a4e2-4c18-b924-ce8449c1f2af",
        "api_id": "7295b267-8a30-4675-a73e-652ecd94f786",
        "name": "taskList",
        "type": "array",
        "des": ""
    },
    {
        "id": "c7c5cba3-6899-45f1-b8e3-d34bcb9114c9",
        "api_id": "7295b267-8a30-4675-a73e-652ecd94f786",
        "name": "environmentState",
        "type": "object",
        "des": ""
    },
    {
        "id": "4f9c225f-aa2d-41d1-a052-5563e04072c2",
        "api_id": "7295b267-8a30-4675-a73e-652ecd94f786",
        "name": "preferences",
        "type": "object",
        "des": ""
    },
    {
        "id": "99109f68-a6e8-40fc-a0e7-65651180e263",
        "api_id": "87c2c1d3-4339-47b1-bcf8-7a74ecfbcec6",
        "name": "spatialMap",
        "type": "object",
        "des": ""
    },
    {
        "id": "ac95c4d2-55ce-41e0-8e45-645cca1a8844",
        "api_id": "87c2c1d3-4339-47b1-bcf8-7a74ecfbcec6",
        "name": "startPosition",
        "type": "object",
        "des": ""
    },
    {
        "id": "c1097076-263f-454e-9cd7-8f67c2b9797b",
        "api_id": "87c2c1d3-4339-47b1-bcf8-7a74ecfbcec6",
        "name": "targetPosition",
        "type": "object",
        "des": ""
    },
    {
        "id": "1f365bb6-e4ea-4c13-8f07-0d38a6095fe4",
        "api_id": "20474c78-8753-4508-bc99-d7f56a11b1c6",
        "name": "command",
        "type": "string",
        "des": ""
    },
    {
        "id": "42032d53-6add-4469-9933-17a375c35fbe",
        "api_id": "20474c78-8753-4508-bc99-d7f56a11b1c6",
        "name": "environmentData",
        "type": "object",
        "des": ""
    },
    {
        "id": "cf2b9688-1f11-472b-a2cb-c832046643f9",
        "api_id": "20474c78-8753-4508-bc99-d7f56a11b1c6",
        "name": "userContext",
        "type": "object",
        "des": ""
    },
    {
        "id": "db0e2c8a-9769-4ac2-90b6-db5b0923bf74",
        "api_id": "20474c78-8753-4508-bc99-d7f56a11b1c6",
        "name": "executionMode",
        "type": "string",
        "des": ""
    },
]
