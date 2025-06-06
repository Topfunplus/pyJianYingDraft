from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


# 这个类是用来 自定义用户模型在 Django 管理后台的显示方式

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'nickname',
                    'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'nickname')

    fieldsets = list(BaseUserAdmin.fieldsets) + [
        ('扩展信息', {
            'fields': ('nickname', 'avatar', 'phone', 'bio')
        }),
    ]

    add_fieldsets = list(BaseUserAdmin.add_fieldsets) + [
        ('扩展信息', {
            'fields': ('nickname', 'phone', 'bio')
        }),
    ]
