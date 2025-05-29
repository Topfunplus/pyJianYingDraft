import os
import sys
from flask import request, jsonify

# 添加web目录到路径
current_dir = os.path.dirname(__file__)
web_dir = os.path.dirname(current_dir)
sys.path.insert(0, web_dir)

from service.draft_service import DraftService
from logs.logger import setup_logger

# 设置日志记录器
logger = setup_logger('DraftController')


class DraftController:
    """剪映草稿控制器"""
    
    @staticmethod
    def basic_project():
        """基础项目创建控制器"""
        try:
            result = DraftService.create_basic_project()
            return jsonify(result)
        except Exception as e:
            logger.error(f"❌ 基础项目创建失败: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"基础项目创建失败: {str(e)}"
            }), 500
    
    @staticmethod
    def audio_segment():
        """音频片段控制器"""
        try:
            data = request.get_json() or {}
            
            duration = data.get('duration', '5s')
            volume = data.get('volume', 0.6)
            fade_in = data.get('fade_in', '1s')
            
            result = DraftService.create_audio_segment(duration, volume, fade_in)
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"❌ 音频片段创建失败: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"音频片段创建失败: {str(e)}"
            }), 500
    
    @staticmethod
    def video_segment():
        """视频片段控制器"""
        try:
            data = request.get_json() or {}
            duration = data.get('duration', '4.2s')
            
            result = DraftService.create_video_segment(duration)
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"❌ 视频片段创建失败: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"视频片段创建失败: {str(e)}"
            }), 500
    
    @staticmethod
    def text_segment():
        """文本片段控制器"""
        try:
            data = request.get_json() or {}
            
            text = data.get('text', '这是一个文本测试')
            duration = data.get('duration', '3s')
            color = data.get('color', [1.0, 1.0, 0.0])
            font = data.get('font', '文轩体')
            
            result = DraftService.create_text_segment(text, duration, color, font)
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"❌ 文本片段创建失败: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"文本片段创建失败: {str(e)}"
            }), 500
    
    @staticmethod
    def video_animation():
        """视频动画控制器"""
        try:
            data = request.get_json() or {}
            
            duration = data.get('duration', '4.2s')
            animation = data.get('animation', '斜切')
            
            result = DraftService.create_video_animation(duration, animation)
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"❌ 视频动画创建失败: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"视频动画创建失败: {str(e)}"
            }), 500
    
    @staticmethod
    def text_animation():
        """文本动画控制器"""
        try:
            data = request.get_json() or {}
            
            text = data.get('text', '文本动画测试')
            duration = data.get('duration', '3s')
            animation = data.get('animation', '故障闪动')
            animation_duration = data.get('animation_duration', '1s')
            
            result = DraftService.create_text_animation(text, duration, animation, animation_duration)
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"❌ 文本动画创建失败: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"文本动画创建失败: {str(e)}"
            }), 500
    
    @staticmethod
    def transition():
        """转场效果控制器"""
        try:
            data = request.get_json() or {}
            
            transition_type = data.get('transition', '信号故障')
            segment1_duration = data.get('segment1_duration', '2s')
            segment2_duration = data.get('segment2_duration', '2s')
            
            result = DraftService.create_transition(transition_type, segment1_duration, segment2_duration)
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"❌ 转场效果创建失败: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"转场效果创建失败: {str(e)}"
            }), 500
    
    @staticmethod
    def background_filling():
        """背景填充控制器"""
        try:
            data = request.get_json() or {}
            
            duration = data.get('duration', '3s')
            blur_type = data.get('blur_type', 'blur')
            blur_intensity = data.get('blur_intensity', 0.0625)
            
            result = DraftService.create_background_filling(duration, blur_type, blur_intensity)
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"❌ 背景填充创建失败: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"背景填充创建失败: {str(e)}"
            }), 500
    
    @staticmethod
    def text_effects():
        """文本特效控制器"""
        try:
            data = request.get_json() or {}
            
            text = data.get('text', '文本特效测试')
            duration = data.get('duration', '4s')
            bubble_id = data.get('bubble_id', '361595')
            bubble_resource_id = data.get('bubble_resource_id', '6742029398926430728')
            effect_id = data.get('effect_id', '7296357486490144036')
            
            result = DraftService.create_text_effects(text, duration, bubble_id, bubble_resource_id, effect_id)
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"❌ 文本特效创建失败: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"文本特效创建失败: {str(e)}"
            }), 500
    
    @staticmethod
    def comprehensive():
        """综合测试控制器"""
        try:
            result = DraftService.create_comprehensive()
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"❌ 综合项目创建失败: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"综合项目创建失败: {str(e)}"
            }), 500
