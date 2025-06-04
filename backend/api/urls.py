from django.urls import path, re_path

from . import views

urlpatterns = [
    # 健康检查（无需认证）
    re_path(r'^health/?$', views.health_check, name='health'),
    # 仪表盘和统计（需要认证）
    re_path(r'^dashboard/?$', views.dashboard_data, name='dashboard_data'),
    re_path(r'^projects/?$', views.project_list, name='project_list'),
    re_path(r'^stats/?$', views.get_project_stats, name='project_stats'),
    # 项目创建API（需要认证）
    re_path(r'^basic-project/?$', views.basic_project, name='basic_project'),
    re_path(r'^text-segment/?$', views.text_segment, name='text_segment'),
    re_path(r'^text-animation/?$', views.text_animation, name='text_animation'),
    re_path(r'^text-effects/?$', views.text_effects, name='text_effects'),
    re_path(r'^audio-segment/?$', views.audio_segment, name='audio_segment'),
    re_path(r'^video-segment/?$', views.video_segment, name='video_segment'),
    re_path(r'^video-animation/?$', views.video_animation, name='video_animation'),
    re_path(r'^transition/?$', views.transition, name='transition'),
    re_path(r'^background-filling/?$', views.background_filling, name='background_filling'),
    re_path(r'^comprehensive/?$', views.comprehensive, name='comprehensive'),
    re_path(r'^comprehensive-create/?$', views.comprehensive_create, name='comprehensive_create'),
    # 文件和下载功能
    re_path(r'^download-from-url/?$', views.download_from_url, name='download_from_url'),
    re_path(r'^select-project-dir/?$', views.select_project_dir, name='select_project_dir'),
    re_path(r'^download-patch-simple/?$', views.download_patch_simple, name='download_patch_simple'),
    # 兼容旧API接口
    re_path(r'^get-projects/?$', views.get_projects, name='get_projects'),
    re_path(r'^get-dashboard-data/?$', views.get_dashboard_data, name='get_dashboard_data'),
]
