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
def handle_audio_segment():
    """处理音频片段API"""
    data = request.get_json() or {}
    duration = data.get('duration', '5s')
    volume = data.get('volume', 0.6)
    fade_in = data.get('fade_in', '1s')
    
    logger.info(f"🎵 开始创建音频片段 - 时长:{duration}, 音量:{volume}, 淡入:{fade_in}")
    
    script = create_basic_script()
    script.add_track(draft.Track_type.audio)
    
    audio_material = draft.Audio_material(get_asset_path('audio.mp3'))
    audio_segment = draft.Audio_segment(audio_material, trange("0s", duration), volume=volume)
    audio_segment.add_fade(fade_in, "0s")
    script.add_segment(audio_segment)
    
    return jsonify({
        "success": True,
        "message": "音频片段创建成功",
        "output_path": "/mock/audio_segment",
        "audio_info": {"duration": duration, "volume": volume, "fade_in": fade_in}
    })

@api_error_handler
def handle_video_segment():
    """处理视频片段API"""
    data = request.get_json() or {}
    duration = data.get('duration', '4.2s')
    
    logger.info(f"🎬 开始创建视频片段 - 时长:{duration}")
    
    script = create_basic_script()
    script.add_track(draft.Track_type.video)
    
    video_material = draft.Video_material(get_asset_path('video.mp4'))
    video_segment = draft.Video_segment(video_material, trange("0s", duration))
    script.add_segment(video_segment)
    
    return jsonify({
        "success": True,
        "message": "视频片段创建成功",
        "output_path": "/mock/video_segment",
        "video_info": {"duration": duration}
    })

@api_error_handler
def handle_video_animation():
    """处理视频动画API"""
    data = request.get_json() or {}
    duration = data.get('duration', '4.2s')
    animation = data.get('animation', '斜切')
    
    logger.info(f"🎭 开始创建视频动画 - 时长:{duration}, 动画:{animation}")
    
    script = create_basic_script()
    script.add_track(draft.Track_type.video)
    
    video_material = draft.Video_material(get_asset_path('video.mp4'))
    video_segment = draft.Video_segment(video_material, trange("0s", duration))
    
    animation_type = getattr(Intro_type, animation, Intro_type.斜切)
    video_segment.add_animation(animation_type)
    script.add_segment(video_segment)
    
    return jsonify({
        "success": True,
        "message": "视频动画创建成功",
        "output_path": "/mock/video_animation",
        "animation_info": {"duration": duration, "animation": animation}
    })

@api_error_handler
def handle_transition():
    """处理转场效果API"""
    data = request.get_json() or {}
    transition_type = data.get('transition', '信号故障')
    segment1_duration = data.get('segment1_duration', '2s')
    segment2_duration = data.get('segment2_duration', '2s')
    
    logger.info(f"🔄 开始创建转场效果 - 转场:{transition_type}")
    
    script = create_basic_script()
    script.add_track(draft.Track_type.video)
    
    video_material = draft.Video_material(get_asset_path('video.mp4'))
    gif_material = draft.Video_material(get_asset_path('sticker.gif'))
    
    video_segment1 = draft.Video_segment(video_material, trange("0s", segment1_duration))
    transition = getattr(Transition_type, transition_type, Transition_type.信号故障)
    video_segment1.add_transition(transition)
    
    video_segment2 = draft.Video_segment(gif_material, trange(video_segment1.end, segment2_duration))
    
    script.add_segment(video_segment1).add_segment(video_segment2)
    
    return jsonify({
        "success": True,
        "message": "转场效果创建成功",
        "output_path": "/mock/transition",
        "transition_info": {"transition": transition_type, "segment1_duration": segment1_duration, "segment2_duration": segment2_duration}
    })

@api_error_handler
def handle_background_filling():
    """处理背景填充API"""
    data = request.get_json() or {}
    duration = data.get('duration', '3s')
    blur_type = data.get('blur_type', 'blur')
    blur_intensity = data.get('blur_intensity', 0.0625)
    
    logger.info(f"🌈 开始创建背景填充 - 时长:{duration}, 模糊强度:{blur_intensity}")
    
    script = create_basic_script()
    script.add_track(draft.Track_type.video)
    
    gif_material = draft.Video_material(get_asset_path('sticker.gif'))
    gif_segment = draft.Video_segment(gif_material, trange("0s", duration))
    gif_segment.add_background_filling(blur_type, blur_intensity)
    script.add_segment(gif_segment)
    
    return jsonify({
        "success": True,
        "message": "背景填充创建成功",
        "output_path": "/mock/background_filling",
        "background_info": {"duration": duration, "blur_type": blur_type, "blur_intensity": blur_intensity}
    })
