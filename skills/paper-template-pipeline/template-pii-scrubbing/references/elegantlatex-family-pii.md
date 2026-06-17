# ElegantLaTeX Family PII (elegantpaper, elegantpaper-custom, elegantpaper-template)

All three repos share identical PII from the upstream ElegantLaTeX/ElegantPaper source.
Scrub identically.

## elegantpaper.cls (lines 1-3)

```
% Author: Dongsheng Deng & Ran Wang    →  % Author: 模板维护者
% Email: ranwang.osbert@outlook.com    →  % Email: example@example.com
% Lastest Version: https://github.com/ElegantLaTeX/ElegantPaper  → PRESERVE (public origin)
```

## references.bib

| Key | Old author | New author | New key |
|-----|-----------|-----------|---------|
| en3 | Li, Qiang and Chen, Liwen and Zeng, Yong | Smith, Tom and Doe, Jane and Brown, John | (unchanged) |
| cn1 | 方军雄 | 张三 | zhang1 san1 |
| cn2 | 刘凤良 and 章潇萌 and 于泽 | 李四 and 王五 and 赵六 | li3 si4 wang2 wu3 zhao4 liu4 |
| cn3 | 吕捷 and 王高望 | 孙七 and 周八 | sun1 qi1 zhou1 ba1 |

Foreign authors (Carlstrom, Quadrini) — leave unchanged.

## main.tex (elegantpaper + elegantpaper-custom only, NOT elegantpaper-template)

Line ~43: Gitee mirror link. Remove the clause after `用户可以在线使用。`:
```
另外，为了方便国内用户，模板也已经传至\href{https://gitee.com/ElegantLaTeX/ElegantPaper}{码云}。
```
→ delete. The Overleaf link stays.

Elegantpaper-template does NOT have this Gitee link — it was already stripped.

## Sed commands (apply from workdir)

```bash
# CLS header
sed -i '' 's/% Author: Dongsheng Deng \& Ran Wang/% Author: 模板维护者/' elegantpaper.cls
sed -i '' 's/% Email: ranwang.osbert@outlook.com/% Email: example@example.com/' elegantpaper.cls

# References
sed -i '' 's/author={Li, Qiang and Chen, Liwen and Zeng, Yong}/author={Smith, Tom and Doe, Jane and Brown, John}/' references.bib
sed -i '' 's/author = {方军雄}/author = {张三}/' references.bib
sed -i '' 's/author = {刘凤良 and 章潇萌 and 于泽}/author = {李四 and 王五 and 赵六}/' references.bib
sed -i '' 's/author = {吕捷 and 王高望}/author = {孙七 and 周八}/' references.bib
sed -i '' 's/key = {fang1 jun1 xiong2}/key = {zhang1 san1}/' references.bib
sed -i '' 's/key = {liu2 feng4 liang2 zhang1 xiao1 meng2 yu2 ze2}/key = {li3 si4 wang2 wu3 zhao4 liu4}/' references.bib
sed -i '' 's/key = {lv3 jie2 wang2 gao1 wang4}/key = {sun1 qi1 zhou1 ba1}/' references.bib

# Gitee link (elegantpaper + elegantpaper-custom only)
# Use patch tool — sed with \href gets blocked
```
