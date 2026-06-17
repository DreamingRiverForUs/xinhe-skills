# PII Scrubbing for Non-Official LaTeX Templates

When processing user-created LaTeX templates for 心河Paper, scrub all personal identifiable information before deployment.

## Context

- Official publisher templates (Elsevier, Springer, IEEE, ACM, MDPI, etc.): **SKIP scrubbing** — only compile-verify
- Non-official templates (university theses, MCM, beamer, resumes, books): **MUST scrub**

## Search Patterns

Run these grep searches on `.tex`, `.cls`, `.sty`, `.bib`, `.md`, `.cfg`, `.def` files:

```bash
# Chinese names in author/contact fields
grep -rn '作者\|联系人\|指导老师' *.tex *.cls

# English names
grep -rn '\\author{\|\\thanks{\|Author:' *.tex *.cls

# Phone numbers
grep -rnE '[0-9]{11}' *.tex *.cls *.md

# Email addresses
grep -rnE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' *.tex *.cls *.md

# QQ/WeChat
grep -rniE '(qq|wechat|微信|扣扣)[:：]?\s*[0-9]{5,}' *.tex *.cls *.md

# QR code references
grep -rniE '(qr|二维码|扫码|加微信|加群)' *.tex *.cls *.md

# Personal GitHub/social links in comments
grep -rniE 'github\.com/[^/]+/|zhihu|blog\.|个人主页|CSDN|Bilibili' *.tex *.cls *.md

# Developer attribution in cls headers
grep -rn '作者\|原作者\|维护者\|author\|maintainer' *.cls *.sty
```

## Replacement Rules

| PII Type | Replace With |
|----------|-------------|
| Chinese names (authors, mentors, contacts) | 张三, 李四, 王五, 赵六 (rotate) |
| English names | Tom Smith, Jerry Johnson, King Williams, Mary Brown |
| Student IDs | 000000000000 |
| Emails | example@example.com |
| Phone numbers | 13800138000 |
| QQ/WeChat IDs | Remove line entirely |
| QR code images | 1×1 transparent PNG placeholder |
| Personal GitHub links | Remove or repoint to `iftaken` |
| Developer names in cls | 模板维护者 |
| bib author names | 张三, 李四, 王五, 赵六 (rotate) |
| Personal blog/CSDN/Bilibili links | Remove line entirely |
| Donation/payment QR codes | Replace with 1×1 transparent PNG |

## DO NOT Change

- University names in template titles (these ARE the product)
- LaTeX package names and versions
- File paths and directory structure
- University logos and official seals
- cls/sty technical structure

## 1×1 Transparent PNG

```bash
python3 -c "
import struct, zlib
w, h = 1, 1
raw = b''.join([b'\x00\xff\xff\xff\xff' * w for _ in range(h)])
ihdr = struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)
crc = lambda d: struct.pack('>I', zlib.crc32(d) & 0xffffffff)
png = b'\x89PNG\r\n\x1a\n' + b'IHDR' + ihdr + crc(b'IHDR' + ihdr) + b'IDAT' + zlib.compress(raw) + crc(b'IDAT' + zlib.compress(raw)) + b'IEND' + crc(b'IEND')
open('placeholder.png', 'wb').write(png)
"
```

## Scale

Typical PII found per template:
- 2-5 author/developer names
- 1-3 emails
- 0-2 phone numbers
- 0-2 QQ/WeChat contacts
- 0-2 QR code images
- 10-30 bib author names
- 1-5 personal GitHub/social links

Total across 125 templates (2026-06 session): 500+ names, 70+ emails, 30+ phones, 50+ social contacts removed.
