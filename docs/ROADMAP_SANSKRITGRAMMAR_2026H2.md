# Roadmap — SanskritGrammar, second half of 2026

_Created: 18-07-2026 · Last updated: 18-07-2026_

Wave structure and full handoff specs for the plan whose cover is
[`docs/PLAN_SANGRAM_EDITORIAL_NOTES_AND_CHARTER_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANGRAM_EDITORIAL_NOTES_AND_CHARTER_2026H2.md).

## 1. Wave shape

Waves here are **gated on contracts, not dates** — the same principle this plan applies to the
charter (ruling 3). A wave opens when its entry contract is satisfiable and closes when its
acceptance gate passes.

| Wave | Opens when | Closes when |
|---|---|---|
| **W1 · Editorial debt** | The 81 applicable notes are extracted into a tracked note index | All **60** open notes are terminal — applied, deferred with a reason, or escalated as `@DECIDE` — with H1274 (22) + H1275 (8) + H1276 (9) = 39 here, plus H1257 (10) + H1258 (11) = 21 in concurrent handoffs, summing to exactly 60; `review/` is tracked |
| **W2 · Governance** | W1 ledger exists (charter/roadmap rewrites cite real production numbers) | Charter carries no calendar years; ACL roadmap is Sangram-primary |
| **W3 · Instrumented pilot** | Systema's R20 cabinet-baseline window is closed | n≈5 pilot has run and reported honestly as a pilot |

W1 and W2 are parallel-safe (disjoint files). W3 is serialised behind an external repo's schedule.

## 2. Handoff specs

Tier derivation is load-bearing — [`next_task_scan.py`](https://github.com/gasyoun/Uprava/blob/main/tools/next_task_scan.py)
routes on the filename model token. Mechanical → Sonnet/Haiku · correctness-critical design → Opus ·
register-sensitive Russian editorial → Fable.

### W1-A · `sangram-editorial-note-ledger-build`

> **Minted as [H1273](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1273-Sonnet_SanskritGrammar_sangram-review-votes-track-h856-reversal_18.07.26.md), re-scoped.**
> The ledger half was dropped — [H1260](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1260-Sonnet_SanskritGrammar_sangram-consolidation-policy-ledger_18.07.26.md)
> owns the Sangram article-disposition ledger. H1273 keeps the `review/` tracking + H856 reversal and
> a deliberately-renamed per-note **index**. See the disposition table in the plan's §4.

| Field | Value |
|---|---|
| Tier | **Sonnet** — deterministic parse, file move, gitignore edit; no Russian judgment |
| Repo | SanskritGrammar |
| Deliverable | (a) `review/EDITORIAL_NOTE_INDEX.tsv` — one row per applicable note; (b) `.gitignore` line 23 `/review/` removed; (c) `docs/DECISION_RECORD_REVIEW_TRACKING_H856_REVERSAL.md` |
| Human gate | none |
| Acceptance | Index has exactly **81** rows; the 6 non-applicable items appear in a separate `review/EDITORIAL_NOTE_INDEX_EXCLUDED.tsv` with their disposition; `git status` shows all 13 `decisions.json` + 9 `review.html` as tracked additions; the decision record names H856 and states the reversal rationale |

Ledger columns: `note_uid · sheet_id · item_id · decision · target_file · applied_status ·
note_class · note_ru`. `note_uid` = `<sheet_id>#<item_id>` — stable, and the only thing that survives
if a sheet HTML is lost again. `applied_status` is emitted as `UNKNOWN` by this handoff; W1-B fills it.

> This handoff performs the ruling-2 gitignore reversal. It must **not** silently edit `.gitignore` —
> the decision record is part of the deliverable, and the commit message must reference the H856
> reversal explicitly.

### W1-B · `sangram-editorial-note-applied-adjudication`

| Field | Value |
|---|---|
| Tier | **Fable** — reading Russian article prose and Russian notes to judge "has this been addressed" |
| Repo | SanskritGrammar |
| Deliverable | `applied_status` filled for all 81 rows: `APPLIED` / `OPEN` / `PARTIAL`, each with an evidence pointer |
| Human gate | none |
| Acceptance | Zero `UNKNOWN` remain; every `APPLIED`/`PARTIAL` row cites a revision-history line or article section; the total `OPEN` count is reported and reconciled against this plan's count of **60**, with any divergence explained |

Known-applied anchors to start from, verified this session: `future` cites MO021-01/02/03/04/05/07 in
its revision row; `causative` cites MO028-05/07/08/09; `taddhita-overview` cites TAD2-01/03/04;
`precative` P1/P4/P5 landed on `origin/main` in commit `3b4f9e4`
([PR #416](https://github.com/gasyoun/SanskritGrammar/pull/416), H1253) — HK-39 `mg_footnote`, OCH-3
`number`, OCH-30 `number` + `mg_footnote`, all three cited in the two `CHANGELOG.md` files;
`a-stems` records visa edits in prose without ids. `perfect` records the visa but **not** the edits —
its notes are largely open, except A7, whose substance became
[`SANGRAM_STYLE_GUIDE_PROSE_RU.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/editorial/SANGRAM_STYLE_GUIDE_PROSE_RU.mdx).

### W1-C · `sangram-editorial-notes-apply-articles`

| Field | Value |
|---|---|
| Tier | **Fable** — applying author's editorial notes to Russian grammar prose, in the author's register |
| Repo | SanskritGrammar |
| Deliverable | **32** open notes applied: `declension-overview` (8), `w2-core` cluster (10), `perfect` (4), the prose style guide (4), `sg-wf-004-taddhita` (5 — WF004-05/-06/-08/-09/-10), `sg-wf-004-taddhita-revisa` (1 — TAD2-08) |
| Human gate | none for application; any note requiring a *new* corpus number escalates |
| Acceptance | All 32 are terminal (`APPLIED`/`DEFERRED`/`ESCALATED`); each applied note leaves a revision-history row citing `sheet_id` + `item_id`; no published DCS figure changed; every note classed `RESEARCH` in the ledger is deferred with a probe stub, not guessed |

> **Both taddhita sheets belong to this handoff.** `sg-wf-004-taddhita` and its re-visa
> `sg-wf-004-taddhita-revisa` are distinct sheets with distinct id families (`WF004-*` vs `TAD2-*`) that
> share one target article. An earlier draft of this spec covered only the revisa sheet's TAD2-08 while
> quoting `[WF004-10]` as representative in-scope work — leaving that sheet's five open notes unowned.
> They are owned here.

Representative work in scope, quoted from the votes:
- `[A2] declension-overview` — «предмет кластера „Композиты“ → привычнее Сложные слова»: terminology change.
- `[A3] declension-overview` — «дательный реже всех (2,2 %) — не просто реже, а почти не засвидетельствован»: a hedging/register fix, **not** a number change.
- `[MO26] w2-core` — «-ya/-tya на 97,8 % — так сколько -ya и сколько -tya? 5 частотных примеров для каждого»: needs a corpus split → probe, then apply.
- `[A7] declension-overview`, `[WF004-10] taddhita` — both attack invented jargon («осиротевший пин», «подмножество EM5»). These are a single cross-cutting register defect; fix the vocabulary repo-wide, not per-article.

### W1-D · `sangram-editorial-notes-apply-metodichki`

| Field | Value |
|---|---|
| Tier | **Fable** — pedagogical companion prose in Russian |
| Repo | SanskritGrammar |
| Deliverable | **19** open notes applied: Apte (8) + Kochergina (11) |
| Human gate | The Likhushina translation note asserts permission exists — an agent may widen usage but must not assert the rights basis in print without the human confirming scope |
| Acceptance | Each note applied with a revision row; the Scherzl government data is actually consulted, not merely cited |

Two notes here are the highest-value in the whole set:
- `[razdel-1-frame] apte` — «перевод Лихушиной цитируется минимально — зря, нужно использовать максимально, есть разрешение».
- `[zan-07] apte` — use `index_Shertsl_Byuler_dopoln_180721` in [`BuhlerLeitfaden_1923/`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923) to add Bühler + Scherzl government data.
- `[razdel-1-frame] kochergina` — corrects a published claim that the textbook is «фактически точен»: the author states 750+ typos in the 2015 edition, ≥50 in 2024. This *contradicts a shipped statement* and should be applied first.

### W1-E · `sangram-a65-claim-notes-apply`

| Field | Value |
|---|---|
| Tier | **Fable** — claim-level scholarly adjudication in Russian |
| Repo | SanskritGrammar |
| Deliverable | 9 open notes on the A65 verdict-validation disagreements applied to the claim registries |
| Human gate | none |
| Acceptance | Each `HB-*`/`HK-*` note resolves to its row in [`BuhlerLeitfaden_1923/claims.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims.json) or [`KocherginaUchebnik_1998/claims.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/claims.json) and its verdict/footnote is updated there |

Contains two standing-policy notes that must be lifted out of the article layer and into the style
guide / method doc rather than applied locally: `[HK-4b]` «Всегда верить Витни, сверить все
утверждения всех грамматик с Витни» and `[HB-100]` «только у Зализняка вся правда, ее надо проверить
отдельной гипотезой на DCS» — the latter explicitly asks for a **hypothesis**, i.e. a probe, not an edit.

### W2-A · `sangram-charter-decalendar-rewrite`

> **NOT minted — deferred, 18-07-2026.** [H1260](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1260-Sonnet_SanskritGrammar_sangram-consolidation-policy-ledger_18.07.26.md) §5
> is concurrently editing the charter to document the consolidation freeze. The de-calendar ruling
> stands and is re-minted once H1260 lands; two sessions rewriting the same constitution at once is
> the H214 pattern this org guards against.

| Field | Value |
|---|---|
| Tier | **Fable** — the project's constitution, in Russian, register-critical |
| Repo | SanskritGrammar |
| Deliverable | [`sangram/SANGRAM_CHARTER_2026_2031.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_CHARTER_2026_2031.mdx) rewritten: waves become sequential milestones gated on contracts + checkpoints, all calendar years removed |
| Human gate | none |
| Acceptance | No wave carries a year range; the mermaid gantt (lines ~129–141) is replaced by a dependency/gate diagram; the revision history states the calendar was removed **because production overtook it by ~2 years**; R6's English-locale trigger is restated as a contract condition, not a date |

The measured contradiction driving this: the charter dates W2 to 2027–2028 and W3 to 2028–2029
behind a July-2028 checkpoint. In July 2026, W2 core closed 19/19 and nine W3-programme SE articles
shipped. The document's title and slug (`charter-2026-2031`) may stay — retitling breaks the published
slug; only the internal calendar goes.

### W2-B · `sangram-acl-roadmap-rebase-on-sangram`

| Field | Value |
|---|---|
| Tier | **Fable** — research strategy narrative |
| Repo | SanskritGrammar |
| Deliverable | [`ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md) rewritten with Sangram primary; S1–S4 demoted to instruments feeding it |
| Human gate | none |
| Acceptance | The string "Sangram" occurs (it currently occurs **zero** times, while `sangram/` is essentially all the output); both ACL papers survive as the publication arm (ruling 4 — keep both); the S1 τ and S5 κ results are described as *already cited inside Sangram articles*, so the papers productionise existing one-off analyses; the [Uprava/ROADMAP_INDEX.md](https://github.com/gasyoun/Uprava/blob/main/ROADMAP_INDEX.md) row is updated |

### W3-A · `sangram-rq4-consent-pilot-n5-design`

> **NOT minted — superseded, 18-07-2026.** [H1261](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1261-Sonnet_Systema-Sanscriticum_rq4-study-go-live_18.07.26.md)
> records a same-day ruling of **GO now** — activate and recruit under the unchanged approved
> protocol, "never alter the protocol". A human ruled that H1261 governs, so the n≈5 pilot is not
> built. This section is retained as the record of a superseded ruling, not as work.

| Field | Value |
|---|---|
| Tier | **Opus** — human-subjects exposure; correctness-critical, and scheduling-sensitive |
| Repo | SanskritGrammar |
| Deliverable | An **execution runbook** for an n≈5 pilot — not a new design |
| Human gate | **Launch is human-only.** No agent recruits participants or sends the consent text to anyone |
| Acceptance | The runbook consumes the settled decisions rather than re-deriving them; states the R20 non-collision window; defines pilot stopping rules; specifies that results are reported as a pilot in A32, never as a powered result |

> **Scope correction, verified this session.** The brief framed this as designing the instrument and
> consent flow. Both already exist and are *ruled*:
> [`docs/RQ4_EVALUATION_PROTOCOL_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RQ4_EVALUATION_PROTOCOL_2026.md)
> §6 records all four `@DECIDE`s closed — recruitment = Systema's Kochergina-stage students,
> retention N = 4 weeks, hosting = Systema-hosted flow (harness merged, Systema PR #536), and §6.4
> consent wording **approved verbatim 16-07-2026 with no revisions**. §7 already recommends a pilot
> rather than the full study, so ruling 5 confirms an existing recommendation. The item bank (24
> items) exists as [`rq4_item_bank.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/rq4_item_bank.json).
> Re-designing any of this would be duplicate work.

**Consent handling, stated explicitly** (this is the repo's only human-subjects exposure): the
approved Russian consent paragraph is used **verbatim**; participation is voluntary and
anonymous-to-analysis; participants are told what is measured and that a second contact follows at
4 weeks. An agent may prepare the flow; only a human may run it against real students.

**The collision the pilot must respect:** Systema's R20 cabinet baseline was already ruled to
serialise against the **same** student population. The pilot must not recruit into that window —
this is a hard sequencing constraint, not a preference, and W3 does not open until R20's window closes.

## 3. Out of scope, with reasons

| Item | Why not this wave |
|---|---|
| Visa sheet for the unpublished candidates | Ruling 1 — they stay unpublished this wave |
| A61 branch consolidation | Ruling 6 — human-gated; two live Codex worktrees |
| H1243 Wackernagel + Renou columns | Ruling 7 — blocked on MG supplying both PDFs; a human `@DO` |
| H1242 Bühler + Zaliznyak v2 grid | Proceeds independently in its own live worktree |
| Registry reconciliation | Inherited from **H1252** ([Uprava-wide, all 170 rows](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1252-Opus_Uprava_registry-lifecycle-state-reconciliation_18.07.26.md); depends on H1247/H1248/H1251). Not re-minted here, and no wave-1 gate blocks on it |
| Precative sheet notes | Already applied on `origin/main` (`3b4f9e4`, [PR #416](https://github.com/gasyoun/SanskritGrammar/pull/416), H1253). 0 open — no handoff owns it |

_Dr. Mārcis Gasūns_
