---
name: xinhe-marketing
description: 心河Paper内容营销自动化。使用 xinhe-marketing CLI 创建知乎文章和小红书图文，推入内容工厂草稿箱，由用户在前端审核后发布。覆盖素材查询、内容撰写、工厂推送的完整闭环。
category: productivity
platforms: [macos]
---

# 心河Paper 内容营销自动化

通过 xinhe-marketing CLI 工具，将 Hermes 撰写的内容推入心河内容工厂草稿箱。用户在前端审核、微调后发布。

## 核心原则

- Hermes 负责：数据分析 → 选题决策 → 内容撰写 → 推入工厂草稿箱
- 用户负责：在前端审核、微调、发布
- 工厂是内容中台（DB + 资产 + 前端界面），不内置 AI 逻辑
- 内容策略：VibeCoding/工具分享角度，避开「竞赛+解题/答案/保奖」等限流关键词
- 不用等用户确认内容细节——写好直接推。用户打开前端就能看到
- **数据看板优先CLI而非前端页面**：用户作为创始人需要管线状态 + 账号性能 + 内容归因三层视图，但偏好 `daily-brief` 风格的终端表格，而不是在浏览器里新建 Ant Design 页面。新建前端页面之前先增强 CLI 输出
- **绝不编造数据**：URL、播放量、粉丝数等所有数字必须从浏览器实际提取或 API 返回。禁止凭空编造。用户对虚假数据零容忍（2026.6.16 会话中被严厉纠正过：知乎/B站/小红书/抖音/CSDN 的 URL 全部编造，B站频道级聚合数据被误当作单作品指标）

## CLI 架构与代码路径

### 架构哲学

```
xinhe-marketing-factory  = 内容中台（DB + 资产 + 人机界面）
xinhe-paper CLI           = 实时数据（模板热度、搜索缺口）
xinhe-marketing CLI       = 桥接层（连接工厂 + 数据源）
Hermes skill              = 决策引擎 + 内容生产调度
用户                      = 审批 + 微调 + 发布
```

工厂**不内置 AI 管理逻辑**。Hermes 通过 HTTP API 和 CLI 读写工厂数据。工厂前端只用于"看一眼、微调、发"。

### CLI 安装

```bash
cd /Users/ming/project/xinhe-marketing-factory/cli
.venv/bin/python -m pip install -e .
```

需要 Python >= 3.11。venv 已在 `/Users/ming/project/xinhe-marketing-factory/cli/.venv/`。

### 配置文件

CLI 从 `cli/.env` 读取配置：

```env
FACTORY_BASE_URL=http://192.168.31.32:8195
API_TOKEN=sadklwqiesajdhqwe2sjahdq
```

配置正确后 `xinhe-marketing config` 应显示"API Token: 已设置"。所有 API 请求带 `Authorization: Bearer <token>` header。

### CLI 运行环境

```bash
# CLI 路径
CLI=/Users/ming/project/xinhe-marketing-factory/cli/.venv/bin/xinhe-marketing

# 运行前设置 PATH（xinhe-paper 依赖）
export PATH="/Users/ming/project/xinhe-marketing-factory/cli/.venv/bin:/Users/ming/project/cli_xinhe_status/.venv/bin:$PATH"
```

### 代码路径

| 组件 | 路径 |
|------|------|
| CLI 源码 | `/Users/ming/project/xinhe-marketing-factory/cli/xinhe_marketing/` |
| API 客户端 | `cli/xinhe_marketing/client.py` |
| CLI 命令 | `cli/xinhe_marketing/cli.py` |
| xinhe-paper 桥接 | `cli/xinhe_marketing/paper_cli.py` |
| 工厂后端 API | `/Users/ming/project/xinhe-marketing-factory/backend/app/api/v1/` |
| 工厂数据模型 | `/Users/ming/project/xinhe-marketing-factory/docs/architecture/data-model.md` |
| venv | `/Users/ming/project/xinhe-marketing-factory/cli/.venv/` |
| .env | `/Users/ming/project/xinhe-marketing-factory/cli/.env` |

## 工作流

### 1. 分析数据

```bash
$CLI daily-brief
```

输出：热门模板排行、已发布内容表现、可用选题库、社媒账号矩阵。

### 2. 查素材

```bash
$CLI list-materials --page-size 50
$CLI list-materials --keyword "模板"
```

用素材 COS URL 嵌入文章：`![描述](cos_url)`

### 3. 知乎长文

```bash
$CLI create-draft -t "标题" -c @/tmp/article.md -p zhihu -m "素材ID1,素材ID2"
```

规范：
- 标题干货感，结构：痛点→方法→案例→数据→行动号召
- 嵌入真实 COS 素材图，不用占位图
- 引用 xinhe-paper 真实数据
- 1500-2500字，Markdown格式
- 避开限流词：用「排版工具」「效率提升」「VibeCoding」替代「解题思路」「答案」「保奖」

### 4. 小红书图文

```bash
$CLI create-draft -t "标题" -c @/tmp/xhs_caption.md -p xiaohongshu --image-text --slides "$(cat /tmp/xhs_slides.json)"
```

规范：
- 标题网感+emoji+关键词
- 正文口语化，结构：情绪开场→1️⃣2️⃣3️⃣分点→数据/紧迫感→话题标签
- 每张 slide 用工厂素材库真实 COS 图片
- caption 350字以内，4-6个话题标签
- 封面自动从 slides[0] 取，不需手动传

### 5. 浏览器扩展分发

内容推入工厂后，通过「心河内容同步助手」Chrome 扩展完成跨平台分发：

```
工厂草稿箱 → 扩展侧边栏(🏭工厂按钮) → 选中文章 → 分发 → 注入编辑器 → 手动发布
```

扩展路径：`/Users/ming/project/content-distributor/`（Plasmo 框架，Chrome MV3）

核心流程：
- 侧边栏点"🏭 工厂" → 自动拉取工厂最新文章/图文列表
- 点一篇 → title/body 自动填入编辑区
- 选目标平台 → 点分发 → 扩展后台打开各平台编辑器 → content script 注入内容
- 手动确认发布 → 扩展回写工厂 `publications` 表

已适配平台（content scripts）：知乎(`zhihu.ts`)、CSDN、简书。完整版(`extension/`)另有 19 平台。

**知乎专栏注入要点**（`src/contents/zhihu.ts`）：
- 标题：`.WriteIndex-titleInput` textarea，native setter + dispatchEvent
- 正文：`.public-DraftEditor-content`（Draft.js），innerHTML + `input` + `change` + `blur` 事件序列

### 6. 上传素材

```bash
$CLI upload-material /path/to/image.png [--tags "配图,模板"]
```

上传文件到 COS + 注册到工厂素材库。支持图片/视频/文档。

### 7. 账号管理（摸底 + 更新）

**PITFALL**: 工厂里的账号数据可能严重过时（昵称、粉丝数、甚至账号名都不对）。做任何账号相关决策前，必须先用浏览器摸底验证。`get-account` CLI 命令返回 404（后端未实现），用直接 API 替代。

#### 7a. 账号摸底（浏览器验证）

用 WebBridge 打开各平台创作者中心，snapshot 提取真实数据。详见 `references/account-audit.md`（含全部创作者中心 URL 和每个平台的数据提取方法）。

核心流程：
```
WebBridge 打开创作者中心 → snapshot → 提取账号名/粉丝/数据 → 对比工厂 → API 更新
```

#### 7b. 列出账号（CLI + API 均可）

```bash
$CLI list-accounts [--status normal] [--platform zhihu]
```

或直接调 API：
```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://192.168.31.32:8195/api/v1/social-accounts?page_size=50"
```

API 返回含 `phone_number`、`primary_device`、`follower_count` 等完整字段。

#### 7c. 更新账号（直接 API，CLI 不可用）

`get-account` 和 `update-account` CLI 命令均返回 404。用直接 API：

```bash
# 更新
curl -s -X PUT "http://192.168.31.32:8195/api/v1/social-accounts/{id}" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"username":"新昵称","follower_count":1218,"persona":"新描述","remark":"浏览器实测"}'

# 创建（必须带 phone_number_id）
curl -s -X POST "http://192.168.31.32:8195/api/v1/social-accounts" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"username":"账号名","platform":"zhihu","phone_number_id":"UUID","follower_count":0,"status":"normal","remark":"浏览器实测"}'
```

创建新账号时必须提供 `phone_number_id`（可从已有账号的 API 返回中获取）。

### 8. 作品管理（新模块，替代发布追踪）

**CLI 命令** (2026.6.16 新增):
```bash
list-works    # 列出作品，支持 --platform --limit --page
get-work ID   # 查看详情(含账号+最新metrics)
create-work   # 创建作品，--upsert 模式防重复(需 --platform-content-id)
delete-work ID -y  # 软删除(-y 跳过确认)
```

**PITFALL: DELETE 后重新录入必须分页遍历** — `GET /works?page_size=100` 只返回前100条。超过100条时,要用循环检查 `resp.get('total')` 直到为0, 不能 while+break。

**PITFALL: create-work --upsert 需要 platform_content_id** — upsert 按 platform+platform_content_id 匹配,不是按标题。抖音/B站等有 content_id 的平台可用,小红书/视频号等无 content_id 的平台用不了。

**PITFALL: 聚合数据 vs 单作品数据** — 各平台创作者中心首页展示的是**频道级聚合数据**（近7日总计），不能当作单条作品的指标。

```bash
TOKEN=$(grep API_TOKEN /Users/ming/project/xinhe-marketing-factory/cli/.env | cut -d= -f2)

# 列出作品（支持 ?platform=&account_id=&status=&page=&page_size=）
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://192.168.31.32:8195/api/v1/works?page_size=20"

# 创建作品
curl -s -X POST "http://192.168.31.32:8195/api/v1/works" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"platform":"zhihu","account_id":"UUID","content_type":"article",
       "title":"文章标题","platform_url":"https://zhuanlan.zhihu.com/p/xxx",
       "platform_content_id":"xxx","published_at":"2026-06-04T12:00:00Z",
       "tags":["数模"],"status":"published"}'

# 获取详情（含 latest_metrics）
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://192.168.31.32:8195/api/v1/works/{id}"

# 追加 metrics（时序数据）
curl -s -X POST "http://192.168.31.32:8195/api/v1/works/{id}/metrics" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"view_count":366,"like_count":10,"comment_count":0,
       "share_count":0,"favorite_count":6,"collected_at":"2026-06-16T08:00:00Z"}'

# 删除作品（软删除）
curl -s -X DELETE -H "Authorization: Bearer $TOKEN" \
  "http://192.168.31.32:8195/api/v1/works/{id}"
```

#### 8b. 数据提取规则

**PITFALL: 聚合数据 vs 单作品数据** — 各平台创作者中心首页展示的是**频道级聚合数据**（近7日总计），不能当作单条作品的指标。必须进入内容管理/作品列表页，逐条提取。

| 平台 | 首页显示 | 单作品数据在哪 |
|------|---------|---------------|
| 知乎 | 近7日阅读/赞同/评论(聚合) | 首页「最新创作」区域，每条有独立阅读/赞同/评论/收藏 |
| B站 | 播放量/评论/点赞(聚合) | 内容管理 → 视频管理，每条有独立数据 |
| 抖音 | 播放量/主页访问(聚合) | 首页「最新作品」区域，单条有播放/点赞/评论/分享 |
| 小红书 | 曝光/观看/点赞(聚合) | 首页「最新笔记」区域，单条有观看/点赞/收藏/评论 |
| 视频号 | 昨日净增/新增播放(聚合) | 首页视频列表，单条有播放/点赞/评论/分享/收藏 |
| CSDN | — | 文章管理列表，单条有阅读/点赞/评论/收藏 |

#### 8c. URL 提取方法

**PITFALL: SPA 页面无法通过 evaluate 直接提取链接** — 小红书和抖音是 SPA，链接不是 `<a href>` 渲染的。需要用 snapshot 找到目标元素 → click 进入详情页 → 从详情页 URL bar 或 evaluate `window.location.href` 获取。

已验证的可直接提取平台：
- **知乎**：`evaluate` 遍历 `<a>` 标签，筛选 `href` 含 `zhuanlan.zhihu.com/p/` 的
- **B站**：`evaluate` 遍历 `<a>` 标签，筛选 `href` 含 `bilibili.com/video/BV` 的
- **CSDN**：`evaluate` 遍历 `<a>` 标签，筛选 `href` 含 `blog.csdn.net` + `article/details` 的
- **视频号**：目前无法提取公网 URL（视频号没有公开分享链接的机制）

不可直接提取的平台（SPA）：
- **小红书**：需 snapshot → 找到笔记卡片 → click → 等详情页加载 → evaluate `window.location.href`
- **抖音**：同上，需 snapshot → 找到视频卡片 → click → 等详情页 → evaluate `window.location.href`

完整技术手册见 `references/spa-data-extraction.md`（含各平台提取方法、失败记录、已测试的无效方法列表）。

全平台批量采集脚本见 `scripts/batch_collect_works.py`（可独立运行：`python3 scripts/batch_collect_works.py [平台名...]`）。

#### 8d. 定时同步（cron）

已有每日 8:00 cron job（job_id: 56c769c9354c，名称「每日账号数据同步」）。流程：
```
遍历各平台创作者中心 → snapshot 读账号数据 → PUT /social-accounts 更新粉丝
  → snapshot 读作品列表 → 新作品 POST /works → 已有作品 POST /works/{id}/metrics
```


#### 8e. 各平台采集器详解

每个平台的创作者中心有不同的DOM结构、滚动方式和stats映射。详细的平台采集配方见：

- **B站** → `references/bilibili-collector.md` — 标准翻页(10条/页)，Vue渲染必须evaluate，7项stats
- **小红书** → `references/xiaohongshu-collector.md` — 滚动`div.content`容器，stats无文字标签按SVG图标顺序映射
- **Spa通用技术** → `references/spa-data-extraction.md` — 各平台已验证/无效方法总览

全平台批量采集脚本：`scripts/batch_collect_works.py`

### 9. 查看配置

```bash
$CLI config
```

### 10. 用户审核

推入后输出工厂链接，用户打开：
- 预览 → 微调 → 发布

## 限流绕行

| 不要用 | 改用 |
|--------|------|
| 中青杯A题解题思路 | 数学建模论文排版避坑指南 |
| 中青杯B题参考答案 | 用VibeCoding速通数模赛题 |
| 保奖论文模板 | LaTeX模板一键套用 |

## 常见问题

- **图片哪来？** list-materials 查工厂素材库，用 COS URL
- **封面空？** 不传 cover_image_url，后端自动从 slides[0] 取（PR #1 已修复）
- **命令被拒？** 用 write_file 写到 /tmp/ 再 -c @/tmp/file.md 引用
- **浏览器分发扩展开发？** 见 `references/browser-extension-development.md`
- 知乎 Draft.js 注入？ 页面 JS 无法注入，必须用扩展 content script。见 reference 文件。
- Draft.js 注入失效？ 不要在 WebBridge evaluate 中直接设置 innerHTML——Draft.js 用 React 内部状态管理，页面上下文无法触发。必须走扩展的 content script（zhihu.ts）注入，它运行在隔离世界中有正确的事件序列。如果扩展未加载，先检查 `chrome://extensions` 确认扩展已启用并刷新
- **写视频口播稿/产品演示脚本？** 见 `references/video-script-conventions.md`——有硬约定：不说错定价、不编造功能、不写素材里没有的画面、不用真实平台数据
- **PATH 问题**：xinhe-paper CLI 不在 xinhe-marketing venv 的默认 PATH 中，直接运行 `daily-brief` 会报"xinhe-paper CLI 未安装"。必须加 PATH 前缀（见 CLI 运行环境）。
- **publications 接口不稳定**：工厂后端热更新后可能 502，首次失败先重试。
- **素材嵌入文章**：在 markdown 正文中用 `![描述](COS_URL)` 嵌入图片，同时通过 `-m` 参数传入 material_ids 建立数据库关联。不要只嵌图不关联，也不要只关联不嵌图。
- **账号数据过时？** 工厂里的账号名、粉丝数可能严重偏离实际（本次会话发现：知乎昵称完全不对、抖音粉丝差5倍、B站账号名完全不对）。做任何运营决策前，先用 WebBridge 打开创作者中心验证。账号摸底流程见 `references/account-audit.md`。
- **get-account / update-account 404？** CLI 这两个命令后端未实现。用直接 API 调 `/api/v1/social-accounts`（PUT 更新、POST 创建）。创建时必须带 `phone_number_id`。
