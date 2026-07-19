# -*- coding: utf-8 -*-
"""H1259 — apply hybrid line-edit replacements with NBSP-tolerant matching.

The manuscript .mdx uses U+00A0 (NBSP) typography (1,800+ instances), while
edit pairs are authored with plain spaces. This applier:
  1. matches `old` against the file with every space treated as [ \\u00A0]
     (must match exactly ONCE — else the pair is rejected, H385 fuse);
  2. restores NBSP in `new` wherever the matched raw span used NBSP in an
     identical local context (trigram carry-over), so surviving fragments
     keep their typography;
  3. appends a {file, before, after} record per applied edit to
     rws_edits_h1259.jsonl for the review-docx build (rws_to_docx.py schema).

Usage: python rws_h1259_apply.py <batch.json>   # [{"old": ..., "new": ...}, ...]
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(BASE, '02_gasuns-dhatu-PhD-text2.mdx')
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rws_edits_h1259.jsonl')
NBSP = ' '


def flex_pattern(s):
    return re.compile(''.join(r'[  ]' if c == ' ' else re.escape(c) for c in s))


def restore_nbsp(raw_old, new):
    """Carry NBSP typography from the matched raw span into the replacement."""
    out = new
    for m in re.finditer(NBSP, raw_old):
        i = m.start()
        left = raw_old[max(0, i - 4):i]
        right = raw_old[i + 1:i + 5]
        plain = left + ' ' + right
        nb = left + NBSP + right
        out = out.replace(plain, nb)
    return out


def main():
    obj = json.load(open(sys.argv[1], encoding='utf-8'))
    batch = obj['edits'] if isinstance(obj, dict) else obj
    text = open(TARGET, encoding='utf-8').read()
    records, failed = [], []
    if isinstance(obj, dict):
        for r in obj.get('log_only', []):
            records.append({'file': '02_gasuns-dhatu-PhD-text2.mdx',
                            'before': r['before'], 'after': r['after'],
                            'finding_ids': [], 'styles': ['h1259-line-edit']})
    for pair in batch:
        old, new = pair['old'], pair['new']
        hits = list(flex_pattern(old).finditer(text))
        if len(hits) != 1:
            failed.append((old[:80], len(hits)))
            continue
        raw_old = hits[0].group(0)
        raw_new = restore_nbsp(raw_old, new)
        text = text[:hits[0].start()] + raw_new + text[hits[0].end():]
        records.append({'file': '02_gasuns-dhatu-PhD-text2.mdx',
                        'before': raw_old, 'after': raw_new,
                        'finding_ids': pair.get('finding_ids', []),
                        'styles': pair.get('styles', ['h1259-line-edit'])})
    if failed:
        for f, n in failed:
            print('REJECTED (%d matches): %s...' % (n, f))
    if records:
        open(TARGET, 'w', encoding='utf-8', newline='').write(text)
        with open(LOG, 'a', encoding='utf-8') as fh:
            for r in records:
                fh.write(json.dumps(r, ensure_ascii=False) + '\n')
    print('applied %d / %d edits; log: %s' % (len(records), len(batch), LOG))
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
