from .models import Project
from config.settings import get_asset_path
from .utils import (
    api_error_handler, create_basic_script, create_success_response,
    create_error_response, create_and_save_script,
    logger
)
from pyJianYingDraft import trange, tim, Intro_type, Transition_type
import pyJianYingDraft as draft
import os
# 添加项目根目录到Python路径
import sys
from datetime import datetime

from django.conf import settings
from django.db.models import Count, Q
from django.http import HttpResponse, FileResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)


# 添加Project模型导入
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(requests):
    """健康检查接口"""
    return Response({
        "success": True,
        "message": "pyJianYingDraft API 服务正常运行",
        "version": "1.0.0",
        "timestamp": "2024-01-01T00:00:00Z"
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@api_error_handler
def basic_project(request):
    """基础项目创建接口"""
    logger.info("🚀 开始创建基础项目")

    script = create_basic_script()
    output_path = "/mock/basic_project"
    # 保存到数据库时关联用户
    project = Project.objects.create(
        user=request.user,
        name=f'基础项目_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
        type='basic-project',
        status='completed',
        draft_content=script.to_dict() if hasattr(script, 'to_dict') else {},
        output_path=output_path
    )

    return create_success_response(
        "基础项目创建成功",
        output_path=output_path,
        project_info={"id": project.id, "name": project.name, "type": project.type}
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@api_error_handler
def text_segment(request):
    """处理文本片段API"""
    data = request.data
    text = data.get('text', '这是一个文本测试')
    duration = data.get('duration', '3s')
    color = data.get('color', [1.0, 1.0, 0.0])
    font = data.get('font', '文轩体')

    logger.info(f"📝 开始创建文本片段 - 文本:{text}, 时长:{duration}, 颜色:{color}")

    script = create_basic_script()
    script.add_track(draft.Track_type.text)

    text_segment = draft.Text_segment(
        text, trange("0s", duration),
        font=getattr(draft.Font_type, font, draft.Font_type.文轩体),
        style=draft.Text_style(color=tuple(color)),
        clip_settings=draft.Clip_settings(transform_y=-0.8)
    )
    script.add_segment(text_segment)

    # 保存项目到数据库
    project = Project.objects.create(
        user=request.user,
        name=f'文本片段_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
        type='text-segment',
        status='completed',
        draft_content=script.to_dict() if hasattr(script, 'to_dict') else {},
        output_path="/mock/text_segment"
    )

    return create_success_response(
        "文本片段创建成功",
        output_path="/mock/text_segment",
        text_info={"text": text, "duration": duration, "color": color, "font": font},
        project_info={"id": project.id, "name": project.name}
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@api_error_handler
def text_animation(request):
    """处理文本动画API"""
    data = request.data
    text = data.get('text', '文本动画测试')
    duration = data.get('duration', '3s')
    animation = data.get('animation', '故障闪动')
    animation_duration = data.get('animation_duration', '1s')
    logger.info(f"📝🎭 开始创建文本动画 - 文本:{text}, 时长:{duration}, 动画:{animation}")
    script = create_basic_script()
    script.add_track(draft.Track_type.text)
    text_segment = draft.Text_segment(
        text, trange("0s", duration),
        font=draft.Font_type.文轩体,
        style=draft.Text_style(color=(1.0, 0.0, 0.0))
    )
    animation_type = getattr(draft.Text_outro, animation, draft.Text_outro.故障闪动)
    text_segment.add_animation(animation_type, duration=tim(animation_duration))
    script.add_segment(text_segment)
    return create_success_response(
        "文本动画创建成功",
        output_path="/mock/text_animation",
        animation_info={"text": text, "duration": duration, "animation": animation, "animation_duration": animation_duration}
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@api_error_handler
def text_effects(request):
    """处理文本特效API"""
    data = request.data
    text = data.get('text', '文本特效测试')
    duration = data.get('duration', '4s')
    bubble_id = data.get('bubble_id', '361595')
    bubble_resource_id = data.get('bubble_resource_id', '6742029398926430728')
    effect_id = data.get('effect_id', '7296357486490144036')

    logger.info(f"✨ 开始创建文本特效 - 文本:{text}, 时长:{duration}")

    script = create_basic_script()
    script.add_track(draft.Track_type.text)

    text_segment = draft.Text_segment(
        text, trange("0s", duration),
        font=draft.Font_type.文轩体,
        style=draft.Text_style(color=(0.0, 1.0, 1.0))
    )

    text_segment.add_bubble(bubble_id, bubble_resource_id)
    text_segment.add_effect(effect_id)
    script.add_segment(text_segment)

    return create_success_response(
        "文本特效创建成功",
        output_path="/mock/text_effects",
        effect_info={"text": text, "duration": duration, "bubble_id": bubble_id, "effect_id": effect_id}
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@api_error_handler
def audio_segment(request):
    """处理音频片段API"""
    data = request.data
    duration = data.get('duration', '5s')
    volume = data.get('volume', 0.6)
    fade_in = data.get('fade_in', '1s')

    logger.info(f"🎵 开始创建音频片段 - 时长:{duration}, 音量:{volume}, 淡入:{fade_in}")

    script = create_basic_script()
    script.add_track(draft.Track_type.audio)

    audio_material = draft.Audio_material(get_asset_path('audio.mp3'))
    audio_segment = draft.Audio_segment(audio_material, trange("0s", duration), volume=volume)
    audio_segment.add_fade(fade_in, "0s")
    script.add_segment(audio_segment)

    return create_success_response(
        "音频片段创建成功",
        output_path="/mock/audio_segment",
        audio_info={"duration": duration, "volume": volume, "fade_in": fade_in}
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@api_error_handler
def video_segment(request):
    """处理视频片段API"""
    data = request.data
    duration = data.get('duration', '4.2s')

    logger.info(f"🎬 开始创建视频片段 - 时长:{duration}")

    script = create_basic_script()
    script.add_track(draft.Track_type.video)

    video_material = draft.Video_material(get_asset_path('video.mp4'))
    video_segment = draft.Video_segment(video_material, trange("0s", duration))
    script.add_segment(video_segment)

    return create_success_response(
        "视频片段创建成功",
        output_path="/mock/video_segment",
        video_info={"duration": duration}
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@api_error_handler
def video_animation(request):
    """处理视频动画API"""
    data = request.data
    duration = data.get('duration', '4.2s')
    animation = data.get('animation', '斜切')

    logger.info(f"🎭 开始创建视频动画 - 时长:{duration}, 动画:{animation}")

    script = create_basic_script()
    script.add_track(draft.Track_type.video)

    video_material = draft.Video_material(get_asset_path('video.mp4'))
    video_segment = draft.Video_segment(video_material, trange("0s", duration))

    animation_type = getattr(Intro_type, animation, Intro_type.斜切)
    video_segment.add_animation(animation_type)
    script.add_segment(video_segment)

    return create_success_response(
        "视频动画创建成功",
        output_path="/mock/video_animation",
        animation_info={"duration": duration, "animation": animation}
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@api_error_handler
def transition(request):
    """处理转场效果API"""
    data = request.data
    transition_type = data.get('transition', '信号故障')
    segment1_duration = data.get('segment1_duration', '2s')
    segment2_duration = data.get('segment2_duration', '2s')

    logger.info(f"🔄 开始创建转场效果 - 转场:{transition_type}")

    script = create_basic_script()
    script.add_track(draft.Track_type.video)

    video_material = draft.Video_material(get_asset_path('video.mp4'))
    gif_material = draft.Video_material(get_asset_path('sticker.gif'))

    video_segment1 = draft.Video_segment(video_material, trange("0s", segment1_duration))
    transition_effect = getattr(Transition_type, transition_type, Transition_type.信号故障)
    video_segment1.add_transition(transition_effect)

    video_segment2 = draft.Video_segment(gif_material, trange(video_segment1.end, segment2_duration))

    script.add_segment(video_segment1).add_segment(video_segment2)

    return create_success_response(
        "转场效果创建成功",
        output_path="/mock/transition",
        transition_info={"transition": transition_type, "segment1_duration": segment1_duration, "segment2_duration": segment2_duration}
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@api_error_handler
def background_filling(request):
    """处理背景填充API"""
    data = request.data
    duration = data.get('duration', '3s')
    blur_type = data.get('blur_type', 'blur')
    blur_intensity = data.get('blur_intensity', 0.0625)

    logger.info(f"🌈 开始创建背景填充 - 时长:{duration}, 模糊强度:{blur_intensity}")

    script = create_basic_script()
    script.add_track(draft.Track_type.video)

    gif_material = draft.Video_material(get_asset_path('sticker.gif'))
    gif_segment = draft.Video_segment(gif_material, trange("0s", duration))
    gif_segment.add_background_filling(blur_type, blur_intensity)
    script.add_segment(gif_segment)

    return create_success_response(
        "背景填充创建成功",
        output_path="/mock/background_filling",
        background_info={"duration": duration, "blur_type": blur_type, "blur_intensity": blur_intensity}
    )

# 添加权限装饰器到现有视图


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_data(request):
    """仪表盘数据"""
    user = request.user

    try:
        # 项目统计
        project_stats = Project.objects.filter(user=user).aggregate(
            total_projects=Count('id'),
            completed_projects=Count('id', filter=Q(status='completed')),
            processing_projects=Count('id', filter=Q(status='processing')),
            draft_projects=Count('id', filter=Q(status='draft'))
        )

        # 最近活动
        recent_projects = Project.objects.filter(user=user).order_by('-created_at')[:5]
        activities = []
        for project in recent_projects:
            activities.append({
                'title': f'创建项目: {project.name}',
                'time': project.created_at.strftime('%Y-%m-%d %H:%M'),
                'status': 'success'
            })

        return Response({
            'success': True,
            'data': {
                'stats': project_stats,
                'activities': activities,
                'user_info': {
                    'username': user.username,
                    'nickname': getattr(user, 'nickname', user.username),
                    'is_admin': getattr(user, 'is_admin', False)
                }
            }
        })
    except Exception as e:
        logger.error(f"获取仪表盘数据失败: {e}")
        return Response({
            'success': True,
            'data': {
                'stats': {'total_projects': 0, 'completed_projects': 0, 'processing_projects': 0, 'draft_projects': 0},
                'activities': [],
                'user_info': {
                    'username': user.username,
                    'nickname': getattr(user, 'nickname', user.username),
                    'is_admin': getattr(user, 'is_admin', False)
                }
            }
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_list(request):
    """项目列表"""
    user = request.user

    try:
        projects = Project.objects.filter(user=user).order_by('-created_at')

        # 添加统计信息
        stats = projects.aggregate(
            total_projects=Count('id'),
            completed_projects=Count('id', filter=Q(status='completed')),
            processing_projects=Count('id', filter=Q(status='processing')),
            draft_projects=Count('id', filter=Q(status='draft'))
        )

        project_data = []
        for project in projects:
            project_data.append({
                'id': project.id,
                'name': project.name,
                'type': project.type,
                'status': project.status,
                'created_at': project.created_at.isoformat(),
                'output_path': project.output_path,
                'description': f'{project.type}类型项目',
                'file_size': len(str(project.draft_content)) / 1024 if project.draft_content else 0,
                'assets_count': len(project.draft_content.get('materials', [])) if project.draft_content else 0
            })

        return Response({
            'success': True,
            'data': project_data,
            'stats': stats
        })
    except Exception as e:
        logger.error(f"获取项目列表失败: {e}")
        return Response({
            'success': True,
            'data': [],
            'stats': {'total_projects': 0, 'completed_projects': 0, 'processing_projects': 0, 'draft_projects': 0}
        })

# 更新其他创建API的权限和用户关联


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@api_error_handler
def comprehensive(request):
    """处理综合测试API"""
    logger.info("🎊 开始创建综合项目")

    script = create_basic_script()
    script.add_track(draft.Track_type.audio).add_track(draft.Track_type.video).add_track(draft.Track_type.text)

    # 素材
    audio_material = draft.Audio_material(get_asset_path('audio.mp3'))
    video_material = draft.Video_material(get_asset_path('video.mp4'))
    gif_material = draft.Video_material(get_asset_path('sticker.gif'))

    # 音频片段
    audio_segment = draft.Audio_segment(audio_material, trange("0s", "5s"), volume=0.6)
    audio_segment.add_fade("1s", "0s")

    # 视频片段
    video_segment = draft.Video_segment(video_material, trange("0s", "4.2s"))
    video_segment.add_animation(Intro_type.斜切)

    # GIF片段
    gif_segment = draft.Video_segment(gif_material, trange(video_segment.end, gif_material.duration))
    gif_segment.add_background_filling("blur", 0.0625)
    video_segment.add_transition(Transition_type.信号故障)

    # 文本片段
    text_segment = draft.Text_segment(
        "pyJianYingDraft综合测试", video_segment.target_timerange,
        font=draft.Font_type.文轩体,
        style=draft.Text_style(color=(1.0, 1.0, 0.0)),
        clip_settings=draft.Clip_settings(transform_y=-0.8)
    )
    text_segment.add_animation(draft.Text_outro.故障闪动, duration=tim("1s"))
    text_segment.add_bubble("361595", "6742029398926430728")
    text_segment.add_effect("7296357486490144036")

    script.add_segment(audio_segment).add_segment(video_segment).add_segment(gif_segment).add_segment(text_segment)

    return create_and_save_script(
        script, "comprehensive", "综合项目创建成功",
        {"project_info": {
            "tracks": ["audio", "video", "text"],
            "segments": ["audio", "video", "gif", "text"],
            "effects": ["fade", "animation", "transition", "background_filling", "text_effects"]
        }}
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@api_error_handler
def comprehensive_create(request):
    """综合创建项目API"""
    data = request.data
    logger.info("🎊 开始创建综合创作项目")

    # 创建基础脚本
    script = create_basic_script()

    # 根据配置添加轨道和内容
    if data.get('text', {}).get('enabled'):
        script.add_track(draft.Track_type.text)
        config = data['text']['config']
        text_segment = draft.Text_segment(
            config.get('text', '测试文本'),
            trange("0s", config.get('duration', '3s')),
            font=getattr(draft.Font_type, config.get('font', '文轩体'), draft.Font_type.文轩体),
            style=draft.Text_style(color=tuple(config.get('color', [1.0, 1.0, 0.0]))),
            clip_settings=draft.Clip_settings(transform_y=-0.8)
        )
        script.add_segment(text_segment)

    if data.get('audio', {}).get('enabled'):
        script.add_track(draft.Track_type.audio)
        config = data['audio']['config']
        audio_material = draft.Audio_material(get_asset_path('audio.mp3'))
        audio_segment = draft.Audio_segment(
            audio_material,
            trange("0s", config.get('duration', '5s')),
            volume=config.get('volume', 0.6)
        )
        audio_segment.add_fade(config.get('fade_in', '1s'), "0s")
        script.add_segment(audio_segment)

    if data.get('video', {}).get('enabled'):
        script.add_track(draft.Track_type.video)
        config = data['video']['config']
        video_material = draft.Video_material(get_asset_path('video.mp4'))
        video_segment = draft.Video_segment(video_material, trange("0s", config.get('duration', '4.2s')))
        script.add_segment(video_segment)

    return create_and_save_script(
        script, "comprehensive_create", "综合创作项目创建成功",
        {"config": data, "project_type": "comprehensive_create"}
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_projects(request):
    """获取项目列表API - 兼容旧接口"""
    return Response({
        "success": True,
        "data": [],
        "stats": {"total": 0, "completed": 0, "pending": 0},
        "total": 0
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_dashboard_data(request):
    """获取仪表盘数据API - 兼容旧接口"""
    return Response({
        "success": True,
        "stats": {"total": 0, "completed": 0, "pending": 0},
        "activities": []
    })


@api_view(['POST'])
@permission_classes([AllowAny])
@api_error_handler
def download_from_url(request):
    """从URL下载API"""
    data = request.data
    url = data.get('url', '')

    if not url:
        return create_error_response("URL不能为空")

    logger.info(f"📥 收到下载请求: {url}")

    return create_success_response(
        "下载功能开发中",
        data={"url": url, "status": "pending"}
    )


@api_view(['POST'])
@permission_classes([AllowAny])
@api_error_handler
def select_project_dir(request):
    """选择项目目录API"""
    data = request.data
    project_dir = data.get('project_dir', '')

    if not project_dir:
        return create_error_response("项目目录不能为空")

    logger.info(f"📁 项目目录设置: {project_dir}")

    return create_success_response(
        "项目目录设置成功",
        data={"project_dir": project_dir}
    )


@api_view(['POST'])
@permission_classes([AllowAny])
@api_error_handler
def download_patch_simple(request):
    """简单下载补丁API"""
    data = request.data
    logger.info("📦 执行简单下载补丁")

    return create_success_response(
        "下载补丁功能开发中",
        data=data
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def openapi_spec(request):
    """返回OpenAPI规范文档"""
    docs_path = os.path.join(settings.BASE_DIR, 'docs', 'openapi.yaml')
    if os.path.exists(docs_path):
        return FileResponse(open(docs_path, 'rb'), content_type='text/yaml')
    else:
        return HttpResponse("OpenAPI文档未找到", status=404)


# 添加统计相关API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_project_stats(request):
    """获取项目统计信息"""
    user = request.user
    
    try:
        stats = Project.objects.filter(user=user).aggregate(
            total_projects=Count('id'),
            completed_projects=Count('id', filter=Q(status='completed')),
            processing_projects=Count('id', filter=Q(status='processing')),
            draft_projects=Count('id', filter=Q(status='draft'))
        )
        
        return Response({
            'success': True,
            'data': stats
        })
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        return Response({
            'success': True,
            'data': {'total_projects': 0, 'completed_projects': 0, 'processing_projects': 0, 'draft_projects': 0}
        })
