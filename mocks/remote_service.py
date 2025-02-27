from flask import Flask, request, jsonify

# 创建Flask应用
app = Flask(__name__)

@app.route('/api/process', methods=['POST'])
def process_file():
    """
    模拟远程服务处理接口
    
    接收:
    {
        "file_name": "main.py",
        "file_content": "print('Hello World')"
    }
    
    返回:
    {
        "files": {
            "generated_file1.py": "print('Generated content 1')",
            "generated_file2.py": "print('Generated content 2')"
        }
    }
    """
    # 检查请求格式
    if not request.is_json:
        return jsonify({
            "error": "请求必须是JSON格式"
        }), 400
    
    data = request.get_json()
    
    # 检查请求参数
    if 'file_name' not in data or 'file_content' not in data:
        return jsonify({
            "error": "缺少必要的参数: file_name 或 file_content"
        }), 400
    
    # 从请求中获取文件名和内容
    file_name = data['file_name']
    file_content = data['file_content']
    
    print(f"收到文件: {file_name}")
    print(f"文件内容: {file_content[:100]}..." if len(file_content) > 100 else f"文件内容: {file_content}")
    
    # 模拟处理逻辑
    generated_files = {
        f"generated_{file_name}": f"# 这是由远程服务生成的文件\n# 基于源文件: {file_name}\n\n{file_content}\n\n# 添加了一些新功能\nprint('这是由远程服务生成的内容')",
        "helper.py": "# 辅助函数\n\ndef helper_function():\n    print('这是一个辅助函数')\n    return 'helper result'"
    }
    
    # 返回生成的文件
    return jsonify({
        "files": generated_files
    })

if __name__ == '__main__':
    print("启动模拟远程服务在 http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=True) 