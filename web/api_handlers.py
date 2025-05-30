import os
import json
import uuid
import time
import requests
import hashlib
from datetime import datetime
from flask import Blueprint, jsonify, request, send_file
from werkzeug.utils import secure_filename
from urllib.parse import urlparse
import mimetypes
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
web_dir = os.path.dirname(__file__)
sys.path.insert(0, web_dir)
import pyJianYingDraft as draft
from pyJianYingDraft import Track_type, trange, tim
from handlers.doc_handler import show_documentation 

# 使用绝对导入
try:
    from template.template import default_template
except ImportError:
    # 备用默认模板
    default_template = {
        "canvas_config": {"height": 1080, "width": 1920},
        "tracks": [],
        "materials": {"videos": [], "audios": [], "texts": []},
        "version": "1.0.0"
    }

# 创建Blueprint
api_bp = Blueprint('api', __name__)

# 创建用户上传目录
def ensure_user_uploads_dir():
    """确保用户上传目录存在"""
    user_uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'user_uploads')
    if not os.path.exists(user_uploads_dir):
        os.makedirs(user_uploads_dir)
        print(f"✅ 创建用户上传目录: {user_uploads_dir}")
    return user_uploads_dir

def get_file_extension_from_url(url, content_type=None):
    """从URL或Content-Type获取文件扩展名"""
    # 首先尝试从URL获取
    parsed_url = urlparse(url)
    path = parsed_url.path
    if '.' in path:
        ext = os.path.splitext(path)[1]
        if ext:
            return ext.lower()
    
    # 如果URL没有扩展名，从Content-Type获取
    if content_type:
        ext = mimetypes.guess_extension(content_type)
        if ext:
            return ext.lower()
    
    # 默认扩展名
    return '.mp4' if 'video' in (content_type or '') else '.mp3'

# 加载草稿模板
def load_draft_template():
    """加载草稿模板"""
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pyJianYingDraft', 'draft_content_template.json')
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # 如果模板文件不存在，返回基础模板
        return default_template

def create_video_track():
    """创建视频轨道"""
    return {
        "attribute": 0,
        "flag": 0,
        "id": str(uuid.uuid4()).upper(),
        "segments": [],
        "type": "video"
    }

def create_audio_track():
    """创建音频轨道"""
    return {
        "attribute": 0,
        "flag": 0,
        "id": str(uuid.uuid4()).upper(),
        "segments": [],
        "type": "audio"
    }

def create_text_track():
    """创建文本轨道"""
    return {
        "attribute": 0,
        "flag": 0,
        "id": str(uuid.uuid4()).upper(),
        "segments": [],
        "type": "text"
    }
# API处理函数
def health_check():
    """健康检查接口"""
    return jsonify({
        "success": True,
        "message": "API服务正常运行",
        "endpoints": {
            "/api/basic-project": "创建基础项目",
            "/api/audio-segment": "创建音频片段",
            "/api/video-segment": "创建视频片段", 
            "/api/text-segment": "创建文本片段",
            "/api/video-animation": "创建视频动画",
            "/api/text-animation": "创建文本动画",
            "/api/transition": "创建转场效果",
            "/api/background-filling": "创建背景填充",
            "/api/text-effects": "创建文本特效",
            "/api/comprehensive": "创建综合项目"
        },
        "version": "1.0.0",
        "status": "running"
    })

def handle_basic_project():
    """处理基础项目创建API"""
    try:
        # 创建剪映草稿
        script = draft.Script_file(1920, 1080)  # 1920x1080分辨率
        # 添加基础轨道
        script.add_track(Track_type.video).add_track(Track_type.audio)
        # 导出为JSON格式
        draft_json = script.dumps()
        return jsonify({
            "success": True,
            "message": "基础项目创建成功",
            "data": json.loads(draft_json)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"创建基础项目失败: {str(e)}"
        }), 500

def handle_text_segment():
    """处理文本片段API"""
    try:
        data = request.get_json() or {}
        text = data.get('text', '这是一个文本测试')
        duration_str = data.get('duration', '3s')
        color = data.get('color', [1.0, 1.0, 1.0])  # 默认白色
        font = data.get('font', None)
        # 创建剪映草稿
        script = draft.Script_file(1920, 1080)
        # 添加文本轨道
        script.add_track(Track_type.text)
        # 创建文本样式
        text_style = draft.Text_style(color=tuple(color))
        # 创建文本片段
        text_segment = draft.Text_segment(
            text, 
            trange("0s", duration_str),
            style=text_style,
            clip_settings=draft.Clip_settings(transform_y=-0.8)
        )
        # 设置字体（如果提供）
        if font and hasattr(draft.Font_type, font):
            text_segment.font = getattr(draft.Font_type, font).value
        
        # 添加片段到脚本
        script.add_segment(text_segment)
        
        # 导出为JSON格式
        draft_json = script.dumps()
        
        return jsonify({
            "success": True,
            "message": "文本片段创建成功",
            "data": json.loads(draft_json)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"创建文本片段失败: {str(e)}"
        }), 500

def handle_audio_segment():
    """处理音频片段API"""
    try:
        data = request.get_json() or {}
        duration_str = data.get('duration', '5s')
        volume = data.get('volume', 0.6)
        fade_in = data.get('fade_in', '0s')
        # 创建剪映草稿
        script = draft.Script_file(1920, 1080)
        # 添加音频轨道
        script.add_track(Track_type.audio)
        # 注意：由于没有实际音频文件，这里创建一个模拟的音频材料
        # 在实际使用中，需要提供真实的音频文件路径
        # 导出为JSON格式（基础项目结构）
        draft_json = script.dumps()
        return jsonify({
            "success": True,
            "message": "音频片段创建成功（需要实际音频文件）",
            "data": json.loads(draft_json),
            "note": "实际使用时需要提供音频文件路径"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"创建音频片段失败: {str(e)}"
        }), 500

def handle_video_segment():
    """处理视频片段API"""
    try:
        data = request.get_json() or {}
        duration_str = data.get('duration', '4.2s')
        
        # 创建剪映草稿
        script = draft.Script_file(1920, 1080)
        
        # 添加视频轨道
        script.add_track(Track_type.video)
        
        # 注意：由于没有实际视频文件，这里创建基础项目结构
        # 在实际使用中，需要提供真实的视频文件路径
        
        # 导出为JSON格式
        draft_json = script.dumps()
        
        return jsonify({
            "success": True,
            "message": "视频片段创建成功（需要实际视频文件）",
            "data": json.loads(draft_json),
            "note": "实际使用时需要提供视频文件路径"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"创建视频片段失败: {str(e)}"
        }), 500

def handle_comprehensive():
    """处理综合测试API"""
    try:
        # 创建剪映草稿
        script = draft.Script_file(1920, 1080)
        
        # 添加多个轨道
        script.add_track(Track_type.audio).add_track(Track_type.video).add_track(Track_type.text)
        
        # 创建文本片段
        text_segment = draft.Text_segment(
            "pyJianYingDraft综合测试", 
            trange("0s", "4.2s"),
            style=draft.Text_style(color=(1.0, 1.0, 0.0)),  # 黄色
            clip_settings=draft.Clip_settings(transform_y=-0.8)
        )
        
        # 添加文本动画
        text_segment.add_animation(draft.Text_outro.故障闪动, duration=tim("1s"))
        
        # 添加片段到脚本
        script.add_segment(text_segment)
        
        # 导出为JSON格式
        draft_json = script.dumps()
        
        return jsonify({
            "success": True,
            "message": "综合项目创建成功",
            "data": json.loads(draft_json)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"创建综合项目失败: {str(e)}"
        }), 500

def handle_video_animation():
    """处理视频动画API"""
    try:
        data = request.get_json() or {}
        animation_type = data.get('animation_type', '斜切')
        duration_str = data.get('duration', '3s')
        
        # 创建剪映草稿
        script = draft.Script_file(1920, 1080)
        script.add_track(Track_type.video)
        
        # 注意：实际使用时需要视频素材
        # 这里只展示动画配置的数据结构
        
        draft_json = script.dumps()
        
        return jsonify({
            "success": True,
            "message": f"视频动画({animation_type})配置成功",
            "data": json.loads(draft_json),
            "animation": animation_type
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"配置视频动画失败: {str(e)}"
        }), 500

def handle_text_animation():
    """处理文本动画API"""
    try:
        data = request.get_json() or {}
        text = data.get('text', '动画文本测试')
        animation_type = data.get('animation_type', '渐显')
        duration_str = data.get('duration', '2s')
        
        # 创建剪映草稿
        script = draft.Script_file(1920, 1080)
        script.add_track(Track_type.text)
        
        # 创建文本片段
        text_segment = draft.Text_segment(
            text, 
            trange("0s", duration_str),
            style=draft.Text_style(color=(0.0, 1.0, 1.0)),  # 青色
        )
        
        # 尝试添加入场动画
        try:
            if hasattr(draft.Text_intro, animation_type):
                animation = getattr(draft.Text_intro, animation_type)
                text_segment.add_animation(animation, duration=tim("0.5s"))
        except:
            pass  # 如果动画类型不存在，忽略错误
        
        script.add_segment(text_segment)
        draft_json = script.dumps()
        
        return jsonify({
            "success": True,
            "message": f"文本动画({animation_type})创建成功",
            "data": json.loads(draft_json)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"创建文本动画失败: {str(e)}"
        }), 500

def handle_transition():
    """处理转场效果API"""
    try:
        data = request.get_json() or {}
        transition_type = data.get('transition_type', '淡化')
        
        # 创建剪映草稿
        script = draft.Script_file(1920, 1080)
        script.add_track(Track_type.video)
        
        # 注意：转场需要两个视频片段，这里只展示配置结构
        
        draft_json = script.dumps()
        
        return jsonify({
            "success": True,
            "message": f"转场效果({transition_type})配置成功",
            "data": json.loads(draft_json),
            "transition": transition_type,
            "note": "转场效果需要两个视频片段才能生效"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"配置转场效果失败: {str(e)}"
        }), 500

def handle_background_filling():
    """处理背景填充API"""
    try:
        data = request.get_json() or {}
        fill_type = data.get('fill_type', 'blur')
        intensity = data.get('intensity', 0.0625)
        
        # 创建剪映草稿
        script = draft.Script_file(1920, 1080)
        script.add_track(Track_type.video)
        
        # 注意：背景填充需要视频素材
        
        draft_json = script.dumps()
        
        return jsonify({
            "success": True,
            "message": f"背景填充({fill_type})配置成功",
            "data": json.loads(draft_json),
            "fill_type": fill_type,
            "intensity": intensity
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"配置背景填充失败: {str(e)}"
        }), 500

def handle_text_effects():
    """处理文本特效API"""
    try:
        data = request.get_json() or {}
        text = data.get('text', '特效文本')
        effect_type = data.get('effect_type', 'bubble')
        
        # 创建剪映草稿
        script = draft.Script_file(1920, 1080)
        script.add_track(Track_type.text)
        
        # 创建文本片段
        text_segment = draft.Text_segment(
            text, 
            trange("0s", "3s"),
            style=draft.Text_style(color=(1.0, 0.5, 0.0)),  # 橙色
        )
        
        # 根据特效类型添加效果
        if effect_type == 'bubble':
            # 示例气泡效果ID（实际使用时需要从模板中获取）
            try:
                text_segment.add_bubble("361595", "6742029398926430728")
            except:
                pass
        elif effect_type == 'flower':
            # 示例花字效果ID
            try:
                text_segment.add_effect("7296357486490144036")
            except:
                pass
        
        script.add_segment(text_segment)
        draft_json = script.dumps()
        
        return jsonify({
            "success": True,
            "message": f"文本特效({effect_type})创建成功",
            "data": json.loads(draft_json)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"创建文本特效失败: {str(e)}"
        }), 500

def handle_comprehensive_create():
    """处理综合创作API - 集成所有组件到一个项目中"""
    try:
        print("🚀 收到综合创作请求")
        data = request.get_json() or {}
        print(f"📝 请求数据: {data}")
        
        # 创建剪映草稿
        script = draft.Script_file(1920, 1080)
        
        # 添加所有类型的轨道
        script.add_track(Track_type.text).add_track(Track_type.video).add_track(Track_type.audio)
        
        segments_info = []
        required_assets = []
        current_time = 0
        
        # 检查默认素材文件
        tutorial_asset_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'readme_assets', 'tutorial')
        user_uploads_dir = ensure_user_uploads_dir()
        
        # 处理音频组件
        if data.get('audio', {}).get('enabled', False):
            audio_config = data['audio'].get('config', {})
            duration = audio_config.get('duration', '5s')
            volume = audio_config.get('volume', 0.6)
            fade_in = audio_config.get('fade_in', '1s')
            
            # 确定音频文件信息
            audio_filename = None
            audio_source = "default"
            actual_audio_path = None
            
            if os.path.exists(user_uploads_dir):
                user_audio_files = [f for f in os.listdir(user_uploads_dir) if f.startswith('audio_') and os.path.isfile(os.path.join(user_uploads_dir, f))]
                if user_audio_files:
                    user_audio_files.sort(reverse=True)
                    audio_filename = user_audio_files[0]
                    audio_source = "user_upload"
                    actual_audio_path = os.path.join(user_uploads_dir, audio_filename)
                    print(f"📁 将使用用户音频文件: {audio_filename}")
            
            if not audio_filename:
                audio_filename = "default_audio.mp3"
                audio_source = "default"
                actual_audio_path = os.path.join(tutorial_asset_dir, 'audio.mp3')
                print(f"📁 将使用默认音频文件: {audio_filename}")
            
            # 创建音频素材
            try:
                if os.path.exists(actual_audio_path):
                    audio_material = draft.Audio_material(actual_audio_path)
                    audio_segment = draft.Audio_segment(
                        audio_material,
                        trange("0s", duration),
                        volume=volume
                    )
                    if fade_in != '0s':
                        audio_segment.add_fade(fade_in, "0s")
                    
                    script.add_segment(audio_segment)
                    
                    # 记录素材信息，使用占位符路径
                    required_assets.append({
                        "type": "audio",
                        "filename": audio_filename,
                        "actual_path": actual_audio_path,
                        "placeholder_path": f"{{PROJECT_DIR}}/assets/{audio_filename}",
                        "source": audio_source,
                        "description": f"音频素材文件 - {audio_source == 'user_upload' and '用户上传' or '系统默认'}"
                    })
                    print(f"✅ 成功添加音频片段: {audio_filename}")
                else:
                    print(f"❌ 音频文件不存在: {actual_audio_path}")
                    
            except Exception as e:
                print(f"❌ 音频片段添加失败: {e}")
            
            segments_info.append({
                "type": "audio",
                "duration": duration,
                "volume": volume,
                "fade_in": fade_in,
                "filename": audio_filename,
                "source": audio_source,
                "supports_user_upload": True,
                "supports_url_download": True
            })
        
        # 处理视频组件
        if data.get('video', {}).get('enabled', False):
            video_config = data['video'].get('config', {})
            duration = video_config.get('duration', '4.2s')
            
            # 确定视频文件信息
            video_filename = None
            video_source = "default"
            actual_video_path = None
            
            if os.path.exists(user_uploads_dir):
                user_video_files = [f for f in os.listdir(user_uploads_dir) if f.startswith('video_') and os.path.isfile(os.path.join(user_uploads_dir, f))]
                if user_video_files:
                    user_video_files.sort(reverse=True)
                    video_filename = user_video_files[0]
                    video_source = "user_upload"
                    actual_video_path = os.path.join(user_uploads_dir, video_filename)
                    print(f"📁 将使用用户视频文件: {video_filename}")
            
            if not video_filename:
                video_filename = "default_video.mp4"
                video_source = "default"
                actual_video_path = os.path.join(tutorial_asset_dir, 'video.mp4')
                print(f"📁 将使用默认视频文件: {video_filename}")
            
            # 创建视频素材
            try:
                if os.path.exists(actual_video_path):
                    video_material = draft.Video_material(actual_video_path)
                    video_segment = draft.Video_segment(
                        video_material,
                        trange(f"{current_time}s", duration)
                    )
                    script.add_segment(video_segment)
                    
                    # 记录素材信息，使用占位符路径
                    required_assets.append({
                        "type": "video",
                        "filename": video_filename,
                        "actual_path": actual_video_path,
                        "placeholder_path": f"{{PROJECT_DIR}}/assets/{video_filename}",
                        "source": video_source,
                        "description": f"视频素材文件 - {video_source == 'user_upload' and '用户上传' or '系统默认'}"
                    })
                    print(f"✅ 成功添加视频片段: {video_filename}")
                else:
                    print(f"❌ 视频文件不存在: {actual_video_path}")
                    
            except Exception as e:
                print(f"❌ 视频片段添加失败: {e}")
            
            segments_info.append({
                "type": "video",
                "duration": duration,
                "start_time": f"{current_time}s",
                "filename": video_filename,
                "source": video_source,
                "supports_user_upload": True,
                "supports_url_download": True
            })
            current_time += float(duration.replace('s', ''))
        
        # 处理文本组件
        if data.get('text', {}).get('enabled', False):
            text_config = data['text'].get('config', {})
            duration = text_config.get('duration', '3s')
            
            text_segment = draft.Text_segment(
                text_config.get('text', '综合创作文本'),
                trange(f"{current_time}s", duration),
                style=draft.Text_style(color=tuple(text_config.get('color', [1.0, 1.0, 1.0]))),
                clip_settings=draft.Clip_settings(transform_y=-0.8)
            )
            
            # 设置字体
            font = text_config.get('font', '文轩体')
            if hasattr(draft.Font_type, font):
                text_segment.font = getattr(draft.Font_type, font)
            
            script.add_segment(text_segment)
            segments_info.append({
                "type": "text",
                "content": text_config.get('text', '综合创作文本'),
                "duration": duration,
                "start_time": f"{current_time}s"
            })
            current_time += float(duration.replace('s', ''))
        
        # 处理动画组件
        if data.get('animation', {}).get('enabled', False):
            animation_config = data['animation'].get('config', {})
            duration = animation_config.get('duration', '2s')
            
            animation_segment = draft.Text_segment(
                animation_config.get('text', '动画文本'),
                trange(f"{current_time}s", duration),
                style=draft.Text_style(color=(0.0, 1.0, 1.0)),
                clip_settings=draft.Clip_settings(transform_y=0.8)  # 上方位置，避免重叠
            )
            
            # 添加动画效果
            try:
                animation_type = animation_config.get('animation_type', '故障闪动')
                if hasattr(draft.Text_outro, animation_type):
                    animation = getattr(draft.Text_outro, animation_type)
                    animation_segment.add_animation(animation, duration=tim("1s"))
                elif hasattr(draft.Text_intro, animation_type):
                    animation = getattr(draft.Text_intro, animation_type)
                    animation_segment.add_animation(animation, duration=tim("0.5s"))
            except Exception as e:
                print(f"动画添加失败: {e}")
            
            script.add_segment(animation_segment)
            segments_info.append({
                "type": "text_animation", 
                "content": animation_config.get('text', '动画文本'),
                "animation_type": animation_config.get('animation_type', '故障闪动'),
                "duration": duration,
                "start_time": f"{current_time}s"
            })
            current_time += float(duration.replace('s', ''))
        
        # 处理特效组件
        if data.get('effects', {}).get('enabled', False):
            effects_config = data['effects'].get('config', {})
            duration = effects_config.get('duration', '3s')
            
            effects_segment = draft.Text_segment(
                effects_config.get('text', '特效文本'),
                trange(f"{current_time}s", duration),
                style=draft.Text_style(color=(1.0, 0.5, 0.0)),
                clip_settings=draft.Clip_settings(transform_y=0.0)  # 中间位置
            )
            
            # 添加特效
            try:
                effect_type = effects_config.get('effect_type', 'bubble')
                if effect_type == 'bubble':
                    effects_segment.add_bubble("361595", "6742029398926430728")
                elif effect_type == 'flower':
                    effects_segment.add_effect("7296357486490144036")
            except Exception as e:
                print(f"特效添加失败: {e}")
            
            script.add_segment(effects_segment)
            segments_info.append({
                "type": "text_effects",
                "content": effects_config.get('text', '特效文本'),
                "effect_type": effects_config.get('effect_type', 'bubble'),
                "duration": duration,
                "start_time": f"{current_time}s"
            })
            current_time += float(duration.replace('s', ''))
        
        # 处理转场组件
        if data.get('transition', {}).get('enabled', False):
            transition_config = data['transition'].get('config', {})
            segments_info.append({
                "type": "transition",
                "transition_type": transition_config.get('transition_type', '信号故障'),
                "segment1_duration": transition_config.get('segment1_duration', '2s'),
                "segment2_duration": transition_config.get('segment2_duration', '2s'),
                "note": "转场效果需要两个视频片段"
            })
        
        # 如果没有任何组件，创建默认内容
        if not segments_info:
            default_segment = draft.Text_segment(
                "默认综合项目 - 请配置组件",
                trange("0s", "3s"),
                style=draft.Text_style(color=(1.0, 1.0, 0.0)),
                clip_settings=draft.Clip_settings(transform_y=-0.8)
            )
            script.add_segment(default_segment)
            segments_info.append({
                "type": "default_text",
                "content": "默认综合项目 - 请配置组件",
                "duration": "3s",
                "start_time": "0s"
            })
        
        # 导出为统一的JSON格式
        draft_json = script.dumps()
        unified_data = json.loads(draft_json)
        
        # 替换材料路径为占位符路径
        unified_data = replace_paths_with_placeholders(unified_data, required_assets)
        
        # 添加项目元信息
        unified_data['project_meta'] = {
            "created_by": "pyJianYingDraft综合创作",
            "creation_time": current_time,
            "total_duration": f"{current_time}s",
            "components_count": len(segments_info),
            "enabled_features": [key for key, value in data.items() if value.get('enabled', False)],
            "segments_summary": segments_info,
            "required_assets": required_assets,
            "supports_user_assets": True,
            "supports_url_download": True,
            "user_uploads_dir": user_uploads_dir,
            "path_info": {
                "note": "所有素材路径使用占位符 {PROJECT_DIR}/assets/filename",
                "import_instruction": "下载时需要选择剪映工程目录，系统将自动替换为正确的绝对路径"
            }
        }
        
        print(f"✅ 综合项目创建成功，包含 {len(segments_info)} 个组件，{len(required_assets)} 个素材文件")
        
        response_data = {
            "success": True,
            "message": "综合项目创建成功",
            "data": unified_data,
            "summary": {
                "total_duration": f"{current_time}s",
                "components_count": len(segments_info),
                "enabled_features": [key for key, value in data.items() if value.get('enabled', False)],
                "segments": segments_info,
                "assets": required_assets
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ 综合创作失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"创建综合项目失败: {str(e)}"
        }), 500

def replace_paths_with_placeholders(data, assets):
    """将JSON中的绝对路径替换为占位符路径"""
    try:
        print(f"🔄 开始路径占位符替换，共有 {len(assets)} 个素材文件")
        
        # 创建路径映射字典
        path_mapping = {}
        for asset in assets:
            actual_path = asset.get('actual_path', '')
            placeholder_path = asset.get('placeholder_path', f"{{PROJECT_DIR}}/assets/{asset['filename']}")
            if actual_path:
                # 统一路径分隔符并添加多种格式的映射
                normalized_actual = os.path.normpath(actual_path).replace('\\', '/')
                path_mapping[normalized_actual] = placeholder_path
                path_mapping[actual_path] = placeholder_path
                path_mapping[actual_path.replace('\\', '/')] = placeholder_path
                path_mapping[actual_path.replace('/', '\\')] = placeholder_path
                print(f"📍 路径映射: {actual_path} -> {placeholder_path}")
        
        # 递归替换路径
        def replace_paths_recursive(obj, parent_key=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, str):
                        original_value = value  # 在这里初始化变量
                        # 检查是否包含路径分隔符
                        if ('\\' in value or '/' in value) and len(value) > 10:
                            # 尝试直接匹配
                            for actual_path, placeholder_path in path_mapping.items():
                                if actual_path in value:
                                    value = value.replace(actual_path, placeholder_path)
                                    break
                        
                        # 记录替换结果
                        if value != original_value:
                            print(f"✅ 路径替换成功: {parent_key}.{key}")
                            print(f"   原路径: {original_value}")
                            print(f"   占位符: {value}")
                            obj[key] = value
                        elif os.path.isabs(original_value):
                            # 如果仍然是绝对路径，使用通用占位符
                            filename = os.path.basename(original_value)
                            fallback_placeholder = f"{{PROJECT_DIR}}/assets/{filename}"
                            obj[key] = fallback_placeholder
                            print(f"⚠️ 使用备用占位符: {parent_key}.{key} -> {fallback_placeholder}")
                    elif isinstance(value, (dict, list)):
                        replace_paths_recursive(value, f"{parent_key}.{key}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    replace_paths_recursive(item, f"{parent_key}[{i}]")
        
        # 执行路径替换
        replace_paths_recursive(data)
        
        print("✅ 路径占位符替换完成")
        return data
        
    except Exception as e:
        print(f"❌ 路径占位符替换失败: {e}")
        import traceback
        traceback.print_exc()
        return data

def replace_placeholders_with_absolute_paths(data, project_dir):
    """将占位符路径替换为用户选择的绝对路径"""
    try:
        print(f"🔄 开始将占位符替换为绝对路径: {project_dir}")
        
        # 统一路径分隔符
        project_dir = os.path.normpath(project_dir).replace('\\', '/')
        
        # 递归替换占位符
        def replace_placeholders_recursive(obj, parent_key=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, str):
                        if '{PROJECT_DIR}' in value:
                            original_value = value
                            # 替换占位符为实际路径
                            new_value = value.replace('{PROJECT_DIR}', project_dir)
                            # 统一路径分隔符
                            new_value = os.path.normpath(new_value).replace('\\', '/')
                            obj[key] = new_value
                            print(f"✅ 占位符替换: {parent_key}.{key}")
                            print(f"   原占位符: {original_value}")
                            print(f"   新绝对路径: {new_value}")
                    elif isinstance(value, (dict, list)):
                        replace_placeholders_recursive(value, f"{parent_key}.{key}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    replace_placeholders_recursive(item, f"{parent_key}[{i}]")
        
        # 创建数据副本以避免修改原始数据
        import copy
        result_data = copy.deepcopy(data)
        
        # 执行占位符替换
        replace_placeholders_recursive(result_data)
        
        print("✅ 占位符替换为绝对路径完成")
        return result_data
        
    except Exception as e:
        print(f"❌ 占位符替换失败: {e}")
        import traceback
        traceback.print_exc()
        return data

@api_bp.route('/api/download-from-url', methods=['POST'])
def api_download_from_url():
    """从网址下载音视频文件"""
    try:
        data = request.get_json() or {}
        url = data.get('url', '').strip()
        file_type = data.get('type', 'video')  # 'audio' or 'video'
        
        if not url:
            return jsonify({
                "success": False,
                "message": "请提供有效的网址"
            }), 400
        
        print(f"🌐 开始下载 {file_type} 文件: {url}")
        
        # 确保用户上传目录存在
        user_uploads_dir = ensure_user_uploads_dir()
        
        # 发送请求下载文件
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()
        
        # 获取Content-Type
        content_type = response.headers.get('content-type', '').lower()
        
        # 验证文件类型
        if file_type == 'audio' and not any(t in content_type for t in ['audio', 'mpeg', 'mp3', 'wav', 'ogg']):
            return jsonify({
                "success": False,
                "message": "网址不是有效的音频文件"
            }), 400
        elif file_type == 'video' and not any(t in content_type for t in ['video', 'mp4', 'avi', 'mov', 'webm']):
            return jsonify({
                "success": False,
                "message": "网址不是有效的视频文件"
            }), 400
        
        # 生成唯一文件名
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        timestamp = int(time.time())
        file_extension = get_file_extension_from_url(url, content_type)
        filename = f"{file_type}_{timestamp}_{url_hash}{file_extension}"
        
        # 保存文件
        file_path = os.path.join(user_uploads_dir, filename)
        file_size = 0
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    file_size += len(chunk)
        
        print(f"✅ 文件下载成功: {filename} ({file_size/1024/1024:.2f} MB)")
        
        return jsonify({
            "success": True,
            "message": f"{file_type}文件下载成功",
            "filename": filename,
            "size": file_size,
            "path": file_path
        })
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"下载失败: 网络错误 - {str(e)}"
        }), 400
    except Exception as e:
        print(f"❌ 下载失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"下载失败: {str(e)}"
        }), 500

@api_bp.route('/api/download-patch-with-files', methods=['POST'])
def api_download_patch_with_files():
    """下载补丁包（包含模板JSON和用户上传/下载的素材文件）"""
    try:
        print("🔄 收到补丁包下载请求")
        
        # 获取请求数据
        project_data_str = request.form.get('project_data')
        project_dir = request.form.get('project_dir', '').strip()
        uploaded_files = request.files.getlist('assets')
        asset_files_info = request.form.getlist('asset_files')
        
        print(f"📝 请求参数:")
        print(f"   - project_data: {'存在' if project_data_str else '缺失'}")
        print(f"   - project_dir: '{project_dir}'")
        print(f"   - uploaded_files: {len(uploaded_files)} 个文件")
        print(f"   - asset_files_info: {len(asset_files_info)} 个信息")
        
        # 验证必需参数
        if not project_data_str:
            return jsonify({
                "success": False,
                "message": "缺少项目数据"
            }), 400
        
        if not project_dir:
            return jsonify({
                "success": False,
                "message": "请选择工程目录"
            }), 400
        
        try:
            project_data = json.loads(project_data_str)
        except json.JSONDecodeError as e:
            return jsonify({
                "success": False,
                "message": f"项目数据格式错误: {str(e)}"
            }), 400
        
        print(f"📂 用户选择的工程目录: {project_dir}")
        
        import zipfile
        import tempfile
        
        # 创建临时目录
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, f"project_patch_{int(time.time())}.zip")
        
        user_uploads_dir = ensure_user_uploads_dir()
        
        # 直接修改项目数据中的路径为绝对路径
        final_project_data = set_absolute_paths_in_project(project_data, project_dir)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 添加模板JSON文件
            json_content = json.dumps(final_project_data, indent=2, ensure_ascii=False)
            zipf.writestr("draft_content.json", json_content)
            print("✅ 添加 draft_content.json 到补丁包")
            
            # 收集所有素材文件
            collected_assets = []
            
            # 添加用户上传的文件
            for uploaded_file in uploaded_files:
                if uploaded_file.filename:
                    safe_filename = secure_filename(uploaded_file.filename)
                    file_data = uploaded_file.read()
                    zipf.writestr(f"assets/{safe_filename}", file_data)
                    
                    collected_assets.append({
                        "filename": safe_filename,
                        "size": len(file_data),
                        "source": "用户上传"
                    })
                    print(f"✅ 添加用户上传文件: {safe_filename}")
            
            # 添加网络下载的文件
            for asset_info_str in asset_files_info:
                try:
                    asset_info = json.loads(asset_info_str)
                    filename = asset_info['filename']
                    file_path = os.path.join(user_uploads_dir, filename)
                    
                    if os.path.exists(file_path):
                        zipf.write(file_path, f"assets/{filename}")
                        file_size = os.path.getsize(file_path)
                        collected_assets.append({
                            "filename": filename,
                            "size": file_size,
                            "source": "网络下载"
                        })
                        print(f"✅ 添加网络下载文件: {filename}")
                except json.JSONDecodeError:
                    print(f"❌ 解析资产文件信息失败: {asset_info_str}")
            
            # 添加系统默认素材文件
            tutorial_asset_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'readme_assets', 'tutorial')
            for asset_file in ['audio.mp3', 'video.mp4']:
                asset_path = os.path.join(tutorial_asset_dir, asset_file)
                if os.path.exists(asset_path):
                    standard_filename = f"default_{asset_file}"
                    zipf.write(asset_path, f"assets/{standard_filename}")
                    collected_assets.append({
                        "filename": standard_filename,
                        "size": os.path.getsize(asset_path),
                        "source": "系统默认"
                    })
                    print(f"✅ 添加系统默认文件: {standard_filename}")
            
            # 生成说明文件
            assets_info = "\n".join([
                f"- {asset['filename']} ({asset['size']/1024/1024:.2f} MB) - {asset['source']}" 
                for asset in collected_assets
            ]) if collected_assets else "无素材文件"
            
            readme_content = f"""# 剪映项目补丁包

## 🎯 使用方法
1. 解压补丁包到任意目录
2. **创建素材目录**: {project_dir}\\assets\\
3. **复制素材文件**: 将 assets 文件夹中的所有文件复制到上述目录
4. **导入项目**: 将 draft_content.json 复制到剪映草稿目录
5. **打开剪映**: 在剪映中打开项目即可

## 📂 路径配置
- **工程目录**: {project_dir}
- **素材目录**: {project_dir}\\assets\\
- **路径类型**: 绝对路径（已配置完成）

## 📋 包含文件
{assets_info}

## ⚠️ 重要提示
1. 必须将素材文件放在指定位置: {project_dir}\\assets\\
2. 不要更改素材文件名
3. 确保剪映有权限访问该目录

## 🕒 生成信息
- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 素材数量: {len(collected_assets)} 个文件
- 项目分辨率: 1920x1080
"""
            zipf.writestr("README.md", readme_content)
        
        print(f"✅ 补丁包生成成功，工程目录: {project_dir}")
        
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=f"jianying_project_{int(time.time())}.zip",
            mimetype='application/zip'
        )
        
    except Exception as e:
        print(f"❌ 生成补丁包失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"生成补丁包失败: {str(e)}"
        }), 500

def set_absolute_paths_in_project(project_data, project_dir):
    """将项目数据中的素材路径设置为绝对路径"""
    try:
        print(f"🔄 设置绝对路径: {project_dir}")
        
        # 统一路径分隔符（Windows风格）
        project_dir = os.path.normpath(project_dir)
        assets_dir = os.path.join(project_dir, 'assets')
        
        # 创建项目数据副本
        import copy
        result_data = copy.deepcopy(project_data)
        
        # 递归处理所有路径
        def process_paths(obj, parent_key=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, str):
                        # 检查是否是文件路径（包含文件扩展名）
                        if any(ext in value.lower() for ext in ['.mp3', '.mp4', '.wav', '.avi', '.mov', '.m4a', '.aac']):
                            # 提取文件名
                            filename = os.path.basename(value)
                            
                            # 如果文件名以 default_ 开头，保持原样
                            if filename.startswith('default_'):
                                new_path = os.path.join(assets_dir, filename)
                            else:
                                # 为用户文件添加前缀以避免冲突
                                if filename.startswith('audio_') or filename.startswith('video_'):
                                    new_path = os.path.join(assets_dir, filename)
                                else:
                                    # 根据文件扩展名添加前缀
                                    if any(ext in filename.lower() for ext in ['.mp3', '.wav', '.m4a', '.aac']):
                                        new_path = os.path.join(assets_dir, f"default_audio.mp3")
                                    else:
                                        new_path = os.path.join(assets_dir, f"default_video.mp4")
                            
                            # 转换为Windows路径格式
                            new_path = os.path.normpath(new_path)
                            obj[key] = new_path
                            print(f"✅ 路径更新: {parent_key}.{key} -> {new_path}")
                    
                    elif isinstance(value, (dict, list)):
                        process_paths(value, f"{parent_key}.{key}")
            
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    process_paths(item, f"{parent_key}[{i}]")
        
        # 执行路径处理
        process_paths(result_data)
        
        print("✅ 绝对路径设置完成")
        return result_data
        
    except Exception as e:
        print(f"❌ 设置绝对路径失败: {e}")
        import traceback
        traceback.print_exc()
        return project_data

# 注册路由
@api_bp.route('/', methods=['GET'])
def root_documentation():
    """根路径文档展示"""
    return show_documentation()

@api_bp.route('/api/health', methods=['GET'])
def api_health():
    """API健康检查"""
    return health_check()

@api_bp.route('/api/basic-project', methods=['POST'])
def api_basic_project():
    """基础项目创建"""
    return handle_basic_project()

@api_bp.route('/api/text-segment', methods=['POST'])
def api_text_segment():
    """文本片段处理"""
    return handle_text_segment()

@api_bp.route('/api/audio-segment', methods=['POST'])
def api_audio_segment():
    """音频片段处理"""
    return handle_audio_segment()

@api_bp.route('/api/video-segment', methods=['POST'])
def api_video_segment():
    """视频片段处理"""
    return handle_video_segment()

@api_bp.route('/api/comprehensive', methods=['POST'])
def api_comprehensive():
    """综合项目创建"""
    return handle_comprehensive()

@api_bp.route('/api/video-animation', methods=['POST'])
def api_video_animation():
    """视频动画处理"""
    return handle_video_animation()

@api_bp.route('/api/text-animation', methods=['POST'])
def api_text_animation():
    """文本动画处理"""
    return handle_text_animation()

@api_bp.route('/api/transition', methods=['POST'])
def api_transition():
    """转场效果处理"""
    return handle_transition()

@api_bp.route('/api/background-filling', methods=['POST'])
def api_background_filling():
    """背景填充处理"""
    return handle_background_filling()

@api_bp.route('/api/text-effects', methods=['POST'])
def api_text_effects():
    """文本特效处理"""
    return handle_text_effects()

@api_bp.route('/api/comprehensive-create', methods=['POST'])
def api_comprehensive_create():
    """综合创作项目"""
    return handle_comprehensive_create()

# 添加新的API端点来处理路径选择
@api_bp.route('/api/select-project-dir', methods=['POST'])
def api_select_project_dir():
    """选择项目目录并返回配置好的项目数据"""
    try:
        data = request.get_json() or {}
        project_data = data.get('project_data')
        project_dir = data.get('project_dir', '').strip()
        
        if not project_data:
            return jsonify({
                "success": False,
                "message": "缺少项目数据"
            }), 400
        
        if not project_dir:
            return jsonify({
                "success": False,
                "message": "请选择工程目录"
            }), 400
        
        print(f"📂 用户选择的工程目录: {project_dir}")
        
        # 直接修改项目数据中的路径为绝对路径
        final_project_data = set_absolute_paths_in_project(project_data, project_dir)
        
        return jsonify({
            "success": True,
            "message": "路径配置成功",
            "data": final_project_data,
            "project_dir": project_dir
        })
        
    except Exception as e:
        print(f"❌ 路径配置失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"路径配置失败: {str(e)}"
        }), 500

# 简化下载补丁包API
@api_bp.route('/api/download-patch-simple', methods=['POST'])
def api_download_patch_simple():
    """下载补丁包（简化版，已配置好路径）"""
    try:
        print("🔄 收到简化补丁包下载请求")
        
        data = request.get_json() or {}
        project_data = data.get('project_data')
        project_dir = data.get('project_dir', '').strip()
        
        if not project_data:
            return jsonify({
                "success": False,
                "message": "缺少项目数据"
            }), 400
        
        if not project_dir:
            return jsonify({
                "success": False,
                "message": "请选择工程目录"
            }), 400
        
        print(f"📂 用户工程目录: {project_dir}")
        
        import zipfile
        import tempfile
        
        # 创建临时目录
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, f"jianying_project_{int(time.time())}.zip")
        
        user_uploads_dir = ensure_user_uploads_dir()
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 添加模板JSON文件
            json_content = json.dumps(project_data, indent=2, ensure_ascii=False)
            zipf.writestr("draft_content.json", json_content)
            print("✅ 添加 draft_content.json 到补丁包")
            
            # 收集所有素材文件
            collected_assets = []
            
            # 添加用户下载的文件
            if os.path.exists(user_uploads_dir):
                for filename in os.listdir(user_uploads_dir):
                    file_path = os.path.join(user_uploads_dir, filename)
                    if os.path.isfile(file_path):
                        zipf.write(file_path, f"assets/{filename}")
                        file_size = os.path.getsize(file_path)
                        collected_assets.append({
                            "filename": filename,
                            "size": file_size,
                            "source": "用户下载"
                        })
                        print(f"✅ 添加用户文件: {filename}")
            
            # 添加系统默认素材文件
            tutorial_asset_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'readme_assets', 'tutorial')
            for asset_file in ['audio.mp3', 'video.mp4']:
                asset_path = os.path.join(tutorial_asset_dir, asset_file)
                if os.path.exists(asset_path):
                    standard_filename = f"default_{asset_file}"
                    zipf.write(asset_path, f"assets/{standard_filename}")
                    collected_assets.append({
                        "filename": standard_filename,
                        "size": os.path.getsize(asset_path),
                        "source": "系统默认"
                    })
                    print(f"✅ 添加系统默认文件: {standard_filename}")
            
            # 生成说明文件
            assets_info = "\n".join([
                f"- {asset['filename']} ({asset['size']/1024/1024:.2f} MB) - {asset['source']}" 
                for asset in collected_assets
            ]) if collected_assets else "无素材文件"
            
            readme_content = f"""# 剪映项目补丁包

## 🎯 使用方法
1. 解压补丁包到任意目录
2. **创建素材目录**: {project_dir}\\assets\\
3. **复制素材文件**: 将 assets 文件夹中的所有文件复制到上述目录
4. **导入项目**: 将 draft_content.json 复制到剪映草稿目录
5. **打开剪映**: 在剪映中打开项目即可

## 📂 路径配置
- **工程目录**: {project_dir}
- **素材目录**: {project_dir}\\assets\\
- **路径类型**: 绝对路径（已配置完成）

## 📋 包含文件
{assets_info}

## ⚠️ 重要提示
1. 必须将素材文件放在指定位置: {project_dir}\\assets\\
2. 不要更改素材文件名
3. 确保剪映有权限访问该目录

## 🕒 生成信息
- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 素材数量: {len(collected_assets)} 个文件
- 项目分辨率: 1920x1080
"""
            zipf.writestr("README.md", readme_content)
        
        print(f"✅ 补丁包生成成功，工程目录: {project_dir}")
        
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=f"jianying_project_{int(time.time())}.zip",
            mimetype='application/zip'
        )
        
    except Exception as e:
        print(f"❌ 生成补丁包失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"生成补丁包失败: {str(e)}"
        }), 500

# 注册新路由
@api_bp.route('/api/select-project-dir', methods=['POST'])
def api_select_project_dir_route():
    """选择项目目录路由"""
    return api_select_project_dir()

@api_bp.route('/api/download-patch-simple', methods=['POST'])
def api_download_patch_simple_route():
    """下载简化补丁包路由"""
    return api_download_patch_simple()

print("✅ API路由注册完成 - 使用pyJianYingDraft动态生成")
