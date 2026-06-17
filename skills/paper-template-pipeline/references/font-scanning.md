# 字体依赖扫描方法

编译前必须在 `.cls` / `.sty` / `.tex` 中扫描所有字体声明。

## 扫描命令

```bash
# 1. 提取所有 fontspec/xeCJK 字体声明
grep -nE '\\(setmainfont|setsansfont|setmonofont|setCJKmainfont|setCJKfamilyfont|setCJKsansfont|setCJKmonofont|newfontfamily|newCJKfontfamily)\{' *.cls *.sty *.tex 2>/dev/null

# 2. 提取 fontset 声明（ctex 文档类选项）
grep -n 'fontset' *.cls *.tex 2>/dev/null

# 3. 提取 font-path 声明
grep -n 'font.path\|font-path\|Path=.*font' *.cls *.tex 2>/dev/null
```

## 扫描结果分类

将扫描到的字体按来源分类：

1. **系统字体名**（如 `Times New Roman`、`Arial`）→ 查 font-availability.md 确认是否存在
2. **文件名 + Path=**（如 `Path=./font/, simkai.ttf`）→ 确认文件在 font_url.txt 中
3. **Fandol 系列** → ❌ 不可用（仅 tectonic 缓存中，fontspec 找不到）
4. **TeX Gyre 系列** → ❌ 不可用（同上）

## 常见字体声明模式

| 模式 | 示例 | 是否在 Docker 可用 | 处理 |
|------|------|-------------------|------|
| 系统字体名 | `\setmainfont{Times New Roman}` | ✅ | 无需处理 |
| 系统字体名 | `\setsansfont{Arial}` | ❌ | 改为 Liberation Sans |
| fontset=windows | `\documentclass[fontset=windows]{ctexbook}` | 部分 | 中文字体通过 ctex 映射，需确认 simsun/simhei 存在 |
| CJK + Path + 文件名 | `\setCJKfamilyfont{kai}[Path=./font/]{simkai.ttf}` | N/A（需下载） | 加入 init.sh |
| fontset=none + 手动声明 | 手动 `\setCJKmainfont` | 视声明而定 | 逐个检查 |

## 扫描后输出格式

```
字体扫描结果：
  Times New Roman → 系统字体 ✅
  Arial → ❌ 需替换为 Liberation Sans
  simkai.ttf → 加入 init.sh（COS 可用 ✅）
  simfang.ttf → 加入 init.sh（COS 可用 ✅）
  FandolSong-Regular → ❌ 不可用，改用 SimSun
  TeX Gyre Termes → ❌ 不可用，改用 Times New Roman
```
