import os
import sys
from flask import request, jsonify

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pyJianYingDraft as draft
from pyJianYingDraft import trange, tim, Intro_type, Transition_type

from ..utils.common import (
    api_error_handler, create_and_save_script, create_basic_script, 
    get_asset_path, logger
)

@api_error_handler
def handle_basic_project():
    """处理基础项目创建API"""
    logger.info("🎬 开始创建基础项目")
    
    script = create_basic_script()
    script.add_track(draft.Track_type.video)
    
    return create_and_save_script(
        script, "basic_project", "基础项目创建成功",
        {"project_info": {"width": 1920, "height": 1080, "tracks": ["video"]}}
    )

@api_error_handler
def handle_comprehensive():
    """处理综合测试API"""
    logger.info("🎊 开始创建综合项目")
    
    script = create_basic_script()
    script.add_track(draft.Track_type.audio).add_track(draft.Track_type.video).add_track(draft.Track_type.text)
    
    # 素材
    audio_material = draft.Audio_material(get_asset_path('audio.mp3'))
    video_material = draft.Video_material(get_asset_path('video.mp4'))
    gif_material = draft.Video_material(get_asset_path('sticker.gif'))
    
    # 音频片段
    audio_segment = draft.Audio_segment(audio_material, trange("0s", "5s"), volume=0.6)
    audio_segment.add_fade("1s", "0s")
    
    # 视频片段
    video_segment = draft.Video_segment(video_material, trange("0s", "4.2s"))
    video_segment.add_animation(Intro_type.斜切)
    
    # GIF片段
    gif_segment = draft.Video_segment(gif_material, trange(video_segment.end, gif_material.duration))
    gif_segment.add_background_filling("blur", 0.0625)
    video_segment.add_transition(Transition_type.信号故障)
    
    # 文本片段
    text_segment = draft.Text_segment(
        "pyJianYingDraft综合测试", video_segment.target_timerange,
        font=draft.Font_type.文轩体,
        style=draft.Text_style(color=(1.0, 1.0, 0.0)),
        clip_settings=draft.Clip_settings(transform_y=-0.8)
    )
    text_segment.add_animation(draft.Text_outro.故障闪动, duration=tim("1s"))
    text_segment.add_bubble("361595", "6742029398926430728")
    text_segment.add_effect("7296357486490144036")
    
    script.add_segment(audio_segment).add_segment(video_segment).add_segment(gif_segment).add_segment(text_segment)
    
    return create_and_save_script(
        script, "comprehensive", "综合项目创建成功",
        {"project_info": {
            "tracks": ["audio", "video", "text"],
            "segments": ["audio", "video", "gif", "text"],
            "effects": ["fade", "animation", "transition", "background_filling", "text_effects"]
        }}
    )
