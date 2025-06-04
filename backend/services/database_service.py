#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库服务类
"""
from contextlib import contextmanager
from datetime import datetime
from typing import Dict, List, Any, Optional

from config.database import engine, SessionLocal
from logs.logger import setup_logger
from models.asset import Asset
from models.project import Project
from models.user import User
from sqlalchemy import desc, and_, func
from sqlalchemy.orm import sessionmaker, Session

logger = setup_logger('DatabaseService')

class DatabaseService:
    """数据库服务类"""
    
    def __init__(self):
        self.db: Session = SessionLocal()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.db.rollback()
        self.db.close()
    
    # 项目相关操作
    def create_project(self, project_data: Dict[str, Any]) -> Project:
        """创建项目"""
        try:
            project = Project(
                name=project_data.get('name', f'项目_{datetime.now().strftime("%Y%m%d_%H%M%S")}'),
                description=project_data.get('description', ''),
                type=project_data.get('type', 'basic-project'),
                status='draft',
                config=project_data.get('config', {}),
                draft_content=project_data.get('draft_content'),
                width=project_data.get('width', 1920),
                height=project_data.get('height', 1080),
                duration=project_data.get('duration'),
                output_path=project_data.get('output_path'),
                user_id=project_data.get('user_id', 1)
            )
            
            self.db.add(project)
            self.db.commit()
            self.db.refresh(project)
            
            logger.info(f"✅ 项目创建成功: {project.name} (ID: {project.id})")
            return project
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ 项目创建失败: {e}")
            raise
    
    def get_project(self, project_id: int) -> Optional[Project]:
        """获取项目"""
        return self.db.query(Project).filter(Project.id == project_id).first()
    
    def get_projects(self, user_id: int = 1, limit: int = 50, offset: int = 0) -> List[Project]:
        """获取项目列表"""
        return (self.db.query(Project)
                .filter(Project.user_id == user_id)
                .order_by(desc(Project.updated_at))
                .offset(offset)
                .limit(limit)
                .all())
    
    def update_project(self, project_id: int, update_data: Dict[str, Any]) -> Optional[Project]:
        """更新项目"""
        try:
            project = self.get_project(project_id)
            if not project:
                return None
            
            for key, value in update_data.items():
                if hasattr(project, key):
                    setattr(project, key, value)
            
            project.updated_at = datetime.now()
            self.db.commit()
            self.db.refresh(project)
            
            logger.info(f"✅ 项目更新成功: {project.name} (ID: {project.id})")
            return project
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ 项目更新失败: {e}")
            raise
    
    def delete_project(self, project_id: int) -> bool:
        """删除项目"""
        try:
            project = self.get_project(project_id)
            if not project:
                return False
            
            self.db.delete(project)
            self.db.commit()
            
            logger.info(f"✅ 项目删除成功: {project.name} (ID: {project.id})")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ 项目删除失败: {e}")
            return False
    
    # 素材相关操作
    def create_asset(self, asset_data: Dict[str, Any]) -> Asset:
        """创建素材"""
        try:
            asset = Asset(
                filename=asset_data['filename'],
                original_name=asset_data.get('original_name'),
                file_path=asset_data.get('file_path'),
                file_size=asset_data.get('file_size'),
                type=asset_data['type'],
                source=asset_data.get('source', 'upload'),
                duration=asset_data.get('duration'),
                width=asset_data.get('width'),
                height=asset_data.get('height'),
                download_url=asset_data.get('download_url'),
                project_id=asset_data.get('project_id')
            )
            
            self.db.add(asset)
            self.db.commit()
            self.db.refresh(asset)
            
            logger.info(f"✅ 素材创建成功: {asset.filename} (ID: {asset.id})")
            return asset
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ 素材创建失败: {e}")
            raise
    
    def get_assets_by_project(self, project_id: int) -> List[Asset]:
        """获取项目的素材列表"""
        return (self.db.query(Asset)
                .filter(Asset.project_id == project_id)
                .filter(Asset.is_active == True)
                .order_by(desc(Asset.created_at))
                .all())
    
    # 统计相关操作
    def get_project_stats(self, user_id: int = 1) -> Dict[str, Any]:
        """获取项目统计信息"""
        try:
            total_projects = self.db.query(Project).filter(Project.user_id == user_id).count()
            
            completed_projects = (self.db.query(Project)
                                 .filter(Project.user_id == user_id)
                                 .filter(Project.status == 'completed')
                                 .count())
            
            processing_projects = (self.db.query(Project)
                                 .filter(Project.user_id == user_id)
                                 .filter(Project.status == 'processing')
                                 .count())
            
            draft_projects = (self.db.query(Project)
                            .filter(Project.user_id == user_id)
                            .filter(Project.status == 'draft')
                            .count())
            
            # 按类型统计
            type_stats = (self.db.query(Project.type, func.count(Project.id))
                         .filter(Project.user_id == user_id)
                         .group_by(Project.type)
                         .all())
            
            return {
                'total_projects': total_projects,
                'completed_projects': completed_projects,
                'processing_projects': processing_projects,
                'draft_projects': draft_projects,
                'type_distribution': {type_name: count for type_name, count in type_stats}
            }
            
        except Exception as e:
            logger.error(f"❌ 统计信息获取失败: {e}")
            return {}
    
    def get_recent_activities(self, user_id: int = 1, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最近活动"""
        try:
            recent_projects = (self.db.query(Project)
                             .filter(Project.user_id == user_id)
                             .order_by(desc(Project.updated_at))
                             .limit(limit)
                             .all())
            
            activities = []
            for project in recent_projects:
                activity = {
                    'title': f'项目操作: {project.name}',
                    'description': f'{project.type} 类型项目',
                    'time': project.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'status': project.status,
                    'project_id': project.id
                }
                activities.append(activity)
            
            return activities
            
        except Exception as e:
            logger.error(f"❌ 最近活动获取失败: {e}")
            return []
    
    # 用户相关操作
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """创建用户"""
        try:
            user = User(
                username=user_data['username'],
                password_hash=user_data['password_hash'],
                email=user_data.get('email'),
                nickname=user_data.get('nickname'),
                is_active=user_data.get('is_active', True)
            )
            
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"✅ 用户创建成功: {user.username} (ID: {user.id})")
            return user
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ 用户创建失败: {e}")
            raise
    
    def get_user(self, user_id: int) -> Optional[User]:
        """获取用户"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_users(self, limit: int = 50, offset: int = 0) -> List[User]:
        """获取用户列表"""
        return (self.db.query(User)
                .order_by(desc(User.created_at))
                .offset(offset)
                .limit(limit)
                .all())
    
    def update_user(self, user_id: int, update_data: Dict[str, Any]) -> Optional[User]:
        """更新用户"""
        try:
            user = self.get_user(user_id)
            if not user:
                return None
            
            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            user.updated_at = datetime.now()
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"✅ 用户更新成功: {user.username} (ID: {user.id})")
            return user
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ 用户更新失败: {e}")
            raise
    
    def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        try:
            user = self.get_user(user_id)
            if not user:
                return False
            
            self.db.delete(user)
            self.db.commit()
            
            logger.info(f"✅ 用户删除成功: {user.username} (ID: {user.id})")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ 用户删除失败: {e}")
            return False

@contextmanager
def get_database_service():
    """获取数据库服务实例（上下文管理器）"""
    service = DatabaseService()
    try:
        yield service
    except Exception as e:
        service.db.rollback()
        logger.error(f"❌ 数据库操作异常: {e}")
        raise
    finally:
        service.db.close()
