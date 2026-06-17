# USTB 本科毕业论文模板（bosswnx/ustb-thesis）

## 模板概况

| 项目 | 值 |
|------|-----|
| 名称 | 北京科技大学本科毕业论文 |
| 来源 | `bosswnx/ustb-thesis` (GitHub), 作者: 王诺贤 |
| TeXPage | https://www.texpage.com/template/20576956-6100-402f-b6c6-f55089c2dfb7 |
| 目标仓库 | `iftaken/ustb-bachelor-thesis` |
| 文档类 | `ustb-thesis.cls` (基于 `\LoadClass{ctexrep}`) |
| 参考文献 | biblatex + gb7714-2015 |
| 区别 | **本科**毕业论文，不同于 YiFraternity/USTBThesis（硕博） |

## 核心适配

原模板 **仅有 `\ifwindows` 字体分支**，无 macOS/Linux 路径。需完整添加非 Windows 分支。

### 适配步骤

1. **`\PassOptionsToClass{fontset=none}{ctexrep}`** 插入在 `\ProvidesClass` 之后、`\LoadClass` 之前，防止 ctex 自动检测 Fandol 字体并预定义 CJK 家族（会导致后续手动声明冲突）

2. **添加 `\else` 分支**：在 `\ifwindows` 块之后添加完整的非 Windows 字体设置

3. **手动定义 CJK 切换命令**：fontset=none 时 ctex 不定义 `\songti`/`\heiti`/`\kaishu`/`\fangsong`，需在 cls 中添加：
   ```latex
   \NewDocumentCommand\songti{}{\CJKfamily{zhsong}}
   \NewDocumentCommand\heiti{}{\CJKfamily{zhhei}}
   \NewDocumentCommand\kaishu{}{\CJKfamily{zhkai}}
   \NewDocumentCommand\fangsong{}{\CJKfamily{zhfs}}
   ```

4. **`\addbibresource{refs.bib}` → `\addbibresource{references.bib}`**

### 字体映射（Linux 分支）

| 字体 | 来源 | 声明方式 |
|------|------|---------|
| SimSun (宋体) | Docker 系统字体 | `\setCJKmainfont{SimSun}` |
| SimHei (黑体) | Docker 系统字体 | `\setCJKsansfont{SimHei}` |
| Times New Roman | Docker 系统字体 | `\setmainfont{Times New Roman}` |
| simkai.ttf (楷体) | COS 下载 | `\setCJKfamilyfont{zhkai}[Path=font/]{simkai.ttf}` |
| simfang.ttf (仿宋) | COS 下载 | `\setCJKfamilyfont{zhfs}[Path=font/]{simfang.ttf}` |

### 编译结果

- tectonic 成功编译，main.pdf ≈ 931KB
- 28 个文件进入 git 追踪（不含 font/）
