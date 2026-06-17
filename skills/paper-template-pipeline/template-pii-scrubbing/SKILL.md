---
name: template-pii-scrubbing
description: PII scrubbing for LaTeX template repos before public release. Clone, scan, replace, image-check, compile, push.
category: paper-template-pipeline
---

# Template PII Scrubbing

Post-import sanitization of LaTeX template repos before they go live on GitHub (iftaken/*).
Scrubs personal names, emails, phone numbers, social media links, QQ/WeChat handles, QR codes, and student IDs
from .tex, .cls, .sty, .bib, .md, .sh, .dtx files.

## Trigger

Load this skill when the user asks to "scrub PII", "sanitize templates", "remove personal info from repos",
or when processing a batch of template repos for public release.

See `references/batch-2026-06-patterns.md` for concrete PII patterns from the June 2026 batch (batch A: cmc-msu, cqu-report, cspc-ccs, cug-thesis-english, cumcm).
See `references/batch-2026-06b-patterns.md` for the second batch (batch B: dbss-mcm-2026-template, dlmu-bachelor-thesis, dlmu-thesis, ecnu-beamer, elegantbook-custom).
See `references/batch-2026-06c-patterns.md` for the third batch (batch C: hust-thesis, iiser-trivandrum-thesis, iiser-tvm-thesis, imust-bachelor-proposal, imust-bachelor-thesis, imust-microcomputer, imust-microcomputer-training, imust-proposal-template).
See `references/batch-2026-06d-patterns.md` for the fourth batch (batch D: gxu-thesis-template, heu-beamer, hhu-thesis, hitsz-thesis, hkust-thesis, hnu-thesis, huizhou-cs-thesis, huizhou-cv).
See `references/batch-2026-06e-patterns.md` for the fifth batch (batch E: njit-thesis, nju-thesis-texpage, njupt-thesis, nku-beamer, nuist-thesis, nwpu-thesis, oreilly-template, overleaf-lzu-thesis).
See `references/batch-2026-06f-patterns.md` for the sixth batch (batch F: shnu-thesis-template, sht-template, shumo-cup-2025, shuweibei-2025, sjtu-beamer, sjtu-thesis, snut-thesis, southwest-forestry-university-thesis).
See `references/batch-2026-06f-patterns.md` for the sixth batch (batch F: stu-thesis, suda-thesis-231, swfu-graduate-thesis, sxu-homework, sysu-thesis, sztu-thesis, thesis-proposal-template, thu-thesis).
See `references/batch-2026-06f-patterns.md` for the sixth batch (batch F: sdu-thesis, sdu-thesis-design, sdu-thesis-template, sgu-exam, sgu-thesis, sgu-thesis-v1_1, sh-t-latex, shnu-thesis).
See `references/batch-2026-06g-patterns.md` for the seventh batch (batch G: xdu-graduate-thesis, xdu-thesis, xynu-beamer, xynu-thesis, xynu-year-paper, ynu-thesis, zhku-thesis, zjicm-thesis, zjicmv-exp-report, zzuli-thesis, ajbook-template, apmcm-thesis, cjc-template).
See `references/batch-2026-06g-patterns.md` for the seventh batch (batch G: timeline-template, tju-thesis, tufte-template, tutor-resume-template, um-aia-report, us-patent-template, ustb-bachelor-thesis, ustb-graduate-thesis).

See `references/batch-2026-06h-patterns.md` for the eighth batch (batch H: ustb-thesis, ustc-thesis, ustc-thesis-template, whu-proposal, whu-thesis, whut-thesis, wzu-thesis, xauat-thesis).

See `references/batch-2026-06i-stragglers.md` for the straggler batch (batch I: oreilly-template, overleaf-lzu-thesis, scu-beamer, scu-thesis, sh-t-latex, shnu-thesis, southwest-forestry-university-thesis).

See `references/batch-2026-06j-stragglers.md` for the second straggler batch (batch J: gxu-thesis, guet-thesis, huizhou-cs-thesis, huizhou-cv, neu-thesis-proposal, neuq-thesis, nuist-thesis, nwpu-thesis).

## Workflow (per repo)

```
① Clone → ② Scan → ③ Replace → ④ Image check → ⑤ Compile → ⑥ Push
```

### ① Clone

```bash
cd /tmp && rm -rf <repo>-work && git clone git@github.com:iftaken/<repo>.git <repo>-work
```

Always work in `/tmp/<repo>-work`. Delete stale directories first.

### ② Scan for PII

Run these sweeps **in parallel** across `*.{tex,cls,sty,bib,md,cfg,def,dtx}` for the first 3, plus `*` (all files) for social/QR patterns:

**1. Emails:**
```
search_files glob='*.{tex,cls,sty,bib,md,cfg,def,dtx}' pattern='[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
```

**2. Phone numbers (11-digit Chinese mobile):**
```
search_files glob='*.{tex,cls,sty,bib,md,cfg,def,dtx}' pattern='[0-9]{11}|[0-9]{3}[-. ][0-9]{4}[-. ][0-9]{4}'
```

**3. Chinese names in author/contact/thanks fields:**
```
search_files glob='*.{tex,cls,sty,bib,md,cfg,def,dtx}' pattern='\\\\author\{|\\\\thanks\{|\\\\email\{|author\s*=|Author:|作者|原作者|维护者|maintainer'
```
Then grep specifically for 2-4 char Chinese name patterns in those hits:
```
search_files glob='*.{tex,cls,sty,bib,md,cfg,def}' pattern='[\u4e00-\u9fff]{2,4}'
```

**4. QQ/WeChat IDs (number patterns with contact keywords):**
```
search_files pattern='(?i)(qq|wechat|微信|扣扣)[:：]?\s*[0-9]{5,}'
```

**5. Social media / personal links (includes Gitee, 闲鱼):**
```
search_files pattern='(?i)(github\\.com/[^/\\s]+/|gitee\\.com/[^/\\s]+/|zhihu\\.com/people/|blog\\.csdn\\.net/|bilibili\\.com/video/|blog\\.|个人主页|主页|闲鱼)'
```

**6. QR codes / contact invitations (all files):**
```
search_files pattern='(?i)(qr|二维码|扫码|加微信|加群|gongzhonghao|公众号|erweima)'
```
Additionally, check for image filenames containing Chinese pinyin QR indicators: `gongzhonghao-n`, `qrcode`, `erweima-*`. These are WeChat Official Account QR codes and should be replaced with 1x1 transparent PNG placeholders even if the source image file is missing from git (common in templates where images are .gitignore'd).

**7. LaTeX-specific PII vectors:**
```
search_files pattern='(?i)\\\\bioinfo\{邮箱|\\\\aauthor\{|\\\\mentorONE\{|\\\\signofstudent\{|\\\\signofmentor\{'
```
These catch `\bioinfo{邮箱}{sx12101184@qq.com}`, `\aauthor{阿海}`, `\signofstudent{\includegraphics{signatures/阿海.png}}`, etc.

**8. \includegraphics references (for image audit):**
```
search_files glob='*.{tex,cls,sty}' pattern='\\\\includegraphics'
```

**9. Hex-encoded PII in donation/sponsorship blocks (.cls/.sty):**
```
search_files glob='*.{cls,sty}' pattern='\\\\str_set_convert|\\\\\\\\alipayqr|\\\\\\\\wxpqr|\\\\\\\\qqqr'
```
xduts-derived templates use hex-encoded strings for emails and payment QR URLs inside
commented-out `\str_set_convert:Nnnn` blocks. These are always in LaTeX comments (`%` lines).
If found, remove the entire block (typically 58 lines from `\changes{...赞助二维码}` to `\end{figure}`)
and replace with a single comment: `% 赞助二维码部分已移除 (PII scrubbed)`.

**10. Beamer \\titlegraphic portrait images:**
```
search_files glob='*.{tex,cls,sty}' pattern='\\\\titlegraphic'
```
Beamer title graphics often contain personal headshots (e.g., `head.png` at 400KB+). Check the referenced image files — if they are large PNGs (>50KB, non-vector dimensions), they are likely personal portraits and should be replaced with 1x1 transparent PNG placeholders.

### ③ Replace — what to change vs. preserve

**CHANGE / REMOVE:**
- Author real names → fake Chinese names (张三, 李四, 王五, 赵六) or "Tom Smith" depending on language context
- English real names in TeX comments (`% Created by Joel Sleeba`, `% Connect with me at personal.site`) → "模板维护者" or "Tom Smith" depending on template language
- Personal website/GitHub links in comments (`joelsleeba.github.io`, `github.com/joelsleeba`) → remove or repoint to iftaken
- Personal acknowledgements naming specific individuals (`I am thankful to Nikhil Alex Verghese, BS-MS'17`) → generalize to "the contributors"
- Personal copyright lines (TeX files) → change author to "模板维护者" or "Tom Smith"
- LICENSE file copyright lines (`Copyright (c) YYYY personalHandle`) → "Copyright (c) YYYY iftaken"
- Bio info emails
- Personal author commands (`\aauthor{阿海}`, `\mentorONE{海老师}`) → fake names
- Signature image refs (`\signofstudent{\includegraphics{signatures/阿海.png}}`) → `{signatures/placeholder.png}`
- Emails → "example@example.com"
- Personal GitHub repo links → remove entire line or replace with "example/template"
- QQ group numbers, WeChat IDs → remove the line/mention
- QQ numbers in text (e.g., `910014191`, `976053605`) → remove entire table row/line
- Personal blog URLs (cnblogs.com/1210x1184, hatenablog.com, azurekite.cn) → remove
- Weibo, Bilibili, personal website links → remove
- QR code images (WeChat/Alipay donation PNGs) → replace with 1x1 transparent PNG placeholder
- Beamer title graphic portraits (`\titlegraphic{\includegraphics{head.png}}`, 400KB+ PNGs) → replace with 1x1 transparent PNG placeholder
- Signature images (`signatures/阿海.png`, `signatures/海老师.png`) → replace with 1x1 transparent PNG placeholder
- AGENTS.md author/source fields → scrub to fake names or "模板维护者"
- Student IDs (e.g., "20230537华晓蔚") → remove entirely or replace with generic text

**Bib file Chinese author names rule:** When a .bib file is part of a template distribution (not an actual paper's reference list),
replace real Chinese author names with fake ones AND update the bib keys. Example:
`author={付梦印 and 邓志红 and 张继伟}` with key `付梦印2003` → `author={张三 and 李四 and 王五}` with key `张三2003`.
Same for title/school — replace real titles/schools with generic text ("示例书籍标题", "XX大学").
Foreign author names (Stauffer, Chris; Grimson, W Eric L) in the same bib are fine — leave them.

**PRESERVE (do NOT change):**
- University names (e.g., "Lomonosov Moscow State University", "重庆大学", "Camarines Sur Polytechnic Colleges") — these are product-defining
- University logos (`\\includegraphics{pic/校徽...}`) — institutional assets, not personal
- Placeholder names already in place (e.g., "Zhang San" = John Doe, "Li Si" = Jane Doe, "Author Name 1", "Surname Name Patronymic")
- Template licenses (CC BY 4.0)
- TeXPage/Overleaf template URLs (public resource links)
- latexstudio.net URLs (public community sites)

**Edge case: placeholder names in Chinese templates.** "Zhang San" (张三), "Li Si" (李四), "Author Name 1", "Surname Name Patronymic"
are already fake. Don't overwrite them — the scan + human review determines which are real.

### ④ Image check

Find all `\includegraphics` references:
```
search_files glob='*.{tex,cls,sty}' pattern='\\includegraphics'
```

Check actual image files in the repo (`search_files target=files` on image directories).

**Replace if:** the image is a QR code, WeChat public account QR, personal portrait, or contains personal contact info.
**Keep if:** university logo, generic placeholder ("example.jpg"), diagram, chart.

If unsure, check file size/type. Large photos (80KB+ JPG) could be portraits — but skip unless obviously personal.

### ⑤ Compile test

**5a. Run init.sh first (font download):**

If `init.sh` exists in the repo, run it BEFORE compiling. Many paper-pipeline templates
download required CJK fonts (FangSong, SimLi, etc.) from COS. Skipping this causes
spurious compile failures that look like pre-existing issues but are trivially fixable.

```bash
cd <workdir> && bash init.sh 2>&1
```

If `init.sh` prints "No external fonts needed" or similar, that's fine — fonts are already
in the Docker image or TeX Live bundle. Proceed to compile.

**5b. Docker compile:**

```bash
mkdir -p ~/.cache/paper-tectonic && docker run --rm --platform linux/amd64 \
  -v <workdir>:/app \
  -v ~/.cache/paper-tectonic:/root/.cache/Tectonic \
  crpi-b75iph3qtzyryyvz.cn-hangzhou.personal.cr.aliyuncs.com/paper-prod/paper-sandbox-cli:latest \
  tectonic -X compile main.tex 2>&1 | tail -5
```

**Success:** exit code 0, main.pdf generated, size >= 10KB.
**Failure:** if font error persists after init.sh, it's a genuine pre-existing template issue — note it and move on.
Warnings (Overfull hbox, missing characters, absolute path) are OK — only fatal errors matter.

### ⑥ Commit and push

```bash
cd <workdir>
git add -A
git diff --cached --stat
git commit -m "scrub: remove PII, replace with placeholder names"
git push origin main
```

If no PII changes were needed but PDF was regenerated:
```
git commit -m "scrub: no PII found, regenerate main.pdf"
```

## Empty repos

If `git clone` returns "You appear to have cloned an empty repository" — skip immediately.
No files to scrub, no compile possible.

## Pitfalls

### Prefer sed over patch for TeX files

The `patch` tool doubles backslashes in `.tex`/`.sty`/`.cls` files. For simple replacements
(emails, names, numbers, URLs), use `sed -i '' 's/old/new/g'` instead. See the **patch tool
corrupts TeX backslashes** section under ③ Replace for the full workaround and recovery steps.

### Patch fails with "Could not find a match"

This happens when `old_string` has too much surrounding context with subtle whitespace/encoding differences,
especially with Chinese text. **Fix:** retry with a shorter `old_string` — match just the line/segment that
needs changing, not the surrounding lines. Break multi-line replacements into separate single-line patches.

### Never trust "PII already done" — always re-scan

When a repo is marked as "PII done, just needs compile+push" by a human, do NOT skip the scan step.
Run the full scan sweep anyway. Example: `cumcm-paper-template` was marked "QQ numbers removed, WeChat QR ref removed"
but still had 3 QQ group numbers (91940767, 478023327, 640633524) and 2 WeChat QR image files
(gongzhonghao.jpg, gongzhonghao2.png). The earlier scrub was incomplete.

Human status notes are hints, not guarantees. The scan is fast and catches what they missed.

### Diff shows only main.pdf changed

This means the repo was already clean (all names were placeholders). Use the alternative commit message
and push anyway — the compile step generates a fresh PDF.

### Chinese text in TeX comments

Chinese characters in `%` comments can be PII (e.g., `% 20230537华晓蔚`). Scan Chinese patterns too.
Replace with generic Chinese text (e.g., `% Adapted from template`) when found.

### Commented-out resume/patent/achievement example blocks

Templates often include example resume or patent achievement sections that are entirely commented out
with `%` — but still contain real author names from published patents (e.g., `% \item 胡楚雄, 付宏, 朱煜, 等. 一种磁悬浮平面电机`).
These look like harmless boilerplate but carry real PII. When scanning `resume.tex` or achievement sections,
check commented-out blocks too. Replace the names with fake cycling placeholders (张三/李四/王五).

### patch tool corrupts TeX backslashes — use sed for simple replacements

The `patch` tool (StrReplaceFile) doubles backslashes in TeX files: `\texttt` becomes `\\texttt`,
`\Large` becomes `\\Large`, and literal tab characters can become `\t` (backslash-t, interpreted by
TeX as a command prefix). This causes `You can't use a prefix with '\aftergroup'` errors.

**Fix:** For simple string replacements (emails, names, QQ numbers), use `sed` instead:

```bash
cd <workdir> && sed -i '' 's/real-email@example.com/example@example.com/g' main.tex tex/chapter1.tex
```

Verify with `grep -n` afterward. Only use `patch` for replacements that require precise
context matching across multiple lines where sed is impractical — and verify the file
afterward by compiling.

If `patch` already corrupted a file, restore it from git before redoing with sed:
```bash
git checkout main.tex tex/chapter1.tex
```

### Replacing signature / QR images

When a template references personal signature images (`signatures/阿海.png`) or QR codes, create a 1x1 transparent PNG placeholder:
```python
import struct, zlib
def create_placeholder_png():
    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>I', 13) + b'IHDR' + struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)
    ihdr += struct.pack('>I', zlib.crc32(ihdr[4:]))
    raw = zlib.compress(b'\x00\x00\x00\x00')
    idat = struct.pack('>I', len(raw)) + b'IDAT' + raw + struct.pack('>I', zlib.crc32(b'IDAT' + raw))
    iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', zlib.crc32(b'IEND'))
    return sig + ihdr + idat + iend
```
Place in the same directory as the original image. Remove original images after replacing references in .tex.

### Compile failure due to missing fonts

If `tectonic` fails with a font-not-found error, **first run `bash init.sh`** in the work directory.
Paper-pipeline repos have `init.sh` scripts that download required CJK fonts (FangSong, SimLi, etc.) from COS.
This fixes most font errors — only treat it as a genuine pre-existing issue if the error persists AFTER init.sh.
Fonts like "CMU Typewriter Text" or exotic math fonts that init.sh does not cover are genuine pre-existing template
issues — note them in the summary and move on. Do NOT attempt to download fonts outside init.sh — that is beyond
PII scrubbing scope.

**init.sh depends on missing `font_url.txt`**: Some templates (e.g., cjc-template) use an init.sh that
reads font download URLs from `font_url.txt` via `grep`, but the file was never committed to the repo.
Without it, `init.sh` runs silently and produces an empty `font/` directory — no fonts downloaded.
**Fix**: switch to Fandol fonts (tectonic bundle built-in) via `\setCJKmainfont{FandolSong-Regular.otf}`
etc. in main.tex. Fandol provides Song/Hei/Kai/Fang four-weight coverage, zero download. See
`paper-template-pipeline/references/cjc-template.md` for the full migration pattern.

### Compile failure due to missing figures (pre-existing)

When `tectonic` errors with "Unable to load picture or PDF file" for an `\includegraphics` reference,
the referenced figure file wasn't committed. This is NOT a PII issue — it's a pre-existing template gap.

**Verify it's pre-existing** before assuming your PII changes caused it:

```bash
cd <workdir> && git stash && docker run ... tectonic -X compile main.tex; git stash pop
```

If the same error occurs on the original code, it's pre-existing — note it and push anyway.
If the error only occurs after your changes, one of your replacements broke a reference — undo and retry.

**Fix:** create a 1x1 transparent PNG placeholder (same Python snippet as QR/signature section above)
in the expected location. If the reference is to a `.pdf` file, create a `.png` instead and update
the `.tex` reference from `.pdf` → `.png`. Example: replace `figures/smokeblk.pdf` with `figures/smokeblk.png`
in the `.tex`, then create `figures/smokeblk.png` via the Python placeholder snippet.

Only do this for clearly non-PII instructional figures (diagrams, charts, example images).
Do NOT create placeholders for signature images, QR codes, or personal portrait references —
those should go through the normal QR/signature replacement workflow with the 1x1 PNG + reference update.

### Beamer `\author{姓名}` PII in main.tex

Beamer templates commonly have `\author{}`, `\institute{}`, `\title{}` in the main.tex preamble. Scan for Chinese names in `\author{}` — not just in AGENTS.md or .cls headers. PII example: `\author{羊忱}` → `\author{张三}`. Also check `\institute{四川大学公共卫生学院}` — the institute name itself is institutional, so preserve it; only the author name is PII.

### Missing main.tex/references.bib — symlink adaptation

When a repo has `template.tex` instead of `main.tex` and `bib/template.bib` instead of `references.bib`, create symlinks before compiling:

```bash
ln -sf template.tex main.tex
ln -sf bib/template.bib references.bib
```

Symlinks are preferred over copies — changes to the source file propagate. Git tracks symlinks correctly. Note: if `template.tex` uses `\bibliography{bib/template}`, the relative path still resolves through the symlink.

### Font adaptation via cls `overleaf` option (Fandol font swap)

Some cls files have a conditional `\if...overleaffonts` block that uses Fandol fonts (available in Docker/tectonic bundle) instead of SimSun/SimHei/SimFang (requires local fonts/ directory). When compilation fails with "font not found" for SimSun, check if the cls supports an `overleaf` class option:

```latex
% Before:
\documentclass[AutoFakeBold]{LZUThesis_xb}
% After — activates Fandol branch:
\documentclass[overleaf,AutoFakeBold]{LZUThesis_xb}
```

This pattern applies to any template cls that has an `overleaf` option or `\if...overleaffonts` conditional. Look for `\DeclareOption{overleaf}` near the top of the cls.

The phone number pattern `[0-9]{11}` matches 13-digit ISBNs (e.g., `9780763714970`).
Treat any 11+ digit number starting with `978` or `979` as an ISBN false positive — do NOT scrub.
Verify context: if the containing line has `isbn` or `ISBN`, it's definitively bibliographic.

### License-required attribution links (CC BY) must be preserved

Some templates carry CC BY 4.0 attribution to upstream GitHub repos (e.g., `andy123t/Thesis-Slides`).
These are NOT personal PII — they are required by the template's license. **Preserve** them.
Only scrub GitHub links that are personal portfolio/contact links (e.g., `github.com/joelsleeba`),
NOT attribution/credit links from the template's origin.

### English names replaced with Chinese in English-only templates cause font warnings

When scrubbing English names like "Joel Sleeba" to Chinese like "模板维护者", English-only templates
(using Latin Modern font) will produce "Missing character" warnings for CJK glyphs.
This does NOT break compilation but clutters the log.
**In English-only templates, prefer English fake names like "Tom Smith" over Chinese text.**
Reserve Chinese replacement text for templates that already use Chinese content.

### Replacing the last PII match in an English-only template

When the only Chinese replacement is in a copyright line (e.g., `\copyright 模板维护者`),
the warnings are harmless and can be ignored. The compile still succeeds.

### Underscores in LaTeX replacement text cause "Missing $ inserted"

LaTeX treats `_` as a math-mode subscript marker. Never use underscores in replacement
names inside `.tex` files — use hyphens (`-`) instead. Example:
- WRONG: `example_user` → compile fails with "Missing $ inserted"
- RIGHT: `example-user` → compiles fine

### Acknowledgment files are PII-dense (forum usernames, mailto links)

`ack.tex` or acknowledgment chapters often carry the densest PII clusters:
- Forum usernames with `@` prefix (`@Sagittarius Rover`, `@赣医一附院神经内科黄旭华`)
- `\href{mailto:real@email.com}` wrapped emails in footnotes
- Chinese real names mixed into footnote acknowledgments
- Personal identity tags (`生物工程2201` class/year identifiers)

When scrubbing `@username` references: if the username or surrounding text contains
real names, replace both the username and display text with generic placeholders
(e.g., `@论坛用户1`, `@论坛用户2`). Preserve `@` references that are purely GitHub
attributions to public template repos (e.g., `@tzaiyang`, `@hushidong`).

### Chinese platform personal links (CSDN, Bilibili)

Add these to the personal-link scrub list:
- `blog.csdn.net/<user ID>` — CSDN personal blog articles
- `bilibili.com/video/<BV...>` — personal Bilibili tutorial links with tracking params
- `zhihu.com/people/` — already covered; also check `zhihu.com/column/`

### Delete stale work dirs before cloning

```bash
rm -rf /tmp/<repo>-work
```
Otherwise leftover files from prior scrubs can contaminate the scan.

### ElegantLaTeX family repos share identical PII

The ElegantPaper template family (elegantpaper, elegantpaper-custom, elegantpaper-template) all
carry the same PII because they derive from a single upstream source:

- `elegantpaper.cls` header: `% Author: Dongsheng Deng & Ran Wang` + `% Email: ranwang.osbert@outlook.com`
- `references.bib`: 4 real Chinese author name entries (方军雄, 刘凤良/章潇萌/于泽, 吕捷/王高望, Li Qiang/Chen Liwen/Zeng Yong)
- `main.tex`: Gitee mirror link (elegantpaper + elegantpaper-custom only; template variant already stripped)

When you find PII in one ElegantLaTeX repo, check the siblings — they will have the same.
Scrub them identically: .cls header → "模板维护者" + example@example.com, bib authors → placeholders,
Gitee link → remove.

See `references/elegantlatex-family-pii.md` for the exact sed commands and PII locations.

### Cross-file email repetition (gxu-thesis pattern)

Some template authors include their personal email in every file header as a "signature."
Example from gxu-thesis: `junhaowu_hit@163.com` appeared in 6 files — gxuthesis.cls, gxufrontmatter.tex,
main.tex, 论文内容/第5章.tex (as `\href{mailto:...}`), README.md, and two third-party bundled
package files (gb7714-2025.cbx, gb7714-2025.bbx).

**Strategy**: use grep to find every occurrence across all files, then scrub with sed targeting all
files at once. One scan hit doesn't mean one fix — count the matches and confirm zero via grep after.

Also: bundled third-party `.cbx`/`.bbx` files (like gb7714-2025) from upstream package authors
(e.g., hushidong) often carry the upstream maintainer's email (`hzzmail@163.com`). Scrub these too —
they're still PII in the template distribution context.

### 闲鱼 (Xianyu) selling references

Some template authors use the template header to advertise personal marketplace services:
```
%% 欢迎闲鱼找「薛定谔之花_」下单
```
These are personal commercial solicitations — remove the entire line. Scan for `闲鱼` alongside
other Chinese platform keywords.

### Duplicate bib files in different directories

Some repos ship copies of the same `.bib` file in multiple directories (e.g., `references.bib` at root and `reference/refs.bib`). Scrub BOTH — they typically have identical content and must stay in sync.

### demo.tex mirrors main.tex PII

Some templates ship a `demo.tex` alongside `main.tex` with near-identical `\whusetup{info={...}}` or similar config blocks. Scan and scrub `demo.tex` with the same rigor as `main.tex` — all author names, emails, and contact info that appear in one often appear in both.

### Maintainer lists in .cls/.sty headers

Class and style file headers often list multiple maintainers with `Name <email>` on separate lines:
```
%% The Current Maintainers of this work are
%%   Siyu Wu <2401336502@qq.com>
%%   Kangwei Xia <kangweixia_xdyy@163.com>
```
Replace all names with English fake names and all emails with `example@example.com`. Also scan the same repo's `.dtx` file for mirrored maintainer info — `.dtx` files often contain the same PII blocks as their derived `.cls`.

## Batch processing

When processing multiple repos (e.g., 8), work sequentially:
1. Clone and process one repo completely (scan → replace → compile → push)
2. Move to the next
3. Track progress — report summary after each repo

Don't clone all repos at once to save disk space in `/tmp`.

When processing consecutive batches, check if repos from prior sessions still exist in `/tmp/<repo>-work` before cloning. Use `ls -d /tmp/<repo>-work` to check. If present, `git pull origin main` to sync instead of re-cloning. This avoids redundant clone operations when working across multiple sessions.

## PII hotspot locations (order of likelihood)

1. **ack.tex / acknowledgment chapters** — densest PII: forum `@username` references with real names, `\href{mailto:...}` emails in footnotes, QQ/WeChat contact info, personal identity markers. Scan aggressively and read full file context.
2. **README.md** — BibTeX citation examples often carry real author names, emails, GitHub profiles, QQ/WeChat numbers. Scan aggressively. Also check HTML `<a href="mailto:...">` links in contact sections.
3. **LICENSE** — Copyright lines often carry the original author's GitHub username or real name. Pattern: `Copyright (c) YYYY <GitHubUser>`. Replace with `iftaken`.
4. **.cls / .sty copyright headers** — `% Copyright (C) YYYY by NAME <email>` pattern is common. Also check for multi-line maintainer lists with name+email combos. Always scan class/style files.
5. **.dtx documentation files** — `.dtx` files are the literate source for `.cls`/`.sty` files. They often contain the same PII as their derived class files AND additional personal acknowledgments (e.g., `向fduthesis的作者曾祥东先生表示感谢`). Always scan `.dtx` files — they're not in the default compile path but are part of the repo. Replace personal names with fake names.
5. **Hex-encoded donation sections in .cls/.sty** — xduts-derived templates have ~58-line commented-out sections with hex-encoded emails (`\str_set_convert:Nnnn ... 6e6f746532383640666f786d61696c2e636f6d`) and payment QR URLs. Scan for `\str_set_convert`, `\alipayqr`, `\wxpqr`, `\qqqr`. Remove the entire block (from `\changes{...赞助二维码}` to `\end{figure}`).
6. **Cross-file duplicate PII blocks** — when a template has multiple `.cls`/`.sty` files, they often contain IDENTICAL PII blocks. Always scan ALL class/style files; don't stop after finding PII in one.
7. **main.tex comments and acknowledgements** — Chinese comments like `% 20230537华晓蔚` or `\textbf{XurongLiu}` in thanks sections.
8. **AGENTS.md author/source fields** — `- **作者**：realName` or `- **原始来源**：personal/repo`. Also check cross-references between related repos for "同作者" (same author) mentions.
9. **references.bib first entry** — often a self-citation by the template author.
10. **Beamer `\\titlegraphic` in tutorial/demo slides** — `\\titlegraphic{\\includegraphics{head.png}}` often points to a personal portrait (400KB+ PNG). Check file size; replace with 1x1 transparent PNG if >50KB.
11. **Credits.md files** — some templates ship a `Credits.md` with upstream project attributions that include personal maintainer emails (e.g., `hzzmail@163.com`, `huangrui.mo@gmail.com`) and real names. These are distinct from README.md and easily missed. Always grep for emails/names in `Credits.md` when present.

12. **zhihu.md files** — some template repos include the full Zhihu (知乎) article text used to promote the template. These files are dense with personal PII: GitHub Pages URLs (author's academic site), personal GitHub repo links in `[text](url)` markdown format, and author attribution mentions. Scan aggressively — replace all personal GitHub orgs/handles with `iftaken` in URLs and scrub personal site links.

13. **Single-file CV/résumé templates** — all PII is concentrated in `main.tex` with no subdirectories. CVs pack name (often with English romanization: `黄客家 (Hakka Huang)`), phone, edu email, QQ email, GitHub profile, and personal website into a single TeX file. Commented-out TikZ blocks in footer bars often carry REAL contact info (not example data). Scan with the same patterns but expect everything in one file — no need to search subdirectories.

## Link handling policy

- **Personal GitHub repos** → repoint to `iftaken/<repo>` when a mirror exists, otherwise `example/template`.
- **Gitee links** → strip entirely. iftaken has no Gitee presence.
- **QQ group numbers** → always remove. Personal contact infrastructure, not product-defining.
- **CSDN blog links / Bilibili video links** → strip or replace with generic text. Personal content platforms.
- **Public template origins** (e.g., `muzimuzhi/jssms-template` in source attribution) → preserve. Product-defining.
- **Overleaf/TeXPage template URLs** → preserve. Public resource links.

## Placeholder repos

Many repos in this pipeline are "source files pending extraction from TeXPage." They contain minimal main.tex
placeholders. Still compile with Docker to regenerate main.pdf and push — even if no PII was found. Use commit
message `"scrub: no PII found, regenerate main.pdf"`.
