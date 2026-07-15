# Root classification audit — Zaliznyak, Morphophonological Classification (1975)

_Created: 15-07-2026 · Last updated: 15-07-2026_

Summary of [`build_root_classifier.py`](build_root_classifier.py) / [`root_classifier.json`](root_classifier.json)
— the H797 Phase 2 pass on the fourth Zaliznyak/Kochergina/Bühler/Knauer source checked. No
generator/`claims.yml` here (see "Why this register looks different" below); this is a
hand-written summary of a bespoke script's output.

## Why this register looks different from the other three

[H797](https://github.com/gasyoun/Uprava/blob/main/handoffs/H797-Fable_SanskritGrammar_claim-verification-backlog-verify-and-cross-grammar-generalise_12.07.26.md)'s
pipeline harvests **discursive corpus-frequency claims** (Kochergina/Bühler/Ocherk/Konspekt:
"usually", "rarely", verified against DCS token counts) or **individual footnote parses**
(Knauer: verified one at a time against Whitney citations). This paper — Zaliznyak's actual
1975 published morphophonological classification article — is neither. Its falsifiable unit is
**how many of Whitney's ~750–847 verbal roots fall into each cell of a classification scheme**
(alternation series A/I/U/R/L/M/N × degree-of-alternation Type I–IV, and separately
aniṭ/seṭ/veṭ). That is checkable only against an actual enumerated root list, not a corpus
frequency count — a genuinely different kind of ground truth from the other three sources.

**What this script does NOT do:** independently re-derive Zaliznyak's classification from raw
phonology. Doing that would mean redoing his own scholarly analysis from scratch, with real risk
of a non-Indologist getting subtle judgment calls wrong. **What it does instead:** digitizes the
~180 roots Zaliznyak names *explicitly* throughout his own prose into structured, queryable form
(his own primary data, faithfully transcribed), then checks that against two things checkable
without redoing his linguistics: (1) do these roots actually exist in an independent, structured
Whitney root inventory — [`WhitneyRoots/crosswalk/roots.csv`](https://github.com/gasyoun/WhitneyRoots/blob/main/crosswalk/roots.csv)
(930 entries); (2) do his own stated summary counts add up internally.

## Root existence check

**208 of 224 named-root citations (210 distinct roots) — 93% — found** in WhitneyRoots'
structured inventory, after normalizing a transliteration-convention difference: the paper's
English translation uses the older ç/ṁ IAST convention (ç = ś, ṁ = ṃ); WhitneyRoots uses the
modern ś/ṃ convention. Same phonemes, two spelling schemes — not a data problem once normalized
(before normalizing, only 184/224 matched).

The remaining 16 non-matches are not root-inventory errors; each falls into an expected category:

- **Quasi-roots, not in Whitney's primary list by definition** — *chay*, *hvay*, *çvay*, *vay*
  are all explicitly labeled "quasi-root" in the paper itself (derived stems used to build forms
  normally derived from a primary root); Whitney's list covers primary roots, so their absence is
  exactly what should happen, not a gap.
- **Citation-grade convention differences** — Whitney sometimes cites a root in a different grade
  than Zaliznyak's regularized by-type convention would predict. E.g. Zaliznyak's Type-II
  citation convention gives *spardh*, but WhitneyRoots cites the same root as *spṛdh* (zero
  grade) — confirmed by checking the entry directly (whitney_no 882, gloss "contend", attested
  forms include *spardhate*, *aspardhanta*). Similarly *krap*: Zaliznyak's own footnote at mdx
  line 173 already says "in Whitney's list, kṛp" — he flags the citation difference himself.
- **Blend/variant naming** — *manth* "blends with *math* in later language" per the paper's own
  text (mdx line 231); WhitneyRoots has *math* (whitney_no 544) but not a separate *manth* entry,
  consistent with the paper's own account of the blend.
- **A handful of genuine misses not yet explained** — *med*, *kṣaṇ*, *randh*, *sañj*, *granth*,
  *aṁç*, *añc*, *hvā*, *bhraç* were not found under any spelling variant checked in this pass.
  These may be grouped under a different Whitney headword (e.g. as a sub-entry or cross-reference)
  rather than genuinely absent — not resolved here, flagged for a follow-up pass rather than
  guessed at.

## Table arithmetic — internal consistency

**Table 4 (root-type distribution) summary row:** 435 (Type I) + 229+109 (Type II, definite +
ambiguous) + 117 (Type III) = **890**. The paper itself states its analyzed corpus is
"approximately 750 out of 847" roots (mdx line 29) and separately notes that roots showing
historical transitions or fluctuations are **counted twice** in these tallies (mdx line 287). The
890 vs. ~750 gap (140 roots) is the right order of magnitude for that stated double-counting
correction — **plausible, not a contradiction**, though this pass did not independently verify
the *exact* count of double-counted roots, so it's reported as PLAUSIBLE rather than CONFIRMED.

**Table 5 (aniṭ/seṭ distribution) summary row:** ≈170 + ≈100 + ≈320 = **≈590**. The paper states
this table excludes "approximately 240" roots with no attested relevant forms (mdx line 307) plus
*all* ā-final roots as a separate, uncounted category. Without knowing how many roots are
"ā-final" in this table's terms, `750 − 240 − X = ~590` cannot be checked — **this pass could not
resolve X**, so the arithmetic is neither confirmed nor flagged as wrong. Genuinely unresolved,
not glossed over: a real Sanskritist would need to either supply the ā-final count or recompute it
from Whitney's list directly.

**Whitney corpus size:** WhitneyRoots' `roots.csv` has 930 entries against the paper's stated
Whitney total of 847 "non-cross-referenced entries." Likely a different counting convention (the
digitized list may include cross-referenced/homonym-split entries the paper's phrasing explicitly
excludes) rather than an error in either source — not resolved here, flagged for whoever
maintains WhitneyRoots to confirm.

## Honest scope statement

This is an infrastructure-building pass, not a claim-by-claim verdict register like the other
three books. It digitizes real primary data (Zaliznyak's own named-root classifications) into
queryable form and runs the checks a non-specialist can responsibly run — existence and
arithmetic — without attempting to re-adjudicate root-by-root Type/series assignments that would
require redoing professional Indological analysis. Three items are explicitly left **unresolved**
rather than force-closed: the 9 genuinely-unmatched roots, Table 5's arithmetic gap, and the
847-vs-930 Whitney-corpus-size discrepancy. All three are legitimate targets for a follow-up pass
by someone (human or a future session) with either deeper Sanskrit philology or direct access to
Whitney's original 1885 root appendix to resolve definitively.

---

_Dr. Mārcis Gasūns_
