#!/usr/bin/env python3
"""Extract files from a docstrip .dtx file without needing a TeX installation.

Docstrip semantics implemented:
  - %<*tag1|tag2>        → starts a guard block (only those tags active)
  - %</tag1|tag2>        → ends the guard block
  - %<tag1|tag2>rest     → line belongs to tag1/tag2 REGARDLESS of active guard
  - %<!tag>rest          → line does NOT belong to tag (goes to everything else)
  - no prefix            → belongs to currently active guard(s); if none active, to ALL outputs

USAGE:
    python3 extract_dtx.py njuthesis.dtx

Edit the output_map dict in main() to change which tags get extracted and to where.
"""
import re
import sys

def extract_dtx(dtx_path, output_map):
    with open(dtx_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    outputs = {tag: [] for tag in output_map}
    active_guards = set()

    for line in lines:
        # Guard start: %<*tag1|tag2>
        m = re.match(r'%<\*(.+?)>\s*$', line)
        if m:
            active_guards = set(m.group(1).split('|'))
            continue

        # Guard end: %</tag1|tag2>
        m = re.match(r'%<\/(.+?)>\s*$', line)
        if m:
            active_guards = set()
            continue

        # Single-line guard: %<tag1|tag2>rest  or  %<!tag>rest
        m = re.match(r'%<(.+?)>(.*)', line)
        if m:
            guard_expr = m.group(1)
            rest = m.group(2) + '\n'  # regex .* doesn't capture \n
            # Handle negation: %<!tag>
            neg_match = re.match(r'!(.+)', guard_expr)
            if neg_match:
                neg_tags = set(neg_match.group(1).split('|'))
                for tag in output_map:
                    if tag not in neg_tags:
                        outputs[tag].append(rest)
            else:
                guard_tags = set(guard_expr.split('|'))
                for tag in guard_tags:
                    if tag in output_map:
                        outputs[tag].append(rest)
            continue

        # Line without any %<...> guard prefix
        if active_guards:
            for tag in active_guards:
                if tag in output_map:
                    outputs[tag].append(line)
        else:
            for tag in output_map:
                outputs[tag].append(line)

    for tag, out_lines in outputs.items():
        outpath = output_map[tag]
        content = ''.join(out_lines)
        with open(outpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Wrote {len(out_lines)} lines to {outpath}")

if __name__ == '__main__':
    dtx = sys.argv[1] if len(sys.argv) > 1 else 'njuthesis.dtx'
    output_map = {
        'class': 'njuthesis.cls',
        'def-u': 'njuthesis-undergraduate.def',
        'def-g': 'njuthesis-graduate.def',
        'def-p': 'njuthesis-postdoctoral.def',
        'doc-cls': 'njuthesis-doc.cls',
    }
    extract_dtx(dtx, output_map)
