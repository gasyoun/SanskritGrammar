# Verification — Sangram editorial notes, charter and roadmap

_Created: 18-07-2026 · Last updated: 19-07-2026_

Acceptance gates for wave 1. A handoff is not done until its gate passes and the check is recorded.
Implementation: [`docs/IMPLEMENTATION_SANGRAM_EDITORIAL_NOTES.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/IMPLEMENTATION_SANGRAM_EDITORIAL_NOTES.md).

> **Naming note (19-07-2026, [H1273](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1273-Sonnet_SanskritGrammar_sangram-review-votes-track-h856-reversal_18.07.26.md)).** Gates A1/A2 below originally named this artifact `EDITORIAL_NOTES_LEDGER.tsv` / `EDITORIAL_NOTES_EXCLUDED.tsv`. It shipped as [`review/EDITORIAL_NOTE_INDEX.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/EDITORIAL_NOTE_INDEX.tsv) / [`review/EDITORIAL_NOTE_INDEX_EXCLUDED.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/EDITORIAL_NOTE_INDEX_EXCLUDED.tsv) instead — a deliberate divergence so the word "ledger" stays [H1260](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1260-Sonnet_SanskritGrammar_sangram-consolidation-policy-ledger_18.07.26.md)'s alone (that handoff owns the Sangram **article-disposition ledger**, a different object). Gate names below are updated to match. **Gate A6 also shipped a different count than spec'd** (4 rows, not 8) — H1273's fresh re-derivation against `origin/main` found half of the originally-assumed-open `prose-style-guide`/`perfect` notes were already applied by prior sessions (H1003, H1205) before the sheet HTML was lost, so only 4 notes were genuinely still open+orphaned. Full accounting in [PR #455](https://github.com/gasyoun/SanskritGrammar/pull/455).

## 1. Invariants — must hold at every point in the wave

| # | Invariant | How it is checked |
|---|---|---|
| I1 | Ledger has exactly **81** rows | Row count vs. re-parse of the 13 `decisions.json` |
| I2 | Excluded file has exactly **6** rows (3 `reject`, 3 `null`) | Row count + decision values |
| I3 | 81 + 6 + 33 (approved, no note) = **120** voted items | Sums to the parsed total |
| I4 | No published DCS number changed without a verified probe | Diff every numeral in touched articles against `origin/main` |
| I5 | Every `APPLIED` row cites a revision-history line | Grep `note_uid` / `item_id` in `target_file` |
| I6 | No write outside the executing worktree | `git -C <each live worktree> status` unchanged |
| I7 | No commit touches A61 branches | Branch diff. Note `codex/a61-history-argument` is **not** an ancestor of `codex/a61-sol-evidence` (`merge-base --is-ancestor` exits 1) — an ancestry-based "already merged, safe to drop" check on it returns the wrong answer |

> I4 is the one that protects the project's credibility. H1229 re-derived 129 published DCS numbers
> and refuted 3; the notes contain several challenges to figures, and none of them licenses editing
> a number directly.

## 2. Per-handoff gates

### W1-A · ledger build

| Gate | Pass condition |
|---|---|
| A1 | `review/EDITORIAL_NOTE_INDEX.tsv` exists with 81 rows, 8 columns |
| A2 | `review/EDITORIAL_NOTE_INDEX_EXCLUDED.tsv` has 6 rows, each with a disposition |
| A3 | `git check-ignore review/` returns nothing (no longer ignored) |
| A4 | `git status --short review/` lists 13 `decisions.json` + 9 `_review.html` as staged additions |
| A5 | `docs/DECISION_RECORD_REVIEW_TRACKING_H856_REVERSAL.md` exists and names H856, the reversal, and the ~250 KB cost |
| A6 | **Shipped as 4, not 8** — rows carry `provenance=RECONSTRUCTED` only for the genuinely-still-open `prose-style-guide`/`perfect` notes (`prose-style-guide` A1/A2/B1 + `perfect` A5); the other 8 orphan-sheet rows that turned out already resolved via an existing citation carry `provenance=ORPHAN_MOOT` instead (see PR #455) |
| A7 | Every row's `target_file` exists on disk |

Failure mode to check explicitly: a ledger of **87** rows means the note-only filter was used
instead of approve-and-note. That is the single likeliest defect in this handoff.

### W1-B · applied adjudication

| Gate | Pass condition |
|---|---|
| B1 | Zero `UNKNOWN` in `applied_status` |
| B2 | Every `APPLIED`/`PARTIAL` row carries an evidence pointer (file + line or revision-row text) |
| B3 | `future` = 7 `APPLIED`, `causative` = 4, `taddhita-revisa` = 3 `APPLIED` + TAD2-08 `OPEN`, `a-stems` = 3 `APPLIED`, `precative` = 3 `APPLIED` (P1/P4/P5, evidence = commit `3b4f9e4` / [PR #416](https://github.com/gasyoun/SanskritGrammar/pull/416)) |
| B4 | The 9 A65 `HB-*`/`HK-*` notes are **not** marked `APPLIED` on the strength of a `claims.json` hit alone |
| B5 | Final `OPEN` count = **60**, and `APPLIED` = 21; any divergence explained, not silently absorbed |
| B6 | The run began with `git fetch origin` and adjudicated against `origin/main`, not a local HEAD. `precative` is the regression case: it was 3 `OPEN` at drafting time and 3 `APPLIED` hours later |

B4 is a deliberate trap check — a naive grep marks all 9 applied. If B3 and B4 both pass, the
adjudication was done by reading, not grepping.

### W1-C / W1-D / W1-E · applying notes

| Gate | Pass condition |
|---|---|
| C1 | Every note now `APPLIED` has a revision row citing `sheet_id` + `item_id` |
| C2 | Every note left `DEFERRED` names what it is waiting on (probe, PDF, human) |
| C3 | Every `ESCALATED` note has a real `@DECIDE` row in GTD, two paragraphs, quoting the note |
| C4 | No `QUESTION`-class note is marked `APPLIED` |
| C5 | `POLICY` notes wrote to the style guide, not to individual articles |
| C6 | Docusaurus build green; no broken internal links |
| C7 | Russian prose passes a register read — no new invented jargon (the notes' most-repeated complaint) |
| C8 | H1274's 22 + H1275's 8 + H1276's 9 = **39**, plus H1257's 10 (`w2-core`) + H1258's 11 (`metodichka-kochergina`) = **21**, account for **all 60** open notes; no note-index row with status `OPEN` lacks an owning handoff **in this plan or a named concurrent one** |

C4 is the anti-fabrication gate. `metodichka-apte-v1#zan-09` «А как Шерцль?» and
`sangram-prose-style-guide-visa#A8` «Сам корпус слова „перфект“ не знает — верно ли?» cannot be
"applied"; if they show as `APPLIED`, an answer was invented. Both are cited with their sheet
qualifier deliberately: `A8` is **not** a `perfect`-sheet id despite discussing the perfect — that
sheet's ids stop at `A7`/`B1`. A bare positional id in a gate is unverifiable.

### W2-A · charter

| Gate | Pass condition |
|---|---|
| D1 | `grep -E '20(2[7-9]\|3[01])' sangram/SANGRAM_CHARTER_2026_2031.mdx` returns only the title, slug, sidebar label and description — no wave dates |
| D2 | Each of the five waves has an explicit "opens when / closes when" contract |
| D3 | The gantt is gone; a gate/dependency diagram replaces it |
| D4 | Revision history states the calendar was removed because production overtook it by ~2 years, with the W2-closed-19/19 evidence |
| D5 | The published slug `/sangram/charter-2026-2031` is unchanged |
| D6 | R6's English-locale trigger is a contract condition, not a date |

### W2-B · ACL roadmap

| Gate | Pass condition |
|---|---|
| E1 | `grep -ci sangram ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md` > 0 — it is currently **0** |
| E2 | Both ACL papers still present (ruling 4: keep both) |
| E3 | S1–S4 described as instruments feeding Sangram, not as the primary programme |
| E4 | S1 τ and S5 κ described as already cited inside Sangram articles |
| E5 | `Uprava/ROADMAP_INDEX.md` row updated |

### W3-A · RQ4 pilot runbook

| Gate | Pass condition |
|---|---|
| F1 | The runbook **consumes** the ruled decisions (recruitment, N = 4 weeks, Systema hosting, approved consent text) and re-derives none of them |
| F2 | The approved Russian consent paragraph appears **verbatim** |
| F3 | The R20 non-collision constraint is stated as a hard sequencing gate |
| F4 | Stopping rules and the n≈5 target are explicit |
| F5 | A32 reporting is specified as a pilot, never as a powered confirmatory result |
| F6 | No agent step recruits, contacts, or enrols a participant |

F6 is absolute. This is the repo's only human-subjects exposure; agents prepare, a human runs.

## 3. Cross-cutting doc gates

| Gate | Pass condition |
|---|---|
| G1 | Every `.md`/`.mdx` touched has `_Created: … · Last updated: …_` in `DD-MM-YYYY` |
| G2 | Every touched file closes with `_Dr. Mārcis Gasūns_` |
| G3 | No raw HTML in `.md` |
| G4 | Every filename/path/URL in committed markdown is a **full** `https://github.com/gasyoun/…/blob/…` link |
| G5 | `CHANGELOG.md` has an `[Unreleased]` entry per handoff; `/cut-release` run |
| G6 | `.ai_state.md` moved landed items to Completed |

## 4. Wave-level exit

Wave 1 closes when all of the following hold.

| # | Condition |
|---|---|
| X1 | All 81 ledger rows are terminal: `APPLIED`, `DEFERRED` (with a reason), or `ESCALATED` |
| X2 | `review/` is tracked and the H856 reversal has a decision record |
| X3 | The charter carries no calendar years |
| X4 | The ACL roadmap mentions Sangram and keeps both papers |
| X5 | The 3 undecided items sit in a re-vote sheet awaiting a human — **not** applied |
| X6 | The registry hazard is **measured and recorded**, not assumed fixed: re-run the §2.3 method against `git show origin/main:handoffs/README.md` at wave close and record the then-current "🟡 SanskritGrammar rows whose H-id is cited by a SanskritGrammar `origin/main` commit" count (**51 of 67** at 18-07-2026). No duplicate handoff was minted for it. **X6 does not gate on H1252 completing** — H1252 is Uprava-wide (all 170 rows) and itself depends on H1247/H1248/H1251; wave 1 inherits its fix, it does not wait for it |
| X7 | The A61 contradiction (H1222 ✅ vs PR #403 body) is recorded as awaiting a human ruling |

## 5. Known-false checks — do not add these

| Tempting check | Why it is wrong |
|---|---|
| "14 articles carry «Статья-кандидат»" | The string appears in all 35 articles, in historical revision rows of *published* ones. Status must be read from the top-of-article status line |
| "All decisions are approve, so all 87 notes apply" | 3 rejects and 3 nulls carry notes; only 81 are applicable |
| "`HB-*` id in `claims.json` ⇒ note applied" | `claims.json` lists claims, not applications. False-positive on all 9 A65 notes |
| "Next-free-ID marker is stale ⇒ next mint collides" | [`mint_handoff.py`](https://github.com/gasyoun/Uprava/blob/main/tools/mint_handoff.py) takes `max()` over `handoffs/` + `archive/` **and** the marker. Collision-safe; the staleness is a dispatch/doc defect only |
| "`git merge-base` says nothing, so `codex/a61-sol-evidence` contains the other branch" | It exits **1** — not an ancestor. The branches diverged at `072443d`. Dominance here is patch-identity (`d43fb38` ≡ `35d932f`), a content fact that must be measured each time, not an ancestry fact |
| "H1252 is an unfilled stub with no registry row" | True only on a **stale** Uprava clone (the drafting clone was 74 commits behind). On `origin/main` H1252 is filled and rowed. Read registry state from `origin/main` or not at all |
| "`generated` is `DD-MM-YYYY`" | Two forms in the wild: 6 files `DD-MM-YYYY`, 7 files ISO-8601 UTC. A single-format parser silently mis-dates half the ledger |
| "The precative sheet has 3 open notes" | Zero. Applied by commit `3b4f9e4` / [PR #416](https://github.com/gasyoun/SanskritGrammar/pull/416) on 18-07-2026, after this plan's first draft. Re-derive the ledger against `origin/main`, never against the draft |

_Dr. Mārcis Gasūns_
