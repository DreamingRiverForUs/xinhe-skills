# Batch D — June 14, 2026
# Repos: gxu-thesis-template, heu-beamer (empty), hhu-thesis, hitsz-thesis, hkust-thesis, hnu-thesis, huizhou-cs-thesis (stub), huizhou-cv (TBD)

## New PII patterns discovered

### 1. 闲鱼 (Xianyu) marketplace contact strings
Chinese templates sometimes carry commercial contact info — seller names and storefront references on Xianyu (闲鱼):
```
%% 欢迎闲鱼找「薛定谔之花_」下单
\bicaption{闲鱼「薛定谔之花_」\LaTeX 排版服务}{...}
\fignote{如有疑问，欢迎闲鱼联系模板作者...}
```
Pattern: `(?i)(闲鱼|xianyu|咸鱼)`
Action: remove the full comment/line/caption. Contact detail → generic ("LaTeX 排版服务" or remove caption text).

### 2. Promo/QR images inside chapter tex files
PII images are not limited to signatures in class files — promo images can appear in `\includegraphics` within
chapter tex files, e.g.:
```
\includegraphics[width=0.3\linewidth]{图/LaTeX排版服务.jpg}
```
These are promotional (likely QR or contact card images). Replace with 1x1 transparent PNG placeholder.

### 3. Personal signature images in main.tex
Some templates reference personal signatures that go on declaration/thesis-commitment pages:
```
\renewcommand{\statementauthor}{\includegraphics[height=2em]{签名/作者签名.png}}
\renewcommand{\statementsupervisor}{\includegraphics[height=2em]{签名/导师签名.png}}
```
These directories (`签名/`, `signatures/`) are personal. Replace the image files with 1x1 transparent PNGs.
The `\renewcommand` wrapper is LaTeX-tool infrastructure, not PII — keep it, just replace the image argument.

### 4. Dual emails on one line
Some contact headers list two emails separated by comma:
```
%%%% contact via <kisfg@hotmail.com, haikureimu@hnu.edu.cn>
```
Both must be replaced. Pattern `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` catches both individually
as separate matches, but awareness of dual-email lines helps with manual review.

### 5. Upstream GitHub usernames in AGENTS.md and main.tex comments
Most templates carry a reference to their upstream source:
```
| SOURCE_REPO | lazyshawn/hitszthesis_undergraduate |
%% 来源：TrisenYu/hnu_thesis_latex_template
%% https://github.com/HKFoggyU/hkust-thesis
```
Action: repoint to `iftaken/<repo-name>`.

### 6. Phone numbers in TeX \renewcommand infrastructure
Chinese thesis templates often define contact-info commands that take phone/email values:
```
\renewcommand{\statementphone}{13812345678}
\renewcommand{\statementemail}{xxx@st.gxu.edu.cn}
```
The phone: replace with `13800138000`. The email placeholder `xxx@st.gxu.edu.cn` is already anonymous — keep.
Also search for `\statementphone` specifically.

### 7. English name-only author headers in English templates
English-language templates (like hkust-thesis) may list real names:
```
%% Author: Shawn
%% Shawn's personal template.
```
Replace with "Tom Smith" or "模板维护者" depending on template language. In English-only templates
(no CJK content elsewhere), prefer English fake names to avoid font warnings.

## Repo-specific findings

### gxu-thesis-template (heavy PII)
- 3 files with Xianyu seller contact + email header comments (gxuthesis.cls, gxufrontmatter.tex, main.tex)
- 1 file with Xianyu caption and email in figure (论文内容/第5章.tex)
- 1 file with author name in body text (论文内容/第1章.tex)
- Phone number in main.tex
- 2 signature PNGs (签名/作者签名.png, 签名/导师签名.png)
- 1 promo JPG (图/LaTeX排版服务.jpg)
- README with real student name (王信哲) + KingwithQueen GitHub + personal emails
- AGENTS.md with upstream SchrodingerBlume/gxuthesis reference
- Font download needed: simfang.ttf, SIMLI.TTF via init.sh

### heu-beamer
- Empty repo. Nothing to scrub.

### hhu-thesis
- .cls header with Wei Zhilong + email
- README with email + Vitzron GitHub links + "By [Wei Zhilong]" footer
- AGENTS.md with Vitzron source reference
- Clean info.tex (all placeholder names)

### hitsz-thesis
- .cls header "Shawn's personal template" + file reference "texshawn.cls"
- main.tex "Author: Shawn" comment
- AGENTS.md with lazyshawn source references

### hkust-thesis
- main.tex with HKFoggyU GitHub URLs (2 occurrences)
- chapters/Ch_Introduction.tex with HKFoggyU releases link
- AGENTS.md with HKFoggyU upstream URL
- All author names already Evangelion-anime placeholders (Cruel Angel, Prof. Lilith, etc.) — intentional, not PII

### hnu-thesis
- format/setup.tex with dual-email contact line
- format/package.tex with same dual-email contact line
- main.tex with TrisenYu source comment
- AGENTS.md with TrisenYu source references

### huizhou-cs-thesis
- Stub/placeholder repo. Only main.tex exists. No PII found in initial scans.
- Still needs compile test to verify.

## Scan improvements for future batches

### Student ID detection
The phone-number scan `[0-9]{11}` catches 11-digit Chinese mobiles but misses 12-digit student IDs
(e.g., `123456789012` in tex/info.tex). Consider adding a separate student-ID scan:
```
search_files pattern='\\\\studentid\{[0-9]+\}'
search_files pattern='\\\\StudentID\{[0-9]+\}'
search_files pattern='(?i)student.?id.*[0-9]{10,}'
```
Student IDs that are clearly placeholders (like `123456789012`) can be left alone — only scrub when
paired with a real name or otherwise identifiable.

### Unicode-aware name scanning
For Chinese templates, add a broader name-hunt after the targeted email/author scans:
```
search_files pattern='(?i)(薛定谔|[\\u4e00-\\u9fff]{2,4}老师|[\\u4e00-\\u9fff]{2,4}同学)'
```
This catches honorifics with real names that might not be caught by targeted `\author{}` scans.

### Image directory listing
After `\includegraphics` scan, list actual image files to cross-reference:
```
search_files target=files glob='*.{jpg,png,gif,bmp}' path=<workdir>
```
This surfaces image files that exist on disk but might not be referenced in TeX source
(orphaned personal photos in the repo).
