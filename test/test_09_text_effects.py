from base_config import *
from pyJianYingDraft import trange

def test_text_effects():
    """测试文本特效"""
    print("测试：文本特效")
    
    # 创建剪映草稿
    script = create_basic_script()
    script.add_track(draft.Track_type.text)
    
    # 创建文本片段
    text_segment = draft.Text_segment(
        "文本特效测试",
        trange("0s", "4s"),
        font=draft.Font_type.文轩体,
        style=draft.Text_style(color=(0.0, 1.0, 1.0))
    )
    
    # 添加气泡效果和花字效果
    text_segment.add_bubble("361595", "6742029398926430728")
    text_segment.add_effect("7296357486490144036")
    
    # 添加到脚本
    script.add_segment(text_segment)
    
    # 保存草稿
    output_path = get_output_path("text_effects")
    script.dump(output_path)
    
    print(f"文本特效测试完成，输出文件：{output_path}")

if __name__ == "__main__":
    test_text_effects()
