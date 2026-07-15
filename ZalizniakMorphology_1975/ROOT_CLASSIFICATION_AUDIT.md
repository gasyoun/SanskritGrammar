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

## Independent corroboration at scale — Tolchelnikov's Talmud data (added on MG's tip)

MG pointed out that [`TolchelnikovTalmud_2026/data/z_root_map.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/z_root_map.json)
already exists: 905 roots from samskrtam.ru/z/ (Толчельников И.Е. «Санскритская морфология»),
joined to Whitney numbers, tagged with alternation series (Ряд) and aniṭ/seṭ/veṭ — the SAME
classificatory model Zaliznyak published in 1975, applied independently by a different scholar to
nearly the same root inventory. That is a genuinely useful thing to check aggregate counts
against, at 5× the scale of this pass's hand-transcription — while still not being literally
Zaliznyak's own dataset, so results below are framed as "corroborates", never "confirms".

**Alternation-series distribution — strong agreement on four of five groups:**

| Series group | Zaliznyak's stated count | Talmud's actual count | Gap |
|---|--:|--:|--:|
| A1 (general ~100 + samprasāraṇa ~60) | ~160 | 155 | −5 (−3.1%) |
| A2 (~50 + ~30) | ~80 | 85 | +5 (+6.2%) |
| L (~20) | ~20 | 21 | +1 (+5.0%) |
| I+U+R (~120 + ~360) | ~480 | 461 | −19 (−4.0%) |
| M+N (~50 + ~60) | ~110 | 80 | **−30 (−27.3%)** |

Four groups land within ±6% of Zaliznyak's own approximate counts despite the two corpora not
being identically scoped — genuinely strong corroboration, not a coincidence. The M+N group is
the outlier (110 stated vs. 80 actual); not resolved in this pass, but worth a closer look before
assuming it's just corpus-scoping noise like the other four.

**Table 5 (aniṭ/seṭ) — strong agreement on two of three columns:** spot-checking which of the
paper's three summary-table example roots Talmud tags as which category (col 1 examples *ci,
śru, dṛś, vac, pad* are consistently aniṭ in Talmud; col 3 examples *gad, cumb, ḍhauk, rud, vraj,
rakṣ* are consistently seṭ) gives a reasonably confident column mapping. Against that mapping:
**aniṭ 178 vs. Zaliznyak's stated ≈170** (gap +8), **seṭ 325 vs. his stated ≈320** (gap +5) — both
within a few percent. The middle veṭ-family total (294) does **not** match his stated middle
column (≈100) — likely because that column is a narrower type/series-specific subset in his
table, not a corpus-wide veṭ total; not resolved, flagged rather than forced to fit.

**Per-root series cross-validation — honest, partially inconclusive:** checking each of this
pass's ~180 hand-transcribed roots against Talmud's independent series tag gives **122 agree, 67
disagree, 28 not found**. A meaningful chunk of the 67 disagreements traces to a genuine ambiguity
this pass tried and failed to resolve cleanly: Talmud's z_series carries a `0`-variant tag
(I0/U0/R0/N0/M0) alongside the `1`/`2` subseries, and no single mapping rule from this script's own
"ends in consonant" vs. "ends in alternating element" transcription onto Talmud's `0`-vs-`1`/`2`
distinction reconciled all cases — a first attempt (map "ends in consonant" → the `0` variant)
fixed some roots (*sev, lok, garh, edh* → correctly I0/U0/R0) but broke others that already matched
under a plain-strip mapping (*bhikṣ, cumb, vṛj, krīḍ, pūj* → Talmud tags these plain I1/U1/R1/I2/U2,
not `0`), and went the *opposite* direction for the M/N-series consonant-final group (*stambh,
dhvaṁs, taṁs* etc., which this pass calls "M1", are tagged plain **N1** in Talmud, not M0 or even
M-anything). That specific M→N pattern may itself be a real, useful finding — it's consistent with
the M+N group's −27% count gap above — but resolving it needs a trained Sanskritist, not a
heuristic string mapping. Reported honestly as unresolved rather than forced into either "fix."

## Honest scope statement

This is an infrastructure-building pass, not a claim-by-claim verdict register like the other
three books. It digitizes real primary data (Zaliznyak's own named-root classifications) into
queryable form and runs the checks a non-specialist can responsibly run — existence, arithmetic,
and now independent-corroboration-at-scale via Talmud's data — without attempting to re-adjudicate
root-by-root Type/series assignments that would require redoing professional Indological analysis.
Several items are explicitly left **unresolved** rather than force-closed: the 9 genuinely-
unmatched roots, Table 5's internal-arithmetic gap (though the Talmud cross-check substantially
supersedes it for two of three columns), the 847-vs-930 Whitney-corpus-size discrepancy, the M+N
group's −27% count gap, and the I/U/R/M/N `0`-vs-`1`/`2` subseries-tagging ambiguity. All are
legitimate targets for a follow-up pass by someone (human or a future session) with either deeper
Sanskrit philology or direct access to Whitney's original 1885 root appendix to resolve
definitively.

---

_Dr. Mārcis Gasūns_
