# GitHub 模板仓库盘点工作流

## 用途

对比 iftaken GitHub 仓库与心河Paper 平台已上线模板，找出尚未投放的模板仓库。

## 步骤

### 1. 拉取平台模板（含 GitHub repo 信息）

`search-templates` CLI 需要 `-k` 参数，无法列全表。用 `safe_query` 直查：

```bash
cd /Users/ming/project/cli_xinhe_status && .venv/bin/python -c "
import asyncio, json
from xinhe_paper.db import db_session, safe_query

async def main():
    async with db_session():
        templates = await safe_query(
            'SELECT id, name, status, \"remoteConfig\", \"sourceType\", \"commitHash\" FROM \"PaperTemplate\" ORDER BY status, name',
            limit=200
        )
        for t in templates:
            rc = t.get('remoteConfig') or {}
            if isinstance(rc, str):
                rc = json.loads(rc)
            url = rc.get('url', '')
            repo = ''
            if 'github.com' in url:
                repo = url.split('github.com/')[-1].replace('.git', '').rstrip('/')
            print(f\"[{t['status']:12}] {t['name'][:60]} | repo={repo}\")

asyncio.run(main())
"
```

### 2. 拉取 iftaken 仓库列表

```bash
gh repo list iftaken --limit 300 --json name,description,isPrivate
```

### 3. 交叉对比

- 提取所有看起来像 LaTeX 模板的仓库名（排除 AI/爬虫/学习笔记等非模板仓库）
- 匹配 `remoteConfig.url` 中以 `iftaken/` 开头的仓库
- 差集 = 未上线模板

### 4. 边界情况

- **同一个模板在 iftaken 和 XinhePaper 都有仓库**：如 CUG-thesis, HZAU_TEMPLATE, CQUPT-thesis, xinhe-thesis。这些已通过 XinhePaper org 上线，iftaken 版本是转移/复制，不应计入"未上线"。
- **同一模板多个版本**：如 cjc-template vs cjc_latex_template（前者未上线，后者已上线），hnie-thesis vs hnie-thesis-template（均为草稿）。
- **用户名拼写错误**：HUZA-Thesis-Proposal 很可能是 HZAU-Thesis-Proposal 的手误。
- **外部用户仓库**：如 mrxxx-creat/NJUT、mrxxx-creat/shanxi 来自非 iftaken 的外部账号，也需要纳入统计。

## 已知数据（截至 2025-06-14）

- 平台已发布：32 个（全部 sourceType=github）
- iftaken 已发布：26 个
- XinhePaper org 发布：4 个
- 外部用户 repo 发布：2 个
- 草稿（iftaken）：2 个
- iftaken 未上线模板：约 163 个（其中 74 个是高校学位论文模板）
