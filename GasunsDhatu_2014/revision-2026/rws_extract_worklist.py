# -*- coding: utf-8 -*-
"""H385 — extract the exact paragraph text for every apply-paragraph.

Reads rws_triage.json + the source .mdx files and, for each paragraph that
carries an APPLY finding, pulls the exact current paragraph block (bounded by
blank lines around the finding's `line`). Emits rws_apply_worklist.json so the
rewrite step works on the real text and the apply step can match it verbatim.
Stdlib only.
"""
import json, sys, io, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\user\Documents\GitHub\SanskritGrammar-h385\GasunsDhatu_2014'
REV = BASE + r'\revision-2026'

def load_lines(fn):
    with open(BASE + '\\' + fn, encoding='utf-8') as f:
        return f.read().split('\n')

def is_blank(s):
    return s.strip() == ''

def para_block(lines, line1):
    """Return (start_idx, end_idx_exclusive, text) for the blank-line-bounded
    block containing 1-based line `line1`. Skips fenced/heading-only lines
    only implicitly (we keep whatever the block is)."""
    n = len(lines)
    i = line1 - 1
    if i < 0 or i >= n:
        return None
    # if the target line itself is blank, try the next non-blank
    if is_blank(lines[i]):
        j = i
        while j < n and is_blank(lines[j]):
            j += 1
        if j >= n:
            return None
        i = j
    start = i
    while start > 0 and not is_blank(lines[start - 1]):
        start -= 1
    end = i
    while end < n and not is_blank(lines[end]):
        end += 1
    return start, end, '\n'.join(lines[start:end])

def main():
    tri = json.load(open(REV + r'\rws_triage.json', encoding='utf-8'))
    filecache = {}
    work = []
    misses = []
    for p in tri['paragraphs']:
        if not p['has_apply']:
            continue
        fn, ln = p['file'], p['line']
        if ln is None:
            misses.append({'file': fn, 'reason': 'no line number'})
            continue
        if fn not in filecache:
            filecache[fn] = load_lines(fn)
        blk = para_block(filecache[fn], ln)
        if blk is None:
            misses.append({'file': fn, 'line': ln, 'reason': 'block extract failed'})
            continue
        start, end, text = blk
        applies = [f for f in p['findings'] if f['disposition'] == 'APPLY']
        softens = [f for f in p['findings'] if f['disposition'] == 'SOFTEN']
        work.append({
            'file': fn,
            'line': ln,
            'para_hash': hashlib.sha1(text.encode('utf-8')).hexdigest()[:12],
            'char_len': len(text),
            'apply': [{'idx': f['idx'], 'style': f['style'], 'severity': f['severity'],
                       'type': f['type'], 'finding': f['finding'], 'suggestion': f['suggestion']}
                      for f in applies],
            'soften': [{'idx': f['idx'], 'style': f['style'], 'type': f['type'],
                        'suggestion': f['suggestion']} for f in softens],
            'before': text,
        })
    json.dump({'paragraphs': work, 'misses': misses},
              open(REV + r'\rws_apply_worklist.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('apply-paragraphs extracted:', len(work))
    print('misses:', len(misses))
    for m in misses[:20]:
        print('  MISS', m)
    # size stats
    tot = sum(w['char_len'] for w in work)
    print('total chars in apply-paragraphs:', tot)
    from collections import Counter
    print('by file:', dict(Counter(w['file'] for w in work)))

if __name__ == '__main__':
    main()
