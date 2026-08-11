#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""数据库初始化脚本"""

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from app import create_app
from app.extensions import db

# 创建应用
app = create_app('development')

# 初始化数据库
with app.app_context():
    db.create_all()
    print('Database initialized successfully')