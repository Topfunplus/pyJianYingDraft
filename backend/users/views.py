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
    ChangePasswordSerializer
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
                    'token': str(refresh.access_token)
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
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # 更新最后登录IP
            user.last_login_ip = self.get_client_ip(request)
            user.save(update_fields=['last_login_ip'])
            
            refresh = RefreshToken.for_user(user)
            logger.info(f"✅ 用户登录成功: {user.username} (ID: {user.id})")
            
            return Response({
                'success': True,
                'message': '登录成功',
                'data': {
                    'user': UserSerializer(user).data,
                    'token': str(refresh.access_token)
                }
            })
        
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
        return Response({
            'success': True,
            'data': UserSerializer(request.user).data
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
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_admin or self.request.user.is_superuser:
            return User.objects.all().order_by('-created_at')
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return super().get_permissions()

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """用户详情管理"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_admin or self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """用户统计信息"""
    user = request.user
    
    # 用户项目统计
    project_stats = Project.objects.filter(user=user).aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='completed')),
        processing=Count('id', filter=Q(status='processing')),
        draft=Count('id', filter=Q(status='draft'))
    )
    
    # 最近7天的项目数量
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
                'join_date': user.date_joined,
                'last_login': user.last_login,
                'is_admin': user.is_admin
            }
        }
    })
