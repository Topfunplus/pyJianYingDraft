from base_config import *
from pyJianYingDraft import trange

def test_background_filling():
    """测试背景填充"""
    print("测试：背景填充")
    
    # 创建剪映草稿
    script = create_basic_script()
    script.add_track(draft.Track_type.video)
    
    # 读取GIF素材
    gif_material = draft.Video_material(get_asset_path('sticker.gif'))
    
    # 创建视频片段并添加背景填充
    gif_segment = draft.Video_segment(
        gif_material,
        trange("0s", "3s")
    )
    gif_segment.add_background_filling("blur", 0.0625)
    
    # 添加到脚本
    script.add_segment(gif_segment)
    
    # 保存草稿
    output_path = get_output_path("background_filling")
    script.dump(output_path)
    
    print(f"背景填充测试完成，输出文件：{output_path}")

if __name__ == "__main__":
    test_background_filling()
