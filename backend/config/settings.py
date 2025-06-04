import os

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_asset_path(filename):
    """获取素材文件路径"""
    assets_dir = os.path.join(PROJECT_ROOT, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    return os.path.join(assets_dir, filename)


def get_output_path(filename):
    """获取输出文件路径"""
    outputs_dir = os.path.join(PROJECT_ROOT, "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    return os.path.join(outputs_dir, f"{filename}.json")
