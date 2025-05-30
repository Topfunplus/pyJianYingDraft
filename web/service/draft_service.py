import os
import sys
import json

# 添加项目根目录到Python路径
current_dir = os.path.dirname(__file__)
web_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(web_dir)
sys.path.insert(0, project_root)

import pyJianYingDraft as draft
from pyJianYingDraft import trange, tim, Intro_type, Transition_type

# 添加web目录到路径
sys.path.insert(0, web_dir)
from config.settings import get_asset_path, get_output_path
from logs.logger import setup_logger
from utils.common import create_basic_script, ensure_user_uploads_dir, replace_paths_with_placeholders

# 设置日志记录器
logger = setup_logger('DraftService')

class DraftService:
    """剪映草稿服务类"""
    
    @staticmethod
    def create_basic_project():
        """创建基础项目"""
        logger.info("🎬 开始创建基础项目")
        
        script = create_basic_script()
        script.add_track(draft.Track_type.video)
        
        output_path = get_output_path("basic_project")
        script.dump(output_path)
        
        logger.info(f"✅ 基础项目创建成功: {output_path}")
        
        return {
            "success": True,
            "message": "基础项目创建成功",
            "output_path": output_path,
            "project_info": {
                "width": 1920,
                "height": 1080,
                "tracks": ["video"]
            }
        }
    
    @staticmethod
    def _create_segment_with_material(material_type, file_key, duration, **kwargs):
        """创建带素材的片段的通用方法"""
        script = create_basic_script()
        
        if material_type == "audio":
            script.add_track(draft.Track_type.audio)
            material = draft.Audio_material(get_asset_path(file_key))
            segment = draft.Audio_segment(
                material,
                trange("0s", duration),
                volume=kwargs.get('volume', 0.6)
            )
            if kwargs.get('fade_in', '0s') != '0s':
                segment.add_fade(kwargs['fade_in'], "0s")
        else:  # video
            script.add_track(draft.Track_type.video)
            material = draft.Video_material(get_asset_path(file_key))
            segment = draft.Video_segment(material, trange("0s", duration))
        
        script.add_segment(segment)
        return script
    
    @staticmethod
    def create_audio_segment(duration="5s", volume=0.6, fade_in="1s"):
        """创建音频片段"""
        logger.info(f"🎵 开始创建音频片段 - 时长:{duration}, 音量:{volume}, 淡入:{fade_in}")
        
        script = DraftService._create_segment_with_material(
            "audio", 'audio.mp3', duration, volume=volume, fade_in=fade_in
        )
        
        output_path = get_output_path("audio_segment")
        script.dump(output_path)
        
        logger.info(f"✅ 音频片段创建成功: {output_path}")
        
        return {
            "success": True,
            "message": "音频片段创建成功",
            "output_path": output_path,
            "audio_info": {"duration": duration, "volume": volume, "fade_in": fade_in}
        }
    
    @staticmethod
    def create_video_segment(duration="4.2s"):
        """创建视频片段"""
        logger.info(f"🎬 开始创建视频片段 - 时长:{duration}")
        
        script = DraftService._create_segment_with_material("video", 'video.mp4', duration)
        
        output_path = get_output_path("video_segment")
        script.dump(output_path)
        
        logger.info(f"✅ 视频片段创建成功: {output_path}")
        
        return {
            "success": True,
            "message": "视频片段创建成功",
            "output_path": output_path,
            "video_info": {"duration": duration}
        }
    
    @staticmethod
    def _create_text_segment_base(text, duration, color=(1.0, 1.0, 0.0), font="文轩体", transform_y=-0.8):
        """创建文本片段的基础方法"""
        script = create_basic_script()
        script.add_track(draft.Track_type.text)
        
        text_segment = draft.Text_segment(
            text,
            trange("0s", duration),
            font=getattr(draft.Font_type, font, draft.Font_type.文轩体),
            style=draft.Text_style(color=tuple(color)),
            clip_settings=draft.Clip_settings(transform_y=transform_y)
        )
        
        return script, text_segment
    
    @staticmethod
    def create_text_segment(text="这是一个文本测试", duration="3s", color=(1.0, 1.0, 0.0), font="文轩体"):
        """创建文本片段"""
        logger.info(f"📝 开始创建文本片段 - 文本:{text}, 时长:{duration}, 颜色:{color}")
        
        script, text_segment = DraftService._create_text_segment_base(text, duration, color, font)
        script.add_segment(text_segment)
        
        output_path = get_output_path("text_segment")
        script.dump(output_path)
        
        logger.info(f"✅ 文本片段创建成功: {output_path}")
        
        return {
            "success": True,
            "message": "文本片段创建成功",
            "output_path": output_path,
            "text_info": {"text": text, "duration": duration, "color": color, "font": font}
        }
    
    @staticmethod
    def create_comprehensive_project(components_config):
        """创建综合项目 - 统一入口"""
        logger.info("🎊 开始创建综合项目")
        
        script = create_basic_script()
        script.add_track(draft.Track_type.audio).add_track(draft.Track_type.video).add_track(draft.Track_type.text)
        
        segments_info = []
        required_assets = []
        current_time = 0
        
        # 处理各种组件...
        tutorial_asset_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'readme_assets', 'tutorial')
        user_uploads_dir = ensure_user_uploads_dir()
        
        # 如果没有任何组件，创建默认内容
        has_any_component = any(components_config.get(comp_type, {}).get('enabled', False) 
                               for comp_type in ['audio', 'video', 'text', 'animation', 'effects', 'transition'])
        
        if not has_any_component:
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
            current_time = 3
        else:
            # 处理启用的组件
            component_handlers = {
                'text': DraftService._handle_text_component,
                'audio': DraftService._handle_audio_component,
                'video': DraftService._handle_video_component,
                'animation': DraftService._handle_animation_component,
                'effects': DraftService._handle_effects_component,
            }
            
            for component_type, handler in component_handlers.items():
                if components_config.get(component_type, {}).get('enabled', False):
                    try:
                        component_result = handler(
                            components_config[component_type].get('config', {}),
                            script, current_time, tutorial_asset_dir, user_uploads_dir
                        )
                        if component_result:
                            segments_info.extend(component_result.get('segments', []))
                            required_assets.extend(component_result.get('assets', []))
                            current_time = component_result.get('current_time', current_time)
                    except Exception as e:
                        logger.error(f"❌ 处理组件 {component_type} 失败: {e}")
        
        # 导出并处理路径
        draft_json = script.dumps()
        unified_data = json.loads(draft_json)
        unified_data = replace_paths_with_placeholders(unified_data, required_assets)
        
        # 添加项目元信息
        unified_data['project_meta'] = {
            "created_by": "pyJianYingDraft综合创作",
            "creation_time": current_time,
            "total_duration": f"{current_time}s",
            "components_count": len(segments_info),
            "enabled_features": [key for key, value in components_config.items() if value.get('enabled', False)],
            "segments_summary": segments_info,
            "required_assets": required_assets,
            "supports_user_assets": True,
            "supports_url_download": True,
            "user_uploads_dir": user_uploads_dir
        }
        
        logger.info(f"✅ 综合项目创建成功，包含 {len(segments_info)} 个组件")
        
        return {
            "success": True,
            "message": "综合项目创建成功",
            "data": unified_data,
            "summary": {
                "total_duration": f"{current_time}s",
                "components_count": len(segments_info),
                "enabled_features": [key for key, value in components_config.items() if value.get('enabled', False)],
                "segments": segments_info,
                "assets": required_assets
            }
        }
    
    # 私有方法处理各种组件类型
    @staticmethod
    def _handle_text_component(config, script, current_time, tutorial_dir, user_dir):
        """处理文本组件"""
        try:
            duration = config.get('duration', '3s')
            text_segment = draft.Text_segment(
                config.get('text', '综合创作文本'),
                trange(f"{current_time}s", duration),
                style=draft.Text_style(color=tuple(config.get('color', [1.0, 1.0, 1.0]))),
                clip_settings=draft.Clip_settings(transform_y=-0.8)
            )
            
            font = config.get('font', '文轩体')
            if hasattr(draft.Font_type, font):
                text_segment.font = getattr(draft.Font_type, font)
            
            script.add_segment(text_segment)
            
            return {
                "segments": [{
                    "type": "text",
                    "content": config.get('text', '综合创作文本'),
                    "duration": duration,
                    "start_time": f"{current_time}s"
                }],
                "assets": [],
                "current_time": current_time + float(duration.replace('s', ''))
            }
        except Exception as e:
            logger.error(f"❌ 处理文本组件失败: {e}")
            return None
    
    @staticmethod
    def _handle_audio_component(config, script, current_time, tutorial_dir, user_dir):
        """处理音频组件"""
        # 简化实现，实际需要更完整的音频处理逻辑
        return {
            "segments": [{"type": "audio", "note": "音频组件处理中"}],
            "assets": [],
            "current_time": current_time
        }
    
    @staticmethod
    def _handle_video_component(config, script, current_time, tutorial_dir, user_dir):
        """处理视频组件"""
        # 简化实现，实际需要更完整的视频处理逻辑
        return {
            "segments": [{"type": "video", "note": "视频组件处理中"}],
            "assets": [],
            "current_time": current_time
        }
    
    @staticmethod
    def _handle_animation_component(config, script, current_time, tutorial_dir, user_dir):
        """处理动画组件"""
        # 简化实现，实际需要更完整的动画处理逻辑
        return {
            "segments": [{"type": "animation", "note": "动画组件处理中"}],
            "assets": [],
            "current_time": current_time
        }
    
    @staticmethod
    def _handle_effects_component(config, script, current_time, tutorial_dir, user_dir):
        """处理特效组件"""
        # 简化实现，实际需要更完整的特效处理逻辑
        return {
            "segments": [{"type": "effects", "note": "特效组件处理中"}],
            "assets": [],
            "current_time": current_time
        }
    
    @staticmethod
    def _handle_transition_component(config, script, current_time, tutorial_dir, user_dir):
        # 处理转场组件的具体逻辑...
        pass
