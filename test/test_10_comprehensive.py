from base_config import *
from pyJianYingDraft import trange, tim, Intro_type, Transition_type

def test_comprehensive():
    """综合测试所有功能"""
    print("测试：综合功能测试")
    
    # 创建剪映草稿
    script = create_basic_script()
    script.add_track(draft.Track_type.audio).add_track(draft.Track_type.video).add_track(draft.Track_type.text)
    
    # 读取素材
    audio_material = draft.Audio_material(get_asset_path('audio.mp3'))
    video_material = draft.Video_material(get_asset_path('video.mp4'))
    gif_material = draft.Video_material(get_asset_path('sticker.gif'))
    
    # 创建音频片段
    audio_segment = draft.Audio_segment(
        audio_material,
        trange("0s", "5s"),
        volume=0.6
    )
    audio_segment.add_fade("1s", "0s")
    
    # 创建视频片段
    video_segment = draft.Video_segment(video_material, trange("0s", "4.2s"))
    video_segment.add_animation(Intro_type.斜切)
    
    # 创建GIF片段
    gif_segment = draft.Video_segment(
        gif_material,
        trange(video_segment.end, gif_material.duration)
    )
    gif_segment.add_background_filling("blur", 0.0625)
    video_segment.add_transition(Transition_type.信号故障)
    
    # 创建文本片段
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
    
    # 添加所有片段到脚本
    script.add_segment(audio_segment).add_segment(video_segment).add_segment(gif_segment).add_segment(text_segment)
    
    # 保存草稿
    output_path = get_output_path("comprehensive")
    script.dump(output_path)
    
    print(f"综合功能测试完成，输出文件：{output_path}")

if __name__ == "__main__":
    test_comprehensive()
