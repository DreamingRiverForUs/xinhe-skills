# 模板批量导入到心河Paper平台

## 前置条件

- Kimi WebBridge 运行中（localhost:10086）
- 浏览器已登录 paper.huimengxinhe.com
- 模板仓库已在 iftaken 组织下完成代码审查和 PII 清洗

## 流程

1. 生成 CSV 文件（repo_name, display_name, description, tags, category, branch, subdir）
2. 运行 `scripts/bulk_import_templates.py`

```bash
# 单模板测试
python3 scripts/bulk_import_templates.py --single --repo "acl-template" \
  --name "ACL 期刊模板" --desc "ACL LaTeX 模板" --tags "ACL,期刊" --category "期刊论文"

# 批量导入
python3 scripts/bulk_import_templates.py /tmp/templates.csv

# 断点续传
python3 scripts/bulk_import_templates.py /tmp/templates.csv --start-from 50
```

## 验证导入结果

通过 xinhe-paper CLI 查询草稿数量：

```python
cd /path/to/cli_xinhe_status && .venv/bin/python -c "
from xinhe_paper.db import db_session, safe_query
import asyncio
async def main():
    async with db_session():
        r = await safe_query(
            'SELECT status, COUNT(*) as cnt FROM \"PaperTemplate\" WHERE \"sourceType\"=''github'' GROUP BY status',
            limit=10
        )
        for t in r: print(t['status'], t['cnt'])
asyncio.run(main())
"
```

## 关键坑点

- **React 表单**：必须用 `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set` 设置值，直接 `.value =` 无效。详见 kimi-webbridge → `references/react-controlled-inputs.md`
- **WebBridge fill 不可用**：Next.js 表单上 fill 命令返回 false
- **网络监控不捕获**：该站的 API 调用不走 fetch/XHR（可能是 Next.js server actions），network 命令返回空
- **网页验证不可靠**：「我的模板」页面有分页限制，数据库查询是权威源
