# xinhe-marketing CLI 与 Factory API 映射

> 更新: 2026-06-09 | 本文件记录 CLI 命令与后端 API 的完整映射关系

## 已实现的 CLI 命令

| CLI 命令 | HTTP 调用 | 说明 |
|---------|----------|------|
| `daily-brief` | 见下方 | 综合四个数据源 |
| `create-draft` (文章) | POST /api/v1/articles | 推文章草稿 |
| `create-draft --image-text` | POST /api/v1/image-text-works | 推图文草稿 |
| `review` | GET /api/v1/publications | 发布数据复盘 |
| `list-accounts` | GET /api/v1/social-accounts | 查看社媒账号矩阵 |
| `get-account <id>` | GET /api/v1/social-accounts/{id} | 单账号详情 |
| `update-account <id>` | PUT /api/v1/social-accounts/{id} | 更新账号状态/人设 |

### daily-brief 数据源拆解

| 面板 | 数据来源 | 方式 |
|------|---------|------|
| 热门模板 | xinhe-paper top-templates | subprocess |
| 发布表现 | GET /api/v1/publications?status=published,tracking | FactoryClient |
| 选题库 | GET /api/v1/topics?status=approved | FactoryClient |
| 社媒账号 | GET /api/v1/social-accounts?status=normal | FactoryClient |

## CLI 待补齐命令

这些 Factory API 已就绪，client.py 有对应方法，但 CLI 入口未写：

### list-materials（高优先级）

```python
# client.py 已有方法
def list_materials(self, page=1, page_size=20) -> dict
```

**API**: GET /api/v1/materials?page=&page_size=

**用途**: 写文章前查素材库，找到合适的配图。素材库现66个素材（论文写作截图为主）。

### upload-material（中优先级）

**API**: POST /api/v1/materials (multipart form-data)

**用途**: 上传新素材到 COS + 工厂素材库。

## 素材库现状

- 总数: 66 个
- 类型: 图片 (PNG), 论文/教程截图为主
- COS: `xinhepaperdev-1257733029.cos.ap-shanghai.myqcloud.com`
- 示例文件名: 模型假设、问题重述、优化对比、AI检测、Bootstrap验证等

## 工厂认证

所有 API 调用使用 `Authorization: Bearer <API_TOKEN>` 请求头。
