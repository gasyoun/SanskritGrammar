# -*- coding: utf-8 -*-
"""H1259 — derive full-paragraph {before, after} records by diffing the edited
02_gasuns-dhatu-PhD-text2.mdx against its origin/main version, so that
rws_to_docx.py (which keys on whole blank-line-separated blocks) highlights
every edited paragraph with its exact pre-edit text in the comment.

Overwrites rws_edits_h1259.jsonl with the block-level records.
"""
import difflib, json, os, subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REV = os.path.dirname(os.path.abspath(__file__))
FN = '02_gasuns-dhatu-PhD-text2.mdx'


def blocks(text):
    out, buf = [], []
    for line in text.split('\n'):
        if line.strip() == '':
            if buf:
                out.append('\n'.join(buf))
                buf = []
        else:
            buf.append(line)
    if buf:
        out.append('\n'.join(buf))
    return out


old_text = subprocess.run(
    ['git', 'show', 'origin/main:GasunsDhatu_2014/' + FN],
    cwd=BASE, capture_output=True, encoding='utf-8').stdout
new_text = open(os.path.join(BASE, FN), encoding='utf-8').read()

ob, nb = blocks(old_text), blocks(new_text)
sm = difflib.SequenceMatcher(a=ob, b=nb, autojunk=False)
records = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'replace':
        continue
    before_group = ob[i1:i2]
    after_group = nb[j1:j2]
    if len(before_group) == len(after_group):
        pairs = zip(before_group, after_group)
    else:
        joined = '\n\n'.join(before_group)
        pairs = ((joined, a) for a in after_group)
    for before, after in pairs:
        records.append({'file': FN, 'before': before, 'after': after,
                        'finding_ids': [], 'styles': ['h1259-line-edit']})

out = os.path.join(REV, 'rws_edits_h1259.jsonl')
with open(out, 'w', encoding='utf-8') as fh:
    for r in records:
        fh.write(json.dumps(r, ensure_ascii=False) + '\n')
print('block-level records:', len(records))
