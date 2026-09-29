import click
from flask.cli import FlaskGroup

from app import create_app
from app.extensions import db
from app.utils.flask_utils import get_flask_env
from mocks.seed import seed_all_mock_data

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
    seed_all_mock_data()
    click.echo("示例数据添加成功")


@cli.command("seed_clinical")
def seed_clinical():
    """Initialize a fresh clinical database without importing demo users or services."""
    from app.models import Dictionary, Role, RolePermission
    from mocks.dictionary import MOCK_DICTIONARIES
    from mocks.user import MOCK_ROLES, MOCK_ROLES_PERMISSIONS

    db.create_all()
    allowed_roles = {"root", "admin", "publisher", "user", "AppDev", "MPAdm"}
    for row in MOCK_ROLES:
        if row["id"] in allowed_roles and not db.session.get(Role, row["id"]):
            db.session.add(Role(**row))
    for row in MOCK_ROLES_PERMISSIONS:
        if row["role_id"] in allowed_roles and not RolePermission.query.filter_by(
            role_id=row["role_id"], permission_id=row["permission_id"]
        ).first():
            db.session.add(RolePermission(**row))
    for item in MOCK_DICTIONARIES:
        if item["category"] == "domain" and item["code"] != "clinical":
            continue
        if not Dictionary.query.filter_by(category=item["category"], code=item["code"]).first():
            db.session.add(Dictionary(**item))
    db.session.commit()
    click.echo("临床站角色与字典初始化完成；未创建示例用户")


@cli.command("grant_clinical_admin")
@click.argument("username")
def grant_clinical_admin(username):
    """Grant the three platform permissions to an existing clinical-site account."""
    from app.models import User

    user = User.query.filter_by(username=username, deleted=0).first()
    if not user:
        raise click.ClickException("用户不存在，请先在临床站注册")
    user.role_id = "root"
    db.session.commit()
    click.echo(f"已授予 {username} 临床站管理员权限")


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
