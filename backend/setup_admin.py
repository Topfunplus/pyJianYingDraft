#!/usr/bin/env python
"""
快速创建管理员用户脚本
使用方法: python setup_admin.py
"""

import os
import sys
import django
from pathlib import Path

# 添加项目路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jianying_web.settings')
django.setup()

from django.contrib.auth import get_user_model
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

User = get_user_model()

def create_admin():
    """创建管理员用户"""
    # 从环境变量获取管理员信息
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_password = os.getenv('ADMIN_PASSWORD', 'Admin@123456')
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@jianying.com')
    admin_nickname = os.getenv('ADMIN_NICKNAME', '系统管理员')

    print("🚀 开始创建管理员用户...")
    
    # 检查管理员是否已存在
    if User.objects.filter(username=admin_username).exists():
        print(f"⚠️  管理员用户 '{admin_username}' 已存在")
        
        choice = input("是否要重新创建？(y/N): ").lower()
        if choice == 'y':
            User.objects.filter(username=admin_username).delete()
            print(f"🗑️  已删除现有管理员用户")
        else:
            print("❌ 取消操作")
            return

    try:
        # 创建管理员用户
        admin_user = User.objects.create_user(
            username=admin_username,
            email=admin_email,
            password=admin_password
        )
        
        # 设置管理员属性
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_admin = True
        admin_user.nickname = admin_nickname
        admin_user.save()

        print("✅ 管理员用户创建成功!")
        print("=" * 40)
        print(f"用户名: {admin_username}")
        print(f"密码: {admin_password}")
        print(f"邮箱: {admin_email}")
        print(f"昵称: {admin_nickname}")
        print("=" * 40)
        print("⚠️  请妥善保管管理员密码，建议首次登录后修改密码")
        
    except Exception as e:
        print(f"❌ 创建管理员用户失败: {str(e)}")

if __name__ == '__main__':
    create_admin()
