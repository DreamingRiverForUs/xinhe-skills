# 湖南大学本科生毕业论文（设计）LaTeX 模板

## 来源

| 项目 | 值 |
|------|-----|
| 源仓库 | learnmorezhan/HNU-bachelor-thesis-latex-template-2026 |
| 文档类 | hnuthesis.cls（基于 ctexbook，fontset=none） |
| TeXPage | https://www.texpage.com/template/cdfc5453-7e25-4b62-a235-dcb334fba84f |

## 模板结构

```
main.tex          # 入口：\documentclass{hnuthesis}
metadata.tex      # 用户论文信息（标题/姓名/学号/学院/导师/关键词）
metadata.template.tex  # 用户信息模板
cls/hnuthesis.cls # 文档类（需复制到根目录供 tectonic 使用）
chapters/         # 章节（ch01-03，通过 \input 引入）
frontmatter/      # 前置内容（中英文摘要、致谢）
appendices/       # 附录（app-a/b/c）
assets/           # 校徽 png、水印 png
figures/          # 图片资源
references.bib    # 参考文献（gbt7714 国标格式）
```

## 适配要点

### 1. cls 子目录 → 根目录

tectonic 不识别 TEXINPUTS 环境变量，`\documentclass{hnuthesis}` 需要 `hnuthesis.cls` 在项目根目录（与 main.tex 同级）。

```bash
cp cls/hnuthesis.cls hnuthesis.cls
```

### 2. 移除 unicode-math + Cambria Math

原模板使用 `\RequirePackage{unicode-math}` + `\setmathfont{Cambria Math}`。Docker 无 Cambria Math 系统字体，且 `\IfFontExistsTF{Cambria Math}` 检查在 cls preamble 中会触发错误。对本科论文无实质影响，直接移除。

```latex
# 移除行
\RequirePackage{unicode-math}
```

### 3. 私有字体 → Docker 系统字体

原 cls 通过 `\HNU@privatepath`（指向 `fonts/private/`）加载 Times 和 SimSun/SimHei 字体文件，且包含硬错误检查（`\ClassError` 阻断编译）。

**替换方案**：
```latex
\setmainfont{Times New Roman}[
  BoldFont=Times New Roman Bold,
  ItalicFont=Times New Roman Italic,
  BoldItalicFont=Times New Roman Bold Italic
]
\setsansfont{Times New Roman}[BoldFont=Times New Roman Bold]
\setmonofont{Times New Roman}
\setCJKmainfont{SimSun}[AutoFakeBold=true,AutoFakeSlant=true]
\setCJKsansfont{SimHei}[AutoFakeBold=true]
\setCJKmonofont{SimSun}
\setCJKfamilyfont{hnu@zhsong}{SimSun}[AutoFakeBold=true,AutoFakeSlant=true]
\setCJKfamilyfont{hnu@zhhei}{SimHei}[AutoFakeBold=true]
\setCJKfamilyfont{hnu@zhfs}{SimSun}[AutoFakeSlant=true]
```

**注意**：Docker 无 FangSong，`hnu@zhfs`（仿宋家族）回退到 SimSun。模板通过 `\providecommand{\fangsong}{\CJKfamily{hnu@zhfs}}` 注册，实际显示为宋体。

### 4. 移除字体硬错误检查

原 cls 在加载阶段执行 `\HNU@ensurebundledtextfonts` 和 `\HNU@ensuremathfont`，缺失字体时抛出 `\ClassError` 阻断编译。全部移除。

### 5. 无外部字体依赖

Docker 镜像自带 Times New Roman 和 SimSun/SimHei 系统字体，init.sh 为空操作。

```bash
FONT_DIR="font"
FONT_FILES=()
```

## 编译验证

```bash
docker run --rm --platform linux/amd64 \
  -v $(pwd):/app \
  -v ~/.cache/paper-tectonic:/root/.cache/Tectonic \
  crpi-b75iph3qtzyryyvz.cn-hangzhou.personal.cr.aliyuncs.com/paper-prod/paper-sandbox-cli:latest \
  tectonic -X compile main.tex
```

结果：exit 0，main.pdf ~406KB。

## Pitfalls

- **`\IfFontExistsTF{Cambria Math}` 在 cls preamble 不可用**：此命令在 .cls 加载阶段触发 `Missing \begin{document}`，是额外移除 unicode-math 的理由之一。
- **Times New Roman Bold/Italic/BoldItalic**：Docker 中 TIMESBD.TTF、TIMESI.TTF、TIMESBI.TTF 分别注册为 "Times New Roman Bold"、"Times New Roman Italic"、"Times New Roman Bold Italic"，fontspec 可通过字体名找到。
- **SimSun ExtG / SimSunB 等额外字体**：原 `fonts/private/` 包含 `SimsunExtG.ttf`、`simsunb.ttf`，但 cls 未引用，无需处理。
