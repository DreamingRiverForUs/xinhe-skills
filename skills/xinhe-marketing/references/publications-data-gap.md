# 发布追踪数据断链分析

## 原架构（已废弃）

```
内容生成 → 工厂(articles表) → publications表 → MediaCrawlerPro爬虫 → metrics写入
                                                   ↑
                                              挂了很久了（http://127.0.0.1:8990）
```

## 断链原因

1. **MediaCrawlerPro 爬虫服务已死** — `backend/app/services/crawler_client.py` 依赖 `MEDIAPRO_BASE_URL=http://127.0.0.1:8990`，该服务已停止运行
2. **publications 表数据全空** — 所有记录状态停留在 "tracking"，metrics 字段全为 `—`
3. **`review` 命令返回空** — `review -d 30` 输出「最近30天内没有发布数据」
4. **前端「发布追踪」页面 404** — `http://192.168.31.32:3566/tracking` 不存在

## 影响范围

- `backend/app/services/publication_service.py` — `submit_publication_crawl()` 和 `poll_publication_crawl()` 完全依赖爬虫
- `backend/app/services/crawler_scheduler.py` — 选题爬虫调度同样依赖
- `cli/xinhe_marketing/review.py` — `review` 命令查询 publications 表

## 解决方案

**新作品管理模块（works）完全替代 publications**：
- works 表不依赖爬虫，数据由 Hermes 通过浏览器采集
- work_metrics 表支持时序数据（每天一条，可看趋势）
- 与 articles/image_text_works 的关系改为可选关联（nullable FK）
- 定时任务每天 8:00 自动采集 metrics

## 迁移状态

- publications 表保留但不再使用
- 等 works 模块稳定运行后删除 publications 相关表
- 迁移脚本：`backend/migrations/migrate_publications_to_works.py`
