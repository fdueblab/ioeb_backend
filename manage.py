import os

import click
import dotenv
from flask.cli import FlaskGroup

from app import create_app
from app.extensions import db
from app.models import (
    Dictionary,
    Role,
    RolePermission,
    Service,
    ServiceApi,
    ServiceApiParameter,
    ServiceApiTool,
    ServiceNorm,
    ServiceSource,
    User,
)
from app.utils.flask_utils import get_flask_env
from mocks.dictionary import MOCK_DICTIONARIES, MOCK_DICTIONARIES_UMS
from mocks.service import (
    MOCK_SERVICE_API_PARAMETERS,
    MOCK_SERVICE_API_TOOLS,
    MOCK_SERVICE_APIS,
    MOCK_SERVICE_NORMS,
    MOCK_SERVICE_SOURCES,
    MOCK_SERVICES,
)
from mocks.user import MOCK_ROLES, MOCK_ROLES_PERMISSIONS, MOCK_USERS

dotenv.load_dotenv()

env = get_flask_env()
app = create_app(env)
cli = FlaskGroup(create_app=lambda: app)


@cli.command("create_db")
def create_db():
    """创建数据库表"""
    db.create_all()
    click.echo("数据库表创建成功")


@cli.command("drop_db")
def drop_db():
    """删除数据库表"""
    if click.confirm("确定要删除所有数据库表吗？"):
        db.drop_all()
        click.echo("数据库表已删除")


@cli.command("seed_db")
def seed_db():
    """添加示例数据"""
    # 添加示例用户
    for user in MOCK_USERS:
        db.session.add(User(**user))
    # 添加示例角色
    for role in MOCK_ROLES:
        db.session.add(Role(**role))
    # 添加示例角色权限
    for role_permission in MOCK_ROLES_PERMISSIONS:
        db.session.add(RolePermission(**role_permission))

    # 添加示例服务数据
    for service in MOCK_SERVICES:
        db.session.add(Service(**service))
    # 添加示例服务规范数据
    for norm in MOCK_SERVICE_NORMS:
        db.session.add(ServiceNorm(**norm))
    # 添加示例服务来源数据
    for source in MOCK_SERVICE_SOURCES:
        db.session.add(ServiceSource(**source))
    # 添加示例服务API数据
    for api in MOCK_SERVICE_APIS:
        db.session.add(ServiceApi(**api))
    # 添加示例服务API参数数据
    for param in MOCK_SERVICE_API_PARAMETERS:
        db.session.add(ServiceApiParameter(**param))
    # 添加示例服务API工具数据
    for tool in MOCK_SERVICE_API_TOOLS:
        db.session.add(ServiceApiTool(**tool))
    # 添加示例字典数据
    if "dev" in os.getenv("DB_NAME"):
        for dictionary in MOCK_DICTIONARIES:
            db.session.add(Dictionary(**dictionary))
    elif "prod" in os.getenv("DB_NAME"):
        for dictionary in MOCK_DICTIONARIES_UMS:
            db.session.add(Dictionary(**dictionary))

    db.session.commit()
    click.echo("示例数据添加成功")


@cli.command("import_cos_datasets")
@click.option("--prefix", default="datasets/", help="COS对象前缀路径")
@click.option("--creator-id", help="创建者ID")
@click.option("--dry-run", is_flag=True, help="仅打印不执行导入")
@click.option("--force", is_flag=True, help="强制导入，即使文件已存在于数据库中")
def import_cos_datasets(prefix, creator_id, dry_run, force):
    """从腾讯云对象存储导入数据集文件"""
    # 检查COS工具是否初始化
    from app.utils.cos_utils import cos_utils
    from scripts.import_cos_datasets import import_cos_files

    if not hasattr(cos_utils, "_client") or cos_utils._client is None:
        click.echo("COS工具未正确初始化，请检查环境变量或配置")
        return

    # 导入文件
    import_cos_files(prefix=prefix, creator_id=creator_id, dry_run=dry_run, force=force)
    click.echo("导入完成")


if __name__ == "__main__":
    cli()
