#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SG-WF-004 taddhita — PWG denominal-derivation extraction (citation-backed).

The visa follow-up (H1236, notes TAD2-01 + TAD2-04): redo the dictionary track
over the **Petersburger Wörterbuch (PWG, großes PW)**, which — unlike Monier-
Williams — attaches a source citation (`<ls>`) to almost every sense.

PWG marks derivation in German prose with the base word in SLP1 braces:
`{#aMSaka#}¦ (von 1. {#aMSa#}) m.` = aṃśaka ← aṃśa. The existing Cologne
extractor [csl-orig/v02/pwg/analyze_pwg_etymology.py] keeps only ROOT bases
(`von {#stem#}` is dropped unless the source is a known dhātu) — so it captured
11,492 primary (kṛt) derivations and only 34 denominal ones. This script INVERTS
that guard: it keeps `von {#nominal-base#}` where the base is NOT a root and the
headword RECONSTRUCTS as base(+vṛddhi/+final-vowel-elision) + a known taddhita
suffix. That reconstruction gate replaces the dhātu whitelist and keeps precision
high (manual spot-check of 25 -ya derivations: 25/25 genuine denominal taddhita).

Why this matters for the article's §3-ter conclusion: MW's POS-only method could
not separate possessive -in / relational -ya from their kṛt homonyms (agent -in,
gerundive -ya) — 25 % / 31 % sample precision. PWG states the base EXPLICITLY as a
nominal ("von {#nominal#}"), and roots are excluded, so a PWG denominal -in/-ya IS
structurally distinct from a kṛt -in/-ya. PWG resolves the homonymy MW could not —
at the cost of coverage (only where PWG wrote an explicit derivation note; a
high-precision LOWER bound, not a full census).

Read-only. Reads csl-orig (never writes there) + the pinned DCS master. Emits
sangram/articles/taddhita-overview/data/pwg_taddhita_derivations.tsv and
pwg_taddhita_summary.json. Deterministic.

Usage:
    python scripts/sg_wf_004_taddhita_pwg.py
"""
import argparse
import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_PWG = GITHUB / "csl-orig" / "v02" / "pwg" / "pwg.txt"
DEFAULT_DHATU = GITHUB / "csl-orig" / "v02" / "etymology_stats" / "dhatu_roots.txt"
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT_DIR = ROOT / "sangram" / "articles" / "taddhita-overview" / "data"

SLP1 = {'A': 'ā', 'I': 'ī', 'U': 'ū', 'f': 'ṛ', 'F': 'ṝ', 'x': 'ḷ', 'X': 'ḹ',
        'E': 'ai', 'O': 'au', 'M': 'ṃ', 'H': 'ḥ', 'K': 'kh', 'G': 'gh', 'N': 'ṅ',
        'C': 'ch', 'J': 'jh', 'Y': 'ñ', 'w': 'ṭ', 'W': 'ṭh', 'q': 'ḍ', 'Q': 'ḍh',
        'R': 'ṇ', 'T': 'th', 'D': 'dh', 'P': 'ph', 'B': 'bh', 'S': 'ś', 'z': 'ṣ',
        '~': 'm̐', '|': '', '@': ''}


def to_iast(s):
    return ''.join(SLP1.get(c, c) for c in s)


# taddhita suffix -> Russian class label (aligned with the article's §3 tables)
SUF_CLASS = {
    'tva': 'абстракт', 'tA': 'абстракт', 'tvana': 'абстракт', 'tana': 'абстракт',
    'in': 'поссессив', 'vin': 'поссессив', 'min': 'поссессив',
    'vat': 'поссессив', 'mat': 'поссессив', 'vala': 'поссессив',
    'ika': 'относит./vṛddhi', 'ya': 'относит./vṛddhi',
    'Iya': 'относит./vṛddhi', 'eya': 'относит./vṛddhi',
    'maya': 'материал', 'ka': 'уменьш./собират.',
    'tara': 'сравнение', 'tama': 'сравнение',
    'tas': 'адверб', 'Sas': 'адверб',
    'anIya': 'герундивообразный', 'tavya': 'герундивообразный',
}
SUFFIXES = sorted(SUF_CLASS, key=len, reverse=True)  # longest-first

# vṛddhi of the first vowel of a stem (SLP1)
VR = {'a': 'A', 'A': 'A', 'i': 'E', 'I': 'E', 'u': 'O', 'U': 'O',
      'f': 'Ar', 'e': 'E', 'o': 'O', 'E': 'E', 'O': 'O'}


def vrddhi(stem):
    for i, ch in enumerate(stem):
        if ch in 'aAiIuUfeoEO':
            return stem[:i] + VR[ch] + stem[i + 1:]
    return stem


def base_variants(base):
    """Plausible stem forms of `base` before a taddhita suffix."""
    vs = {base}
    if base and base[-1] in 'aAiIuUf':
        vs.add(base[:-1])
    vs.add(vrddhi(base))
    if base and base[-1] in 'aAiIuUf':
        vs.add(vrddhi(base[:-1]))
    return vs


def match_suffix(hw, base):
    """Longest taddhita suffix S such that hw == base_variant + S; else None."""
    bvs = base_variants(base)
    for suf in SUFFIXES:
        if hw.endswith(suf):
            stem = hw[:-len(suf)]
            if len(stem) >= 2 and stem in bvs:
                return suf
    return None


DERIV_RE = re.compile(
    r"(?P<cue>Von|von|Wurzel|Stamm)\s+(?:<hom>[^<]*</hom>\s*)?\{#(?P<src>[^#]+)#\}")
LS_RE = re.compile(r"<ls>([^<]+)</ls>")
LEX_RE = re.compile(r"<lex>([^<]+)</lex>")


def load_roots(path):
    roots = set()
    for ln in open(path, encoding='utf-8'):
        ln = ln.strip()
        if ln and not ln.startswith('#'):
            roots.add(ln)
    return roots


def entries(path):
    L_id = hw = None
    buf, collecting = [], False
    for ln in open(path, encoding='utf-8'):
        ln = ln.rstrip('\n')
        h = re.match(r'<L>(\d+).*?<k1>([^<]*)', ln)
        if h:
            if collecting and L_id:
                yield L_id, hw, buf
            L_id, hw = h.group(1), h.group(2)
            buf, collecting = [], True
            continue
        if collecting:
            if ln.startswith('<LEND>'):
                yield L_id, hw, buf
                collecting = False
            else:
                buf.append(ln)


def extract(pwg_path, roots):
    records = []
    seen = set()
    for L_id, hw, buf in entries(pwg_path):
        body = '\n'.join(buf)
        flat = ' '.join(body.split())
        cites = LS_RE.findall(body)
        lex = LEX_RE.findall(body)
        for m in DERIV_RE.finditer(flat):
            base = m.group('src').strip()
            if ' ' in base or len(base) > 18:
                continue
            if base in roots:                 # root base -> primary (kṛt), skip
                continue
            suf = match_suffix(hw, base)
            if not suf:
                continue
            key = (hw, base, suf)
            if key in seen:
                continue
            seen.add(key)
            records.append({
                'L_id': L_id,
                'headword_slp1': hw,
                'headword': to_iast(hw),
                'base_slp1': base,
                'base': to_iast(base),
                'suffix': suf,
                'suffix_class': SUF_CLASS[suf],
                'lex': lex[0] if lex else '',
                'citations': cites[:8],
                'n_citations': len(cites),
            })
    return records


def dcs_join(db_path, records):
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    cur = con.cursor()
    prov = dict(cur.execute("SELECT key, value FROM provenance").fetchall())
    if "source_commit" not in prov:
        print("ERROR: DCS master has no provenance pin — refusing", file=sys.stderr)
        sys.exit(1)
    lemmas = sorted({r['headword'] for r in records})
    tok = {}
    for i in range(0, len(lemmas), 500):
        ch = lemmas[i:i + 500]
        ph = ",".join("?" * len(ch))
        for lem, c in cur.execute(
                f"SELECT lemma, COUNT(*) FROM token WHERE upos IN ('NOUN','ADJ') "
                f"AND lemma IN ({ph}) GROUP BY lemma", ch):
            tok[lem] = c
    con.close()
    return prov, tok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pwg", default=str(DEFAULT_PWG))
    ap.add_argument("--dhatu", default=str(DEFAULT_DHATU))
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()
    pwg, dhatu, db = Path(args.pwg), Path(args.dhatu), Path(args.db)
    for p, label in ((pwg, "PWG text"), (dhatu, "dhātu roots"), (db, "DCS master")):
        if not p.exists():
            print(f"ERROR: {label} not found: {p}", file=sys.stderr)
            return 1

    roots = load_roots(dhatu)
    records = extract(pwg, roots)
    prov, tok = dcs_join(db, records)

    for r in records:
        r['dcs_tokens'] = tok.get(r['headword'], 0)
        r['dcs_attested'] = r['headword'] in tok

    n = len(records)
    with_cite = sum(1 for r in records if r['n_citations'] > 0)
    attested = [r for r in records if r['dcs_attested']]
    by_class_types = Counter(r['suffix_class'] for r in records)
    by_class_att = Counter(r['suffix_class'] for r in attested)
    # Tokens are a property of the derived LEMMA, not the (base,suffix) record —
    # dedupe by (class, headword) so a word derived from two bases is not counted
    # twice, and sum the grand total over unique attested lemmas.
    by_class_tok = defaultdict(int)
    seen_cls_lemma = set()
    for r in attested:
        k = (r['suffix_class'], r['headword'])
        if k in seen_cls_lemma:
            continue
        seen_cls_lemma.add(k)
        by_class_tok[r['suffix_class']] += r['dcs_tokens']
    total_tokens = sum(tok[l] for l in {r['headword'] for r in attested})
    by_suffix_types = Counter(r['suffix'] for r in records)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cols = ['L_id', 'headword_slp1', 'headword', 'base_slp1', 'base', 'suffix',
            'suffix_class', 'lex', 'n_citations', 'dcs_tokens', 'dcs_attested', 'citations']
    tsv = OUT_DIR / "pwg_taddhita_derivations.tsv"
    with tsv.open('w', encoding='utf-8', newline='') as f:
        f.write('\t'.join(cols) + '\n')
        for r in sorted(records, key=lambda x: (x['suffix_class'], -x['dcs_tokens'], x['headword'])):
            row = dict(r)
            row['citations'] = '; '.join(r['citations'])
            f.write('\t'.join(str(row[c]).replace('\t', ' ') for c in cols) + '\n')

    summary = {
        'as_of': '2026-07-18',
        'method': 'PWG denominal-derivation extraction (von {#non-root base#} + reconstruction gate) x DCS token join',
        'source_pwg': 'csl-orig/v02/pwg/pwg.txt',
        'dcs_source_commit': prov.get('source_commit', ''),
        'total_derivations': n,
        'with_citation': with_cite,
        'citation_coverage_pct': round(100 * with_cite / max(1, n), 1),
        'dcs_attested_types': len({r['headword'] for r in attested}),
        'dcs_total_tokens': total_tokens,
        'by_class_types': dict(by_class_types.most_common()),
        'by_class_attested_types': dict(by_class_att.most_common()),
        'by_class_tokens': dict(sorted(by_class_tok.items(), key=lambda x: -x[1])),
        'by_suffix_types': dict(by_suffix_types.most_common()),
    }
    (OUT_DIR / "pwg_taddhita_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f"PWG denominal taddhita derivations: {n}")
    print(f"citation-backed: {with_cite} ({summary['citation_coverage_pct']} %)")
    print(f"DCS-attested types: {summary['dcs_attested_types']} · tokens: {summary['dcs_total_tokens']}")
    print(f"DCS pin: {prov.get('source_commit','')[:12]}")
    print("\nby class (types / attested / tokens):")
    for cls in by_class_types:
        print(f"  {cls:22s} {by_class_types[cls]:5d} / {by_class_att[cls]:5d} / {by_class_tok[cls]:6d}")
    print(f"\nwrote {tsv.name} + pwg_taddhita_summary.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
