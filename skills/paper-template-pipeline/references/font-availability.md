# Docker 镜像字体可用性与 fontspec 陷阱

## 镜像预装系统字体（fc-list / fontconfig 可查）

| 字体名 | 路径 | 用途 |
|--------|------|------|
| Times New Roman | `/usr/local/share/fonts/custom/TIMES*.TTF` | 衬线（serif） |
| SimSun (宋体) | `/usr/local/share/fonts/custom/SIMSUN.TTC` | CJK 主字体 |
| SimHei (黑体) | `/usr/local/share/fonts/custom/SIMHEI.TTF` | CJK 黑体 |
| Cambria | `/usr/local/share/fonts/custom/CAMBRIA.TTC` | 数学/衬线 |
| Liberation Sans | `/usr/share/fonts/truetype/liberation/LiberationSans-*.ttf` | 无衬线（Arial 替代） |
| Liberation Serif | `/usr/share/fonts/truetype/liberation/LiberationSerif-*.ttf` | 衬线 |
| Liberation Mono | `/usr/share/fonts/truetype/liberation/LiberationMono-*.ttf` | 等宽 |
| DejaVu Sans | `/usr/share/fonts/truetype/dejavu/DejaVuSans*.ttf` | 无衬线 |
| DejaVu Serif | `/usr/share/fonts/truetype/dejavu/DejaVuSerif*.ttf` | 衬线 |
| DejaVu Sans Mono | `/usr/share/fonts/truetype/dejavu/DejaVuSansMono*.ttf` | 等宽 |
| Noto Sans CJK | `/usr/share/fonts/opentype/noto/NotoSansCJK-*.ttc` | CJK 无衬线（含 Black 字重，可替代 Arial Black） |
| Noto Serif CJK | `/usr/share/fonts/opentype/noto/NotoSerifCJK-*.ttc` | CJK 衬线 |
| FandolSong | tectonic 缓存（仅编译时可用） | CJK 宋体 |

## 不在系统字体中的（需 init.sh 下载）

| 字体 | 原因 | COS URL |
|------|------|---------|
| simkai.ttf (楷体) | 不在 Docker 镜像系统字体 | font_url.txt |
| simfang.ttf (仿宋) | 同上 | font_url.txt |
| Arial | 不在镜像中 | 有，但建议用 Liberation Sans 替代 |
| Arial Black | 不在镜像中 | 无，用 Noto Sans CJK SC Black 替代 |
| TeX Gyre Termes | 不在系统字体（仅 tectonic 缓存） | 无，改用 Times New Roman |
| Fandol 全系列 | 不在系统字体（仅 tectonic 缓存） | 无，改用 SimSun/SimHei 或下载 |

## fontspec API 关键差异（高频陷阱）

```
\setmainfont / \setsansfont / \setmonofont:
  第一个参数 = 字体名称（不是文件名！）
  ❌ \setmainfont[Path=./font/]{times.ttf}  → 报错 "font cannot be found"
  ✅ \setmainfont{Times New Roman}
  fontspec 按名称在系统中搜索，Path= 只表示在哪个目录里找，不改变匹配方式

\setCJKmainfont / \setCJKfamilyfont（xeCJK 提供）:
  第一个参数 = 文件名（当指定 Path= 时）
  ✅ \setCJKfamilyfont{kai}[Path=./font/]{simkai.ttf}
  xeCJK 的 Path= 行为与 fontspec 不同——它确实按文件名查找
```

### 典型修复模式

原始模板代码：
```latex
\setmainfont[Path=fonts/,UprightFont=times.ttf,BoldFont=timesbd.ttf,...]{times.ttf}
\setsansfont[Path=fonts/,UprightFont=times.ttf,...]{times.ttf}
\setCJKfamilyfont{kai}[Path=fonts/,AutoFakeBold=2.5]{simkai.ttf}
```

修复后：
```latex
\setmainfont{Times New Roman}                    % 系统字体
\setsansfont{Liberation Sans}                     % 系统字体（替代 Arial）
\setCJKfamilyfont{kai}[Path=fonts/,AutoFakeBold=2.5]{simkai.ttf}  % 此写法正确，不变
```

## 字体策略决策树

```
模板字体声明 → 检查是否在 Docker 系统字体中？
  ├─ 是 → 直接用字体名（如 Times New Roman, Liberation Sans, SimSun）
  └─ 否 → 加入 init.sh 下载 + 检查声明方式
       ├─ \setCJKfamilyfont → 保持 Path=./font/ + 文件名 ✅
       └─ \setmainfont/\setsansfont → 改用系统字体替代
            ├─ Arial → Liberation Sans（metrically equivalent）
            ├─ Arial Black → Noto Sans CJK SC Black
            ├─ Courier New → Liberation Mono
            ├─ TeX Gyre Termes → Times New Roman
            └─ Fandol系列 → SimSun/SimHei
```

## `\fontspec_font_if_exist:nTF` 模式（移植友好）

部分模板（如 nkthesis）使用条件检测避免硬编码字体路径：

```latex
\fontspec_font_if_exist:nTF { SimSun }
    { \setCJKmainfont { SimSun } }
    { \setCJKmainfont { simsun.ttc } [ Path = fonts/ ] }
```

如果系统有 SimSun 就用系统字体，否则从 `fonts/` 目录加载文件。**此模式是心河Paper 的最佳实践**，因为 Docker 镜像已预装 SimSun/SimHei/Times New Roman，无需下载这些字体，只需处理镜像缺失的字体（如 simkai/simfang）。

遇到此类模板时：
- Docker 系统字体的声明 → 自动命中系统路径，**无需修改**
- Docker 非系统字体的声明 → 需确认 `fonts/` 目录有对应文件（由 init.sh 下载）
- 注意目录名：模板可能用 `fonts/`（有 s）而非 `font/`，init.sh 和 .gitignore 必须匹配
