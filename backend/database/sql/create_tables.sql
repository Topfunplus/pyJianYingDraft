-- 用户表
CREATE TABLE IF NOT EXISTS `users_customuser` (
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
    `nickname` varchar(50) DEFAULT NULL,
    `avatar` varchar(200) DEFAULT NULL,
    `phone` varchar(20) DEFAULT NULL,
    `is_admin` tinyint(1) NOT NULL DEFAULT 0,
    `last_login_ip` varchar(45) DEFAULT NULL,
    `created_at` datetime(6) NOT NULL,
    `updated_at` datetime(6) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 项目表
CREATE TABLE IF NOT EXISTS `api_project` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `name` varchar(200) NOT NULL,
    `type` varchar(50) NOT NULL,
    `status` varchar(20) NOT NULL DEFAULT 'draft',
    `draft_content` json DEFAULT NULL,
    `output_path` varchar(500) DEFAULT NULL,
    `created_at` datetime(6) NOT NULL,
    `updated_at` datetime(6) NOT NULL,
    `user_id` bigint NOT NULL,
    PRIMARY KEY (`id`),
    KEY `api_project_user_id_fk` (`user_id`),
    CONSTRAINT `api_project_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建索引
CREATE INDEX IF NOT EXISTS `idx_project_user_created` ON `api_project` (`user_id`, `created_at`);
CREATE INDEX IF NOT EXISTS `idx_project_status` ON `api_project` (`status`);
CREATE INDEX IF NOT EXISTS `idx_project_type` ON `api_project` (`type`);

-- 插入管理员用户数据 (密码: Admin@123456)
INSERT INTO `users_customuser` (
    `username`, `password`, `email`, `nickname`, `first_name`, `last_name`,
    `is_staff`, `is_superuser`, `is_active`, `is_admin`, 
    `date_joined`, `created_at`, `updated_at`
) VALUES (
    'admin', 
    'pbkdf2_sha256$600000$salt$hash', -- 这里应该是加密后的密码
    'admin@jianying.com', 
    '系统管理员', 
    '系统', 
    '管理员',
    1, 1, 1, 1, 
    NOW(), NOW(), NOW()
) ON DUPLICATE KEY UPDATE 
    `email` = VALUES(`email`),
    `nickname` = VALUES(`nickname`),
    `is_admin` = 1,
    `is_staff` = 1,
    `is_superuser` = 1,
    `updated_at` = NOW();
