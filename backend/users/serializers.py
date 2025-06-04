from api.models import Project
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    # 添加权限相关字段
    permissions = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'phone', 'avatar', 'is_active', 
                 'is_admin', 'is_superuser', 'last_login', 'created_at', 'updated_at', 'permissions')
        read_only_fields = ('id', 'last_login', 'created_at', 'updated_at', 'permissions')
    
    def get_permissions(self, obj):
        """获取用户权限信息"""
        return {
            'is_admin': obj.is_admin or obj.is_superuser,
            'is_superuser': obj.is_superuser,
            'can_manage_users': obj.is_admin or obj.is_superuser,
            'can_access_api_debug': obj.is_admin or obj.is_superuser,
            'can_view_all_projects': obj.is_admin or obj.is_superuser
        }

class UserRegistrationSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirmPassword', 'nickname', 'phone')
        extra_kwargs = {
            'email': {'required': False},
            'nickname': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmPassword']:
            raise serializers.ValidationError("密码不匹配")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirmPassword', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        if validated_data.get('nickname'):
            user.nickname = validated_data['nickname']
            user.save()
        return user

class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('用户名或密码错误')
            if not user.is_active:
                raise serializers.ValidationError('用户账户已被禁用')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('必须提供用户名和密码')
        return attrs

class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError('新密码确认不匹配')
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("原密码错误")
        return value

class ProjectListSerializer(serializers.ModelSerializer):
    """项目列表序列化器"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Project
        fields = ('id', 'name', 'type', 'status', 'created_at', 'user_name', 'output_path')
        read_only_fields = ('id', 'created_at', 'user_name')

class UserManagementSerializer(serializers.ModelSerializer):
    """用户管理序列化器 - 用于管理员创建/管理用户"""
    password = serializers.CharField(write_only=True, required=False)
    permissions = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'phone', 'is_active', 
                 'is_admin', 'is_superuser', 'password', 'created_at', 'updated_at', 
                 'last_login', 'permissions')
        read_only_fields = ('id', 'created_at', 'updated_at', 'last_login', 'permissions')
        extra_kwargs = {
            'email': {'required': False},
            'nickname': {'required': False},
            'phone': {'required': False},
            'password': {'required': False}
        }
    
    def get_permissions(self, obj):
        """获取用户权限信息"""
        return {
            'is_admin': obj.is_admin or obj.is_superuser,
            'is_superuser': obj.is_superuser,
            'can_manage_users': obj.is_admin or obj.is_superuser,
            'can_access_api_debug': obj.is_admin or obj.is_superuser,
            'can_view_all_projects': obj.is_admin or obj.is_superuser
        }
    
    def create(self, validated_data):
        # 管理员创建用户时，如果没有提供密码，使用默认密码
        password = validated_data.pop('password', 'default123')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=password
        )
        
        # 设置其他字段
        for field, value in validated_data.items():
            setattr(user, field, value)
        
        user.save()
        return user
    
    def update(self, instance, validated_data):
        # 如果提供了新密码，更新密码
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        
        # 更新其他字段
        for field, value in validated_data.items():
            setattr(instance, field, value)
        
        instance.save()
        return instance
