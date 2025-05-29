from base_config import *
from pyJianYingDraft import trange

def test_text_segment():
    """测试文本片段添加"""
    print("测试：文本片段添加")
    
    # 创建剪映草稿
    script = create_basic_script()
    script.add_track(draft.Track_type.text)
    
    # 创建文本片段
    text_segment = draft.Text_segment(
        "这是一个文本测试",
        trange("0s", "3s"),
        font=draft.Font_type.文轩体,
        style=draft.Text_style(color=(1.0, 1.0, 0.0)),
        clip_settings=draft.Clip_settings(transform_y=-0.8)
    )
    
    # 添加到脚本
    script.add_segment(text_segment)
    
    # 保存草稿
    output_path = get_output_path("text_segment")
    script.dump(output_path)
    
    print(f"文本片段测试完成，输出文件：{output_path}")

if __name__ == "__main__":
    test_text_segment()
