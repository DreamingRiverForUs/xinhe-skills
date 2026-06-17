# 竞赛获奖匹配工作流

将心河Paper写作空间中的用户与实际竞赛获奖结果进行匹配。

## 适用场景

- 五一杯、数模国赛、美赛等竞赛出获奖名单后
- 想知道"使用我们模板的用户中有多少人获奖"
- 用于产品宣传素材（"使用心河Paper的XX队获一等奖"）

## 完整流水线

### Step 1: 查模板使用情况

```bash
xinhe-paper search-templates -k "五一杯" -l 20
# 拿到 template UUID
```

然后导出所有使用该模板的 paperID：

```python
# 绕过 search-sessions CLI 的 is_paid/isPaid bug
import asyncio
from xinhe_paper.db import db_session, safe_query
async with db_session():
    sessions = await safe_query(
        'SELECT id, title, "createdAt" FROM "ChatSession" WHERE "templateId" = $1 ORDER BY "createdAt" DESC',
        '<template_uuid>', limit=1000
    )
# 导出为 CSV: paperID, title, createdAt
```

### Step 2: 扫描写作空间提取队号

写作空间路径: `/mnt/nas/xinhe_paper/{paperID}/workspace/workspace/`

提取 `main.tex` 中的 `\baominghao{xxx}` 命令。

**重要坑**: 不要 fallback 到 `chapters/chapter1.tex`。该文件包含 `\begin{tcode}...\end{tcode}` 示例代码块，里面是模板教程用的 `\baominghao{4321}`，不是用户真实队号。如果 fallback 到这里，会把 156/421 条记录都标记为 `4321`。

正确做法：只扫 `main.tex`，且过滤掉注释行（`^[[:space:]]*%`）和占位符（`xxxx`, `xxxxxxxxxxxx`, `4321`）。

### Step 3: 解析获奖名单 PDF

获奖名单 PDF 是分页表格，pymupdf 提取纯文本后格式为：

```
队号
学校名
队员姓名
指导老师
获奖等级
```

提取逻辑：

```python
team_re = re.compile(r'^[ZBY]\d{8}$')  # Z=专科, B=本科, Y=研究生
award_re = re.compile(r'^(一等奖|二等奖|三等奖|成功参赛奖|未成功参赛)$')

# 找到每个队号后，往下找最近的奖项关键词（最多15行内）
```

输出: `team_number → award` 映射 CSV。

### Step 4: JOIN 匹配

将 Step 2 的 `paperID → team_number` 与 Step 3 的 `team_number → award` 做 join，得到 `paperID → award`。

由于队号格式可能不统一（用户可能填错），只匹配符合 `[ZBY]\d{8}` 格式的队号。

### 典型产出

| paperID | 队号 | 奖项 | 标题 |
|----------|------|------|------|

## 历史案例

### 2026 五一杯

- 模板: `00197479-0954-41c2-855c-bf61c6df2967` (五一杯数学建模竞赛推荐模板)
- 使用该模板的 paper: 421 个
- 填写了规范队号的: 13 个
- 匹配到获奖记录: 12 个 (1 二等奖, 7 三等奖, 4 成功参赛奖)
