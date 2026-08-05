"""
成果更新执行服务
实现自动更新逻辑
"""

import json
import uuid
import datetime
import time
import requests
from app.extensions import db
from app.models.service.service import Service
from app.models.service_update_strategy import ServiceUpdateStrategy
from app.models.service_update_history import ServiceUpdateHistory


class UpdateService:
    """成果更新服务"""

    def run_service_update(self, service_id, update_type="manual", reason=None):
        """
        执行成果更新

        Args:
            service_id: 成果ID
            update_type: 更新类型（manual/auto/scheduled）
            reason: 更新原因

        Returns:
            dict: 更新结果
        """
        # 获取成果信息
        service = Service.query.filter_by(id=service_id).first()
        if not service:
            return {"success": False, "error": "成果不存在"}

        # 创建更新记录
        update_record = ServiceUpdateHistory(
            id=str(uuid.uuid4()),
            service_id=service_id,
            update_type=update_type,
            update_status="pending",
            update_reason=reason or f"{update_type}更新"
        )
        db.session.add(update_record)
        db.session.commit()

        # 执行更新
        start_time = time.time()
        result = self._execute_update(service, update_type)
        end_time = time.time()
        duration = int((end_time - start_time) * 1000)

        # 更新记录
        update_record.update_status = result["status"]
        update_record.update_result = json.dumps(result)
        update_record.duration = duration
        update_record.update_time = int(datetime.datetime.now().timestamp() * 1000)

        db.session.commit()

        return result

    def _execute_update(self, service, update_type):
        """
        执行实际更新

        Args:
            service: 服务对象
            update_type: 更新类型

        Returns:
            dict: 更新结果
        """
        try:
            # 模拟更新过程
            # 实际应用中，这里应该：
            # 1. 检查是否有新版本
            # 2. 下载新版本代码
            # 3. 停止旧服务
            # 4. 部署新服务
            # 5. 启动新服务
            # 6. 验证服务状态

            # 这里简化实现：重新部署服务
            result = self._redeploy_service(service)

            return result

        except Exception as e:
            return {
                "success": False,
                "status": "error",
                "error": str(e),
                "service_name": service.name,
                "message": f"更新失败: {str(e)}"
            }

    def _redeploy_service(self, service):
        """
        重新部署服务

        Args:
            service: 服务对象

        Returns:
            dict: 部署结果
        """
        try:
            # 检查服务状态
            if service.status not in ["200", "ready", "running"]:
                return {
                    "success": False,
                    "status": "error",
                    "error": "服务状态异常，无法更新",
                    "service_name": service.name
                }

            # 模拟重新部署过程
            # 实际应用中应该调用部署接口或执行部署脚本

            # 更新服务状态（模拟）
            old_status = service.status
            service.status = "updating"
            db.session.commit()

            # 等待2秒模拟部署过程
            time.sleep(2)

            # 恢复服务状态
            service.status = "200"
            db.session.commit()

            return {
                "success": True,
                "status": "success",
                "service_name": service.name,
                "old_status": old_status,
                "new_status": "200",
                "message": "服务更新成功"
            }

        except Exception as e:
            # 恢复服务状态
            service.status = "error"
            db.session.commit()

            return {
                "success": False,
                "status": "error",
                "error": str(e),
                "service_name": service.name
            }

    def get_update_history(self, service_id, limit=10):
        """
        获取更新历史

        Args:
            service_id: 成果ID
            limit: 限制数量

        Returns:
            list: 更新历史列表
        """
        histories = ServiceUpdateHistory.query.filter_by(
            service_id=service_id
        ).order_by(
            ServiceUpdateHistory.update_time.desc()
        ).limit(limit).all()

        return [h.to_dict() for h in histories]

    def check_and_run_scheduled_updates(self):
        """
        检查并执行定时更新
        由定时任务调用
        """
        current_time = int(datetime.datetime.now().timestamp() * 1000)

        # 查询需要更新的成果
        strategies = ServiceUpdateStrategy.query.filter(
            ServiceUpdateStrategy.update_strategy_type == "scheduled"
        ).all()

        results = []
        for strategy in strategies:
            # 检查是否到了更新时间
            update_config = {}
            if strategy.update_config:
                try:
                    update_config = json.loads(strategy.update_config)
                except:
                    pass

            scheduled_date = update_config.get("scheduledDate")
            if scheduled_date:
                # 解析日期并检查是否需要更新
                try:
                    from datetime import datetime as dt
                    scheduled_time = int(dt.strptime(scheduled_date, "%Y-%m-%d").timestamp() * 1000)

                    if current_time >= scheduled_time:
                        result = self.run_service_update(
                            strategy.service_id,
                            update_type="scheduled",
                            reason="定时更新"
                        )
                        results.append({
                            "service_id": strategy.service_id,
                            "result": result
                        })
                except:
                    pass

        return results


# 创建全局实例
update_service = UpdateService()