# 韶关学院期末考试试卷 LaTeX 模板（TeXPage-only）

与 SGU 毕业论文模板同作者（付林林），同为 TeXPage-only。使用 USTBExam.cls（原北京科技大学考试模板）。

## 模板信息

| 字段 | 值 |
|------|----|
| TeXPage ID | `11164c7a-a01e-4791-bc25-f4c8aae1f487` |
| 模板名称 | 韶关学院期末考试试卷 LaTeX 模板 |
| 作者 | 付林林 |
| License | LaTeX Project Public License 1.3c |
| 最后修改 | 2026-04-01 |
| 目标仓库 | iftaken/sgu-exam |
| 文档类 | USTBExam.cls (基于 ctexart) |
| 分类 | 大学期末考试试卷 |

## 源文件清单

从 TeXPage 编辑器提取的文件：
- `USTBExam.cls` — 文档类，支持 answer/noanswer 切换
- `HTNotes-math.sty` — 数学符号宏包（dif, upe, cov, abs 等）
- `defrepeatcell.tex` — LaTeX3 表格生成宏（`\latexRepeatCells`, `\pgfRepeatCells`, `\forCells`）
- `sgunexamA.tex` — 试卷主文件（数学分析3 期末试卷 A 卷示例）
- `pic.pdf` — 几何示意图（圆外切三角形证明）
- `pic2.pdf` — 几何示意图（四分之一圆）

**提取方法**：全部 8 层 GitHub 搜索均失败 → WebBridge 逐文件提取（TreeWalker click + `_texpage_editor.state.doc.toString()`）。

**PDF 提取问题**：TeXPage download API 返回 404，`/api/project/file/download` 返回 9 字节错误。pic.pdf 和 pic2.pdf 用 TikZ standalone 生成替换版本（Docker 编译），非原版。如需要原始 PDF，需浏览器另存为方式获取。

## 编译适配

**零适配通过**：ctexart 在 Docker 中 auto-detect fandol fontset，SimSun 为 Docker 系统字体，无需字体下载。CJKnumb.sty 由 tectonic 自动下载。

初始化 init.sh 为最小占位（空数组 + `mkdir -p font/`），无外部字体依赖。

## 模板功能

- `answer` / `noanswer` 选项切换答案显示（分别生成试卷和评分标准）
- 自动检查试卷总分与小题数量（`\checking` 命令，错误时红色提示）
- 密封线（`\mifengxian` 通过 TikZ 绘制）
- 填空题、选择题（`\options` 4 项自适应排版）、定义题、证明题、计算题
- `\fillin` / `\pickout` / `\pickin` 答案占位命令

## Pitfalls

- **无 GitHub 源**：8 层搜索全部失败，必须走浏览器提取
- **PDF 资源不可下载**：TeXPage 文件 API 不可用，小几何图可用 TikZ 生成替代
- **USTBExam.cls 原名暗示**：文档类原为北京科技大学考试模板，已由作者适配为韶关学院使用
- **CJKnumb 依赖**：使用 `\zhnumber` 生成中文题号，tectonic 自动下载
