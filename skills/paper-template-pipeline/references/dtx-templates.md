# dtx/docstrip 模板处理

部分 LaTeX 模板以 dtx（DocTeX）格式发布，需从 .dtx/.ins 中提取 .cls/.sty 文件后才能编译。

## 识别特征

- 仓库中有 `.dtx` 和 `.ins` 文件
- `.dtx` 内包含大量 `%<class>` / `%<*class>` 标记行
- README 中提到 `l3build unpack` 或 `latex nkthesis.ins` 生成类文件

## 获取 .cls 文件

### 方式 A：从 GitHub Releases 下载（优先）

多数 dtx 模板的 Release 中会附带预编译的 .cls 文件：

```bash
gh release download --repo <owner>/<repo> --pattern '*.cls' --dir .
```

**优点**：不依赖本地 TeX 环境。**Pitfall**：需确认 Release 版本匹配仓库源码版本。

### 方式 B：本地 l3build 解包

```bash
l3build unpack
# 生成 build/unpacked/<name>.cls
cp build/unpacked/<name>.cls .
```

需要 `l3build` 命令（TeX Live 自带）。macOS 上通常 `which l3build` 找不到时用方式 A。

### 方式 C：Docker 中运行 latex

```bash
docker run --rm --platform linux/amd64 \
  -v $(pwd):/app \
  <镜像> latex nkthesis.ins
```

## .gitignore 注意

dtx 源仓库通常把 `*.cls` 写入 .gitignore（因为 .cls 是生成文件）。但心河Paper 模板中 **nkthesis.cls 必须进 git 追踪**，需在 .gitignore 中加例外：

```
*.cls   ← 源仓库可能有这条
```

心河Paper 的 .gitignore 中**不要复制 `*.cls` 规则**，或改用 `!nkthesis.cls` 例外。

## 示例：nkthesis（南开大学）

- 源：`alumik/nkthesis`，v2026.5.0
- `.ins` 中 `\generate{\file{nkthesis.cls}{\from{nkthesis.dtx}{class}}}` 生成 nkthesis.cls
- Release 中直接提供预编译 nkthesis.cls，无需本地编译
- 注意：`nkthesis.cls` 引用 `\\NeedsTeXFormat{LaTeX2e}[2024/11/01]` 及大量 expl3 新版语法（`:e` 变体、`\\ProcessKeyOptions` 等）。在 tectonic 的 TeX Live ≈2023 环境需多步修复，详见 `references/tectonic-expl3-compatibility.md`。
