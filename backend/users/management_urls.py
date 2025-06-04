from django.urls import path
from . import views

urlpatterns = [
    # 用户管理（管理员功能）
    path('', views.UserListView.as_view(), name='user_management_list'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user_management_detail'),
]
