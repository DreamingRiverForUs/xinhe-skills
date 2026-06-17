# Tectonic / expl3 兼容性修复手册

Tectonic 使用的 TeX Live bundle ≈2023，expl3 版本较早。模板若使用了 2022 年之后新增的 expl3 特性，会在 Docker 编译时报 `Undefined control sequence`。

## 快速诊断

```bash
# 找出所有 :e 扩展变体（旧版 expl3 不支持，包括 :en/:eN/:eT/:eF/:eV/:eo 等）
grep -n ':e[nNTVFvopwf]' *.cls *.tex

# 找出 \ProcessKeyOptions / \DeclareKeys / \SetKeys（需要新版 l3keys2e）
grep -n 'ProcessKeyOptions\|DeclareKeys\|SetKeys' *.cls *.def 2>/dev/null

# 找出新版 subcaption 命令
grep -n 'subcaptionsetup' *.cls

# 找出 :e 变体生成
grep -n 'cs_generate_variant.*{ e }' *.cls
```

## 修复映射表

### `\ProcessKeyOptions` → `\ProcessKeysOptions`

**症状**：`Undefined control sequence` at `\ProcessKeyOptions`

**原因**：`\ProcessKeyOptions` 是 LaTeX kernel 2022-06-01 新增的命令。旧版使用 `l3keys2e` 包提供的 `\ProcessKeysOptions`（注意多了字母 's'，参数用花括号 `{}` 而非方括号 `[]`）。

**修复三步走**：

1. 降低 `\NeedsTeXFormat` 日期：
   ```latex
   \NeedsTeXFormat{LaTeX2e}[2022/06/01]   % 原值可能是 2024/11/01
   ```

2. 添加 `l3keys2e`：
   ```latex
   \RequirePackage{expl3}
   \RequirePackage{l3keys2e}   % ← 新增此行
   ```

3. 修改语法：
   ```latex
   % 旧：\ProcessKeyOptions [ __module / options ]
   % 新：
   \ProcessKeysOptions { __module / options }
   ```

### `\subcaptionsetup` → `\captionsetup[subfigure]`

**症状**：`Undefined control sequence` at `\subcaptionsetup`

**原因**：`\subcaptionsetup` 在较新的 subcaption 包中引入。旧版使用 `\captionsetup[subfigure]`。

**修复**：
```latex
% 旧：\subcaptionsetup { labelsep = none, ... }
% 新：
\captionsetup[subfigure] { labelsep = none, ... }
```

### `:e`-expansion 变体 → `\exp_args:Ne` 前缀

**症状**：`Undefined control sequence` 包含 `:eTF` / `:enF` / `:eV` 等模式

**原因**：`e`-expansion 于 2022 年加入 expl3。旧版 expl3 只有 `n`（不展开）、`V`（变量值）、`o`（展开一次）等变体。

**受影响命令**：
| 旧写法 | 新写法 |
|--------|--------|
| `\tl_if_empty:eTF { ARG } { T } { F }` | `\exp_args:Ne \tl_if_empty:nTF { ARG } { T } { F }` |
| `\str_case:enF { ARG } { CASES } { F }` | `\exp_args:Ne \str_case:nnF { ARG } { CASES } { F }` |
| `\__helper:en { ARG }` | `\exp_args:Ne \__helper:nn { ARG }` |

**技巧**：用 `replace_all` 一次性替换：
```
old: \tl_if_empty:eTF
new: \exp_args:Ne \tl_if_empty:nTF
```

然后对 `\str_case:enF` 等单个命令单独替换。

### `\cs_generate_variant:Nn ... { e }` 移除

**症状**：`Undefined control sequence` 于 `\cs_generate_variant:Nn` 行（该行本身不报错，但在使用 `:e` 变体的地方报错）

**原因**：`\cs_generate_variant:Nn` 确实存在，但不支持 `e` 类型参数。

**修复**：删除 `\cs_generate_variant:Nn \xxx:nn { e }` 行，并将所有 `\xxx:en` 调用改为 `\exp_args:Ne \xxx:nn`。

### LaTeX 2024-06-01 内核模板系统 → 硬件阻断（不可修）

**症状**：`Undefined control sequence` at `\NewTemplateType`、`\DeclareTemplateInterface`、`\DeclareTemplateCode`、`\DeclareInstance`、`\UseInstance`、`\EditInstance` 等

**原因**：这些命令是 LaTeX 2024-06-01 内核新增的模板系统（ltcmd），将旧 `xtemplate` 包的功能整合进内核并增强了 API。Tectonic TL2023 的内核不包含这些命令。

**与旧 xtemplate 的区别**：
- `\NewTemplateType{module}{nargs}` — **新命令**，注册模板类型。旧 xtemplate 无此命令，用内部数据结构隐式注册
- `\DeclareTemplateInterface` / `\DeclareTemplateCode` — 存在于旧 xtemplate，但签名和行为有差异
- `\DeclareInstance` / `\UseInstance` — 存在于旧 xtemplate，API 兼容

**修复尝试路径**（已验证失败）：
1. `\RequirePackage{xtemplate}` → `\DeclareTemplateInterface` 等命令可用，但需要 `\NewTemplateType` 先注册类型
2. 简陋 shim（仅设 token list）→ xtemplate 报 `The object type 'sysu' is unknown`，因内部类型注册机制未完成
3. 完整 shim 需要深入 xtemplate 内部数据结构（`\g__xtemplate_type_<name>_tl` 等），实现复杂且脆弱

**处理决策**：遇到此类模板 → **直接跳过，标记为「需 Docker 镜像升级至 TL2024+」**。源码和 AGENTS.md 可照常上线（用户在 TL2024+ 本地环境仍可编译），但 tectonic 编译验证跳过。

**识别特征**：
```bash
grep -n 'NewTemplateType\|DeclareTemplateInterface\|DeclareTemplateCode' *.cls
```
若上述命令有输出，该模板大概率需要 TL2024+。

**已知受影响模板**：sysuthesis（中山大学）、任何使用 `\NewTemplateType` 的新式模板。

**示例（sysuthesis.cls）**：
```latex
\NewTemplateType { sysu } { \c_zero_int }
\DeclareTemplateInterface { sysu } { element } { \c_zero_int }
  { content: tokenlist = \c_empty_tl, ... }
\DeclareTemplateCode { sysu } { element } { \c_zero_int } { ... }
```

## 注意

- `\exp_args:Ne` 对 `\nktget{...}` 这类展开型命令有效，因为 `\nktget` 是可展开的
- 如果被展开的命令不可展开（robust），需要改用 `\tl_set:Nn` + `\tl_if_empty:NTF` 模式
- :e 变体的扫描命令：`grep -n ':e[nNTVFvopwf]' *.cls`

### `\DeclareKeys` / `\SetKeys` → expl3 原生 `\keys_define:nn` / `\keys_set:nn`

**症状**：`Undefined control sequence` at `\DeclareKeys` 或 `\SetKeys`，即使已加载 `\RequirePackage{l3keys2e}` 也无效

**原因**：tectonic 的 l3keys2e 包版本早于 2022-06-01，不含 `\DeclareKeys`、`\SetKeys`、`\ProcessKeyOptions` 三个命令。**仅加载 l3keys2e 不足以修复**——这三个命令全部需要替换为 expl3 原生等价物。

**诊断**：
```bash
grep -n 'DeclareKeys\|SetKeys\|ProcessKeyOptions' *.cls *.def 2>/dev/null
```

**修复三步**（以 module 名 `nwputhesis` 为例，替换为你模板的实际 module 名）：

**Step 1：将 `\DeclareKeys [ <module> ]` 替换为 `\keys_define:nn { <module> }`**

```latex
% 旧：
\DeclareKeys [ nwputhesis ]
  {
    title    .code:n = { \set@title {#1} },
    author   .code:n = { \set@author {#1} },
  }

% 新（语法完全兼容，只是命令名变化）：
\keys_define:nn { nwputhesis }
  {
    title    .code:n = { \set@title {#1} },
    author   .code:n = { \set@author {#1} },
  }
```

注意：`.default:n`、`.code:n`、`unknown .code:n` 等 key 属性语法在 `\keys_define:nn` 中完全一致，无需修改键定义体本身。

**Step 2：将 `\SetKeys [ <module> ] { <args> }` 替换为 `\keys_set:nn { <module> } { <args> }`**

```latex
% 旧：\SetKeys [ nwputhesis ] {#1}
% 新：
\keys_set:nn { nwputhesis } {#1}
```

**Step 3：将 `\ProcessKeyOptions [ <module> ]` 替换为手动处理 `\@classoptionslist`**

这是最关键的一步。`\ProcessKeyOptions`（以及 `\ProcessKeysOptions`）在旧版 l3keys2e 中均不可用。需用以下代码块替换：

```latex
%% 手动处理 \@classoptionslist（兼容旧 LaTeX 内核）
\cs_new_protected:Npn \__<module>_process_class_options:
  {
    \clist_if_empty:NF \@classoptionslist
      {
        \exp_args:Nnx \keys_set:nn { <module> } { \@classoptionslist }
      }
  }
\__<module>_process_class_options:
```

将 `<module>` 替换为模板的 module 名（如 `nwputhesis`）。

**完整示例（nwputhesis 模板）**：

原始代码（options.def）：
```latex
\DeclareKeys [ nwputhesis ]
  {
    degree   .code:n = { \nwpu_degree_set:n {#1} },
    lang     .code:n = { \nwpu_lang_set:n {#1} },
    unknown  .code:n = { \nwpu_unknown_key:n {#1} },
  }
\ProcessKeyOptions [ nwputhesis ]
```

修复后：
```latex
\keys_define:nn { nwputhesis }
  {
    degree   .code:n = { \nwpu_degree_set:n {#1} },
    lang     .code:n = { \nwpu_lang_set:n {#1} },
    unknown  .code:n = { \nwpu_unknown_key:n {#1} },
  }
\cs_new_protected:Npn \__nwpu_process_class_options:
  {
    \clist_if_empty:NF \@classoptionslist
      {
        \exp_args:Nnx \keys_set:nn { nwputhesis } { \@classoptionslist }
      }
  }
\__nwpu_process_class_options:
```

同样修复方法也需应用于 `\nwputhesissetup` 内部的 `\SetKeys` 调用：
```latex
% 旧：
\NewDocumentCommand \nwputhesissetup { m }
  {
    \SetKeys [ nwputhesis ] {#1}
  }

% 新：
\NewDocumentCommand \nwputhesissetup { m }
  {
    \keys_set:nn { nwputhesis } {#1}
  }
```

**已验证模板**：nwputhesis（西北工业大学）— `\DeclareKeys` 出现于 `infra/options.def` 和 `infra/metadata.def`，`\SetKeys` 出现于 `infra/metadata.def`。三处全部替换后编译通过。
