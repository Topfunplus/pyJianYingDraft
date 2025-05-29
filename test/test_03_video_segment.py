from base_config import *
from pyJianYingDraft import trange

def test_video_segment():
    """测试视频片段添加"""
    print("测试：视频片段添加")
    
    # 创建剪映草稿
    script = create_basic_script()
    script.add_track(draft.Track_type.video)
    
    # 读取视频素材
    video_material = draft.Video_material(get_asset_path('video.mp4'))
    
    # 创建视频片段
    video_segment = draft.Video_segment(
        video_material,
        trange("0s", "4.2s")
    )
    
    # 添加到脚本
    script.add_segment(video_segment)
    
    # 保存草稿
    output_path = get_output_path("video_segment")
    script.dump(output_path)
    
    print(f"视频片段测试完成，输出文件：{output_path}")

if __name__ == "__main__":
    test_video_segment()
