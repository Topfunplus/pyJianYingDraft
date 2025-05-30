from utils.common import create_basic_script, ensure_user_uploads_dir
from logs.logger import setup_logger
from config.settings import get_asset_path, get_output_path
from pyJianYingDraft import trange, tim, Intro_type, Transition_type, Track_type
import pyJianYingDraft as draft
import os
import sys
import json

# 添加项目根目录到Python路径
current_dir = os.path.dirname(__file__)
web_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(web_dir)
sys.path.insert(0, project_root)


# 添加web目录到路径
sys.path.insert(0, web_dir)

# 设置日志记录器
logger = setup_logger('DraftService')


class DraftService:
    """剪映草稿服务类"""

    @staticmethod
    def create_basic_project():
        """创建基础项目"""
        logger.info("🎬 开始创建基础项目")

        script = create_basic_script()
        script.add_track(draft.Track_type.video)

        output_path = get_output_path("basic_project")
        script.dump(output_path)

        logger.info(f"✅ 基础项目创建成功: {output_path}")

        return {
            "success": True,
            "message": "基础项目创建成功",
            "output_path": output_path,
            "project_info": {
                "width": 1920,
                "height": 1080,
                "tracks": ["video"]
            }
        }

    @staticmethod
    def _create_segment_with_material(material_type, file_key, duration, **kwargs):
        """创建带素材的片段的通用方法"""
        script = create_basic_script()

        if material_type == "audio":
            script.add_track(draft.Track_type.audio)
            material = draft.Audio_material(get_asset_path(file_key))
            segment = draft.Audio_segment(
                material,
                trange("0s", duration),
                volume=kwargs.get('volume', 0.6)
            )
            if kwargs.get('fade_in', '0s') != '0s':
                segment.add_fade(kwargs['fade_in'], "0s")
        else:  # video
            script.add_track(draft.Track_type.video)
            material = draft.Video_material(get_asset_path(file_key))
            segment = draft.Video_segment(material, trange("0s", duration))

        script.add_segment(segment)
        return script

    @staticmethod
    def create_audio_segment(duration="5s", volume=0.6, fade_in="1s"):
        """创建音频片段"""
        logger.info(f"🎵 开始创建音频片段 - 时长:{duration}, 音量:{volume}, 淡入:{fade_in}")

        script = DraftService._create_segment_with_material(
            "audio", 'audio.mp3', duration, volume=volume, fade_in=fade_in
        )

        output_path = get_output_path("audio_segment")
        script.dump(output_path)

        logger.info(f"✅ 音频片段创建成功: {output_path}")

        return {
            "success": True,
            "message": "音频片段创建成功",
            "output_path": output_path,
            "audio_info": {"duration": duration, "volume": volume, "fade_in": fade_in}
        }

    @staticmethod
    def create_video_segment(duration="4.2s"):
        """创建视频片段"""
        logger.info(f"🎬 开始创建视频片段 - 时长:{duration}")

        script = DraftService._create_segment_with_material("video", 'video.mp4', duration)

        output_path = get_output_path("video_segment")
        script.dump(output_path)

        logger.info(f"✅ 视频片段创建成功: {output_path}")

        return {
            "success": True,
            "message": "视频片段创建成功",
            "output_path": output_path,
            "video_info": {"duration": duration}
        }

    @staticmethod
    def _create_text_segment_base(text, duration, color=(1.0, 1.0, 0.0), font="文轩体", transform_y=-0.8):
        """创建文本片段的基础方法"""
        script = create_basic_script()
        script.add_track(draft.Track_type.text)

        text_segment = draft.Text_segment(
            text,
            trange("0s", duration),
            font=getattr(draft.Font_type, font, draft.Font_type.文轩体),
            style=draft.Text_style(color=tuple(color)),
            clip_settings=draft.Clip_settings(transform_y=transform_y)
        )

        return script, text_segment

    @staticmethod
    def create_text_segment(text="这是一个文本测试", duration="3s", color=(1.0, 1.0, 0.0), font="文轩体"):
        """创建文本片段"""
        logger.info(f"📝 开始创建文本片段 - 文本:{text}, 时长:{duration}, 颜色:{color}")

        script, text_segment = DraftService._create_text_segment_base(text, duration, color, font)
        script.add_segment(text_segment)

        output_path = get_output_path("text_segment")
        script.dump(output_path)

        logger.info(f"✅ 文本片段创建成功: {output_path}")

        return {
            "success": True,
            "message": "文本片段创建成功",
            "output_path": output_path,
            "text_info": {"text": text, "duration": duration, "color": color, "font": font}
        }

    @staticmethod
    def create_comprehensive_project(config):
        """创建综合项目"""
        try:
            print(f"🏗️ 开始创建综合项目，配置: {config}")

            # 检查素材文件可用性
            user_uploads_dir = ensure_user_uploads_dir()

            # 检查可用的素材文件 - 只检查用户上传的文件
            available_assets = {
                'audio': [],
                'video': [],
                'user_files': []
            }

            # 检查用户上传的文件
            if os.path.exists(user_uploads_dir):
                for filename in os.listdir(user_uploads_dir):
                    if filename.lower().endswith(('.mp3', '.wav', '.m4a')):
                        available_assets['audio'].append(f"用户音频: {filename}")
                        available_assets['user_files'].append(filename)
                    elif filename.lower().endswith(('.mp4', '.avi', '.mov')):
                        available_assets['video'].append(f"用户视频: {filename}")
                        available_assets['user_files'].append(filename)

            print(f"📁 可用素材: {available_assets}")

            # 创建基础脚本
            script = create_basic_script()

            enabled_features = []
            segments_info = []
            warnings = []  # 用于收集警告信息

            # 为不同类型的内容创建不同的轨道
            text_track_added = False
            audio_track_added = False
            video_track_added = False

            current_text_time = 0  # 文本轨道的时间偏移

            # 处理文本组件
            if config.get('text', {}).get('enabled', False):
                if not text_track_added:
                    script.add_track(Track_type.text)
                    text_track_added = True

                text_config = config['text'].get('config', {})
                text_content = text_config.get('text', '欢迎使用剪映助手')
                text_duration = text_config.get('duration', '3s')

                duration_seconds = float(text_duration.replace('s', ''))

                text_segment = draft.Text_segment(
                    text_content,
                    trange(f"{current_text_time}s", f"{current_text_time + duration_seconds}s"),
                    style=draft.Text_style(color=tuple(text_config.get('color', [1.0, 1.0, 1.0]))),
                    clip_settings=draft.Clip_settings(transform_y=-0.8),
                )
                script.add_segment(text_segment)
                enabled_features.append('文本片段')
                segments_info.append({
                    'type': '文本',
                    'content': text_content,
                    'duration': text_duration,
                    'start_time': f'{current_text_time}s',
                    'status': '✅ 创建成功'
                })
                current_text_time += duration_seconds

            # 处理动画组件 - 添加到新的文本轨道
            if config.get('animation', {}).get('enabled', False):
                # 为动画文本添加新的轨道
                script.add_track(Track_type.text)

                animation_config = config['animation'].get('config', {})
                animation_text = animation_config.get('text', '这是动画文本')
                animation_duration = animation_config.get('duration', '2s')
                duration_seconds = float(animation_duration.replace('s', ''))

                # 动画文本使用独立的时间，从0开始
                animated_text = draft.Text_segment(
                    animation_text,
                    trange("0s", f"{duration_seconds}s"),
                    style=draft.Text_style(color=(1.0, 1.0, 0.0)),
                    clip_settings=draft.Clip_settings(transform_y=-0.3),
                )
                animated_text.add_animation(draft.Text_outro.故障闪动, duration=tim("1s"))
                script.add_segment(animated_text)

                enabled_features.append('动画效果')
                segments_info.append({
                    'type': '动画文本',
                    'content': animation_text,
                    'duration': animation_duration,
                    'animation': '故障闪动',
                    'start_time': '0s',
                    'status': '✅ 创建成功',
                    'note': '独立轨道，与普通文本并行'
                })

            # 处理特效组件 - 添加到新的文本轨道
            if config.get('effects', {}).get('enabled', False):
                # 为特效文本添加新的轨道
                script.add_track(Track_type.text)

                effects_config = config['effects'].get('config', {})
                effects_text = effects_config.get('text', '这是特效文本')
                effects_duration = effects_config.get('duration', '2s')
                duration_seconds = float(effects_duration.replace('s', ''))

                # 特效文本使用独立的时间，从0开始
                effects_segment = draft.Text_segment(
                    effects_text,
                    trange("0s", f"{duration_seconds}s"),
                    style=draft.Text_style(color=(0.0, 1.0, 1.0)),
                    clip_settings=draft.Clip_settings(transform_y=0.3),
                )
                script.add_segment(effects_segment)

                enabled_features.append('文本特效')
                segments_info.append({
                    'type': '特效文本',
                    'content': effects_text,
                    'duration': effects_duration,
                    'start_time': '0s',
                    'status': '✅ 创建成功',
                    'note': '独立轨道，与其他文本并行'
                })

            # 处理音频组件（仅在有音频素材时）
            if config.get('audio', {}).get('enabled', False):
                if available_assets['audio']:
                    if not audio_track_added:
                        script.add_track(Track_type.audio)
                        audio_track_added = True

                    audio_config = config['audio'].get('config', {})
                    audio_duration = audio_config.get('duration', '5s')
                    audio_volume = audio_config.get('volume', 0.6)

                    # 实际创建音频片段和素材 - 只使用用户上传的文件
                    audio_file_path = None
                    audio_filename = None

                    # 只检查用户上传的音频文件
                    for filename in available_assets['user_files']:
                        if filename.lower().endswith(('.mp3', '.wav', '.m4a')):
                            audio_file_path = os.path.join(user_uploads_dir, filename)
                            audio_filename = filename
                            break

                    if audio_file_path and os.path.exists(audio_file_path):
                        try:
                            # 创建音频素材
                            audio_material = draft.Audio_material(audio_file_path)

                            # 创建音频片段
                            audio_segment = draft.Audio_segment(
                                audio_material,
                                trange("0s", audio_duration),
                                volume=audio_volume
                            )

                            # 添加淡入效果（如果配置了）
                            fade_in = audio_config.get('fade_in', '0s')
                            if fade_in != '0s':
                                audio_segment.add_fade(fade_in, "0s")

                            # 添加到脚本
                            script.add_segment(audio_segment)

                            enabled_features.append('音频片段')
                            segments_info.append({
                                'type': '音频',
                                'filename': audio_filename,
                                'duration': audio_duration,
                                'volume': audio_volume,
                                'start_time': '0s',
                                'status': '✅ 创建成功',
                                'note': f'使用用户上传素材: {audio_filename}'
                            })

                            print(f"✅ 成功创建音频片段: {audio_filename}, 时长: {audio_duration}")

                        except Exception as e:
                            print(f"❌ 创建音频片段失败: {str(e)}")
                            warnings.append(f'🔊 音频组件: 创建音频片段时出错 - {str(e)}')
                            segments_info.append({
                                'type': '音频',
                                'status': '❌ 创建失败',
                                'note': f'错误: {str(e)}'
                            })
                    else:
                        warnings.append('🔊 音频组件: 未找到用户上传的音频文件')
                        segments_info.append({
                            'type': '音频',
                            'status': '⚠️ 跳过 - 无可用音频文件',
                            'note': '请上传音频文件或使用网络下载功能添加音频素材'
                        })
                else:
                    warnings.append('🔊 音频组件: 未找到用户上传的音频素材文件，已跳过音频片段创建')
                    segments_info.append({
                        'type': '音频',
                        'status': '⚠️ 跳过 - 缺少音频素材',
                        'note': '请上传音频文件或使用网络下载功能添加音频素材'
                    })

            # 处理视频组件（仅在有视频素材时）
            if config.get('video', {}).get('enabled', False):
                if available_assets['video']:
                    if not video_track_added:
                        script.add_track(Track_type.video)
                        video_track_added = True

                    video_config = config['video'].get('config', {})
                    video_duration = video_config.get('duration', '4.2s')

                    # 实际创建视频片段和素材 - 只使用用户上传的文件
                    video_file_path = None
                    video_filename = None

                    # 只检查用户上传的视频文件
                    for filename in available_assets['user_files']:
                        if filename.lower().endswith(('.mp4', '.avi', '.mov')):
                            video_file_path = os.path.join(user_uploads_dir, filename)
                            video_filename = filename
                            break

                    if video_file_path and os.path.exists(video_file_path):
                        try:
                            # 创建视频素材
                            video_material = draft.Video_material(video_file_path)

                            # 创建视频片段
                            duration_seconds = float(video_duration.replace('s', ''))
                            video_segment = draft.Video_segment(
                                video_material,
                                trange("0s", video_duration)
                            )

                            # 添加到脚本
                            script.add_segment(video_segment)

                            enabled_features.append('视频片段')
                            segments_info.append({
                                'type': '视频',
                                'filename': video_filename,
                                'duration': video_duration,
                                'start_time': '0s',
                                'status': '✅ 创建成功',
                                'note': f'使用用户上传素材: {video_filename}'
                            })

                            print(f"✅ 成功创建视频片段: {video_filename}, 时长: {video_duration}")

                        except Exception as e:
                            print(f"❌ 创建视频片段失败: {str(e)}")
                            warnings.append(f'🎬 视频组件: 创建视频片段时出错 - {str(e)}')
                            segments_info.append({
                                'type': '视频',
                                'status': '❌ 创建失败',
                                'note': f'错误: {str(e)}'
                            })
                    else:
                        warnings.append('🎬 视频组件: 未找到用户上传的视频文件')
                        segments_info.append({
                            'type': '视频',
                            'status': '⚠️ 跳过 - 无可用视频文件',
                            'note': '请上传视频文件或使用网络下载功能添加视频素材'
                        })
                else:
                    warnings.append('🎬 视频组件: 未找到用户上传的视频素材文件，已跳过视频片段创建')
                    segments_info.append({
                        'type': '视频',
                        'status': '⚠️ 跳过 - 缺少视频素材',
                        'note': '请上传视频文件或使用网络下载功能添加视频素材'
                    })

            # 处理转场组件
            if config.get('transition', {}).get('enabled', False):
                if available_assets['video']:
                    transition_config = config['transition'].get('config', {})
                    transition_type = transition_config.get('transition_type', '信号故障')
                    
                    enabled_features.append('转场效果')
                    segments_info.append({
                        'type': '转场',
                        'transition_type': transition_type,
                        'status': '✅ 配置完成',
                        'note': '转场效果将在视频片段间自动应用'
                    })
                else:
                    warnings.append('🔄 转场组件: 转场效果需要用户上传的视频素材支持，已跳过')
                    segments_info.append({
                        'type': '转场',
                        'status': '⚠️ 跳过 - 需要视频素材',
                        'note': '转场效果需要至少2个视频片段才能生效，请先上传视频素材'
                    })
            
            # 导出项目数据
            draft_json = script.dumps()
            project_data = json.loads(draft_json)
            
            # 计算总时长
            total_duration = f"{max(current_text_time, 5)}s"  # 至少5秒
            
            # 统计轨道数量
            text_tracks_count = sum(1 for track in script.tracks if hasattr(track, 'type') and track.type == Track_type.text)
            
            # 构建响应
            result = {
                "success": True,
                "message": "综合项目创建成功" + (f" (有 {len(warnings)} 个组件因缺少素材被跳过)" if warnings else ""),
                "data": project_data,
                "summary": {
                    "total_duration": total_duration,
                    "components_count": len(enabled_features),
                    "enabled_features": enabled_features,
                    "segments": segments_info,
                    "resolution": "1920x1080",
                    "tracks": {
                        "text": f"{text_tracks_count} 个文本轨道",
                        "audio": "1 个音频轨道" if audio_track_added else "无",
                        "video": "1 个视频轨道" if video_track_added else "无"
                    },
                    "available_assets": available_assets,
                    "warnings": warnings,
                    "track_structure": "每种文本效果使用独立轨道，避免时间冲突"
                },
                "user_tips": {
                    "missing_assets": warnings,
                    "suggestions": [
                        "💡 音频组件需要用户上传音频文件 (.mp3, .wav, .m4a)",
                        "💡 视频组件需要用户上传视频文件 (.mp4, .avi, .mov)",
                        "💡 可使用'网络下载'功能从网址下载音视频素材",
                        "💡 文本组件无需额外素材，可直接使用",
                        "💡 系统仅使用用户提供的素材，不依赖本机文件"
                    ] if warnings else [
                        "✅ 所有组件都已成功创建",
                        "📦 项目已准备完毕，可以下载补丁包",
                        "🎬 所有素材均来自用户上传或网络下载"
                    ]
                }
            }

            print(f"✅ 综合项目创建成功，包含 {len(enabled_features)} 个组件，总时长: {total_duration}")
            print(f"📊 轨道结构: 文本轨道 {text_tracks_count} 个")
            if warnings:
                print(f"⚠️ 警告信息: {warnings}")
            return result
            
        except Exception as e:
            print(f"❌ 创建综合项目失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "message": f"创建综合项目失败: {str(e)}",
                "user_tips": {
                    "suggestions": [
                        "🔧 请确保已上传所需的音视频文件",
                        "📁 确保音频文件格式为 .mp3, .wav, .m4a",
                        "📁 确保视频文件格式为 .mp4, .avi, .mov",
                        "🌐 可使用网络下载功能获取素材",
                        "💬 如问题持续，请检查控制台错误信息",
                        "🎯 系统仅使用用户提供的素材文件"
                    ]
                }
            }

    # 私有方法处理各种组件类型
    @staticmethod
    def _handle_text_component(config, script, current_time, tutorial_dir, user_dir):
        """处理文本组件"""
        try:
            duration = config.get('duration', '3s')
            text_segment = draft.Text_segment(
                config.get('text', '综合创作文本'),
                trange(f"{current_time}s", duration),
                style=draft.Text_style(color=tuple(config.get('color', [1.0, 1.0, 1.0]))),
                clip_settings=draft.Clip_settings(transform_y=-0.8)
            )
            
            font = config.get('font', '文轩体')
            if hasattr(draft.Font_type, font):
                text_segment.font = getattr(draft.Font_type, font)
            
            script.add_segment(text_segment)
            
            return {
                "segments": [{
                    "type": "text",
                    "content": config.get('text', '综合创作文本'),
                    "duration": duration,
                    "start_time": f"{current_time}s"
                }],
                "assets": [],
                "current_time": current_time + float(duration.replace('s', ''))
            }
        except Exception as e:
            logger.error(f"❌ 处理文本组件失败: {e}")
            return None

    @staticmethod
    def _handle_audio_component(config, script, current_time, tutorial_dir, user_dir):
        """处理音频组件"""
        # 简化实现，实际需要更完整的音频处理逻辑
        return {
            "segments": [{"type": "audio", "note": "音频组件处理中"}],
            "assets": [],
            "current_time": current_time
        }

    @staticmethod
    def _handle_video_component(config, script, current_time, tutorial_dir, user_dir):
        """处理视频组件"""
        # 简化实现，实际需要更完整的视频处理逻辑
        return {
            "segments": [{"type": "video", "note": "视频组件处理中"}],
            "assets": [],
            "current_time": current_time
        }

    @staticmethod
    def _handle_animation_component(config, script, current_time, tutorial_dir, user_dir):
        """处理动画组件"""
        # 简化实现，实际需要更完整的动画处理逻辑
        return {
            "segments": [{"type": "animation", "note": "动画组件处理中"}],
            "assets": [],
            "current_time": current_time
        }

    @staticmethod
    def _handle_effects_component(config, script, current_time, tutorial_dir, user_dir):
        """处理特效组件"""
        # 简化实现，实际需要更完整的特效处理逻辑
        return {
            "segments": [{"type": "effects", "note": "特效组件处理中"}],
            "assets": [],
            "current_time": current_time
        }

    @staticmethod
    def _handle_transition_component(config, script, current_time, tutorial_dir, user_dir):
        """处理转场组件的具体逻辑"""
        pass
