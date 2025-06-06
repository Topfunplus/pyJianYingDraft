from django.urls import path
from . import views


# 这个是用来定义用户管理相关的 URL 路由
# 主要是供管理员使用的功能
urlpatterns = [
    # 用户管理（管理员功能）
    path('', views.UserListView.as_view(), name='user_management_list'),
    path('<int:pk>/', views.UserDetailView.as_view(),
         name='user_management_detail'),
]
