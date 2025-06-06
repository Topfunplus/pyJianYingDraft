from .models import Project
from .utils import (
    api_error_handler, create_basic_script, create_success_response,
    logger
)
import os
# 添加项目根目录到Python路径
import sys
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(requests):
    """健康检查接口"""
    return Response({
        "success": True,
        "message": "pyJianYingDraft API 服务正常运行",
        "version": "1.0.0",
        "timestamp": "2024-01-01T00:00:00Z"
    })


# @permission_classes([IsAuthenticated]) 表示API需要进行授权才可以访问

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@api_error_handler
def basic_project(request):
    """基础项目创建接口"""
    logger.info("🚀 开始创建基础项目")

    script = create_basic_script()
    # 保存到数据库时关联用户

    # objects.create 是 Django 模型的一个方法，用于创建一个新的模型实例并将其保存到数据库中
    project = Project.objects.create(
        user=request.user,
        name=f'基础项目_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
        type='basic-project',
        status='completed',
        draft_content=script.dumps() if hasattr(script, 'to_dict') else {})

    return create_success_response(
        "基础项目创建成功",
        project_info={
            "id": project.id,
            "name": project.name, "type": project.type}
    )
