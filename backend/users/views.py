import logging
from datetime import datetime, timedelta

from api.models import Project
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserSerializer, UserRegistrationSerializer, LoginSerializer,
    ChangePasswordSerializer, UserManagementSerializer
)

User = get_user_model()
logger = logging.getLogger('api')


class RegisterView(APIView):
    """用户注册"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        logger.info(f"📝 注册请求数据: {request.data}")

        # 处理字段名映射 - 支持前端发送的 confirmPassword
        data = request.data.copy()
        if 'confirmPassword' in data and 'password_confirm' not in data:
            data['confirmPassword'] = data['confirmPassword']

        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            logger.info(f"✅ 新用户注册成功: {user.username} (ID: {user.id})")

            return Response({
                'success': True,
                'message': '注册成功',
                'data': {
                    'user': UserSerializer(user).data,
                    'token': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_201_CREATED)

        logger.error(f"❌ 注册失败，验证错误: {serializer.errors}")
        return Response({
            'success': False,
            'message': '注册失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """用户登录"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        logger.info(f"📝 登录请求数据: {request.data}")

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # 更新最后登录IP
            user.last_login_ip = self.get_client_ip(request)
            user.save(update_fields=['last_login_ip'])

            refresh = RefreshToken.for_user(user)
            logger.info(f"✅ 用户登录成功: {user.username} (ID: {user.id}) - 管理员: {user.is_admin or user.is_superuser}")

            return Response({
                'success': True,
                'message': '登录成功',
                'data': {
                    'user': UserSerializer(user).data,
                    'token': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            })

        logger.error(f"❌ 登录失败，验证错误: {serializer.errors}")
        return Response({
            'success': False,
            'message': '登录失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LogoutView(APIView):
    """用户登出"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            return Response({
                'success': True,
                'message': '登出成功'
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': f'登出失败: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """用户资料管理"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取当前用户信息"""
        user_data = UserSerializer(request.user).data
        logger.info(f"📝 用户 {request.user.username} 获取资料，权限: {user_data.get('permissions', {})}")

        return Response({
            'success': True,
            'data': user_data
        })

    def put(self, request):
        """更新用户资料"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"✅ 用户资料更新成功: {request.user.username} (ID: {request.user.id})")
            return Response({
                'success': True,
                'message': '资料更新成功',
                'data': serializer.data
            })

        return Response({
            'success': False,
            'message': '更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """修改密码"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            logger.info(f"✅ 用户密码修改成功: {user.username} (ID: {user.id})")

            return Response({
                'success': True,
                'message': '密码修改成功'
            })

        return Response({
            'success': False,
            'message': '密码修改失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListCreateAPIView):
    """用户列表管理（管理员功能）"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        # POST请求使用管理序列化器，GET请求使用普通序列化器
        if self.request.method == 'POST':
            from .serializers import UserManagementSerializer
            return UserManagementSerializer
        return UserSerializer

    def get_queryset(self):
        # 只有管理员可以看到所有用户，普通用户只能看到自己
        if self.request.user.is_admin or self.request.user.is_superuser:
            return User.objects.all().order_by('-created_at')
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        # 获取用户列表需要登录，创建用户需要管理员权限
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        """重写列表方法，返回格式化的用户列表"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        logger.info(f"📋 用户 {request.user.username} 获取用户列表，数量: {queryset.count()}")

        return Response({
            'success': True,
            'data': serializer.data,
            'total': queryset.count()
        })

    def create(self, request, *args, **kwargs):
        """重写创建方法，返回格式化响应"""
        # 检查用户权限
        if not (request.user.is_admin or request.user.is_superuser):
            return Response({
                'success': False,
                'message': '权限不足，只有管理员可以创建用户'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"✅ 管理员 {request.user.username} 创建用户成功: {user.username} (ID: {user.id})")

            return Response({
                'success': True,
                'message': '用户创建成功',
                'data': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)

        logger.error(f"❌ 用户创建失败，验证错误: {serializer.errors}")
        return Response({
            'success': False,
            'message': '用户创建失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """用户详情管理"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def get_queryset(self):
        # 只有管理员可以管理所有用户，普通用户只能管理自己
        if self.request.user.is_admin or self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        # 更新操作使用管理序列化器
        if self.request.method in ['PUT', 'PATCH']:
            from .serializers import UserManagementSerializer
            return UserManagementSerializer
        return UserSerializer

    def retrieve(self, request, *args, **kwargs):
        """重写详情方法，返回格式化的用户详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        logger.info(f"📋 用户 {request.user.username} 获取用户详情: {instance.username}")

        return Response({
            'success': True,
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        """重写更新方法，返回格式化响应"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 检查权限：管理员可以修改任何用户，普通用户只能修改自己
        if not (request.user.is_admin or request.user.is_superuser or instance.id == request.user.id):
            return Response({
                'success': False,
                'message': '权限不足，无法修改该用户信息'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"✅ 用户信息更新成功: {user.username} (ID: {user.id}) by {request.user.username}")

            return Response({
                'success': True,
                'message': '用户信息更新成功',
                'data': UserSerializer(user).data
            })

        return Response({
            'success': False,
            'message': '用户信息更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """重写删除方法，返回格式化响应"""
        instance = self.get_object()

        # 检查权限：只有管理员可以删除用户，且不能删除自己
        if not (request.user.is_admin or request.user.is_superuser):
            return Response({
                'success': False,
                'message': '权限不足，只有管理员可以删除用户'
            }, status=status.HTTP_403_FORBIDDEN)

        if instance.id == request.user.id:
            return Response({
                'success': False,
                'message': '不能删除自己的账户'
            }, status=status.HTTP_400_BAD_REQUEST)

        username = instance.username
        instance.delete()
        logger.info(f"✅ 管理员 {request.user.username} 删除用户成功: {username}")

        return Response({
            'success': True,
            'message': '用户删除成功'
        })


class UserManagementView(APIView):
    """用户管理视图 - 管理员功能"""
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """只有管理员可以访问"""
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get(self, request):
        """获取用户列表"""
        if not (request.user.is_admin or request.user.is_superuser):
            return Response({
                'success': False,
                'message': '权限不足，只有管理员可以查看用户列表'
            }, status=status.HTTP_403_FORBIDDEN)

        users = User.objects.all().order_by('-created_at')
        serializer = UserManagementSerializer(users, many=True)

        # 统计信息
        stats = {
            'total_users': users.count(),
            'active_users': users.filter(is_active=True).count(),
            'admin_users': users.filter(is_admin=True).count(),
            'recent_users': users.filter(created_at__gte=datetime.now() - timedelta(days=7)).count()
        }

        return Response({
            'success': True,
            'data': serializer.data,
            'stats': stats
        })

    def post(self, request):
        """创建新用户"""
        if not (request.user.is_admin or request.user.is_superuser):
            return Response({
                'success': False,
                'message': '权限不足，只有管理员可以创建用户'
            }, status=status.HTTP_403_FORBIDDEN)

        logger.info(f"📝 管理员 {request.user.username} 创建用户，数据: {request.data}")

        # 处理创建用户的数据
        data = request.data.copy()

        # 如果没有提供密码，使用默认密码
        if 'password' not in data or not data['password']:
            data['password'] = 'default123'

        serializer = UserManagementSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()

            # 记录日志
            logger.info(f"✅ 管理员 {request.user.username} 成功创建用户: {user.username} (ID: {user.id})")

            return Response({
                'success': True,
                'message': '用户创建成功',
                'data': UserManagementSerializer(user).data
            }, status=status.HTTP_201_CREATED)

        logger.error(f"❌ 创建用户失败，验证错误: {serializer.errors}")
        return Response({
            'success': False,
            'message': '用户创建失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserManagementDetailView(APIView):
    """用户详情管理视图"""
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """只有管理员可以访问"""
        return [permissions.IsAuthenticated(), permissions.IsAdminUser()]

    def get_object(self, pk):
        """获取用户对象"""
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        """获取单个用户详情"""
        user = self.get_object(pk)
        if not user:
            return Response({
                'success': False,
                'message': '用户不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        # 获取用户的项目统计
        from api.models import Project
        project_stats = Project.objects.filter(user=user).aggregate(
            total_projects=Count('id'),
            completed_projects=Count('id', filter=Q(status='completed')),
            processing_projects=Count('id', filter=Q(status='processing')),
            draft_projects=Count('id', filter=Q(status='draft'))
        )

        serializer = UserManagementSerializer(user)
        return Response({
            'success': True,
            'data': {
                **serializer.data,
                'project_stats': project_stats
            }
        })

    def put(self, request, pk):
        """更新用户信息"""
        user = self.get_object(pk)
        if not user:
            return Response({
                'success': False,
                'message': '用户不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = UserManagementSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"✅ 管理员 {request.user.username} 更新用户: {user.username}")

            return Response({
                'success': True,
                'message': '用户信息更新成功',
                'data': UserManagementSerializer(user).data
            })

        return Response({
            'success': False,
            'message': '更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """删除用户"""
        user = self.get_object(pk)
        if not user:
            return Response({
                'success': False,
                'message': '用户不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        # 防止删除自己
        if user.id == request.user.id:
            return Response({
                'success': False,
                'message': '不能删除自己的账户'
            }, status=status.HTTP_400_BAD_REQUEST)

        username = user.username
        user.delete()

        logger.info(f"✅ 管理员 {request.user.username} 删除用户: {username}")

        return Response({
            'success': True,
            'message': f'用户 {username} 删除成功'
        })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """用户统计信息"""
    user = request.user

    # 用户项目统计
    if user.is_admin or user.is_superuser:
        # 管理员可以看到所有统计
        project_stats = Project.objects.aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            processing=Count('id', filter=Q(status='processing')),
            draft=Count('id', filter=Q(status='draft'))
        )

        recent_projects = Project.objects.filter(
            created_at__gte=datetime.now() - timedelta(days=7)
        ).count()
    else:
        # 普通用户只能看到自己的统计
        project_stats = Project.objects.filter(user=user).aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            processing=Count('id', filter=Q(status='processing')),
            draft=Count('id', filter=Q(status='draft'))
        )

        recent_projects = Project.objects.filter(
            user=user,
            created_at__gte=datetime.now() - timedelta(days=7)
        ).count()

    return Response({
        'success': True,
        'data': {
            'project_stats': project_stats,
            'recent_projects': recent_projects,
            'user_info': {
                'username': user.username,
                'nickname': getattr(user, 'nickname', user.username),
                'join_date': user.date_joined,
                'last_login': user.last_login,
                'permissions': {
                    'is_admin': user.is_admin or user.is_superuser,
                    'is_superuser': user.is_superuser,
                    'can_manage_users': user.is_admin or user.is_superuser,
                    'can_access_api_debug': user.is_admin or user.is_superuser,
                    'can_view_all_projects': user.is_admin or user.is_superuser
                }
            }
        }
    })
