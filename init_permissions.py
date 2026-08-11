#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""为AppDev角色添加默认权限"""

from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.extensions import db
from app.models.user.role_permission import RolePermission

app = create_app('development')

with app.app_context():
    # 检查AppDev角色是否已有权限
    existing_permissions = RolePermission.query.filter_by(role_id='AppDev').count()

    if existing_permissions == 0:
        print("Adding default permissions for AppDev role...")

        # 添加基本权限（根据实际需求调整）
        default_permissions = [
            {'permission_id': 'dashboard', 'permission_name': '仪表盘'},
            {'permission_id': 'user', 'permission_name': '用户中心'},
            {'permission_id': 'service', 'permission_name': '服务管理'},
            {'permission_id': 'dataset', 'permission_name': '数据集管理'},
        ]

        for perm in default_permissions:
            role_perm = RolePermission(
                role_id='AppDev',
                permission_id=perm['permission_id'],
                permission_name=perm['permission_name'],
                data_access='{}'  # 使用JSON字符串
            )
            db.session.add(role_perm)

        db.session.commit()
        print(f"[OK] Added {len(default_permissions)} permissions to AppDev role")
    else:
        print(f"[OK] AppDev role already has {existing_permissions} permissions")

    # 显示所有权限
    permissions = RolePermission.query.filter_by(role_id='AppDev').all()
    print("\nAppDev role permissions:")
    for p in permissions:
        print(f"  - {p.permission_id}: {p.permission_name}")