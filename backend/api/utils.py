import pyJianYingDraft as draft
import logging
import os
import sys
from functools import wraps
import json
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
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


def create_basic_script():
    """创建基础脚本对象"""
    return draft.Script_file(1920, 1080, fps=30)


def save_draft_to_file(draft_content, filename=None):
    """保存草稿内容到文件"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"draft_{timestamp}.json"

    # 使用Django settings中的配置
    web_output_dir = getattr(settings, 'WEB_OUTPUT_DIR',
                             os.path.join(project_root, "web_outputs"))
    os.makedirs(web_output_dir, exist_ok=True)
    file_path = os.path.join(web_output_dir, filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(draft_content, f, ensure_ascii=False, indent=2)

    logger.info(f"✅ 草稿文件已保存: {file_path}")
    return file_path


def get_project_path():
    """获取项目保存路径"""
    # 使用与get_asset_path相同的基础目录，但子目录不同
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_dir = os.path.join(base_dir, 'projects')
    os.makedirs(project_dir, exist_ok=True)
    return project_dir


def get_output_path(project_name):
    """获取输出文件路径"""
    return os.path.join(get_project_path(), project_name)


def create_and_save_script(script, template_name, success_message, additional_data=None):
    """序列化草稿脚本对象并返回，不保存到本地

    Args:
        script: 草稿脚本对象
        template_name: 模板名称(仅用于标识，不会创建实际的文件)
        success_message: 成功消息
        additional_data: 附加数据

    Returns:
        Response: API响应，包含序列化的脚本内容
    """
    # 将Script_file对象序列化为JSON字符串，然后解析为字典
    script_json = json.loads(script.dumps())

    # 准备项目信息
    project_info = {
        "name": template_name
    }

    # 构建响应
    response_data = {
        "template_name": template_name,
        "project_info": project_info,
        "draft_content": script_json  # 直接返回序列化后的草稿内容
    }

    if additional_data:
        # 确保additional_data不覆盖draft_content
        if isinstance(additional_data, dict) and "draft_content" in additional_data:
            additional_data.pop("draft_content")
        response_data.update(additional_data)

    return create_success_response(success_message, **response_data)
