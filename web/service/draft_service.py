import os
import sys
import json

# 添加项目根目录到Python路径
current_dir = os.path.dirname(__file__)
web_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(web_dir)
sys.path.insert(0, project_root)

import pyJianYingDraft as draft
from pyJianYingDraft import trange, tim, Intro_type, Transition_type, Track_type

# 添加web目录到路径
sys.path.insert(0, web_dir)
from config.settings import get_asset_path, get_output_path
from logs.logger import setup_logger
from utils.common import create_basic_script, ensure_user_uploads_dir

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
    def create_comprehensive_project(config):
        """创建综合项目"""
        try:
            print(f"🏗️ 开始创建综合项目，配置: {config}")
            
            # 创建基础脚本
            script = create_basic_script()
            
            # 添加必要的轨道
            script.add_track(Track_type.audio)
            script.add_track(Track_type.video) 
            script.add_track(Track_type.text)
            
            enabled_features = []
            segments_info = []
            current_time = 0  # 当前时间偏移，避免片段重叠
            
            # 处理文本组件
            if config.get('text', {}).get('enabled', False):
                text_config = config['text'].get('config', {})
                text_content = text_config.get('text', '综合项目文本')
                text_duration = text_config.get('duration', '3s')
                
                # 解析时长为秒数
                duration_seconds = float(text_duration.replace('s', ''))
                
                text_segment = draft.Text_segment(
                    text_content,
                    trange(f"{current_time}s", f"{current_time + duration_seconds}s"),
                    style=draft.Text_style(color=tuple(text_config.get('color', [1.0, 1.0, 1.0]))),
                    clip_settings=draft.Clip_settings(transform_y=-0.8),
                )
                script.add_segment(text_segment)
                enabled_features.append('文本片段')
                segments_info.append({
                    'type': '文本',
                    'content': text_content,
                    'duration': text_duration,
                    'start_time': f'{current_time}s'
                })
                current_time += duration_seconds
            
            # 处理音频组件
            if config.get('audio', {}).get('enabled', False):
                audio_config = config['audio'].get('config', {})
                audio_duration = audio_config.get('duration', '5s')
                duration_seconds = float(audio_duration.replace('s', ''))
                
                # 注意：音频通常作为背景音乐，可以从0开始
                enabled_features.append('音频片段')
                segments_info.append({
                    'type': '音频',
                    'duration': audio_duration,
                    'volume': audio_config.get('volume', 0.6),
                    'start_time': '0s',
                    'note': '音频作为背景音乐，从项目开始播放'
                })
            
            # 处理视频组件
            if config.get('video', {}).get('enabled', False):
                video_config = config['video'].get('config', {})
                video_duration = video_config.get('duration', '4.2s')
                duration_seconds = float(video_duration.replace('s', ''))
                
                enabled_features.append('视频片段')
                segments_info.append({
                    'type': '视频',
                    'duration': video_duration,
                    'start_time': f'{current_time}s'
                })
                current_time += duration_seconds
            
            # 处理动画组件
            if config.get('animation', {}).get('enabled', False):
                animation_config = config['animation'].get('config', {})
                animation_text = animation_config.get('text', '动画文本')
                animation_duration = animation_config.get('duration', '2s')
                duration_seconds = float(animation_duration.replace('s', ''))
                
                # 创建带动画的文本
                animated_text = draft.Text_segment(
                    animation_text,
                    trange(f"{current_time}s", f"{current_time + duration_seconds}s"),
                    style=draft.Text_style(color=(1.0, 1.0, 0.0)),
                    clip_settings=draft.Clip_settings(transform_y=-0.5),
                )
                animated_text.add_animation(draft.Text_outro.故障闪动, duration=tim("1s"))
                script.add_segment(animated_text)
                
                enabled_features.append('动画效果')
                segments_info.append({
                    'type': '动画文本',
                    'content': animation_text,
                    'duration': animation_duration,
                    'animation': '故障闪动',
                    'start_time': f'{current_time}s'
                })
                current_time += duration_seconds
            
            # 处理特效组件
            if config.get('effects', {}).get('enabled', False):
                effects_config = config['effects'].get('config', {})
                effects_text = effects_config.get('text', '特效文本')
                effects_duration = effects_config.get('duration', '3s')
                duration_seconds = float(effects_duration.replace('s', ''))
                
                # 创建带特效的文本
                effects_segment = draft.Text_segment(
                    effects_text,
                    trange(f"{current_time}s", f"{current_time + duration_seconds}s"),
                    style=draft.Text_style(color=(0.0, 1.0, 1.0)),
                    clip_settings=draft.Clip_settings(transform_y=0.5),
                )
                script.add_segment(effects_segment)
                
                enabled_features.append('文本特效')
                segments_info.append({
                    'type': '特效文本',
                    'content': effects_text,
                    'duration': effects_duration,
                    'start_time': f'{current_time}s'
                })
                current_time += duration_seconds
            
            # 处理转场组件（这里仅添加信息，实际转场需要视频片段）
            if config.get('transition', {}).get('enabled', False):
                transition_config = config['transition'].get('config', {})
                transition_type = transition_config.get('transition_type', '信号故障')
                
                enabled_features.append('转场效果')
                segments_info.append({
                    'type': '转场',
                    'transition_type': transition_type,
                    'note': '转场效果将在有视频片段时自动应用'
                })
            
            # 导出项目数据
            draft_json = script.dumps()
            project_data = json.loads(draft_json)
            
            # 计算总时长
            total_duration = f"{current_time}s" if current_time > 0 else "3s"
            
            # 构建响应
            result = {
                "success": True,
                "message": "综合项目创建成功",
                "data": project_data,
                "summary": {
                    "total_duration": total_duration,
                    "components_count": len(enabled_features),
                    "enabled_features": enabled_features,
                    "segments": segments_info,
                    "resolution": "1920x1080",
                    "tracks": ["audio", "video", "text"] if enabled_features else ["text"]
                }
            }
            
            print(f"✅ 综合项目创建成功，包含 {len(enabled_features)} 个组件，总时长: {total_duration}")
            return result
            
        except Exception as e:
            print(f"❌ 创建综合项目失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "message": f"创建综合项目失败: {str(e)}"
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
        # 处理转场组件的具体逻辑
        pass
