# pyJianYingDraft 项目 Wiki

## 项目概述

pyJianYingDraft 是一个轻量、灵活、易上手的 Python 剪映草稿生成及导出工具，旨在构建全自动化视频剪辑/混剪流水线。该项目允许开发者通过 Python 代码自动生成剪映草稿文件，并提供批量导出功能。

## 核心功能

### 1. 模板模式功能
- ✅ 加载未加密的 `draft_content.json` 文件作为模板
- ✅ 根据名称替换音视频片段的素材
- ✅ 修改文本片段的文本内容
- ✅ 导入模板草稿中的音视频/文本轨道到另一草稿
- ✅ 提取模板中的贴纸/气泡/花字等元信息

### 2. 批量导出功能
- ✅ 控制剪映打开指定草稿
- ✅ 导出草稿至指定位置
- ✅ 调节导出分辨率和帧率

### 3. 视频与图片处理
- ✅ 添加本地视频/图片素材
- ✅ 自定义片段时间、持续时长或播放速度
- ✅ 视频整体调节（旋转、缩放、亮度等）
- ✅ 关键帧生成
- ✅ 入场/出场/组合动画
- ✅ 蒙版、片段特效和滤镜
- ✅ 视频背景填充

### 4. 音频处理
- ✅ 添加本地音频素材
- ✅ 自定义片段时间、持续时长或播放速度
- ✅ 调整淡入淡出时长和音量
- ✅ 音量关键帧
- ✅ 添加音频场景音效果

### 5. 文本及字幕
- ✅ 添加文本、设置字体及样式
- ✅ 文本关键帧和动画
- ✅ 文字描边和背景
- ✅ 文字气泡和花字效果
- ✅ 导入 `.srt` 文件生成字幕

## 系统要求

### 支持的操作系统
- **Windows**: 完整支持（推荐）
- **macOS/Linux**: 部分功能支持（不包括批量导出功能）

### Python 版本要求
- **Python 3.8+** （推荐 3.8、3.10 或 3.11）
- **不推荐 Python 3.13**（可能存在依赖问题）

### 剪映版本兼容性
- **模板模式**: 支持剪映 5.9 及以下版本（6+ 版本文件已加密）
- **批量导出**: 支持剪映 6 及以下版本（7+ 版本控件被隐藏）
- **草稿生成**: 支持剪映 5 及以上所有版本

## 安装方法

### 方式一：pip 安装（推荐）
```bash
pip install pyJianYingDraft
```

### 方式二：源码安装
```bash
git clone https://github.com/GuanYixuan/pyJianYingDraft.git
cd pyJianYingDraft
pip install -r requirements.txt
pip install -e .
```

### 依赖包说明
- `pymediainfo`: 用于读取媒体文件信息
- `imageio`: 用于图像处理
- `uiautomation>=2`: 用于 Windows 下的剪映控制（仅 Windows）

## 项目结构

```
pyJianYingDraft/
├── pyJianYingDraft/           # 主要源码目录
│   ├── __init__.py           # 包初始化文件
│   ├── script_file.py        # 核心脚本文件类
│   ├── local_materials.py    # 本地素材处理
│   ├── video_segment.py      # 视频片段处理
│   ├── audio_segment.py      # 音频片段处理
│   ├── text_segment.py       # 文本片段处理
│   ├── effect_segment.py     # 特效片段处理
│   ├── track.py             # 轨道管理
│   ├── template_mode.py      # 模板模式功能
│   ├── draft_folder.py       # 草稿文件夹管理
│   ├── jianying_controller.py # 剪映控制器
│   ├── time_util.py          # 时间工具
│   ├── keyframe.py          # 关键帧处理
│   ├── metadata.py          # 元数据定义
│   ├── util.py              # 工具函数
│   ├── exceptions.py        # 异常定义
│   └── draft_content_template.json # 草稿模板
├── readme_assets/            # 文档资源
├── requirements.txt          # 依赖列表
├── setup.py                 # 安装配置
├── demo.py                  # 示例代码
└── README.md                # 项目说明
```

## 快速开始

### 1. 创建第一个草稿

```python
import pyJianYingDraft as draft
from pyJianYingDraft import trange

# 创建 1920x1080 分辨率的草稿
script = draft.Script_file(1920, 1080)

# 添加轨道
script.add_track(draft.Track_type.video)
script.add_track(draft.Track_type.audio)
script.add_track(draft.Track_type.text)

# 保存草稿
script.dump("path/to/your/draft_content.json")
```

### 2. 运行示例代码

1. 在剪映中创建一个空草稿
2. 找到草稿文件夹路径（类似 `.../JianyingPro Drafts/草稿名称`）
3. 修改 `demo.py` 中的 `DUMP_PATH` 为草稿的 `draft_content.json` 路径
4. 返回剪映首页或退出剪映
5. 运行 `python demo.py`
6. 重新打开剪映中的草稿查看效果

## 主要使用场景

### 1. 模板批量处理
```python
import pyJianYingDraft as draft

# 管理草稿文件夹
draft_folder = draft.Draft_folder("path/to/JianyingPro Drafts")

# 基于模板创建新草稿
script = draft_folder.duplicate_as_template("模板草稿", "新草稿")

# 替换素材
new_video = draft.Video_material("new_video.mp4")
script.replace_material_by_name("old_video.mp4", new_video)

# 保存
script.save()
```

### 2. 自动生成视频内容
```python
import pyJianYingDraft as draft
from pyJianYingDraft import trange

script = draft.Script_file(1920, 1080)
script.add_track(draft.Track_type.video)

# 添加视频素材
video_material = draft.Video_material("video.mp4")
video_segment = draft.Video_segment(
    video_material, 
    trange("0s", "10s"),  # 前10秒
    speed=1.5             # 1.5倍速
)

# 添加特效和动画
video_segment.add_animation(draft.Intro_type.淡入)
video_segment.add_filter(draft.Filter_type.复古, 80)

script.add_segment(video_segment)
script.dump("output/draft_content.json")
```

### 3. 批量导出
```python
import pyJianYingDraft as draft

# 控制剪映（需要剪映已打开并在目录页）
ctrl = draft.Jianying_controller()

# 批量导出草稿
draft_names = ["草稿1", "草稿2", "草稿3"]
for name in draft_names:
    ctrl.export_draft(name, f"output/{name}.mp4")
```

## 时间格式说明

pyJianYingDraft 支持两种时间格式：

### 微秒格式（内部使用）
```python
1000000  # 1秒 = 1,000,000 微秒
```

### 字符串格式（推荐使用）
```python
"1s"        # 1秒
"1.5s"      # 1.5秒
"1m30s"     # 1分30秒
"1h2m3s"    # 1小时2分3秒
```

### 时间工具函数
```python
from pyJianYingDraft import tim, trange, SEC

# 转换时间
time_us = tim("2.5s")  # 转换为微秒

# 创建时间范围
time_range = trange("1s", "3s")  # 从1s开始，持续3s

# 常量
one_second = SEC  # 1秒的微秒数
```

## 常见问题解答

### Q: 为什么模板功能不支持剪映6+版本？
A: 剪映6+版本对 `draft_content.json` 文件进行了加密，目前尚未找到解密方法。

### Q: 为什么批量导出不支持剪映7+版本？
A: 剪映7+版本隐藏了相关UI控件，导致自动化脚本无法定位。

### Q: 安装后 import 失败怎么办？
A: 可能是 uiautomation 兼容性问题，建议：
1. 使用 Python 3.8、3.10 或 3.11
2. 手动安装 uiautomation: `pip install uiautomation>=2`

### Q: 如何获取贴纸、气泡等素材的 resource_id？
A: 使用 `inspect_material()` 方法：
```python
script = draft_folder.load_template("模板草稿")
script.inspect_material()  # 会打印所有素材的元数据
```

### Q: 片段重叠怎么办？
A: 确保片段的时间范围不重叠，或使用不同的轨道：
```python
script.add_track(draft.Track_type.video, "轨道1")
script.add_track(draft.Track_type.video, "轨道2")
```

## 进阶功能

### 1. 关键帧动画
```python
from pyJianYingDraft import Keyframe_property

video_segment.add_keyframe(Keyframe_property.alpha, "2s", 0.5)  # 2秒时透明度50%
video_segment.add_keyframe(Keyframe_property.alpha, "4s", 1.0)  # 4秒时透明度100%
```

### 2. 多轨道管理
```python
# 创建多个视频轨道
script.add_track(draft.Track_type.video, "背景", relative_index=1)
script.add_track(draft.Track_type.video, "前景", relative_index=2)

# 指定轨道添加片段
script.add_segment(background_video, "背景")
script.add_segment(foreground_video, "前景")
```

### 3. 字幕批量导入
```python
# 导入SRT字幕文件
script.import_srt(
    "subtitles.srt",
    track_name="字幕",
    text_style=draft.Text_style(size=8, color=(1, 1, 1)),
    time_offset="0.5s"  # 字幕延迟0.5秒
)
```

## 开发贡献

### 环境设置
```bash
git clone https://github.com/GuanYixuan/pyJianYingDraft.git
cd pyJianYingDraft
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

### 代码规范
- 使用 Python 3.8+ 语法
- 遵循 PEP 8 代码风格
- 添加类型注解
- 编写单元测试

## 许可证

本项目采用开源许可证，具体请查看项目仓库。

## 社区支持

- **GitHub Issues**: 报告 Bug 和功能请求
- **Discord**: [加入讨论服务器](https://discord.gg/WfHgGQvhyW)
- **文档**: 查看 README.md 获取详细用法

## 更新日志

当前版本：v0.1.3

主要更新：
- 支持剪映5+版本的草稿生成
- 完善模板模式功能
- 新增批量导出功能
- 优化时间处理工具

---

*最后更新：2024年*
