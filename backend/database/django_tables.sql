-- Django 项目数据库表结构
-- 数据库: jianying_draft

-- 用户表 (Django 扩展用户模型)
CREATE TABLE `users_user` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `password` varchar(128) NOT NULL,
    `last_login` datetime(6) DEFAULT NULL,
    `is_superuser` tinyint(1) NOT NULL,
    `username` varchar(150) NOT NULL UNIQUE,
    `first_name` varchar(150) NOT NULL,
    `last_name` varchar(150) NOT NULL,
    `email` varchar(254) NOT NULL,
    `is_staff` tinyint(1) NOT NULL,
    `is_active` tinyint(1) NOT NULL,
    `date_joined` datetime(6) NOT NULL,
    `nickname` varchar(50) NOT NULL,
    `phone` varchar(20) NOT NULL,
    `avatar` varchar(200) NOT NULL,
    `is_admin` tinyint(1) NOT NULL DEFAULT 0,
    `last_login_ip` char(39) DEFAULT NULL,
    `created_at` datetime(6) NOT NULL,
    `updated_at` datetime(6) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `users_user_username_idx` (`username`),
    KEY `users_user_email_idx` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 用户配置表
CREATE TABLE `users_userprofile` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `theme` varchar(20) NOT NULL DEFAULT 'light',
    `language` varchar(10) NOT NULL DEFAULT 'zh-CN',
    `timezone` varchar(50) NOT NULL DEFAULT 'Asia/Shanghai',
    `notifications_enabled` tinyint(1) NOT NULL DEFAULT 1,
    `user_id` bigint NOT NULL UNIQUE,
    PRIMARY KEY (`id`),
    CONSTRAINT `users_userprofile_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户配置表';

-- 项目表
CREATE TABLE `api_project` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `name` varchar(200) NOT NULL,
    `description` longtext NOT NULL,
    `type` varchar(50) NOT NULL,
    `status` varchar(20) NOT NULL DEFAULT 'draft',
    `config` json DEFAULT NULL,
    `draft_content` json DEFAULT NULL,
    `width` int NOT NULL DEFAULT 1920,
    `height` int NOT NULL DEFAULT 1080,
    `duration` varchar(50) NOT NULL,
    `output_path` varchar(500) NOT NULL,
    `file_size` decimal(10,2) DEFAULT NULL,
    `user_id` bigint NOT NULL,
    `created_at` datetime(6) NOT NULL,
    `updated_at` datetime(6) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `api_project_user_id_idx` (`user_id`),
    KEY `api_project_type_idx` (`type`),
    KEY `api_project_status_idx` (`status`),
    KEY `api_project_created_at_idx` (`created_at`),
    CONSTRAINT `api_project_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='项目表';

-- 素材文件表
CREATE TABLE `api_assets` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `name` varchar(200) NOT NULL,
    `filename` varchar(200) NOT NULL,
    `file_type` varchar(20) NOT NULL,
    `file_path` varchar(500) NOT NULL,
    `file_size` bigint NOT NULL,
    `duration` double DEFAULT NULL,
    `width` int DEFAULT NULL,
    `height` int DEFAULT NULL,
    `url` varchar(200) DEFAULT NULL,
    `user_id` bigint DEFAULT NULL,
    `created_at` datetime(6) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `api_assets_user_id_idx` (`user_id`),
    KEY `api_assets_file_type_idx` (`file_type`),
    KEY `api_assets_created_at_idx` (`created_at`),
    CONSTRAINT `api_assets_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='素材文件表';

-- Django 系统表
CREATE TABLE `django_migrations` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `app` varchar(255) NOT NULL,
    `name` varchar(255) NOT NULL,
    `applied` datetime(6) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `django_content_type` (
    `id` int NOT NULL AUTO_INCREMENT,
    `app_label` varchar(100) NOT NULL,
    `model` varchar(100) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `django_content_type_app_label_model_uniq` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `auth_permission` (
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `content_type_id` int NOT NULL,
    `codename` varchar(100) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `auth_permission_content_type_id_codename_uniq` (`content_type_id`,`codename`),
    CONSTRAINT `auth_permission_content_type_id_fk` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `users_user_groups` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `user_id` bigint NOT NULL,
    `group_id` int NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `users_user_groups_user_id_group_id_uniq` (`user_id`,`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `users_user_user_permissions` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `user_id` bigint NOT NULL,
    `permission_id` int NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `users_user_user_permissions_user_id_permission_id_uniq` (`user_id`,`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- JWT 黑名单表 (如果使用 djangorestframework-simplejwt)
CREATE TABLE `token_blacklist_outstandingtoken` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `token` longtext NOT NULL,
    `created_at` datetime(6) DEFAULT NULL,
    `expires_at` datetime(6) NOT NULL,
    `user_id` bigint DEFAULT NULL,
    `jti` varchar(255) NOT NULL UNIQUE,
    PRIMARY KEY (`id`),
    KEY `token_blacklist_outstandingtoken_user_id_idx` (`user_id`),
    KEY `token_blacklist_outstandingtoken_jti_idx` (`jti`),
    CONSTRAINT `token_blacklist_outstandingtoken_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `token_blacklist_blacklistedtoken` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `blacklisted_at` datetime(6) NOT NULL,
    `token_id` bigint NOT NULL UNIQUE,
    PRIMARY KEY (`id`),
    CONSTRAINT `token_blacklist_blacklistedtoken_token_id_fk` FOREIGN KEY (`token_id`) REFERENCES `token_blacklist_outstandingtoken` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
