from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from users import views as user_views

urlpatterns = [
    # 健康检查（无需认证）
    re_path(r'^health/?$', views.health_check, name='health'),
    # 用户认证相关
    re_path(r'^auth/register/?$', user_views.RegisterView.as_view(), name='register'),
    re_path(r'^auth/login/?$', user_views.LoginView.as_view(), name='login'),
    re_path(r'^auth/logout/?$', user_views.LogoutView.as_view(), name='logout'),
    re_path(r'^auth/token/refresh/?$', TokenRefreshView.as_view(), name='token_refresh'),
    # 用户资料管理
    re_path(r'^auth/me/?$', user_views.UserProfileView.as_view(), name='user_profile'),
    re_path(r'^auth/profile/?$', user_views.UserProfileView.as_view(), name='user_profile_alt'),
    re_path(r'^auth/change-password/?$', user_views.ChangePasswordView.as_view(), name='change_password'),
    re_path(r'^auth/stats/?$', user_views.user_stats, name='user_stats'),
    # 用户管理（管理员功能）
    re_path(r'^users/?$', user_views.UserListView.as_view(), name='user_management_list'),
    re_path(r'^users/(?P<pk>\d+)/?$', user_views.UserDetailView.as_view(), name='user_management_detail'),
    # 仪表盘和统计（需要认证）
    re_path(r'^dashboard/?$', views.dashboard_data, name='dashboard_data'),
    re_path(r'^projects/?$', views.project_list, name='project_list'),
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
]
