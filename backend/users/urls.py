from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    # 认证相关
    re_path(r'^register/?$', views.RegisterView.as_view(), name='register'),
    re_path(r'^login/?$', views.LoginView.as_view(), name='login'),
    re_path(r'^logout/?$', views.LogoutView.as_view(), name='logout'),
    re_path(r'^token/refresh/?$', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 用户资料
    re_path(r'^me/?$', views.UserProfileView.as_view(), name='user_profile'),
    re_path(r'^profile/?$', views.UserProfileView.as_view(), name='user_profile_alt'),
    re_path(r'^change-password/?$', views.ChangePasswordView.as_view(), name='change_password'),
    re_path(r'^stats/?$', views.user_stats, name='user_stats'),
]
