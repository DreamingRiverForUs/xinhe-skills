# HKUST Thesis Template (hkust-thesis)

## Source

- **Upstream**: `HKFoggyU/hkust-thesis`
- **Format**: dtx/docstrip (LaTeX3)
- **Type**: PhD/MPhil thesis, English-only
- **TeXPage**: https://www.texpage.com/template/373737be-dc33-4df2-a7d0-a512a92715ef

## Pre-built cls

The GitHub release (`hkust-thesis-v*.zip`) contains a pre-built `hkustthesis.cls` (26KB). Use this directly — no need to extract from dtx.

```bash
curl -sL 'https://api.github.com/repos/HKFoggyU/hkust-thesis/releases/latest' | \
  python3 -c "import sys,json; r=json.load(sys.stdin); a=[x for x in r['assets'] if x['name'].endswith('.zip')]; print(a[0]['browser_download_url'] if a else '')" \
  | xargs curl -sLo /tmp/hkust-release.zip
unzip -o /tmp/hkust-release.zip hkustthesis.cls
```

## Font Strategy

**No Chinese fonts needed.** HKUST is English-medium; the template only sets Latin fonts.

Auto-detection in the cls:
1. `\sys_if_platform_windows:TF` → Windows fontset (Times New Roman, Arial, Courier New)
2. `\file_if_exist:nTF { /System/Library/Fonts/Menlo.ttc }` → macOS fontset (TNR + smcp hack, Arial, Menlo)
3. Fallback → **gyre** (TeX Gyre Termes, Heros, Cursor via `Extension=.otf`)

In tectonic's Docker (Linux), detection hits the gyre fallback. TeX Gyre OTF fonts are available in tectonic's bundles — no download needed.

## Compilation

```bash
tectonic -X compile main.tex
```

- Uses `biblatex` + `biber`. Tectonic handles biber automatically via `/usr/local/bin/tectonic-biber` — **no setup needed**.
- `unicode-math` with XITSMath + latinmodern-math — both in tectonic bundles.
- First compilation downloads ~6 extra packages (mhchem, physics, thmtools, wrapfig, blindtext, ieee.bbx).
- 3-pass compilation: TeX → biber → TeX → TeX → xdvipdfmx. Output ~73KB.

## Non-issues

The following warnings are safe and do not need fixing:
- `algorithm.sty:11: Invalid UTF-8 byte` — legacy encoding in algorithmicx comments
- `algorithmic.sty:11: Invalid UTF-8 byte` — same
- `Underfull \hbox` / `Overfull \hbox` — example chapter has intentional wide text

## File Mapping

| Original | Adapted |
|----------|---------|
| `mythesis.tex` | `main.tex` |
| `mythesis.bib` | `references.bib` |
| `mythesis_LoP.bib` | `mythesis_LoP.bib` (kept — List of Publications) |
| `hkustthesis.cls` | `hkustthesis.cls` (kept) |
| `chapters/*.tex` | `chapters/*.tex` (kept) |

## init.sh

Minimal — creates `font/` directory only. No font downloads needed.
