import os

import django
from django.core.management import execute_from_command_line


def main():
    """启动Django服务器"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jianying_web.settings')
    
    try:
        django.setup()
        print("=" * 50)
        print("🎬 pyJianYingDraft Django服务")
        print("🌐 地址: http://127.0.0.1:5000")
        print("=" * 50)
        
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == '__main__':
    main()
