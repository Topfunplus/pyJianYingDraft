import os
import time

# 基础配置
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
WEB_OUTPUT_DIR = r"C:\\Users\\zxsm\Desktop\\工作记录及模板\\剪影自动化脚本\\pyJianYingDraft\web_outputs"
TUTORIAL_ASSET_DIR = os.path.join(BASE_DIR, 'readme_assets', 'tutorial')

# 确保输出目录存在
os.makedirs(WEB_OUTPUT_DIR, exist_ok=True)

# Flask配置
class Config:
    SECRET_KEY = 'pyJianYingDraft_web_service_2024'
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    UPLOAD_FOLDER = os.path.join(WEB_OUTPUT_DIR, 'uploads')
    
    # 确保上传目录存在
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_asset_path(filename):
    """获取素材文件路径"""
    return os.path.join(TUTORIAL_ASSET_DIR, filename)

def get_output_path(test_name):
    """获取输出文件路径"""
    timestamp = int(time.time())
    return os.path.join(WEB_OUTPUT_DIR, f"{test_name}_{timestamp}_draft_content.json")
