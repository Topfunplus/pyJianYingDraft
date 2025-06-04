from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, DECIMAL
from sqlalchemy.sql import func


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, comment="项目名称")
    description = Column(Text, comment="项目描述")
    type = Column(String(50), nullable=False, comment="项目类型")
    status = Column(String(20), default='draft', comment="项目状态")
    config = Column(JSON, comment="项目配置")
    draft_content = Column(JSON, comment="剪映草稿内容")
    
    # 项目属性
    width = Column(Integer, default=1920, comment="项目宽度")
    height = Column(Integer, default=1080, comment="项目高度")
    duration = Column(String(50), comment="项目总时长")
    output_path = Column(String(500), comment="输出文件路径")
    file_size = Column(DECIMAL(10, 2), comment="文件大小(MB)")
    
    # 关联用户
    user_id = Column(Integer, default=1, comment="用户ID")
    
    # 时间戳
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'status': self.status,
            'config': self.config,
            'draft_content': self.draft_content,
            'width': self.width,
            'height': self.height,
            'duration': self.duration,
            'output_path': self.output_path,
            'file_size': float(self.file_size) if self.file_size else None,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', type='{self.type}')>"
