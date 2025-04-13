#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import uuid
import re
import datetime

# 领域类型常量
DOMAINS = {
    'aml': 'AML',
    'aircraft': '无人机',
    'health': '医疗健康',
    'agriculture': '农业数智',
    'evtol': 'eVTOL',
    'ecommerce': '跨境电商',
    'homeAI': '家庭机器人'
}

# API_IDS 存储，用于后续生成相同ID
API_IDS = {}

def generate_uuid():
    """生成UUID"""
    return str(uuid.uuid4())

def read_js_variable(js_file, variable_name):
    """从JS文件中提取变量内容"""
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式找到变量定义
    pattern = "const {} = (\\[.*?\\])".format(variable_name)
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("在文件中未找到 {} 变量".format(variable_name))
        return []
    
    js_array = match.group(1)
    
    # 手动将JS数组转换为Python字典列表
    try:
        # 尝试直接用json处理简单情况
        js_array = js_array.replace("'", '"')
        js_array = re.sub(r'([{,])\s*(\w+):', r'\1"\2":', js_array)
        js_array = re.sub(r',\s*([}\]])', r'\1', js_array)
        
        return json.loads(js_array)
    except json.JSONDecodeError as e:
        print("解析 {} 时出错: {}".format(variable_name, e))
        print("尝试手动解析模式...")
        
        # 这里可以添加更复杂的手动解析逻辑
        # 简化处理：假设空数组
        return []

def transform_service(service, domain):
    """将JS格式的服务数据转换为Python格式"""
    # 生成服务ID
    service_id = generate_uuid()
    
    # 创建时间戳（毫秒级）
    create_time = int(datetime.datetime.now().timestamp() * 1000)
    
    # 转换服务数据
    transformed = {
        "id": service_id,
        "name": service.get("name", ""),
        "attribute": service.get("attribute", 0),
        "type": service.get("type", 0),
        "domain": service.get("domain", 0),
        "industry": service.get("industry", 0),
        "scenario": service.get("scenario", 0),
        "technology": service.get("technology", 0),
        "network": service.get("netWork", "bridge"),
        "port": service.get("port", ""),
        "volume": service.get("volume", ""),
        "status": service.get("status", 0),
        "number": service.get("number", "0"),
        "deleted": 0,
        "create_time": create_time,
        "creator_id": "",
    }
    
    return service_id, transformed

def transform_norm(norm, service_id):
    """将JS格式的规范数据转换为Python格式"""
    return {
        "id": generate_uuid(),
        "service_id": service_id,
        "key": norm.get("key", 0),
        "score": norm.get("score", 5),
    }

def transform_source(source, service_id):
    """将JS格式的来源数据转换为Python格式"""
    return {
        "id": generate_uuid(),
        "service_id": service_id,
        "popover_title": source.get("popoverTitle", ""),
        "company_name": source.get("companyName", ""),
        "company_address": source.get("companyAddress", ""),
        "company_contact": source.get("companyContact", ""),
        "company_introduce": source.get("companyIntroduce", ""),
        "ms_introduce": source.get("msIntroduce", ""),
        "company_score": source.get("companyScore", 5),
        "ms_score": source.get("msScore", 5),
    }

def transform_api(api, service_id):
    """将JS格式的API数据转换为Python格式"""
    api_name = api.get("name", "")
    
    # 对于已存在的API名称，使用相同的ID
    if api_name in API_IDS:
        api_id = API_IDS[api_name]
    else:
        api_id = generate_uuid()
        API_IDS[api_name] = api_id
    
    # 获取API响应
    response = None
    if "response" in api and api.get("response") is not None:
        try:
            if isinstance(api.get("response"), dict):
                response = json.dumps(api.get("response"))
            else:
                response = api.get("response")
        except:
            response = str(api.get("response"))
    
    transformed = {
        "id": api_id,
        "service_id": service_id,
        "name": api_name,
        "url": api.get("url", ""),
        "method": api.get("method", "GET"),
        "des": api.get("des", ""),
        "parameter_type": api.get("parameterType", 0),
        "response_type": api.get("responseType", 0),
        "is_fake": 1 if api.get("isFake", False) else 0,
        "response": response,
    }
    
    return api_id, transformed

def transform_parameter(param, api_id):
    """将JS格式的参数数据转换为Python格式"""
    return {
        "id": generate_uuid(),
        "api_id": api_id,
        "name": param.get("name", ""),
        "type": param.get("type", ""),
        "des": param.get("des", ""),
    }

def generate_api_ids_dict():
    """生成API_IDS字典用于写入service.py"""
    api_ids_dict = "API_IDS = {\n"
    for name, id in API_IDS.items():
        api_ids_dict += '    "{0}": "{1}",\n'.format(name, id)
    api_ids_dict += "}\n"
    return api_ids_dict

def extract_js_array(js_file, variable_name):
    """手动提取JS文件中的变量数组"""
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到变量的起始位置
    start_pattern = "const {0} = [".format(variable_name)
    start_pos = content.find(start_pattern)
    
    if start_pos == -1:
        print("在文件中未找到 {0} 变量".format(variable_name))
        return []
    
    # 寻找数组结束位置
    start_pos += len(start_pattern) - 1  # 减1是为了包含 [
    bracket_count = 1
    end_pos = start_pos + 1
    
    while bracket_count > 0 and end_pos < len(content):
        if content[end_pos] == '[':
            bracket_count += 1
        elif content[end_pos] == ']':
            bracket_count -= 1
        end_pos += 1
    
    if bracket_count != 0:
        print("无法找到 {0} 变量的结束位置".format(variable_name))
        return []
    
    # 提取JS数组字符串
    js_array = content[start_pos:end_pos]
    
    # 转换为Python可解析的JSON格式
    try:
        # 将单引号替换为双引号
        js_array = js_array.replace("'", '"')
        
        # 处理JS对象属性名（没有引号的属性名）
        js_array = re.sub(r'([{,])\s*(\w+):', r'\1"\2":', js_array)
        
        # 移除尾随逗号
        js_array = re.sub(r',\s*([}\]])', r'\1', js_array)
        
        return json.loads(js_array)
    except json.JSONDecodeError as e:
        print("解析 {0} 时出错: {1}".format(variable_name, e))
        return []

def process_domain_services(js_file, service_var, meta_app_var):
    """处理特定领域的服务和元应用数据"""
    services = extract_js_array(js_file, service_var)
    meta_apps = extract_js_array(js_file, meta_app_var)
    
    all_services = []
    all_norms = []
    all_sources = []
    all_apis = []
    all_parameters = []
    
    # 处理微服务
    for service in services:
        service_id, transformed_service = transform_service(service, service_var)
        all_services.append(transformed_service)
        
        # 处理规范
        if "norm" in service:
            for norm in service["norm"]:
                all_norms.append(transform_norm(norm, service_id))
        
        # 处理来源
        if "source" in service:
            all_sources.append(transform_source(service["source"], service_id))
        
        # 处理API
        if "apiList" in service:
            for api in service["apiList"]:
                api_id, transformed_api = transform_api(api, service_id)
                all_apis.append(transformed_api)
                
                # 处理参数
                if "parameters" in api:
                    for param in api["parameters"]:
                        all_parameters.append(transform_parameter(param, api_id))
    
    # 处理元应用
    for app in meta_apps:
        app_id, transformed_app = transform_service(app, meta_app_var)
        all_services.append(transformed_app)
        
        # 处理规范
        if "norm" in app:
            for norm in app["norm"]:
                all_norms.append(transform_norm(norm, app_id))
        
        # 处理来源
        if "source" in app:
            all_sources.append(transform_source(app["source"], app_id))
        
        # 处理API
        if "apiList" in app:
            for api in app["apiList"]:
                api_id, transformed_api = transform_api(api, app_id)
                all_apis.append(transformed_api)
                
                # 处理参数
                if "parameters" in api:
                    for param in api["parameters"]:
                        all_parameters.append(transform_parameter(param, api_id))
    
    return all_services, all_norms, all_sources, all_apis, all_parameters

def write_service_py(services, norms, sources, apis, parameters, output_file):
    """将所有数据写入service.py文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        # 写入API_IDS字典
        f.write(generate_api_ids_dict())
        f.write("\n")
        
        # 写入服务数据
        f.write("# MOCK_SERVICES 数据\n")
        f.write("MOCK_SERVICES = [\n")
        for service in services:
            json_str = json.dumps(service, ensure_ascii=False, indent=4).replace('\\n', '\\n    ')
            f.write("    {0},\n".format(json_str))
        f.write("]\n\n")
        
        # 写入规范数据
        f.write("# MOCK_SERVICE_NORMS 数据\n")
        f.write("MOCK_SERVICE_NORMS = [\n")
        for norm in norms:
            json_str = json.dumps(norm, ensure_ascii=False, indent=4).replace('\\n', '\\n    ')
            f.write("    {0},\n".format(json_str))
        f.write("]\n\n")
        
        # 写入来源数据
        f.write("# MOCK_SERVICE_SOURCES 数据\n")
        f.write("MOCK_SERVICE_SOURCES = [\n")
        for source in sources:
            json_str = json.dumps(source, ensure_ascii=False, indent=4).replace('\\n', '\\n    ')
            f.write("    {0},\n".format(json_str))
        f.write("]\n\n")
        
        # 写入API数据
        f.write("# MOCK_SERVICE_APIS 数据\n")
        f.write("MOCK_SERVICE_APIS = [\n")
        for api in apis:
            json_str = json.dumps(api, ensure_ascii=False, indent=4).replace('\\n', '\\n    ')
            f.write("    {0},\n".format(json_str))
        f.write("]\n\n")
        
        # 写入参数数据
        f.write("# MOCK_SERVICE_API_PARAMETERS 数据\n")
        f.write("MOCK_SERVICE_API_PARAMETERS = [\n")
        for param in parameters:
            json_str = json.dumps(param, ensure_ascii=False, indent=4).replace('\\n', '\\n    ')
            f.write("    {0},\n".format(json_str))
        f.write("]\n")

def main():
    print("开始执行数据生成脚本...")
    js_file = "mocks/services_data.js"
    output_file = "mocks/service_generated.py"  # 修改为新的输出文件名，避免覆盖原始文件
    
    print("读取数据源: {0}".format(js_file))
    print("输出文件: {0}".format(output_file))
    
    all_services = []
    all_norms = []
    all_sources = []
    all_apis = []
    all_parameters = []
    
    # 处理AML领域
    print("正在处理 AML 领域...")
    try:
        aml_services, aml_norms, aml_sources, aml_apis, aml_parameters = process_domain_services(
            js_file, "amlServices", "amlMetaApps"
        )
        all_services.extend(aml_services)
        all_norms.extend(aml_norms)
        all_sources.extend(aml_sources)
        all_apis.extend(aml_apis)
        all_parameters.extend(aml_parameters)
        print("  AML 领域处理完成: {0}个服务, {1}个规范, {2}个来源, {3}个API, {4}个参数".format(
            len(aml_services), len(aml_norms), len(aml_sources), len(aml_apis), len(aml_parameters)
        ))
    except Exception as e:
        print("处理AML领域时出错: {}".format(e))
    
    # 处理无人机领域
    print("正在处理 无人机 领域...")
    try:
        aircraft_services, aircraft_norms, aircraft_sources, aircraft_apis, aircraft_parameters = process_domain_services(
            js_file, "airCraftServices", "airCraftMetaApps"
        )
        all_services.extend(aircraft_services)
        all_norms.extend(aircraft_norms)
        all_sources.extend(aircraft_sources)
        all_apis.extend(aircraft_apis)
        all_parameters.extend(aircraft_parameters)
        print("  无人机领域处理完成: {0}个服务, {1}个规范, {2}个来源, {3}个API, {4}个参数".format(
            len(aircraft_services), len(aircraft_norms), len(aircraft_sources), len(aircraft_apis), len(aircraft_parameters)
        ))
    except Exception as e:
        print("处理无人机领域时出错: {}".format(e))
    
    # 处理医疗健康领域
    print("正在处理 医疗健康 领域...")
    try:
        health_services, health_norms, health_sources, health_apis, health_parameters = process_domain_services(
            js_file, "healthServices", "healthMetaApps"
        )
        all_services.extend(health_services)
        all_norms.extend(health_norms)
        all_sources.extend(health_sources)
        all_apis.extend(health_apis)
        all_parameters.extend(health_parameters)
        print("  医疗健康领域处理完成: {0}个服务, {1}个规范, {2}个来源, {3}个API, {4}个参数".format(
            len(health_services), len(health_norms), len(health_sources), len(health_apis), len(health_parameters)
        ))
    except Exception as e:
        print("处理医疗健康领域时出错: {}".format(e))
    
    # 处理农业数智领域
    print("正在处理 农业数智 领域...")
    try:
        agriculture_services, agriculture_norms, agriculture_sources, agriculture_apis, agriculture_parameters = process_domain_services(
            js_file, "agricultureServices", "agricultureMetaApps"
        )
        all_services.extend(agriculture_services)
        all_norms.extend(agriculture_norms)
        all_sources.extend(agriculture_sources)
        all_apis.extend(agriculture_apis)
        all_parameters.extend(agriculture_parameters)
        print("  农业数智领域处理完成: {0}个服务, {1}个规范, {2}个来源, {3}个API, {4}个参数".format(
            len(agriculture_services), len(agriculture_norms), len(agriculture_sources), len(agriculture_apis), len(agriculture_parameters)
        ))
    except Exception as e:
        print("处理农业数智领域时出错: {}".format(e))
    
    # 处理eVTOL领域
    print("正在处理 eVTOL 领域...")
    try:
        evtol_services, evtol_norms, evtol_sources, evtol_apis, evtol_parameters = process_domain_services(
            js_file, "evtolServices", "evtolMetaApps"
        )
        all_services.extend(evtol_services)
        all_norms.extend(evtol_norms)
        all_sources.extend(evtol_sources)
        all_apis.extend(evtol_apis)
        all_parameters.extend(evtol_parameters)
        print("  eVTOL领域处理完成: {0}个服务, {1}个规范, {2}个来源, {3}个API, {4}个参数".format(
            len(evtol_services), len(evtol_norms), len(evtol_sources), len(evtol_apis), len(evtol_parameters)
        ))
    except Exception as e:
        print("处理eVTOL领域时出错: {}".format(e))
    
    # 处理跨境电商领域
    print("正在处理 跨境电商 领域...")
    try:
        ecommerce_services, ecommerce_norms, ecommerce_sources, ecommerce_apis, ecommerce_parameters = process_domain_services(
            js_file, "ecommerceServices", "ecommerceMetaApps"
        )
        all_services.extend(ecommerce_services)
        all_norms.extend(ecommerce_norms)
        all_sources.extend(ecommerce_sources)
        all_apis.extend(ecommerce_apis)
        all_parameters.extend(ecommerce_parameters)
        print("  跨境电商领域处理完成: {0}个服务, {1}个规范, {2}个来源, {3}个API, {4}个参数".format(
            len(ecommerce_services), len(ecommerce_norms), len(ecommerce_sources), len(ecommerce_apis), len(ecommerce_parameters)
        ))
    except Exception as e:
        print("处理跨境电商领域时出错: {}".format(e))
        import traceback
        traceback.print_exc()
    
    # 处理家庭机器人领域
    print("正在处理 家庭机器人 领域...")
    try:
        homeai_services, homeai_norms, homeai_sources, homeai_apis, homeai_parameters = process_domain_services(
            js_file, "homeAIServices", "homeAIMetaApps"
        )
        all_services.extend(homeai_services)
        all_norms.extend(homeai_norms)
        all_sources.extend(homeai_sources)
        all_apis.extend(homeai_apis)
        all_parameters.extend(homeai_parameters)
        print("  家庭机器人领域处理完成: {0}个服务, {1}个规范, {2}个来源, {3}个API, {4}个参数".format(
            len(homeai_services), len(homeai_norms), len(homeai_sources), len(homeai_apis), len(homeai_parameters)
        ))
    except Exception as e:
        print("处理家庭机器人领域时出错: {}".format(e))
    
    # 生成数据统计信息
    print("\n数据统计：")
    print("服务总数: {0}".format(len(all_services)))
    print("规范总数: {0}".format(len(all_norms)))
    print("来源总数: {0}".format(len(all_sources)))
    print("API总数: {0}".format(len(all_apis)))
    print("参数总数: {0}".format(len(all_parameters)))
    
    # 写入所有数据到service.py
    try:
        print("\n开始写入数据到输出文件...")
        write_service_py(all_services, all_norms, all_sources, all_apis, all_parameters, output_file)
        print("\n已成功生成 {0} 文件".format(output_file))
    except Exception as e:
        print("写入输出文件时出错: {}".format(e))
        import traceback
        traceback.print_exc()
    
    print("脚本执行完毕!")

if __name__ == "__main__":
    main() 