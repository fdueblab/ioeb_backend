from flask_restx import Namespace, Resource

# 创建命名空间
api = Namespace("health", description="健康检查API")


@api.route("")
class HealthCheck(Resource):
    @api.doc("health_check", responses={200: "服务正常运行", 500: "服务异常"})
    def get(self):
        """健康检查接口"""
        return {"status": "success", "message": "服务运行正常"}, 200
