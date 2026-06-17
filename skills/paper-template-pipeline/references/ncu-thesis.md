# 南昌大学论文模板 (NCU Thesis)

## 基本信息

| 属性 | 值 |
|------|-----|
| 上游仓库 | Jin-bao/NCU-thesis |
| 文档类 | ncuthesis.cls (expl3-based) |
| 基础类 | ctexbook, fontset=none |
| 版本 | v1.1f (2025/03/26) |
| 目标仓库 | iftaken/ncu-thesis |

## 模板结构

```
.
├── main.tex              # 论文主入口
├── ncuthesis.cls         # 核心文档类 (expl3)
├── references.bib        # 参考文献 (BibTeX, gbt7714-numerical)
├── resources/
│   ├── academic.clo      # 学术硕士设置 (默认)
│   ├── professional.clo  # 专业硕士设置
│   ├── bachelor.clo      # 本科设置
│   ├── newcmd.def        # 自定义命令 (含 \lr, \thickhline 等)
│   ├── newenv.def        # 自定义环境 (定理类)
│   ├── logo.jpg          # 校徽
│   └── logo-name.png     # 校名图片
```

## 字体策略

**零外部字体下载** — 全部使用 tectonic bundle 内置字体。

| 字体类型 | Linux/Docker | Windows |
|----------|-------------|---------|
| CJK (宋/黑) | FandolSong/FandolHei (Extension=.otf) | SimSun/SimHei |
| CJK (楷/仿) | FandolKai/FandolFang (Extension=.otf) | KaiTi/FangSong |
| 英文正文 | XITS (Extension=.otf) | XITS |
| 英文无衬线 | FiraSans (Extension=.otf) | FiraSans |
| 英文等宽 | FiraMono (Extension=.otf) | FiraMono |
| 数学 | XITSMath-Regular + XITSMath-Bold + NewCMMath-Book | 同左 |

**自动检测逻辑** (`academic.clo` line 400-403):
- Windows → `cjk-font=windows`
- 非 Windows (Linux/Docker) → `cjk-font=fandol`

所有字体通过 `Extension=.otf` + kpathsea 文件名查找加载，**不走 fontspec 系统字体搜索**。Fandol 四体、XITS、FiraSans/FiraMono 均在 tectonic bundle 中可用。

## 适配要点

### 必须修复: `\tl_if_eq:enT` → `\exp_args:Ne \tl_if_eq:nnT`

`resources/newcmd.def` 中的 `\lr` 命令（左右定界符配对）使用了 TL2024 `:e` 变体:

```latex
% 原始 (TL2024, 不可用)
\NewDocumentCommand \lr {mmm} {
  \tl_if_eq:enT {#1} {.} {\kern-\nulldelimiterspace}
  ...
}

% 修复 (TL2023 兼容)
\NewDocumentCommand \lr {mmm} {
  \exp_args:Ne \tl_if_eq:nnT {#1} {.} {\kern-\nulldelimiterspace}
  ...
}
```

这是 TL2023 适配的**唯一必要修改**。模板主体使用 `\ProcessKeysOptions`（带 's'，旧版语法），已经 TL2023 兼容。

### 无需修改的部分

- 字体: 全 tectonic bundle 内置，无需 init.sh 下载
- ctexbook fontset=none + 手动 Fandol: 正常
- XITSMath 数学字体: `\setmathfont {XITSMath-Regular.otf}` 通过 kpathsea 加载正常
- `\ProcessKeysOptions {ncu/option}`: 旧版语法，TL2023 兼容
- `\keys_define:nn`: TL2023 原生支持

## 编译命令

```bash
docker run --rm --platform linux/amd64 \
  -v $(pwd):/app \
  -v ~/.cache/paper-tectonic:/root/.cache/Tectonic \
  crpi-b75iph3qtzyryyvz.cn-hangzhou.personal.cr.aliyuncs.com/paper-prod/paper-sandbox-cli:latest \
  tectonic -X compile main.tex
```

## 已知警告（安全）

- `Missing character: U+245F (⑟) in font [XITS-Regular.otf]`: 示例文本中的 Unicode 脚注标记字符，不影响输出
- 编译后自动 rerun（BibTeX → aux changed → TeX rerun → xdvipdfmx）
