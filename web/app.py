#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pyJianYingDraft Web Application - 精简版本
"""
from flask import Flask, jsonify
from logs.logger import setup_logger
from api_handlers import api_bp

logger = setup_logger('WebApp')

def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    
    # 配置
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'
    
    # 注册Blueprint
    app.register_blueprint(api_bp)
    logger.info("✅ 成功注册API Blueprint")
    
    # 统一错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": "接口不存在",
            "error": "404 Not Found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "message": "服务器内部错误",
            "error": "500 Internal Server Error"
        }), 500

    # 添加CORS支持
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    logger.info("============================================================")
    logger.info("🎬 pyJianYingDraft Web Service - 精简版本")
    logger.info("============================================================")
    logger.info("📝 项目描述: 剪映草稿生成Web服务")
    logger.info("🔧 版本信息: v1.0.0")
    logger.info("🌐 服务地址: http://0.0.0.0:5000")
    logger.info("============================================================")
    
    return app

# 创建应用实例
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
