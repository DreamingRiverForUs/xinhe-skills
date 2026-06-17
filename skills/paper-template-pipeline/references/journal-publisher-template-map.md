# 期刊投稿模板 — 出版商到 LaTeX 模板映射

## 出版商 → 文档类

| 出版商 | 推荐模板 | 获取方式 | 许可证 |
|--------|----------|----------|--------|
| **Elsevier** | `elsarticle.cls` | tectonic bundle 自动下载 或 CTAN mirrors.ctan.org/macros/latex/contrib/elsarticle.zip | LPPL |
| **Springer Nature** | `sn-jnl.cls` | Springer CDN: https://resource-cms.springernature.com/.../LaTeX-template.zip | 官方分发 |
| **IEEE** | `IEEEtran.cls` | tectonic bundle 自动下载 | LPPL |
| **Taylor & Francis** | `article` + natbib + apa | interact.cls 不可公开分发，用标准 article 替代 | — |
| **Wiley** | `article` + natbib + apalike | 无公开 cls，apalike.bst 在 TeX Live 中 | — |
| **Emerald** | `article` + natbib + apa | 无公开 cls | — |

## 模板特征

| 出版商 | 引用风格 | 字体 | 列数 | 特殊宏包 |
|--------|----------|------|------|----------|
| Elsevier | 数字或 Harvard | Times | 单/双列 | elsarticle 前后置结构 |
| Springer | 数字 (sn-mathphys-num) | Times | 单列 | sn-jnl 内置定理环境 |
| IEEE | 数字 [1] | Times | 双列 | IEEEtran 专用定理 |
| T&F | APA 作者-年 | Times New Roman | 单列 | double-spaced 投稿 |
| Wiley | APA-like 作者-年 | Times New Roman | 单列 | apalike.bst |
| Emerald | APA 作者-年 | Times New Roman | 单列 | 同 T&F 模式 |

## 批量上线流程

```
1. 按出版商分组（6 组 13 本期刊 = 每出版商 1-4 本）
2. 每组获取/确认通用模板 cls 文件
3. delegate_task 并行上线（每批 3 个，纯英文无 CJK 依赖）
4. 每期刊仓库包含: cls + 期刊特化示例 main.tex + references.bib + CI
```

## 示例内容策略

每个期刊的 `main.tex` 应包含该期刊领域的**技术深度示例**：
- 运筹/优化类: MILP 模型 + 算法伪代码 + 数值实验
- 供应链类: 博弈模型 + 案例研究 + 管理洞察
- 工程管理类: 框架图 + 假设-命题 + 实证设计

## Pitfalls

- **T&F interact.cls 不可公开分发**：Taylor & Francis 官方 LaTeX 模板需从 Author Services 下载，不在 CTAN。GitHub 搜索返回空结果。**处理**：用 `article` + `natbib` + `apa` 替代，README 中说明获取官方 cls 的链接。
- **Wiley/emerald 同样无公开 cls**：这两个出版商的官方文档类也不在 CTAN 或 GitHub 上。使用 `article` + `apalike` (Wiley) 或 `article` + `apa` (Emerald)。
- **Elsevier elsarticle 从 CTAN zip 不包含预编译 cls**：CTAN 上的 elsarticle.zip 只有源码 (.dtx)，需要触发 tectonic 编译一次让其自动下载 cls，再从 tectonic 缓存提取 `~/.cache/paper-tectonic/bundles/data/<hash>/elsarticle.cls`。
- **期刊模板全英文，零 CJK 依赖**：无需 ctex、fontset、init.sh 字体下载。这使得 delegate_task 子 Agent 成功率极高（接近 100%），每个约 4-8 分钟。
- **按出版商分组复用模板**：同一出版商的多个期刊共享同一个文档类。先获取/确认通用 cls 一次，然后每个期刊仅在 main.tex 示例内容上有差异。不要为每个期刊重新搜索模板。
