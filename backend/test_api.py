#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Django API测试脚本
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api_endpoint(endpoint, data=None, description=""):
    """测试API端点"""
    print(f"\n🧪 测试: {description}")
    print(f"📍 端点: {endpoint}")
    
    try:
        start_time = time.time()
        
        if data:
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        else:
            if endpoint.endswith('/'):
                response = requests.post(f"{BASE_URL}{endpoint}")
            else:
                response = requests.get(f"{BASE_URL}{endpoint}")
        
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000
        
        print(f"⏱️ 响应时间: {execution_time:.2f}ms")
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 测试成功")
            if 'output_path' in result:
                print(f"📁 输出文件: {result['output_path']}")
        else:
            print(f"❌ 测试失败: {response.text}")
            
    except Exception as e:
        print(f"💥 请求异常: {str(e)}")

def main():
    """主测试函数"""
    print("🎬 pyJianYingDraft Django API 测试")
    print("=" * 50)
    
    # 测试服务状态
    try:
        response = requests.get(f"{BASE_URL}/health/")
        if response.status_code == 200:
            print("✅ Django服务运行正常")
        else:
            print("❌ 服务异常")
            return
    except:
        print("❌ 无法连接到Django服务，请确保服务已启动")
        return
    
    # Django API测试用例
    test_cases = [
        ("/api/health/", None, "健康检查"),
        ("/api/basic-project/", {}, "基础项目创建"),
        ("/api/text-segment/", {
            "text": "Django API测试",
            "duration": "3s",
            "color": [1.0, 1.0, 0.0],
            "font": "文轩体"
        }, "文本片段创建"),
        ("/api/audio-segment/", {
            "duration": "5s",
            "volume": 0.6,
            "fade_in": "1s"
        }, "音频片段创建"),
        ("/api/video-segment/", {
            "duration": "4.2s"
        }, "视频片段创建"),
        ("/api/comprehensive/", {}, "综合项目创建"),
        ("/api/projects/", None, "项目列表查询"),
        ("/api/dashboard/", None, "仪表盘数据")
    ]
    
    for endpoint, data, description in test_cases:
        test_api_endpoint(endpoint, data, description)
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("🎊 Django API测试完成")

if __name__ == '__main__':
    main()
