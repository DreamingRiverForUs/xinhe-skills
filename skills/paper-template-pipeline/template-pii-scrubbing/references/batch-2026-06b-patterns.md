# PII Patterns Discovered (June 2026 Batch B — 8 iftaken LaTeX Template Repos)

Second batch of repos processed for PII scrubbing. These are all iftaken/* repos in the paper-template-pipeline.

## Repository: dbss-mcm-2026-template (东北三省数学建模竞赛)

| Pattern | Location | Action |
|---------|----------|--------|
| `JL <yhlaozero2@163.com>` | main.cls copyright | → "Template Maintainer <example@example.com>" |
| `12377778900`, `13477778900`, `14577778900` | main.tex phone numbers | → "13800138000" |
| same phone numbers | AGENTS.md documentation | → "13800138000" |
| `https://github.com/zepinglee/gbt7714-bibtex-style` | gbt7714-numerical.bst comment | Line removed |

## Repository: dlmu-bachelor-thesis (大连海事大学本科论文)

| Pattern | Location | Action |
|---------|----------|--------|
| `JL <yhlaozero2@163.com>` | dlmubachelorthesis.cls copyright | → "Template Maintainer <example@example.com>" |
| `JL, yhlaozero2@163.com` | README.md header | → "Template Maintainer, example@example.com" |
| `\aauthor{海哥}` | main.tex, main_STEM.tex, main_humanities.tex | → `\aauthor{张三}` |
| `\mentorONE{海老}` | main.tex, main_STEM.tex, main_humanities.tex | → `\mentorONE{李四}` |
| `\definechangesauthor[name={海哥}]`, `[name={海老}]` | main_STEM.tex, main_humanities.tex | → 张三, 李四 |
| `付梦印, 邓志红, 张继伟, 邓宇, 张爱茜, 陈日清, 魏东斌, 王连生` | references.bib, refs/refs_STEM.bib | → 张三, 李四, 王五, 赵六 |
| `童星, 郑功成, 陈洁` | refs/refs_humanities.bib | → 张三, 李四, 王五 |
| `Hank Lo (JohnsonLo00)` | AGENTS.md author | → "模板维护者" |
| Multiple `github.com/JohnsonLo00/` links | README.md | → `iftaken/dlmu-bachelor-thesis` |
| `https://github.com/zepinglee/gbt7714-bibtex-style` | thuthesis-bachelor.bst | Line removed |

## Repository: dlmu-thesis (大连海事大学学位论文)

| Pattern | Location | Action |
|---------|----------|--------|
| `JL <yhlaozero2@163.com>` | dlmuthesis.cls copyright | → "Template Maintainer <example@example.com>" |
| `Hank Lo, yhlaozero2@163.com` | README.md header | → "Template Maintainer, example@example.com" |
| `QQ交流群：976053605` | README.md | Line removed entirely |
| `\aauthor{阿海}` | main.tex | → `\aauthor{张三}` |
| `\mentorONE{海老师（教授）}` | main.tex | → `\mentorONE{李四（教授）}` |
| `signatures/阿海.png`, `signatures/海老师.png` | main.tex signature images | → `signatures/placeholder.png` (1x1 transparent PNG created) |
| `付梦印, 邓志红, 张继伟, 邓宇, 张爱茜, 陈日清, 魏东斌, 王连生` | references.bib | → 张三, 李四, 王五, 赵六 |
| `张旭明, 徐滨士, 董世运, 张中祥, 许崇祥, 燕卫江, 苏宇锋, 贾志刚` | references.bib, refs/ref_MA.bib, refs/ref_DOC.bib | → fake names |
| Multiple `github.com/JohnsonLo00/` + gitee links | README.md | → `iftaken/dlmu-thesis` |
| `Hank Lo (JohnsonLo00)` | AGENTS.md | → "模板维护者" |

## Repository: ecnu-beamer (ECNU Math Beamer)

| Pattern | Location | Action |
|---------|----------|--------|
| `author@ecnu.edu.cn` | main.tex \author email | → "example@example.com" |
| `Author Name` | main.tex | → "Tom Smith" |
| `73Dsi` | main.cls comment, AGENTS.md | → removed / "模板维护者" |

Minimal PII — mostly already placeholders.

## Repository: elegantbook-custom (GorgeousBook)

| Pattern | Location | Action |
|---------|----------|--------|
| `雨霓同学 \& Azure1210` | main.tex \author | → "张三 & 模板维护者" |
| `\bioinfo{邮箱}{sx12101184@qq.com}` | main.tex | → `example@example.com` |
| `elegantlatex2e@gmail.com`, `sx12101184@qq.com` | main.cls copyright | → `example@example.com` |
| `github.com/Azure1210/elegantbook-magic-revision` | main.cls, cha/xuzhang.tex | → `iftaken/elegantbook-custom` |
| `colin-young@live.com` + hatenablog URL | cha/xuzhang.tex | → email removed, blog URL removed |
| `Azurekite & 雨霓同学 & 1210` | cha/xuzhang.tex | → "模板维护者 & 张三" |
| `QQ:910014191`, `WeChat:雨霓同学` | cha/zhixie.tex | **Entire zhixie.tex rewritten** |
| `QQ群:754044950`, `Weibo:5713129191` | cha/zhixie.tex | Removed with entire file rewrite |
| `github.com/Azure1210/`, `cnblogs.com/1210x1184/` | cha/zhixie.tex | Removed |
| `azurekite.cn`, `space.bilibili.com/44523572` | cha/zhixie.tex | Removed |
| `wxpng2.png`, `zfbpng.png` | figure/ QR code donation images | → 1x1 transparent PNG placeholders |
| Donation acknowledgment table (names + amounts) | cha/zhixie.tex | Removed with file rewrite |

**Note:** zhixie.tex was a personal donation/social media contact page with WeChat/Alipay QR codes,
QQ numbers, Weibo, Bilibili, personal blog, personal website. Entire file replaced with simple acknowledgment.
Compile failed due to pre-existing missing font (CMU Typewriter Text) — not caused by PII edits.

## Repos not yet started
- elegantpaper
- elegantpaper-custom
- elegantpaper-template

## False Positives (verified safe)

| Pattern | Reason safe |
|---------|-------------|
| `ElegantLaTeX` organization GitHub links | Public open-source org, not personal |
| `East China Normal University` | Product-defining university identity |
| `大连海事大学` | Product-defining university identity |
| `东北三省数学建模竞赛` | Product-defining competition name |
| latexstudio.net URLs | Public community site |
| `Stauffer, Chris; Grimson, W Eric L` | Foreign citation authors — already public |
| `zepinglee/gbt7714-bibtex-style` copyright | Public project attribution (email is obfuscated with "AT") |
| University logos (ECNU, DLMU) | Institutional assets |
