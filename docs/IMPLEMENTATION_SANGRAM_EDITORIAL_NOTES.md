# Implementation — applying the Sangram editorial notes

_Created: 18-07-2026 · Last updated: 19-07-2026_

Step-by-step execution detail for wave 1. Architecture:
[`docs/ARCHITECTURE_SANGRAM_EDITORIAL_NOTE_PIPELINE.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ARCHITECTURE_SANGRAM_EDITORIAL_NOTE_PIPELINE.md).
Acceptance gates: [`docs/VERIFICATION_SANGRAM_EDITORIAL_NOTES.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_SANGRAM_EDITORIAL_NOTES.md).

## 0. Preconditions for every wave-1 handoff

| Check | Command / rule |
|---|---|
| Fresh clone state | `git fetch origin` **first** — a stale clone is how H919 built a duplicate |
| Worktree, never the shared tree | `git worktree add -b <branch> ../SanskritGrammar-<slug> origin/main` |
| Do not enter live worktrees | Enumerate them, never trust a list: `git worktree list` → every entry but the main tree and your own is foreign; then `ls -d ../SanskritGrammar-*` for same-pattern dirs git no longer tracks (as of 18-07-2026 that is six registered foreign worktrees, including `.codex-worktrees/roadmap-sanskritgrammar-20260718` and `.claude/worktrees/agent-afd4e9eb320e94171`, plus untracked `SanskritGrammar-h917` and `SanskritGrammar-mo023`) |
| Remove the worktree same pass | `git -C <repo> worktree remove <path>` once the PR lands |

## 1. W1-A — build the ledger

### 1.1 Parse

Read all 13 `review/*_decisions.json`. The key set is uniform, the **`generated` value is not**:

```
{ "sheet_id": ..., "generated": <see below>, "decided": <int>, "items": [ {"id","decision","note"} ] }
```

`generated` comes in **two incompatible forms** and a parser written to one of them mis-parses the
other. Measured across the 13 files, 18-07-2026:

| Form | Example | Files |
|---|---|---:|
| `DD-MM-YYYY` | `"17-07-2026"` | **6** — `prose-style-guide`, `declension-overview`, `a-stems`, `perfect`, `w2-core`, `precative` |
| ISO-8601 UTC timestamp | `"2026-07-17T18:16:42.748Z"` | **7** — `a65`, `metodichka-apte`, `metodichka-kochergina`, `sg-mo-021-future`, `sg-mo-028-causative`, `sg-wf-004-taddhita`, `sg-wf-004-taddhita-revisa` |

The parser **must** accept both — try ISO-8601 first, fall back to `%d-%m-%Y` — and normalise to one
form in the ledger. Do not "fix" the source files: they are the author's cast votes and are about to
become tracked artifacts (§1.3); normalise on read, never on disk. `decision` is a third trap: it is
`"approve"` / `"reject"` / **JSON `null`**, and `null` is a value, not a missing key.

Emit a row **only** where `decision == "approve"` and `note` is non-empty → exactly **81** rows.
Everything else goes to `review/EDITORIAL_NOTE_INDEX_EXCLUDED.tsv` (6 rows: 3 `reject`, 3 `null`).

> Do not filter on `note` alone. 87 items carry notes, but 3 of those notes are rejection rationale
> and 3 sit on undecided items. Applying all 87 applies six things the author did not approve.

### 1.2 Resolve `target_file`

| Sheet prefix | Target |
|---|---|
| `sangram-sg-mo-001-declension-overview` | [`sangram/articles/declension-overview/index.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/declension-overview/index.mdx) |
| `sangram-sg-mo-002-a-stems` | [`sangram/articles/a-stems/index.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/a-stems/index.mdx) |
| `sangram-sg-mo-017-perfect` | [`sangram/articles/perfect/index.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/perfect/index.mdx) |
| `sanskritgrammar-sg-mo-021-future` | [`sangram/articles/future/index.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/future/index.mdx) |
| `sanskritgrammar-sg-mo-028-causative` | [`sangram/articles/causative/index.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/causative/index.mdx) |
| `sanskritgrammar-sg-wf-004-taddhita*` | [`sangram/articles/taddhita-overview/index.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/taddhita-overview/index.mdx) |
| `sangram-prose-style-guide` | [`sangram/editorial/SANGRAM_STYLE_GUIDE_PROSE_RU.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/editorial/SANGRAM_STYLE_GUIDE_PROSE_RU.mdx) |
| `sanskritgrammar-metodichka-apte-v1` | `ApteSyntax_1885/METODICHKA_APTE_*.md` |
| `sanskritgrammar-metodichka-kochergina-v1` | `KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_*.md` |
| `sanskritgrammar-a65-verdict-validation` | `claims.json` in `BuhlerLeitfaden_1923/` and `KocherginaUchebnik_1998/` |
| `sanskritgrammar-precative-label-dcs2026` | Settled, not open — commit `3b4f9e4` resolved P1/P4/P5 to `KocherginaUchebnik_1998/claims.json` (HK-39) and `ZalizniakOcherk_1978/claims.json` (OCH-3, OCH-30). Record those as the `target_file`s; no application work remains |
| `sangram-w2-core-11candidates` | **Per item** — `WF*`/`MO*` prefix maps to its own article |

`w2-core` is the one sheet whose 10 notes fan out across many articles; its item ids
(`WF01`, `MO06`, `MO23`, `MO26`, `MO28`…) are article codes, resolvable from the sheet HTML, which
survives.

### 1.3 The gitignore reversal

1. Remove line 23 `/review/` from [`.gitignore`](https://github.com/gasyoun/SanskritGrammar/blob/main/.gitignore), and the two H856 rationale comment lines above it.
2. Write `docs/DECISION_RECORD_REVIEW_TRACKING_H856_REVERSAL.md` — content is §5 of the architecture doc.
3. `git add review/` → 13 `decisions.json` + 9 `_review.html`.
4. Commit message must name the reversal, e.g. `feat(review): track review/ artifacts — reverses H856`.

## 2. W1-B — adjudicate applied/open

For each of the 81 rows, decide `APPLIED` / `PARTIAL` / `OPEN`.

**Evidence ranking**, strongest first:

1. A revision-history row citing the `item_id` verbatim — conclusive.
2. A revision-history row describing the edit in prose without ids (`a-stems`) — conclusive if the prose matches the note.
3. Article text that plainly satisfies the note — `PARTIAL` unless unambiguous.
4. The id appearing in `claims.json` / `CLAIMS_VERIFIED.md` — **not evidence of application.** These registries list claims, so an `HB-*` id appears there whether or not the note was acted on. This is a live false-positive trap: a naive grep marks all 9 A65 notes applied when none are.

Known anchors: `future` 7/7 applied · `causative` 4/4 · `taddhita-revisa` 3/4 (TAD2-08 open) ·
`a-stems` 3/3 · `precative` 3/3 (P1/P4/P5, commit `3b4f9e4`,
[PR #416](https://github.com/gasyoun/SanskritGrammar/pull/416)) · `perfect` 1/5 (A7 → style guide).
Expected total `APPLIED` = **21**, `OPEN` = **60**.

> `precative` is the anchor that shows why W1-B must re-fetch before adjudicating. Its three notes were
> open when this plan was drafted and closed hours later by a merge to `origin/main`. A stale clone
> would re-apply them — the H919 duplicate-build failure, exactly.

## 3. W1-C / W1-D / W1-E — apply the open notes

### 3.1 Order within a handoff

1. `LOCAL` notes first — cheapest, and they clear noise before harder ones.
2. `POLICY` notes next — they may change how remaining `LOCAL` ones are phrased.
3. `RESEARCH` notes last — each opens a probe; several will not close this wave.
4. `QUESTION` notes are never "done" — write the `@DECIDE` and move on.

### 3.2 Applying a `LOCAL` note

```
1. Read the note and the sheet item it refers to (via note_uid).
2. Locate the passage in target_file.
3. Make the minimal edit that satisfies the note, in the author's register.
4. Append a revision-history row citing sheet_id + item_id.
5. Update the ledger row: applied_status = APPLIED, with the row as evidence.
```

Worked example, `[MO028-08]`:

> Note: «vṛддхi — это помесь на 3 языках — русском, санскрите и украинском сразу»
> Edit: replace the mixed-script token with `vṛddhi` throughout.
> Row: `| 17-07-2026 | «vṛддхи»→«vṛddhi» везде (MO028-08) | Лист sanskritgrammar-sg-mo-028-causative_visa |`

That row already exists — which is exactly how this note is known to be applied.

### 3.3 Applying a `POLICY` note

Do **not** edit the article. Write the rule into
[`SANGRAM_STYLE_GUIDE_PROSE_RU.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/editorial/SANGRAM_STYLE_GUIDE_PROSE_RU.mdx)
or the method doc, then note in the ledger which articles will need a later sweep.

Two policy notes recur across sheets and should be handled once, globally:

| Policy | Sources |
|---|---|
| Minimum 5 examples per pattern, "по возможности" | **5 notes, 4 sheets** — `causative#MO028-09`, `taddhita#WF004-09`, `future#MO021-05`, `future#MO021-07`, `declension-overview#A5` |
| No invented jargon; if the author cannot parse it, it is wrong | **5 notes, 5 sheets** — `declension-overview#A7`, `taddhita#WF004-10`, `w2-core#MO16`, `future#MO021-02`, `precative#P6` |

The second is the most-repeated complaint in the entire vote set — five independent notes across **five
different sheets** attack the same defect («осиротевший пин», «подмножество EM5», «птичий язык»,
«написано на каком языке?», «я не знаю на каком языке это написано… даже мне, составителю»). It is a
repo-wide register problem, not five article bugs. Note that `precative#P6` sits on a **rejected** item,
so it is in `EXCLUDED.tsv`, not the ledger: it is evidence of the pattern's reach, not a fifth unit of
work — and the precative sheet's own applicable notes are already applied (§2), so no article edit is
owed there. The first policy's five notes span only four sheets because `future` contributes two.

### 3.4 Applying a `RESEARCH` note

```
1. Do NOT edit the disputed number.
2. Write a probe spec: what would settle it, against which DCS release.
3. Run the probe; verify adversarially (the H1229 discipline).
4. Only if verified: edit, and cite both the probe and the note in the revision row.
5. If unresolved this wave: ledger = DEFERRED with the probe stub linked.
```

### 3.5 Applying a `QUESTION` note

Answer only from in-repo evidence. Otherwise write the `@DECIDE` into
[`Uprava/GTD_NEXT_ACTIONS.md`](https://github.com/gasyoun/Uprava/blob/main/GTD_NEXT_ACTIONS.md)
with the note quoted verbatim, and set ledger status `ESCALATED`. A decision ask is two paragraphs —
what is lacking, and the trade-offs — never a one-liner.

### 3.6 Notes with an external-source dependency

Three notes need material that may not be on disk. Check before starting; if absent, `DEFERRED`,
not invented:

| Note | Needs |
|---|---|
| `[zan-07]` apte | `index_Shertsl_Byuler_dopoln_180721` in [`BuhlerLeitfaden_1923/`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923) |
| `[zan-19]` apte | Elizarenkova, *Аорист в Ригведе* — scan posted to the Society, not necessarily in-repo |
| `[B1]` declension | Elizarenkova 2004 PDF, `SanskritGrammar/Elizarenkova_2004` |
| `[WF06]`, `[HK-34]`, `[zan-32]` | Leitan's samāsa lecture notes — [`codebook_leitan.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/tatpurusha/data/codebook_leitan.md) is the in-repo starting point |

## 4. W2-A — charter de-calendaring

| Step | Detail |
|---|---|
| 1 | Replace the mermaid gantt (≈ lines 129–141) with a gate/dependency diagram — no dates |
| 2 | Rewrite the five wave headings (≈ lines 150–186): `### W2 · 2027–2028 · Морфология` → `### W2 · Морфология`, each with an "opens when / closes when" contract |
| 3 | Restate the 30-06-2031 success condition (line 109) as a checkpoint condition, not a deadline |
| 4 | Restate R6's English-locale trigger as a contract condition |
| 5 | Revision-history row stating the calendar was removed **because production overtook it by ~2 years** — W2 core closed 19/19 and nine W3-programme SE articles shipped in July 2026, against a charter that dated W2 to 2027–2028 |

Keep the title, slug (`/sangram/charter-2026-2031`) and filename — the slug is published; only the
internal calendar goes.

## 5. W2-B — ACL roadmap re-basing

| Step | Detail |
|---|---|
| 1 | Open with Sangram as the product; the two ACL papers are its publication arm (ruling 4: keep both) |
| 2 | Demote S1–S4 from workstreams to **instruments** that feed Sangram articles |
| 3 | State that the S1 τ and S5 κ results are already cited inside Sangram articles — the papers productionise analyses that exist as one-offs |
| 4 | Update the [`Uprava/ROADMAP_INDEX.md`](https://github.com/gasyoun/Uprava/blob/main/ROADMAP_INDEX.md) row |

## 6. Hub sync — required, same pass

| Hub | Update |
|---|---|
| [`Uprava/GTD_NEXT_ACTIONS.md`](https://github.com/gasyoun/Uprava/blob/main/GTD_NEXT_ACTIONS.md) | Every `ESCALATED` note; the 3-item re-vote `@DECIDE`; the A61 contradiction |
| [`Uprava/REVIEW_SHEETS_INDEX.md`](https://github.com/gasyoun/Uprava/blob/main/REVIEW_SHEETS_INDEX.md) | All 13 sheets registered, now tracked and citable by blob URL |
| [`Uprava/FINDINGS.md`](https://github.com/gasyoun/Uprava/blob/main/FINDINGS.md) | The `claims.json` false-positive trap (§2 rank 4) — it will bite any future note-status grep |
| `CHANGELOG.md` | `[Unreleased]` entry per handoff, then `/cut-release` |
| `.ai_state.md` | WIP → Completed as each handoff lands |

_Dr. Mārcis Gasūns_
