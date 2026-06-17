# 南京信息工程大学本科毕业论文模板

## 来源信息

| 字段 | 值 |
|------|-----|
| TeXPage ID | `5f752d9b-c4a4-498d-8b6d-03b998851918` |
| TeXPage 作者 | 钨丝心脏 |
| GitHub 源仓库 | `sakronos/NUIST_Bachelor_Thesis_LaTeX_Template` |
| License | GPL-3.0 |
| 目标仓库 | `iftaken/nuist-thesis` |
| 分类 | 本科毕业论文 |
| 来源方式 | 方式 A（GitHub 源仓库） |

## 模板技术特征

- **文档类**: `nuist.cls`，通过 `\LoadClass[a4paper,zihao=5,UTF8]{ctexart}` 加载 ctexart（非 ctexbook）
- **CJK 字体**: 不使用 ctex fontset，在 cls 中手动声明所有 CJK 字体
- **\kaishu 声明**: 使用旧式 `[simkai.ttf]` 方括号文件名语法 → 需改为 `[Path=./font/simkai.ttf]`
- **参考文献**: `gbt7714` 宏包 + 自定义 `gbt7714-2005-numerical.bst`
- **封面**: `\cover{标题}{姓名}{学号}{学院}{专业}{导师}{日期}` 7 参数命令，内嵌校徽 `nuist_logo/nuist.pdf` 和校徽图片 `nuist_logo/xiaohui.jpg`
- **摘要**: `\abstractofchinese` / `\abstractofenglish` 两对命令（标题+摘要内容）
- **致谢**: `\thanking{内容}` 命令

## 字体依赖

| 字体 | 来源 | Docker 可用性 | 处理 |
|------|------|--------------|------|
| SimSun（宋体） | 系统字体 | ✅ `/usr/local/share/fonts/custom/SIMSUN.TTC` | 无需处理 |
| SimHei（黑体） | 系统字体 | ✅ `/usr/local/share/fonts/custom/SIMHEI.TTF` | 无需处理 |
| simkai.ttf（楷体） | COS 下载 | ❌ 需 init.sh | `Path=./font/simkai.ttf` |
| Times New Roman | 系统字体 | ✅ `/usr/local/share/fonts/custom/TIMES.TTF` | 无需处理 |

## 适配修改清单

### 1. simkai.ttf 字体路径（nuist.cls L23）

旧: `\setCJKfamilyfont{localkaishu}[AutoFakeBold,AutoFakeSlant]{[simkai.ttf]}`
新: `\setCJKfamilyfont{localkaishu}[AutoFakeBold,AutoFakeSlant,Path=./font/]{simkai.ttf}`

### 2. 参考文献引用（body/bib.tex L1）

旧: `\bibliography{bibliography}`
新: `\bibliography{references}`

文件 `bibliography.bib` 重命名为 `references.bib`。

## 编译特征

- tectonic 初次编译需下载 `tcolorbox`、`subfigure`、`xltxtra`、`shapepar` 等宏包
- `algorithm.sty` 和 `algorithmic.sty` 的 UTF-8 警告为已知 harmless
- `nuist_logo/nuist.pdf` 的 PDF 版本(1.7) > 输出版本(1.5) 警告非致命
- 参考文献处理触发一次 BibTeX re-run
- 编译需 3 轮（BibTeX + toc 变化 + aux 变化）

## .gitignore 特殊规则

校徽 PDF 需保留在仓库中 → 添加例外:
```
!nuist_logo/nuist.pdf
```

## 模板依赖宏包（非 ctex 默认）

| 宏包 | 用途 | 注意事项 |
|------|------|---------|
| `xltxtra` | `\LaTeX` logo 输出 | tectonic 自动下载 |
| `shapepar` | `\heartpar` 致谢装饰 | 非必需，tectonic 自动下载 |
| `gbt7714` | 参考文献格式 | 配合自定义 .bst |
| `subfigure` | 子图（已弃用但有效） | tectonic 自动下载 |
| `tcolorbox` | 代码块样式 | tectonic 自动下载 |
| `algorithm` / `algorithmic` | 算法伪代码 | UTF-8 警告 harmless |
