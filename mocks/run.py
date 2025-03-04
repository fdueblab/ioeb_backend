#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mock服务启动脚本
"""

from mocks.remote_service import app

if __name__ == "__main__":
    print("=" * 50)
    print("启动模拟远程服务在 http://localhost:8000")
    print("该服务用于模拟接收主文件并返回生成的文件")
    print("=" * 50)
    app.run(host="0.0.0.0", port=8000, debug=True)
