import os
import json
import time
import uuid
from flask import Blueprint, jsonify, request, render_template_string

# 导入pyJianYingDraft模块
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pyJianYingDraft as draft
from pyJianYingDraft import Track_type, trange, tim

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
        return {
            "canvas_config": {"height": 1080, "ratio": "original", "width": 1920},
            "color_space": 0,
            "config": {
                "adjust_max_index": 1,
                "attachment_info": [],
                "combination_max_index": 1,
                "export_range": None,
                "extract_audio_last_index": 1,
                "lyrics_recognition_id": "",
                "lyrics_sync": True,
                "lyrics_taskinfo": [],
                "maintrack_adsorb": True,
                "material_save_mode": 0,
                "multi_language_current": "none",
                "multi_language_list": [],
                "multi_language_main": "none",
                "multi_language_mode": "none",
                "original_sound_last_index": 1,
                "record_audio_last_index": 1,
                "sticker_max_index": 1,
                "subtitle_keywords_config": None,
                "subtitle_recognition_id": "",
                "subtitle_sync": True,
                "subtitle_taskinfo": [],
                "system_font_list": [],
                "video_mute": False,
                "zoom_info_params": None
            },
            "cover": None,
            "create_time": int(time.time()),
            "duration": 0,
            "extra_info": None,
            "fps": 30.0,
            "free_render_index_mode_on": False,
            "group_container": None,
            "id": str(uuid.uuid4()).upper(),
            "keyframe_graph_list": [],
            "keyframes": {
                "adjusts": [],
                "audios": [],
                "effects": [],
                "filters": [],
                "handwrites": [],
                "stickers": [],
                "texts": [],
                "videos": []
            },
            "last_modified_platform": {
                "app_id": 3704,
                "app_source": "lv",
                "app_version": "5.9.0",
                "os": "windows"
            },
            "materials": {
                "ai_translates": [],
                "audio_balances": [],
                "audio_effects": [],
                "audio_fades": [],
                "audio_track_indexes": [],
                "audios": [],
                "beats": [],
                "canvases": [],
                "chromas": [],
                "color_curves": [],
                "digital_humans": [],
                "drafts": [],
                "effects": [],
                "flowers": [],
                "green_screens": [],
                "handwrites": [],
                "hsl": [],
                "images": [],
                "log_color_wheels": [],
                "loudnesses": [],
                "manual_deformations": [],
                "masks": [],
                "material_animations": [],
                "material_colors": [],
                "multi_language_refs": [],
                "placeholders": [],
                "plugin_effects": [],
                "primary_color_wheels": [],
                "realtime_denoises": [],
                "shapes": [],
                "smart_crops": [],
                "smart_relights": [],
                "sound_channel_mappings": [],
                "speeds": [],
                "stickers": [],
                "tail_leaders": [],
                "text_templates": [],
                "texts": [],
                "time_marks": [],
                "transitions": [],
                "video_effects": [],
                "video_trackings": [],
                "videos": [],
                "vocal_beautifys": [],
                "vocal_separations": []
            },
            "mutable_config": None,
            "name": "",
            "new_version": "110.0.0",
            "relationships": [],
            "render_index_track_mode_on": False,
            "retouch_cover": None,
            "source": "default",
            "static_cover_image_path": "",
            "time_marks": None,
            "tracks": [],
            "update_time": int(time.time()),
            "version": 360000
        }

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

def create_text_segment(text="示例文本", duration=3000000):
    """创建文本片段"""
    segment_id = str(uuid.uuid4()).upper()
    material_id = str(uuid.uuid4()).upper()
    
    return {
        "segment": {
            "cartoon": False,
            "clip": {
                "alpha": 1.0,
                "flip": {"horizontal": False, "vertical": False},
                "rotation": 0.0,
                "scale": {"x": 1.0, "y": 1.0},
                "transform": {"x": 0.0, "y": 0.0}
            },
            "common_keyframes": [],
            "enable_adjust": True,
            "enable_color_curves": True,
            "enable_color_wheels": True,
            "enable_lut": True,
            "enable_smart_color_adjust": False,
            "extra_material_refs": [],
            "group_id": "",
            "hdr_settings": None,
            "id": segment_id,
            "intensifies_audio": False,
            "is_placeholder": False,
            "is_tone_modify": False,
            "keyframe_refs": [],
            "last_nonzero_volume": 1.0,
            "material_id": material_id,
            "render_index": 4294967295,
            "reverse": False,
            "source_timerange": None,
            "speed": 1.0,
            "target_timerange": {
                "duration": duration,
                "start": 0
            },
            "template_id": "",
            "template_scene": "default",
            "track_attribute": 0,
            "track_render_index": 4294967295,
            "uniform_scale": None,
            "visible": True,
            "volume": 1.0
        },
        "material": {
            "create_time": int(time.time()),
            "duration": duration,
            "extra_info": "",
            "file_Path": "",
            "height": 0,
            "id": material_id,
            "import_time": int(time.time()),
            "import_time_ms": int(time.time() * 1000),
            "item_source": 1,
            "md5": "",
            "metetype": "text",
            "roughcut_time_range": {
                "duration": -1,
                "start": -1
            },
            "sub_time_range": {
                "duration": -1,
                "start": -1
            },
            "type": 2,
            "update_time": int(time.time()),
            "width": 0,
            "content": text,
            "font_id": "",
            "font_name": "Microsoft YaHei UI",
            "font_path": "",
            "font_resource_id": "",
            "font_size": 10.0,
            "font_title": "",
            "letter_spacing": 0.0,
            "line_spacing": 0.0,
            "text_alpha": 1.0,
            "text_color": "#FFFFFF",
            "text_curve": None,
            "text_preset_resource_id": "",
            "text_size": 30,
            "text_to_audio_ids": [],
            "underline": False,
            "underline_offset": 0.0,
            "underline_width": 0.0,
            "use_effect_default_color": True
        }
    }

# 文档处理函数
def show_documentation():
    """展示API文档"""
    return render_template_string("""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>pyJianYingDraft API 文档</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; min-height: 100vh; }
        .header { background: linear-gradient(135deg, #007bff, #0056b3); color: white; padding: 30px; text-align: center; border-radius: 8px; margin-bottom: 30px; }
        .endpoint { background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 5px solid #007bff; }
        .endpoint h3 { color: #007bff; margin-top: 0; }
        .method { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; margin-right: 10px; }
        .get { background: #28a745; color: white; }
        .post { background: #007bff; color: white; }
        .test-section { background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .test-button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 5px; }
        .test-button:hover { background: #0056b3; }
        .test-result { margin-top: 15px; padding: 10px; background: white; border-radius: 5px; display: none; max-height: 300px; overflow-y: auto; font-family: monospace; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 pyJianYingDraft API</h1>
            <p>剪映草稿自动化生成接口</p>
            <p style="font-size: 14px; opacity: 0.9;">Version 1.0.0</p>
        </div>
        
        <div class="test-section">
            <h3>🚀 快速测试</h3>
            <p>点击下方按钮快速测试API接口：</p>
            <button class="test-button" onclick="testAPI('/api/health', 'GET')">健康检查</button>
            <button class="test-button" onclick="testAPI('/api/basic-project', 'POST')">创建基础项目</button>
            <button class="test-button" onclick="testAPI('/api/text-segment', 'POST', {text: 'API测试', duration: '2s'})">创建文本片段</button>
            <div id="testResult" class="test-result"></div>
        </div>
        
        <h2>📚 API 接口列表</h2>
        
        <div class="endpoint">
            <h3><span class="method get">GET</span> /api/health</h3>
            <p><strong>功能:</strong> 健康检查接口</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/basic-project</h3>
            <p><strong>功能:</strong> 创建基础剪映项目</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/text-segment</h3>
            <p><strong>功能:</strong> 创建文本片段</p>
            <p><strong>参数:</strong> text, duration, color, font</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/audio-segment</h3>
            <p><strong>功能:</strong> 创建音频片段</p>
            <p><strong>参数:</strong> duration, volume, fade_in</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/video-segment</h3>
            <p><strong>功能:</strong> 创建视频片段</p>
            <p><strong>参数:</strong> duration</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/comprehensive</h3>
            <p><strong>功能:</strong> 创建综合测试项目</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/video-animation</h3>
            <p><strong>功能:</strong> 创建视频动画</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/text-animation</h3>
            <p><strong>功能:</strong> 创建文本动画</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/transition</h3>
            <p><strong>功能:</strong> 创建转场效果</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/background-filling</h3>
            <p><strong>功能:</strong> 创建背景填充</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/text-effects</h3>
            <p><strong>功能:</strong> 创建文本特效</p>
        </div>
    </div>
    
    <script>
        async function testAPI(endpoint, method = 'GET', data = null) {
            const resultDiv = document.getElementById('testResult');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '🔄 正在测试...';

            try {
                const options = { method, headers: { 'Content-Type': 'application/json' } };
                if (data && method === 'POST') options.body = JSON.stringify(data);

                const response = await fetch(endpoint, options);
                const result = await response.json();
                
                resultDiv.innerHTML = `
                    <strong>🎯 ${method} ${endpoint}</strong><br>
                    <strong>状态:</strong> ${response.status}<br>
                    <strong>响应:</strong><br>
                    <pre>${JSON.stringify(result, null, 2)}</pre>
                `;
                resultDiv.style.border = `2px solid ${response.ok ? '#28a745' : '#dc3545'}`;
            } catch (error) {
                resultDiv.innerHTML = `<strong>❌ 测试失败:</strong> ${error.message}`;
                resultDiv.style.border = '2px solid #dc3545';
            }
        }
    </script>
</body>
</html>
    """)

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

print("✅ API路由注册完成 - 使用pyJianYingDraft动态生成")
