import os
from flask import Blueprint, jsonify, request, render_template_string

# 创建Blueprint
api_bp = Blueprint('api', __name__)

# 文档处理函数
def show_documentation():
    """展示API文档"""
    return render_template_string("""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>pyJianYingDraft API 文档</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; min-height: 100vh; }
        .header { background: linear-gradient(135deg, #007bff, #0056b3); color: white; padding: 30px; text-align: center; border-radius: 8px; margin-bottom: 30px; }
        .endpoint { background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 5px solid #007bff; }
        .endpoint h3 { color: #007bff; margin-top: 0; }
        .method { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; margin-right: 10px; }
        .get { background: #28a745; color: white; }
        .post { background: #007bff; color: white; }
        .test-section { background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .test-button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 5px; }
        .test-button:hover { background: #0056b3; }
        .test-result { margin-top: 15px; padding: 10px; background: white; border-radius: 5px; display: none; max-height: 300px; overflow-y: auto; font-family: monospace; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 pyJianYingDraft API</h1>
            <p>剪映草稿自动化生成接口</p>
            <p style="font-size: 14px; opacity: 0.9;">Version 1.0.0</p>
        </div>
        
        <div class="test-section">
            <h3>🚀 快速测试</h3>
            <p>点击下方按钮快速测试API接口：</p>
            <button class="test-button" onclick="testAPI('/api/health', 'GET')">健康检查</button>
            <button class="test-button" onclick="testAPI('/api/basic-project', 'POST')">创建基础项目</button>
            <button class="test-button" onclick="testAPI('/api/text-segment', 'POST', {text: 'API测试', duration: '2s'})">创建文本片段</button>
            <div id="testResult" class="test-result"></div>
        </div>
        
        <h2>📚 API 接口列表</h2>
        
        <div class="endpoint">
            <h3><span class="method get">GET</span> /api/health</h3>
            <p><strong>功能:</strong> 健康检查接口</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/basic-project</h3>
            <p><strong>功能:</strong> 创建基础剪映项目</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/text-segment</h3>
            <p><strong>功能:</strong> 创建文本片段</p>
            <p><strong>参数:</strong> text, duration, color, font</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/audio-segment</h3>
            <p><strong>功能:</strong> 创建音频片段</p>
            <p><strong>参数:</strong> duration, volume, fade_in</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/video-segment</h3>
            <p><strong>功能:</strong> 创建视频片段</p>
            <p><strong>参数:</strong> duration</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/comprehensive</h3>
            <p><strong>功能:</strong> 创建综合测试项目</p>
        </div>
    </div>
    
    <script>
        async function testAPI(endpoint, method = 'GET', data = null) {
            const resultDiv = document.getElementById('testResult');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '🔄 正在测试...';

            try {
                const options = { method, headers: { 'Content-Type': 'application/json' } };
                if (data && method === 'POST') options.body = JSON.stringify(data);

                const response = await fetch(endpoint, options);
                const result = await response.json();
                
                resultDiv.innerHTML = `
                    <strong>🎯 ${method} ${endpoint}</strong><br>
                    <strong>状态:</strong> ${response.status}<br>
                    <strong>响应:</strong><br>
                    <pre>${JSON.stringify(result, null, 2)}</pre>
                `;
                resultDiv.style.border = `2px solid ${response.ok ? '#28a745' : '#dc3545'}`;
            } catch (error) {
                resultDiv.innerHTML = `<strong>❌ 测试失败:</strong> ${error.message}`;
                resultDiv.style.border = '2px solid #dc3545';
            }
        }
    </script>
</body>
</html>
    """)

# API处理函数
def health_check():
    """健康检查接口"""
    return jsonify({
        "success": True,
        "message": "API服务正常运行",
        "endpoints": {
            "/api/basic-project": "创建基础项目",
            "/api/audio-segment": "创建音频片段",
            "/api/video-segment": "创建视频片段", 
            "/api/text-segment": "创建文本片段",
            "/api/video-animation": "创建视频动画",
            "/api/text-animation": "创建文本动画",
            "/api/transition": "创建转场效果",
            "/api/background-filling": "创建背景填充",
            "/api/text-effects": "创建文本特效",
            "/api/comprehensive": "创建综合项目"
        },
        "version": "1.0.0",
        "status": "running"
    })

def handle_basic_project():
    """处理基础项目创建API"""
    return jsonify({
        "success": True,
        "message": "基础项目创建成功",
        "output_path": "/mock/basic_project",
        "project_info": {"width": 1920, "height": 1080, "tracks": ["video"]}
    })

def handle_text_segment():
    """处理文本片段API"""
    data = request.get_json() or {}
    text = data.get('text', '这是一个文本测试')
    duration = data.get('duration', '3s')
    color = data.get('color', [1.0, 1.0, 0.0])
    font = data.get('font', '文轩体')
    
    return jsonify({
        "success": True,
        "message": "文本片段创建成功",
        "output_path": "/mock/text_segment",
        "text_info": {"text": text, "duration": duration, "color": color, "font": font}
    })

def handle_audio_segment():
    """处理音频片段API"""
    data = request.get_json() or {}
    duration = data.get('duration', '5s')
    volume = data.get('volume', 0.6)
    fade_in = data.get('fade_in', '1s')
    
    return jsonify({
        "success": True,
        "message": "音频片段创建成功",
        "output_path": "/mock/audio_segment",
        "audio_info": {"duration": duration, "volume": volume, "fade_in": fade_in}
    })

def handle_video_segment():
    """处理视频片段API"""
    data = request.get_json() or {}
    duration = data.get('duration', '4.2s')
    
    return jsonify({
        "success": True,
        "message": "视频片段创建成功",
        "output_path": "/mock/video_segment",
        "video_info": {"duration": duration}
    })

def handle_comprehensive():
    """处理综合测试API"""
    return jsonify({
        "success": True,
        "message": "综合项目创建成功",
        "output_path": "/mock/comprehensive",
        "project_info": {
            "tracks": ["audio", "video", "text"],
            "segments": ["audio", "video", "gif", "text"],
            "effects": ["fade", "animation", "transition", "background_filling", "text_effects"]
        }
    })

# 注册路由
@api_bp.route('/', methods=['GET'])
def root_documentation():
    """根路径文档展示"""
    return show_documentation()

@api_bp.route('/api/health', methods=['GET'])
def api_health():
    """API健康检查"""
    return health_check()

@api_bp.route('/api/basic-project', methods=['POST'])
def api_basic_project():
    """基础项目创建"""
    return handle_basic_project()

@api_bp.route('/api/text-segment', methods=['POST'])
def api_text_segment():
    """文本片段处理"""
    return handle_text_segment()

@api_bp.route('/api/audio-segment', methods=['POST'])
def api_audio_segment():
    """音频片段处理"""
    return handle_audio_segment()

@api_bp.route('/api/video-segment', methods=['POST'])
def api_video_segment():
    """视频片段处理"""
    return handle_video_segment()

@api_bp.route('/api/comprehensive', methods=['POST'])
def api_comprehensive():
    """综合项目创建"""
    return handle_comprehensive()

print("✅ API路由注册完成")
