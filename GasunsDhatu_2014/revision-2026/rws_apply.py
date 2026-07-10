# -*- coding: utf-8 -*-
"""H385 — apply rws_edits.jsonl to the source .mdx files.

Deterministic: for each edit, the exact `before` block must occur EXACTLY once
in its file; it is replaced by `after`. If any edit's `before` is missing or
ambiguous, nothing is written for that file and the conflict is reported, so a
partial/garbled apply can never land silently.

    python rws_apply.py            # apply
    python rws_apply.py --check    # report only, write nothing
Stdlib only.
"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\user\Documents\GitHub\SanskritGrammar-h385\GasunsDhatu_2014'
REV = BASE + r'\revision-2026'
CHECK = '--check' in sys.argv

def main():
    edits = [json.loads(l) for l in open(REV + r'\rws_edits.jsonl', encoding='utf-8') if l.strip()]
    byfile = {}
    for e in edits:
        byfile.setdefault(e['file'], []).append(e)
    total_ok = 0
    for fn, es in byfile.items():
        path = BASE + '\\' + fn
        text = open(path, encoding='utf-8').read()
        problems = []
        # verify all matches first (exactly once), then apply
        for e in es:
            c = text.count(e['before'])
            if c != 1:
                problems.append((e['para_hash'], c))
        if problems:
            print(f'!! {fn}: {len(problems)} edits not uniquely matchable — file NOT written')
            for h, c in problems[:20]:
                print(f'   para {h}: found {c}x (need 1)')
            continue
        new = text
        for e in es:
            new = new.replace(e['before'], e['after'], 1)
        if CHECK:
            print(f'-- {fn}: {len(es)} edits would apply cleanly (check only)')
            total_ok += len(es)
            continue
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(new)
        print(f'OK {fn}: applied {len(es)} edits ({len(text)} -> {len(new)} chars)')
        total_ok += len(es)
    print(('checked' if CHECK else 'applied'), total_ok, 'edits total')

if __name__ == '__main__':
    main()
