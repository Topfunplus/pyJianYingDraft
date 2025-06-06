# API 文档

本目录包含 pyJianYingDraft API 的 OpenAPI 规范文档。

## 文件说明

- `openapi.yaml` - OpenAPI 3.0 规范文档，定义了所有API接口
- `README.md` - 本说明文件

## 查看文档

### 在线查看
1. 访问 [Swagger Editor](https://editor.swagger.io/)
2. 复制 `openapi.yaml` 的内容到编辑器中

### 本地查看
1. 安装 Swagger UI 或使用 VS Code 的 OpenAPI 扩展
2. 打开 `openapi.yaml` 文件

## API 概述

### 认证方式
API 使用 JWT (JSON Web Token) 进行身份验证：
1. 通过 `/api/auth/login` 获取访问令牌
2. 在请求头中添加：`Authorization: Bearer <access_token>`

### 主要功能模块

#### 1. 健康检查
- `GET /api/health` - 检查服务状态

#### 2. 用户认证
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/logout` - 用户登出
- `POST /api/auth/token/refresh` - 刷新令牌

#### 3. 用户资料管理
- `GET /api/auth/me` - 获取当前用户信息
- `PUT /api/auth/me` - 更新用户资料
- `POST /api/auth/change-password` - 修改密码
- `GET /api/auth/stats` - 获取用户统计信息

#### 4. 用户管理（管理员功能）
- `GET /api/users` - 获取用户列表（支持搜索、筛选、排序、分页）
- `POST /api/users` - 创建新用户
- `GET /api/users/{id}` - 获取用户详情
- `PUT /api/users/{id}` - 更新用户信息
- `DELETE /api/users/{id}` - 删除用户

##### 用户列表高级功能

**搜索功能：**
```bash
# 按关键词搜索（支持用户名、邮箱、昵称）
GET /api/users?search=admin
```

**筛选功能：**
```bash
# 筛选激活用户
GET /api/users?is_active=true

# 筛选管理员用户
GET /api/users?is_admin=true

# 筛选超级用户
GET /api/users?is_superuser=false

# 按注册日期范围筛选
GET /api/users?date_from=2024-01-01&date_to=2024-12-31
```

**排序功能：**
```bash
# 按用户名正序
GET /api/users?ordering=username

# 按创建时间倒序（默认）
GET /api/users?ordering=-created_at

# 按最后登录时间倒序
GET /api/users?ordering=-last_login
```

**分页功能：**
```bash
# 第1页，每页10条
GET /api/users?page=1&page_size=10

# 第2页，每页50条
GET /api/users?page=2&page_size=50
```

**组合查询示例：**
```bash
# 搜索激活的管理员用户，按用户名排序，每页20条
GET /api/users?search=admin&is_active=true&is_admin=true&ordering=username&page=1&page_size=20

# 查询2024年注册的普通用户，按注册时间倒序
GET /api/users?date_from=2024-01-01&date_to=2024-12-31&is_admin=false&ordering=-created_at
```

**响应格式示例：**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "nickname": "管理员",
      "is_active": true,
      "is_admin": true,
      "created_at": "2024-01-01T00:00:00Z",
      "last_login": "2024-01-02T10:30:00Z"
    }
  ],
  "pagination": {
    "total": 50,
    "page": 1,
    "page_size": 20,
    "total_pages": 3,
    "has_next": true,
    "has_previous": false
  },
  "filters": {
    "search": "admin",
    "is_active": "true",
    "is_admin": "true",
    "is_superuser": null,
    "date_from": null,
    "date_to": null,
    "ordering": "-created_at"
  }
}
```

## 权限说明

### 公开接口（无需认证）
- 健康检查
- 用户注册
- 用户登录

### 认证接口（需要登录）
- 用户资料管理
- 项目相关操作
- 用户统计信息

### 管理员接口（需要管理员权限）
- 用户管理（创建、删除用户等）
- 查看所有用户信息

## 响应格式

### 成功响应
```json
{
  "success": true,
  "message": "操作成功",
  "data": { ... }
}
```

### 错误响应
```json
{
  "success": false,
  "message": "错误信息",
  "errors": { ... }
}
```

## 状态码说明

- `200` - 操作成功
- `201` - 资源创建成功
- `400` - 请求参数错误
- `401` - 未授权（需要登录）
- `403` - 权限不足
- `404` - 资源不存在
- `500` - 服务器内部错误

## 查询参数说明

### 用户列表接口 (`GET /api/users`)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `search` | string | 否 | - | 搜索关键词，支持用户名、邮箱、昵称模糊搜索 |
| `is_active` | boolean | 否 | - | 筛选激活状态，true/false |
| `is_admin` | boolean | 否 | - | 筛选管理员状态，true/false |
| `is_superuser` | boolean | 否 | - | 筛选超级用户状态，true/false |
| `date_from` | date | 否 | - | 注册日期起始时间，格式：YYYY-MM-DD |
| `date_to` | date | 否 | - | 注册日期结束时间，格式：YYYY-MM-DD |
| `ordering` | string | 否 | -created_at | 排序字段，支持字段见下表 |
| `page` | integer | 否 | 1 | 页码，从1开始 |
| `page_size` | integer | 否 | 20 | 每页数量，最大100 |

### 支持的排序字段

| 字段 | 说明 |
|------|------|
| `id`, `-id` | 按ID正序/倒序 |
| `username`, `-username` | 按用户名正序/倒序 |
| `email`, `-email` | 按邮箱正序/倒序 |
| `nickname`, `-nickname` | 按昵称正序/倒序 |
| `created_at`, `-created_at` | 按创建时间正序/倒序 |
| `last_login`, `-last_login` | 按最后登录时间正序/倒序 |
| `is_active`, `-is_active` | 按激活状态正序/倒序 |
| `is_admin`, `-is_admin` | 按管理员状态正序/倒序 |
| `is_superuser`, `-is_superuser` | 按超级用户状态正序/倒序 |

**注意：** 字段名前加 `-` 表示倒序排列
