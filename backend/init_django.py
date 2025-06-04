import os
import sys

import django
from django.core.management import execute_from_command_line


def main():
    """初始化Django项目"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jianying_web.settings')
    try:
        django.setup()
        
        print("📝 创建数据库迁移文件...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        
        print("🗄️  执行数据库迁移...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("📁 收集静态文件...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        
        print("👤 创建超级用户...")
        try:
            execute_from_command_line(['manage.py', 'createsuperuser'])
        except KeyboardInterrupt:
            print("跳过创建超级用户")
        
        print("✅ Django项目初始化完成！")
        print("🌐 可以运行以下命令启动开发服务器:")
        print("   python manage.py runserver 0.0.0.0:8000")

    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
