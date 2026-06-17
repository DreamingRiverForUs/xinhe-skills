# 广西大学硕博学位论文模板 (GXU Thesis Template)

源仓库：SchrodingerBlume/gxuthesis（基于 KingwithQueen/GXU-Masters-and-PhD-Thesis-Templates 重构）
TeXPage 入口：https://www.texpage.com/template/6148c7dc-7325-4c07-aa31-bda5d0b8e783
目标仓库：iftaken/gxu-thesis-template

## 模板结构特点

- 使用自定义文档类 `\documentclass{gxuthesis}`，核心文件 `gxuthesis.cls` + `gxufrontmatter.tex`
- **目录名使用中文**：`字体/`、`论文内容/`、`参考文献/`、`签名/`、`图/`、`预览/`
- 参考文献：默认 GB/T 7714-2015，可选 gb7714-2025（通过 class option）
- 自带 gb7714-2025.bbx/.cbx 本地文件
- 编译需要 Biber（`backend=biber`）

## 字体清单与处理

| 字体 | 模板声明 | Docker 可用？ | 处理 |
|------|---------|-------------|------|
| Times New Roman | `\setmainfont{Times New Roman}` | ✅ 系统字体 | 无修改 |
| SimSun (宋体) | `\setCJKmainfont{SimSun}` + 文件回退 | ✅ 系统字体 | 命中系统路径，无修改 |
| SimHei (黑体) | `\setCJKfamilyfont{heiti}{SimHei}` + 文件回退 | ✅ 系统字体 | 命中系统路径，无修改 |
| FangSong (仿宋) | `\setCJKfamilyfont{zhfs}{FangSong}` | ❌ 不在系统中 | **添加文件优先回退** → `字体/simfang.ttf` |
| SimLi (隶书) | 文件优先 `字体/simli.ttf`，系统回退 | ❌ 不在系统中 | 下载到 `字体/` |
| XITS Math | `\setmathfont{XITS Math}` | ❌ 不在 tectonic | **注释掉**，使用 unicode-math 默认字体 |

### FangSong 回退代码（已添加到 gxuthesis.cls）

```latex
% FangSong fallback (Docker 系统无 FangSong，需从 字体/ 加载)
\newif\ifgxufangsongfound
\gxufangsongfoundfalse
\IfFileExists{字体/simfang.ttf}{%
    \setCJKfamilyfont{zhfs}{simfang.ttf}[AutoFakeBold=3, AutoFakeSlant=0.25, Path=字体/]%
    \gxufangsongfoundtrue
}{%
    \gxutrysysfont{FangSong}{%
        \setCJKfamilyfont{zhfs}{FangSong}[AutoFakeBold=3, AutoFakeSlant=0.25]%
        \gxufangsongfoundtrue
    }{%
        \PackageWarning{gxuthesis}{FangSong not found, falling back to songti}%
    }%
}
```

### init.sh 字体下载

```
FONT_FILES=("simfang.ttf" "SIMLI.TTF")
```

注意：COS 存储 `SIMLI.TTF`（大写），模板内引用 `simli.ttf`（小写）。macOS 大小写不敏感自动兼容，Linux 需 init.sh 内 `cp SIMLI.TTF simli.ttf`。

### XITS Math 处理

注释掉 `\setmathfont{XITS Math}[...]`，保留 `\usepackage{unicode-math}`。默认使用 Latin Modern Math，功能无损。

## 适配修改记录

1. **参考文献路径**：`\addbibresource{参考文献/ref1.bib}` + `\addbibresource{参考文献/ref2.bib}` → `\addbibresource{references.bib}`
2. **references.bib**：合并 ref1.bib + ref2.bib 到根目录
3. **FangSong 回退**：添加文件优先检查逻辑（见上）
4. **XITS Math**：注释掉 setmathfont 行
5. **.gitignore**：排除 `字体/`（非 `font/`，匹配模板实际目录名）
6. **init.sh**：下载 simfang.ttf + SIMLI.TTF

## 编译结果

Docker tectonic 编译：exit code 0，main.pdf 1.6 MiB。仅有 overfull hbox / JPEG resolution / PDF version 警告，无 Error。
