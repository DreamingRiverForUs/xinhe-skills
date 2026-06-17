# GitHub Fork 不完整 + 上游已删除：诊断与补救

## 场景特征

GitHub 上找到一个 fork（如 `zhout26/stuthesis`），仓库看起来是模板但**缺少核心 `.cls` 文件**。
原始上游 repo 已被删除或私有化。

## 实例：汕头大学学位论文模板 (stuthesis)

### 链条

```
TeXPage 模板 c0ed1f97-112e-42cc-9d73-cca941efb8fc
  → GitHub fork: zhout26/stuthesis（仅 1 个 commit，2021-10-07）
  → 原始上游: stutug/stuthesis（已删除，org stutug 也已 404 不存在）
```

### 缺失的文件

`zhout26/stuthesis` 有但**缺 `stuthesis.cls`**：

```
有: main.tex, stusetup.tex, stuthesis-doc.tex
    stuthesis-*.bst, stuthesis-*.bbx, stuthesis-*.cbx
    chapters/*.tex, figures/stu-badge.pdf, figures/stu-name.pdf
    bib/references.bib, README.md, CHANGELOG.md, LICENSE
缺: stuthesis.cls  ← 文档类核心
```

### 诊断确认

```bash
# 确认 .cls 缺失
find . -name '*.cls'          # 返回空

# 确认上游已死
gh repo view stutug/stuthesis # 404 Not Found
gh api orgs/stutug          # 404 Not Found（org 本身也已不存在）
```

### 尝试过的无效路径（全部失败）

| 路径 | 命令 | 结果 |
|------|------|------|
| GitHub code search | `gh search code 'stuthesis.cls'` | 全网 0 结果 |
| CTAN | `curl ctan.org/pkg/stuthesis` | 404，包不存在 |
| Overleaf zip 下载 | `curl overleaf.com/.../download/zip` | 返回 HTML（需认证） |
| Wayback Machine | `web.archive.org/.../stutug/stuthesis/.../stuthesis.cls` | 无存档 |
| 校内镜像 | `git.lug.stu.edu.cn/stutug/stuthesis` | 外网不可达 |
| TeXPage OSS URL | `latex-static.texpage.com/template/<uuid>/...` | NoSuchKey |
| TeXPage OSS file | `latex-file.texpageusercontent.com/...` | AccessDenied |
| TeXPage curl 页面 | `curl texpage.com/template/<uuid>` | 403 (ESA 拦截) |
| TeXPage API | `api.texpage.com/v1/templates/<uuid>` | Not logged in |

### 唯一有效路径

**回到 TeXPage 浏览器端手动提取**：

1. 浏览器打开 `https://www.texpage.com/template/<uuid>`
2. 点击 "Open as Template" 创建项目
3. 在项目编辑器中，点击左侧文件树找到 `stuthesis.cls`
4. 用 DevTools `document.querySelector('.cm-content').textContent` 或 Monaco API 读取内容
5. 保存到本地，走正常流水线

此场景的本质是：TeXPage 模板 → GitHub 源仓库 → fork 不完整。TeXPage 服务器上**有**完整文件，但非登录 curl 被拦截。

### 模板关键信息（即使未完成上线也要记录）

| 属性 | 值 |
|------|----|
| 模板名 | 汕头大学学位论文 LaTeX 模板 |
| 文档类 | `stuthesis` |
| 编译引擎 | XeLaTeX |
| 读者选项 | `degree=bachelor|master|doctor`, `fontset=windows|mac|ubuntu|fandol` |
| 参考文献 | natbib (stuthesis-numerical.bst / stuthesis-authoryear.bst / stuthesis-bachelor.bst) + biblatex 备选 |
| 基础模板 | 基于中国科学技术大学 ustctug/ustcthesis |
| 上游 | stutug/stuthesis（已删除）|
| 可用 fork | zhout26/stuthesis（不完整，缺 .cls）|
| TeXPage | c0ed1f97-112e-42cc-9d73-cca941efb8fc |
| 心河Paper 仓库 | iftaken/stu-thesis（占位结构已初始化，含所有用户文件 + 占位 main.tex，待浏览器提取 .cls）|
| Overleaf | latex-template-for-stu-thesis/jvtdfkqsrycm |
