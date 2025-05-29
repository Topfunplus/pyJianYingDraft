from base_config import *
from pyJianYingDraft import trange, Intro_type

def test_video_animation():
    """测试视频动画效果"""
    print("测试：视频动画效果")
    
    # 创建剪映草稿
    script = create_basic_script()
    script.add_track(draft.Track_type.video)
    
    # 读取视频素材
    video_material = draft.Video_material(get_asset_path('video.mp4'))
    
    # 创建视频片段并添加入场动画
    video_segment = draft.Video_segment(
        video_material,
        trange("0s", "4.2s")
    )
    video_segment.add_animation(Intro_type.斜切)
    
    # 添加到脚本
    script.add_segment(video_segment)
    
    # 保存草稿
    output_path = get_output_path("video_animation")
    script.dump(output_path)
    
    print(f"视频动画效果测试完成，输出文件：{output_path}")

if __name__ == "__main__":
    test_video_animation()
