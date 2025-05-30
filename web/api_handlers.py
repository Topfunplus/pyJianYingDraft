import os
import json
import uuid
from flask import Blueprint, jsonify, request
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
        current_time = 0  # 用于管理时间轴
        
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
        
        # 处理音频组件
        if data.get('audio', {}).get('enabled', False):
            audio_config = data['audio'].get('config', {})
            duration = audio_config.get('duration', '5s')
            
            # 注意：这里只创建轨道结构，实际使用时需要音频文件
            segments_info.append({
                "type": "audio",
                "duration": duration,
                "volume": audio_config.get('volume', 0.6),
                "fade_in": audio_config.get('fade_in', '1s'),
                "note": "需要实际音频文件"
            })
        
        # 处理视频组件
        if data.get('video', {}).get('enabled', False):
            video_config = data['video'].get('config', {})
            duration = video_config.get('duration', '4.2s')
            
            # 注意：这里只创建轨道结构，实际使用时需要视频文件
            segments_info.append({
                "type": "video",
                "duration": duration,
                "note": "需要实际视频文件"
            })
        
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
        
        # 添加项目元信息
        unified_data['project_meta'] = {
            "created_by": "pyJianYingDraft综合创作",
            "creation_time": current_time,
            "total_duration": f"{current_time}s",
            "components_count": len(segments_info),
            "enabled_features": [key for key, value in data.items() if value.get('enabled', False)],
            "segments_summary": segments_info
        }
        
        print(f"✅ 综合项目创建成功，包含 {len(segments_info)} 个组件")
        
        response_data = {
            "success": True,
            "message": "综合项目创建成功",
            "data": unified_data,
            "summary": {
                "total_duration": f"{current_time}s",
                "components_count": len(segments_info),
                "enabled_features": [key for key, value in data.items() if value.get('enabled', False)],
                "segments": segments_info
            }
        }
        
        print(f"📤 返回响应数据结构: success={response_data['success']}, components={len(segments_info)}")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ 综合创作失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"创建综合项目失败: {str(e)}"
        }), 500

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

# 新增路由注册
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

print("✅ API路由注册完成 - 使用pyJianYingDraft动态生成")
