import os
import sys
import json
import uuid
import time
import hashlib
import copy
from functools import wraps
from flask import jsonify, request
from urllib.parse import urlparse
import mimetypes

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
            import traceback
            traceback.print_exc()
            return jsonify({
                "success": False,
                "message": f"{func.__name__} 失败: {str(e)}"
            }), 500
    return wrapper

def create_basic_script():
    """创建基础脚本对象"""
    return draft.Script_file(1920, 1080)

def ensure_user_uploads_dir():
    """确保用户上传目录存在"""
    user_uploads_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'user_uploads')
    if not os.path.exists(user_uploads_dir):
        os.makedirs(user_uploads_dir)
        logger.info(f"✅ 创建用户上传目录: {user_uploads_dir}")
    return user_uploads_dir

def get_file_extension_from_url(url, content_type=None):
    """从URL或Content-Type获取文件扩展名"""
    parsed_url = urlparse(url)
    path = parsed_url.path
    if '.' in path:
        ext = os.path.splitext(path)[1]
        if ext:
            return ext.lower()
    
    if content_type:
        ext = mimetypes.guess_extension(content_type)
        if ext:
            return ext.lower()
    
    return '.mp4' if 'video' in (content_type or '') else '.mp3'

def generate_unique_filename(file_type, url=None):
    """生成唯一文件名"""
    timestamp = int(time.time())
    if url:
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        return f"{file_type}_{timestamp}_{url_hash}"
    return f"{file_type}_{timestamp}_{str(uuid.uuid4())[:8]}"

def get_request_data():
    """获取请求数据，统一处理JSON和表单数据"""
    if request.is_json:
        return request.get_json() or {}
    return request.form.to_dict()

def create_success_response(message, data=None, **kwargs):
    """创建成功响应"""
    response = {
        "success": True,
        "message": message
    }
    if data is not None:
        response["data"] = data
    response.update(kwargs)
    return jsonify(response)

def create_error_response(message, status_code=500):
    """创建错误响应"""
    return jsonify({
        "success": False,
        "message": message
    }), status_code

def replace_paths_with_placeholders(data, assets):
    """将JSON中的绝对路径替换为占位符路径"""
    try:
        logger.info(f"🔄 开始路径占位符替换，共有 {len(assets)} 个素材文件")
        
        path_mapping = {}
        for asset in assets:
            actual_path = asset.get('actual_path', '')
            placeholder_path = asset.get('placeholder_path', f"{{PROJECT_DIR}}/assets/{asset['filename']}")
            if actual_path:
                normalized_actual = os.path.normpath(actual_path).replace('\\', '/')
                path_mapping[normalized_actual] = placeholder_path
                path_mapping[actual_path] = placeholder_path
                path_mapping[actual_path.replace('\\', '/')] = placeholder_path
                path_mapping[actual_path.replace('/', '\\')] = placeholder_path
        
        def replace_paths_recursive(obj, parent_key=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, str):
                        original_value = value
                        if ('\\' in value or '/' in value) and len(value) > 10:
                            for actual_path, placeholder_path in path_mapping.items():
                                if actual_path in value:
                                    value = value.replace(actual_path, placeholder_path)
                                    break
                        
                        if value != original_value:
                            logger.info(f"✅ 路径替换成功: {parent_key}.{key}")
                            obj[key] = value
                        elif os.path.isabs(original_value):
                            filename = os.path.basename(original_value)
                            fallback_placeholder = f"{{PROJECT_DIR}}/assets/{filename}"
                            obj[key] = fallback_placeholder
                    elif isinstance(value, (dict, list)):
                        replace_paths_recursive(value, f"{parent_key}.{key}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    replace_paths_recursive(item, f"{parent_key}[{i}]")
        
        replace_paths_recursive(data)
        logger.info("✅ 路径占位符替换完成")
        return data
        
    except Exception as e:
        logger.error(f"❌ 路径占位符替换失败: {e}")
        return data

def set_absolute_paths_in_project(project_data, project_dir):
    """将项目数据中的素材路径设置为绝对路径"""
    try:
        logger.info(f"🔄 设置绝对路径: {project_dir}")
        
        project_dir = os.path.normpath(project_dir)
        assets_dir = os.path.join(project_dir, 'assets')
        
        result_data = copy.deepcopy(project_data)
        
        def process_paths(obj, parent_key=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, str):
                        if any(ext in value.lower() for ext in ['.mp3', '.mp4', '.wav', '.avi', '.mov', '.m4a', '.aac']):
                            filename = os.path.basename(value)
                            
                            if filename.startswith('default_'):
                                new_path = os.path.join(assets_dir, filename)
                            else:
                                if filename.startswith('audio_') or filename.startswith('video_'):
                                    new_path = os.path.join(assets_dir, filename)
                                else:
                                    if any(ext in filename.lower() for ext in ['.mp3', '.wav', '.m4a', '.aac']):
                                        new_path = os.path.join(assets_dir, f"default_audio.mp3")
                                    else:
                                        new_path = os.path.join(assets_dir, f"default_video.mp4")
                            
                            new_path = os.path.normpath(new_path)
                            obj[key] = new_path
                            logger.info(f"✅ 路径更新: {parent_key}.{key} -> {new_path}")
                    
                    elif isinstance(value, (dict, list)):
                        process_paths(value, f"{parent_key}.{key}")
            
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    process_paths(item, f"{parent_key}[{i}]")
        
        process_paths(result_data)
        logger.info("✅ 绝对路径设置完成")
        return result_data
        
    except Exception as e:
        logger.error(f"❌ 设置绝对路径失败: {e}")
        return project_data

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
