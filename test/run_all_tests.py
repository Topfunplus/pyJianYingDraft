import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

# 导入所有测试模块
from test_01_basic_project import test_basic_project
from test_02_audio_segment import test_audio_segment  
from test_03_video_segment import test_video_segment
from test_04_text_segment import test_text_segment
from test_05_video_animation import test_video_animation
from test_06_text_animation import test_text_animation
from test_07_transition import test_transition
from test_08_background_filling import test_background_filling
from test_09_text_effects import test_text_effects
from test_10_comprehensive import test_comprehensive

def run_all_tests():
    """运行所有测试"""
    tests = [
        ("基础项目创建", test_basic_project),
        ("音频片段", test_audio_segment),
        ("视频片段", test_video_segment),
        ("文本片段", test_text_segment),
        ("视频动画", test_video_animation),
        ("文本动画", test_text_animation),
        ("转场效果", test_transition),
        ("背景填充", test_background_filling),
        ("文本特效", test_text_effects),
        ("综合测试", test_comprehensive),
    ]
    
    print("=" * 50)
    print("开始运行所有单元测试")
    print("=" * 50)
    
    for test_name, test_func in tests:
        try:
            print(f"\n>>> 运行测试：{test_name}")
            test_func()
            print(f"✓ {test_name} 测试通过")
        except Exception as e:
            print(f"✗ {test_name} 测试失败：{e}")
    
    print("\n" + "=" * 50)
    print("所有测试运行完成")
    print("=" * 50)

if __name__ == "__main__":
    run_all_tests()
