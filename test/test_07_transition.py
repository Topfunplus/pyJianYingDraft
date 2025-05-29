from base_config import *
from pyJianYingDraft import trange, Transition_type

def test_transition():
    """测试转场效果"""
    print("测试：转场效果")
    
    # 创建剪映草稿
    script = create_basic_script()
    script.add_track(draft.Track_type.video)
    
    # 读取视频素材
    video_material = draft.Video_material(get_asset_path('video.mp4'))
    gif_material = draft.Video_material(get_asset_path('sticker.gif'))
    
    # 创建第一个视频片段
    video_segment1 = draft.Video_segment(
        video_material,
        trange("0s", "2s")
    )
    video_segment1.add_transition(Transition_type.信号故障)
    
    # 创建第二个视频片段
    video_segment2 = draft.Video_segment(
        gif_material,
        trange(video_segment1.end, "2s")
    )
    
    # 添加到脚本
    script.add_segment(video_segment1).add_segment(video_segment2)
    
    # 保存草稿
    output_path = get_output_path("transition")
    script.dump(output_path)
    
    print(f"转场效果测试完成，输出文件：{output_path}")

if __name__ == "__main__":
    test_transition()
