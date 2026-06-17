# 心河Paper 模板批量导入 (WebBridge)

通过 Kimi WebBridge 自动化导入 GitHub 模板到心河Paper。

## 流程

1. 导航到 `https://paper.huimengxinhe.com/writing/new`
2. 点击「我的模板」tab
3. 点击「新增模板」→「GitHub/Gitee 导入」
4. 填写表单：URL、分支、子目录、模板名、描述、标签
5. 点击「添加」确认标签
6. 点击「确认导入」

## 关键坑点

### React 受控组件

心河Paper 使用 React + shadcn/ui，表单输入是受控组件。必须用原生 value setter：

```js
var ns = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
var nts = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
// ns.call(inputElement, value)  // 触发 React state 更新
// nts.call(textareaElement, value)
```

直接 `element.value = x` + 事件派发不够——表单验证会报「请完善以下必填项」。

### 导入后状态

新导入的模板状态为 `draft`，需要手动「分享到市场」+ 管理员审核后才能变为 `published`。

## 自动化脚本

位置: `/Users/ming/project/cli_xinhe_status/scripts/bulk_import_templates.py`

```bash
# 单模板
python3 scripts/bulk_import_templates.py --single \
  --repo "repo-name" --name "显示名称" --desc "描述" --tags "标签" --category "分类"

# 批量
python3 scripts/bulk_import_templates.py /tmp/templates_import.csv
```

CSV 格式: `repo_name,display_name,description,tags,category,branch,subdir`

## 验证

```bash
cd /Users/ming/project/cli_xinhe_status
.venv/bin/python -c "
import asyncio
from xinhe_paper.db import db_session, safe_query
async def main():
    async with db_session():
        r = await safe_query(
            \"SELECT name, status FROM \\\"PaperTemplate\\\" ORDER BY \\\"createdAt\\\" DESC LIMIT 20\",
            limit=20
        )
        for t in r: print(t['status'], t['name'])
asyncio.run(main())
"
```
