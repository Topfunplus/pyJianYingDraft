from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """扩展用户模型"""
    nickname = models.CharField(max_length=50, blank=True, verbose_name='昵称')
    phone = models.CharField(max_length=20, blank=True, verbose_name='手机号')
    avatar = models.URLField(blank=True, verbose_name='头像链接')
    is_admin = models.BooleanField(default=False, verbose_name='管理员')
    last_login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='最后登录IP')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-created_at']

class UserProfile(models.Model):
    """用户配置文件"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    theme = models.CharField(max_length=20, default='light', verbose_name='主题')
    language = models.CharField(max_length=10, default='zh-CN', verbose_name='语言')
    timezone = models.CharField(max_length=50, default='Asia/Shanghai', verbose_name='时区')
    notifications_enabled = models.BooleanField(default=True, verbose_name='启用通知')
    
    class Meta:
        verbose_name = '用户配置'
        verbose_name_plural = '用户配置'
