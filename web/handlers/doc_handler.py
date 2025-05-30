from flask import jsonify, render_template_string

def show_documentation():
    """展示API文档"""
    try:
        # 使用原始字符串来避免Unicode转义问题
        html_content = r"""
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
        .new-feature { background: #d4edda; border-left: 5px solid #28a745; }
        
        /* 弹窗样式 */
        .modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); }
        .modal-content { background-color: white; margin: 15% auto; padding: 20px; border-radius: 8px; width: 500px; max-width: 90%; }
        .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .modal-title { font-size: 18px; font-weight: bold; color: #007bff; }
        .close { color: #aaa; font-size: 28px; font-weight: bold; cursor: pointer; }
        .close:hover { color: #000; }
        .form-group { margin-bottom: 15px; }
        .form-label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-input { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        .modal-buttons { display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px; }
        .btn { padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; }
        .btn-primary { background: #007bff; color: white; }
        .btn-secondary { background: #6c757d; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 pyJianYingDraft API</h1>
            <p>剪映草稿自动化生成接口</p>
            <p style="font-size: 14px; opacity: 0.9;">Version 1.3.0 - 智能路径配置</p>
        </div>
        
        <div class="test-section">
            <h3>🚀 快速测试</h3>
            <p>点击下方按钮快速测试API接口：</p>
            <button class="test-button" onclick="testAPI('/api/health', 'GET')">健康检查</button>
            <button class="test-button" onclick="testAPI('/api/basic-project', 'POST')">创建基础项目</button>
            <button class="test-button" onclick="testAPI('/api/text-segment', 'POST', {text: 'API测试', duration: '2s'})">创建文本片段</button>
            <button class="test-button" onclick="testDownloadAPI()">测试网络下载</button>
            <button class="test-button" onclick="testSimplePatch()">测试简单补丁包</button>
            <button class="test-button" onclick="showDownloadModal()">📦 下载完整补丁包</button>
            <div id="testResult" class="test-result"></div>
        </div>
        
        <h2>📚 API 接口列表</h2>
        
        <div class="endpoint">
            <h3><span class="method get">GET</span> /api/health</h3>
            <p><strong>功能:</strong> 健康检查接口，返回API状态和所有可用接口列表</p>
            <p><strong>参数:</strong> 无</p>
        </div>
        
        <div class="endpoint new-feature">
            <h3><span class="method post">POST</span> /api/download-from-url</h3>
            <p><strong>功能:</strong> 🆕 从网址下载音视频文件到服务器</p>
            <p><strong>参数:</strong> url(网址), type(文件类型: 'audio' 或 'video')</p>
            <p><strong>说明:</strong> 支持直链下载，自动验证文件类型，生成唯一文件名</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/basic-project</h3>
            <p><strong>功能:</strong> 创建基础剪映项目</p>
            <p><strong>参数:</strong> 无</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/text-segment</h3>
            <p><strong>功能:</strong> 创建文本片段</p>
            <p><strong>参数:</strong> text(文本内容), duration(时长), color(颜色), font(字体)</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/audio-segment</h3>
            <p><strong>功能:</strong> 创建音频片段</p>
            <p><strong>参数:</strong> duration(时长), volume(音量), fade_in(淡入时间)</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/video-segment</h3>
            <p><strong>功能:</strong> 创建视频片段</p>
            <p><strong>参数:</strong> duration(时长)</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /api/comprehensive</h3>
            <p><strong>功能:</strong> 创建综合测试项目，包含所有功能</p>
            <p><strong>参数:</strong> 无</p>
        </div>
        
        <div class="endpoint new-feature">
            <h3><span class="method post">POST</span> /api/comprehensive-create</h3>
            <p><strong>功能:</strong> 🆕 综合创作项目，支持多组件配置集成</p>
            <p><strong>参数:</strong> 组件配置对象，支持文本、音频、视频、动画、特效等</p>
            <p><strong>说明:</strong> 自动使用用户上传/下载的素材文件，支持本地上传和网络下载</p>
        </div>
        
        <div class="endpoint new-feature">
            <h3><span class="method post">POST</span> /api/download-patch-with-files</h3>
            <p><strong>功能:</strong> 🆕 下载完整补丁包（智能路径配置）</p>
            <p><strong>参数:</strong> project_data(项目数据), project_dir(剪映工程目录)</p>
            <p><strong>说明:</strong> 根据用户选择的工程目录，自动配置所有素材的绝对路径，生成即用补丁包</p>
        </div>
        
        <div style="background: #d1ecf1; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 5px solid #17a2b8;">
            <h4>🎯 智能路径配置特性</h4>
            <ul>
                <li><strong>弹窗路径选择:</strong> 下载时弹出窗口让用户选择工程目录</li>
                <li><strong>自动绝对路径:</strong> 所有素材路径自动配置为选择目录的绝对路径</li>
                <li><strong>即插即用:</strong> 下载后按说明放置文件即可在剪映中使用</li>
                <li><strong>Windows兼容:</strong> 使用Windows标准路径格式，确保剪映识别</li>
                <li><strong>智能文件管理:</strong> 自动处理用户上传、网络下载和系统默认素材</li>
            </ul>
        </div>

        <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 5px solid #ffc107;">
            <h4>📋 使用流程</h4>
            <ol>
                <li><strong>创建项目:</strong> 使用API创建包含音频、视频、文本等组件的项目</li>
                <li><strong>选择目录:</strong> 点击"下载完整补丁包"，在弹窗中选择剪映工程目录</li>
                <li><strong>下载补丁:</strong> 系统自动生成配置好路径的补丁包</li>
                <li><strong>放置文件:</strong> 解压补丁包，将素材文件放到指定的assets目录</li>
                <li><strong>导入剪映:</strong> 将draft_content.json导入剪映即可使用</li>
            </ol>
        </div>

        <p style="margin-top: 30px; text-align: center;">
            <a href="/api/health" style="color: #007bff;">📋 获取完整接口信息</a>
        </p>
    </div>
    
    <!-- 路径选择弹窗 -->
    <div id="pathModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <span class="modal-title">📁 选择剪映工程目录</span>
                <span class="close" onclick="closeModal()">&times;</span>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label">工程目录路径：</label>
                    <input type="text" id="projectDirInput" class="form-input" 
                           placeholder="例如: C:/Users/用户名/Desktop/剪映项目" 
                           value="C:/Users/Default/Desktop/剪映项目">
                    <small style="color: #666; margin-top: 5px; display: block;">
                        请输入您希望存放剪映素材的目录路径。所有音视频素材将保存在此目录的 assets 子文件夹中。
                    </small>
                </div>
                <div class="form-group">
                    <label class="form-label">示例路径：</label>
                    <select id="pathExamples" class="form-input" onchange="fillExamplePath()">
                        <option value="">-- 选择示例路径 --</option>
                        <option value="C:/Users/用户名/Desktop/剪映项目">桌面/剪映项目</option>
                        <option value="D:/剪映工程/我的项目">D盘/剪映工程/我的项目</option>
                        <option value="C:/JianYing/Projects">C盘/JianYing/Projects</option>
                    </select>
                </div>
            </div>
            <div class="modal-buttons">
                <button class="btn btn-secondary" onclick="closeModal()">取消</button>
                <button class="btn btn-primary" onclick="downloadWithPath()">确定下载</button>
            </div>
        </div>
    </div>
    
    <script>
        let currentProjectData = null;
        
        // 显示下载弹窗
        function showDownloadModal() {
            createProjectForDownload();
        }
        
        // 创建项目用于下载
        async function createProjectForDownload() {
            const resultDiv = document.getElementById('testResult');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '🔄 正在准备下载项目...';
            
            try {
                const response = await fetch('/api/comprehensive-create', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        audio: { enabled: true, config: { duration: '5s', volume: 0.6 } },
                        video: { enabled: true, config: { duration: '4.2s' } },
                        text: { enabled: true, config: { text: '测试项目', duration: '3s' } }
                    })
                });
                
                if (!response.ok) {
                    throw new Error('创建项目失败');
                }
                
                const result = await response.json();
                currentProjectData = result.data;
                
                resultDiv.innerHTML = '✅ 项目创建成功，请选择工程目录';
                resultDiv.style.border = '2px solid #28a745';
                
                document.getElementById('pathModal').style.display = 'block';
                
            } catch (error) {
                resultDiv.innerHTML = `❌ 创建项目失败: ${error.message}`;
                resultDiv.style.border = '2px solid #dc3545';
            }
        }
        
        // 填充示例路径
        function fillExamplePath() {
            const select = document.getElementById('pathExamples');
            const input = document.getElementById('projectDirInput');
            if (select.value) {
                input.value = select.value;
            }
        }
        
        // 关闭弹窗
        function closeModal() {
            document.getElementById('pathModal').style.display = 'none';
        }
        
        // 点击弹窗外部关闭
        window.onclick = function(event) {
            const modal = document.getElementById('pathModal');
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        }
        
        // 使用选择的路径下载
        async function downloadWithPath() {
            const projectDir = document.getElementById('projectDirInput').value.trim();
            const resultDiv = document.getElementById('testResult');
            
            if (!projectDir) {
                alert('请输入工程目录路径');
                return;
            }
            
            if (!currentProjectData) {
                alert('没有项目数据，请重新创建项目');
                closeModal();
                return;
            }
            
            resultDiv.innerHTML = '🔄 正在配置路径...';
            
            try {
                // 第一步：配置路径
                const configResponse = await fetch('/api/select-project-dir', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        project_data: currentProjectData,
                        project_dir: projectDir
                    })
                });
                
                if (!configResponse.ok) {
                    const errorResult = await configResponse.json();
                    throw new Error(errorResult.message || '路径配置失败');
                }
                
                const configResult = await configResponse.json();
                resultDiv.innerHTML = '🔄 正在生成补丁包...';
                
                // 第二步：下载补丁包
                const downloadResponse = await fetch('/api/download-patch-simple', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        project_data: configResult.data,
                        project_dir: projectDir
                    })
                });
                
                if (downloadResponse.ok) {
                    const blob = await downloadResponse.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `jianying_project_${Date.now()}.zip`;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);
                    
                    resultDiv.innerHTML = `
                        <strong>✅ 补丁包下载成功</strong><br>
                        <strong>工程目录:</strong> ${projectDir}<br>
                        <strong>素材目录:</strong> ${projectDir}/assets/<br>
                        <strong>说明:</strong> 补丁包已开始下载，请按照README.md说明操作
                    `;
                    resultDiv.style.border = '2px solid #28a745';
                    
                    closeModal();
                } else {
                    const errorResult = await downloadResponse.json();
                    throw new Error(errorResult.message || '下载失败');
                }
                
            } catch (error) {
                resultDiv.innerHTML = `❌ 下载失败: ${error.message}`;
                resultDiv.style.border = '2px solid #dc3545';
                closeModal();
            }
        }
        
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
        
        async function testDownloadAPI() {
            const resultDiv = document.getElementById('testResult');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '🔄 正在测试网络下载功能...';

            try {
                const testData = {
                    url: 'https://www.w3schools.com/html/mov_bbb.mp4',
                    type: 'video'
                };
                
                const response = await fetch('/api/download-from-url', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(testData)
                });
                
                const result = await response.json();
                
                resultDiv.innerHTML = `
                    <strong>🎯 POST /api/download-from-url</strong><br>
                    <strong>测试URL:</strong> ${testData.url}<br>
                    <strong>状态:</strong> ${response.status}<br>
                    <strong>响应:</strong><br>
                    <pre>${JSON.stringify(result, null, 2)}</pre>
                `;
                resultDiv.style.border = `2px solid ${response.ok ? '#28a745' : '#dc3545'}`;
            } catch (error) {
                resultDiv.innerHTML = `<strong>❌ 网络下载测试失败:</strong> ${error.message}`;
                resultDiv.style.border = '2px solid #dc3545';
            }
        }
        
        async function testSimplePatch() {
            const resultDiv = document.getElementById('testResult');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '🔄 正在测试简单补丁包下载...';

            try {
                const projectResponse = await fetch('/api/basic-project', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                
                if (!projectResponse.ok) {
                    throw new Error('创建项目失败');
                }
                
                const projectData = await projectResponse.json();
                
                const patchResponse = await fetch('/api/download-simple-patch', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        project_data: projectData.data,
                        project_dir: 'C:/Users/测试用户/Desktop/剪映项目'
                    })
                });
                
                if (patchResponse.ok) {
                    const blob = await patchResponse.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `test_patch_${Date.now()}.zip`;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);
                    
                    resultDiv.innerHTML = `
                        <strong>✅ 简单补丁包测试成功</strong><br>
                        <strong>状态:</strong> ${patchResponse.status}<br>
                        <strong>说明:</strong> 补丁包已开始下载<br>
                        <strong>测试目录:</strong> C:/Users/测试用户/Desktop/剪映项目
                    `;
                    resultDiv.style.border = '2px solid #28a745';
                } else {
                    const errorResult = await patchResponse.json();
                    throw new Error(errorResult.message || '下载失败');
                }
            } catch (error) {
                resultDiv.innerHTML = `<strong>❌ 补丁包测试失败:</strong> ${error.message}`;
                resultDiv.style.border = '2px solid #dc3545';
            }
        }
    </script>
</body>
</html>
        """
        
        return render_template_string(html_content)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"读取文档失败: {str(e)}",
            "error_type": type(e).__name__
        }), 500

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
            "/api/comprehensive": "创建综合项目",
            "/api/comprehensive-create": "综合创作项目（集成版）",
            "/api/download-from-url": "🆕 网络下载音视频文件",
            "/api/download-patch-with-files": "🆕 下载完整补丁包（配置绝对路径）",
            "/api/download-simple-patch": "🆕 下载简单补丁包（测试用）"
        },
        "version": "1.3.1",
        "status": "running",
        "new_features": [
            "网络URL下载音视频文件",
            "智能文件管理和存储",
            "完整补丁包生成",
            "多种素材来源支持",
            "用户选择工程目录",
            "自动绝对路径配置",
            "简单补丁包测试功能"
        ]
    })
