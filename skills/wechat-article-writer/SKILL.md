---
name: wechat-article-writer
description: 公众号/自媒体全流程。根据用户表述自动匹配：撰写文章、封面图、正文插图、风格提取。支持多种写作风格。当用户提到写公众号、技术博客、公众号封面、正文插图、步骤图、演示图、流程示意、分析写作风格、克隆文风、模仿爆款、提取风格时使用。详见 reference 目录。
---

# 公众号/自媒体创作

## 一、任务识别

根据用户需求选择执行路径：


| 任务类型    | 触发词                           | 执行                                                          |
| ------- | ----------------------------- | ----------------------------------------------------------- |
| 仅封面/结尾图 | 封面图、公众号封面、B站封面、小红书配图          | 读取 [cover_guide.md](reference/cover_guide.md)               |
| 仅正文插图   | 插图、步骤图、演示图、流程示意、前后对比          | 读取 [illustration_guide.md](reference/illustration_guide.md) |
| 撰写文章    | 写公众号、写文章、自媒体写作、爆款文章、内容创作      | 执行 Step 2–6                                                 |
| 风格提取    | 分析写作风格、克隆文风、模仿某篇、提取风格、范文转风格指南 | 执行「四、风格提取流程」                                                |


## 二、写作风格

撰写文章时，按用户指定选择风格文件；未指定则用默认风格。


| 序号  | 风格       | 触发词（互不重复）          | 参考文件                                                                           | 篇幅          |
| --- | -------- | ------------------ | ------------------------------------------------------------------------------ | ----------- |
| 1   | 默认       | （未指定时）             | [writing_style.md](reference/writing_style.md)                                 | 2000–4000 字 |
| 2   | 高流量/爆款   | 高流量、爆款、像 Skills 那篇 | [viral_style.md](reference/viral_style.md)                                     | 2500–4000 字 |
| 3   | 清单体/方法论  | 清单体、方法论、干货、步骤      | [checklist_methodology_style.md](reference/checklist_methodology_style.md)     | 2000–4000 字 |
| 4   | 资源盘点     | 盘点、替代方案、合集         | [resource_roundup_style.md](reference/resource_roundup_style.md)               | 3000–6000 字 |
| 5   | 个人实测推荐   | 个人实测、亲身推荐          | [personal_tool_review_style.md](reference/personal_tool_review_style.md)       | 4000–7000 字 |
| 6   | 认知颠覆     | 认知颠覆、反常识、观点文       | [contrarian_opinion_style.md](reference/contrarian_opinion_style.md)           | 2000–3500 字 |
| 7   | 身份共鸣/逆袭  | 身份共鸣、逆袭、你也行、转行经历   | [identity_transformation_style.md](reference/identity_transformation_style.md) | 2500–4000 字 |
| 8   | 故事化/情感共鸣 | 故事化、情感共鸣、人物故事      | [story_emotional_style.md](reference/story_emotional_style.md)                 | 2500–4500 字 |
| 9   | 深度随笔     | 深度思考、随笔、像日记那篇、个人感悟 | [personal_essay_style.md](reference/personal_essay_style.md)                   | 4000–7000 字 |


## 三、撰写流程（Step 2–6）

### Step 2：搜索资料

- 并行搜索多来源（官方文档、X/Twitter、Reddit、技术论坛等）
- 优先当月/当季最新资料
- 深度总结后再进入撰写

### Step 3：撰写文章

1. **读取风格文件**：按「二、写作风格」选择对应 reference 文件，严格遵循其写作规范与结尾语
2. **通用要求**：故事化开头、带情感色彩、准备 2–3 个备选标题
3. **去AI味（重要）**：写完后加载 `humanizer` skill 过一遍。核心规则：
   - 去掉"首先其次最后""此外""总而言之""值得注意的是"等机械连接词
   - 不用"至关重要""错综复杂""深刻认识到"等 AI 惯用空洞形容词
   - 不用 em dash（—）、不用 emoji 装饰标题、不用 bold 列表堆砌
   - 段落长短不一，信息密度疏密交替，不要每段"一样满"
   - 加入具体场景和故事（对话、时间、地点、数字），别只给观点
   - 开头用叙事钩子（烧烤摊对话、凌晨调格式），别用"在当今...""近年来..."
   - 用户偏好：直接务实、不端着、像给朋友讲产品，厌恶营销套话和推销感

### Step 4：生成标题

生成 5 个爆款风格标题：痛点明确、数字吸引、结果导向、情绪调动、悬念设置。

### Step 5：排版优化

输出排版与配图建议：段落结构、配图位置（封面/正文/结尾）、代码块留白、金句单独成段。

### Step 6：生成配图（可选）

用户要求或排版建议中标注配图时：

1. **读取指南**：
   - **封面/结尾图** → 读取 `reference/cover_guide.md`
   - **正文插图** → 读取 `reference/illustration_guide.md`
   - **漫画配图（故事性文章推荐）** → 读取 `reference/comic-article-combo.md`，用 baoyu-comic 生成极简手绘漫画嵌入文章中

2. **生成并保存 .drawio 文件**：
   - **必须保存**：生成完整的 mxGraph XML 内容并保存为文件
   - **封面图**保存为 `images/covers/source/主题关键词-cover.drawio`
   - **正文插图**保存为 `images/illustrations/source/主题关键词-图序号.drawio`
   - 配色与文章统一
   - 保存成功后告知用户文件路径

3. **自动转换为 PNG（可选）**：
   - 检查是否安装 draw.io CLI 工具
   - 如已安装：自动运行 `bash scripts/export-drawio.sh covers`，将 drawio 转为 PNG
   - 如未安装：提示用户手动导出或安装 draw.io CLI
   - PNG 保存到 `images/covers/export/` 或 `images/illustrations/export/`

4. **输出使用说明**：
   - 封面说明：布局用途与风格（1-2 句）
   - 文件路径：已保存的 .drawio 文件位置
   - 如果自动转换成功：PNG 文件位置
   - 如果需要手动导出：导出步骤说明

**图片文件夹结构**：
```
images/
├── covers/source/        # 封面 .drawio 文件（自动保存）✅
├── covers/export/        # 封面 PNG/JPG（自动或手动导出）
├── illustrations/source/ # 正文 .drawio 文件（自动保存）✅
└── illustrations/export/ # 正文 PNG/JPG（自动或手动导出）
```

**导出 PNG 方式**（三选一）：
1. **自动导出（推荐）**：如果已安装 draw.io CLI，系统会自动转换
2. **脚本导出**：手动运行 `bash scripts/export-drawio.sh covers`
3. **手动导出**：用 Draw.io 打开 → 文件 → 导出为 → PNG（2x 分辨率）

### 常见陷阱

**Obsidian 图片路径问题**：如果文章要放入 Obsidian vault，图片引用必须用 wikilink 格式 `![[assets/配图/xxx.png]]`（从 vault 根目录解析），不能用相对路径 `![alt](../assets/xxx.png)`。因为 Obsidian vault 里文章可能在多级子目录下，相对路径会断链。同时图片文件需复制到 vault 的 `assets/` 目录下。

### Step 7：上传到微信公众号（可选）

用户要求上传到草稿箱时执行，支持手动和自动两种模式。

#### **前置准备**

1. 确保图片已导出为 PNG/JPG 格式（Step 6）
2. 配置微信公众号凭证（仅自动模式需要）：
   ```bash
   # .env 文件
   WECHAT_APPID=your_app_id
   WECHAT_SECRET=your_app_secret
   ```

#### **模式 A：手动上传（零代码，推荐新手）**

1. **读取已生成的文件**：
   - 文章路径：`drafts/日期-主题.md`（Step 3 已保存）
   - 标题路径：`drafts/备选标题.txt`（Step 4 已保存）
   - 封面图：`images/covers/source/主题-cover.drawio`（Step 6 已保存）

2. **导出封面图**：
   - 用 Draw.io 打开 `.drawio` 文件
   - 文件 → 导出为 → PNG（2x 分辨率）
   - 保存到 `images/covers/export/`

3. **转换 Markdown 为微信格式**：
   - 打开 [Doocs MD 编辑器](https://md.openwrite.cn/)
   - 打开 `drafts/日期-主题.md`，复制全部内容
   - 粘贴到 Doocs MD 左侧编辑区
   - 选择主题样式（默认、橙心、姹紫等）
   - 右侧实时预览微信格式

4. **复制到公众号**：
   - 点击"复制"按钮
   - 打开公众号后台 → 新建图文 → 粘贴内容
   - 上传封面图（从 `images/covers/export/`）
   - 从 `备选标题.txt` 中选择标题
   - 保存为草稿或直接发布

**优点**：无需技术配置，即开即用，样式丰富，所有文件已自动生成
**适用场景**：偶尔发文、注重样式调整

#### **模式 B：自动上传（API 调用，推荐频繁发文）**

1. **读取已生成的文件**：
   - 文章：`drafts/日期-主题.md`（Step 3 已保存）
   - 封面：`images/covers/export/主题-cover.png`（需先导出）
   - 标题：从 `drafts/备选标题.txt` 中选择

2. **自动执行流程**：
   ```bash
   # 方式 1: 使用现成工具（推荐）
   npx wechat-article-publisher \
     --markdown drafts/2026-03-19-ai-tools.md \
     --cover images/covers/export/ai-tools-cover.png \
     --images images/illustrations/export/ \
     --auto-upload

   # 方式 2: 使用自定义脚本
   node scripts/upload-to-wechat.js \
     --title "2026 最全 AI 编程工具盘点：30+ 神器让代码写得飞起" \
     --content drafts/2026-03-19-ai-tools.md \
     --cover images/covers/export/ai-tools-cover.png
   ```

2. **自动化步骤**（脚本内部执行）：
   - 获取微信 access_token（自动缓存 7200 秒）
   - 上传封面图到素材库 → 获取 `thumb_media_id`
   - 上传正文图片 → 替换 Markdown 中的图片链接
   - 转换 Markdown → 微信 HTML（内联样式）
   - 调用草稿箱 API 创建草稿
   - 返回草稿 ID 和预览链接

3. **输出示例**：
   ```
   ✅ 草稿已上传成功！
   ✅ 草稿 media_id: Mzg5MjQ3NTg2Mg==_1234567890
   ✅ 请在公众号后台查看并发布
   ⏱️  耗时: 3.2 秒
   ```

**优点**：全自动化，批量发布，节省时间
**适用场景**：频繁发文、团队协作、内容矩阵

#### **注意事项**

⚠️ **限制条件**：
- 必须是已认证的公众号（个人号无法使用发布 API）
- 封面图 < 10MB，格式 JPG/PNG
- 正文图 < 2MB，格式 JPG/PNG/GIF

⚠️ **安全提醒**：
- 不要将 AppSecret 提交到 Git 仓库
- 使用 `.env` 文件或环境变量存储凭证
- Token 缓存后提前 5 分钟刷新，避免 40001 错误

⚠️ **发布限制（2025年7月起）**：
- 个人未认证账号：只能创建草稿，需手动发布
- 已认证账号：可调用发布 API 自动发布

## 四、风格提取流程

当用户提供样本文章（全文粘贴或本地路径），希望分析风格、克隆文风、将范文转为风格指南时执行。

**先读取** [extraction_dimensions.md](reference/extraction_dimensions.md)，按统一维度提取。

### Step 1：任务确认

- 样本数量（1 篇或多篇）
- 使用目标（模仿写作 / 团队风格规范 / Prompt 固化）
- 是否保留作者口头禅、品牌词

### Step 2：结构拆解

提取：开头钩子模式、行文骨架、段落节奏、结尾动作。

### Step 3：语言与修辞拆解

提取：语气人称、句式与标点、高频词/过渡词/口头禅、修辞手法。

### Step 4：产出风格规则包

输出必须包含：风格画像（100–200 字）、可执行规则（15–30 条，必须/优先/避免）、风格复刻 Prompt、反向自检清单、边界声明。

### Step 5：验证与回放（可选）

若用户需要：同主题试写大纲、100–200 字试写段落、相似点/差异点说明。

**输出顺序**：样本概况 → 风格画像 → 风格规则包 → Prompt 模板 → 自检清单 → 边界声明

## 五、写作风格偏好（用户定制）

本用户（心河Paper创始人）对公众号文章有以下明确偏好，写作时必须遵守：

1. **直接务实，拒绝营销套话**：不要用"你正在看的是..."、"传统写论文的痛，你我都经历过"这类开场白。不要用"新范式""颠覆""革命性"等大词。像在给朋友讲产品，不是推销。
2. **口语自然**：用短句，像聊天。不要堆砌术语炫技。
3. **有观点有态度**：文章要有自己的判断和方法论，不写"一方面...另一方面..."的骑墙文。
4. **适合数模/学术/技术类读者**：读者是大学生和研究生，内容要有实操性（具体步骤、时间分配、工具推荐），不要空洞道理。
5. **文章结构偏好**：直接开头（故事/场景/反常识观点）→ 方法步骤（编号清晰）→ 总结升华。每个部分要有"为什么"而不只是"做什么"。

## 六、文章评估框架（运营视角）

写完初稿后，从运营视角做一次自我评估。读取 `reference/article-evaluation.md` 获取完整框架。核心维度：

1. **情绪曲线**：读者从头到尾的情绪变化（共鸣→痛点→冲击→实用→紧迫→行动→金句）。中间不能"平"，情绪塌了读者会划走。
2. **钩子密度**：每个段落是否有钩子拉住读者？类型包括场景钩/数据钩/反常识钩/警示钩/金句钩。
3. **目的达成度**：文章每个核心目的（建立信任/传递方法/制造紧迫/促成转发）是否达成？
4. **完整性检查**：段落风格是否统一？关键信息是否被埋没？节奏是否割裂？

## 七、迭代工作流

当用户对质量要求高时，使用「生成 → 评估 → 生成」循环：

1. 写出初稿
2. 用「六、文章评估框架」逐项打分，找出薄弱段
3. 针对性修改（不是微调字句，是重构段落结构或叙事策略）
4. 输出新版，标注 v1→v2→v3
5. 每个版本存到 Obsidian 同一目录便于对比

v1→v2 通常修语气和AI味，v2→v3 修结构和痛感深度，v3→v4 修产品定位和事实准确性。

## 八、产品提及规范

提及心河Paper时，必须准确反映产品能力。产品是**在线 VibeCoding 写作空间**，不是模板下载站：

- ✅ 正确表述："在写作空间中选中模板""AI帮你分析赛题+出模型框架""LaTeX+Word双引擎在线编译""AI自动生成模型流程图和结果可视化"
- ❌ 禁止表述："下载模板""安装TexLive""导出LaTeX文件"
- 如果文章需要嵌入产品截图，通过 xinhe-marketing CLI 的 `list-materials` 查素材库，获取素材 ID 后用 `create-draft` 推入工厂时自动关联 COS 图片 URL。

## 九、示例


| 用户请求                                  | 执行                                          |
| ------------------------------------- | ------------------------------------------- |
| 生成这篇文章的封面                             | 读取 cover_guide.md，默认生成合并封面（1283×383）        |
| 生成 Cursor 启用四步骤的步骤图                   | 读取 illustration_guide.md 并生成                |
| 帮我写一篇关于 Cursor Skills 的公众号文章          | Step 2–6 完整流程                               |
| 用高流量风格写一篇关于 Vibe Coding 的文章，并上传到草稿箱 | 读取 viral_style.md，按爆款风格撰写 + Step 7 自动上传     |
| 用资源盘点风格写免费传大文件替代方案                    | 读取 resource_roundup_style.md，按盘点风格撰写        |
| 用深度随笔风格写 AI 时代记日记                     | 读取 personal_essay_style.md，按随笔风格撰写          |
| 用个人实测风格写软件推荐                          | 读取 personal_tool_review_style.md，按实测推荐风格撰写  |
| 用清单体写提升效率的 5 个习惯                      | 读取 checklist_methodology_style.md，按方法论风格撰写  |
| 用故事化风格写职场转型经历                         | 读取 story_emotional_style.md，按情感共鸣风格撰写       |
| 用认知颠覆风格写「努力是最被高估的品质」                  | 读取 contrarian_opinion_style.md，按反常识观点撰写     |
| 用身份共鸣风格写 30 岁转行做自媒体                   | 读取 identity_transformation_style.md，按逆袭叙事撰写 |
| 写完后帮我转换成微信格式                          | 执行 Step 7A（手动模式），输出 Doocs MD 使用指引          |
| 自动上传这篇文章到公众号                          | 执行 Step 7B（自动模式），调用微信 API 上传               |
| 分析这篇公众号文章的写作风格、提取可复用规则                | 执行「四、风格提取流程」                                |