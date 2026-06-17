# Customization 平台模式适配

当模板使用平台分支式字体配置（如 windows/macos/ubuntu/web/customization），但 Docker 不属于其中任一正常分支时，优先使用 `customization` 模式。

## 适用场景

- 模板自身管理 `\setmainfont`/`\setCJKmainfont`，按平台分支做 if/else 选择
- Docker（Linux 容器）的字体环境与 ubuntu 分支不完全匹配（如 ubuntu 用 FandolSong 但 Docker 无）
- 使用 `customization` 模式后，模板不主动设置字体，交由 ctex 自动检测或用户在 main.tex 中声明

## 典型例子：DLML thesis (dlmuthesis.cls)

dlmuthesis.cls 有 5 个平台分支：
- `windows` → SimSun + Times New Roman ✓ Docker 可工作（但语义不对）
- `macos` → STSong + Times New Roman ✗ Docker 无 STSong
- `ubuntu` → FandolSong + Times New Roman ✗ Docker 无 FandolSong
- `web` → 同 ubuntu ✗
- `customization` → 不设置任何字体，交由用户/ctex 处理 ✓

直接用 `customization` 模式：
```latex
\documentclass[MA,customization]{dlmuthesis}
```

ctex 自动检测到 Docker 中的 SimSun/SimHei/CJK 字体，英文使用默认 Latin Modern。无需下载任何字体，init.sh 仅需创建空 font/ 目录。

## 关键前提

`customization` 模式仅在模板**未**使用 `ctex` 的 `fontset=...` 选项且**未**强制要求特定字体时可行。ctex 能通过 fontconfig 自动发现 Docker 镜像预装的 SimSun、SimHei、Times New Roman 等字体。

## 检查清单

1. 确认模板的 customization 分支不设置字体（仅 `\typeout{...}`）
2. 确认模板没有 `\newCJKfontfamily` 等命令在 customization 分支外无条件执行（定义即可，调用才出错）
3. 确认 ctex 加载时未指定 `fontset=...`（否则 ctex 会自行管理字体）
4. 编译后验证中英文渲染正常
