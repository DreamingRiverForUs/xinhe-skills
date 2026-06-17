# Batch G — July 2026 (iftaken batch 15+16)

Repos processed in this batch, all under `github.com/iftaken/`:

| # | Repo | PII Type | Details |
|---|------|----------|---------|
| 1 | xdu-graduate-thesis | GitHub username | `note286` in main.tex comment |
| 2 | xdu-thesis | GitHub username + email + QR codes | `note286` in 3 locations (main.tex), hex-encoded `note286@foxmail.com`, alipay/WeChat/QQ QR codes in xdupgthesis.cls + xdufont.sty donation sections |
| 3 | xynu-beamer | None | Placeholder template, clean |
| 4 | xynu-thesis | None | Placeholder template, clean |
| 5 | xynu-year-paper | GitHub username + real name | `kelasike1216` (LiKunfeng) in main.tex + AGENTS.md |
| 6 | ynu-thesis | Real name | 赵苡积 (Dr. Zhao Yiji) in 6 files: main.tex, ynu-thesis.cls, YNU-Thesis-本科.tex, YNU-Thesis-硕博.tex, README.md, AGENTS.md. Also `yijizhao` GitHub handle in AGENTS.md |

## Notable patterns discovered

### Hex-encoded PII in donation/sponsorship sections

xduts-derived templates (xdu-thesis, xdu-graduate-thesis) contain ~58-line commented-out donation sections
in their `.cls` and `.sty` files. These sections include:

- Hex-encoded email: `6e6f746532383640666f786d61696c2e636f6d` decodes to `note286@foxmail.com`
- Hex-encoded Alipay QR URLs
- Hex-encoded WeChat Pay QR URLs
- Hex-encoded QQ Pay QR URLs with personal tracking parameters

**Scan for**: `\str_set_convert:Nnnn` blocks with long hex strings, QR-related commands (`\alipayqr`, `\wxpqr`, `\qqqr`),
and `\emailaddress` definitions. These are always commented out with `%` but still contain real payment links.

**Remediation**: Replace the entire block (~58 lines spanning from `\changes{...}{赞助二维码}` to `\end{figure}`)
with a single comment: `% 赞助二维码部分已移除 (PII scrubbed)`.

### Cross-file duplicate PII blocks

When a template has multiple `.cls` / `.sty` files (e.g., xdupgthesis.cls AND xdufont.sty),
they often contain IDENTICAL PII blocks. The same hex-encoded donation section appeared in both files
verbatim. Always scan ALL class/style files — don't stop after finding PII in one.

### AGENTS.md metadata as PII vector

The 心河Paper pipeline adds AGENTS.md files with upstream author tracking:
```
- **上游作者**：kelasike1216（LiKunfeng）
- **原始仓库**：yijizhao/YNU-Thesis-Latex
```

These are metadata, not template content, but they contain real names and personal GitHub handles.
Always scan AGENTS.md alongside README.md for author PII.

### Placeholder repos dominate xynu-* series

xynu-beamer, xynu-thesis are placeholder shells awaiting source extraction from TeXPage.
They contain deliberate placeholder text (作者姓名, 模板维护者) and no real PII.
Skip quickly — scan, note "clean", and move on. Don't waste compile cycles on clearly empty templates.

### Pre-existing compile failure verification

When the Docker compile fails after PII changes:

1. `git stash` the changes
2. Re-compile the original
3. If same error → pre-existing, not caused by PII scrubbing
4. `git stash pop` to restore changes
5. Note it in the summary and push anyway

Example: ynu-thesis failed with "Unable to load picture or PDF file figures/ch2/figure1.pdf"
both before and after PII changes — the `figures/` directory was `.gitignore`'d and never committed.
