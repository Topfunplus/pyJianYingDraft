import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = '创建管理员用户'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='强制重新创建管理员用户（如果已存在则删除重建）',
        )

    def handle(self, *args, **options):
        # 从环境变量获取管理员信息
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_password = os.getenv('ADMIN_PASSWORD', 'Admin@123456')
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@jianying.com')
        admin_nickname = os.getenv('ADMIN_NICKNAME', '系统管理员')

        # 检查管理员是否已存在
        try:
            admin_user = User.objects.get(username=admin_username)
            if options['force']:
                admin_user.delete()
                self.stdout.write(
                    self.style.WARNING(f'已删除现有管理员用户: {admin_username}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'管理员用户 {admin_username} 已存在，使用 --force 参数强制重建')
                )
                return
        except User.DoesNotExist:
            pass

        # 创建管理员用户
        try:
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

            self.stdout.write(
                self.style.SUCCESS(f'✅ 管理员用户创建成功!')
            )
            self.stdout.write(f'用户名: {admin_username}')
            self.stdout.write(f'密码: {admin_password}')
            self.stdout.write(f'邮箱: {admin_email}')
            self.stdout.write(f'昵称: {admin_nickname}')
            self.stdout.write(
                self.style.WARNING('⚠️  请妥善保管管理员密码，建议首次登录后修改密码')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ 创建管理员用户失败: {str(e)}')
            )
