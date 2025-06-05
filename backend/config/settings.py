import os

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))


# 获取静态资源的路径
def get_asset_path(filename):
    assets_dir = os.path.join(PROJECT_ROOT, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    return os.path.join(assets_dir, filename)


# 获取文件的输出路径
def get_output_path(filename):
    outputs_dir = os.path.join(PROJECT_ROOT, "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    return os.path.join(outputs_dir, f"{filename}.json")
