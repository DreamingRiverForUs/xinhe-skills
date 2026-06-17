---
name: paper-template-pipeline
description: 心河Paper 模板自动化上线流水线。从模板确定 → GitHub 仓库创建 → 结构初始化 → Docker 编译验证 → 推送上线。适用于方式2（LaTeX 平台整合）模板。
category: productivity
---

# 心河Paper 模板自动化上线流水线

## 触发条件

飞书多维表格中有"待适配"状态的模板（方式2，LaTeX 来源），需要走完上线流程。

## 流水线总览

```
[① 模板确定] → [② 仓库创建] → [③ 结构初始化] → [④ 适配开发] → [⑤ 编译验证] → [⑥ 推送上线]
```

**预计耗时**：单个模板 10-30 分钟。tectonic 初次编译需下载资源包（~3-8 分钟），字体下载 ~30s，Git 操作秒级。**子 Agent 模式 timeout 需 ≥ 1800s（30分钟）**。

## 变体：预存仓库恢复上线（Resume）

当目标仓库已存在（如从前期占位先行或中断的适配流程恢复），且结构已完整（AGENTS.md、main.tex、.cls、.gitignore、init.sh、references.bib 齐备），跳过②③④阶段，走简化流程：

```
[①R 核对AGENTS.md UUID] → [⑤R Docker编译验证] → [⑥R 推送上线]
```

**关键动作**：
1. 核对 AGENTS.md 中 TeXPage URL 的 UUID 与任务指定是否一致——不一致则修正
2. Docker 编译验证（同标准流程⑤）
3. git commit + push（同标准流程⑥）
4. 飞书记录更新为\"已上线\"

**诊断**：若仓库存在但 AGENTS.md UUID 是旧值（如模板版本不同导致的 ID 差异），说明仓库来自前期占位/初始适配，UUID 未被修正。这是预期场景，直接修正即可。

**批量编译验证变体**：当任务是验证一批已上线的模板仍可编译（无适配、无 PII 清洗），走简化循环：clone → Docker 编译 → git add -f main.pdf + commit + push。详细流程见 `references/batch-compile-verification.md`。注意：Docker tectonic 编译建议分批并行（≤4/批，缓存竞争极少）；非标准 .tex 文件名（sample.tex / anor-article.tex）直接用实际文件名编译和推送，不算 FAIL。

## 全局资源

| 资源 | 路径 |
|------|------|
| AGENTS.md 模板 | `templates/AGENTS.md` |
| .gitignore 模板 | `templates/gitignore.template` |
| init.sh 模板 | `templates/init.sh.template` |
| dtx 提取脚本 | `scripts/extract_dtx.py` |
| 字体链接库 | `references/font_url.txt` |
| 编译错误速查 | `references/tectonic-quick-fix.md` |
| Docker 镜像 | `crpi-b75iph3qtzyryyvz.cn-hangzhou.personal.cr.aliyuncs.com/paper-prod/paper-sandbox-cli:latest` |
| PII 清洗规范 | `references/pii-scrubbing.md` |
| 字体可用性参考 | `references/font-availability.md` |
| 字体扫描方法 | `references/font-scanning.md` |
| 模板管理飞书表格 | `references/template-management-table.md` |
| WebBridge 模板导入 | `references/web-bridge-template-onboarding.md` |
| PII 清洗批量工作流 | `references/pii-scrubbing-batch-workflow.md` |
| config-driven 无 .cls 模板 | `references/config-driven-no-cls-template.md` |
| customization 平台模式 | `references/customization-platform-mode.md` |
| tectonic/expl3 兼容性 | `references/tectonic-expl3-compatibility.md` |
| 期刊投稿模板（出版商映射） | `references/journal-publisher-template-map.md` |
| 外国期刊快速上线 | `references/foreign-journal-templates.md` |
| dtx 模板处理 | `references/dtx-templates.md` |
| CCT→ctexart 适配 | `references/cct-to-ctexart-adaptation.md` |
| 数学学报(中文)模板 | `references/acta-math-sinica.md` |
| 南开大学论文模板 | `references/nankai-template.md` |
| 南昌大学论文模板 | `references/ncu-thesis.md` |
| 信阳师范大学模板（XYNU） | `references/xynu-template.md` |
| 全国大学生数学建模（CUMCM）模板 | `references/cumcm-template.md` |
| 研究生数学建模（GMCM）模板 | `references/gmcm-template.md` |
| 亚太数学建模（APMCM）模板 | `references/apmcm-template.md` |
| 数维杯（SWMCM）模板 | `references/swmcm-template.md` |
| GB 国家标准模板 | `references/gb-template.md` |
| 四川大学 Beamer 模板 (SCU) | `references/scu-beamer.md` |
| 期刊投稿模板（出版商映射） | `references/journal-publisher-template-map.md` |
| MDPI 期刊模板 | `references/mdpi-template.md` |ferences/nankai-template.md` |
| 全国大学生数学建模（CUMCM）模板 | `references/cumcm-template.md` |
| 研究生数学建模（GMCM）模板 | `references/gmcm-template.md` |
| 亚太数学建模（APMCM）模板 | `references/apmcm-template.md` |
| 数维杯（SWMCM）模板 | `references/swmcm-template.md` |
| GB 国家标准模板 | `references/gb-template.md` |
| 四川大学 Beamer 模板 (SCU) | `references/scu-beamer.md` |
| 期刊投稿模板（出版商映射） | `references/journal-publisher-template-map.md` |
| 外国期刊快速上线 | `references/foreign-journal-templates.md` |
| dtx 模板处理 | `references/dtx-templates.md` |
| CCT→ctexart 适配 | `references/cct-to-ctexart-adaptation.md` |s/foreign-journal-templates.md` |
| dtx 模板处理 | `references/dtx-templates.md` |
| CCT→ctexart 适配 | `references/cct-to-ctexart-adaptation.md` |
| 数学学报(中文)模板 | `references/acta-math-sinica.md` |
| 南开大学论文模板 | `references/nankai-template.md` |
| 南昌大学论文模板 | `references/ncu-thesis.md` |
| 信阳师范大学模板（XYNU） | `references/xynu-template.md` |
| 全国大学生数学建模（CUMCM）模板 | `references/cumcm-template.md` |
| 研究生数学建模（GMCM）模板 | `references/gmcm-template.md` |
| 亚太数学建模（APMCM）模板 | `references/apmcm-template.md` |
| 数维杯（SWMCM）模板 | `references/swmcm-template.md` |
| GB 国家标准模板 | `references/gb-template.md` |
| 四川大学 Beamer 模板 (SCU) | `references/scu-beamer.md` |
| 期刊投稿模板（出版商映射） | `references/journal-publisher-template-map.md` |
| 外国期刊快速上线 | `references/foreign-journal-templates.md` |
| dtx 模板处理 | `references/dtx-templates.md` |
| CCT→ctexart 适配 | `references/cct-to-ctexart-adaptation.md` |
| 内蒙古科技大学本科生毕业设计模板 | `references/imust-bachelor-thesis.md` |
| 北京理工大学 BIThesis（研究生+本科） | `references/bit-template.md` |
| 期刊投稿模板（出版商映射） | `references/journal-publisher-template-map.md` |
| 外国期刊快速上线 | `references/foreign-journal-templates.md` |
| dtx 模板处理 | `references/dtx-templates.md` |
| CCT→ctexart 适配 | `references/cct-to-ctexart-adaptation.md` |
| 数学学报(中文)模板 | `references/acta-math-sinica.md` |
| 南开大学论文模板 | `references/nankai-template.md` |
| 南昌大学论文模板 | `references/ncu-thesis.md` |
| 信阳师范大学模板（XYNU） | `references/xynu-template.md` |
| 全国大学生数学建模（CUMCM）模板 | `references/cumcm-template.md` |
| 研究生数学建模（GMCM）模板 | `references/gmcm-template.md` |
| 亚太数学建模（APMCM）模板 | `references/apmcm-template.md` |
| 数维杯（SWMCM）模板 | `references/swmcm-template.md` |
| GB 国家标准模板 | `references/gb-template.md` |
| 四川大学 Beamer 模板 (SCU) | `references/scu-beamer.md` |
| 期刊投稿模板（出版商映射） | `references/journal-publisher-template-map.md` |
| 外国期刊快速上线 | `references/foreign-journal-templates.md` |
| dtx 模板处理 | `references/dtx-templates.md` |
| CCT→ctexart 适配 | `references/cct-to-ctexart-adaptation.md` |
| 期刊投稿模板（出版商映射） | `references/journal-publisher-template-map.md` |
| 外国期刊快速上线 | `references/foreign-journal-templates.md` |
| dtx 模板处理 | `references/dtx-templates.md` |
| CCT→ctexart 适配 | `references/cct-to-ctexart-adaptation.md` |
| 数学学报(中文)模板 | `references/acta-math-sinica.md` |
| 南开大学论文模板 | `references/nankai-template.md` |
| 南昌大学论文模板 | `references/ncu-thesis.md` |
| 信阳师范大学模板（XYNU） | `references/xynu-template.md` |
| 全国大学生数学建模（CUMCM）模板 | `references/cumcm-template.md` |
| 研究生数学建模（GMCM）模板 | `references/gmcm-template.md` |
| 亚太数学建模（APMCM）模板 | `references/apmcm-template.md` |
| 数维杯（SWMCM）模板 | `references/swmcm-template.md` |
| GB 国家标准模板 | `references/gb-template.md` |
| 四川大学 Beamer 模板 (SCU) | `references/scu-beamer.md` |
| 期刊投稿模板（出版商映射） | `references/journal-publisher-template-map.md` |
| 外国期刊快速上线 | `references/foreign-journal-templates.md` |
| dtx 模板处理 | `references/dtx-templates.md` |
| CCT→ctexart 适配 | `references/cct-to-ctexart-adaptation.md` |
| 内蒙古科技大学本科生毕业设计模板 | `references/imust-bachelor-thesis.md` |
| 北京理工大学 BIThesis（研究生+本科） | `references/bit-template.md` |
| 内蒙古科技大学微型计算机实训模版 | `references/imust-microcomputer-template.md` |
| 清华大学硕博论文模板 | `references/thu-thesis.md` |
| 中国科学技术大学论文模板 | `references/ustc-thesis.md` |
| 苏大 sudathesis（thuthesis 派生，本地字体检测） | `references/suda-thuthesis-adaptation.md` |
| ustcthesis 派生模板（陕西理工等，force windows fontset） | `references/ustcthesis-derivative.md` |
| 武汉大学论文模板 (WHU) | `references/whu-thesis.md` |
| 武汉大学开题报告模板 (WHU Proposal) | `references/whu-proposal.md` |
| memoir/GOST 非CJK模板（俄语论文） | `references/memoir-gost-template.md` |
thesis.md` |
| 内蒙古科技大学本科生毕业设计模板 | `references/imust-bachelor-thesis.md` |
| 北京理工大学 BIThesis（研究生+本科） | `references/bit-template.md` |
| 期刊投稿模板（出版商映射） | `references/journal-publisher-template-map.md` |
| 外国期刊快速上线 | `references/foreign-journal-templates.md` |
| dtx 模板处理 | `references/dtx-templates.md` |
| CCT→ctexart 适配 | `references/cct-to-ctexart-adaptation.md` |
| 数学学报(中文)模板 | `references/acta-math-sinica.md` |
| 南开大学论文模板 | `references/nankai-template.md` |
| 南昌大学论文模板 | `references/ncu-thesis.md` |
| 信阳师范大学模板（XYNU） | `references/xynu-template.md` |
| 全国大学生数学建模（CUMCM）模板 | `references/cumcm-template.md` |
| 研究生数学建模（GMCM）模板 | `references/gmcm-template.md` |
| 亚太数学建模（APMCM）模板 | `references/apmcm-template.md` |
| 数维杯（SWMCM）模板 | `references/swmcm-template.md` |
| GB 国家标准模板 | `references/gb-template.md` |
| 四川大学 Beamer 模板 (SCU) | `references/scu-beamer.md` |
| 期刊投稿模板（出版商映射） | `references/journal-publisher-template-map.md` |
| 外国期刊快速上线 | `references/foreign-journal-templates.md` |
| dtx 模板处理 | `references/dtx-templates.md` |
| CCT→ctexart 适配 | `references/cct-to-ctexart-adaptation.md` |s/foreign-journal-templates.md` |
| dtx 模板处理 | `references/dtx-templates.md` |
| CCT→ctexart 适配 | `references/cct-to-ctexart-adaptation.md` |
| 数学学报(中文)模板 | `references/acta-math-sinica.md` |
| 南开大学论文模板 | `references/nankai-template.md` |
| 南昌大学论文模板 | `references/ncu-thesis.md` |
| 信阳师范大学模板（XYNU） | `references/xynu-template.md` |
| 全国大学生数学建模（CUMCM）模板 | `references/cumcm-template.md` |
| 研究生数学建模（GMCM）模板 | `references/gmcm-template.md` |
| 亚太数学建模（APMCM）模板 | `references/apmcm-template.md` |
| 数维杯（SWMCM）模板 | `references/swmcm-template.md` |
| GB 国家标准模板 | `references/gb-template.md` |
| 四川大学 Beamer 模板 (SCU) | `references/scu-beamer.md` |
| 期刊投稿模板（出版商映射） | `references/journal-publisher-template-map.md` |
| 外国期刊快速上线 | `references/foreign-journal-templates.md` |
| dtx 模板处理 | `references/dtx-templates.md` |
| CCT→ctexart 适配 | `references/cct-to-ctexart-adaptation.md` |
| 南昌大学论文模板 | `references/ncu-thesis.md` |
| 韶关学院本科毕业论文模板 | `references/sgu-template.md` |
| 韶关学院期末考试试卷模板 | `references/sgu-exam-template.md` |
| 计算机学报模板 | `references/cjc-template.md` |
| CVPR / ICCV / ECCV 论文模板 | `references/cvpr-template.md` |
| 中国地质大学武汉CUG本科生毕业论文模板英文版 | `references/cug-english-template.md` |
| 大连海事大学论文模板（DLMU） | `references/dlmu-thesis.md` |
| 湖南大学本科毕业论文模板（HNU） | `references/hnu-bachelor-thesis.md` |
| ACL 论文模板 | `references/acl-template.md` |
| 内蒙古科技大学硕士学位论文模板 | `references/imust-master-thesis.md` |
| 内蒙古科技大学本科生毕业设计模板 | `references/imust-bachelor-thesis.md` |
| 北京理工大学 BIThesis（研究生+本科） | `references/bit-template.md` |
| 内蒙古科技大学微型计算机实训模版 | `references/imust-microcomputer-template.md` |
| 清华大学硕博论文模板 | `references/thu-thesis.md` |
| 中国科学技术大学论文模板 | `references/ustc-thesis.md` |
| 苏大 sudathesis（thuthesis 派生，本地字体检测） | `references/suda-thuthesis-adaptation.md` |
| ustcthesis 派生模板（陕西理工等，force windows fontset） | `references/ustcthesis-derivative.md` |
| 武汉大学论文模板 (WHU) | `references/whu-thesis.md` |
| 武汉大学开题报告模板 (WHU Proposal) | `references/whu-proposal.md` |
| memoir/GOST 非CJK模板（俄语论文） | `references/memoir-gost-template.md` |
is.md` |
| 内蒙古科技大学本科生毕业设计模板 | `references/imust-bachelor-thesis.md` |
| 北京理工大学 BIThesis（研究生+本科） | `references/bit-template.md` |
| 内蒙古科技大学微型计算机实训模版 | `references/imust-microcomputer-template.md` |
| 清华大学硕博论文模板 | `references/thu-thesis.md` |
| 中国科学技术大学论文模板 | `references/ustc-thesis.md` |
| 苏大 sudathesis（thuthesis 派生，本地字体检测） | `references/suda-thuthesis-adaptation.md` |
| ustcthesis 派生模板（陕西理工等，force windows fontset） | `references/ustcthesis-derivative.md` |
| 武汉大学论文模板 (WHU) | `references/whu-thesis.md` |
| 武汉大学开题报告模板 (WHU Proposal) | `references/whu-proposal.md` |
| memoir/GOST 非CJK模板（俄语论文） | `references/memoir-gost-template.md` |

| 字体链接库 | `references/font_url.txt` |
| 编译错误速查 | `references/tectonic-quick-fix.md` |
| Docker 镜像 | `crpi-b75iph3qtzyryyvz.cn-hangzhou.personal.cr.aliyuncs.com/paper-prod/paper-sandbox-cli:latest` |
| tectonic 缓存（宿主机） | `~/.cache/paper-tectonic` |
| 模板工作区 | `~/project/templates/` |

## 各阶段详细操作

### ① 模板确定

**输入**：原始 LaTeX 模板文件（.tex / .cls / .bst / .sty 等）
**动作**：
1. 分析模板结构：文档类、宏包依赖、字体声明
2. 确定模板分类（数模竞赛 / 毕业论文 / 期刊投稿 / ...）
3. 识别所需字体列表
**校验门**：
- [ ] 来源文件完整（至少 .cls + .tex 示例；用 `find . -name '*.cls' | grep -v font` 确认 .cls 存在）
- [ ] 如果 .cls 缺失 — 检查上游是否仍在（`gh repo view <上游>`），若上游已删除走浏览器提取路径
- [ ] 字体依赖已识别
- [ ] 模板分类已确定

### ② 仓库创建

**动作**：
```bash
gh repo create xinhepaper/<模板名> --private --clone
```
**校验门**：
- [ ] 仓库为 private
- [ ] 本地克隆成功

### ③ 结构初始化

**动作**：
1. 复制 `templates/AGENTS.md` → 项目根目录
2. 复制 `templates/gitignore.template` → 项目 `.gitignore`
3. 根据模板字体依赖，生成 `init.sh`（从 `references/font_url.txt` 匹配字体 URL）
4. 确保 `main.tex`、`references.bib` 占位文件存在
5. 组织原始文件为标准结构

**校验门**：
- [ ] `AGENTS.md` 存在
- [ ] `.gitignore` 排除了 font/ 和编译产物
- [ ] `init.sh` 可执行，字体 URL 正确
- [ ] `main.tex`、`references.bib` 存在

### ④ 适配开发

**PII 清洗**：在适配开发阶段，先扫描并清洗个人信息（姓名、邮箱、手机、学号、GitHub 个人链接等）。完整流程见 `references/pii-scrubbing.md`。

**动作**：详见 `templates/AGENTS.md` 中的工作流。

### ⑤ 编译验证与质检

**Docker 编译**：
```bash
docker run --rm --platform linux/amd64 \
  -v $(pwd):/app \
  -v ~/.cache/paper-tectonic:/root/.cache/Tectonic \
  <镜像> tectonic -X compile main.tex
```

**质检门**（阻断级）：
- [ ] `tectonic -X compile main.tex` 返回 0
- [ ] `main.pdf` 存在且 ≥ 10KB
- [ ] 编译日志无致命 Error
- [ ] `font/` 目录未进入 git 追踪（`git status` 不包含 font/）
- [ ] `main.tex`、`references.bib`、`main.pdf` 三文件存在

**质检项（警告级）**：
- [ ] `AGENTS.md` 格式完整
- [ ] `.gitignore` 有效
- [ ] 中文渲染正常（视觉抽查）

### ⑥ 推送上线

**动作**：
```bash
git add -A
git commit -m "init: <模板名> - 编译验证通过"
git push origin main
```
**校验门**：
- [ ] push 成功
- [ ] 远程仓库可见

## 字体适配（阶段④ 最关键步骤）

编译前扫描 `.cls` 中字体声明。**核心规则**：`\setmainfont`/`\setsansfont` 和 `\setCJKfamilyfont` 的 `Path=` 行为不同。详见 `references/font-availability.md`。扫描方法见 `references/font-scanning.md`。

快速决策：Times New Roman / Liberation Sans / SimSun / SimHei → 系统字体直接用。Arial → 改用 Liberation Sans。Arial Black → 改用 Noto Sans CJK SC Black。simkai / simfang → init.sh 下载。Fandol 系列 → ✅ tectonic bundle 内置（Song/Hei/Kai/Fang 四体齐全），优先使用。TeX Gyre Heros → tectonic bundle 不一定有，改用 FandolHei。TeX Gyre Termes → 改用 Times New Roman（Docker 系统字体）。Noto Sans/Serif CJK → 除非 Docker 预装，否则改用 FandolHei/FandolSong。

**thuthesis 派生模板本地字体检测变体（优先策略）**：部分 thuthesis 派生模板（如 sudathesis）在 .cls 中添加了 `\IfFileExists{./fonts/simsun.ttc}` 作为第一优先级检测。当检测到 fonts/ 目录存在时，走 `Path=fonts/` 本地路径分支，完全绕开系统字体问题。**识别方法**：`grep -n 'IfFileExists.*fonts.*simsun' *.cls`。若存在 → 只需 init.sh 下载字体 + 修复英文系统字体（Arial→Liberation Sans 等），无需 patch CJK 分支。详见 `references/suda-thuthesis-adaptation.md`。

**标准 ctex fontset 三层回退策略**（当模板用 ctex 管理 CJK 字体时）：
0. **先试默认（不加 fontset 选项）**：在 Linux/Docker 上，ctexbook/ctexrep 默认 auto-detect 到 **fandol** fontset，FandolFont 系列（Song/Hei/Kai/Fang）全部在 tectonic bundle 中可用。如果编译通过，这就是最简单的路线——零字体下载。HHU-thesis、sdu-thesis 等 ctexbook 模板均走此路线。
1. 若默认失败（报 Fandol 字体找不到等），尝试 `fontset=ubuntu`（使用 Docker 预装 Noto CJK 字体）→ 若报 `AR PL KaitiM GB cannot be found` 则进入下一层
2. 检查模板实际使用的 CJK 命令（`grep 'songti\\|heiti\\|kaishu\\|fangsong' *.cls *.tex`）
3. **若模板在 .cls 中通过 `\\LoadClass{ctexrep}`（而非 main.tex 的 `\\documentclass`）加载 ctex**：在 cls 的 `\\ProvidesClass` 后、`\\LoadClass` 前插入 `\\PassOptionsToClass{fontset=none}{ctexrep}`，然后在字体设置块末尾手动定义 `\\songti`/`\\heiti`/`\\kaishu`/`\\fangsong`（见下方 pitfall）。**若模板在 main.tex 中通过 `\\documentclass` 加载 ctex**：改 `fontset=none` + 在 `\\documentclass` 后手动声明：
```latex
\\setCJKmainfont{SimSun}
\\setCJKsansfont{SimHei}
\\setCJKmonofont{SimSun}
\\setCJKfamilyfont{zhsong}{SimSun}
\\setCJKfamilyfont{zhhei}{SimHei}
\\NewDocumentCommand\\songti{}{\\CJKfamily{zhsong}}
\\NewDocumentCommand\\heiti{}{\\CJKfamily{zhhei}}
```
若模板也用 `\\kaishu`/`\\fangsong`，回退到 `\\songti`（SimSun 宋体）。**此模式适用于所有 ctex-based 模板**（如 USTBThesis、BITThesis 派生的高校模板）。详见 `references/ustb-template.md`（硕博）和 `references/ustb-bachelor-template.md`（本科）。

## 依赖扫描与补齐（阶段①/④ 关键步骤）

编译前必须扫描模板的**三类外部依赖**，缺失会导致编译失败：

### 1. 字体依赖（最常见）

见 `references/font-scanning.md`。规则：镜像中不存在的字体 → 加入 init.sh + 模板改用 `[Path=./font/]`。

### 2. 输入文件依赖（`\input` / `\include`）

```bash
grep -n '\\\\input\\{|\\\\include\\{' main.tex *.cls 2>/dev/null
```

如果引用的 `.def` / `.cfg` / `.tex` 不在仓库中 → **创建最小 stub**。
例如 NJU 模板缺 `njuthesis-setup.def`，需根据 `.cls` 中的 key 定义写出最小配置文件。

**关键 pitfall**：stub 里用到的 key 必须在 `.cls` 的 `\keys_define:nn` 中存在，否则会报 `unknown key` 错误。用 `grep "keys_define:nn" *.cls` 确认 key 名。

### 3. 资源文件依赖（`\\includegraphics` / logo / 代码文件）

```bash
grep -oP '\\\\includegraphics[^}]*\\{[^}]+\\}' *.cls *.tex *.def 2>/dev/null
# 代码文件引用（lstinputlisting 也引用外部文件，高频遗漏）
grep -rn '\\\\lstinputlisting' chapters/ *.tex 2>/dev/null
```

如果引用的 PDF/PNG/JPG/code 不在仓库中 → 从上游模板仓库补：
```bash
gh repo clone <上游> /tmp/upstream -- --depth 1
find /tmp/upstream -name "<缺失文件>" -exec cp {} . \;
# 代码目录整体复制
cp -r /tmp/upstream/codes .
```

**关键 pitfall**：资源 PDF（如校徽）会被 `.gitignore` 的 `*.pdf` 规则误杀。需在 `.gitignore` 中加例外：
```
!nju-emblem-black.pdf
!nju-name-black.pdf
```

**关键 pitfall**：`\\lstinputlisting` 引用外部代码文件（如 `codes/funfactorial.cpp`），模板作者常用此展示示例代码。这些文件不在标准目录中，编译会报 `File not found`。解决方案：`cp -r <上游>/codes .` 整体复制代码目录。

**关键 pitfall**：`\\includegraphics` 引用的文件在上游仓库中也不存在（如作者忘了提交 `figures/unified.png` 等示例图）。此时编译报 `Unable to load picture or PDF file`，且 `find <上游>/figures -name` 返回空。**修复**：创建最小占位 PNG（1×1 透明像素）避免修改 .tex 源文件。Python 一行：`python3 -c "import struct,zlib;w,h=1,1;raw=b'';raw=b''.join([b'\x00\xff\xff\xff\xff'*w for _ in range(h)]);ihdr=struct.pack('>IIBBBBB',w,h,8,6,0,0,0);crc=lambda d:struct.pack('>I',zlib.crc32(d)&0xffffffff);png=b'\x89PNG\r\n\x1a\n'+b'IHDR'+ihdr+crc(b'IHDR'+ihdr)+b'IDAT'+zlib.compress(raw)+crc(b'IDAT'+zlib.compress(raw))+b'IEND'+crc(b'IEND');open('figures/missing.png','wb').write(png)"`。注意：此方法仅适用于示例/占位图，学校 logo/签章等必须从上游补真实文件。

## 期刊投稿模板上线（新分类）

学术期刊模板与大学论文模板的关键区别：**按出版商分组复用通用文档类**，期刊间仅示例内容不同。

### 出版商 → 模板映射

| 出版商 | 文档类 | 获取方式 |
|--------|--------|----------|
| Elsevier | `elsarticle.cls` | CTAN zip → tectonic触发下载 → 从缓存提取 |
| Springer Nature | `sn-jnl.cls` | Springer CDN 直接下载 |
| IEEE | `IEEEtran.cls` | tectonic bundle 自动下载 |
| Taylor & Francis | `article` + natbib + apa | interact.cls 不可公开分发 |
| Wiley | `article` + natbib + apalike | 无公开 cls |
| MDPI | `mdpi.cls` | GitHub `xiuliyouran/MDPI_Template_LaTex`（官方模板） | 需 EPS→PDF 转换 + 移除 pdftex 选项 |

### 批量上线流程

```
1. 按出版商分组 → 2. 每组获取/确认 cls → 3. delegate_task 并行 3/批 → 4. 每期刊特化示例内容
```

- **先获取通用 cls 一次**，然后每期刊仅写不同的 `main.tex` 示例 + `references.bib`
- **纯英文模板零 CJK 依赖**：无需 ctex、fontset、init.sh 字体下载

- **CJK→English 模板适配模式**：当需要从 CJK 中文模板派生纯英文版本时，步骤为：① 删除 `xeCJK`/`ctex`/`zhnumber`；② 替换 `\ctexset` 为标准 `titlesec`；③ 删除 CJK 字体命令（`\song`/`\hei`/`\ccwd`）；④ 翻译所有中文字符串；⑤ init.sh 设空。详见 `references/cug-english-template.md`。
- **子Agent 成功率极高**（~100%），每个 4-8 分钟
- 示例内容要有**技术深度**：运筹类写 MILP+伪代码，供应链类写博弈模型+案例

### Pitfalls

- **Elsevier elsarticle CTAN zip 不含预编译 cls**：需先触发编译让 tectonic 下载 `elsarticle.cls`，再从缓存提取
- **T&F interact.cls 不可公开分发**：在 README 中说明获取官方 cls 的链接
- **同一出版商多期刊只需一次 cls 获取**：不要每个期刊重复搜索模板

详见 `references/journal-publisher-template-map.md`。

**单文件文章模板**：部分 TeXPage 模板为单文件期刊文章（IEEEtran 等），无需自定义 .cls、使用 xeCJK 直接声明字体、thebibliography 手动参考文献。适配流程与论文模板不同——详见 `references/single-file-article-templates.md`。

### Pitfalls

## 来源渠道速查

| 来源 | 获取方式 | 技能 |
|------|----------|------|
| GitHub 公开仓库 | `gh repo clone` SSH 克隆 | 本技能 |
| TeXPage 模板 | WebBridge → Open as Template → `_texpage_editor.state.doc.toString()` 逐文件提取 | 本技能 |
| Overleaf 模板 | WebBridge → Open as Template → File → Download as source (.zip) | **`overleaf-template-pipeline`** |
| 期刊官网 | curl 下载（Magtech 403 常见） | 本技能 |
| 用户 Word 模板 | 方式1，非本技能范围 | customization-platform-mode |

**Overleaf 优先于 TeXPage**：ZIP 下载包含全部源码和二进制文件，速度快 10 倍。新增模板优先检查 Overleaf 是否有镜像。

| 模板来源 | 获取方式 | 示例 |
|------|----------|------|
| GitHub 公开仓库 | `gh repo clone` 直接克隆 | iftaken/cycmcm_latex |
| GitHub dtx 仓库 | `gh repo clone` + `scripts/extract_dtx.py` 提取 cls/def | nju-lug/NJUThesis |
| GitHub fork（不完整） | 克隆 + 从上游补资源文件 | mrxxx-creat/NJUT → nju-lug/NJUThesis |
| TeXPage 模板 | 浏览器 Open as Template → 创建项目 → 从 GitHub 源仓库克隆 | texpage.com/template/xxx → XurongLiu/HNIE-Thesis-LaTeX-Template |
| 期刊官网下载（Magtech） | 从期刊网站直接下载 zip（如 `CN/item/downloadFile.do?id=N`），解包 cls/tex | actamath.cjoe.ac.cn → amse-new.cls |

详见 `references/dtx-templates.md`。

**期刊官网下载（Magtech 平台）**：国内大量学术期刊使用 Magtech 系统，模板下载 URL 格式为 `<journal>/CN/item/downloadFile.do?id=<N>`。在 TeXPage 模板描述中看到 `From: https://xxx.cjoe.ac.cn/...` 时，直接访问该期刊网站的栏目页，搜索 "downloadFile.do" 找到模板下载链接。示例：`https://actamath.cjoe.ac.cn/Jwk_sxxb_en/CN/item/downloadFile.do?id=10`。下载为 zip 包（通常含 .cls + .tex 示例），走标准流水线。**优点**：无需浏览器、无需登录、直接 curl 下载。

TeXPage 操作流程：

**方式 A：有 GitHub 源仓库（优先）**

```bash
# 方法1（快）：直接从 TeXPage 页面 HTML 提取 GitHub URL
curl -sL -H 'User-Agent: Chrome' https://www.texpage.com/template/<id> | \
  grep -oE 'github\.com/[^"<> ]+' | head -3

# 方法2（稳）：WebBridge snapshot 查看页面描述文本
# 模板描述中通常包含 "项目地址：https://github.com/xxx"
navigate → url → snapshot → 从 tree 中提取 GitHub URL

# 方法3（回退）：GitHub 搜索。当 TeXPage 页面为 SPA 无 GitHub 链接时，
# 优先用 gh search repos（CLI 捷径，比 REST API 更简洁）：
gh search repos <模板关键词> --limit 10
# 若搜索结果不精确，再用 REST API 按模板名称/学校名搜索：
gh api search/repositories?q=<keywords>&per_page=10 | python3 -m json.tool
# 注意：当 TeXPage 描述中提到的是关联仓库（如 whutug/whu-thesis）而非
# 目标仓库（如 whutug/whu-proposal）时，搜索模板类名/功能名而非描述中的仓库名。

# 拿到 GitHub URL 后直接克隆
gh repo clone <owner/repo> /tmp/source
```

**方式 B：无 GitHub 源仓库（回退）**

部分 TeXPage 模板**仅存在于 TeXPage 平台**，没有 GitHub 镜像（实测约占 60%）。此时需要：

**B1: ZIP 下载（已失效 — 全部 404）**

`/api/project/download`、`/api/project/export`、`/api/template/download` 等 8 个端点全部返回 404 或 JSON error（1003 Not logged in）。TeXPage 已下线 ZIP 导出功能。直接跳到 B2。

**B2: CodeMirror JS API（当前唯一可靠路径）**
1. 点击左侧文件树的每个文件，在编辑器中打开
2. 使用 evaluate 调用：`window._texpage_editor.state.doc.toString()`
3. 可直接获取 CodeMirror 6 编辑器的完整内容（不受虚拟视口限制）
4. **注意**：`_texpage_editor` 是 TeXPage 内部变量，平台更新后可能变化。Chrome MV3 Service Worker 长时间闲置会终止（`extension_connected: false`），需 `osascript` 唤醒
5. **限制**：CodeMirror 只能提取**文本文件**（.tex, .cls, .sty, .bib, .md 等）。二进制文件（.jpg, .png, .pdf, .eps）无法通过 `state.doc.toString()` 提取——图片和 PDF 资源需要注释掉相关 `\\includegraphics` 行，或尝试通过 WebBridge network tab 拦截下载 URL 后用 curl 获取（需带 cookie）

**B2: 编辑器逐文件提取（兜底）**
1. 导航 → Open as Template → 进入项目编辑器
2. snapshot 看文件树，逐个 click 文件
3. 读取 CodeMirror 6 内容：
   - 方法A: `document.querySelectorAll('.cm-line')` 逐行读（虚拟视口可能不完整）
   - 方法B: `window._texpage_editor.state.doc.toString()` 获取完整文档（推荐）

详见 `references/texpage-platform.md`。

## 孤儿模板恢复（已编译但未推送的模板发现）\n\n多轮子 Agent 并行处理后，部分模板可能已完成 Docker 编译但未推送或未被飞书记录。发现方法：\n\n```bash\n# 查找所有已编译但无 git remote 的模板\nfor d in /tmp/*/; do\n  if [ -f \"$d/main.pdf\" ] && [ \"$(stat -f%z \"$d/main.pdf\" 2>/dev/null)\" -gt 10000 ]; then\n    remote=$(cd \"$d\" 2>/dev/null && git remote get-url origin 2>/dev/null || echo \"NO_REMOTE\")\n    size=$(stat -f%z \"$d/main.pdf\" 2>/dev/null)\n    echo \"$d | PDF:${size} | remote:${remote}\"\n  fi\ndone | sort -t: -k2 -rn\n```\n\n发现后检查 AGENTS.md 确认模板身份→补全标准结构→初始化 git→推送。\n\n## PII 清洗（非官方模板）

对于个人开发者制作的模板，部署前必须清洗敏感信息。详见 `references/pii-scrubbing.md` — 搜索模式、替换规则、1×1 透明 PNG 生成。

官方期刊模板（Elsevier, Springer, IEEE 等）跳过清洗，仅编译验证。

## 模板管理流水线（导入 + 提交审核）

模板上线三步：**导入 (draft) → 提交审核 (pending) → 管理员批准 (published)**。

详见 `references/template-management-workflow.md` — WebBridge 批量导入脚本、submit-audit 数据库操作、API 端点、Pitfalls。

关键规则：**绝不直接设 status=published**，必须经过 pending 审核状态。

## 批量任务委派

对于批量 TeXPage-only 模板（需人工浏览器提取），可创建飞书任务管理 Base：

1. 使用 `lark-cli base +base-create --as user --name "任务名"` 创建 Base
2. 添加字段：模板名称(text)、TeXPage链接(text)、问题描述(text)、奖金(number)、状态(select:待处理/进行中/已完成)
3. 使用 `+record-upsert` 写入记录（**注意：upsert 的 JSON body 是原始字段映射，不包 `{"fields":{...}}` 外层**）
4. 分享 Base URL 给团队成员

团队成员在浏览器提取源文件后，Agent 接管后续编译→推送流水线。 项目可能包含 GitHub 源仓库没有的额外文件（如 gbt7714.sty），需比对后补全。

## 管道健康检查（快速概览）

需要了解"还有多少模板待处理"时，不逐条翻阅飞书表格 — 直接 grep 统计：

```bash
# 单命令概览
lark-cli base +record-list --as user \
  --base-token ErlObuSw9aTdOysjjkUce6j1nNh \
  --table-id tbl0YkvmiUznuZ8O \
  --limit 200 2>&1 | grep -cE '\["待适配"\]|\["待收集"\]|\["适配中"\]|\["待测试"\]'

# 按状态分别统计
for s in 待适配 待收集 适配中 待测试; do
  count=$(lark-cli base +record-list --as user \
    --base-token ErlObuSw9aTdOysjjkUce6j1nNh \
    --table-id tbl0YkvmiUznuZ8O --limit 200 2>&1 | grep -c "\\\\[\"$s\"\\\\]")
  echo "$s: $count"
done

# 只看"待适配"的具体列表（非 TeXPage 的 Word 模板通常可直接处理）
lark-cli base +record-list --as user \
  --base-token ErlObuSw9aTdOysjjkUce6j1nNh \
  --table-id tbl0YkvmiUznuZ8O --limit 200 2>&1 | grep '待适配'
```

输出解读：
- **待收集** — 还没拿到源文件，大部分是 TeXPage-only，需浏览器提取
- **待适配** — 源文件到手，等待 LaTeX 适配 + Docker 编译验证
- **适配中** — 正在处理或卡住（检查备注看是否需要介入）
- **待测试** — 适配完成待验证

## 批量流水线与飞书联动

### 批量处理模式

```
1. 从飞书表格拉取待处理列表 → 2. 每批 3 并发 → 3. 结果写回飞书 → 4. 下一批，直到全部处理完
```

```bash
# 查询待处理
lark-cli base +record-list --as user --base-token <token> --table-id <table> | grep "Texpage"

# 更新单条记录状态
lark-cli base +record-upsert --as user --base-token <token> --table-id <table> \
  --record-id <id> --json '{"状态":"待适配","适配说明":"具体问题描述"}'

# 批量更新同状态记录（高效：一次调用更新最多 200 条）
lark-cli base +record-batch-update --as user --base-token <token> --table-id <table> \
  --json '{"record_id_list":["reclvAa","reclvBb",...],"patch":{"状态":"已上线"}}'
# 注意：record-batch-update 对所有 record_id_list 应用相同的 patch。
# 如果需要不同状态/GitHub URL，需按状态分组多轮调用。
```

### 子 Agent toolsets 选择

| 模板类型 | toolsets |
|----------|----------|
| 有 GitHub 源 | `["terminal","file","web","skills"]` |
| 无 GitHub 源（方式 B） | `["terminal","file","web","browser","skills","vision"]` |

### 飞书字段参考

| 字段 | field_id | 类型 | 值示例 |
|------|----------|------|--------|
| 状态 | fldsjL3dxX | select | "待适配", "已上线" |
| 适配说明 | fldyq0nwFq | text | "TeXPage-only，无GitHub源" |
| 负责人 | fldALeO1AB | user | open_id（需 contact:user:search scope） |

## Pitfalls

- **Magtech 期刊官网直接下载全部返回 403（高频）**：国内大量学术期刊使用 Magtech 系统，模板下载 URL 格式为 `<journal>/CN/item/downloadFile.do?id=N`。但 Magtech 平台对非浏览器请求（curl/wget）有访问控制，所有 id 均返回 403。**处理**：此时模板只能从 TeXPage 获取源文件；若无 GitHub 源仓库，走「占位先行 + TeXPage 浏览器提取」。已验证被 403 阻止的期刊：actamath.cjoe.ac.cn（数学学报）。

- **dtx/docstrip 提取后的 cls/def 仍有安装器头部（高频）**：部分大学模板（南大、南开等）使用 dtx 格式。提取后的 `.cls`/`.def` 文件仍保留 docstrip 安装器头部（bare `}`、`\obeyspaces`、`\Msg{...}`、`\endbatchfile`）和未展开的 `\ExplFileDate`/`\ExplFileVersion`/`\ExplFileDescription` 宏，直接编译报 `Too many }'s` 和 `Undefined control sequence`。即使用 `scripts/extract_dtx.py` 提取后也需手动修复三件事：① 注释掉安装器块（`}` 到 `\endbatchfile` 之间所有行）；② 注释掉 stray 描述行如 `{Thesis template...}`；③ 将 `\ExplFileDate` 宏替换为字面值如 `{2026/05/30}{1.5.1}{...}`。详见 `references/nju-template.md`。

- **TeXPage 模板 ID 可能被误传（高频诊断信号）**：当用户（或子Agent调用者）提供的 TeXPage UUID curl 后返回的是**通用模板列表页**（含多个不相关模板如 HNIE Thesis、Monograph Beamer 等），而非单一模板详情页时，说明 UUID 错误或已失效。**诊断信号**：`curl -sL texpage.com/template/<id>` 返回的 HTML 中出现多个 `<h2 title='...'>` 条目。**变体：ID 解析为通用模板列表页**（页面 title 为 "LaTeX Templates - TeXPage"，URL 变为 `/template` 不带 UUID，snapshot 中不含 `detail-info` 元素）。此为同一问题——UUID 已失效或指向不存在的模板，TeXPpage SPA 静默回退到列表页。**修复**：从飞书记录的 `原始来源链接` 字段获取正确 UUID（不要反复尝试错误的 UUID，每个都 200 且无报错但内容不匹配）。已验证案例：IMUST 硕士模板，用户传 `59239f8f-4c12...` → 通用列表页；飞书记录正确 UUID 为 `59239f8f-78ed...`。pku-coe-phd-thesis 模板 UUID `2c853e34-5143-4c1d-af53-82acf1535e70` → 模板列表页（2026-06 确认）。\n\n- **WebBridge evaluate 可提取文件内容，但逐文件提取慢（5-15分钟/模板）**：TeXPage 的 REST API（/api/project/download、/api/project/files 等 8 个端点）全部返回 404 或权限不足。唯一可行方案：TreeWalker 逐文件点击 → evaluate 读取 `window._texpage_editor.state.doc.toString()`（CodeMirror 6 完整文档，不受虚拟视口限制）→ 保存 → 下一文件。详见 `references/texpage-extraction-techniques.md`。模板 ID 必须精确匹配飞书表格中的 URL（错误 ID 静默重定向不报错）。

- **`_texpage_editor.state.doc.toString()` 是获取完整源码的唯一可靠方法**（2026-06 验证）：`.cm-line` 或 `.cm-content` 只返回可见视口内容（CodeMirror 6 虚拟滚动），`_texpage_editor` 是 TeXPage 全局变量，返回完整文档。文件树切换：`document.querySelectorAll(".tree-node")` 中找匹配 `textContent.trim()` 的文件名 → `.click()` → 等待 2s → 读取 `_texpage_editor.state.doc.toString()`。二进制文件（PDF/PNG/JPG）无法通过此方法提取，需占位替代或注释相关 `\includegraphics` 行。

- **v1.0/v1.1 变体模板可跳过浏览器提取（高频捷径）**：当 TeXPage 上同一模板存在多版本（如 韶关学院 v1.0 和 v1.1），且其中一版已有 GitHub 源，直接复制 GitHub 源到另一版的占位仓库，适配编译即可。版本间差异通常极小（class 名称、字体声明微调），无需逐文件从 TeXPage 提取。识别方法：同作者 + 同学校 + 版本号不同。

- **通用 Beamer 提案模板基座（高频捷径）**：当 TeXPage-only 模板是 Beamer 类型的开题报告/答辩幻灯片模板时，检查 `iftaken/thesis-proposal-template`（andy123t/Thesis-Slides，Madrid+rose 主题）。如果 TeXPage 模板与此基座结构一致（Beamer + ctex 默认字体 + thebibliography），直接从基座复制 → 仅修改 header/institute/title page 文字即可上线，**零字体依赖、编译即通过**。适用场景：任何大学的开题报告/答辩 Beamer 模板（如 IMUST、HZAU 等）。检测方法：`gh repo view iftaken/thesis-proposal-template` 确认可用。适配仅需改 5 处：`\header{}`、`\institute{}`、标题页字段标签、章节内容标题、日期。完整案例见 `references/imust-proposal-template.md`。

- **无浏览器可用时的方式 B \"占位先行\"策略**：当 `computer_use` / `cua-driver` 未安装且无 `selenium`/`playwright` 时，无法从 TeXPage 提取源文件。此时走占位先行流程，不阻塞后续模板处理：\n  1. 创建 repo + 标准结构（AGENTS.md、.gitignore、init.sh、references.bib）\n  2. 编写最小占位 `main.tex`（`\\documentclass{ctexart}`，说明待从 TeXPage 提取）\n  3. Docker 编译生成占位 `main.pdf`（验证结构正确）\n  4. Commit + push，commit message 标注\"占位结构初始化\"\n  5. 标记模板为\"源文件待提取\"状态\n  6. 后续在浏览器可用环境中通过 \"Open as Template\" 提取完整源文件覆盖占位\n  - **占位覆盖 push 冲突（高频）**：当从占位升级为正式 init 时，`gh repo clone` 可能因网络超时失败。回退方案：`git init && git remote add origin && git push --force`（远程已有占位 commit 时直接用 force push 覆盖）。不要 git pull rebase 解决冲突——占位文件全部被正式版取代，merge 毫无意义。
  不要无限循环尝试 TeXPage API（全部返回 code:1003 \"Not logged in\"），不要尝试 `git.texpage.com`（需用户名密码认证），不要尝试 TeXPage OSS URL（NoSuchKey / AccessDenied）。
- **占位 init.sh 的 set -u 空数组陷阱**：占位模式的 init.sh 使用 `FONT_FILES=()`（空数组）。若脚本有 `set -euo pipefail`（含 -u），则 `for f in "${FONT_FILES[@]}"` 触发 `unbound variable`。修复：在 for 前检查 `${#FONT_FILES[@]} -eq 0`，为 0 则直接 exit 0。init.sh 模板不受影响（用 `set -e` 无 -u）。
- **tectonic TeX Live 版本 ≈2023，不支持 2024+ 语法（高频）**：部分新模板（如 南开 v2026.5）使用了 LaTeX2e 2024/11+ 和 expl3 `:e`/`:en` 变体。tectonic bundle 基于 TeX Live 2023，不兼容。**诊断方法**：编译报 `NeedsTeXFormat[2024/11/01]`、`Undefined control sequence: \\str_case:en`、`\\ProcessKeyOptions` 未定义时即为此类问题。

- **Beamer 模板常见适配陷阱**：
  - **TeXPage 文件树中的 "Frame" 节点是文档大纲而非文件**：Beamer 模板在 TeXPage 编辑器中仅显示 `main.tex` 一个实际文件，文件树下的 "Frame" 节点是 beamer frame 导航大纲（类似目录结构），不可点击打开也没新内容。直接 evaluate 获取 main.tex 即可，无需展开 Frame 节点。
  - **单文件 Beamer 模板零字体依赖**：`\usefonttheme{serif}` + T1 fontenc 使用标准 LaTeX 字体，init.sh FONT_FILES=() 空数组。详见 `references/texpage-platform.md`。
  - `auto-pst-pdf` + `pstricks`：THU Beamer 派生模板常含 PSTricks 演示帧。tectonic bundle 不含 pstricks.sty，且 auto-pst-pdf 需 shell-escape。**修复**：移除两个包 + 删除 PSTricks 帧（或转为 TikZ）。详见 `references/cqu-template.md`。
  - `fontspec` 显式加载冲突：ctex 在 XeTeX 下自动加载 fontspec，Beamer 模板中显式 `\\usepackage{fontspec}` 应在 ctex 之前移除（ctex 会处理）。
  - **Beamer 导航字体 `nullfont` Missing character 警告**：安全，来自 beamer navigation symbols。
  - **`\\usepackage[T1]{fontenc}` 在 Beamer + ctex 中多余**：ctex（XeLaTeX 模式）自动通过 fontspec 管理字体编码，`\\usepackage[T1]{fontenc}` 在 XeTeX 下无效且可能干扰。**修复**：直接注释掉该行。此模式在从 pdflatex 迁移到 XeTeX 的 Beamer 模板中高频出现。
  - LXGW WenKai（霞鹜文楷）字体替换：部分 Beamer 模板使用此字体做导航栏字体（`\\setCJKsansfont{LXGWWenKai-Medium}`），可替换为 tectonic bundle 内置的 `FandolKai-Regular.otf`，`\\setCJKsansfont` 行直接移除（ctex 管理 CJK sans 字体）。
  - `\NeedsTeXFormat[2024/11/01]` → 降为 `[2022/06/01]`
   - `\ProcessKeyOptions [ ... ]` → `\ProcessKeysOptions { ... }`（需加 `\RequirePackage{l3keys2e}`）。⚠️ 若模板同时使用了 `\DeclareKeys` 和 `\SetKeys`（同样来自 l3keys2e 2022-06-01），tectonic 的旧版 l3keys2e 不含这三个命令中的任何一个，必须用 expl3 原生替代：`\DeclareKeys` → `\keys_define:nn`、`\SetKeys` → `\keys_set:nn`、`\ProcessKeyOptions` → 手动 `\@classoptionslist` 处理。详见 `references/tectonic-expl3-compatibility.md`「`\DeclareKeys` / `\SetKeys`」章节。
  - `\str_case:enF` → `\exp_args:Ne \str_case:nnF`（`:e`/`:en` 变体全部展开为 `:Ne` + `:nn`）
  - `\tl_if_empty:eTF` → `\exp_args:Ne \tl_if_empty:nTF`
  - `\cs_generate_variant:Nn ... { e }` → 直接移除（e 变体生成不可用）
  - `\subcaptionsetup` → `\captionsetup[subfigure]`（旧版 subcaption 无此命令）
  - **`\end{sidepic}` 误写为 `\end{frame}`（Sapienza/SINTEF 派生 Beamer 高频）**：`sidepic` 环境在主题 .sty 中定义为 `\newenvironment{sidepic}[2]{...\begin{frame}{#2}...}{...\end{frame}...}`，内部包裹了一个 frame。关闭时必须用 `\end{sidepic}`，写成 `\end{frame}` 会触发 beamer 内部错误 `\begin{beamer@framepauses} ended by \end{beamer@frameslide}`。**诊断**：编译报此错误且行号指向 `\end{frame}` 位于 sidepic 内容之后。**修复**：`\end{frame}` → `\end{sidepic}`。此模式也适用于同主题的 `chapter` 环境（同样内部包裹 frame）。
- **dtx-based 模板需额外提取**：部分模板（如 nju-lug/NJUThesis）源码为 `.dtx` 格式（docstrip），需先用 Python 脚本提取 `.cls`/`.def` 文件，或从 GitHub Releases 下载预编译的 `.cls`。`l3build unpack` 可在有 TeX Live 的环境下自动提取。
- **Docker 平台不匹配**：macOS ARM64 必须加 `--platform linux/amd64`
- **fontspec API 差异（高频）**：`\\setmainfont`/`\\setsansfont` 参数是字体名不是文件名，不能用 `Path=./font/` + 文件名。只有 `\\setCJKmainfont`/`\\setCJKfamilyfont` 支持 Path= + 文件名。详见 `references/font-availability.md`

- **`Path=./font/` vs `Path=font/` 在 .cls 文件中行为不同**：在 .cls 文件的 preamble 上下文中，`\\setCJKfamilyfont{xxx}[Path=./font/]{file.ttf}` 报 `Missing \\begin{document}` 错误，但 `Path=font/`（去掉 `./` 前缀）正常。根因：.cls 被加载时当前工作目录语义与文档 body 不同，`./` 解析失败。**修复**：在 .cls 中使用 `Path=font/` 而非 `Path=./font/`。

- **`\\IfFontExistsTF` 在 .cls preamble 中不可用**：`\\IfFontExistsTF`（fontspec 命令）在 .cls 文件的 preamble 中调用会触发 `Missing \\begin{document}` 错误。即使在 xeCJK/fontspec 已加载之后也如此。**修复**：避免在 .cls 中使用 `\\IfFontExistsTF` 做条件判断；改用 `\\IfFileExists{font/file.ttf}` 检查文件是否存在，或在 .tex 主文件中处理条件逻辑。

- **占位 main.tex 中 `\\url{}` 需显式加载 `hyperref`**：`ctexart` 文档类不自动加载 `hyperref`/`url` 宏包。占位文档中如果用 `\\url{https://...}` 链接到 TeXPage 模板页，必须在 preamble 加 `\\usepackage{hyperref}`，否则编译报 `Undefined control sequence`。
- **占位 main.tex 中符号命令需 `amssymb` + math mode**：`ctexart` 不自动加载 `amssymb`。占位文档中如果用 `\square`、`\checkmark`、`\Box` 等 AMS 符号，需：① 加载 `\usepackage{amssymb}`（否则报 `Undefined control sequence`）；② 使用 `$\square$`/`$\checkmark$` 而非裸 `\square`/`\checkmark`（这些命令是 math-mode 宏，在文本模式下报 `Missing $ inserted`）。

- **fontset=none 后需手动定义 `\\songti`/`\\heiti`/`\\kaishu`/`\\fangsong`**：当使用 `\\PassOptionsToClass{fontset=none}{ctexrep}` 或 `fontset=none` 选项时，ctex 不自动注册 CJK 家族切换命令。在设置完 `\\setCJKfamilyfont{zhsong}...` 后，必须添加：
```latex
\\NewDocumentCommand\\songti{}{\\CJKfamily{zhsong}}
\\NewDocumentCommand\\heiti{}{\\CJKfamily{zhhei}}
\\NewDocumentCommand\\kaishu{}{\\CJKfamily{zhkai}}
\\NewDocumentCommand\\fangsong{}{\\CJKfamily{zhfs}}
```
否则模板中任何使用 `\\songti`/`\\heiti` 的地方都会报 `Undefined control sequence`。
- **字体目录命名不统一**：有的模板用 `font/`，有的用 `fonts/`（加 s）。init.sh 的 `FONT_DIR` 和 .gitignore 的排除规则必须匹配模板实际目录名。部分模板（如 GXU thesis）还使用中文字体目录名 `字体/`，init.sh 和 .gitignore 需同步用中文
- **模板目录名可能是中文**：部分 CTeX 模板使用中文目录名（如 `论文内容/`、`参考文献/`、`图/`、`签名/`）。`.gitignore` 中的排除规则和 `init.sh` 的目标目录必须匹配这些实际名称，不能用英文假定替代
- **上游仓库可能不完整**：fork 仓库通常只含 tex/cls 源码，缺资源文件和用户配置文件。必须先编译一次，根据错误信息补全三类依赖
- **`.gitignore` 非开箱即用**：`*.pdf` 会误杀校徽/logo 等模板资源，每个模板需单独审查并加例外
- **TexPage ↔ GitHub 内容不同**：TeXPage 上的模板项目可能包含额外文件（如 gbt7714.sty），GitHub 源仓库不一定有
- **`\\include` 导致 BibTeX/biber chapter aux 错误（高频）**：`\\include{chapters/xxx}` 会为每个章节生成独立 .aux 文件。如果章节有 `\\cite` 但没有 `\\bibliography`/`\\bibdata`（BibTeX）或 `\\addbibresource` 在 main.tex 中（biblatex/biber），BibTeX/biber 在该 aux 上失败。**修复**：将 main.tex 中的 `\\include` 改为 `\\input`（`\\input` 不生成独立 aux）。biblatex 模板额外需将 `\\addbibresource{old/path.bib}` 改为 `\\addbibresource{references.bib}`。
- **缓存目录需预创建**：`mkdir -p ~/.cache/paper-tectonic` 先建好
- **tectonic re-run**：交叉引用导致自动 re-run，设置 timeout ≥ 300s
- **gbt7714 .bst 获取**：tectonic 自动下载 `.sty` 但不下载 `.bst`。`.bst` 文件在 tectonic 缓存中：`~/.cache/paper-tectonic/bundles/data/<hash>/gbt7714-numerical.bst`，直接 `cp` 到项目根目录即可。不要从 CTAN curl（会被重定向到 HTML）
- **商业字体替换**：从 TeXPage ZIP 下载的模板可能包含商业 OTF/TTF 字体（如 HelveticaNeueLTPro、ProGB18030）。这些字体不在 COS 字体库中，需替换为 Docker 系统字体。替换映射：Helvetica → Liberation Sans 或 DejaVu Sans，ProGB18030 → SimHei 或 Noto Sans CJK。在 `\setmainfont`/`\setCJKmainfont` 声明中直接改为系统字体名
- **`\\\\fancyheadwidth` 未定义（fancyhdr v4+ 命令）**：tectonic 的 TeX Live bundle 不支持 fancyhdr 4.0+ 的 `\\\\fancyheadwidth`。**修复**：注释掉对应行，影响极小

- **`glossaries-extra` 参数栈溢出（tectonic TL2023，高频）**：`\\\\usepackage[automake,...]{glossaries-extra}` 在 TL2023 触发 `TeX capacity exceeded [parameter stack size=10000]`。**修复**：移除 glossaries-extra，仅保留基础 `glossaries` 包。`automake`、`acronym`、`postdot` 等功能非必需

- **`\\\\chinese` 需要计数器名而非展开值（高频陷阱）**：用 ctex 的 `\\chinese` 替代 CJKnumb 的 `\\CJKnumber` 时，参数必须是计数器名（如 `\\chinese{chapter}`），**不能**用展开值（如 `\\chinese{\\thechapter}`）。展开值会导致 `zhnumber Error: '\\thechapter' is not a LaTeX counter` 和 `Use of \\??? doesn't match its definition`。**修复**：`\\renewcommand{\\chaptername}{\\prechaptername\\chinese{chapter}\\postchaptername}`。若 BST 文件或其他代码仍引用 `\\CJKnumber`，在 main.tex preamble 添加兼容 shim：`\\providecommand{\\CJKnumber}[1]{\\chinese{#1}}`（shim 可接受展开值，因为它在 document body 而非 moving argument 中执行）。\n\n- **`newtxtext`/`newtxmath`/`lmodern`/`T1 fontenc` 与 XeTeX 不兼容（高频）**：老模板常同时加载 pdflatex 字体包（`\\usepackage{newtxtext}`、`\\usepackage{lmodern}`、`\\usepackage[T1]{fontenc}`）和 xeCJK/ctexbook。这些包在 XeTeX 模式下无效或冲突（fontspec 管理字体）。**修复**：全部移除。ctexbook 在 XeTeX 下自动使用 fontspec + Latin Modern 或 Fandol CJK 字体。**诊断信号**：编译报 `No file OMLTeXGyreTermesX(0).fd` → `Font shape 'OML/TeXGyreTermesX(0)/m/n' undefined` → `Missing endcsname inserted` 三条链式错误 — 根因是 `newtxmath` 的 OML 编码字体定义在 XeTeX 下不可用。\n\n- **`lastpage` + `footmisc perpage` → `\\c@abspage` 双重定义（TL2023 高频）**：`\\RequirePackage{lastpage}` 和 `footmisc` 的 `perpage` 选项都会触发 `\\newcounter{abspage}`，而 hyperref 在 TL2023 中通过 zref-abspage 也定义同一计数器。三个入口任一命中即报 `Command \\c@abspage already defined`。**修复**：① 若 fancyhdr 未引用 `\\lastpage`，直接移除 `lastpage` 包；② `footmisc` 移除 `perpage` 选项（仅保留 `bottom`）。**诊断**：编译报 `zref-abspage.sty:60: ... \\c@abspage already defined`，日志中可见 `perpage.sty` 或 `\\Hy@abspage` 提前定义。\n\n- **bicaption `\\captionsetup[bi-first]{bi-first}` 顺序依赖**：`\\captionsetup[bi-first]{bi-first}` 必须在 `\\DeclareCaptionOption{bi-first}{...}` **之后**调用，否则 `bi-first` family 在 caption 系统中未注册 → `Package caption Error: 'bi-first' undefined in families 'caption'`。**修复**：将 `\\DeclareCaptionOption` 块移到 `\\captionsetup[bi-first]`/`\\captionsetup[bi-second]` 之前。\n\n- **`\\\\CJKtilde` 在 XeTeX 模式下未定义（ctex 模板）**：原 pdflatex 模板中的 `\\\\CJKtilde`（波浪号 CJK 间距处理）在 XeTeX 模式下无效。**修复**：直接删除该行，XeTeX 原生处理 Unicode 间距

- **`\\\\DisableLigatures` 仅 pdfTeX 支持（microtype）**：`microtype` 的 `\\\\DisableLigatures{encoding = *, family = *}` 在 XeTeX 下报错。**修复**：注释掉，改用 fontspec 的 `Ligatures=NoCommon` 特性，或直接移除（连字符控制为次要排版优化）

- **`ipaex-type1` 日语字体包可移除**：部分中文模板附带 `\\\\usepackage{ipaex-type1}`（日语字体），XeTeX 下无需且可能冲突。**修复**：直接移除
- **`\\RequirePackage[twoside,...]{fancyhdr}` 报 Unknown option `twoside`（高频）**：tectonic 的 fancyhdr bundle 不识别 `twoside` 选项。**修复**：从选项列表中移除 `twoside`，保留其余选项（如 `nocheck`）。`\\RequirePackage[twoside, nocheck]{fancyhdr}` → `\\RequirePackage[nocheck]{fancyhdr}`
- **fontspec option clash：ctex 先加载 fontspec，模板再次 `\\RequirePackage[quiet]{fontspec}` 冲突（高频）**：ctex（XeLaTeX 模式）自动加载 fontspec（无选项），模板中后续的 `\\RequirePackage[quiet]{fontspec}` 触发 "Option clash for package fontspec"。**修复**：在 `\\RequirePackage{ctex}` 之前添加 `\\PassOptionsToPackage{quiet}{fontspec}`，让 fontspec 首次加载时带上 quiet 选项

- **xcolor option clash：tikz 加载 xcolor（无选项）→ 后续 `\\RequirePackage[usenames,dvipsnames,table]{xcolor}` 冲突（高频）**：`.cls` 中 `\\usepackage{tikz}`（tikz 内部加载 xcolor 无选项）在 artratex.sty 的 `\\RequirePackage[usenames,dvipsnames,table]{xcolor}` 之前执行，触发 "Option clash for package xcolor"。**修复二选一**：① **推荐**：在 tikz 之前用 `\\PassOptionsToPackage{dvipsnames}{xcolor}` 传递选项（tikz 内部首次加载 xcolor 时自动带上选项，无需显式 `\\RequirePackage{xcolor}`）；② 回退：在 .cls 中 `\\usepackage{tikz}` **之前** 显式加载 `\\usepackage[dvipsnames]{xcolor}`，让 tikz 后续看到已加载的 xcolor 而跳过。**注意**：一旦 xcolor 已被 tikz 加载，`\\PassOptionsToPackage` 就无效了——必须在 tikz 之前调用。本会话案例：ECNU Beamer cls 用方案①通过编译。
- **`circledtext.sty` 未找到（tectonic 不包含）**：`circledtext` 是 TeX Live 标准发行版的宏包，但 tectonic bundle 不包含。**诊断**：编译报 `File 'circledtext.sty' not found`。**修复**：检查 `.cls` 中 `circledtext` 的实际用途（通常用于带圈数字或带圈文字），方案① 若仅用 `\\Circled{1}` 等简单功能，用 `\\textcircled{1}` 或 pifont 宏包的 `\\ding{172}` 替代；方案② 若功能复杂，需从 CTAN 下载 `circledtext.sty` 放入项目目录（但需同步下载其依赖如 `pgfkeys.sty` 等）

- **`fixdif.sty` 未找到（tectonic TL2023 不包含）**：`fixdif` 包提供 `\\d` 命令（直立微分算子 d，用于 `\\int f(x) \\d x`）。tectonic TL2023 bundle 不含此包。**诊断**：编译报 `File 'fixdif.sty' not found`。**修复**：一行替换 —— `\\providecommand{\\d}{\\mathop{}\\!\\mathrm{d}}`。无需 CTAN 下载，定义完全等价。已确认：WHU thesis 模板使用此方案。
- **FangSong（仿宋）不在 Docker 镜像中（高频）**：Docker 系统字体含 SimSun/SimHei 但不含 FangSong（及 KaiTi）。部分模板（如 GXU thesis）使用 `\\setCJKfamilyfont{zhfs}{FangSong}` 会报 font not found。**修复**：添加文件优先回退模式（先检查 `字体/simfang.ttf`，再 fallback 到系统 FangSong）。详见 `references/gxu-template.md`。

- **`\\newCJKfontfamily{\\cmd}{BundleFont}` 在 Docker 中失败 — fontspec 找不到 TeX Live bundle 字体（高频）**：`\\newCJKfontfamily` 和 `\\setCJKfamilyfont`（不带 `Path=`）走 **fontspec 系统字体搜索路径**，不搜索 TeX Live / tectonic bundle 内部路径。因此 `\\newCJKfontfamily{\\kt}{FandolKai}` 或 `\\setCJKfamilyfont{zhkai}{FandolKai}` 会报 `fontspec Error: The font "FandolKai" cannot be found` —— 即使 FandolKai 在 tectonic bundle 中完全可用、ctex 的 `\\kaishu` 命令工作正常。**诊断信号**：编译报 `Package fontspec Error: The font "Fandol..." cannot be found`，但同一模板的 `\\songti`/`\\heiti`（ctex 内建）正常。**根因**：ctex 走 TeX Live font map（kpathsea），fontspec 走系统 fontconfig/fc-match。**修复**：不要尝试改字体名为 FandolXxx —— 将自定义字体命令重定向到 ctex 等价命令：`\\newcommand{\\kt}{\\heiti}`（楷体→黑体）或 `\\let\\kt\\kaishu`（楷体→ctex 楷体）。若必须保持楷体，使用 `\\setCJKfamilyfont{zhkai}[Path=font/]{simkai.ttf}` + init.sh 下载 simkai.ttf。本会话案例：`sduthesis-front-cover.def` 中 `\\newCJKfontfamily{\\kt}[AutoFakeBold]{FandolKai}` → `\\newcommand{\\kt}{\\heiti}`。\n  **子变体：带扩展名的文件名参数（如 `{simkai.ttf}`，无 `Path=`）**：当 `\\setCJKfamilyfont` 的参数带扩展名（如 `.ttf`）且无 `Path=` 时，fontspec 将参数解释为**当前工作目录下的文件名**（而非系统字体名），在 CWD 查找该文件。Docker 中 `/app/simkai.ttf` 不存在 → 同样报 `font not found`。此模式与上述 FandolKai 模式不同（后者走系统字体搜索），但**修复方法完全一致**：重定向到 ctex 内建命令。本会话案例：GDUT thesis cls 中 `\\setCJKfamilyfont{kai}[AutoFakeBold]{simkai.ttf}` → `\\newcommand*{\\kai}{\\kaishu}`。注意同 cls 中 `\\setCJKfamilyfont{song}[AutoFakeBold]{SimSun}` 走字体名搜索且 SimSun 是 Docker 系统字体，**无需修改**。
- **fontset=ubuntu → cjk-font=noto 路径仍依赖 FandolKai/FandolFang（thuthesis 派生模板高频）**：当模板显式设置 `fontset=ubuntu` 以使用 Docker 中的 Noto CJK 字体时，thuthesis 派生模板的 noto CJK handler 仍然使用 `FandolKai`/`FandolFang`（Extension=.otf）声明 zhkai/zhfs，而 Fandol 字体不在 Docker 中。**诊断**：编译报 `FandolKai-Regular.otf cannot be found` 或类似。**修复**：在 cls 的 `wzu@set@cjk@font@noto`（或等价函数）中将 `\\setCJKfamilyfont{zhfs}{FandolFang}[Extension=.otf,...]` 改为 `\\setCJKfamilyfont{zhfs}{simfang}[Path=./font/,Extension=.ttf]`，zhkai 同理改为 simkai。示例见 `references/wzu-template.md`。
- **thuthesis 派生模板在 Docker 中 auto-detect 到 windows 分支的陷阱**：Docker 有 SimSun，所以 `\\IfFontExistsTF{SimSun}` 为 true → fontset 自动设为 windows → CJK windows handler 直接声明 KaiTi/FangSong 失败。即使你显式写 `fontset=ubuntu`，若 cls 的 auto-detect 在 `\\ProcessKeyvalOptions` 之前运行（取决于代码组织），可能仍被覆盖。**修复**：显式写 `fontset=ubuntu,font=times`，并确认 auto-detect 在选项处理后执行（用 `\\wzu@debug{Detected fontset: \\wzu@fontset}` 查看编译日志确认）。
  **SimSun 分支内的 KaiTi/FangSong 独立检测（高频子模式）**：模板的 Windows 字体分支以 `\\IfFontExistsTF{SimSun}` 为入口，进入后直接设置全部四种字体（song/hei/kai/fang）。Docker 有 SimSun 但无 KaiTi/FangSong → 进入 Windows 分支后后两者失败。**修复**：在 Windows 分支内为 zhkai/zhfs 添加独立的 `\\IfFontExistsTF{KaiTi}` 和 `\\IfFontExistsTF{FangSong}` 检测，缺失时回退到 FandolKai/FandolFang（Extension=.otf, UprightFont=*-Regular）。详见 `references/neu-thesis-proposal.md`。
- **refs.bib 文件名不兼容**：心河Paper 系统要求参考文献文件必须命名为 `references.bib`。如果模板使用 `refs.bib`、`ref.bib` 等别名，需重命名文件并更新 `\\bibliography{refs}` → `\\bibliography{references}`。若参考文献样式文件使用非标准扩展名（如 `.buk`），需重命名为 `.bst`（`ref.buk` → `ref.bst`，`\\bibliographystyle{ref}`）

- **`thebibliography` + natbib 混用模式（纯英文期刊常见）**：部分英文期刊模板在 .cls 中加载 natbib，但 main.tex 使用 `\begin{thebibliography}` 手动管理参考文献（非 BibTeX）。此模式在 tectonic 中正常工作，**但心河Paper 系统仍要求 `references.bib` 文件存在**——创建占位 `references.bib` 即可，不需要将 `thebibliography` 转换为 BibTeX。

- **`subfigure` 废弃宏包可安全移除**：`subfigure` 是 LaTeX 2.09 时代的宏包（已被 `subfig`/`subcaption` 取代）。若 .cls 中 `\RequirePackage{subfigure}` 但模板自身未使用任何 subfigure 环境，可直接移除。不影响编译和输出。

- **`.cls` 生成的 `.dat` 编译产物需 gitignore（如 `lastpage.dat`）**：部分期刊 .cls 通过 `\openout`/`\write` 在编译时生成 `.dat` 文件（如 `lastpage.dat`）用于跨次编译传递页码信息。这些是编译产物，必须在 `.gitignore` 中显式排除（当前 `templates/gitignore.template` 未覆盖 `*.dat`）。编译后检查 `git status`——若有 `.dat` 文件出现，立即追加到 `.gitignore`。
- **`\usepackage{minted}` 需 shell-escape**：`minted` 依赖 Pygments 外部调用，tectonic 不支持 `-shell-escape` 参数。**修复**：移除 `minted`，仅保留 `listings` 包作为代码高亮方案。影响中等——`listings` 功能覆盖大部分代码排版需求
- **`unicode-math` + `\\setmathfont` 可移除**：对于非重度数学模板（如本科毕业论文、数模竞赛），`unicode-math` 宏包和 `\\setmathfont{TeX Gyre Termes Math}` 并非必需。tectonic 的 TeX Live 2023 bundle 中 TeX Gyre Termes 字体在缓存内（非系统字体），unicode-math 可能找不到。**修复**：直接移除 `\\usepackage{unicode-math}` 和 `\\setmathfont{...}`，默认 math font 已足够

- **XITS 字体在 tectonic bundle 中可用 — `\\IfFontExistsTF{XITS-Regular.otf}` 会触发 unicode-math 分支（高频陷阱）**：tectonic 对缺失的宏包/字体会自动下载。XITS 系列字体（XITS-Regular.otf 等）和 XITSMath 数学字体在 tectonic 的 TL2023 bundle 中**存在且会自动下载**。因此 `\\IfFontExistsTF{XITS-Regular.otf}` 返回 TRUE → 加载 `unicode-math` + 设置 XITS 为 main/sans/mono 字体 + 设置 XITSMath 为数学字体 → **覆盖 .cls 中已设置的 `\\setmainfont{Times New Roman}` 等**。**诊断**：编译日志出现 `note: downloading XITS-Regular.otf` 等即确认。**修复二选一**：① 如 XITS 对数学排版无实质影响，保持即可（只是字体外观变化）；② 如必须保持 cls 字体，注释掉 artratex.sty 中 XITS 分支的 `\\setmainfont`/`\\setsansfont`/`\\setmonofont` 调用，保留 `unicode-math` 的数学字体设置
- **`\\setmathfont{XITS Math}` 在 Docker 中失败 — fontspec 找不到字体名（高频子模式）**：即使 XITSMath-Regular.otf 在 tectonic bundle 中，`\\setmathfont{XITS Math}`（通过字体名查找）走 fontspec 系统 fontconfig 路径，Docker 中 XITS Math 未注册为系统字体 → `Package fontspec Error: The font "XITS Math" cannot be found`。**修复**：改为 filename-based 加载：`\\setmathfont{XITSMath-Regular.otf}[StylisticSet=8, BoldFont=XITSMath-Bold.otf]`。`\\setmathfont`（unicode-math）在给文件名时走 kpathsea 搜索，能命中 tectonic bundle。**诊断**：编译报 `The font "XITS Math" cannot be found` 且行号为 `\\setmathfont{XITS Math}`。本会话案例：NEUCLHSBachelorThesis.cls:69
- **示例数据文件使用 unicode-math 命令 → `math-font=none` 反而编译失败（高频）**：当模板示例数据文件（chapters/*.tex、data/*.tex）中使用 `\\increment`、`\\symup`、`\\symbf`、`\\uppi`、`\\symbfsf` 等 unicode-math 命令时，设置 `math-font=none` 不加载 unicode-math → 全部 Undefined control sequence。**诊断**：grep `\\\\symup\\\\|\\\\symbf\\\\|\\\\increment\\\\|\\\\uppi\\\\|\\\\symbfsf` data/*.tex。**修复二选一**：① 若仅个别出现 → 替换为标准 LaTeX（`\\mathbf{}`、`\\Delta` 等）；② 若大量出现 → 使用 `math-font=stix`（STIX Two Math 在 tectonic bundle 中可用，不依赖系统字体）
- **注释含 tab 的行前必须先替换 tab（高频）**：`sed 's/\\t/    /g'` 再 `sed 's/^/\%/'`。tab 前导 `%` → TeX 将 `\t` 解析为 `\csname` → `Missing \endcsname inserted`。此模式在以注释方式移除 `\includegraphics` 引用时极高频触发\n- **源文件中 tab 字符（`\\t`）在括号内导致 \"Missing endcsname inserted\"（诊断陷阱）**：部分模板源文件（如从 TeXPage 导出的 .tex）可能在命令前插入 tab 缩进。当 tab 出现在 `{...}` 分组内（如 `{\\t\\includegraphics{...}}`），TeX 将 tab 后的序列解析为 `\\csname` 调用导致 \"Missing endcsname inserted\" 错误——但错误**不在**行号指向的位置，而是在 tab 字符处。**诊断信号**：编译报 `Missing endcsname inserted` 但行号行内容看似正常，且行内有花括号嵌套。**修复**：用 `cat -A` 检查 $TAB$ 字符，直接删除 tab。`sed 's/\\t//g'` 或手工删。本会话案例：`tex/chapter2.tex:222` 的 `{\\t\\includegraphics}` — tab 前导导致跨行解析错误，与 `newtxmath` 的 OML 字体错误链交织在一起，增加了诊断难度

- **tectonic 缓存不支持并发写入（高频诊断陷阱）**：多个 Docker 容器同时编译且挂载同一宿主机 `~/.cache/paper-tectonic` 时，tectonic bundle 缓存文件被并发读写，导致随机 `Undefined control sequence` 错误——**错误文件和行号每次不同**（已验证：nwputhesis 连续 5 次编译，3 次报错在 options.def:187、options.def:188、metadata.def:271，2 次通过）。**诊断信号**：单独跑通过、并发跑随机失败，错误位置每次漂移。**修复**：① 编译时不要并行跑多个 Docker tectonic 容器；② 子 Agent 并行批处理时，每个 Agent 编译在独立终端串行执行，或使用独立缓存目录。

- **EPS 图片不支持（高频）**：tectonic 不支持 EPS（PostScript）图片格式，编译报 `Unable to load picture`。**修复**：`gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -sOutputFile=image.pdf image.eps` 转换为 PDF
- **`\\providecommand` vs `\\newcommand` for cls 末尾 shim 命令（高频）**：在 cls 末尾添加原模板缺失的自定义命令 shim（如 `\\auctex`、`\\LKeyTab`、`\\Ctrl` 等教程命令）时，必须用 `\\providecommand` 而非 `\\newcommand`。cls 中加载的宏包（如 marvosym、wasysym、pifont）可能已定义了同名命令。**高频冲突**：`\\Frowny` 已被 marvosym 定义，`\\Smiley` 已被 wasysym 定义。`\\newcommand` 会报 `Command already defined`。**修复**：所有 cls 末尾的自定义命令 shim 一律用 `\\providecommand`。

- **`circledtext.sty` 缺失（可修）**：tectonic TL2023 bundle 不含此包。用 TikZ 替代，**注意必须在顶层定义**（不能在 `\\newcommand` 体内，否则 `#1` 被外层参数解析）。方案：`\\usepackage{tikz}\\newcommand{\\circlenum}[1]{\\tikz[baseline=(char.base)]{\\node[shape=circle,draw,inner sep=1pt,font=\\scriptsize] (char) {#1};}}`，然后 `\\providecommand{\\circledtext}[2][]{\\circlenum{#2}}`
- **fancyhdr `twoside` 选项冲突**：tectonic 的 fancyhdr 不支持 `\\RequirePackage[twoside,nocheck]{fancyhdr}`。改为 `\\RequirePackage{fancyhdr}`
- **fontspec 重复加载冲突（高频）**：ctex/ctexbook 内部自动加载 fontspec，cls 中 `\\RequirePackage[quiet]{fontspec}` 与之冲突，报 `Option clash`。删除 cls 中的 fontspec 加载行（注释 `% fontspec already loaded by ctex`）
- **GBK 编码（可修）**：部分中文模板使用 GBK 编码，tectonic 报 `Text line contains an invalid character`。`iconv -f GBK -t UTF-8 main.tex` 对 main.tex 和 cls 都要转
- **`\\IfFontExistsTF` 在 .cls preamble 中使用时机**：此命令需要 fontspec 已加载。若 cls 在 `\\LoadClass{ctexbook}`（会自动加载 fontspec）**之后**调用 `\\IfFontExistsTF`，则可用（如 ustcthesis 的 fontset auto-detect 和 XITS 检测均正常工作）。仅在 fontspec 尚未加载时不可用。
- **`Path=./font/` vs `Path=font/`**：`./font/` 可能报 `Missing \\begin{document}`。统一用 `Path=font/`：编译日志中 `algorithm2e.sty:284: Invalid UTF-8 byte` 和 `algorithmic.sty:11: Invalid UTF-8 byte` 是宏包内部注释中的遗留编码问题（非 ASCII 字符），**不影响编译和输出**。无需修复，视为安全警告
- **ctexfont 模板无需字体下载**：使用 ctex 默认字体方案（chinesefont=ctexfont 或不显式声明 chinesefont）的模板（如 ElegantLaTeX 系列），ctex 自动检测 Docker 中的 SimSun/SimHei 系统字体。此类模板 init.sh 只需创建 font/ 目录，无需从 COS 下载任何字体文件。`\\setCJKmainfont` 等声明由 ctex 内部管理，模板 cls 中不出现显式字体路径

- **ctexbook + Fandol auto-detect = all four CJK fonts available (good news)**：在 Linux (Docker) 上，ctexbook 默认 auto-detect 到 **fandol** fontset（不是 windows，即使 Docker 中有 SimSun/SimHei）。Fandol 是 TeX Live 自带的免费 CJK 字体家族，在 tectonic bundle 中直接可用，提供全部四种字体：FandolSong（宋）、FandolHei（黑）、FandolKai（楷）、FandolFang（仿）。这意味着 ctexbook 模板中的 `\\\\songti`、`\\\\heiti`、`\\\\kaishu`、`\\\\fangsong` 在 Docker 中都能正常工作，**无需下载任何外部字体**。这与 `fontset=none` 后手动配置 Windows 字体（需下载 simfang/simkai）是两条不同的路线。对于编译验证和 PDF 交付，Fandol 路线更简单可靠。

- **老旧 thuthesis 派生模板（2010 年前后，高频模式）**：2010 年左右的 thuthesis 早期派生模板（如 whutthesis）与现代 v7.x 完全不同。典型信号：① 使用 `\\youyuan`、`\\lishu` 等旧 CJK 字体命令（ctexbook+Fandol 不定义）；② 文体示例中夹杂 `\\backslashbox`（slashbox.sty，tectonic 不含）；③ GBK 编码的 `\\begin{CJK*}{GBK}{kai}` 转义；④ `txfonts` 而非 `newtxtext`（txfonts 在 XeTeX+tectonic 下可工作，tectonic 自动下载 tx*.tfm/vf/pfb）；⑤ dtx 生成的 `.cfg` 文件必须一同提取。**修复**：① 在 main.tex 加 `\\providecommand{\\youyuan}{\\kaishu}` 和 `\\providecommand{\\lishu}{\\songti}`；② 移除 slashbox 并对正文中的 `\\backslashbox{x}{y}` 改为纯文本；③ GBK 转义改为 `\\kaishu`；④ 无需移除 txfonts（与 newtxtext 不同，txfonts 在 XeTeX 下不冲突）。详见 `references/whut-thesis.md`。
- **`\\ProcessKeyOptions` 未定义（新版内核命令，高频）**：tectonic 的 TeX Live ≈2023 不含 LaTeX 2022-06-01 新增的 `\\ProcessKeyOptions`。**修复三步走**：① 降低 `\\NeedsTeXFormat` 日期到 `[2022/06/01]`；② 添加 `\\RequirePackage{l3keys2e}`；③ 将 `\\ProcessKeyOptions [ <module> ]` 改为 `\\ProcessKeysOptions { <module> }`（注意多了字母 's'，参数用花括号）。详见 `references/tectonic-expl3-compatibility.md`

- **`\\DeclareKeys` / `\\SetKeys` / `\\ProcessKeyOptions` 三元组（TL2024+ 新版 key-value 接口，nwpu-template 实战）**：部分 2024+ 模板使用 LaTeX 2022-06-01 新增的 key-value 家族（`\\DeclareKeys`、`\\SetKeys`、`\\ProcessKeyOptions`），替代旧的 `\\keys_define:nn`/`\\keys_set:nn`。tectonic TL2023 的 l3keys2e 不含这些命令。**修复**：将 `\\DeclareKeys[...]{<module>}{<keydefs>}` → `\\keys_define:nn { <module> } { <keydefs> }`，`\\SetKeys[...]{<module>}{<vals>}` → `\\keys_set:nn { <module> } { <vals> }`。`\\ProcessKeyOptions[<module>]` 需自建 `\\__xxx_process_class_options:` 函数遍历 `\\@classoptionslist` 调用 `\\keys_set:nn`。详例见 nwputhesis 的 `infra/options.def` 适配。
- **`:en` / `:e` expl3 变体（可修，高频）**：TL2024+ 语法，TL2023 报 `Undefined control sequence`。`\\str_case:enF` → `\\exp_args:Ne \\str_case:nnF`，`\\__xxx:en` → `\\exp_args:Ne \\__xxx:nn`。搜索 `:en` 和 `:e` 批量 patch，每处一行
- **`\\s__clist_stop` xtemplate 泄露（不可修）**：`\\DeclareInstance` 在 TL2023 内核中存在扫描标记泄露 bug，报 `The key '\\s__clist_stop' has no value`。**无法在用户层面修复**，需要升级 Docker 镜像到 TL2024+。遇到此错误直接跳过该模板，标记为"需 TL2024+"

- **不可修复：2024 内核模板系统（高频阻断）**：模板使用 NewTemplateType、DeclareTemplateInterface、DeclareTemplateCode 等 LaTeX 2024-06-01 内核新增的 ltcmd 命令。TL2023 不含，shim 无效（xtemplate 类型注册不匹配）。**处理**：标记「需 TL2024+」，源码可上线。**识别**：grep 这些命令名即可判定。**已知**：sysuthesis（中山大学），详见 references/sysu-template.md 和 references/tectonic-expl3-compatibility.md。
- **`.dtx` 提取残留**：从 .dtx 手工提取的 cls/def 文件可能残留 docstrip installer 代码（`\\obeyspaces`、`\\Msg`、裸 `}`）。优先使用 repo 的 `source/` 目录预构建版本
- **`\\subcaptionsetup`**：TL2024 命令。改用 `\\captionsetup[subfigure]`
- **`circledtext.sty` 缺失**：TL2023 bundle 不含。改为 TikZ 替代：`\\usepackage{tikz}` + `\\newcommand{\\circlenum}[1]{\\tikz[baseline]{\\node[circle,draw,inner sep=1pt]{#1};}}`。**注意**定义必须在 `\\newcommand` 外部，否则 #1 被外层解析
- **fancyhdr `twoside` 选项**：`\\RequirePackage[twoside,nocheck]{fancyhdr}` → 去掉方括号内容：`\\RequirePackage{fancyhdr}`
- **fontspec 选项冲突**：ctexbook 内部已加载 fontspec，cls 中再 `\\RequirePackage[quiet]{fontspec}` 报 Option clash。修复：注释掉 cls 中的重复加载行
- **GBK 编码**：`iconv -f GBK -t UTF-8` 转换源文件，否则 tectonic 报 `Invalid character`
- **EPS 图片**：tectonic 不支持 → `gs -dEPSCrop -sDEVICE=pdfwrite -sOutputFile=xxx.pdf xxx.eps`
- **hustvisual.sty**：CTAN 仅 .dtx 格式，需 tex 编译提取。暂跳过
- **TL2024 kernel 深坑**：SJTU/中山/华科使用 `\\NewTemplateType` 等内核级新命令，非简单 patch 可修。**600s 子Agent 不够**。推送源码占位，标记"需 TL2024+ Docker"

- **`\setmainfont` 在 `\setCJKmainfont` 之后导致 Latin Modern TU 字体找不到（高频）**：当 cls 中先设置 CJK 字体（`\setCJKmainfont`）后设置英文字体（`\setmainfont`）时，ctex 加载的 fontspec 已将编码改为 TU，而 `\normalsize` 在 `\begin{document}` 时尝试用 Latin Modern 的 TU 编码变体，tectonic bundle 中可能不可用。**修复**：将 `\setmainfont{Times New Roman}` 移至 CJK 字体设置**之前**（在 `\RequirePackage{ctex}` 之后、`\setCJKmainfont` 之前立即设置）。编译错误：`Font TU/lmr/m/n/10 not loadable`

- **`ItalicFont=KaiTi` 在 Docker 中不可用**：Docker 镜像不含 KaiTi（楷体）系统字体。`\setCJKmainfont[ItalicFont=KaiTi]{SimSun}` 会报 `fontspec Error: The font "KaiTi" cannot be found`。**修复**：移除 `ItalicFont` 选项（中文 italic 极少使用，不影响输出）
- **`\usepackage{fontawesome5}` 导致 crash（`free(): invalid pointer`）**：tectonic 的 xdvipdfmx 与 fontawesome5 的 OTF 字体存在兼容性问题，编译中途崩溃。**直接移除 fontawesome5**，页面中的 fontawesome 图标 symbol 会丢失显示，但不影响其余 PDF 内容
- **商业字体替换**：TeXPage 模板可能内嵌商业字体（如 HelveticaNeueLTPro、ProGB18030），这些字体不在 COS 库中且不可用。英文: `{Liberation Sans}` 或 `{DejaVu Sans}`，中文: `{SimHei}` 或 `{Noto Sans CJK SC}`。使用 `python3` 做多行替换，`sed` 处理单行
- **`\\setmonofont{Fira Mono}` / FiraSans / FiraMono**：Fira 字体族（FiraSans, FiraMono）在 tectonic bundle 中**可用**（通过 `Extension=.otf` + kpathsea 文件名查找加载）。⚠️ 仅当模板使用 fontspec **系统字体名**搜索（不带 `Extension=`）时才失败——tectonic bundle 字体不走 fontconfig。**诊断**：编译报 `fontspec Error: The font "Fira Mono" cannot be found` 且无 `Extension=` → 添加 `[Extension=.otf, UprightFont=*-Regular, ...]` 让 fontspec 走 kpathsea。已验证可用: FiraSans-Regular/SemiBold/Italic/SemiBoldItalic.otf, FiraMono-Regular/Medium/Oblique/MediumOblique.otf。上一条 pitfall（替换为 DejaVu Sans Mono）仅适用于通过系统字体名查找的场景。
- **GitHub 源仓库不含 .cls 文件（CTAN/TeX Live 分发包模式，高频）**：部分模板（如 sjtug/SJTUThesis）的 GitHub 仓库仅包含用户文件（main.tex、contents/、figures/），`.cls` 和所有 `.def` 文件**不在源码仓库中**——它们是 CTAN/TeX Live 分发包。**诊断信号**：`find . -name '*.cls'` 只返回 `texmf/` 下的预设 `.def`，无 `.cls`；`git clone` 浅克隆后无完整 texmf 树。**修复**：从 GitHub Release 下载完整 zip（如 `SJTUThesis-full-2.3.1.zip`）→ 提取其中的 `texmf/` 目录 → 全量复制到项目根目录。Release zip 通常包含 50+ 文件：3 个 `.cls`、35 个 `.def`（font/lang/preset/scheme）、10+ VI logo PDF 及 `.gitkeep`。

- **tectonic 不识别 TEXINPUTS 环境变量（高频）**：Docker 中设置 `-e TEXINPUTS="./texmf//:"` 对 tectonic 无效，`sjtuthesis.cls` 在 texmf 子目录下仍报 `File not found`。**修复**：将 cls/def 文件直接复制到项目根目录（与 main.tex 同级），tectonic 从当前工作目录查找。详见 `references/sjtu-template.md`。

- **`\\heiti` 在 `\\makebox[s]` 中展开失败（CCT→ctexart 适配）**：`\\makebox[4.5cm][s]{\\heiti系统科学与数学}` 在 ctexart 中 `\\heiti` 于 spread 模式内部被过早展开，报 `Undefined control sequence`。**修复**：在 `\\heiti` 外再加一层花括号 `\\makebox[4.5cm][s]{{\\heiti 系统科学与数学}}`。

- **`\\refname` 重定义中字体命令在 moving argument 失效（CCT→ctexart 适配）**：`\\renewcommand\\refname{\\zihao{5}\\heiti ... \\quad ...}` 在 `\\begin{thebibliography}` 中作为 section heading 使用，内容进入 moving argument 导致 `\\heiti`/`\\quad` 跨行解析失败，报 `Undefined control sequence \\quad献`。**修复**：将字体相关部分用 `{...}` 整体保护 `\\renewcommand\\refname{{\\zihao{5}\\heiti 参 \\quad 考 \\quad 文 \\quad 献}\\vspace*{4mm}}`。

- **`\\sectionname` 未定义（CCT→ctexart 适配）**：`\\renewcommand\\sectionname{\\thesection}` 中使用 CCT 特有的 `\\sectionname`，标准 LaTeX/ctexart 中不存在此命令。**修复**：删除该行。
- **EPS 图片不支持（高频）**：Tectonic 不支持 PostScript/EPS 图片（见 tectonic/issues/27），编译报 `image inclusion failed for ".eps"`。**修复**：用 Ghostscript 将 `.eps` 转 `.pdf`，保留原 `.eps` 为源文件。命令：`for f in *.eps; do gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile="${f%.eps}.pdf" -dEPSCrop "$f"; done`。注意：`\\includegraphics{image1}`（无扩展名）时 XeTeX 会按 `.pdf > .png > .jpg > .eps` 顺序查找，转换后 PDF 版本自动优先。**必须同时更新 .gitignore**：转换后的 `image*.pdf` 会被 `*.pdf` 规则排除，需添加 `!image1.pdf` / `!image2.pdf` 例外
- **`mathspec` 宏包 + `\\setallmainfonts` 在 tectonic 中可用**：部分模板（如 NJUPT）使用 `mathspec` 包的 `\\setallmainfonts{<family>}` 统一设置英文正文、无衬线、等宽及数学字体。此命令在 tectonic 中正常工作，Docker 中的 Times New Roman 系统字体可被正确识别。搭配 `BoldFont`/`ItalicFont`/`BoldItalicFont` 选项也能通过 fontconfig 找到对应变体（TIMESBD.TTF/TIMESI.TTF/TIMESBI.TTF）。\n\n- **`\\newCJKfontfamily` + `Path=` 在 .cls preamble 中报 `Missing \\begin{document}`（高频）**：`\\newCJKfontfamily\\<cmd>[Path=font/]{font.ttf}[features]` 在 .cls preamble 中触发此错误——与 `\\setCJKfamilyfont` 的 `Path=` 行为不同，`\\newCJKfontfamily` 不支持在 .cls 中指定 `Path=`。**修复**：两步法——① `\\setCJKfamilyfont{<family>}[Path=font/,<features>]{font.ttf}`；② `\\NewDocumentCommand\\<cmd>{}{\\CJKfamily{<family>}}`。示例：`\\setCJKfamilyfont{zhkai}[Path=font/,AutoFakeBold]{simkai.ttf}` + `\\NewDocumentCommand\\kaishu{}{\\CJKfamily{zhkai}}`。此写法适用于所有 xeCJK 字体声明命令。\n\n- **`:e`-expansion 变体不支持（旧版 expl3，高频）**：`e`-expansion 于 2022 年加入 expl3，tectonic 的 expl3 版本不支持。涉及 `\\tl_if_empty:eTF`、`\\str_case:enF`、`\\xxx:en` 等模式。**修复**：每个调用前加 `\\exp_args:Ne` 前缀（如 `\\exp_args:Ne \\str_case:nnF`）。扫描命令：`grep -n ':e[nNTVFvopwf]' *.cls`。详见 `references/tectonic-expl3-compatibility.md`
- **`\\cs_generate_variant:Nn ... { e }` 不支持**：`\\cs_generate_variant:Nn` 不接受 `e` 类型参数。**修复**：删除该行，将所有 `\\xxx:en` 调用改为 `\\exp_args:Ne \\xxx:nn`。
- **xtemplate `\\s__clist_stop` 内核 bug（TL2023，不可修）**：部分模板（如 nju-lug/NJUThesis v1.5.1）的 `\\DeclareInstance{...}{page}{key=val,...}` 在 TL2023 的 xtemplate 中触发 `The key '\\s__clist_stop ' has no value`。这是 LaTeX3 内核 scan mark 泄露到 key-value 解析的 bug，**用户层无法修复**。标识：编译报 `Package xtemplate Error: The key '\\s__clist_stop'`。处理：① 确认是 xtemplate bug 而非提取残留；② 在 .def 文件中 grep `\\@@_declare_page:nn` 确认调用位置；③ 如无法绕过，标记为"需 Docker 镜像升级至 TL2024+"，源码+AGENTS.md 可照常上线
- **Times New Roman 在 Docker 中可用**：Docker 镜像 `/usr/local/share/fonts/custom/` 下有 TIMES.TTF / TIMESBD.TTF / TIMESI.TTF / TIMESBI.TTF。`\setmainfont{Times New Roman}` 可通过 fontconfig 找到。但用 `\IfFontExistsTF{./misc/times.ttf}` 按文件名匹配本地文件的 fallback 分支在 Docker 中永远失败，会走到后续 fallback（如 TeX Gyre Termes）。不算 bug，但 compile log 会有 `accessing absolute path` 警告。

- **`\IfFileExists{fonts/}` + `\else \setmainfont{TeX Gyre Termes}` 回退在 Docker 失败（高频）**：部分模板使用 `\IfFileExists{fonts/simsun.ttc}` 检测是否上传了本地字体，在 `\else` 分支用 `\setmainfont{TeX Gyre Termes}` + Fandol CJK 字体。Docker 镜像有 SimSun/SimHei 系统字体但无 TeX Gyre Termes 系统字体，fontspec 找不到。**修复三元组**：① `\setmainfont{TeX Gyre Termes}` → `\setmainfont{Times New Roman}`；② CJK song/hei → `SimSun`/`SimHei`（Docker 有系统字体）；③ CJK kai/fang → 回退到 `SimSun`（Docker 无 KaiTi/FangSong 系统字体，Fandol 字体在 tectonic bundle 中但 fontspec 的系统字体查找路径不可达）。示例见 `references/jssnu-template.md`。

- **COS 字体文件名大小写与模板引用不同（高频）**：COS 存储的某些字体是**大写文件名**（如 `SIMLI.TTF`），但模板内引用使用**小写**（如 `simli.ttf`）。macOS 大小写不敏感文件系统自动兼容，Linux 容器需要 init.sh 内 `cp SIMLI.TTF simli.ttf` 显式处理。影响字体：SIMLI.TTF→simli.ttf, SIMFANG.TTF→simfang.ttf 等。检查方法：对比 `font_url.txt` 中文件名和模板 `.cls` 中 `\IfFileExists{字体/xxx}` 参数

- **nemcmthesis（东北三省数学建模联赛）模板**：`JohnsonLo00/nemcmthesis`，cls 含三级字体 fallback（Times→本地 ttf→TeX Gyre Termes），ctex 默认 CJK，natbib+gbt7714 参考文献，`\lstinputlisting` 引用 codes/。适配要点详见 `references/nemcm-template.md`。

- **Beamer 模板零字体依赖**：beamer 类模板（如 Monograph Beamer Theme）使用 `\\usefonttheme{serif}` + T1 fontenc 的标准 LaTeX 字体，无需额外下载。init.sh 的 `FONT_FILES=()` 设置为空数组

- **零 CJK Beamer 适配：从 ctex+unicode-math 的 GitHub fork 剥离 CJK 依赖（新发现模式）**：当 TeXPage-only Beamer 模板仅能从 GitHub 用户 fork（如 `<template>formyself` 仓库）获取源码，且 fork 添加了 `\\RequirePackage[scheme=plain]{ctex}`、`\\RequirePackage{fontspec}`、`\\RequirePackage{unicode-math}` 等重依赖时，可三步剥离为纯英文零 CJK 模板：① 移除 `ctex`/`fontspec`/`unicode-math` 及所有 `\\setmathfont{...}` 调用（默认 Latin Modern Math 已足够）；② 移除 main.tex 中的 CJK 字体命令（`\\songti` 等）——若 main.tex 无中文内容则零副作用；③ 检查 `main.tex` 和 `.cls` 中是否使用了 `unicode-math` 专有命令（`\\symup`、`\\symbf`、`\\increment` 等）——如有则替换为标准 LaTeX（`\\mathbf{}`、`\\Delta` 等）。**init.sh 用 `FONT_FILES=()` + `set -e`（无 `-u`）**。本会话案例：ECNU Beamer（MonkeyUnderMountain/ecnubeamerformyself）→ iftaken/ecnu-beamer，剥离后 803KB PDF 编译通过。

- **`\\item` 在 frame 内但不在 list 环境内（\"Lonely \\item\" 高频）**：手写 Beamer 源文件常见：`\\begin{frame}{标题}\\n    \\item ...` — 缺少 `\\begin{itemize}`（或 enumerate）。编译报 `LaTeX Error: Lonely \\item--perhaps a missing list environment`。**修复**：在 frame 开头补 `\\begin{itemize}`，末尾补 `\\end{itemize}`。此模式也适用于 frame 内直接使用 `\\item` 的 enumerate 场景。

- **`\\end {frame}` 含空格**：`\\end {frame}`（`\\end` 和 `{frame}` 之间有一个空格）TeX 解析为 `\\end` 命令后跟一个空格，导致 frame 环境未正确关闭。编译可能报 \"Lonely \\item\" 或 \"Missing \\endgroup\"。**修复**：改为 `\\end{frame}`（无空格）。`grep -n '\\\\end {' *.tex` 扫描所有含空格的 `\\end` 命令。
  - **`\\newcommand{。}{．}` Unicode 活动字符在 tectonic 中报 "Missing control sequence inserted"（中频）**：部分 Beamer 模板尝试用 `\\newcommand{。}{．}` 定义 Unicode 活动字符来替换中文句号。tectonic/XeTeX 下此语法失败。**修复**：直接注释掉该行（仅为排版微调，不影响编译和输出）。本会话案例：XJTU_beamer（lonaparte/XJTU_beamer）。
  - **`\\newcommand` 意外嵌套在其他宏定义体内（源码 bug，中频）**：当源文件中 `\\newcommand{\\foo}[N]{...\\end{X}}` 的右花括号缺失或错位时，后续的 `\\newcommand{。}{．}` 可能被吞入该宏的替换文本中，导致编译错误。**诊断**：编译报错行号指向 `\\newcommand{。}{．}`，但上游源码中该行独立于前一个宏定义。**修复**：在 `\\end{figure}`（或等价环境）后补上缺失的 `}`，将该 `\\newcommand{。}{．}` 移到宏定义外部。本会话案例：lonaparte/XJTU_beamer 的 `\\figfig` 末尾缺 `}`，导致 `\\newcommand{。}{．}` 被错误嵌套。
- **多个 tectonic Docker 容器并发编译导致缓存竞争 → 虚假报错（高频，诊断陷阱）**：多个 `docker run` 同时挂载同一个 `~/.cache/paper-tectonic` 目录时，tectonic bundle 文件可能被并发写入/读取，导致非确定性编译失败。**症状**：同一模板第一次失败（`Undefined control sequence`）、第二次成功、第三次又失败——且错误位置随机漂移（options.def:187 → metadata.def:271），不是模板问题。**诊断**：单独跑一次不带并发即通过 = 缓存竞争。**修复**：不要并行编译不同模板；如需并行，为每个编译进程使用独立缓存目录（`-v /tmp/tectonic-cache-XXX:/root/.cache/Tectonic`）。不要基于并发失败结果修改模板代码。\n\n\n\n- **GitHub API 间歇性 EOF 故障（基础设施级）**：`gh repo create`、`gh search repos`、`gh api` 等所有 GraphQL/REST 调用可能全部返回 `EOF`（空响应），持续数小时。**此时只有 SSH git 操作可用**（`git clone git@github.com:...`、`git push`）。处理策略：\n  1. 优先处理已有 repo 的模板（SSH push 直接可用）\n  2. 对于需要新建 repo 的模板，本地完成编译+结构初始化，等 API 恢复后批量 `gh repo create` + `git push`\n  3. 子 Agent 遇到 EOF 会超时（600s）——不要重试同一个 API 调用，改用 SSH 路径或跳过\n  4. 检查 API 恢复：`gh api user --jq '.login'` 返回正常即恢复\n\n- **nwputhesis `\\DeclareKeys`→`\\keys_define:nn` 适配模式（已确认可行）**：`\\DeclareKeys`/`\\SetKeys`/`\\ProcessKeyOptions` 全部替换为 expl3 原生 `\\keys_define:nn`/`\\keys_set:nn` + 自定义 `\\@classoptionslist` 处理函数。tectonic TL2023 不含 l3keys2e 2022-06-01 新版，但 `\\keys_define:nn`（expl3 内核）可用。编译通过 1.5MB PDF。\n\n- **BITThesis v3.8.12 确认 TL2023 兼容**：BITNP/BIThesis 硕博模板（expl3-based, dtx 生成）不使用 `\\ProcessKeyOptions`、`:e` 变体、`\\NewTemplateType` 等 TL2024 特性。Docker 编译通过 560KB，ctex 自动检测 Fandol fontset，零字体下载。\n\n- **DeepSeek API Content Exists Risk 错误（平台级，可复现）**：部分模板的 TeXPage 页面内容或源文件被 DeepSeek 安全审核标记，导致子 Agent API 调返回 `400 Content Exists Risk`。**已确认模板**：哈尔滨工业大学（深圳）空间天气建模课程作业（本会话验证 2 次重试均失败）、钱院学辅 LaTeX 书籍模板。**诊断信号**：子 Agent `exit_reason=max_iterations` 且 error 字段含 `Content Exists Risk`。**处理**：跳过该模板，不重试（重试也失败）。与其他 API 阻塞理由（余额不足等）区分：此错误针对特定模板内容，换模板即可继续。主 Agent 直接操作可尝试但同样不可靠。

- **execute_code 的 read_file→write_file 链会污染文件内容**：`read_file` 返回的内容包含行号前缀（如 `     1|content`），直接作为 `write_file` 的 content 参数会将行号写入磁盘文件 → 编译报 `Missing \begin{document}`。**修复**：从 WebBridge evaluate 返回的原始字符串用 `cat /tmp/file.tex > target` 或 Python `open().write()` 写入，不经过 read_file 管道。

- **TeXPage download API 返回 200 但内容为 JSON 错误（高频陷阱）**：`/api/template/download?templateId=...` 始终返回 HTTP 200，即使未登录也如此。body 是 `{"status":{"code":1003,"message":"Not logged in"}}` 而非 zip 文件。**必须用 `file` 命令或检查前几个字节区分**，不可仅靠 HTTP 状态码

- **GitHub fork 缺失核心 .cls 文件 + 上游已删除（阻塞级）**：部分模板的 GitHub fork（如 zhout26/stuthesis）只包含章节/样式/图片文件，**缺少 `.cls` 文档类本身**。此时若原始上游 repo（如 stutug/stuthesis）已被删除或私有化，GitHub 全网代码搜索也找不到 `.cls` 文件。**诊断信号**：`find . -name '*.cls'` 返回空，`main.tex` 中有 `\documentclass{<name>}` 但找不到 `<name>.cls`。**无效尝试**：CTAN 搜索、Overleaf zip 下载、Wayback Machine、校内 Git 镜像（外网不可达）、TeXPage OSS URL（NoSuchKey/AccessDenied）、GitHub code search（全网无结果）。**唯一有效路径**：回到 TeXPage 浏览器端，"Open as Template" 创建项目后在编辑器中提取 `.cls` 文件内容。TeXPage curl 直接访问会 403（ESA 拦截），必须走实际的浏览器交互。详见 `references/github-fork-incomplete-upstream-gone.md`。

- **GitHub 全网代码搜索可找到孤儿 .cls（不是每次都绝望）**：与上方不同——当模板的原始上游被删除但 **其他用户 fork 了完整仓库**（含 .cls），GitHub 代码搜索可以直接找到。CSPC CCS Thesis 的 `cspcccsthesis.cls` 即通过 `gh search code cspcccsthesis.cls` 在 `crispyp0tat0/thesis` 等 5+ 个 fork 中发现。**判定方法**：`gh search code "<classname>.cls" --language tex` 确认有结果后，选一个最新的 fork clone。这比浏览器提取快 10 倍。

- **GBK/GB2312 编码（高频，旧中文模板）**：2015 年前后的中文 LaTeX 模板源码常使用 GBK/GB2312 编码，`file` 命令显示为 `ISO-8859 text`。tectonic 报大量 `Invalid UTF-8 byte` warning 且最终 `Text line contains an invalid character` error。**修复**：`iconv -f GBK -t UTF-8 <file> > <file>.utf8 && mv <file>.utf8 <file>`。影响文件通常包括 .cls 和 .tex（.sty 文件一般是 ASCII，无需转换）。诊断信号：read_file 返回的注释/中文内容显示为 `���` 乱码。

- **tectonic 报 Undefined control sequence 但不显示具体命令（诊断方法）**：tectonic 的 terminal 输出 `error: main.tex:173: Undefined control sequence` 只给出行号，不显示哪个宏未定义。需加 `--keep-logs` 重新编译，然后查看 `main.log` 搜索 `! Undefined control sequence` 找上下文。常见根因：ctex fontset 失败导致 CJK 命令未注册（见上方 ctex fontset 三层回退策略）。

## 批量处理模式

从飞书表挑选 5-30 个待适配 TeXPage 模板，分批并行上线：

```
1. 查询飞书模板管理表，筛选 Texpage + 非已上线，排除已处理
2. 分 3+3+3+... 批次 delegate_task 并行，每批 timeout 2000s
3. 每批完成后检查结果，失败的手动收尾或记录到任务表
4. 所有完成后汇总：成功/阻塞/失败的 repo URL
5. 飞书批量同步状态（+record-batch-update 分组写回）
```

**子 Agent toolsets 必须包含 browser**：TeXPage 操作依赖 Kimi WebBridge，不含 browser 则无法进行"Open as Template"提取。

**TexPage-only 策略**：发现无 GitHub 源时立即走「占位先行」——创建仓库 + 注入标准文件 + 推占位符，不阻塞流水线。后续交人工（马睿曦）从浏览器提取。

**超时恢复策略（高频）**：子 Agent 首次超时（通常卡在 GitHub 搜索阶段），不要放弃。**立即重试**——这次直接用已知源仓库名 `gh repo clone <known-source>` 跳过搜索，通常 2 分钟内完成。SJTUBeamer：首次 600s 超时 → 重试 `sjtug/SJTUBeamer` 直接 clone → 96s 完成。CMC MSU：首次 50 步用尽 → 重建缺失文件 → 197s 完成。迭代用尽的模板同理：检查已写入文件→补全缺失项→编译→推送。

**超时恢复：检查 /tmp 残留工作目录**：子 Agent 超时后，不要从零重新开始。先 `ls /tmp/<repo-prefix>*` 检查是否留下了部分克隆/编译产物。常见残留模式：`/tmp/<name>-source`（上游克隆）、`/tmp/<name>-work`（适配工作区）、`/tmp/<name>-preview.pdf`（已完成编译的 PDF）。若 PDF 已编译成功且源文件齐全，直接 `git init && git remote add origin && git push --force` 完成上线，无需重新跑流水线。已验证：NUIST、BIThesis 本科均通过此模式恢复。

## 批量导入 + 发布（心河Paper 平台上线）

模板适配完成并推送到 GitHub 后，需导入到平台并发布到模板市场。

### 批量导入（WebBridge 自动化）

```bash
cd /Users/ming/project/cli_xinhe_status
.venv/bin/python scripts/bulk_import_templates.py --single --repo <name> --name "显示名" --desc "描述" --tags "标签" --category "分类"
.venv/bin/python scripts/bulk_import_templates.py /tmp/templates_import.csv
```

脚本通过 Kimi WebBridge 自动化网页表单。**关键 pitfall**：React 受控组件必须用原生 value setter（见 kimi-webbridge: `references/react-controlled-inputs.md`）。

### 批量发布（直接写库）

```bash
cd /Users/ming/project/cli_xinhe_status
.venv/bin/python scripts/bulk_publish.py           # 全量发布
.venv/bin/python scripts/bulk_publish.py --dry-run  # 预览
.venv/bin/python scripts/bulk_publish.py --limit 5  # 测试
```

通过 `write_query()` 直接写 PostgreSQL：`status=published`, `scope=public`, 设置 `auditInfo`。发布后模板立即出现在市场。

### PII 清洗脚本

代码审查中发现的 PII 清洗模式：

```bash
# 扫描：中文名、邮箱、手机、QQ/微信、二维码、GitHub 个人链接
grep -rn "作者\|原作者\|维护者" *.cls *.sty *.tex
grep -rnE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' *.tex *.cls *.md
grep -rnE '(qq|wechat|微信|扣扣)' *.tex *.md
```

替换规则：中文名→张三/李四/王五，英文名→Tom Smith/Jerry Johnson，邮箱→example@example.com，手机→13800138000，QQ/微信/二维码→删除，个人GitHub→iftaken。

**后台编译恢复**：子 Agent 超时但 Docker 编译已在 /tmp 完成时（exit 0 + main.pdf 已生成），直接 `cd /tmp/<workdir> && git init && git remote add origin git@github.com:iftaken/<repo>.git && git add -A && git commit && git push --force` 完成上线，无需重新跑流水线。已验证：NUIST（南京信息工程，3MB PDF，子 Agent 600s 超时但编译成功→推送）。

- **`biblatex-gb7714-2015` 的 `gbrefcompress` counter 在 tectonic TL2023 中不可用（高频）**：使用 `gb7714-2015` 参考文献样式的模板通常有 `\\setcounter{gbrefcompress}{3}` 行。tectonic TL2023 bundle 中的 `biblatex-gb7714-2015` 包未定义此计数器——无论在 preamble 还是 `\\AtBeginDocument` 中调用均报 `No counter 'gbrefcompress' defined`。**修复**：直接注释掉该行。`gbrefcompress` 控制参考文献压缩阈值（三篇起压缩），属于排版微调，不影响编译和输出。

- **tectonic-biber 在 Docker 镜像中可用（不是坑，是好消息）**：Docker 镜像 `/usr/local/bin/tectonic-biber` 是 tectonic 的 Rust 版 biber 实现。当模板使用 biblatex + `\printbibliography` 时，tectonic 会**自动检测并调用 tectonic-biber**，然后自动 rerun 解析交叉引用。不需要注释掉 `\printbibliography`，也不需要手动运行 biber。索引（xindy/imakeidx）仍不支持——需 `\providecommand{\index}[1]{}` 占位。

- **biblatex 样式不兼容 tectonic TL2023（高频）**：部分模板使用特定 biblatex 样式（如 `acmnumeric`、`apa`、`chicago` 等）在 tectonic TL2023 bundle 中不存在。**诊断**：编译报 `Package biblatex Error: Style 'xxx' not found`。**修复**：改用 tectonic bundle 中可用的通用样式——`numeric`（最安全）、`ieee`、`authoryear`、`alphabetic`。本会话案例：CSPC CCS Thesis 使用 `acmnumeric` → `numeric`。

- **纯英文 thesis 模板（gatechthesis 派生）零 CJK 依赖**：部分英文论文模板（如 CSPC CCS Thesis）基于 `report` 类，使用 `\usepackage{times}` 加载 psnfss Times 字体（→ Docker 系统 Times New Roman 可用），不加载 ctex/xeCJK。此类模板 init.sh 的 `FONT_FILES=()` 为空数组，无需下载任何字体。注意：`\usepackage{times}` 在 XeTeX 下可用（psnfss 提供 Times 的 Type1 替代），但 `\setmainfont{Times New Roman}` 更可靠（走 fontspec 系统字体查找）。若 cls 同时加载 `\usepackage{times}` 和 `\RequirePackage{ctex}`，ctex 会自动加载 fontspec 覆盖 psnfss 字体设置，此时无冲突。

- **GitHub 代码搜索找回 .cls 文件（高频捷径）**：当 TeXPage-only 模板缺少 .cls 且无浏览器工具时，可用 `gh search code <classname> --limit 20` 搜索 GitHub 上其他使用同一模板的学生论文仓库。这些仓库常包含完整的 .cls 文件。然后通过 GitHub API 直接提取内容：`gh api repos/<owner>/<repo>/contents/<classname>.cls --jq '.content' | base64 -d`。**注意**：不同学生仓库中的 .cls 可能有本地化修改（硬编码标题、图片路径等），选择通用性最好的版本（检查 `\ProvidesClass` 行日期，选较新且不含硬编码文本的）。本会话案例：CSPC CCS Thesis 从 `crispyp0tat0/thesis` 提取 cls（通用 `\@title`），而非 `CSPC-BSCS-3B/Virgo_Thesis`（硬编码项目标题）。详见 `references/texpage-source-discovery.md`。

- **用户自定义字体宏中的空格污染（高频）**：当模板使用自定义宏（如 `\SetCJKfont`）封装字体加载时，宏定义体中的空格（`{ #1 [ ... ] { #2 } }`）会被 TeX 作为参数的一部分传递给底层命令，导致 fontspec 收到带空格的字体名（如 `" FZ-ShuSong "`）无法匹配。**修复**：宏定义体中去掉所有参数周围的空格，使用 `%` 注释行尾防止换行空格——`{#1[...]{#2}}`。此模式适用于所有封装 `\setCJKmainfont`/`\setCJKfamilyfont`/`\newCJKfontfamily` 的自定义宏。

## 注意事项

- **`patch` 工具 CRLF 陷阱（高频）**：Windows 编辑的 .tex 文件含 `\r\n` 行尾，`patch` 用 LF 匹配会报 `Found N matches` 或 `Could not find a match`。`read_file` 的分页读取也会干扰。**修复**：用 `perl -i -pe 's/old/new/g'` 或 `sed` 批量替换。详见 `references/pii-scrubbing.md`。
- **`patch` 工具反斜杠转义污染（高频）**：`patch` 在替换 TeX 文件内容时会将 `\` 双写为 `\\`（如 `\texttt` → `\\texttt`），导致编译失败。**修复**：对含 TeX 命令的替换，用 `sed -i '' 's/old/new/g'` 替代 patch；如果已污染，用 `git checkout -- <file>` 恢复后用 sed 重做。
- **lark-cli `--json @` 只接受相对路径**：`--json @/tmp/file.json` 报 `must be a relative path within the current directory`。**修复**：cp 到当前目录用 `@./file.json`，或 cd 到目标目录。
- **lark-cli `+record-batch-create` 单批 ≤200 条**：超过需分批。`fields` 数组与 `rows` 中每行按列序一一对应，空值用 `null`。
- **`+record-list` 输出非纯 JSON**：包含表格线，需用 `grep` 提取而非 `jq` 解析。提取 GitHub URL 用 `grep -o 'github\.com/[^ )|]+'`。
- 字体文件**绝对不能**进入 git 仓库
- tectonic 缓存必须挂载宿主机目录
- `main.pdf` 是系统关键文件，必须保留在仓库中
- `font/` 目录放项目内（不进 git），Docker 编译时通过 `-v $(pwd):/app` 挂载生效
- **批量处理优先级**：国内大学模板优先（90%有GitHub源）→ 国外模板其次 → TeXPage-only 最后（需浏览器，占 60%）
- **SJTU/中山/华科等，不要花时间深修，推送源码+标记即可
- **子Agent 复杂模板限时**：简单模板 3-5min，中等 10-15min，复杂 TL2024 直接跳过不要死磕
- **Feishu 状态同步**：每处理完一个更新模板管理表状态（待适配→已上线），复杂/跳过的记录到任务表
- **TeXPage-only 近重复模板快速适配**：当 TeXPage-only 模板与已有 GitHub 源模板高度相似时（如 sgu-thesis v1.0 ↔ v1.1），直接从 GitHub 源克隆+适配，跳过浏览器逐文件提取。逐文件提取每模板耗时 10-20 分钟，仅用于无任何 GitHub 近亲的模板
- **浏览器逐文件提取优先级低**：确认为 TeXPage-only 且无 GitHub 近亲的模板（约占 60%），标记为「待浏览器提取」或「适配中」，不阻塞批量流水线
