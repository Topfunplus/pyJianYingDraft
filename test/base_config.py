import os
import sys

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pyJianYingDraft as draft

# 基础配置
TEST_OUTPUT_DIR = r"I:\测试文件夹\test_outputs"
TUTORIAL_ASSET_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'readme_assets', 'tutorial')

# 确保输出目录存在
os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

def create_basic_script():
    """创建基础脚本对象"""
    script = draft.Script_file(1920, 1080)
    return script

def get_asset_path(filename):
    """获取素材文件路径"""
    return os.path.join(TUTORIAL_ASSET_DIR, filename)

def get_output_path(test_name):
    """获取输出文件路径"""
    return os.path.join(TEST_OUTPUT_DIR, f"{test_name}_draft_content.json")
