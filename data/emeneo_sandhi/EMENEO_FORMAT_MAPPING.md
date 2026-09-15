# Emeneo → kosha sandhi-drills format mapping

_Created: 13-09-2026 · H4486 (OxAlpha drain)_

## Target gold format

kosha `sandhi-drills` (data-v0.2.0, `data/sandhi/sandhi_drills.tsv`) columns:

```
id  type  rule  category  lesson  difficulty  question  answer  choices  context
```

Emeneo drills keep the exact column set; `--check` mode asserts ≥50 rows.

## Field mapping

| kosha field | Emeneo source | convention |
|---|---|---|
| `id` | — | `ESD-####` (Emeneau sandhi drill; kosha uses `SD-####`, disjoint) |
| `type` | item shape | `join` (surface changed), `identify` (junction unchanged — pragṛhiya, m+vowel, voiceless-before-voiceless etc.) |
| `rule` | pamphlet rule no. | `E41…E71`, chains `E66+E67`; pamphlet rule = Whitney ch.III ref (in `context`) |
| `category` | rule class | kosha corpus-sandhi taxonomy: `vowel coalescence` (41–49), `visarga` (50–59), `anusvāra / nasal` (60–65), `consonant` (66–71), `unchanged junction` |
| `lesson` | «После X занятия» anchor | first MG-course lesson number of the exercise: Ex11→7, Ex12→6, Ex13→7, Ex14→5 (full hint preserved in `context`) |
| `difficulty` | junction type | `identify`=easy, sentence `join`=medium, compound=medium |
| `question`/`answer` | derived | answer computed by the committed rules-41–71 junction engine, never hand-recited |
| `choices` | — | answer + 3 deterministic auto-generated distractors (unchanged surface, vowel-cycle mutation, hyphenated/misending variant) — documented as mechanical, not philological |
| `context` | provenance | `Emeneau&vanNooten 2nd ed. Ex.N item L; rule EXX (Whitney ch.III); После … занятия` |

## Interpretation decisions (rule-faithful, documented)

1. **Engine over recitation.** All answers come from `junction()` in
   `scripts/build_emeneo_sandhi_drills.py` implementing pamphlet rules 41–71.
   The gate: every worked example the pamphlet prints for those rules must be
   reproduced exactly (37/37).
2. **Pamphlet typos, engine follows Whitney:** the pamphlet prints `vāñ mama`
   (rule 69) — Whitney 161a, cited by that rule, gives `vāṅ`; excluded from
   parity, engine gives `vāṅmadhura` for `vāk+madhura`.
3. **brahma+rṣi**: the pamphlet tags it rule 43, but `a + r-` is pure compound
   fusion with no surface change — engine labels `E-none`.
4. **ṛ-final stems** (rule 45): semivowelization keeps the following vowel —
   `pitṛ+artham → pitrartham`, `māndhātṛ+upākhyāna → māndhātrupākhyāna`.
5. **Phrase vs compound aspirates** (W163/P8.4.62): phrases double
   (`tat+hiranyam → tad dhiranyam`, parity-verified); compounds simplify to a
   single aspirate — `vāk+hasta+vant → vāghastavant` (attested,
   `COMPOUND_ATTESTED_OVERRIDES`).
6. **Documented exclusions** (never guessed): `bhātṛ+ṛṣi` (ṛ+ṛ junction underdetermined
   by rules 41–71), `go+aśva` (dvandva morphology-dependent), `tat+ḍiṇḍima`
   (t+ḍ cluster not covered by the pamphlet's examples), `vidyut+lekhā`,
   `vidyut+mālā` (W162 t+l is optional), `vāk+hasta` as a bare junction
   (covered by the compound-level override instead).
7. **kosha lesson column**: kosha uses integer lessons 1–N; the MG-course
   anchor is carried in `context` verbatim so nothing is lost in the mapping.

## Enrichment vs duplicate verdict

- The junction/rule layer DUPLICATES kosha corpus-sandhi coverage (the same
  Whitney rules induce kosha's 13k-rule table).
- The ITEM layer ENRICHES: 94 human-authored practice instances keyed to MG's
  own course lessons (Kochergina/Zaliznyak/Elizarenkova anchors), a corpus the
  kosha drills (auto-induced from DCS) do not contain. Verdict: **gold
  enrichment**.

_Dr. Mārcis Gasūns_
