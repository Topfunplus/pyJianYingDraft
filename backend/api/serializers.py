from rest_framework import serializers

from .models import Project, Asset


class ProjectSerializer(serializers.ModelSerializer):
    """项目序列化器"""
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

class AssetSerializer(serializers.ModelSerializer):
    """素材文件序列化器"""
    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at')

class TextSegmentSerializer(serializers.Serializer):
    """文本片段请求序列化器"""
    text = serializers.CharField(default='这是一个文本测试')
    duration = serializers.CharField(default='3s')
    color = serializers.ListField(
        child=serializers.FloatField(),
        default=[1.0, 1.0, 0.0]
    )
    font = serializers.CharField(default='文轩体')

class AudioSegmentSerializer(serializers.Serializer):
    """音频片段请求序列化器"""
    duration = serializers.CharField(default='5s')
    volume = serializers.FloatField(default=0.6)
    fade_in = serializers.CharField(default='1s')

class VideoSegmentSerializer(serializers.Serializer):
    """视频片段请求序列化器"""
    duration = serializers.CharField(default='4.2s')

class ComprehensiveCreateSerializer(serializers.Serializer):
    """综合创作项目请求序列化器"""
    text = serializers.DictField(required=False)
    audio = serializers.DictField(required=False)
    video = serializers.DictField(required=False)
    animation = serializers.DictField(required=False)
    effects = serializers.DictField(required=False)
    transition = serializers.DictField(required=False)
