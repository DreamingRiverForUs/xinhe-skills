# GB 国家标准 LaTeX 模板

## 基本信息

| 字段 | 值 |
|------|-----|
| 模板名称 | 中华人民共和国国家标准 LaTeX 模板 |
| GitHub 源 | ybj2004/GB-Template |
| TeXPage ID | aaa47819-b851-422f-ae4c-2e801fd7491b |
| 目标仓库 | iftaken/gb-template |
| 文档类 | GB-template.cls（基于 ctexbook） |
| 编译引擎 | XeLaTeX (tectonic) |
| 编译结果 | 374 KB PDF，仅有 overfull/underfull hbox 警告 |

## 模板结构

```
GB-template.cls          # 文档类（ctexbook + 国标样式）
main.tex                 # 主入口（定义 ICS/分类号/标准号等参数）
body/
├── preamble.tex         # 前言
├── basic-use.tex        # 模板使用说明
├── test.tex             # 测试章节
└── appendix.tex         # 附录
figures/
└── GB-LOGO.jpg          # 国标 Logo
gbt7714-2005.bst         # 参考文献样式
gb-idxstyle.mst          # 索引样式
adjustind.py             # 索引调整脚本（Windows 专用）
```

## 适配要点

### 1. 字体：零额外下载

ctexbook 在 Docker 中自动检测到 **fandol** fontset（非 windows），FandolSong/Hei/Kai/Fang 全部在 tectonic bundle 中可用。cls 中 `\titlefont{\CJKfontspec{SimSun}}` 通过 Docker 系统字体 `/usr/local/share/fonts/custom/SIMSUN.TTC` 满足。**init.sh 只需创建空 font/ 目录，无需下载任何字体。**

### 2. imakeidx：移除 xindy 选项

原 cls 使用 `\RequirePackage[xindy]{imakeidx}`，Docker 中 xindy 不可用。改为 `\RequirePackage{imakeidx}`。

### 3. 参考文献引用更新

cls 中 `\bibliography{bibfile}` → `\bibliography{references}`，文件重命名 `bibfile.bib` → `references.bib`。

### 4. 索引工具链（可忽略）

模板设计用于 Windows 环境：zhmakeindex.exe + adjustind.py 处理后生成索引。Docker 中这些全部不可用（shell-escape disabled），`\printindex` 和 `\makeindex` 静默失败，不影响正文 PDF 输出。

### 5. main.tex 重命名

`GB-template.tex` → `main.tex`，内部 `\documentclass{GB-template}` 保持不变。

## 编译命令

```bash
docker run --rm --platform linux/amd64 \
  -v $(pwd):/app \
  -v ~/.cache/paper-tectonic:/root/.cache/Tectonic \
  crpi-b75iph3qtzyryyvz.cn-hangzhou.personal.cr.aliyuncs.com/paper-prod/paper-sandbox-cli:latest \
  tectonic -X compile main.tex
```

## 已知警告（安全）

- `accessing absolute path /usr/local/share/fonts/custom/SIMSUN.TTC` — SimSun 系统字体路径
- `runsystem(python adjustind.py main)...disabled` — shell-escape 禁用，索引功能跳过
- 多个 overfull/underfull hbox — 排版微调，不影响输出
- `Object @page.I already defined` — xdvipdfmx 罗马数字页码警告
