"""
定时任务调度器
使用Flask-APScheduler实现定时任务
"""

from flask_apscheduler import APScheduler
from app.services.test_service import test_service
from app.services.update_service import update_service

# 创建调度器实例
scheduler = APScheduler()


def init_scheduler(app):
    """
    初始化定时任务调度器

    Args:
        app: Flask应用实例
    """
    # 配置调度器
    app.config['SCHEDULER_API_ENABLED'] = True
    app.config['SCHEDULER_TIMEZONE'] = "Asia/Shanghai"

    # 初始化调度器
    scheduler.init_app(app)

    # 添加定时任务
    # 每1小时检查一次是否需要执行测试
    @scheduler.task('interval', id='check_scheduled_tests', hours=1, misfire_grace_time=900)
    def check_scheduled_tests():
        """检查并执行定时测试"""
        with app.app_context():
            try:
                results = test_service.check_and_run_scheduled_tests()
                print(f"[定时任务-测试] 执行了 {len(results)} 个自动测试")
            except Exception as e:
                print(f"[定时任务-测试] 执行失败: {e}")

    # 每1小时检查一次是否需要执行更新
    @scheduler.task('interval', id='check_scheduled_updates', hours=1, misfire_grace_time=900)
    def check_scheduled_updates():
        """检查并执行定时更新"""
        with app.app_context():
            try:
                results = update_service.check_and_run_scheduled_updates()
                print(f"[定时任务-更新] 执行了 {len(results)} 个定时更新")
            except Exception as e:
                print(f"[定时任务-更新] 执行失败: {e}")

    # 启动调度器
    scheduler.start()

    print("[调度器] 定时任务调度器已启动")