import os
import sys
from functools import wraps
from flask import jsonify
# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import pyJianYingDraft as draft
from config.settings import get_asset_path, get_output_path
from logs.logger import setup_logger


# 设置日志记录器
logger = setup_logger('API_Handler')

def api_error_handler(func):
    """API错误处理装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"❌ {func.__name__} 失败: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"{func.__name__} 失败: {str(e)}"
            }), 500
    return wrapper

def create_and_save_script(script, output_name, success_message, result_info):
    """创建并保存脚本的公共逻辑"""
    output_path = get_output_path(output_name)
    script.dump(output_path)
    
    logger.info(f"✅ {success_message}: {output_path}")
    
    return jsonify({
        "success": True,
        "message": success_message,
        "output_path": output_path,
        **result_info
    })

def create_basic_script():
    """创建基础脚本对象"""
    return draft.Script_file(1920, 1080)
