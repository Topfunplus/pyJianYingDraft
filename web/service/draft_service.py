import os
import sys

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

# 设置日志记录器
logger = setup_logger('DraftService')


class DraftService:
    """剪映草稿服务类"""
    
    @staticmethod
    def create_basic_script():
        """创建基础脚本对象"""
        return draft.Script_file(1920, 1080)
    
    @staticmethod
    def create_basic_project():
        """创建基础项目"""
        logger.info("🎬 开始创建基础项目")
        
        script = DraftService.create_basic_script()
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
    def create_audio_segment(duration="5s", volume=0.6, fade_in="1s"):
        """创建音频片段"""
        logger.info(f"🎵 开始创建音频片段 - 时长:{duration}, 音量:{volume}, 淡入:{fade_in}")
        
        script = DraftService.create_basic_script()
        script.add_track(draft.Track_type.audio)
        
        audio_material = draft.Audio_material(get_asset_path('audio.mp3'))
        
        audio_segment = draft.Audio_segment(
            audio_material,
            trange("0s", duration),
            volume=volume
        )
        audio_segment.add_fade(fade_in, "0s")
        
        script.add_segment(audio_segment)
        
        output_path = get_output_path("audio_segment")
        script.dump(output_path)
        
        logger.info(f"✅ 音频片段创建成功: {output_path}")
        
        return {
            "success": True,
            "message": "音频片段创建成功",
            "output_path": output_path,
            "audio_info": {
                "duration": duration,
                "volume": volume,
                "fade_in": fade_in
            }
        }
    
    @staticmethod
    def create_video_segment(duration="4.2s"):
        """创建视频片段"""
        logger.info(f"🎬 开始创建视频片段 - 时长:{duration}")
        
        script = DraftService.create_basic_script()
        script.add_track(draft.Track_type.video)
        
        video_material = draft.Video_material(get_asset_path('video.mp4'))
        
        video_segment = draft.Video_segment(
            video_material,
            trange("0s", duration)
        )
        
        script.add_segment(video_segment)
        
        output_path = get_output_path("video_segment")
        script.dump(output_path)
        
        logger.info(f"✅ 视频片段创建成功: {output_path}")
        
        return {
            "success": True,
            "message": "视频片段创建成功",
            "output_path": output_path,
            "video_info": {
                "duration": duration
            }
        }
    
    @staticmethod
    def create_text_segment(text="这是一个文本测试", duration="3s", color=(1.0, 1.0, 0.0), font="文轩体"):
        """创建文本片段"""
        logger.info(f"📝 开始创建文本片段 - 文本:{text}, 时长:{duration}, 颜色:{color}")
        
        script = DraftService.create_basic_script()
        script.add_track(draft.Track_type.text)
        
        text_segment = draft.Text_segment(
            text,
            trange("0s", duration),
            font=getattr(draft.Font_type, font, draft.Font_type.文轩体),
            style=draft.Text_style(color=tuple(color)),
            clip_settings=draft.Clip_settings(transform_y=-0.8)
        )
        
        script.add_segment(text_segment)
        
        output_path = get_output_path("text_segment")
        script.dump(output_path)
        
        logger.info(f"✅ 文本片段创建成功: {output_path}")
        
        return {
            "success": True,
            "message": "文本片段创建成功",
            "output_path": output_path,
            "text_info": {
                "text": text,
                "duration": duration,
                "color": color,
                "font": font
            }
        }
    
    @staticmethod
    def create_video_animation(duration="4.2s", animation="斜切"):
        """创建视频动画"""
        logger.info(f"🎭 开始创建视频动画 - 时长:{duration}, 动画:{animation}")
        
        script = DraftService.create_basic_script()
        script.add_track(draft.Track_type.video)
        
        video_material = draft.Video_material(get_asset_path('video.mp4'))
        
        video_segment = draft.Video_segment(
            video_material,
            trange("0s", duration)
        )
        
        animation_type = getattr(Intro_type, animation, Intro_type.斜切)
        video_segment.add_animation(animation_type)
        
        script.add_segment(video_segment)
        
        output_path = get_output_path("video_animation")
        script.dump(output_path)
        
        logger.info(f"✅ 视频动画创建成功: {output_path}")
        
        return {
            "success": True,
            "message": "视频动画创建成功",
            "output_path": output_path,
            "animation_info": {
                "duration": duration,
                "animation": animation
            }
        }
    
    @staticmethod
    def create_text_animation(text="文本动画测试", duration="3s", animation="故障闪动", animation_duration="1s"):
        """创建文本动画"""
        logger.info(f"📝🎭 开始创建文本动画 - 文本:{text}, 时长:{duration}, 动画:{animation}")
        
        script = DraftService.create_basic_script()
        script.add_track(draft.Track_type.text)
        
        text_segment = draft.Text_segment(
            text,
            trange("0s", duration),
            font=draft.Font_type.文轩体,
            style=draft.Text_style(color=(1.0, 0.0, 0.0))
        )
        
        animation_type = getattr(draft.Text_outro, animation, draft.Text_outro.故障闪动)
        text_segment.add_animation(animation_type, duration=tim(animation_duration))
        
        script.add_segment(text_segment)
        
        output_path = get_output_path("text_animation")
        script.dump(output_path)
        
        logger.info(f"✅ 文本动画创建成功: {output_path}")
        
        return {
            "success": True,
            "message": "文本动画创建成功",
            "output_path": output_path,
            "animation_info": {
                "text": text,
                "duration": duration,
                "animation": animation,
                "animation_duration": animation_duration
            }
        }
    
    @staticmethod
    def create_transition(transition_type="信号故障", segment1_duration="2s", segment2_duration="2s"):
        """创建转场效果"""
        logger.info(f"🔄 开始创建转场效果 - 转场:{transition_type}")
        
        script = DraftService.create_basic_script()
        script.add_track(draft.Track_type.video)
        
        video_material = draft.Video_material(get_asset_path('video.mp4'))
        gif_material = draft.Video_material(get_asset_path('sticker.gif'))
        
        video_segment1 = draft.Video_segment(
            video_material,
            trange("0s", segment1_duration)
        )
        
        transition = getattr(Transition_type, transition_type, Transition_type.信号故障)
        video_segment1.add_transition(transition)
        
        video_segment2 = draft.Video_segment(
            gif_material,
            trange(video_segment1.end, segment2_duration)
        )
        
        script.add_segment(video_segment1).add_segment(video_segment2)
        
        output_path = get_output_path("transition")
        script.dump(output_path)
        
        logger.info(f"✅ 转场效果创建成功: {output_path}")
        
        return {
            "success": True,
            "message": "转场效果创建成功",
            "output_path": output_path,
            "transition_info": {
                "transition": transition_type,
                "segment1_duration": segment1_duration,
                "segment2_duration": segment2_duration
            }
        }
    
    @staticmethod
    def create_background_filling(duration="3s", blur_type="blur", blur_intensity=0.0625):
        """创建背景填充"""
        logger.info(f"🌈 开始创建背景填充 - 时长:{duration}, 模糊强度:{blur_intensity}")
        
        script = DraftService.create_basic_script()
        script.add_track(draft.Track_type.video)
        
        gif_material = draft.Video_material(get_asset_path('sticker.gif'))
        
        gif_segment = draft.Video_segment(
            gif_material,
            trange("0s", duration)
        )
        gif_segment.add_background_filling(blur_type, blur_intensity)
        
        script.add_segment(gif_segment)
        
        output_path = get_output_path("background_filling")
        script.dump(output_path)
        
        logger.info(f"✅ 背景填充创建成功: {output_path}")
        
        return {
            "success": True,
            "message": "背景填充创建成功",
            "output_path": output_path,
            "background_info": {
                "duration": duration,
                "blur_type": blur_type,
                "blur_intensity": blur_intensity
            }
        }
    
    @staticmethod
    def create_text_effects(text="文本特效测试", duration="4s", bubble_id="361595", 
                           bubble_resource_id="6742029398926430728", effect_id="7296357486490144036"):
        """创建文本特效"""
        logger.info(f"✨ 开始创建文本特效 - 文本:{text}, 时长:{duration}")
        
        script = DraftService.create_basic_script()
        script.add_track(draft.Track_type.text)
        
        text_segment = draft.Text_segment(
            text,
            trange("0s", duration),
            font=draft.Font_type.文轩体,
            style=draft.Text_style(color=(0.0, 1.0, 1.0))
        )
        
        text_segment.add_bubble(bubble_id, bubble_resource_id)
        text_segment.add_effect(effect_id)
        
        script.add_segment(text_segment)
        
        output_path = get_output_path("text_effects")
        script.dump(output_path)
        
        logger.info(f"✅ 文本特效创建成功: {output_path}")
        
        return {
            "success": True,
            "message": "文本特效创建成功",
            "output_path": output_path,
            "effect_info": {
                "text": text,
                "duration": duration,
                "bubble_id": bubble_id,
                "effect_id": effect_id
            }
        }
    
    @staticmethod
    def create_comprehensive():
        """创建综合项目"""
        logger.info("🎊 开始创建综合项目")
        
        script = DraftService.create_basic_script()
        script.add_track(draft.Track_type.audio).add_track(draft.Track_type.video).add_track(draft.Track_type.text)
        
        audio_material = draft.Audio_material(get_asset_path('audio.mp3'))
        video_material = draft.Video_material(get_asset_path('video.mp4'))
        gif_material = draft.Video_material(get_asset_path('sticker.gif'))
        
        # 音频片段
        audio_segment = draft.Audio_segment(
            audio_material,
            trange("0s", "5s"),
            volume=0.6
        )
        audio_segment.add_fade("1s", "0s")
        
        # 视频片段
        video_segment = draft.Video_segment(video_material, trange("0s", "4.2s"))
        video_segment.add_animation(Intro_type.斜切)
        
        # GIF片段
        gif_segment = draft.Video_segment(
            gif_material,
            trange(video_segment.end, gif_material.duration)
        )
        gif_segment.add_background_filling("blur", 0.0625)
        video_segment.add_transition(Transition_type.信号故障)
        
        # 文本片段
        text_segment = draft.Text_segment(
            "pyJianYingDraft综合测试",
            video_segment.target_timerange,
            font=draft.Font_type.文轩体,
            style=draft.Text_style(color=(1.0, 1.0, 0.0)),
            clip_settings=draft.Clip_settings(transform_y=-0.8)
        )
        text_segment.add_animation(draft.Text_outro.故障闪动, duration=tim("1s"))
        text_segment.add_bubble("361595", "6742029398926430728")
        text_segment.add_effect("7296357486490144036")
        
        script.add_segment(audio_segment).add_segment(video_segment).add_segment(gif_segment).add_segment(text_segment)
        
        output_path = get_output_path("comprehensive")
        script.dump(output_path)
        
        logger.info(f"✅ 综合项目创建成功: {output_path}")
        
        return {
            "success": True,
            "message": "综合项目创建成功",
            "output_path": output_path,
            "project_info": {
                "tracks": ["audio", "video", "text"],
                "segments": ["audio", "video", "gif", "text"],
                "effects": ["fade", "animation", "transition", "background_filling", "text_effects"]
            }
        }
