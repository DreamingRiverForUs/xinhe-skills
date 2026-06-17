# xinhe-marketing-factory API 清单

路径: `/Users/ming/project/xinhe-marketing-factory/`
repo: `DreamingRiverForUs/xinhe-marketing-factory`

## 认证

工厂使用 JWT 认证（前端登录）。建议新增 `API_TOKEN` 环境变量 + 中间件：
`Authorization: Bearer $API_TOKEN` → 放行，无需走 jwt/login 流程。

## Hermes 需用的端点 (新增 works 模块)

### 作品管理 (works) — 2026.6.16 新模块

- `GET /api/v1/works` — 列表 `?platform=&account_id=&status=published&page=&page_size=`
- `GET /api/v1/works/{id}` — 详情含 `latest_metrics` 和关联 `account`
- `POST /api/v1/works` — 创建 `{platform, account_id, content_type, title, platform_url, platform_content_id, published_at, tags, status}`
- `PUT /api/v1/works/{id}` — 更新
- `DELETE /api/v1/works/{id}` — 软删除
- `POST /api/v1/works/{id}/metrics` — 追加 metrics 记录 `{view_count, like_count, comment_count, share_count, favorite_count, collected_at}`
- `GET /api/v1/works/{id}/metrics` — 获取历史 metrics 列表

### 社媒账号 (social_accounts)

- `GET /api/v1/social-accounts?page_size=50` — 列表（含 phone_number, primary_device, follower_count）
- `PUT /api/v1/social-accounts/{id}` — 更新账号信息
- `POST /api/v1/social-accounts` — 创建（**必须带 phone_number_id**）

### 文章管理 (articles)

- `POST /api/v1/articles` — 创建草稿 `{title, content, material_ids}`
- `GET /api/v1/articles` — 列表 `?keyword=&page=&page_size=`
- `PUT /api/v1/articles/{id}` — 修改 `{title?, content?}`

### 选题库 (topics)

- `GET /api/v1/topics` — 列表 `?status=approved&page=&page_size=`

### 素材库 (materials)

- `GET /api/v1/materials` — 列表 `?page=&page_size=`

### 图文作品 (image_text_works)

- `POST /api/v1/image_text_works` — 创建小红书图文

## 已废弃的模块

- `/publications/*` — 已废弃（依赖死掉的 MediaCrawlerPro，数据全空）。由 `/works/*` 替代。
- `/auth/*` — Hermes 用 API Token，不走登录
- `/cookie_accounts/*` — Cookie管理（非 Hermes 使用）
- `/phone_numbers/*` — 手机号管理（仅创建账号时引用其 UUID）
