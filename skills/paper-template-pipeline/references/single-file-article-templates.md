# 单文件期刊文章模板适配指南

部分 TeXPage 模板是**单文件期刊文章**（如 IEEEtran），与大学论文模板有本质区别。

## 特征识别

| 特征 | 论文模板 | 单文件文章模板 |
|------|----------|--------------|
| 文档类 | 自定义 `.cls`（如 `shtthesis.cls`） | TeX Live 标准类（如 `IEEEtran`） |
| 文件数 | 多文件（`main.tex` + `chapters/`） | 单文件（一个 `.tex` 即全部） |
| CJK 方式 | ctex/ctexbook（自动管理字体） | xeCJK 直接声明（需手动适配） |
| 参考文献 | BibTeX/biblatex + `.bib` | `thebibliography` 环境（手动） |
| .cls 缺失 | 错误——需修复 | 正常——tectonic bundle 自动下载 |
| 图片 | 校徽/logo（需从上游补） | 示例图片（可占位替代） |

## 阶段① 特殊处理

单文件模板通常**无 .cls**，`find . -name '*.cls'` 返回空是正常的**。不要将此判定为「源文件不完整」——检查 `main.tex` 中的 `\documentclass` 是否是标准 TeX Live 类（IEEEtran、article、report 等），若是则无需搜索上游 cls。

## 阶段④ 适配关键差异

### 字体适配：xeCJK 直接声明（非 ctex）

单文件文章模板通常用 `\usepackage{xeCJK}` 直接声明字体，而非 ctex 的 fontset 体系。字体适配直接替换 `\setCJKmainfont`/`\setCJKsansfont`/`\setCJKmonofont` 中的字体名为 Docker 可用字体：

```
Noto Serif CJK SC  → SimSun
Noto Sans CJK SC   → SimHei
Noto Sans Mono CJK SC → SimSun
```

**不要引入 ctex**——IEEEtran + ctex 可能有兼容性问题。保持 xeCJK 路线。

### 包去重清理（高频）

单文件模板常由非 LaTeX 专家编写，容易出现重复/废弃宏包：
- `\usepackage{graphics}` + `\usepackage{graphicx}` → 只保留 `graphicx`（后者是前者的扩展版）
- `\usepackage[usenames]{color}` + `\usepackage{xcolor}` → 只保留 `xcolor`（加 `usenames` 选项）
- `\usepackage{caption}` 出现两次 → 去重
- `\usepackage{epsfig}` → 保留（IEEE 模板常用），但不用它（用 graphicx 替代）

### thebibliography + references.bib 双轨

单文件文章模板常用 `\begin{thebibliography}` 手动管理参考文献（非 BibTeX）。**心河Paper 系统仍要求 `references.bib` 文件存在**——创建占位 `references.bib` 即可（包含与 thebibliography 条目对应的占位 BibTeX 条目），不需要将正文的 thebibliography 转换为 BibTeX。

### 图片资源：占位替代策略

当 TeXPage 模板的图片文件无法从浏览器下载（TeXPage download API 返回 1003），且无 GitHub 上游可补时：
- **Logo 类图片**（LOGO1.png、LOGO2.png）：用 Python 生成最小占位 PNG（有效但内容为纯色块）。后续从学校官网或同校模板补真实 logo。
- **示例图片**（fig1.png）：占位即可，不影响编译验证。

占位 PNG 生成（Python 一行流，无外部依赖）：
```python
import struct, zlib
def png(w,h,color,fn):
    c=lambda t,d:(struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff))
    r=b'\x00'+bytes(color)*w
    open(fn,'wb').write(b'\x89PNG\r\n\x1a\n'+c(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+c(b'IDAT',zlib.compress(r*h))+c(b'IEND',b''))
```

### Docker 编译预期

单文件 IEEEtran 文章模板的 Docker 编译通常**零错误一次过**：
- IEEEtran.cls 由 tectonic bundle 自动下载
- SimSun/SimHei 在 Docker 系统字体中直接可用
- `thebibliography` 不涉及 BibTeX/biber 运行
- 常见警告：Underfull hbox（模板占位文本的正常现象）、lineno.sty UTF-8 警告（宏包内部遗留编码，安全）

## 已处理案例

| 模板 | TeXPage ID | 仓库 | 类型 |
|------|-----------|------|------|
| SH_T-template-latex | 428ffcd2-fc17-409f-a652-d3b7c12e12c3 | iftaken/sht-template | IEEEtran 期刊 + 中文 |
