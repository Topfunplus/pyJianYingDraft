from base_config import *
from pyJianYingDraft import trange

def test_audio_segment():
    """测试音频片段添加"""
    print("测试：音频片段添加")
    
    # 创建剪映草稿
    script = create_basic_script()
    script.add_track(draft.Track_type.audio)
    
    # 读取音频素材
    audio_material = draft.Audio_material(get_asset_path('audio.mp3'))
    
    # 创建音频片段
    audio_segment = draft.Audio_segment(
        audio_material,
        trange("0s", "5s"),
        volume=0.6
    )
    
    # 添加淡入效果
    audio_segment.add_fade("1s", "0s")
    
    # 添加到脚本
    script.add_segment(audio_segment)
    
    # 保存草稿
    output_path = get_output_path("audio_segment")
    script.dump(output_path)
    
    print(f"音频片段测试完成，输出文件：{output_path}")

if __name__ == "__main__":
    test_audio_segment()
