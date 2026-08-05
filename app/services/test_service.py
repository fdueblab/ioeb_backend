"""
成果测试执行服务
实现自动测试逻辑
"""

import json
import uuid
import datetime
import requests
from app.extensions import db
from app.models.service.service import Service
from app.models.service_update_strategy import ServiceUpdateStrategy
from app.models.service_test_history import ServiceTestHistory


class TestService:
    """成果测试服务"""

    def run_service_test(self, service_id, test_type="auto"):
        """
        执行成果测试

        Args:
            service_id: 成果ID
            test_type: 测试类型（auto/manual）

        Returns:
            dict: 测试结果
        """
        # 获取成果信息
        service = Service.query.filter_by(id=service_id).first()
        if not service:
            return {"success": False, "error": "成果不存在"}

        # 获取测试URL
        test_url = self._get_test_url(service)
        if not test_url:
            return {"success": False, "error": "无法获取测试地址"}

        # 创建测试记录
        test_record = ServiceTestHistory(
            id=str(uuid.uuid4()),
            service_id=service_id,
            test_type=test_type,
            test_status="pending"
        )
        db.session.add(test_record)
        db.session.commit()

        # 执行测试
        result = self._execute_test(test_url, service)

        # 更新测试记录
        test_record.test_status = result["status"]
        test_record.test_result = json.dumps(result)
        test_record.response_time = result.get("response_time")
        test_record.status_code = result.get("status_code")
        test_record.test_time = int(datetime.datetime.now().timestamp() * 1000)

        # 更新策略的last_test_time
        strategy = ServiceUpdateStrategy.query.filter_by(service_id=service_id).first()
        if strategy:
            strategy.last_test_time = test_record.test_time
            # 计算下次测试时间
            if strategy.auto_test_enabled and strategy.auto_test_period > 0:
                strategy.next_test_time = test_record.test_time + strategy.auto_test_period * 24 * 60 * 60 * 1000

        db.session.commit()

        return result

    def _get_test_url(self, service):
        """获取测试URL"""
        # 对于MCP类型服务，使用第一个API的URL
        if service.type == "atomic_mcp" and service.apis:
            return service.apis[0].url

        # 对于REST类型服务，使用第一个API的URL
        if service.apis:
            api = service.apis[0]
            return f"{api.url}"

        return None

    def _execute_test(self, url, service):
        """
        执行实际测试

        Args:
            url: 测试URL
            service: 服务对象

        Returns:
            dict: 测试结果
        """
        import time

        start_time = time.time()

        try:
            # 发送测试请求
            response = requests.get(
                url,
                timeout=30,
                headers={"User-Agent": "AutoTest/1.0"}
            )

            end_time = time.time()
            response_time = int((end_time - start_time) * 1000)

            # 判断测试结果
            if response.status_code == 200:
                status = "success"
            else:
                status = "failed"

            return {
                "success": True,
                "status": status,
                "status_code": response.status_code,
                "response_time": response_time,
                "url": url,
                "service_name": service.name,
                "message": f"测试完成，状态码: {response.status_code}"
            }

        except requests.Timeout:
            return {
                "success": False,
                "status": "error",
                "error": "请求超时",
                "url": url,
                "service_name": service.name
            }

        except requests.ConnectionError:
            return {
                "success": False,
                "status": "error",
                "error": "连接失败",
                "url": url,
                "service_name": service.name
            }

        except Exception as e:
            return {
                "success": False,
                "status": "error",
                "error": str(e),
                "url": url,
                "service_name": service.name
            }

    def get_test_history(self, service_id, limit=10):
        """
        获取测试历史

        Args:
            service_id: 成果ID
            limit: 限制数量

        Returns:
            list: 测试历史列表
        """
        histories = ServiceTestHistory.query.filter_by(
            service_id=service_id
        ).order_by(
            ServiceTestHistory.test_time.desc()
        ).limit(limit).all()

        return [h.to_dict() for h in histories]

    def check_and_run_scheduled_tests(self):
        """
        检查并执行定时测试
        由定时任务调用
        """
        current_time = int(datetime.datetime.now().timestamp() * 1000)

        # 查询需要测试的成果
        strategies = ServiceUpdateStrategy.query.filter(
            ServiceUpdateStrategy.auto_test_enabled == True,
            ServiceUpdateStrategy.next_test_time <= current_time
        ).all()

        results = []
        for strategy in strategies:
            result = self.run_service_test(strategy.service_id, test_type="auto")
            results.append({
                "service_id": strategy.service_id,
                "result": result
            })

        return results


# 创建全局实例
test_service = TestService()