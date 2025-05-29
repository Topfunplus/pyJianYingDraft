# pyJianYingDraft API 接口文档

## 概览

pyJianYingDraft Web API 提供了一套完整的剪映草稿创建接口，支持音频、视频、文本等多种媒体类型的处理。

## 基础信息

- **基础URL**: `http://localhost:5000`
- **数据格式**: JSON
- **编码**: UTF-8

## 通用响应格式

### 成功响应
```json
{
    "success": true,
    "message": "操作成功",
    "output_path": "输出文件路径",
    "...": "其他相关信息"
}
```

### 错误响应
```json
{
    "success": false,
    "message": "错误描述信息"
}
```

## API 接口列表

### 1. 健康检查

**接口路径**: `GET /api/health`

**功能**: 检查API服务状态并返回所有可用接口列表

**请求参数**: 无

**响应示例**:
```json
{
    "success": true,
    "message": "API服务正常运行",
    "endpoints": {"接口列表..."}
}
```

---

### 2. 创建基础项目

**接口路径**: `POST /api/basic-project`

**功能**: 创建一个基础的剪映项目文件

**请求参数**: 无需传入参数

**响应示例**:
```json
{
    "success": true,
    "message": "基础项目创建成功",
    "output_path": "/path/to/basic_project_1234567890",
    "project_info": {
        "width": 1920,
        "height": 1080,
        "tracks": ["video"]
    }
}
```

---

### 3. 音频片段处理

**接口路径**: `POST /api/audio-segment`

**功能**: 创建包含音频片段的项目

**请求参数**:
```json
{
    "duration": "5s",        // 可选，音频时长，默认"5s"
    "volume": 0.6,           // 可选，音量大小(0-1)，默认0.6
    "fade_in": "1s"          // 可选，淡入时长，默认"1s"
}
```

**响应示例**:
```json
{
    "success": true,
    "message": "音频片段创建成功",
    "output_path": "/path/to/audio_segment_1234567890",
    "audio_info": {
        "duration": "5s",
        "volume": 0.6,
        "fade_in": "1s"
    }
}
```

---

### 4. 视频片段处理

**接口路径**: `POST /api/video-segment`

**功能**: 创建包含视频片段的项目

**请求参数**:
```json
{
    "duration": "4.2s"       // 可选，视频时长，默认"4.2s"
}
```

**响应示例**:
```json
{
    "success": true,
    "message": "视频片段创建成功",
    "output_path": "/path/to/video_segment_1234567890",
    "video_info": {
        "duration": "4.2s"
    }
}
```

---

### 5. 文本片段处理

**接口路径**: `POST /api/text-segment`

**功能**: 创建包含文本片段的项目

**请求参数**:
```json
{
    "text": "这是一个文本测试",    // 可选，文本内容
    "duration": "3s",         // 可选，显示时长，默认"3s"
    "color": [1.0, 1.0, 0.0], // 可选，文字颜色RGB，默认黄色
    "font": "文轩体"           // 可选，字体名称，默认"文轩体"
}
```

**响应示例**:
```json
{
    "success": true,
    "message": "文本片段创建成功",
    "output_path": "/path/to/text_segment_1234567890",
    "text_info": {
        "text": "这是一个文本测试",
        "duration": "3s",
        "color": [1.0, 1.0, 0.0],
        "font": "文轩体"
    }
}
```

---

### 6. 视频动画效果

**接口路径**: `POST /api/video-animation`

**功能**: 为视频添加动画效果

**请求参数**:
```json
{
    "duration": "4.2s",      // 可选，视频时长，默认"4.2s"
    "animation": "斜切"       // 可选，动画类型，默认"斜切"
}
```

**可用动画类型**: 斜切、淡入、缩放等（具体可用类型请参考pyJianYingDraft文档）

**响应示例**:
```json
{
    "success": true,
    "message": "视频动画创建成功",
    "output_path": "/path/to/video_animation_1234567890",
    "animation_info": {
        "duration": "4.2s",
        "animation": "斜切"
    }
}
```

---

### 7. 文本动画效果

**接口路径**: `POST /api/text-animation`

**功能**: 为文本添加动画效果

**请求参数**:
```json
{
    "text": "文本动画测试",        // 可选，文本内容
    "duration": "3s",           // 可选，总时长，默认"3s"
    "animation": "故障闪动",     // 可选，动画类型，默认"故障闪动"
    "animation_duration": "1s"  // 可选，动画持续时间，默认"1s"
}
```

**响应示例**:
```json
{
    "success": true,
    "message": "文本动画创建成功",
    "output_path": "/path/to/text_animation_1234567890",
    "animation_info": {
        "text": "文本动画测试",
        "duration": "3s",
        "animation": "故障闪动",
        "animation_duration": "1s"
    }
}
```

---

### 8. 转场效果

**接口路径**: `POST /api/transition`

**功能**: 在两个视频片段之间添加转场效果

**请求参数**:
```json
{
    "transition": "信号故障",        // 可选，转场类型，默认"信号故障"
    "segment1_duration": "2s",      // 可选，第一个片段时长，默认"2s"
    "segment2_duration": "2s"       // 可选，第二个片段时长，默认"2s"
}
```

**响应示例**:
```json
{
    "success": true,
    "message": "转场效果创建成功",
    "output_path": "/path/to/transition_1234567890",
    "transition_info": {
        "transition": "信号故障",
        "segment1_duration": "2s",
        "segment2_duration": "2s"
    }
}
```

---

### 9. 背景填充

**接口路径**: `POST /api/background-filling`

**功能**: 为视频添加背景填充效果

**请求参数**:
```json
{
    "duration": "3s",             // 可选，时长，默认"3s"
    "blur_type": "blur",          // 可选，模糊类型，默认"blur"
    "blur_intensity": 0.0625      // 可选，模糊强度，默认0.0625
}
```

**响应示例**:
```json
{
    "success": true,
    "message": "背景填充创建成功",
    "output_path": "/path/to/background_filling_1234567890",
    "background_info": {
        "duration": "3s",
        "blur_type": "blur",
        "blur_intensity": 0.0625
    }
}
```

---

### 10. 文本特效

**接口路径**: `POST /api/text-effects`

**功能**: 为文本添加气泡和花字特效

**请求参数**:
```json
{
    "text": "文本特效测试",                    // 可选，文本内容
    "duration": "4s",                      // 可选，时长，默认"4s"
    "bubble_id": "361595",                 // 可选，气泡效果ID
    "bubble_resource_id": "6742029398926430728",  // 可选，气泡资源ID
    "effect_id": "7296357486490144036"     // 可选，花字效果ID
}
```

**响应示例**:
```json
{
    "success": true,
    "message": "文本特效创建成功",
    "output_path": "/path/to/text_effects_1234567890",
    "effect_info": {
        "text": "文本特效测试",
        "duration": "4s",
        "bubble_id": "361595",
        "effect_id": "7296357486490144036"
    }
}
```

---

### 11. 综合项目

**接口路径**: `POST /api/comprehensive`

**功能**: 创建包含所有功能的综合测试项目

**请求参数**: 无需传入参数

**响应示例**:
```json
{
    "success": true,
    "message": "综合项目创建成功",
    "output_path": "/path/to/comprehensive_1234567890",
    "project_info": {
        "tracks": ["audio", "video", "text"],
        "segments": ["audio", "video", "gif", "text"],
        "effects": ["fade", "animation", "transition", "background_filling", "text_effects"]
    }
}
```

## 使用示例

### cURL 示例

```bash
# 健康检查
curl -X GET http://localhost:5000/api/health

# 创建基础项目
curl -X POST http://localhost:5000/api/basic-project \
  -H "Content-Type: application/json"

# 创建音频片段
curl -X POST http://localhost:5000/api/audio-segment \
  -H "Content-Type: application/json" \
  -d '{"duration": "3s", "volume": 0.8, "fade_in": "0.5s"}'

# 创建文本片段
curl -X POST http://localhost:5000/api/text-segment \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World", "duration": "5s", "color": [1.0, 0.0, 0.0]}'
```

### Python 示例

```python
import requests
import json

# 基础URL
BASE_URL = "http://localhost:5000"

# 健康检查
response = requests.get(f"{BASE_URL}/api/health")
print(response.json())

# 创建音频片段
audio_data = {
    "duration": "3s",
    "volume": 0.8,
    "fade_in": "0.5s"
}
response = requests.post(
    f"{BASE_URL}/api/audio-segment",
    headers={"Content-Type": "application/json"},
    data=json.dumps(audio_data)
)
print(response.json())
```

### JavaScript 示例

```javascript
// 健康检查
fetch('/api/health')
  .then(response => response.json())
  .then(data => console.log(data));

// 创建文本片段
fetch('/api/text-segment', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: "Hello World",
    duration: "5s",
    color: [1.0, 0.0, 0.0]
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 注意事项

1. **素材文件**: 确保在 `assets` 目录下有以下文件：
   - `audio.mp3` - 音频素材
   - `video.mp4` - 视频素材  
   - `sticker.gif` - GIF素材

2. **输出路径**: 生成的草稿文件会保存在 `output` 目录下，文件名包含时间戳

3. **时间格式**: 时间参数支持格式如 "1s", "2.5s", "1000ms" 等

4. **颜色格式**: 颜色使用RGB数组，值范围为0.0-1.0

5. **错误处理**: 所有接口都有统一的错误处理，返回详细的错误信息

## 版本信息

- **当前版本**: 1.0.0
- **更新时间**: 2024年
- **兼容性**: Python 3.7+, Flask 2.0+

## 联系方式

如有问题或建议，请通过GitHub Issues联系我们。
