#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PWG compound (samāsa) segmentation layer — cheap high-value splitter gold.

PWG analyses a compound headword in its etymology parenthesis as a `+`-joined chain
of members in SLP1: `{#aMSaka#}¦ ({#aMSa#} + {#karaRa#})`. This extracts the surface
compound → its ordered underlying members — exactly the surface↔underlying pairing a
sandhi/segmentation splitter is trained and evaluated on. One pass over the committed
pwg.txt (read-only), so it is cheap to regenerate.

The chain is taken **only** from the balanced parenthesis that opens immediately after
the entry's own `{#headword#}¦`, with every nested `[...]` blanked first, and within
each `+`-part only the FIRST `{#…#}` counted as the member. That anchoring is what
makes the layer trustworthy as gold; the pre-26-07-2026 extractor instead took the
first `+`-chain anywhere in the first 400 chars, which silently shipped 344/16,738
rows carrying a bracketed *inner* sub-analysis or a *neighbouring* word's parenthesis
(SanskritGrammar#527). An entry whose paren does not resolve is DROPPED and counted,
never guessed at.

Only analyses whose members are fully spelled are kept — PWG abbreviates a repeated
stem with `˚` (`A˚`), and a truncated member is not usable as splitter gold. Members
keep PWG's order.

Emits (repo `data/pwg_compound_split/` by default, or --out):
  pwg_compound_splits.tsv   headword_slp1 · headword_iast · L_id · arity · members(+-sep)
  pwg_compound_summary.json counts + arity distribution + drop reasons

Deterministic. Reuse: an independent gold reference for the kosha DCS-sandhi programme
and SanskritSpellCheck splitters; a compound-formation teaching surface; a feed for the
pwg_ru translation. Sibling cheap PWG layers: derivation (`von {#base#}`), the Pāṇini
sūtra crosswalk, and German sense glosses.

Usage:
    python scripts/pwg_compound_split.py
    python scripts/pwg_compound_split.py --selftest
"""
import argparse
import itertools
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SLP1 = {'A': 'ā', 'I': 'ī', 'U': 'ū', 'f': 'ṛ', 'F': 'ṝ', 'x': 'ḷ', 'X': 'ḹ',
        'E': 'ai', 'O': 'au', 'M': 'ṃ', 'H': 'ḥ', 'K': 'kh', 'G': 'gh', 'N': 'ṅ',
        'C': 'ch', 'J': 'jh', 'Y': 'ñ', 'w': 'ṭ', 'W': 'ṭh', 'q': 'ḍ', 'Q': 'ḍh',
        'R': 'ṇ', 'T': 'th', 'D': 'dh', 'P': 'ph', 'B': 'bh', 'S': 'ś', 'z': 'ṣ',
        '~': 'm̐', '|': '', '@': ''}


def to_iast(s):
    return ''.join(SLP1.get(c, c) for c in s)


MEMBER = re.compile(r'\{#([^#]+)#\}')
HEAD_RE = re.compile(r'\{#[^#]+#\}¦\s*')      # `{#headword#}¦ `
EMDASH = '—'                                  # PWG's sense divider
MAX_CANDIDATES = 24                           # product cap for ambiguous parts
# Annotation-only material PWG may put between the headword marker and its etymology
# paren (`<lex>m.</lex>`, a sense number, a short German label). A paren is still the
# headword's own across such a gap — but never across another `{#word#}`, a citation,
# a German gloss, or a long stretch of article prose.
GAP_MAX = 120
# a fully-spelled SLP1 member: ASCII letters only. Rejects PWG's abbreviation mark
# `˚` (A˚ = repeat-of-headword-stem, truncated), em-dashes, spaces, digits — those
# members are not usable as splitter gold.
CLEAN_MEMBER = re.compile(r'^[A-Za-z]+$')


def mask_brackets(s):
    """Blank every `[...]` group (PWG's nested sub-analysis) keeping offsets."""
    out = list(s)
    depth = 0
    for i, ch in enumerate(s):
        if ch == '[':
            depth += 1
        if depth:
            out[i] = ' '
        if ch == ']' and depth:
            depth -= 1
    return ''.join(out)


def balanced_paren(s):
    """The balanced `(...)` group at the head of `s`, or None."""
    if not s.startswith('('):
        return None
    depth = 0
    for i, ch in enumerate(s):
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                return s[:i + 1]
    return None


def head_paren(body):
    """The balanced paren belonging to THIS entry's own headword, or (None, why).

    Anchored on the entry's `{#headword#}¦`. The paren may open after
    annotation-only material (`<lex>m.</lex>`, a sense number `1〉`, a short German
    label) — but never after another `{#word#}` (that paren analyses the OTHER word:
    `{#aDikazAzwika#}¦ <lex>adj.</lex> von {#aDikazazwi#} ({#aDika#} + {#zazwi#})`),
    nor after a citation `<ls>`, a gloss `{%…%}`, or a long run of article prose.
    """
    m = HEAD_RE.search(body)
    if not m:
        return None, 'no_head'
    rest = body[m.end():]
    i = 0 if rest.startswith('(') else rest.find('(')
    if i < 0:
        return None, 'no_paren'
    provisional = False
    if i:
        gap = rest[:i]
        if MEMBER.search(gap):
            return None, 'paren_after_other_word'
        if len(gap) > GAP_MAX:
            return None, 'paren_too_far'
        # A citation or a German gloss before the paren is ordinary PWG typography
        # (`{#AmbazWa#}¦ <lex>m.</lex> <ls>P. 8,3,97</ls> ({#Amba#} + {#sTa#})`) —
        # but it is also what an article-body aside looks like, so such a paren is
        # only provisionally the headword's: it must compose the headword to count.
        provisional = '<ls' in gap or '{%' in gap
    paren = balanced_paren(rest[i:])
    if not paren:
        return None, 'unbalanced'
    return paren, 'ok_provisional' if provisional else 'ok'


def covers_surface(hw, members):
    """Do these members account for the headword's surface?

    Sandhi at a seam changes length by at most a character or so (vowel coalescence
    loses one, visarga → r keeps), so a chain that accounts for the headword lands
    within ±1 char per member. A chain that falls short by more is analysing
    something else — typically the base of a *derivative* of the compound
    (`DvajAgravatI` ← `DvajAgravant` ← `Dvaja + agra`), which is not a surface
    segmentation of this headword and so is not splitter gold.
    """
    return abs(sum(len(m) for m in members) - len(hw)) <= len(members)


def pwg_toplevel(body, hw=None):
    """PWG's TOP-LEVEL member chain for the entry's own headword.

    Returns (members|None, paren_text|None, status). Bracket-aware, and within each
    `+`-separated part the member is normally the FIRST `{#…#}` — what follows it is
    PWG's annotation of that member (`<lex>f.</lex> von {#agamya#}`, `= {#loman#}`,
    `<ab>acc.</ab> von {#agni#}`), not a second member.

    First-wins is not safe on its own, though: PWG also writes derivation ladders and
    disjunctions inside a part (`(von {#BAnumant#} oder von {#BAnu#} + {#mati#})`,
    `(<lex>f.</lex> von {#DvajAgravant#} und dieses von {#Dvaja#} + {#agra#})`) where
    the first `{#…#}` is a *base*, not a member. So when a part offers several
    candidates and `hw` is known, the chain is settled against the headword's
    surface: first-wins if it covers, else the unique covering alternative, else the
    entry is DROPPED — never guessed at. A part carrying PWG's em-dash sense divider
    is dropped outright (the paren has run past the end of the analysis).

    Kept in sync with `pwg_toplevel()` in SanskritLexicography's
    `RussianTranslation/src/pilot/adjudicate_compound_differs.py` (H1681), which
    adjudicates this layer against MW: the two must agree on what PWG says, or the
    `differs` queue measures the extractors instead of the dictionaries.
    """
    paren, status = head_paren(body)
    if not paren:
        return None, None, status
    inner = mask_brackets(paren[1:-1])
    parts = []
    for part in inner.split('+'):
        found = MEMBER.findall(part)
        if not found:
            return None, paren, 'part_without_member'
        if len(found) > 1 and EMDASH in part.split('{#', 1)[1]:
            return None, paren, 'ambiguous_sense_divider'
        parts.append(found)
    if len(parts) < 2:
        return None, paren, 'single_member'

    first = [p[0] for p in parts]
    if hw is None:
        return first, paren, 'ok'
    if covers_surface(hw, first):
        return first, paren, 'ok'
    if status == 'ok_provisional':
        # not the headword's own paren after all — an aside in the article body
        return None, paren, 'paren_after_article_text'
    if all(len(p) == 1 for p in parts):
        return first, paren, 'ok'
    # first-wins does not account for the headword — is there exactly one chain that does?
    total = 1
    for p in parts:
        total *= len(p)
    if total > MAX_CANDIDATES:
        return None, paren, 'ambiguous_too_many_candidates'
    covering = [c for c in itertools.product(*parts) if covers_surface(hw, c)]
    if len(covering) == 1:
        return list(covering[0]), paren, 'ok'
    return None, paren, 'ambiguous_no_unique_cover'


def entries(path):
    L = hw = None
    buf, on = [], False
    for ln in open(path, encoding='utf-8'):
        ln = ln.rstrip('\n')
        h = re.match(r'<L>(\d+).*?<k1>([^<]*)', ln)
        if h:
            if on and L:
                yield L, hw, '\n'.join(buf)
            L, hw = h.group(1), h.group(2)
            buf, on = [], True
            continue
        if on:
            if ln.startswith('<LEND>'):
                yield L, hw, '\n'.join(buf)
                on = False
            else:
                buf.append(ln)
    if on and L:
        yield L, hw, '\n'.join(buf)


def lead_ok(hw, first):
    """Headword should begin with the first member's leading (consonant) segment —
    tolerant of vṛddhi/sandhi at the seam, strict enough to reject citation noise."""
    if not first:
        return False
    a = first[:2]
    return hw.startswith(first[:1]) and (hw.startswith(a) or len(first) <= 2 or hw[:1] == first[:1])


# ---------------------------------------------------------------------- selftest

FIXTURES = [
    # (name, headword, body, expected members or None, expected status)
    ("inner_bracketed_subanalysis_not_taken", "akfttaruc",
     "{#akfttaruc#}¦ ({#akftta#} [<hom>3.</hom> {#a#} + {#kftta#} <ab>part.</ab> "
     "von {#kart#}] + {#ruc#})",
     ["akftta", "ruc"], "ok"),
    ("neighbouring_word_paren_not_taken", "aDikazAzwika",
     "{#aDikazAzwika#}¦ <lex>adj.</lex> von {#aDikazazwi#} ({#aDika#} + {#zazwi#})",
     None, "paren_after_other_word"),
    ("annotation_after_member_is_not_a_member", "agnInDa",
     "{#agnInDa#}¦ ({#agnim#} <ab>acc.</ab> von {#agni#} + {#inDa#})",
     ["agnim", "inDa"], "ok"),
    ("plain_binary_chain", "aMSakaraRa",
     "{#aMSakaraRa#}¦ ({#aMSa#} + {#karaRa#})",
     ["aMSa", "karaRa"], "ok"),
    ("ternary_chain", "ADArADeyaBAva",
     "{#ADArADeyaBAva#}¦ ({#ADAra#} + {#ADeya#} + {#BAva#})",
     ["ADAra", "ADeya", "BAva"], "ok"),
    ("single_member_paren_dropped", "aMSa",
     "{#aMSa#}¦ ({#aS#} <ab>v.</ab>)",
     None, "single_member"),
    ("no_headword_marker", "aMSakaraRa",
     "({#aMSa#} + {#karaRa#})",
     None, "no_head"),
    ("nested_paren_stays_balanced", "agnijvalitatejana",
     "{#agnijvalitatejana#}¦ ({#agnijvalita#} (<ab>s. d.</ab>) + {#tejana#})",
     ["agnijvalita", "tejana"], "ok"),
    # --- the paren need not touch `¦`: annotation-only gaps are the headword's own
    ("paren_after_lex_tag_and_sense_number", "BUsuta",
     "{#BUsuta#}¦ 1〉 <lex>m.</lex> (<hom>2.</hom> {#BU#} + {#suta#})",
     ["BU", "suta"], "ok"),
    ("paren_after_citation_kept_when_it_composes", "AmbazWa",
     "{#AmbazWa#}¦ <lex>m.</lex> <ls>P. 8,3,97</ls> ({#Amba#} + {#sTa#}).",
     ["Amba", "sTa"], "ok"),
    ("paren_after_citation_dropped_when_it_does_not", "AkAlikatva",
     "{#AkAlikatva#}¦ <ls>KULL.</ls> fasst das Wort so (<hom>2.</hom> {#A#} + "
     "{#kAla#}) auf.",
     None, "paren_after_article_text"),
    # --- several candidates in one part: settle against the headword's surface
    ("disjunct_bases_settled_by_coverage", "BAnumatin",
     "{#BAnumatin#}¦ (von {#BAnumant#} oder von {#BAnu#} + {#mati#})",
     ["BAnu", "mati"], "ok"),
    ("derivation_ladder_covers_nothing_dropped", "DvajAgravatI",
     "{#DvajAgravatI#}¦ (<lex>f.</lex> von {#DvajAgravant#} und dieses von "
     "{#Dvaja#} + {#agra#})",
     None, "ambiguous_no_unique_cover"),
    ("leading_von_single_candidate_is_fine", "AKukarRI",
     "{#AKukarRI#}¦ (von {#AKu#} {%Maus%} + {#karRa#} {%Ohr%})",
     ["AKu", "karRa"], "ok"),
    ("member_then_von_annotation_first_wins", "CalitarAma",
     "{#CalitarAma#}¦ ({#Calita#} von {#Calay#} + {#rAma#})",
     ["Calita", "rAma"], "ok"),
    ("imperative_annotation_first_wins", "AharakarawA",
     "{#AharakarawA#} und {#AharacelA#}¦ (von {#Ahara#}, <ab>imperat.</ab> von "
     "{#har#} mit {#A#}, + {#karawa#} und {#cela#})",
     ["Ahara", "karawa"], "ok"),
    ("sense_divider_inside_paren_dropped", "anAraByavAda",
     "{#anAraByavAda#}¦ ({#AraBya#} — {#vAda#} + {#vAda#})",
     None, "ambiguous_sense_divider"),
]


def selftest():
    bad = 0
    for name, hw, body, want_members, want_status in FIXTURES:
        members, _paren, status = pwg_toplevel(body, hw)
        if status != want_status or members != want_members:
            bad += 1
            print(f"FAIL {name}: got {members!r}/{status}, want {want_members!r}/{want_status}")
        else:
            print(f"ok   {name}")
    print(f"{len(FIXTURES) - bad}/{len(FIXTURES)} fixtures pass")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pwg", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--selftest", action="store_true",
                    help="run the bracket-awareness fixtures and exit")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    here = Path(__file__).resolve()
    repo = here.parents[1]
    github = here.parents[2]
    pwg = Path(args.pwg) if args.pwg else github / "csl-orig" / "v02" / "pwg" / "pwg.txt"
    if not pwg.exists():
        print(f"ERROR: pwg.txt not found: {pwg}", file=sys.stderr)
        return 1
    out = Path(args.out) if args.out else repo / "data" / "pwg_compound_split"
    out.mkdir(parents=True, exist_ok=True)

    rows = []
    by_arity = Counter()
    dropped = Counter()
    skipped_abbrev = 0
    for L, hw, body in entries(pwg):
        members, _paren, status = pwg_toplevel(body, hw)
        if members is None:
            dropped[status] += 1
            continue
        if not all(CLEAN_MEMBER.match(x) for x in members):
            skipped_abbrev += 1   # abbreviated (A˚) / dash-joined / noisy members
            continue
        if not lead_ok(hw, members[0]):
            dropped['lead_mismatch'] += 1
            continue
        by_arity[len(members)] += 1
        rows.append((hw, L, members))

    rows.sort(key=lambda r: (r[0], int(r[1])))
    tsv = out / "pwg_compound_splits.tsv"
    with tsv.open("w", encoding="utf-8", newline="") as f:
        f.write("headword_slp1\theadword_iast\tL_id\tarity\tmembers_slp1\tmembers_iast\n")
        for hw, L, members in rows:
            f.write(f"{hw}\t{to_iast(hw)}\t{L}\t{len(members)}\t"
                    f"{' + '.join(members)}\t{' + '.join(to_iast(x) for x in members)}\n")

    summary = {
        "study": "PWG compound (samāsa) segmentation layer",
        "as_of": "2026-07-26",
        "source": "csl-orig/v02/pwg/pwg.txt (read-only)",
        "method": ("balanced etymology paren anchored on the entry's own `{#headword#}¦`, "
                   "nested `[...]` blanked, split on `+` at depth 0, one member per part "
                   "(first `{#…#}`, or the unique candidate that composes the headword "
                   "where the part offers several), ≥2 members, lead-compatible with the "
                   "headword"),
        "revision": ("26-07-2026 (SanskritGrammar#527, H1703): headword-anchored + "
                     "bracket-aware re-derivation. vs the 19-07-2026 cut — 16,094 rows "
                     "unchanged, 139 members corrected, 512 dropped as unresolvable, "
                     "879 added that the old head-scan missed."),
        "compounds": len(rows),
        "arity_distribution": dict(sorted(by_arity.items())),
        "excluded_abbreviated_member_analyses": skipped_abbrev,
        "dropped_unresolved": dict(sorted(dropped.items())),
        "note": ("PWG abbreviates a repeated stem with `˚` (A˚); such analyses are excluded here "
                 "because the member is truncated — only fully-spelled member splits are kept. "
                 "`dropped_unresolved` counts entries whose paren could not be resolved to a "
                 "top-level chain for THIS headword — no `¦` head, no paren, the paren "
                 "analyses a neighbouring word, it sits too far into the article, it is "
                 "unbalanced, a `+`-part carries no member or PWG's sense divider, the part "
                 "offers several candidates and none uniquely composes the headword, only one "
                 "member, or the first member is not a lead-compatible prefix. All dropped, "
                 "never guessed at (SanskritGrammar#527)."),
    }
    (out / "pwg_compound_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"compounds: {len(rows)}")
    print(f"arity: {dict(sorted(by_arity.items()))}")
    print(f"dropped: {dict(sorted(dropped.items()))}")
    print(f"wrote {tsv.name} + pwg_compound_summary.json → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
