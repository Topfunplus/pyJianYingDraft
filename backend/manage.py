#!/usr/bin/env python
import os
import sys


# 这个脚本是 Django 的管理脚本，用于执行各种管理任务，如运行服务器、迁移数据库等。
# 它通常位于 Django 项目的根目录下。
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jianying_web.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
