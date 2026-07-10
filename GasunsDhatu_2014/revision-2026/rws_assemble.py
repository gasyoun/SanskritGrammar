# -*- coding: utf-8 -*-
"""H385 — assemble rws_edits.jsonl from the per-batch agent outputs.

Reads the apply worklist (exact `before` text + finding metadata) and every
scratchpad/batches/out_*.json (agent-produced `after` text keyed by para_hash),
joins them, and writes revision-2026/rws_edits.jsonl with one record per edit:
  {section, file, line, para_hash, finding_ids, styles, before, after}
Collects agent-reported per-finding skips into rws_agent_skips.json for the
skipped-list generator. Validates that every `after` maps to a known para_hash
whose `before` is still present verbatim in the current .mdx.
Stdlib only.
"""
import json, os, sys, io, glob, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\user\Documents\GitHub\SanskritGrammar-h385\GasunsDhatu_2014'
REV = BASE + r'\revision-2026'
BDIR = r'C:\Users\user\AppData\Local\Temp\claude\C--Users-user-Documents-GitHub\6822ba6d-a7a3-44af-a90e-f4d8286b3215\scratchpad\batches'

SECTION_OF = {
    '02_gasuns-dhatu-PhD-text2.mdx': 'Основной текст',
    'Морфонологическая запись глагольных корней санскрита.mdx': 'Статья: Морфонологическая запись',
    'О записи омонимии корней в словарях древнеиндийского языка.mdx': 'Статья: Омонимия корней',
    'Распределение рядов согласных.mdx': 'Статья: Распределение рядов согласных',
}

def unsafe_edit(before, after):
    """True if this edit must be rejected as a mis-anchor risk. Bibliography /
    index / TOC rows must never be prose-rewritten (the line-offset in
    RWS_FINDINGS.tsv attaches prose findings to them — see RWS_APPLY_MEMO.md).
    A table edit is allowed ONLY if it stays a table and preserves every digit
    (i.e. a label-only change such as adding IAST), never a prose rewrite."""
    b = before.strip()
    first = b.split('\n', 1)[0].strip()
    digits = lambda s: re.findall(r'\d', s)
    if b.startswith('|') or b.startswith('```'):            # markdown / rst table
        a = after.strip()
        table_kept = a.startswith('|') or a.startswith('```')
        return not (table_kept and digits(before) == digits(after))
    if re.match(r'^\d+[.)]\s*\*\*[^*]+\*\*\s*\d{2,4}', first):   # "33. **Name** 1978"
        return True
    if re.match(r'^-?\s*№\s*\d+', first):                    # "- № 349 ..."
        return True
    if re.match(r'^\d+\.\s+[a-zāīūṛṝḷṃṁḥśṣṭḍṇñṅ]{1,4}\s+\d', first):  # "34. sr 761 ..."
        return True
    if re.match(r'^[A-ZА-Я][\w.]{0,6}\.\s*--\s', first):     # "Ht. -- Huet 2006"
        return True
    if re.search(r'\.{4,}\s*\d+\s*$', first):               # TOC dotted leader
        return True
    return False


def main():
    wl = json.load(open(REV + r'\rws_apply_worklist.json', encoding='utf-8'))['paragraphs']
    by_hash = {p['para_hash']: p for p in wl}
    filetext = {}
    def ftext(fn):
        if fn not in filetext:
            filetext[fn] = open(BASE + '\\' + fn, encoding='utf-8').read()
        return filetext[fn]

    edits, agent_skips = [], []
    seen = set()
    problems = []
    for out in sorted(glob.glob(BDIR + r'\out_*.json')):
        try:
            data = json.load(open(out, encoding='utf-8'))
        except Exception as e:
            problems.append(f'{os.path.basename(out)}: unreadable ({e})')
            continue
        for rec in data:
            h = rec.get('para_hash')
            wp = by_hash.get(h)
            if not wp:
                problems.append(f'{os.path.basename(out)}: unknown para_hash {h}')
                continue
            if h in seen:
                problems.append(f'duplicate para_hash {h} ({os.path.basename(out)})')
                continue
            after = rec.get('after', '')
            if not after or after == wp['before']:
                continue
            if wp['before'] not in ftext(wp['file']):
                problems.append(f'{h}: before-text no longer in {wp["file"]} (drift)')
                continue
            if unsafe_edit(wp['before'], after):
                problems.append(f'{h}: REJECTED — biblio/index/TOC row or table-structure/number change (mis-anchor guard)')
                continue
            seen.add(h)
            fids = rec.get('applied', []) or [f['idx'] for f in wp['apply']]
            styles = sorted({f['style'] for f in wp['apply'] if f['idx'] in set(fids)}) \
                     or sorted({f['style'] for f in wp['apply']})
            edits.append({
                'section': SECTION_OF.get(wp['file'], wp['file']),
                'file': wp['file'], 'line': wp['line'], 'para_hash': h,
                'finding_ids': fids, 'styles': styles,
                'before': wp['before'], 'after': after,
            })
            for sk in rec.get('skipped', []):
                agent_skips.append({'para_hash': h, 'file': wp['file'], 'line': wp['line'],
                                    'idx': sk.get('idx'), 'reason': sk.get('reason', '')})
    # deterministic order: by file (main first), then line
    order = {fn: i for i, fn in enumerate(SECTION_OF)}
    edits.sort(key=lambda e: (order.get(e['file'], 99), e['line'] or 0))
    with open(REV + r'\rws_edits.jsonl', 'w', encoding='utf-8') as f:
        for e in edits:
            f.write(json.dumps(e, ensure_ascii=False) + '\n')
    json.dump(agent_skips, open(REV + r'\rws_agent_skips.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('edits assembled:', len(edits))
    print('agent-reported finding skips:', len(agent_skips))
    print('problems:', len(problems))
    for p in problems[:30]:
        print('  !', p)
    from collections import Counter
    print('edits by file:', dict(Counter(e['file'] for e in edits)))

if __name__ == '__main__':
    main()
