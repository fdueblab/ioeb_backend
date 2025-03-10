import click
from flask.cli import FlaskGroup

from app import create_app
from app.extensions import db
from app.models import Role, RolePermission, User
from app.utils.flask_utils import get_flask_env
from mocks.user import MOCK_ROLES, MOCK_ROLES_PERMISSIONS, MOCK_USERS

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
    db.session.commit()
    click.echo("示例数据添加成功")


if __name__ == "__main__":
    cli()
