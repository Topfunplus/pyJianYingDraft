import React from 'react';
import { Card } from 'antd';
import ReactMarkdown from 'react-markdown';
import { FileTextOutlined } from '@ant-design/icons';

const ApiDocumentation: React.FC = () => {  // 直接嵌入 markdown 内容，避免网络请求问题
  const markdownContent = `# 剪映自动化脚本 API 文档

## 概述

剪映自动化脚本提供了一套 REST API，用于创建和管理剪映项目，特别是通过模板生成各种片段。本文档详细介绍了所有可用的 API 接口。

## 基础信息

- **基础 URL**: \`/api\`
- **认证方式**: Bearer Token
- **内容类型**: \`application/json\`
- **版本**: v1.0.0

## 项目管理

### 创建基础项目

**POST** \`/api/basic-project\`

创建一个基础的剪映项目。

**响应示例:**

\`\`\`json
{
  "success": true,
  "message": "基础项目创建成功",
  "data": {
    "output_path": "/mock/basic_project",
    "project_info": {
      "id": 123,
      "name": "基础项目_20240724_145230",
      "type": "basic-project"
    }
  }
}
\`\`\`

### 创建文本片段

**POST** \`/api/text-segment\`

创建一个包含文本的剪映项目片段。

**请求参数:**

\`\`\`json
{
  "text": "要显示的文本内容",
  "duration": "3s",
  "color": [1.0, 1.0, 0.0],
  "font": "文轩体"
}
\`\`\`

**响应示例:**

\`\`\`json
{
  "success": true,
  "message": "文本片段创建成功",
  "data": {
    "output_path": "/mock/text_segment",
    "text_info": {
      "text": "要显示的文本内容",
      "duration": "3s",
      "color": [1.0, 1.0, 0.0],
      "font": "文轩体"
    },
    "project_info": {
      "id": 124,
      "name": "文本片段_20240724_145230"
    }
  }
}
\`\`\`

### 创建文本动画

**POST** \`/api/text-animation\`

创建一个包含文本动画的剪映项目片段。

**请求参数:**

\`\`\`json
{
  "text": "文本动画测试",
  "duration": "3s",
  "animation": "故障闪动",
  "animation_duration": "1s"
}
\`\`\`

**响应示例:**

\`\`\`json
{
  "success": true,
  "message": "文本动画创建成功",
  "data": {
    "output_path": "/mock/text_animation",
    "animation_info": {
      "text": "文本动画测试",
      "duration": "3s",
      "animation": "故障闪动",
      "animation_duration": "1s"
    }
  }
}
\`\`\`

### 创建文本特效

**POST** \`/api/text-effects\`

创建一个包含文本特效的剪映项目片段。

**请求参数:**

\`\`\`json
{
  "text": "文本特效测试",
  "duration": "4s",
  "bubble_id": "361595",
  "bubble_resource_id": "6742029398926430728",
  "effect_id": "7296357486490144036"
}
\`\`\`

**响应示例:**

\`\`\`json
{
  "success": true,
  "message": "文本特效创建成功",
  "data": {
    "output_path": "/mock/text_effects",
    "effect_info": {
      "text": "文本特效测试",
      "duration": "4s",
      "bubble_id": "361595",
      "effect_id": "7296357486490144036"
    }
  }
}
\`\`\`

### 创建音频片段

**POST** \`/api/audio-segment\`

创建一个包含音频的剪映项目片段。

**请求参数:**

\`\`\`json
{
  "duration": "5s",
  "volume": 0.6,
  "fade_in": "1s"
}
\`\`\`

**响应示例:**

\`\`\`json
{
  "success": true,
  "message": "音频片段创建成功",
  "data": {
    "output_path": "/mock/audio_segment",
    "audio_info": {
      "duration": "5s",
      "volume": 0.6,
      "fade_in": "1s"
    }
  }
}
\`\`\`

### 创建视频片段

**POST** \`/api/video-segment\`

创建一个包含视频的剪映项目片段。

**请求参数:**

\`\`\`json
{
  "duration": "4.2s"
}
\`\`\`

**响应示例:**

\`\`\`json
{
  "success": true,
  "message": "视频片段创建成功",
  "data": {
    "output_path": "/mock/video_segment",
    "video_info": {
      "duration": "4.2s"
    }
  }
}
\`\`\`

### 创建视频动画

**POST** \`/api/video-animation\`

创建一个包含视频动画的剪映项目片段。

**请求参数:**

\`\`\`json
{
  "duration": "4.2s",
  "animation": "斜切"
}
\`\`\`

**响应示例:**

\`\`\`json
{
  "success": true,
  "message": "视频动画创建成功",
  "data": {
    "output_path": "/mock/video_animation",
    "animation_info": {
      "duration": "4.2s",
      "animation": "斜切"
    }
  }
}
\`\`\`

### 创建转场效果

**POST** \`/api/transition\`

创建一个包含转场效果的剪映项目片段。

**请求参数:**

\`\`\`json
{
  "transition": "信号故障",
  "segment1_duration": "2s",
  "segment2_duration": "2s"
}
\`\`\`

**响应示例:**

\`\`\`json
{
  "success": true,
  "message": "转场效果创建成功",
  "data": {
    "output_path": "/mock/transition",
    "transition_info": {
      "transition": "信号故障",
      "segment1_duration": "2s",
      "segment2_duration": "2s"
    }
  }
}
\`\`\`

### 创建背景填充

**POST** \`/api/background-filling\`

创建一个包含背景填充效果的剪映项目片段。

**请求参数:**

\`\`\`json
{
  "duration": "3s",
  "blur_type": "blur",
  "blur_intensity": 0.0625
}
\`\`\`

**响应示例:**

\`\`\`json
{
  "success": true,
  "message": "背景填充创建成功",
  "data": {
    "output_path": "/mock/background_filling",
    "background_info": {
      "duration": "3s",
      "blur_type": "blur",
      "blur_intensity": 0.0625
    }
  }
}
\`\`\`

### 创建综合项目

**POST** \`/api/comprehensive\`

创建一个综合的剪映项目，包含音频、视频、文本等多种元素。

### 创建综合定制项目

**POST** \`/api/comprehensive-create\`

根据自定义配置创建综合项目。

**请求参数:**

\`\`\`json
{
  "text": {
    "enabled": true,
    "config": {
      "text": "测试文本",
      "duration": "3s",
      "font": "文轩体",
      "color": [1.0, 1.0, 0.0]
    }
  },
  "audio": {
    "enabled": true,
    "config": {
      "duration": "5s",
      "volume": 0.6,
      "fade_in": "1s"
    }
  },
  "video": {
    "enabled": true,
    "config": {
      "duration": "4.2s"
    }
  }
}
\`\`\`

**响应示例:**

\`\`\`json
{
  "success": true,
  "message": "综合创作项目创建成功",
  "data": {
    "output_path": "/mock/comprehensive_create",
    "config": {
      "text": {
        "enabled": true,
        "config": {
          "text": "测试文本",
          "duration": "3s",
          "font": "文轩体",
          "color": [1.0, 1.0, 0.0]
        }
      },
      "audio": {
        "enabled": true,
        "config": {
          "duration": "5s",
          "volume": 0.6,
          "fade_in": "1s"
        }
      },
      "video": {
        "enabled": true,
        "config": {
          "duration": "4.2s"
        }
      }
    },
    "project_type": "comprehensive_create"
  }
}
\`\`\`

### 获取项目列表

**GET** \`/api/projects\`

获取当前用户的所有项目。

**响应示例:**

\`\`\`json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "基础项目_20240724_145230",
      "type": "basic-project",
      "status": "completed",
      "created_at": "2024-07-24T06:52:30.488193Z",
      "output_path": "/mock/basic_project",
      "description": "basic-project类型项目",
      "file_size": 0.0,
      "assets_count": 0
    }
  ],
  "stats": {
    "total_projects": 1,
    "completed_projects": 1,
    "processing_projects": 0,
    "draft_projects": 0
  }
}
\`\`\`

## 仪表盘数据

### 获取项目统计

**GET** \`/api/stats\`

获取详细的项目统计信息。

**响应示例:**

\`\`\`json
{
  "success": true,
  "data": {
    "total_projects": 1,
    "completed_projects": 1,
    "processing_projects": 0,
    "draft_projects": 0
  }
}
\`\`\`

## 系统相关

### 健康检查

**GET** \`/api/health\`

检查系统健康状态。

**响应示例:**

\`\`\`json
{
  "success": true,
  "message": "pyJianYingDraft API 服务正常运行",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00Z"
}
\`\`\`

## 错误码说明

| 状态码 | 说明               |
| ------ | ------------------ |
| 200    | 请求成功           |
| 400    | 请求参数错误       |
| 401    | 未授权，需要登录   |
| 403    | 禁止访问，权限不足 |
| 404    | 资源不存在         |
| 500    | 服务器内部错误     |

## 通用响应格式

### 成功响应

\`\`\`json
{
  "success": true,
  "message": "操作成功",
  "data": {
    // 具体数据
  }
}
\`\`\`

### 错误响应

\`\`\`json
{
  "success": false,
  "message": "错误描述",
  "errors": {
    // 详细错误信息
  }
}
\`\`\`

## SDK 示例

### Python

\`\`\`python
import requests
import json

class JianYingAPI:
    def __init__(self, base_url="/api", token=None):
        self.base_url = base_url
        self.token = token
        self.session = requests.Session()
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        self.session.headers.update({"Content-Type": "application/json"})

    def login(self, username, password):
        response = self.session.post(f"{self.base_url}/auth/login",
                                     data=json.dumps({"username": username, "password": password}))
        data = response.json()
        if data["success"]:
            self.token = data["data"]["token"]
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        return data

    def create_text_segment(self, text, duration="3s", color=None, font="文轩体"):
        config = {
            "text": text,
            "duration": duration,
            "color": color or [1.0, 1.0, 0.0],
            "font": font
        }
        response = self.session.post(f"{self.base_url}/text-segment", data=json.dumps(config))
        return response.json()

# 示例用法
api = JianYingAPI()
login_data = api.login("your_username", "your_password")
if login_data["success"]:
    text_segment_data = api.create_text_segment("Hello, JianYing!", duration="5s")
    print(text_segment_data)
else:
    print("Login failed:", login_data)
\`\`\`

## 更新日志

### v1.0.0 (2023-12-01)

- 初始版本发布
- 基础项目创建功能
- 模板片段创建 API
- 项目管理 CRUD 操作
- 仪表盘数据展示

---

*最后更新: 2024 年 7 月 24 日*`;
  return (
    <Card
      title={
        <span>
          <FileTextOutlined style={{ marginRight: '8px' }} />
          API 文档
        </span>
      }
      style={{ height: '100%' }}
      styles={{
        body: {
          padding: '24px',
          maxHeight: 'calc(100vh - 200px)',
          overflow: 'auto'
        }
      }}
    >
      <div 
        style={{
          fontSize: '14px',
          lineHeight: '1.6',
          color: '#333'
        }}
      >
        <ReactMarkdown
          components={{
            h1: ({ children }) => (
              <h1 style={{ 
                color: '#1890ff', 
                borderBottom: '2px solid #1890ff',
                paddingBottom: '8px',
                marginBottom: '24px'
              }}>
                {children}
              </h1>
            ),
            h2: ({ children }) => (
              <h2 style={{ 
                color: '#1890ff',
                marginTop: '32px',
                marginBottom: '16px',
                borderBottom: '1px solid #e8e8e8',
                paddingBottom: '8px'
              }}>
                {children}
              </h2>
            ),
            h3: ({ children }) => (
              <h3 style={{ 
                color: '#333',
                marginTop: '24px',
                marginBottom: '12px'
              }}>
                {children}
              </h3>
            ),
            code: ({ inline, children }: any) => (
              inline ? (
                <code style={{
                  background: '#f5f5f5',
                  padding: '2px 6px',
                  borderRadius: '4px',
                  fontSize: '13px',
                  color: '#d63384'
                }}>
                  {children}
                </code>
              ) : (
                <pre style={{
                  background: '#f8f9fa',
                  border: '1px solid #e9ecef',
                  borderRadius: '6px',
                  padding: '16px',
                  overflow: 'auto',
                  fontSize: '13px',
                  lineHeight: '1.4'
                }}>
                  <code>{children}</code>
                </pre>
              )
            ),
            table: ({ children }) => (
              <div style={{ overflow: 'auto', marginBottom: '16px' }}>
                <table style={{
                  width: '100%',
                  borderCollapse: 'collapse',
                  border: '1px solid #e8e8e8'
                }}>
                  {children}
                </table>
              </div>
            ),
            th: ({ children }) => (
              <th style={{
                background: '#fafafa',
                padding: '12px',
                border: '1px solid #e8e8e8',
                textAlign: 'left',
                fontWeight: 'bold'
              }}>
                {children}
              </th>
            ),
            td: ({ children }) => (
              <td style={{
                padding: '12px',
                border: '1px solid #e8e8e8'
              }}>
                {children}
              </td>
            ),
            blockquote: ({ children }) => (
              <blockquote style={{
                borderLeft: '4px solid #1890ff',
                margin: '16px 0',
                padding: '8px 16px',
                background: '#f6f8fa'
              }}>
                {children}
              </blockquote>
            ),
            ul: ({ children }) => (
              <ul style={{ 
                paddingLeft: '24px',
                marginBottom: '16px'
              }}>
                {children}
              </ul>
            ),
            ol: ({ children }) => (
              <ol style={{ 
                paddingLeft: '24px',
                marginBottom: '16px'
              }}>
                {children}
              </ol>
            ),
            p: ({ children }) => (
              <p style={{ 
                marginBottom: '16px',
                lineHeight: '1.6'
              }}>
                {children}
              </p>
            )
          }}
        >
          {markdownContent}
        </ReactMarkdown>
      </div>
    </Card>
  );
};

export default ApiDocumentation;
