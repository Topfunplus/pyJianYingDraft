#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pyJianYingDraft Web Service 启动脚本
"""

import os
import sys

# 设置当前工作目录为web目录
web_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(web_dir)

# 添加web目录到Python路径
sys.path.insert(0, web_dir)

# 添加项目根目录到Python路径
project_root = os.path.dirname(web_dir)
sys.path.insert(0, project_root)

print(f"📁 当前工作目录: {os.getcwd()}")
print(f"📂 Web目录: {web_dir}")
print(f"📂 项目根目录: {project_root}")
print(f"🐍 Python路径: {sys.path[:3]}...")

from logger_config import setup_logger
logger = setup_logger('WebServer')

try:
    from app import app
    print("✅ 成功导入Flask应用")
except ImportError as import_error:
    print(f"❌ 导入应用失败: {import_error}")
    print("🔧 尝试创建基本Flask应用...")
    
    # 创建基本的Flask应用作为备用
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def fallback_home():
        return jsonify({
            "error": "应用导入失败",
            "message": str(import_error),
            "status": "fallback_mode"
        })
    
    @app.route('/api/health')
    def fallback_health():
        return jsonify({
            "error": "API模块导入失败", 
            "message": str(import_error),
            "status": "fallback_mode"
        })


def main():
    """主函数"""
    if app is None:
        print("❌ 无法创建Flask应用")
        sys.exit(1)
        
    try:
        logger.info("="*60)
        logger.info("🎬 pyJianYingDraft Web Service")
        logger.info("="*60)
        logger.info("📝 项目描述: 剪映草稿生成Web服务")
        logger.info("🔧 版本信息: v1.0.0")
        logger.info("🌐 服务地址: http://0.0.0.0:5000")
        logger.info("📚 API文档: http://0.0.0.0:5000")
        logger.info("="*60)
        
        # 调试：检查路由
        print("\n🔍 检查应用路由:")
        for rule in app.url_map.iter_rules():
            if rule is not None and rule.methods:
                methods = [m for m in rule.methods if m not in ['HEAD', 'OPTIONS']]
                print(f"   {rule.rule} -> {rule.endpoint} [{', '.join(methods)}]")
        print()
        
        # 启动Flask应用
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,  # 生产环境设置为False
            threaded=True
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 收到中断信号，正在关闭服务...")
    except Exception as e:
        logger.error(f"❌ 服务启动失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        logger.info("👋 服务已关闭")

if __name__ == '__main__':
    main()
