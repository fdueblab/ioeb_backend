"""
成果更新策略API路由
提供更新策略的CRUD接口
"""

import json
import uuid
import datetime
from flask import request
from flask_restx import Namespace, Resource, fields
from app.extensions import db
from app.models.service_update_strategy import ServiceUpdateStrategy
from app.models.service.service import Service

api = Namespace("update-strategy", description="成果更新策略管理")


# API模型定义
update_strategy_model = api.model("UpdateStrategy", {
    "autoTestEnabled": fields.Boolean(description="是否启用自动测试"),
    "autoTestPeriod": fields.Integer(description="自动测试周期（天）"),
    "updateStrategyType": fields.String(description="更新策略类型", enum=["manual", "auto", "scheduled"]),
    "updateConfig": fields.Raw(description="更新策略详细配置")
})


@api.route("/<string:service_id>")
@api.param("service_id", "成果ID")
class UpdateStrategyResource(Resource):
    """更新策略资源"""

    @api.doc("get_update_strategy")
    def get(self, service_id):
        """获取成果的更新策略"""
        try:
            # 验证成果是否存在
            service = Service.query.filter_by(id=service_id).first()
            if not service:
                return {"code": 404, "message": "成果不存在"}, 404
            
            # 查询策略
            strategy = ServiceUpdateStrategy.query.filter_by(service_id=service_id).first()
            
            if not strategy:
                return {
                    "code": 200,
                    "status": "success",
                    "data": None,
                    "message": "暂未配置更新策略"
                }
            
            return {
                "code": 200,
                "status": "success",
                "data": strategy.to_dict()
            }
        except Exception as e:
            return {"code": 500, "message": f"获取更新策略失败：{str(e)}"}, 500

    @api.doc("save_update_strategy")
    @api.expect(update_strategy_model)
    def post(self, service_id):
        """保存成果的更新策略"""
        try:
            # 验证成果是否存在
            service = Service.query.filter_by(id=service_id).first()
            if not service:
                return {"code": 404, "message": "成果不存在"}, 404
            
            # 获取请求数据
            data = request.get_json()
            if not data:
                return {"code": 400, "message": "请求数据不能为空"}, 400
            
            # 查询是否已存在策略
            strategy = ServiceUpdateStrategy.query.filter_by(service_id=service_id).first()
            
            current_time = int(datetime.datetime.now().timestamp() * 1000)
            
            if strategy:
                # 更新现有策略
                strategy.auto_test_enabled = data.get("autoTestEnabled", False)
                strategy.auto_test_period = data.get("autoTestPeriod", 0)
                strategy.update_strategy_type = data.get("updateStrategyType", "manual")
                strategy.update_config = json.dumps(data.get("updateConfig", {}))
                strategy.update_time = current_time
                
                # 计算下次测试时间
                if strategy.auto_test_enabled and strategy.auto_test_period > 0:
                    strategy.next_test_time = current_time + strategy.auto_test_period * 24 * 60 * 60 * 1000
                else:
                    strategy.next_test_time = None
            else:
                # 创建新策略
                strategy = ServiceUpdateStrategy(
                    id=str(uuid.uuid4()),
                    service_id=service_id,
                    auto_test_enabled=data.get("autoTestEnabled", False),
                    auto_test_period=data.get("autoTestPeriod", 0),
                    update_strategy_type=data.get("updateStrategyType", "manual"),
                    update_config=json.dumps(data.get("updateConfig", {})),
                    create_time=current_time,
                    update_time=current_time
                )
                
                # 计算下次测试时间
                if strategy.auto_test_enabled and strategy.auto_test_period > 0:
                    strategy.next_test_time = current_time + strategy.auto_test_period * 24 * 60 * 60 * 1000
                
                db.session.add(strategy)
            
            db.session.commit()
            
            return {
                "code": 200,
                "status": "success",
                "data": strategy.to_dict(),
                "message": "保存成功"
            }
        except Exception as e:
            db.session.rollback()
            return {"code": 500, "message": f"保存更新策略失败：{str(e)}"}, 500

    @api.doc("delete_update_strategy")
    def delete(self, service_id):
        """删除成果的更新策略"""
        try:
            # 查询策略
            strategy = ServiceUpdateStrategy.query.filter_by(service_id=service_id).first()
            
            if not strategy:
                return {"code": 404, "message": "更新策略不存在"}, 404
            
            db.session.delete(strategy)
            db.session.commit()
            
            return {
                "code": 200,
                "status": "success",
                "message": "删除成功"
            }
        except Exception as e:
            db.session.rollback()
            return {"code": 500, "message": f"删除更新策略失败：{str(e)}"}, 500


@api.route("/<string:service_id>/trigger-test")
@api.param("service_id", "成果ID")
class TriggerTestResource(Resource):
    """手动触发测试"""

    @api.doc("trigger_manual_test")
    def post(self, service_id):
        """手动触发测试"""
        try:
            # 验证成果是否存在
            service = Service.query.filter_by(id=service_id).first()
            if not service:
                return {"code": 404, "message": "成果不存在"}, 404

            # 执行测试
            from app.services.test_service import test_service
            result = test_service.run_service_test(service_id, test_type="manual")

            return {
                "code": 200,
                "status": "success",
                "data": result,
                "message": "测试执行完成"
            }
        except Exception as e:
            return {"code": 500, "message": f"触发测试失败：{str(e)}"}, 500


@api.route("/<string:service_id>/test-history")
@api.param("service_id", "成果ID")
class TestHistoryResource(Resource):
    """测试历史记录"""

    @api.doc("get_test_history")
    def get(self, service_id):
        """获取成果的测试历史"""
        try:
            # 验证成果是否存在
            service = Service.query.filter_by(id=service_id).first()
            if not service:
                return {"code": 404, "message": "成果不存在"}, 404

            # 获取测试历史
            from app.services.test_service import test_service
            limit = request.args.get('limit', 10, type=int)
            histories = test_service.get_test_history(service_id, limit=limit)

            return {
                "code": 200,
                "status": "success",
                "data": histories,
                "message": "获取测试历史成功"
            }
        except Exception as e:
            return {"code": 500, "message": f"获取测试历史失败：{str(e)}"}, 500


@api.route("/<string:service_id>/trigger-update")
@api.param("service_id", "成果ID")
class TriggerUpdateResource(Resource):
    """手动触发更新"""

    @api.doc("trigger_manual_update")
    def post(self, service_id):
        """手动触发更新"""
        try:
            # 验证成果是否存在
            service = Service.query.filter_by(id=service_id).first()
            if not service:
                return {"code": 404, "message": "成果不存在"}, 404

            # 执行更新
            from app.services.update_service import update_service
            data = request.get_json() or {}
            reason = data.get('reason', '手动更新')
            result = update_service.run_service_update(service_id, update_type="manual", reason=reason)

            return {
                "code": 200,
                "status": "success",
                "data": result,
                "message": "更新执行完成"
            }
        except Exception as e:
            return {"code": 500, "message": f"触发更新失败：{str(e)}"}, 500


@api.route("/<string:service_id>/update-history")
@api.param("service_id", "成果ID")
class UpdateHistoryResource(Resource):
    """更新历史记录"""

    @api.doc("get_update_history")
    def get(self, service_id):
        """获取成果的更新历史"""
        try:
            # 验证成果是否存在
            service = Service.query.filter_by(id=service_id).first()
            if not service:
                return {"code": 404, "message": "成果不存在"}, 404

            # 获取更新历史
            from app.services.update_service import update_service
            limit = request.args.get('limit', 10, type=int)
            histories = update_service.get_update_history(service_id, limit=limit)

            return {
                "code": 200,
                "status": "success",
                "data": histories,
                "message": "获取更新历史成功"
            }
        except Exception as e:
            return {"code": 500, "message": f"获取更新历史失败：{str(e)}"}, 500