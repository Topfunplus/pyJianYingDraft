#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pyJianYingDraft Web Application
"""

import os
import sys
from flask import Flask, jsonify

# 添加项目路径
web_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(web_dir)
sys.path.insert(0, web_dir)
sys.path.insert(0, project_root)

# 配置日志
try:
    from logger_config import setup_logger
    logger = setup_logger('WebApp')
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('WebApp')

# 创建Flask应用
app = Flask(__name__)

# 配置
app.config['JSON_AS_ASCII'] = False  # 支持中文JSON
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'

# 注册Blueprint
try:
    from api_handlers import api_bp
    app.register_blueprint(api_bp)
    logger.info("✅ 成功注册API Blueprint")
    
except ImportError as e:
    logger.error(f"❌ 无法导入API Blueprint: {e}")
    
    # 创建备用根路由
    @app.route('/')
    def fallback_root():
        return jsonify({
            "error": "API Blueprint导入失败",
            "message": str(e),
            "fallback": True
        })

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
