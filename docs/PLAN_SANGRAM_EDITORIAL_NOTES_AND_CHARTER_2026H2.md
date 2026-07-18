# Plan — Sangram editorial notes, charter de-calendaring and roadmap re-basing (2026 H2)

_Created: 18-07-2026 · Last updated: 18-07-2026_

**This is the cover/index** of a layered plan covering the second half of 2026 in
[SanskritGrammar](https://github.com/gasyoun/SanskritGrammar). Its subject is the unapplied
author-visa editorial backlog held in [`review/`](https://github.com/gasyoun/SanskritGrammar/blob/main/review),
plus three structural corrections to the project's own governing documents
(charter, roadmap, review-artifact tracking).

**Goal in one paragraph.** Between 15-07 and 18-07-2026 the author cast visas on thirteen review
sheets and left substantive editorial notes in the margin of a large fraction of them. Those notes
are the highest-value unexploited asset in the repo: they are the author's own scholarly judgment on
already-published articles, and they currently live in untracked local-only files. Wave 1 turns them
into a tracked, addressable, provenance-preserving worklist and applies the open ones; in the same
wave the charter is rewritten to drop a calendar that production overtook by ~2 years, and the ACL
roadmap is re-based on Sangram as the product.

## Layer docs

| Layer | Document |
|---|---|
| Roadmap (waves, gates) | [`docs/ROADMAP_SANSKRITGRAMMAR_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_SANSKRITGRAMMAR_2026H2.md) |
| Architecture (note → worklist item → revision) | [`docs/ARCHITECTURE_SANGRAM_EDITORIAL_NOTE_PIPELINE.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ARCHITECTURE_SANGRAM_EDITORIAL_NOTE_PIPELINE.md) |
| Implementation (step-by-step, per note) | [`docs/IMPLEMENTATION_SANGRAM_EDITORIAL_NOTES.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/IMPLEMENTATION_SANGRAM_EDITORIAL_NOTES.md) |
| Verification (acceptance gates) | [`docs/VERIFICATION_SANGRAM_EDITORIAL_NOTES.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_SANGRAM_EDITORIAL_NOTES.md) |
| This doc's companion record | [`docs/PLAN_SANGRAM_EDITORIAL_NOTES_AND_CHARTER_2026H2.meta.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANGRAM_EDITORIAL_NOTES_AND_CHARTER_2026H2.meta.md) |

## 1. Measured ground truth

Every number below was re-derived this session by parsing the thirteen
`*_decisions.json` files directly. **Three premises carried into this plan from the phase-1 audit did
not survive that parse** — they are corrected here and the corrections are load-bearing.

| # | Briefed premise | Measured reality | Consequence |
|---|---|---|---|
| 1 | "Every decision is `approve`" | 114 approve · **3 `reject`** · 3 `null` | Rejects carry notes too. Those notes are *rejection rationale*, not forward work |
| 2 | "87 notes are real unapplied forward work" | 87 notes total, but only **81** sit on approved items; of those **21 are already applied** — 18 at visa time (logged in revision-history rows) and 3 landed on `origin/main` on 18-07-2026 by [PR #416](https://github.com/gasyoun/SanskritGrammar/pull/416) (H1253) | The genuine open backlog is **60**, not 87 |
| 3 | "14 articles carry the «Статья-кандидат» banner" | The string occurs in all 35 articles — because *published* articles keep historical candidate rows in their revision tables | Banner-grep is not a status signal; status must be read from the top-of-article status line |

### 1.1 The 120 → 60 funnel

| Stage | Count | Note |
|---|---|---|
| Voted items across 13 sheets | 120 | |
| …carrying a non-empty note | 87 | |
| …on an **approved** item (applicable) | **81** | 3 notes sit on rejects, 3 on undecided |
| …not yet reflected in the article | **60** | 21 applied: 18 at visa time + 3 by [PR #416](https://github.com/gasyoun/SanskritGrammar/pull/416) (H1253, 18-07-2026) |

### 1.2 Per-sheet ledger

`applicable` = approve + non-empty note. `applied` = cited in a revision-history row, in a merged
commit, or otherwise evidenced in the article. The `items`/`notes`/`applicable` columns are exact —
re-parsed from the 13 vote files at `origin/main` 3b4f9e4. The applied/open split is evidence-based but
of uneven strength: `precative` (3) rests on a merge commit and is conclusive, the rest on
revision-history rows; it remains the gated output of wave-1 step 1.

| Sheet (`review/…_decisions.json`) | items | notes | applicable | applied | **open** | sheet HTML |
|---|---:|---:|---:|---:|---:|---|
| `sangram-prose-style-guide-visa_16.07.26` | 10 | 4 | 4 | 0 | **4** | orphan |
| `sangram-sg-mo-001-declension-overview-visa_16.07.26` | 8 | 8 | 8 | 0 | **8** | present |
| `sangram-sg-mo-002-a-stems-visa_15.07.26` | 7 | 3 | 3 | 3 | 0 | orphan |
| `sangram-sg-mo-017-perfect-visa_15.07.26` | 8 | 5 | 5 | 1 | **4** | orphan |
| `sangram-w2-core-11candidates-visa_17.07.26` | 12 | 10 | 10 | 0 | **10** | present |
| `sanskritgrammar-a65-verdict-validation-disagreements_16.07.26` | 9 | 9 | 9 | 0 | **9** | orphan |
| `sanskritgrammar-metodichka-apte-v1_17.07.26` | 9 | 9 | 8 | 0 | **8** | present |
| `sanskritgrammar-metodichka-kochergina-v1_16.07.26` | 13 | 12 | 11 | 0 | **11** | present |
| `sanskritgrammar-precative-label-dcs2026-visa_17.07.26` | 7 | 4 | 3 | 3 | 0 | present |
| `sanskritgrammar-sg-mo-021-future_visa` | 9 | 7 | 7 | 7 | 0 | present |
| `sanskritgrammar-sg-mo-028-causative_visa` | 10 | 4 | 4 | 4 | 0 | present |
| `sanskritgrammar-sg-wf-004-taddhita-revisa_visa` | 8 | 4 | 4 | 3 | **1** | present |
| `sanskritgrammar-sg-wf-004-taddhita_visa` | 10 | 8 | 5 | 0 | **5** | present |
| **Total** | **120** | **87** | **81** | **21** | **60** | 4 orphan |

> **Precative sheet — re-derived 18-07-2026 against `origin/main` 3b4f9e4.** This sheet is closed, not
> open. [PR #416](https://github.com/gasyoun/SanskritGrammar/pull/416) (H1253, Sonnet 5
> `claude-sonnet-5`) applied policy B for all three applicable notes: P1's footnote caveat and P5's
> pada-untagged caveat via
> [`KocherginaUchebnik_1998/claims.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/claims.json)
> HK-39 `mg_footnote`, and P4's whole-mood re-label via
> [`ZalizniakOcherk_1978/claims.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/claims.json)
> OCH-3 `number` and OCH-30 `number` + `mg_footnote`. P6 is the rejected item and was explicitly **not**
> applied (§1.3). One residual sub-request inside P4 — «зачем на английском, SANGAM пишем на русском
> языке», aimed at the English-language `number` field — was not acted on and is a schema-wide register
> question, not a note-level edit; it is folded into the style-guide track, not counted as an open note.

### 1.3 The six non-applicable items — explicit disposition

Ruling 1 asks that the 3 undecided items be handled explicitly. Parsing surfaced 3 more that are
equally non-applicable (notes on rejects), so all six are dispositioned here.

| Sheet | id | decision | Disposition |
|---|---|---|---|
| `metodichka-apte-v1` | `zan-29` | `null` | Re-vote. Note proposes deriving P/Ā from observable forms + the Sa–Ru corpus — a research question, not an edit |
| `sg-wf-004-taddhita` | `WF004-03` | `null` | Re-vote. Asks to widen beyond DCS to dictionaries/grammars |
| `sg-wf-004-taddhita` | `WF004-04` | `null` | Re-vote. Challenges the premise that `-tā` is confusable with pronoun `tā` |
| `metodichka-kochergina-v1` | `zan-10` | `reject` | No action. Rationale: both formulations unclear — a re-draft request against the item, not the article |
| `precative-label-dcs2026` | `P6` | `reject` | No action *now*; the note's substance (register complaint) is absorbed by the style-guide track |
| `sg-wf-004-taddhita` | `WF004-07` | `reject` | **Blocked, not dead.** Rationale is literally «Сперва надо учесть все мои прежние оговорки» — it re-enters the queue once the other taddhita notes land |

> The three `null` items cannot be applied by any agent: an undecided item has no author instruction
> to execute. They are routed to a micro re-vote sheet, which is a human `@DECIDE`, not wave-1 work.

## 2. Decisions taken

Seven human rulings (18-07-2026) plus one default applied without asking. "Overturned" marks where
the ruling contradicted the phase-1 batch recommendation.

| # | Decision | Ruling | Overturned batch? |
|---|---|---|---|
| 1 | Wave-1 scope | Apply the editorial notes **only**. No visa sheet for the unpublished candidates this wave | **Yes** — batch recommended doing both |
| 2 | `review/` tracking | Track the **whole** `review/` directory — sheets *and* votes. Reverses H856 | **Yes** — reverses a standing ruling |
| 3 | Charter | Rewrite as sequential milestones gated on contracts + checkpoints, **no calendar years** | No |
| 4 | Roadmap | **Keep both.** Sangram is the product; Track C's two ACL papers are its publication arm | **Yes** — batch leaned to retiring one |
| 5 | RQ4 user study | Small **pilot, n≈5**, to validate instrument + consent flow only | **Yes** — batch proposed the full study |
| 6 | A61 | Human-gated. `codex/a61-sol-evidence` supersedes `codex/a61-history-argument` | No |
| 7 | H1243 (Wackernagel + Renou) | Human `@DO` — MG supplies both PDFs. H1242 proceeds independently | No |
| D | Registry reconciliation | **Default, applied without asking:** execute already-minted **H1252**, do not mint a duplicate | n/a |

### 2.1 Ruling 2 — why this is urgent, with evidence

The votes are currently untracked on one machine. A `git clean -xfd` or a drive failure erases every
author visa cast since 15-07-2026 — 120 adjudicated items representing the only record of the
author's scholarly sign-off. This session found the loss has *already partially occurred*: **4 of 13
sheets have no surviving `_review.html`**, so their item IDs cannot be resolved back to the text
that was voted on. The four are `prose-style-guide`, `sg-mo-017-perfect`, `sg-mo-002-a-stems` and
`a65-verdict-validation`, and they do **not** split two-and-two:

| Orphan sheet | ID form | Recoverable how | Open notes at risk |
|---|---|---|---|
| `prose-style-guide` | positional `A1`–`A9`/`B1` | Match note text against article prose | 4 |
| `sg-mo-017-perfect` | positional `A1`–`A7`/`B1` | Match note text against article prose | 4 |
| `sg-mo-002-a-stems` | positional `A1`–`A6`/`B1` | Same problem, but moot — all 3 notes already applied | 0 |
| `a65-verdict-validation` | domain `HB-*` **and** `HK-*` in one sheet | Resolves against the claim registries | 9 (referent safe) |

So **three** of the four orphans use positional ids with no external registry — leaving **8 open notes
whose referent must be recovered by matching note text against article prose** (`prose-style-guide` 4 +
`perfect` 4; `a-stems`'s 3 are already applied, so nothing is at risk there). Only **one** orphan,
`a65-verdict-validation`, survives with resolvable ids — and it is a single sheet carrying **both** id
families, resolving against
[`BuhlerLeitfaden_1923/claims.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims.json)
(403 claims, the `HB-*` ids) and
[`KocherginaUchebnik_1998/claims.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/claims.json)
(260 claims, the `HK-*` ids). That is luck, not design.

The H856 reversal is recorded as a decision record, not a silent `.gitignore` edit — see
[the architecture doc, §5](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ARCHITECTURE_SANGRAM_EDITORIAL_NOTE_PIPELINE.md).

### 2.2 Ruling 6 — A61 canonicity and the unresolved contradiction

`codex/a61-sol-evidence` supersedes `codex/a61-history-argument` **on content, not by ancestry** — and
the distinction is load-bearing, because acting on a false ancestry belief is how a commit gets
discarded.

Measured (18-07-2026): `git merge-base --is-ancestor codex/a61-history-argument codex/a61-sol-evidence`
exits **1** — not an ancestor. The two branches diverged at `072443d`. `history-argument` carries one
commit, `d43fb38`; `sol-evidence` starts from a *distinct* commit `35d932f` that merely reuses the same
subject line («ai-wip: rebuild A61 around a causal history argument») on a newer base (`26d2b6f`), then
adds `7906d62` and `87a41fa`. What makes sol-evidence dominant is a content fact, verified separately:
`d43fb38` and `35d932f` are **patch-identical** (`git patch-id --stable` agrees; the `MumbaiWSC_2027/`
trees at the two commits diff to nothing), so sol-evidence carries the same A61 rebuild plus two further
commits. A second drift to know about: the local branch tip is `87a41fa` while
`origin/codex/a61-sol-evidence` is two commits ahead (`69b0de8`, `bc8ccde` — the H1222 voice pass), so
the live worktree is not the published state either.

> **Consequence for whoever closes this out.** `codex/a61-history-argument` will never show as merged to
> any ancestry-based check, and deleting it drops `d43fb38` from the ref graph. That is safe *only*
> because the patch-identity above was measured — it must be re-measured, not assumed, at close-out
> time. Both branches also still have live Codex worktrees checked out on them.

Recorded alongside the above, unresolved: the
handoff registry marks **H1222** (Fable author-voice pass) ✅ finished, while draft **PR #403**'s body
says the author pass "follows by formal handoff". One of the two is wrong and **a human decides which**.

> No agent handoff in this plan touches A61 or those branches, and no wave-1 step enters
> `.codex-worktrees/a61-history-20260718` or `.codex-worktrees/a61-sol-20260718` — both are live
> Codex sessions.

### 2.3 The default, logged

Registry reconciliation runs as **H1252**
([registry-lifecycle-state-reconciliation](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1252-Opus_Uprava_registry-lifecycle-state-reconciliation_18.07.26.md)),
already minted, filled, and carrying a row in
[`Uprava/handoffs/README.md`](https://github.com/gasyoun/Uprava/blob/main/handoffs/README.md) — but it is
**Uprava-wide, not SanskritGrammar-scoped**: its title is "reconcile all 170 active handoff rows", and it
declares `Depends on: H1247, H1248, H1251`. This plan therefore *inherits* the fix from H1252; it does not
own it, and nothing here blocks on H1252 completing.

> **Read the registry from `origin/main`, not a local clone.** The Uprava working clone used while drafting
> was 74 commits behind, and at that HEAD H1252's file was still an unfilled `mint_handoff.py` stub with no
> registry row. Both defects were already fixed upstream. Any claim about registry state that is not read
> from `git show origin/main:handoffs/README.md` is worthless.

**The dispatch hazard, re-derived 18-07-2026 against `origin/main`.** The specific figure the phase-1
audit offered — "13 rows in 🟡 describing merged work, PRs #382–#413" — is **not derivable** and is
withdrawn: there is no PR-number citation in any 🟡 SanskritGrammar row, and that PR range is stale
(#415 and #416 have merged since). The derivable statement, with its method:

| Measurement | Value | Method |
|---|---|---|
| SanskritGrammar rows in the registry | 201 | `git show origin/main:handoffs/README.md`, table rows matching `H\d{3,4}` and `SanskritGrammar` |
| …carrying 🟡 «Yet to be launched» | **68** rows / **67** distinct H-ids | H1227 is double-rowed |
| …whose H-id is cited by at least one commit on SanskritGrammar `origin/main` | **51** | `git log origin/main --format=%H%x01%s%x02%b`, word-boundary match per id |
| …with no such commit | 16 | genuinely unlaunched, or launched without citing the id |

So **51 of 67** 🟡-advertised SanskritGrammar handoffs have demonstrably already run — a live
`/next-task` dispatch hazard of the H919 duplicate-build class, an order of magnitude larger than the
audit's "13". The commit-citation test is a lower bound on landed work (it misses handoffs whose commits
never named the id), not a verdict on any single row; per-row adjudication is H1252's job, under its own
rule of re-reading each handoff's deliverables list.

**Terminal-but-unarchived SanskritGrammar rows: four, not five, and only one is ✅.**

| Handoff | Registry status | File location |
|---|---|---|
| H1012 | ⚫ RETIRED (H214-class duplicate of H1008) | `handoffs/` — unarchived |
| H984 | 🔴 CLOSED 17-07-2026 (found already done) | `handoffs/` — unarchived |
| H1222 | ✅ EXECUTED 18-07-2026 | `handoffs/` — unarchived |
| H1228 | 🔴 EXECUTED 18-07-2026 | `handoffs/` — unarchived |

H1065 was listed in error and is struck: it is a **WhitneyRoots** handoff, not SanskritGrammar, and it is
**already archived** at
[`handoffs/archive/H1065-Opus_WhitneyRoots_alternation-type-induction-nonpaninian_16.07.26.md`](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1065-Opus_WhitneyRoots_alternation-type-induction-nonpaninian_16.07.26.md).

Of the four stranded rows the audit flagged, **two** still need reclassifying — H773 (builds paper A60,
merged into A65 on 16-07, so its deliverable no longer exists; still 🔵) and H386 (still 🔵, plan
delivered, restructure deferred). The other two were already reclassified upstream: H967 now reads
⚫ SUPERSEDED and H385 now reads ✅ with its PR merged. None of these is re-minted.

> **Correction to the phase-1 audit, recorded so it does not propagate:** the audit claimed the stale
> "Next free ID" marker would make the next mint collide. It will not.
> [`mint_handoff.py`](https://github.com/gasyoun/Uprava/blob/main/tools/mint_handoff.py) takes
> `max()` over files on disk in both `handoffs/` and `archive/` *and* the marker, so minting is
> collision-safe. The marker's staleness is a documentation and dispatch defect only.

## 3. Autonomy contract

| Boundary | Rule |
|---|---|
| Write scope | Only inside the executing worktree. Never the shared main tree. **Foreign worktrees are enumerated by rule, never by list** — run `git worktree list` and treat every entry other than the main tree and your own as foreign and untouchable, then `ls -d ../SanskritGrammar-*` for same-pattern directories git no longer tracks. A closed list is the wrong shape for a hazard that grows: the four-item list drafted for this plan already missed two registered worktrees (`.codex-worktrees/roadmap-sanskritgrammar-20260718`, `.claude/worktrees/agent-afd4e9eb320e94171` on `feat/talmud-h995-phase4-answer-keys`) and two unregistered on-disk dirs (`SanskritGrammar-h917`, `SanskritGrammar-mo023`) |
| Numbers | No published DCS figure may be altered to satisfy a note. A note that disputes a number opens a probe → verify cycle; it never edits the number in place |
| Author voice | Notes are applied in the author's register. An agent may not invent scholarly positions the note does not contain |
| Escalation | A note that is a *question to the author* is answered with evidence if the evidence exists in-repo, otherwise it becomes an `@DECIDE`, never a guess |
| Human gates | The 3 undecided items, the A61 contradiction, and H1243's PDF supply are human-only |
| Provenance | Every applied note leaves a revision-history row citing sheet id + item id. Losing that link is a defect |

## 4. Wave-1 handoffs

Full specs in [the roadmap](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_SANSKRITGRAMMAR_2026H2.md).
Tier follows the derivation rule: mechanical → Sonnet/Haiku; correctness-critical design → Opus;
register-sensitive Russian editorial → Fable.

> **⚠️ Re-scoped at mint time, 18-07-2026.** This section was authored against a repo state that four
> handoffs minted the same day by concurrent sessions had already changed. The plan was cut down to
> what no one else owns rather than minted as drafted — the `mint_handoff.py` collision guard caught
> the first overlap, and a manual sweep found three more it could not see. **Five** handoffs were
> minted, not eight. The originally-drafted `…-ledger-build`, `…-charter-decalendar-rewrite` and
> `…-rq4-consent-pilot-n5-design` were **not** minted; see the disposition table below.

| ID | Slug | Deliverable | Tier | Gated on |
|---|---|---|---|---|
| [H1273](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1273-Sonnet_SanskritGrammar_sangram-review-votes-track-h856-reversal_18.07.26.md) | `sangram-review-votes-track-h856-reversal` | Track `review/` (reverse H856) + per-note open/applied **index** | Sonnet | — |
| [H1274](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1274-Fable_SanskritGrammar_sangram-apply-notes-articles-remainder_18.07.26.md) | `sangram-apply-notes-articles-remainder` | **22** open notes across the article set + style guide (`w2-core` excluded) | Fable | H1273 |
| [H1275](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1275-Fable_SanskritGrammar_sangram-apply-notes-metodichka-apte_18.07.26.md) | `sangram-apply-notes-metodichka-apte` | **8** open notes on the Apte companion (Kochergina excluded) | Fable | H1273 |
| [H1276](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1276-Fable_SanskritGrammar_sangram-apply-notes-a65-claims_18.07.26.md) | `sangram-apply-notes-a65-claims` | **9** open claim-level notes on the A65 verdict set | Fable | H1273 |
| [H1277](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1277-Fable_SanskritGrammar_sangram-acl-roadmap-rebase-primary_18.07.26.md) | `sangram-acl-roadmap-rebase-primary` | ACL roadmap re-based with Sangram primary, S1–S4 demoted to instruments | Fable | — |

**Disposition of the three drafted-but-unminted handoffs:**

| Drafted | Disposition | Why |
|---|---|---|
| `…-editorial-note-ledger-build` | **folded into H1273** as a *note index*, deliberately renamed | [H1260](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1260-Sonnet_SanskritGrammar_sangram-consolidation-policy-ledger_18.07.26.md) owns the Sangram **article-disposition ledger** under the same directory. Different objects — editorial notes vs article dispositions — but the mint guard flagged the slug overlap, correctly. H1273 keeps the vote-tracking half, which no other handoff claims. |
| `…-charter-decalendar-rewrite` | **deferred** | H1260 §5 edits the charter to document the 18-07 consolidation freeze. Two handoffs rewriting the same constitution concurrently is the H214 pattern. The de-calendar ruling stands and is re-minted after H1260 lands. |
| `…-rq4-consent-pilot-n5-design` | **dropped — superseded** | [H1261](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1261-Sonnet_Systema-Sanscriticum_rq4-study-go-live_18.07.26.md) records a same-day ruling of **GO now** — activate and recruit under the unchanged approved protocol, "never alter the protocol". A human ruled H1261 governs; the n≈5 pilot ruling of §2 is superseded and is retained there only as record. |

**Coverage is exhaustive and closed — across all owners, not just this plan.** The 60 open notes of
§1.2 are fully owned; three sheets belong to concurrent handoffs and are excluded here by design:

| Owner | Sheets | Open notes |
|---|---|---:|
| **H1274** (W1-C) | `sg-mo-001-declension-overview` 8 · `sg-mo-017-perfect` 4 · `prose-style-guide` 4 · `sg-wf-004-taddhita` 5 · `sg-wf-004-taddhita-revisa` 1 | **22** |
| **H1275** (W1-D) | `metodichka-apte-v1` 8 | **8** |
| **H1276** (W1-E) | `a65-verdict-validation-disagreements` 9 | **9** |
| [H1257](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1257-Sonnet_sangram_apply-sangram-w2-core-11candidates-visa_17.07.26-decisions_18.07.26.md) — concurrent | `w2-core-11candidates` 10 | **10** |
| [H1258](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1258-Sonnet_sanskritgrammar_apply-sanskritgrammar-metodichka-kochergina-v1_16.07.26-decisions_18.07.26.md) — concurrent | `metodichka-kochergina-v1` 11 | **11** |
| — (closed sheets, nothing to own) | `a-stems` 0 · `sg-mo-021-future` 0 · `sg-mo-028-causative` 0 · `precative-label-dcs2026` 0 | 0 |
| **Total** | 13 sheets | **60** |

22 + 8 + 9 = **39** owned by this plan; 10 + 11 = **21** owned by concurrent handoffs; 39 + 21 = **60**.
The precative sheet owns none because it has none left (applied by
[PR #416](https://github.com/gasyoun/SanskritGrammar/pull/416)); the 6 non-applicable items of §1.3
are excluded by construction, not unowned.

_Dr. Mārcis Gasūns_
