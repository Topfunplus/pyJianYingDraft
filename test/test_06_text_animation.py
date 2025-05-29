from base_config import *
from pyJianYingDraft import trange, tim

def test_text_animation():
    """测试文本动画效果"""
    print("测试：文本动画效果")
    
    # 创建剪映草稿
    script = create_basic_script()
    script.add_track(draft.Track_type.text)
    
    # 创建文本片段
    text_segment = draft.Text_segment(
        "文本动画测试",
        trange("0s", "3s"),
        font=draft.Font_type.文轩体,
        style=draft.Text_style(color=(1.0, 0.0, 0.0))
    )
    
    # 添加出场动画
    text_segment.add_animation(draft.Text_outro.故障闪动, duration=tim("1s"))
    
    # 添加到脚本
    script.add_segment(text_segment)
    
    # 保存草稿
    output_path = get_output_path("text_animation")
    script.dump(output_path)
    
    print(f"文本动画效果测试完成，输出文件：{output_path}")

if __name__ == "__main__":
    test_text_animation()
