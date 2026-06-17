# Batch E PII Patterns (2026-06-14)

Repos: njit-thesis, nju-thesis-texpage, njupt-thesis, nku-beamer
(remaining: nuist-thesis, nwpu-thesis, oreilly-template, overleaf-lzu-thesis)

## njit-thesis (南京工程学院)

**PII found:**
- `Azidiazide azide 3162572053@qq.com` — QQ email + author handle in comment headers (njit.cls line 2, main.tex line 6)
- Replaced with: `template maintainer example@example.com`

**Compile issues:**
- Missing figures: `figures/smokeblk.pdf`, `figures/cat.pdf` — created 1x1 PNG placeholders, updated .tex refs from .pdf to .png. Pre-existing, not PII-related.

**Verdict:** Light PII, 2 files changed.

## nju-thesis-texpage (南京大学)

**PII found (41 matches across 5 files):**

1. **Email `git+nju-lug-email-3104-issue-@yaoge123.cn`** — GitHub email alias in copyright header (4 files: njuthesis.cls + 3 .def files, lines ~7, ~84-85). Replaced with `example@example.com`.

2. **Email `my@yaoge123.cn` + name `姚舸老师`** — Personal contact in docs (4 files, line ~214). Replaced email with `example@example.com`, name with `模板维护者`.

3. **Chinese name `周煜华`** in BibTeX author examples (4 files, 3 occurrences each at lines 1287/1311/1352). Replaced with `张三`.

4. **Contributor list** in main.tex lines 5-10: real names + personal GitHub handles (atxy-blip, FengChendian, myandeg, glatavento, HermitSun, linyinfeng, Muzimuzhi, liudongmiao, rijuyuezhu). Replaced entire block with generic `% 贡献者（信息已脱敏）\n% 模板维护团队`.

5. **Attribution section** in 4 cls/def files (~lines 246-250): personal names (饶安逸, 赵懿晨) with personal website links (`anyirao.com`, `fengchendian.github.io`) and GitHub handles (@AnyiRao, @FengChendian). Replaced with `% \item 基于前代模板的 NJU Thesis 2018（2018）` and `% \item 基于前代模板的 NJU Thesis 2021（2021）`.

**Compile:** FAIL — LaTeX3 `\s__clist_stop` error (pre-existing Tectonic/TL2023 incompatibility, not caused by scrubbing).

**Verdict:** Heaviest PII so far. All .def files share identical patterns — use `replace_all=true` across files for efficiency.

## njupt-thesis (南京邮电大学)

**PII found:** None. References to `musnows/NJUPT-Bachelor`, `dhiyu/NJUPT-Bachelor`, `imguozr/NJUPThesis-Bachelor`, `lemoxiao/NJUPThesis-Scholar` are upstream attribution links — PRESERVED.

**Compile:** PASS (1.25MB), no font issues.

**Verdict:** Clean repo — all placeholders in place.

## nku-beamer (南开大学 Beamer)

**PII found:**
- `Andrea Gasparini, andrea@gasparini.cloud` — real name + personal email in sty attribution (line 3)
- `Federico Zenith, federico.zenith@sintef.no` — real name + work email (line 6)
- `Håvard Berland` — upstream attribution name (line 7)

Replaced: Andrea Gasparini → Tom Smith, Federico Zenith → Jerry Johnson, emails → example@example.com, Håvard Berland → "the original".

Note: English-only template, so used English fake names per skill rule (not Chinese).

**Compile:** PASS (693KB). Zero CJK font dependency.

**Verdict:** Minimal PII. Single file changed (beamerthemenankai.sty).

## Patterns observed across this batch

- **.def files share identical PII**: When a template has multiple .def variants (undergraduate/graduate/postdoctoral), they're often identical copies with specific tweaks. All PII patterns repeat. Use `replace_all=true` across all of them.
- **Contributor lists in main.tex**: Multi-line blocks with real names + @handles. Replace the entire block rather than individual entries.
- **Attribution sections with personal URLs**: When upstream credits contain personal website URLs (not just GitHub usernames), scrub the names and URLs but preserve the project lineage reference.
- **Missing figures ≠ PII**: Templates sometimes reference example figures that weren't committed. Creating 1x1 PNG placeholders lets the compile pass without introducing PII. Update .tex from .pdf to .png if creating PNG placeholders for missing PDF figures.
