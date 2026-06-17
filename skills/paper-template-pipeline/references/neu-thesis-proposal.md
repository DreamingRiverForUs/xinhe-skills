# 东北大学本科毕业设计开题报告模板

## 基本信息

| 项目 | 值 |
|------|-----|
| TeXPage ID | `9b9b8732-d494-4980-b176-64895e2c745d` |
| 上游 GitHub | `SchrodingerBlume/NEUBachelorProposal-LaTeX` v1.0.3 |
| 目标仓库 | iftaken/neu-thesis-proposal |
| 作者 | 吴俊豪 (SchrodingerBlume) |
| 许可 | LPPL 1.3c |
| 模板类型 | 本科毕业设计开题报告 |
| 文档类 | `NEUBachelorProposal.cls`（基于 ctexart, fontset=none） |

## 文件结构

```
main.tex                    # 主文档入口
NEUBachelorProposal.cls     # 文档类（自适应字体检测）
references.bib              # 参考文献
gb7714-2025.bbx / .cbx      # 国标参考文献样式（biblatex）
huiyijiyao.doc / .pdf       # 会议纪要
figures/flower.png          # 示例图片
```

## 字体策略

模板使用三级优先字体检测：

1. **Windows 系统字体**：SimSun, SimHei, KaiTi, FangSong
2. **macOS 系统字体**：Songti SC, Heiti SC, Kaiti SC, STFangsong
3. **Noto CJK / 思源 / Fandol 回退**

封面标题使用 FZDBSJW.TTF（方正大标宋简体），缺失时自动回退到 FandolSong-Bold。

## Docker 适配要点

### 1. unicode-math 移除（必须）

模板使用 `\setmathfont` 链（XITS Math → STIX Two Math → Latin Modern Math），Docker tectonic TL2023 均无这些 OpenType 数学字体。

**修复**：移除 `\RequirePackage{unicode-math}` 及所有相关命令：
- `\setmathfont{...}` → 删除（所有 math font 声明）
- `\unimathsetup{...}` → 删除
- `\removenolimits{...}` → 删除
- `\DeclareRobustCommand\bm[1]{{\symbfit{#1}}}` → `\DeclareRobustCommand\bm[1]{{\boldsymbol{#1}}}`
- `\DeclareRobustCommand\boldsymbol[1]{{\symbfit{#1}}}` → 删除（amsmath 已有定义）

保留：`\DeclareMathAlphabet{\mathcal}` 和 `\DeclareMathAlphabet{\mathbb}`（标准 LaTeX 命令，无依赖）。

### 2. KaiTi/FangSong 独立回退（必须）

Docker 镜像有 SimSun/SimHei 但**无** KaiTi/FangSong。模板原逻辑是 IfFontExistsTF{SimSun} → 进入 Windows 分支 → 设置全部四种字体。但 KaiTi/FangSong 不存在会报错。

**修复**：在 Windows 分支内为 zhkai 和 zhfs 添加独立检测：

```latex
% KaiTi — Docker 可能无此字体，回退到 FandolKai
\IfFontExistsTF{KaiTi}{
  \setCJKfamilyfont{zhkai}{KaiTi}[AutoFakeBold=..., AutoFakeSlant=...]
}{
  \setCJKfamilyfont{zhkai}{FandolKai}[Extension=.otf, UprightFont=*-Regular, ...]
}
% FangSong — 同理
\IfFontExistsTF{FangSong}{
  \setCJKfamilyfont{zhfs}{FangSong}[...]
  \setCJKmonofont{FangSong}[...]
}{
  \setCJKfamilyfont{zhfs}{FandolFang}[Extension=.otf, UprightFont=*-Regular, ...]
  \setCJKmonofont{FandolFang}[Extension=.otf, UprightFont=*-Regular, ...]
}
```

### 3. Times New Roman 可用

Docker 镜像 `/usr/local/share/fonts/custom/` 下有 TIMES.TTF / TIMESBD.TTF / TIMESI.TTF / TIMESBI.TTF。`\setmainfont{Times New Roman}` 通过 fontconfig 正常工作。

### 4. 参考文献

模板使用 `biblatex` + `biber`（gb7714-2025 样式），tectonic 的 `-X` 参数自动调用 biber。编译顺序自动处理。

## 编译验证

```bash
docker run --rm --platform linux/amd64 \
  -v $(pwd):/app \
  -v ~/.cache/paper-tectonic:/root/.cache/Tectonic \
  crpi-b75iph3qtzyryyvz.cn-hangzhou.personal.cr.aliyuncs.com/paper-prod/paper-sandbox-cli:latest \
  tectonic -X compile main.tex
```

结果：0 errors，420KB PDF，3 次 biber re-run 正常。
