# S2 — Morphoclass three-scheme agreement over the 876-root crosswalk

_Created: 24-09-2026 · Last updated: 24-09-2026_

Q3.4 of [ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md) §4 — Fleiss κ / Krippendorff α over the 876-root crosswalk, never run before this pass. Generator: [scripts/q34_three_scheme_agreement.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/q34_three_scheme_agreement.py). Data: [TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv).

## ⚠ Coder substitution — read this before the numbers

The roadmap names the three coders **Zal./Gas./Tol.** (Zaliznyak 1975 / Gasuns 2014 / Tolchelnikov 2026). **Gasuns 2014 has no independent per-root classification in this repo.** Two sources confirm it: [MORPHOCLASS_3WAY_MEMO.md](https://github.com/gasyoun/SanskritGrammar/blob/main/MORPHOCLASS_3WAY_MEMO.md) axis 2 ("2014. Ряды не трогает — берет как есть") and [GasunsDhatu_2014/07_glava7_ukazatel-zaliznyaka.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/07_glava7_ukazatel-zaliznyaka.mdx) §7.1, whose own index sources its per-root series from "зализняковская классификация 1975 г." rather than proposing one. A literal Zal./Gas./Tol. study is therefore not computable from committed data. What follows substitutes the third genuinely independent classification act actually present in the crosswalk CSV: **Zaliznyak's own 1978 (Ocherk) revision** — a different published scheme by the same original author, rule-derived by [ZalizniakOcherk_1978/build_1978_crosswalk.py](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/build_1978_crosswalk.py). Coders used: **1975** (`ryad_derived`, this repo's rule-based reproduction of Zaliznyak 1975's Table-2 calculus), **1978** (`ryad_1978`, Zaliznyak's Ocherk revision), **2026** (`z_series`, Tolchelnikov's scheme via Shirobokov's `/z/` database). A human wanting the literal Gasuns substitution ruled differently should reopen this as `@DECIDE`.

**Known data caveat carried through, not corrected:** `z_series` contains 115 "0-variant" rows (`I0/N0/R0/U0/M0`) that [z_reconciliation_report.md](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/z_reconciliation_report.md)'s author-ruling addendum calls a `/z/` Table-2 bug, not a real category. Not dropped — reported at two granularities instead, since the letter-only view is immune to the 0-vs-1/2 dispute.

## Result

| Granularity | n items | n categories | Fleiss κ | 95% CI | Krippendorff α | 95% CI | observed agreement P̄ |
|---|--:|--:|--:|---|--:|---|--:|
| full | 844 | 18 | **0.7593** | (0.7319, 0.7845) | **0.7594** | (0.732, 0.7846) | 0.7923 |
| letter | 844 | 7 | **0.8178** | (0.7934, 0.8414) | **0.8179** | (0.7935, 0.8414) | 0.861 |

Rows excluded: missing a value from at least one coder — 1; excluded as uncertain (`ryad_1978` `?`-flagged) — 31.

## Pairwise disagreement (letter granularity) — where the three actually differ

| Pair | n | raw agreement | Cohen κ |
|---|--:|--:|--:|
| 1975 ↔ 1978 | 844 | 0.9171 | 0.8883 |
| 1975 ↔ 2026 | 844 | 0.8258 | 0.7746 |
| 1978 ↔ 2026 | 844 | 0.84 | 0.7952 |

All-three-disagree at letter granularity: **10** of 844 roots — the concrete "where the three actually disagree" the roadmap output column asks for.

## Reading
Full-code Fleiss κ = 0.7593; letter-only Fleiss κ = 0.8178. Per the Landis & Koch (1977) scale (routinely cited for this metric range), full-code κ sits in **substantial** agreement and letter-only κ in **almost perfect** — the three schemes agree on gross alternation series far more often than chance, but genuine three-way disagreement survives even after the disputed 0-vs-1/2 subindex is collapsed away: 10 roots (letter granularity) where 1975, 1978 and 2026 each assign a *different* series, plus the weaker 1975↔2026 pairwise link (0.7746) than either 1975↔1978 (0.8883, same original author, two editions) — expected, since 1975/1978 share an author and 2026 is a fully independent scholar's scheme. This is the number Paper 2 (§4 Q1 2027) formalises.

_Dr. Mārcis Gasūns_
