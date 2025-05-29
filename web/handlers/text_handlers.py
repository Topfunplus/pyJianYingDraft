import os
import sys
from flask import request, jsonify

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pyJianYingDraft as draft
from pyJianYingDraft import trange, tim

from ..utils.common import (
    api_error_handler, create_and_save_script, create_basic_script, 
    get_asset_path, logger
)

@api_error_handler
def handle_text_segment():
    """处理文本片段API"""
    data = request.get_json() or {}
    text = data.get('text', '这是一个文本测试')
    duration = data.get('duration', '3s')
    color = data.get('color', [1.0, 1.0, 0.0])
    font = data.get('font', '文轩体')
    
    logger.info(f"📝 开始创建文本片段 - 文本:{text}, 时长:{duration}, 颜色:{color}")
    
    script = create_basic_script()
    script.add_track(draft.Track_type.text)
    
    text_segment = draft.Text_segment(
        text, trange("0s", duration),
        font=getattr(draft.Font_type, font, draft.Font_type.文轩体),
        style=draft.Text_style(color=tuple(color)),
        clip_settings=draft.Clip_settings(transform_y=-0.8)
    )
    script.add_segment(text_segment)
    
    return jsonify({
        "success": True,
        "message": "文本片段创建成功",
        "output_path": "/mock/text_segment",
        "text_info": {"text": text, "duration": duration, "color": color, "font": font}
    })

@api_error_handler
def handle_text_animation():
    """处理文本动画API"""
    data = request.get_json() or {}
    text = data.get('text', '文本动画测试')
    duration = data.get('duration', '3s')
    animation = data.get('animation', '故障闪动')
    animation_duration = data.get('animation_duration', '1s')
    
    logger.info(f"📝🎭 开始创建文本动画 - 文本:{text}, 时长:{duration}, 动画:{animation}")
    
    script = create_basic_script()
    script.add_track(draft.Track_type.text)
    
    text_segment = draft.Text_segment(
        text, trange("0s", duration),
        font=draft.Font_type.文轩体,
        style=draft.Text_style(color=(1.0, 0.0, 0.0))
    )
    
    animation_type = getattr(draft.Text_outro, animation, draft.Text_outro.故障闪动)
    text_segment.add_animation(animation_type, duration=tim(animation_duration))
    script.add_segment(text_segment)
    
    return jsonify({
        "success": True,
        "message": "文本动画创建成功",
        "output_path": "/mock/text_animation",
        "animation_info": {"text": text, "duration": duration, "animation": animation, "animation_duration": animation_duration}
    })

@api_error_handler
def handle_text_effects():
    """处理文本特效API"""
    data = request.get_json() or {}
    text = data.get('text', '文本特效测试')
    duration = data.get('duration', '4s')
    bubble_id = data.get('bubble_id', '361595')
    bubble_resource_id = data.get('bubble_resource_id', '6742029398926430728')
    effect_id = data.get('effect_id', '7296357486490144036')
    
    logger.info(f"✨ 开始创建文本特效 - 文本:{text}, 时长:{duration}")
    
    script = create_basic_script()
    script.add_track(draft.Track_type.text)
    
    text_segment = draft.Text_segment(
        text, trange("0s", duration),
        font=draft.Font_type.文轩体,
        style=draft.Text_style(color=(0.0, 1.0, 1.0))
    )
    
    text_segment.add_bubble(bubble_id, bubble_resource_id)
    text_segment.add_effect(effect_id)
    script.add_segment(text_segment)
    
    return jsonify({
        "success": True,
        "message": "文本特效创建成功",
        "output_path": "/mock/text_effects",
        "effect_info": {"text": text, "duration": duration, "bubble_id": bubble_id, "effect_id": effect_id}
    })
