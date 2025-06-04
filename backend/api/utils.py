import logging
import os
import sys
from functools import wraps

from rest_framework import status
from rest_framework.response import Response

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

import pyJianYingDraft as draft
from config.settings import get_output_path

logger = logging.getLogger('api')

def api_error_handler(func):
    """API错误处理装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"❌ {func.__name__} 失败: {e}")
            return Response({
                "success": False,
                "message": f"操作失败: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper

def create_basic_script():
    """创建基础脚本对象"""
    return draft.Script_file(1920, 1080)

def create_success_response(message, **kwargs):
    """创建成功响应"""
    data = {"success": True, "message": message}
    data.update(kwargs)
    return Response(data)

def create_error_response(message, status_code=status.HTTP_400_BAD_REQUEST):
    """创建错误响应"""
    return Response({
        "success": False,
        "message": message
    }, status=status_code)

def save_draft_to_file(draft_content, filename=None):
    """保存草稿内容到文件"""
    import json
    from datetime import datetime
    from django.conf import settings
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"draft_{timestamp}.json"
    
    # 使用Django settings中的配置
    web_output_dir = getattr(settings, 'WEB_OUTPUT_DIR', os.path.join(project_root, "web_outputs"))
    os.makedirs(web_output_dir, exist_ok=True)
    file_path = os.path.join(web_output_dir, filename)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(draft_content, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✅ 草稿文件已保存: {file_path}")
    return file_path

def create_and_save_script(script, output_name, success_message, result_info=None):
    """创建并保存脚本"""
    output_path = get_output_path(output_name)
    script.dump(output_path)
    logger.info(f"✅ {success_message}: {output_path}")
    
    response_data = {
        "output_path": output_path,
        **(result_info or {})
    }
    return create_success_response(success_message, **response_data)
