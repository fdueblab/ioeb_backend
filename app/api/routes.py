"""
这个文件中的路由已经被移动到了对应的命名空间中:
- 健康检查: app.api.namespaces.health_ns
- 用户管理: app.api.namespaces.user_ns
- 文件处理: app.api.namespaces.file_ns

保留此文件是为了参考和兼容旧代码。
新的路由应该添加到对应的命名空间中。
"""

# 下面代码已被注释，因为所有功能已移至命名空间中
# 如果需要参考旧代码，请取消注释

'''
from flask import jsonify, request, current_app, send_file
from app.api import api_bp
from app.models import User
from app.extensions import db
from app.utils.file_utils import create_temp_dir, extract_zip, find_main_file, create_zip, cleanup
from app.utils.remote_service import send_file_to_remote_service, RemoteServiceError
import os
import uuid
from werkzeug.utils import secure_filename

@api_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'success',
        'message': '服务运行正常'
    }), 200

@api_bp.route('/users', methods=['GET'])
def get_users():
    """获取所有用户"""
    users = User.query.all()
    return jsonify({
        'status': 'success',
        'users': [user.to_dict() for user in users]
    }), 200

@api_bp.route('/users', methods=['POST'])
def create_user():
    """创建新用户"""
    data = request.get_json()

    if not data or not data.get('username') or not data.get('email'):
        return jsonify({
            'status': 'fail',
            'message': '缺少必要的用户信息'
        }), 400

    # 检查用户是否已存在
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({
            'status': 'fail',
            'message': '用户已存在'
        }), 409

    new_user = User(
        username=data.get('username'),
        email=data.get('email')
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': '用户创建成功',
        'user': new_user.to_dict()
    }), 201

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@api_bp.route('/process', methods=['POST'])
def process_zip_file():
    """
    处理上传的ZIP文件

    流程:
    1. 接收用户上传的ZIP文件
    2. 创建临时目录并解压文件
    3. 分析代码识别主文件
    4. 将主文件发送给远程服务
    5. 接收远程服务返回的生成文件
    6. 将生成的文件写入目录
    7. 重新打包
    8. 返回给前端
    """
    # 检查是否有文件上传
    if 'file' not in request.files:
        return jsonify({
            'status': 'fail',
            'message': '没有文件上传'
        }), 400

    file = request.files['file']

    # 检查文件名
    if file.filename == '':
        return jsonify({
            'status': 'fail',
            'message': '未选择文件'
        }), 400

    # 检查文件类型
    if not allowed_file(file.filename):
        return jsonify({
            'status': 'fail',
            'message': '不支持的文件类型，仅支持ZIP文件'
        }), 400

    # 创建临时目录和变量，用于后续清理
    temp_dirs = []
    temp_files = []
    output_zip = None

    try:
        # 1. 保存上传的文件
        upload_dir = create_temp_dir()
        temp_dirs.append(upload_dir)

        zip_filename = secure_filename(file.filename)
        zip_path = os.path.join(upload_dir, zip_filename)
        file.save(zip_path)
        temp_files.append(zip_path)

        # 2. 创建解压目录并解压文件
        extract_dir = create_temp_dir()
        temp_dirs.append(extract_dir)
        extract_zip(zip_path, extract_dir)

        # 3. 查找主文件
        main_file_path = find_main_file(extract_dir)
        if not main_file_path:
            return jsonify({
                'status': 'fail',
                'message': '无法识别主文件'
            }), 400

        # 读取主文件内容
        with open(main_file_path, 'r', encoding='utf-8') as f:
            main_file_content = f.read()

        # 4. 发送主文件到远程服务
        generated_files = send_file_to_remote_service(
            main_file_path,
            main_file_content
        )

        # 5. 将生成的文件写入解压目录
        for filename, content in generated_files.items():
            # 确保文件名安全
            safe_filename = secure_filename(filename)
            output_path = os.path.join(extract_dir, safe_filename)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 6. 重新打包为ZIP文件
        result_dir = create_temp_dir()
        temp_dirs.append(result_dir)

        output_zip_name = f"processed_{uuid.uuid4().hex}.zip"
        output_zip = os.path.join(result_dir, output_zip_name)
        create_zip(extract_dir, output_zip)

        # 7. 返回处理后的文件
        return send_file(
            output_zip,
            as_attachment=True,
            download_name=output_zip_name,
            mimetype='application/zip'
        )

    except RemoteServiceError as e:
        return jsonify({
            'status': 'fail',
            'message': f'远程服务错误: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'处理文件时发生错误: {str(e)}'
        }), 500
    finally:
        # 清理临时文件和目录
        for temp_dir in temp_dirs:
            cleanup(temp_dir)
        for temp_file in temp_files:
            cleanup(temp_file)
        # 不要清理output_zip，它正在被send_file使用
'''
