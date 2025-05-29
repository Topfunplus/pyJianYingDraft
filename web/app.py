#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pyJianYingDraft Web Application
"""
from flask import Flask, jsonify
# 配置日志
from logs.logger import setup_logger
logger = setup_logger('WebApp')

# 创建Flask应用
app = Flask(__name__)
# 配置
app.config['JSON_AS_ASCII'] = False  # 支持中文JSON
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'
# 初始化异常信息变量
api_import_error = None
# 注册Blueprint
from api_handlers import api_bp
app.register_blueprint(api_bp)
logger.info("✅ 成功注册API Blueprint")
    


# 错误处理
@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        "success": False,
        "message": "接口不存在",
        "error": "404 Not Found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({
        "success": False,
        "message": "服务器内部错误",
        "error": "500 Internal Server Error"
    }), 500

# 添加CORS支持
@app.after_request
def after_request(response):
    """添加CORS头"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
