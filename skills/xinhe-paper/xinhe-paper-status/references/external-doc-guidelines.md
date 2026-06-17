# 心河Paper 对外材料生成规范

当用户要求生成对外材料（评审申报、产品介绍、BP、宣传文档等）时，必须遵守以下规则。

## 1. 禁止暴露运营数据

以下数据**绝对禁止**出现在对外文档中：

- 用户总数、新增用户数、活跃用户数
- 会话总数、完成会话数
- 模板使用次数、排行榜排名数字
- 任何从 `xinhe-paper overview` / `top-templates` / `template-usage` 查询到的定量指标

这些是核心竞争数据。对外文档只能做**定性描述**（如"覆盖主流竞赛""服务多所高校学生"），不能引用具体数字。

**内部使用**（团队决策、战略分析）可以正常使用数据。

## 2. 定价信息必须从产品页面验证

记忆中的定价信息（49.9/99/149）可能来自过往的口播稿约定，可能与当前产品实际方案不一致。写对外材料前必须：

```
1. 打开 paper.huimengxinhe.com/profile（用 Kimi WebBridge）
2. 点击"升级会员"按钮
3. 从页面读取实际的档位名称、价格、权益额度
```

**不要**从 memory 或之前生成的文档里抄定价信息。

## 3. PDF 生成：避免 LaTeX 工具链

本机环境问题：
- tectonic 无法从网络下载 LaTeX 宏包（relay.fullyjustified.net 不可达）
- cupsfilter 不支持 text/html → application/pdf 转换
- wkhtmltopdf / weasyprint 未安装
- pip 有 SSL 证书问题，无法安装 fpdf2

→ **正确做法**：生成自包含 HTML（内联 CSS，无外部依赖），交给用户用浏览器"打印 → 另存为 PDF"。

HTML 模板参见 `templates/external-doc-template.html`。
