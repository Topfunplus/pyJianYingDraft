from django.urls import path, re_path
from . import views

urlpatterns = [
    # 用户管理（管理员功能）
    re_path(r'^$', views.UserListView.as_view(), name='user_management_list'),
    re_path(r'^(?P<pk>\d+)/?$', views.UserDetailView.as_view(), name='user_management_detail'),
]
