from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Project(models.Model):
    """项目模型"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('failed', '失败'),
    ]
    
    TYPE_CHOICES = [
        ('basic-project', '基础项目'),
        ('text-segment', '文本片段'),
        ('audio-segment', '音频片段'),
        ('video-segment', '视频片段'),
        ('comprehensive', '综合项目'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='项目名称')
    description = models.TextField(blank=True, verbose_name='项目描述')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name='项目类型')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='项目状态')
    
    # 项目配置
    config = models.JSONField(default=dict, blank=True, verbose_name='项目配置')
    draft_content = models.JSONField(default=dict, blank=True, verbose_name='剪映草稿内容')
    
    # 项目属性
    width = models.IntegerField(default=1920, verbose_name='项目宽度')
    height = models.IntegerField(default=1080, verbose_name='项目高度')
    duration = models.CharField(max_length=50, blank=True, verbose_name='项目总时长')
    output_path = models.CharField(max_length=500, blank=True, verbose_name='输出文件路径')
    file_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='文件大小(MB)')
    
    # 关联用户
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.name} ({self.type})'

class Asset(models.Model):
    """素材文件模型"""
    TYPE_CHOICES = [
        ('audio', '音频'),
        ('video', '视频'),
        ('image', '图片'),
        ('text', '文本'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='素材名称')
    filename = models.CharField(max_length=200, verbose_name='文件名')
    file_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='文件类型')
    file_path = models.CharField(max_length=500, verbose_name='文件路径')
    file_size = models.BigIntegerField(verbose_name='文件大小(字节)')
    duration = models.FloatField(blank=True, null=True, verbose_name='时长(秒)')
    width = models.IntegerField(blank=True, null=True, verbose_name='宽度')
    height = models.IntegerField(blank=True, null=True, verbose_name='高度')
    url = models.URLField(blank=True, null=True, verbose_name='源URL')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='上传用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'api_assets'
        verbose_name = '素材文件'
        verbose_name_plural = '素材文件'
        ordering = ['-created_at']
