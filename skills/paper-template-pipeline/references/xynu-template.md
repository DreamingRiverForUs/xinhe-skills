# 信阳师范大学 (XYNU) 模板

## GitHub 作者

- **kelasike1216** — 信阳师范大学 LaTeX 模板维护者
  - `kelasike1216/xynuthesis-unofficial` — 硕士毕业论文模板（有 GitHub 源，ustcthesis 派生）
  - 本科学年论文模板 — **仅 TeXPage，无 GitHub 源**（同作者）
  - Beamer 答辩模板 — **仅 TeXPage，无 GitHub 源**

## 模板清单

| 模板 | 类型 | GitHub | TeXPage ID | 飞书记录 | 状态 |
|------|------|--------|------------|----------|------|
| xynuthesis-unofficial | 毕业论文 | kelasike1216/xynuthesis-unofficial | — | — | 已有 GitHub 源 |
| xynu-year-paper | 本科学年论文 | ❌ 无 | `9bbbf15e-7e8e-4543-b29c-69fdcaff14b9` | `recvlPjTMYhGuB` | 占位结构已初始化，待浏览器提取 |
| xynu-beamer | Beamer 答辩 | ❌ 无 | `1d2bcc7f-5253-4d5b-a890-ad8fc9730ea2` | `recvlPjTMXfoeW` | 占位结构已上线，源文件待提取 |

## xynu-year-paper 上线记录

- **仓库**：iftaken/xynu-year-paper (private)
- **TeXPage UUID**：`9bbbf15e-7e8e-4543-b29c-69fdcaff14b9`（注意：误传的 UUID `9bbbf15e-b6cc-4f32-9e20-bcfdb3f7e8e1` 会重定向到通用模板列表页）
- **发现过程**：任务传入错误 UUID → curl 返回通用列表页（title="LaTeX Templates - TeXPage"）→ 查飞书记录 `recvlPjTMYhGuB` 的 `原始来源链接` 字段得正确 UUID → 确认 TeXPage-only（无 GitHub 源）
- **策略**：占位先行，ctexart 最小文档，init.sh 空数组（字体依赖待确定）
- **编译**：tectonic 占位 main.tex 编译通过（exit 0，55KB PDF）
- **作者关联**：上游作者 kelasike1216，相关仓库 xynuthesis-unofficial（硕士论文，同作者，ustcthesis 派生）
- **待办**：浏览器环境下从 TeXPage "Open as Template" 提取完整源文件覆盖占位

### UUID 校验方法

当 TeXPage UUID 疑似错误时，用 curl 检查页面 title：

```bash
curl -sL 'https://www.texpage.com/template/<id>' | grep -oE 'title>[^<]+</title'
```

- title 为具体模板名（如 "信阳师范学院本科学年论文模板 - TeXPage"）→ 正确
- title 为 "LaTeX Templates - TeXPage" → UUID 无效或已失效，静默回退到列表页
- 修复：从飞书记录的 `原始来源链接` 字段取正确 UUID

## xynu-beamer 上线记录

- **仓库**：iftaken/xynu-beamer (private)
- **发现过程**：TeXPage curl grep → 无 GitHub 链接 → 搜索 kelasike1216 repos → 仅有 thesis 无 beamer → 确认为 TeXPage-only
- **策略**：占位先行（beamer 零 CJK 字体，init.sh 空数组）
- **编译**：tectonic 占位 main.tex 编译通过（exit 0，10.28 KiB），Chinese 字符 Missing 警告为预期（无 CJK 字体加载）
- **待办**：浏览器环境下从 TeXPage "Open as Template" 提取完整 .sty 主题文件 + 示例 .tex，覆盖占位后重新编译

## xynuthesis-unofficial（参考）

- GitHub: kelasike1216/xynuthesis-unofficial
- 结构：标准论文模板，含 chapters/、figures/、bib/、xynuthesis.cls
- 参考文献：xynuthesis-authoryear.bbx/cbx、xynuthesis-numeric.bbx/cbx、gbt7714 .bst
- 适配注意事项：与通用 ctexbook 论文模板相同（字体、tectonic 兼容性等）
