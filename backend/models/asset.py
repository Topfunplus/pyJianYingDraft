from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, DECIMAL
from sqlalchemy.sql import func


class Asset(Base):
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(200), nullable=False, comment="文件名")
    original_name = Column(String(200), comment="原始文件名")
    file_path = Column(String(500), comment="文件路径")
    file_size = Column(DECIMAL(10, 2), comment="文件大小(MB)")
    type = Column(String(20), nullable=False, comment="素材类型")
    source = Column(String(20), default='upload', comment="素材来源")
    
    # 媒体属性
    duration = Column(String(50), comment="时长")
    width = Column(Integer, comment="宽度")
    height = Column(Integer, comment="高度")
    
    # 网络资源
    download_url = Column(String(500), comment="下载URL")
    
    # 状态
    is_active = Column(Boolean, default=True, comment="是否有效")
    
    # 关联项目
    project_id = Column(Integer, comment="关联项目ID")
    
    # 时间戳
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'filename': self.filename,
            'original_name': self.original_name,
            'file_path': self.file_path,
            'file_size': float(self.file_size) if self.file_size else None,
            'type': self.type,
            'source': self.source,
            'duration': self.duration,
            'width': self.width,
            'height': self.height,
            'download_url': self.download_url,
            'is_active': self.is_active,
            'project_id': self.project_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Asset(id={self.id}, filename='{self.filename}', type='{self.type}')>"
