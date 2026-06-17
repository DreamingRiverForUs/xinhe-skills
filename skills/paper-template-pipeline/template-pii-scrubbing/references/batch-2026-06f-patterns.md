# Batch 2026-06f PII Patterns (shnu-thesis-template through southwest-forestry-university-thesis)

8 repos processed. 2 empty repos skipped (shumo-cup-2025, sjtu-thesis). 6 repos completed, 4 had PII.

## Pattern summary

| Repo | PII type | Location | Replacement |
|------|----------|----------|-------------|
| shnu-thesis-template | Chinese author names in bib | references.bib, data/bibliography.tex | 李荣华/刘播→张三/李四, LiLiu1997→ZhangLi1997 |
| shuweibei-2025 | Org email in comment | main.tex L12 | latexstudio@qq.com→template@example.com |
| shuweibei-2025 | WeChat QR image (missing file) | main.tex L48 gongzhonghao-n | Created 1x1 PNG placeholder, updated ref to .png |
| sjtu-beamer | 4 contributor emails | src/doc/sjtubeamerdevguide.tex L1317-1320 | All→example@example.com |
| sjtu-beamer | Real author name | main.tex L121 \author{Alexara Wu} | →\author{Tom Smith} |
| sjtu-beamer | Bib entries with real Chinese names | references.bib | 江泽民→张三, 罗伯特/劳伦斯/库恩→李四/王五/赵六 |
| sjtu-beamer | Personal portrait (head.png) | src/support/tutorial/head.png (401KB, 573x376) | Replaced with 1x1 transparent PNG |
| snut-thesis | Real author name + pinyin | ustcsetup.tex L7-8 | 李泽平→张三, Li Zeping→Zhang San |
| snut-thesis | 28 Chinese author names in bib | references.bib | Bulk sed replace to fake names |

## New PII vector: beamer \titlegraphic portraits

`sjtu-beamer` had `head.png` (401KB RGB PNG) used as `\titlegraphic{\includegraphics{head.png}}` in a tutorial step. These are personal headshots uploaded by the template author for demo slides. Scan for `\titlegraphic` in beamer templates the same way you scan for `\includegraphics`.

## New PII vector: WeChat public account QR ("公众号" images)

`shuweibei-2025` had `gongzhonghao-n` — "gongzhonghao" = 公众号 = WeChat Official Account. The image file was already missing from the repo (likely in .gitignore), but the .tex reference remained. Pattern: Chinese pinyin filenames containing "gongzhonghao", "erweima" (二维码), or "qrcode".

## Clean repos (no PII found)

- **sht-template**: All author names already placeholders (作者A, 作者B, 第一作者), email already author@example.com
- **southwest-forestry-university-thesis**: Placeholder repo, source pending TeXPage extraction, author field already "(源文件待从 TeXPage 提取)"
