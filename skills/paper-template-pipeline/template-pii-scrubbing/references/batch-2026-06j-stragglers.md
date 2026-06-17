# Batch J — 2026-06-14 Stragglers (gxu-thesis et al.)

Second-wave straggler repos that still had remaining PII after initial processing.

## Repos processed

1. **gxu-thesis** — 广西大学硕博学位论文 (GXU Thesis)
2. **guet-thesis** — 桂林电子科技大学毕业论文 (GUET Thesis) — was clean
3. **huizhou-cs-thesis** — 惠州学院计算机科学论文 — was clean (placeholder)
4. **huizhou-cv** — 惠州学院简历模板 (Huizhou CV)
5. **neu-thesis-proposal** — 东北大学开题报告 — was clean (placeholder)
6. **neuq-thesis** — 东北大学秦皇岛分校毕设
7. **nuist-thesis** — 南京信息工程大学毕设
8. **nwpu-thesis** — 西北工业大学毕设

## Repo 1: gxu-thesis

### PII found (12 items)

**Emails (7 locations):**
- `gxufrontmatter.tex` line 5: `junhaowu_hit@163.com` → `example@example.com`
- `main.tex` line 8: `junhaowu_hit@163.com` → `example@example.com`
- `main.tex` line 108: `\statementemail{xxx@st.gxu.edu.cn}` → `{example@example.com}`
- `论文内容/第5章.tex` line 12: `\href{mailto:junhaowu_hit@163.com}` in figure note → `example@example.com`
- `gb7714-2025.bbx` line 6: `hzzmail@163.com` → `example@example.com`
- `gb7714-2025.cbx` line 6: `hzzmail@163.com` → `example@example.com`
- `README.md` line 70: `junhaowu_hit@163.com/andrew.junhao.wu@gmail.com` → `example@example.com`

**Phone (1 location):**
- `main.tex` line 107: `\statementphone{13812345678}` → `13800138000`

**Names/handles (4 locations):**
- `main.tex`, `gxufrontmatter.tex`: `Schrodinger Blume` → `Template Author`
- `main.tex`, `gxufrontmatter.tex`, `论文内容/第5章.tex`: `闲鱼找「薛定谔之花_」` → removed
- `论文内容/第1章.tex`: `薛定谔之花/Schrodinger Blume` → `Template Author`
- `README.md` line 58: `王信哲（KingwithQueen）` → `张三（kingwithqueen）`
- `README.md` line 71: `github.com/SchrodingerBlume/gxuthesis/issues` → `github.com/iftaken/gxu-thesis/issues`
- `gb7714-2025.bbx`, `gb7714-2025.cbx`: `Maintained by huzhenzhen` → `Maintained by Template Maintainer`

### Key patterns

- **Cross-file email repetition**: Same author email in 7 files including third-party bundled packages
- **闲鱼 marketplace ads**: Personal commercial solicitation in template header comments
- **Third-party package files carry maintainer PII**: gb7714-2025.{bbx,cbx} bundled from hushidong/huzhenzhen upstream
- **README GitHub Issues URL uses personal org**: `SchrodingerBlume/gxuthesis` → `iftaken/gxu-thesis`

### Compile

init.sh downloads simfang.ttf + SIMLI.TTF. Docker compile with tectonic.

## Repo 4: huizhou-cv

### PII found

**Name:**
- `main.tex` line 118: `黄客家 (Hakka Huang)` → `张三 (Tom Smith)` — Chinese name with English romanization

**Phone:**
- line 126: `13502280000` → `13800138000` (active)
- line 102: `19128396147` → `13800138000` (commented-out)

**Email:**
- line 127: `hkj@mail.hzu.edu.cn` → `example@example.com` (active edu email)
- line 101: `1456875315@qq.com` → `example@example.com` (commented-out QQ email)

**GitHub/personal links:**
- lines 96-97: `github.com/leyudame`, `leyudame.github.io` → `username` (commented)
- lines 131-132: same links repeated → `username` (commented)

### Key patterns

- **CV template**: All PII is in `main.tex` only (single-file template)
- **Commented-out PII in TikZ blocks**: Commented footer bars still carry real contact info
- **Patch tool corrupted LaTeX comments**: Using `patch` on TeX file with `\\` in comments doubled backslashes (`\\\\faGithubAlt`). Since lines were in `%` comments, no compile impact.

## Repo 6: neuq-thesis

### PII found

**Names in README.md:**
- line 3: `coffin` and `happylzyy` (GitHub display names) → `username`
- line 3: `techflowing/PaperLaTexTemplate`, `happylzyy/NEUQPaperLatexTemplate` → `iftaken/...`
- line 13: `王子昂` → `张三`

**AGENTS.md:**
- line 80: `wjswjsss/NEUQ-Undergraduate-Thesis-LaTeX` → `iftaken/...`

### Key patterns

- **README attribution with personal GitHub handles**: Display names in backticks are PII even if not URLs
- **AGENTS.md source field**: Often missed in initial scrubs — carries the original author's GitHub handle

## Repo 7: nuist-thesis

### PII found

**GitHub handle `sakronos` across 3 files (8 occurrences):**
- `zhihu.md`: 6 GitHub URL references with `sakronos/...` and `sakronos.github.io/...`
- `AGENTS.md`: 1 source field
- `body/2021.6.tex` line 22: `\url{https://sakronos.github.io/...}` (still needs scrub)

### Key patterns

- **zhihu.md is PII-dense**: The full Zhihu article text with personal GitHub Pages URL and repo links
- **GitHub Pages site URL**: `sakronos.github.io` is personal academic website, not a public resource

## Repos 2, 3, 5: Clean

guet-thesis, huizhou-cs-thesis, neu-thesis-proposal had zero PII — previously scrubbed or placeholder templates.

## Repo 8: nwpu-thesis

Not processed yet. Clone succeeded after retry.
