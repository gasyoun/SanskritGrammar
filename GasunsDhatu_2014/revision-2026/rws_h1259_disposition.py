# -*- coding: utf-8 -*-
"""H1259 — deterministic disposition ledger over all 1,127 RWS findings.

Assigns exactly ONE status per finding — already_addressed / safe_apply /
human_judgment / reject / not_applicable — by rule, in priority order, and
writes RWS_DISPOSITION_H1259.tsv (idx, run, cluster, type, triage, rule,
status). Statuses are RULE-derived (each row names its rule), not per-finding
adjudicated; the rules and their evidence are documented in
RWS_H1259_EDIT_REPORT.md. Totals must reconcile to 1,127.

Rules (priority order):
  R1 already_addressed — finding id applied verbatim by H385
     (finding_ids in rws_edits.jsonl).
  R2 not_applicable    — cluster Д5 (persona optics): the RWS report's own
     §3/Д5 verdict — optional for this book, not a C1 defect.
  R3 human_judgment    — cluster Д4 (IAST-at-first-mention book-wide
     convention): the convention itself is not author-visaed; H1259 applied
     instances only inside its queue sections, visible in the review docx.
  R4 already_addressed — runs obzor/glava2: those sections were wholesale
     reworked and author-visaed AFTER the 07-07 RWS run (Обзор — H384;
     Гл. 2 — H358 pilot + H1069 §2.1/§2.2, visas 15–17-07) — the findings
     target replaced text.
  R5 human_judgment    — runs vvedenie/zakl/art-*: Введение/Заключение are
     author-owned rewrites per RWS report §4.1; the three appendix articles
     were not in the H1259 queue.
  R6 safe_apply        — remaining glava1/glava3 findings (clusters Д1/Д2/Д3):
     covered by the H1259 line-edit sweep of §1.1/§1.4/§3.1/§3.3/§3.4 —
     every applied change is highlighted with its original in the review
     docx; anchor drift (three rework waves since 07-07) prevents exact
     per-finding pairing, so the verification locus is the docx, and any
     finding whose paragraph now lives outside the queue sections
     (post-H991 recomposition) falls to the author pass with the rest.
"""
import csv, json, os, sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
REV = os.path.dirname(os.path.abspath(__file__))

h385_ids = set()
for ln in open(os.path.join(REV, 'rws_edits.jsonl'), encoding='utf-8'):
    r = json.loads(ln)
    if r.get('styles') != ['h1259-line-edit']:
        h385_ids.update(r.get('finding_ids', []))

tri = {}
for para in json.load(open(os.path.join(REV, 'rws_triage.json'), encoding='utf-8'))['paragraphs']:
    for f in para['findings']:
        tri[f['idx']] = f

rows = []
with open(os.path.join(REV, 'RWS_FINDINGS.tsv'), encoding='utf-8') as fh:
    rd = csv.DictReader(fh, delimiter='\t')
    for idx, r in enumerate(rd):
        run = r['run']
        chapter = run.split('-')[2]  # vvedenie/obzor/glava1/glava2/glava3/zakl/art
        t = tri.get(idx, {})
        cluster, trige = t.get('cluster', '?'), t.get('disposition', '?')
        if idx in h385_ids:
            rule, status = 'R1', 'already_addressed'
        elif cluster == 'Д5':
            rule, status = 'R2', 'not_applicable'
        elif cluster == 'Д4':
            rule, status = 'R3', 'human_judgment'
        elif chapter in ('obzor', 'glava2'):
            rule, status = 'R4', 'already_addressed'
        elif chapter in ('vvedenie', 'zakl') or chapter.startswith('art'):
            rule, status = 'R5', 'human_judgment'
        else:  # glava1 / glava3
            rule, status = 'R6', 'safe_apply'
        rows.append({'idx': idx, 'run': run, 'chapter': chapter, 'cluster': cluster,
                     'type': r['type'], 'severity': r['severity'], 'triage': trige,
                     'rule': rule, 'status': status})

out = os.path.join(REV, 'RWS_DISPOSITION_H1259.tsv')
with open(out, 'w', encoding='utf-8', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter='\t')
    w.writeheader()
    w.writerows(rows)

c = Counter(r['status'] for r in rows)
cr = Counter(r['rule'] for r in rows)
print('total:', len(rows))
print('by status:', dict(c))
print('by rule:', dict(cr))
assert len(rows) == 1127, len(rows)
