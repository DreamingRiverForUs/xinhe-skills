# 模板管理飞书多维表格

## 连接信息

| 属性 | 值 |
|------|-----|
| Base Token | `ErlObuSw9aTdOysjjkUce6j1nNh` |
| Table ID | `tbl0YkvmiUznuZ8O` |
| 认证 | `--as user`（需 `lark-cli auth login --domain base`） |

## 核心字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `模板编号` | text | 递增序号 |
| `模板名称` | text | 模板全称 |
| `状态` | select | 待收集 / 待适配 / 已上线 / 待浏览器提取 / ... |
| `来源平台` | select | Texpage / GitHub / ... |
| `来源方式` | select | 方式2:LaTeX平台整合 / ... |
| `模板分类` | select | 毕业论文 / 期刊投稿 / 数模竞赛 / ... |
| `原始来源链接` | url | TeXPage 或上游 GitHub URL |
| `GitHub仓库链接` | url | 心河Paper 目标仓库（iftaken/xxx） |
| `适配说明` | text | 适配状态、编译结果、阻塞原因等 |
| `优先级` | text | 优先级标记 |
| `负责人` | user | 负责人 open_id |
| `备注` | text | 其他备注 |

## 常用操作

### 读取记录

```bash
lark-cli base +record-get --as user \
  --base-token ErlObuSw9aTdOysjjkUce6j1nNh \
  --table-id tbl0YkvmiUznuZ8O \
  --record-id <record_id>
```

### 更新上线状态

```bash
lark-cli base +record-upsert --as user \
  --base-token ErlObuSw9aTdOysjjkUce6j1nNh \
  --table-id tbl0YkvmiUznuZ8O \
  --record-id <record_id> \
  --json '{"状态":"已上线","GitHub仓库链接":"https://github.com/iftaken/<repo>","适配说明":"<编译结果>"}'
```

### 标记待浏览器提取

```bash
lark-cli base +record-upsert --as user \
  --base-token ErlObuSw9aTdOysjjkUce6j1nNh \
  --table-id tbl0YkvmiUznuZ8O \
  --record-id <record_id> \
  --json '{"状态":"待浏览器提取","适配说明":"TeXPage-only，无GitHub源，占位结构已初始化"}'
```

## Pitfalls

- 字段名必须精确匹配（含大小写），不可凭猜测
- `+record-upsert` 的 JSON body 是原始字段映射，不包 `{"fields":{...}}` 外层
- `+record-batch-update` 对所有 `record_id_list` 应用相同 patch，不同状态需分组多轮
