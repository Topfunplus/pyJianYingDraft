#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API测试脚本
"""

import requests
import json
import time
import os
import sys

# 添加web目录到路径
current_dir = os.path.dirname(__file__)
web_dir = os.path.dirname(current_dir)
sys.path.insert(0, web_dir)

from logs.logger import setup_logger

logger = setup_logger('APITest')

BASE_URL = "http://localhost:5000"

def test_api_endpoint(endpoint, data=None, description=""):
    """测试API端点"""
    logger.info(f"🧪 测试: {description}")
    logger.info(f"📍 端点: {endpoint}")
    
    try:
        start_time = time.time()
        
        if data:
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        else:
            response = requests.post(f"{BASE_URL}{endpoint}")
        
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000
        
        logger.info(f"⏱️ 响应时间: {execution_time:.2f}ms")
        logger.info(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"✅ 测试成功")
            if 'output_path' in result:
                logger.info(f"📁 输出文件: {result['output_path']}")
        else:
            logger.error(f"❌ 测试失败: {response.text}")
            
    except Exception as e:
        logger.error(f"💥 请求异常: {str(e)}")

def main():
    """主测试函数"""
    logger.info("🎬 pyJianYingDraft Web Service API 测试")
    logger.info("=" * 50)
    
    # 测试服务状态
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            logger.info("✅ 服务运行正常")
        else:
            logger.error("❌ 服务异常")
            return
    except:
        logger.error("❌ 无法连接到服务，请确保服务已启动")
        return
    
    # 测试各个API端点
    test_cases = [
        ("/api/basic-project", {}, "基础项目创建"),
        ("/api/audio-segment", {
            "duration": "6s",
            "volume": 0.8,
            "fade_in": "2s"
        }, "音频片段创建"),
        ("/api/video-segment", {
            "duration": "5s"
        }, "视频片段创建"),
        ("/api/text-segment", {
            "text": "API测试文本",
            "duration": "4s",
            "color": [1.0, 0.5, 0.0],
            "font": "文轩体"
        }, "文本片段创建"),
        ("/api/video-animation", {
            "duration": "3s",
            "animation": "斜切"
        }, "视频动画创建"),
        ("/api/text-animation", {
            "text": "动画文本测试",
            "duration": "3s",
            "animation": "故障闪动",
            "animation_duration": "1.5s"
        }, "文本动画创建"),
        ("/api/transition", {
            "transition": "信号故障",
            "segment1_duration": "3s",
            "segment2_duration": "3s"
        }, "转场效果创建"),
        ("/api/background-filling", {
            "duration": "4s",
            "blur_type": "blur",
            "blur_intensity": 0.1
        }, "背景填充创建"),
        ("/api/text-effects", {
            "text": "特效文本测试",
            "duration": "5s"
        }, "文本特效创建"),
        ("/api/comprehensive", {}, "综合项目创建")
    ]
    
    for endpoint, data, description in test_cases:
        test_api_endpoint(endpoint, data, description)
        time.sleep(1)  # 避免请求过快
    
    logger.info("=" * 50)
    logger.info("🎊 所有API测试完成")

if __name__ == '__main__':
    main()
