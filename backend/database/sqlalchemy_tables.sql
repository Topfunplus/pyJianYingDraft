-- SQLAlchemy 模型数据库表结构
-- 数据库: jianying_draft

-- 用户表 (SQLAlchemy 模型)
CREATE TABLE `users` (
    `id` int NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL UNIQUE COMMENT '用户名',
    `password_hash` text NOT NULL COMMENT '密码哈希',
    `email` varchar(100) UNIQUE COMMENT '邮箱',
    `nickname` varchar(100) COMMENT '昵称',
    `is_active` tinyint(1) DEFAULT 1 COMMENT '是否激活',
    `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `last_login_at` datetime COMMENT '最后登录时间',
    PRIMARY KEY (`id`),
    KEY `idx_users_username` (`username`),
    KEY `idx_users_email` (`email`),
    KEY `idx_users_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 项目表 (SQLAlchemy 模型)
CREATE TABLE `projects` (
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(200) NOT NULL COMMENT '项目名称',
    `description` text COMMENT '项目描述',
    `type` varchar(50) NOT NULL COMMENT '项目类型',
    `status` varchar(20) DEFAULT 'draft' COMMENT '项目状态',
    `config` json COMMENT '项目配置',
    `draft_content` json COMMENT '剪映草稿内容',
    `width` int DEFAULT 1920 COMMENT '项目宽度',
    `height` int DEFAULT 1080 COMMENT '项目高度',
    `duration` varchar(50) COMMENT '项目总时长',
    `output_path` varchar(500) COMMENT '输出文件路径',
    `file_size` decimal(10,2) COMMENT '文件大小(MB)',
    `user_id` int DEFAULT 1 COMMENT '用户ID',
    `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_projects_user_id` (`user_id`),
    KEY `idx_projects_type` (`type`),
    KEY `idx_projects_status` (`status`),
    KEY `idx_projects_created_at` (`created_at`),
    CONSTRAINT `fk_projects_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='项目表';

-- 素材表 (SQLAlchemy 模型)
CREATE TABLE `assets` (
    `id` int NOT NULL AUTO_INCREMENT,
    `filename` varchar(200) NOT NULL COMMENT '文件名',
    `original_name` varchar(200) COMMENT '原始文件名',
    `file_path` varchar(500) COMMENT '文件路径',
    `file_size` decimal(10,2) COMMENT '文件大小(MB)',
    `type` varchar(20) NOT NULL COMMENT '素材类型',
    `source` varchar(20) DEFAULT 'upload' COMMENT '素材来源',
    `duration` varchar(50) COMMENT '时长',
    `width` int COMMENT '宽度',
    `height` int COMMENT '高度',
    `download_url` varchar(500) COMMENT '下载URL',
    `is_active` tinyint(1) DEFAULT 1 COMMENT '是否有效',
    `project_id` int COMMENT '关联项目ID',
    `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_assets_project_id` (`project_id`),
    KEY `idx_assets_type` (`type`),
    KEY `idx_assets_source` (`source`),
    KEY `idx_assets_created_at` (`created_at`),
    CONSTRAINT `fk_assets_project_id` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='素材表';

-- 插入默认用户数据
INSERT INTO `users` (`id`, `username`, `password_hash`, `email`, `nickname`, `is_active`) 
VALUES (1, 'admin', 'pbkdf2_sha256$600000$default$hash', 'admin@example.com', '管理员', 1);

