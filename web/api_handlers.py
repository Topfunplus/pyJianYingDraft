from utils.common import (
    api_error_handler,
    create_basic_script,
    ensure_user_uploads_dir,
    get_file_extension_from_url,
    generate_unique_filename,
    get_request_data,
    create_success_response,
    create_error_response,
    set_absolute_paths_in_project,
)
from service.draft_service import DraftService
from pyJianYingDraft import Track_type, trange, tim
import pyJianYingDraft as draft
import os
import json
import time
import requests
from datetime import datetime
from flask import Blueprint, jsonify, request
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
web_dir = os.path.dirname(__file__)
sys.path.insert(0, web_dir)


# 使用绝对导入
try:
    from template.template import default_template
except ImportError:
    # 备用默认模板
    default_template = {
        "canvas_config": {"height": 1080, "width": 1920},
        "tracks": [],
        "materials": {"videos": [], "audios": [], "texts": []},
        "version": "1.0.0",
    }

# 创建Blueprint
api_bp = Blueprint("api", __name__)


# 移除API测试相关路由
@api_bp.route("/api/health", methods=["GET"])
def api_health():
    """API健康检查"""
    return jsonify(
        {
            "success": True,
            "message": "API服务正常运行",
            "version": "1.3.1",
            "status": "running",
        }
    )


# 移除文档展示路由，改为简单的欢迎页面
@api_bp.route("/", methods=["GET"])
def root_welcome():
    """根路径欢迎页面"""
    return jsonify(
        {"success": True, "message": "欢迎使用剪映草稿生成服务", "version": "1.3.1"}
    )


@api_bp.route("/api/basic-project", methods=["POST"])
@api_error_handler
def api_basic_project():
    """基础项目创建"""
    result = DraftService.create_basic_project()
    draft_json = create_basic_script().dumps()
    result["data"] = json.loads(draft_json)
    return jsonify(result)


@api_bp.route("/api/text-segment", methods=["POST"])
@api_error_handler
def api_text_segment():
    """文本片段处理"""
    data = get_request_data()
    result = DraftService.create_text_segment(
        text=data.get("text", "这是一个文本测试"),
        duration=data.get("duration", "3s"),
        color=data.get("color", [1.0, 1.0, 1.0]),
        font=data.get("font", "文轩体"),
    )
    # 添加数据到结果
    script = create_basic_script()
    script.add_track(Track_type.text)
    text_segment = draft.Text_segment(
        data.get("text", "这是一个文本测试"),
        trange("0s", data.get("duration", "3s")),
        style=draft.Text_style(color=tuple(data.get("color", [1.0, 1.0, 1.0]))),
        clip_settings=draft.Clip_settings(transform_y=-0.8),
    )
    script.add_segment(text_segment)
    result["data"] = json.loads(script.dumps())
    return jsonify(result)


@api_bp.route("/api/audio-segment", methods=["POST"])
@api_error_handler
def api_audio_segment():
    """音频片段处理"""
    data = get_request_data()
    result = DraftService.create_audio_segment(
        duration=data.get("duration", "5s"),
        volume=data.get("volume", 0.6),
        fade_in=data.get("fade_in", "1s"),
    )
    # 添加基础数据结构
    script = create_basic_script()
    script.add_track(Track_type.audio)
    result["data"] = json.loads(script.dumps())
    return jsonify(result)


@api_bp.route("/api/video-segment", methods=["POST"])
@api_error_handler
def api_video_segment():
    """视频片段处理"""
    data = get_request_data()
    result = DraftService.create_video_segment(duration=data.get("duration", "4.2s"))
    # 添加基础数据结构
    script = create_basic_script()
    script.add_track(Track_type.video)
    result["data"] = json.loads(script.dumps())
    return jsonify(result)


@api_bp.route("/api/comprehensive-create", methods=["POST"])
@api_error_handler
def api_comprehensive_create():
    """综合创作项目"""
    data = get_request_data()
    result = DraftService.create_comprehensive_project(data)
    return jsonify(result)


@api_bp.route("/api/comprehensive", methods=["POST"])
@api_error_handler
def api_comprehensive():
    """综合项目创建"""
    # 创建剪映草稿
    script = create_basic_script()

    # 添加多个轨道
    script.add_track(Track_type.audio).add_track(Track_type.video).add_track(
        Track_type.text
    )

    # 创建文本片段
    text_segment = draft.Text_segment(
        "pyJianYingDraft综合测试",
        trange("0s", "4.2s"),
        style=draft.Text_style(color=(1.0, 1.0, 0.0)),  # 黄色
        clip_settings=draft.Clip_settings(transform_y=-0.8),
    )

    # 添加文本动画
    text_segment.add_animation(draft.Text_outro.故障闪动, duration=tim("1s"))

    # 添加片段到脚本
    script.add_segment(text_segment)

    # 导出为JSON格式
    draft_json = script.dumps()

    return jsonify(
        {"success": True, "message": "综合项目创建成功", "data": json.loads(draft_json)}
    )


@api_bp.route("/api/download-from-url", methods=["POST"])
@api_error_handler
def api_download_from_url():
    """从网址下载音视频文件"""
    data = get_request_data()
    url = data.get("url", "").strip()
    file_type = data.get("type", "video")

    if not url:
        return create_error_response("请提供有效的网址", 400)

    print(f"🌐 开始下载 {file_type} 文件: {url}")

    user_uploads_dir = ensure_user_uploads_dir()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    response = requests.get(url, headers=headers, stream=True, timeout=30)
    response.raise_for_status()

    content_type = response.headers.get("content-type", "").lower()

    # 验证文件类型
    if file_type == "audio" and not any(
        t in content_type for t in ["audio", "mpeg", "mp3", "wav", "ogg"]
    ):
        return create_error_response("网址不是有效的音频文件", 400)
    elif file_type == "video" and not any(
        t in content_type for t in ["video", "mp4", "avi", "mov", "webm"]
    ):
        return create_error_response("网址不是有效的视频文件", 400)

    # 生成文件名并保存
    filename = generate_unique_filename(file_type, url) + get_file_extension_from_url(
        url, content_type
    )
    file_path = os.path.join(user_uploads_dir, filename)
    file_size = 0

    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                file_size += len(chunk)

    print(f"✅ 文件下载成功: {filename} ({file_size/1024/1024:.2f} MB)")

    return create_success_response(
        f"{file_type}文件下载成功", filename=filename, size=file_size, path=file_path
    )


@api_bp.route("/api/select-project-dir", methods=["POST"])
@api_error_handler
def api_select_project_dir():
    """选择项目目录并返回配置好的项目数据"""
    data = get_request_data()
    project_data = data.get("project_data")
    project_dir = data.get("project_dir", "").strip()

    if not project_data:
        return create_error_response("缺少项目数据", 400)

    if not project_dir:
        return create_error_response("请选择工程目录", 400)

    print(f"📂 用户选择的工程目录: {project_dir}")

    final_project_data = set_absolute_paths_in_project(project_data, project_dir)

    return create_success_response(
        "路径配置成功", data=final_project_data, project_dir=project_dir
    )


# 简化下载补丁包API
@api_bp.route("/api/download-patch-simple", methods=["POST"])
def api_download_patch_simple():
    """下载补丁包（简化版，直接保存到用户指定路径）"""
    try:
        print("🔄 收到简化补丁包下载请求")

        data = request.get_json() or {}
        project_data = data.get("project_data")
        project_dir = data.get("project_dir", "").strip()

        if not project_data:
            return jsonify({"success": False, "message": "缺少项目数据"}), 400

        if not project_dir:
            return jsonify({"success": False, "message": "请选择工程目录"}), 400

        print(f"📂 用户工程目录: {project_dir}")

        import zipfile
        import tempfile
        import shutil

        # 确保目标目录存在
        try:
            os.makedirs(project_dir, exist_ok=True)
            assets_dir = os.path.join(project_dir, "assets")
            os.makedirs(assets_dir, exist_ok=True)
            print(f"✅ 目标目录创建成功: {project_dir}")
        except Exception as e:
            return jsonify(
                {
                    "success": False,
                    "message": f"无法创建目标目录 {project_dir}: {str(e)}",
                }
            ), 400

        # 创建临时目录和ZIP文件
        temp_dir = tempfile.mkdtemp()
        timestamp = int(time.time())
        zip_filename = f"jianying_project_{timestamp}.zip"
        zip_path = os.path.join(temp_dir, zip_filename)

        user_uploads_dir = ensure_user_uploads_dir()

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # 添加模板JSON文件
            json_content = json.dumps(project_data, indent=2, ensure_ascii=False)
            zipf.writestr("draft_content.json", json_content)
            print("✅ 添加 draft_content.json 到补丁包")

            # 收集所有素材文件
            collected_assets = []

            # 添加用户下载的文件
            if os.path.exists(user_uploads_dir):
                for filename in os.listdir(user_uploads_dir):
                    file_path = os.path.join(user_uploads_dir, filename)
                    if os.path.isfile(file_path):
                        zipf.write(file_path, f"assets/{filename}")
                        file_size = os.path.getsize(file_path)
                        collected_assets.append(
                            {
                                "filename": filename,
                                "size": file_size,
                                "source": "用户下载",
                            }
                        )
                        print(f"✅ 添加用户文件: {filename}")

            # 添加系统默认素材文件
            tutorial_asset_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "readme_assets", "tutorial"
            )
            for asset_file in ["audio.mp3", "video.mp4"]:
                asset_path = os.path.join(tutorial_asset_dir, asset_file)
                if os.path.exists(asset_path):
                    standard_filename = f"default_{asset_file}"
                    zipf.write(asset_path, f"assets/{standard_filename}")
                    collected_assets.append(
                        {
                            "filename": standard_filename,
                            "size": os.path.getsize(asset_path),
                            "source": "系统默认",
                        }
                    )
                    print(f"✅ 添加系统默认文件: {standard_filename}")

            # 生成说明文件
            assets_info = (
                "\n".join(
                    [
                        f"- {asset['filename']} ({asset['size']/1024/1024:.2f} MB) - {asset['source']}"
                        for asset in collected_assets
                    ]
                )
                if collected_assets
                else "无素材文件"
            )

            readme_content = f"""# 剪映项目补丁包

## 🎯 使用方法
1. **已自动配置路径**: 补丁包已保存到指定目录
2. **解压补丁包**: 解压 {zip_filename} 文件
3. **素材文件**: 素材文件会自动解压到 assets 目录
4. **导入项目**: 将 draft_content.json 复制到剪映草稿目录
5. **打开剪映**: 在剪映中打开项目即可

## 📂 路径配置
- **工程目录**: {project_dir}
- **素材目录**: {assets_dir}
- **路径类型**: 绝对路径（已配置完成）

## 📋 包含文件
{assets_info}

## ⚠️ 重要提示
1. 补丁包已保存到指定目录: {project_dir}
2. 解压后素材文件将位于正确位置
3. 不要更改素材文件名和位置

## 🕒 生成信息
- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 素材数量: {len(collected_assets)} 个文件
- 项目分辨率: 1920x1080
- 保存位置: {project_dir}\\{zip_filename}
"""
            zipf.writestr("README.md", readme_content)

        # 将ZIP文件复制到用户指定目录
        target_zip_path = os.path.join(project_dir, zip_filename)
        try:
            shutil.copy2(zip_path, target_zip_path)
            print(f"✅ 补丁包已保存到: {target_zip_path}")
        except Exception as e:
            return jsonify(
                {"success": False, "message": f"无法保存到指定目录: {str(e)}"}
            ), 500

        # 解压素材文件到assets目录
        try:
            with zipfile.ZipFile(target_zip_path, "r") as zipf:
                # 只解压assets目录中的文件
                for file_info in zipf.filelist:
                    if file_info.filename.startswith("assets/"):
                        zipf.extract(file_info, project_dir)
                        print(f"✅ 解压素材文件: {file_info.filename}")

                # 解压draft_content.json到项目根目录
                if "draft_content.json" in zipf.namelist():
                    zipf.extract("draft_content.json", project_dir)
                    print("✅ 解压 draft_content.json")

                # 解压README.md
                if "README.md" in zipf.namelist():
                    zipf.extract("README.md", project_dir)
                    print("✅ 解压 README.md")

        except Exception as e:
            print(f"⚠️ 解压文件时出现警告: {str(e)}")

        # 清理临时文件
        try:
            os.remove(zip_path)
            os.rmdir(temp_dir)
        except:
            pass

        print(f"✅ 补丁包生成并保存成功: {target_zip_path}")

        return jsonify(
            {
                "success": True,
                "message": f"补丁包已成功保存到指定目录",
                "details": {
                    "project_dir": project_dir,
                    "zip_file": zip_filename,
                    "full_path": target_zip_path,
                    "assets_count": len(collected_assets),
                    "assets_dir": assets_dir,
                    "instructions": [
                        f"补丁包已保存到: {target_zip_path}",
                        f"素材文件已解压到: {assets_dir}",
                        f"项目文件已准备完毕，可直接在剪映中使用",
                        "如需重新部署，可使用ZIP文件进行备份",
                    ],
                },
            }
        )

    except Exception as e:
        print(f"❌ 生成补丁包失败: {str(e)}")
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "message": f"生成补丁包失败: {str(e)}"}), 500


# 注册新路由
@api_bp.route("/api/select-project-dir", methods=["POST"])
def api_select_project_dir_route():
    """选择项目目录路由"""
    return api_select_project_dir()


@api_bp.route("/api/download-patch-simple", methods=["POST"])
def api_download_patch_simple_route():
    """下载简化补丁包路由"""
    return api_download_patch_simple()


print("✅ API路由注册完成 - 已移除API测试功能")
