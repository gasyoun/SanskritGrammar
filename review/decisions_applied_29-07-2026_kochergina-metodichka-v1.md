# Decisions applied — sanskritgrammar-metodichka-kochergina-v1_16.07.26 (12 approve / 1 reject / 0 defer)

_Created: 29-07-2026 · Last updated: 29-07-2026_

Audit record closing the human vote on the Kochergina-1998 companion methodichka v1 visa
(H807 slice), applied via
[`/decisions-apply`](https://github.com/gasyoun/claude-config/blob/main/commands/decisions-apply.md)
Phase 2b (visa mode). **This session applied nothing new: the sheet was already fully
folded in.** It exists because no `decisions_applied_*` audit record had ever been written
for this sheet, which is why the hub still carried it as unapplied. Verification pass:
Opus 5 (`claude-opus-5[1m]`), 29-07-2026, 13/13 items PASS.

- **Decisions file:** [`review/sanskritgrammar-metodichka-kochergina-v1_16.07.26_decisions.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/sanskritgrammar-metodichka-kochergina-v1_16.07.26_decisions.json)
  (voted 16-07-2026, 13/13 decided, 12 carrying substantive notes).
- **Sheet:** [`review/sanskritgrammar-metodichka-kochergina-v1_16.07.26_review.html`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/sanskritgrammar-metodichka-kochergina-v1_16.07.26_review.html)
  (generated 16-07-2026, Fable 5 `claude-fable-5`, H807).
- **Consumer (pipeline):** the three v1 manuscript files —
  [`METODICHKA_KOCHERGINA_V1_KOMMENTARII_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_V1_KOMMENTARII_2026.md)
  (раздел I),
  [`METODICHKA_KOCHERGINA_V1_UPRAZHNENIIA_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_V1_UPRAZHNENIIA_2026.md)
  (раздел II),
  [`METODICHKA_KOCHERGINA_V1_OTSYLKI_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_V1_OTSYLKI_2026.md)
  (раздел III) — plus the cross-sheet ledger
  [`review/EDITORIAL_NOTE_INDEX.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/EDITORIAL_NOTE_INDEX.tsv).

## Counts

| Verdict | Count |
|---|---:|
| approve → substantive note folded into a manuscript | 11 |
| approve → no note (nothing owed; section stands as written) | 1 (`zan-16`) |
| reject → marked not print-ready, **not** rewritten | 1 (`zan-10`) |
| defer | 0 |
| unvoted | 0 |
| **total** | **13** |

All 13 item ids match the sheet 1:1 — no unknown ids, no unvoted items, no orphan rows.
Applied **this session: 0** — every disposition was already landed by earlier passes (below).

## Where the work actually landed (three prior passes)

| Pass | Handoff | Commit / PR | What it did |
|---|---|---|---|
| 1 | [H1258](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1258-Sonnet_sanskritgrammar_apply-sanskritgrammar-metodichka-kochergina-v1_16.07.26-decisions_18.07.26.md) (Sonnet 5 `claude-sonnet-5`) | `7463cbe`, PR #508, 22-07-2026 | folded 10 of the 12 approved notes into the three manuscripts; marked `zan-10` REJECT in разделы I + II; consolidated the not-yet-researchable notes into an "Открытые вопросы визы" appendix rather than inventing answers |
| 2 | H1258 follow-up (Sonnet 5 `claude-sonnet-5`) | `d185ee3`, PR #509, 22-07-2026 | caught two notes the first pass read off the card render instead of the JSON — `zan-18` (Талмуд on the j/h → k/ṣ reflex) and `zan-22` (causative share of the periphrastic perfect) — added as open items |
| 3 | [H1454](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1454-Fable_SanskritGrammar_kochergina-metodichka-v1-open-items_22.07.26.md) (Grok 4.5 `grok-4.5`) | `06a3d00`, 26-07-2026 | terminalized all nine appendix open items with `APPLIED` / `DEFERRED` / `ESCALATED` / `re-sheeted` statuses + evidence, and wrote the matching `EDITORIAL_NOTE_INDEX.tsv` rows |

A fourth commit, `fafec02` (PR #548, H1758, Fable 5 `claude-fable-5`, 28-07-2026), was a
Russian-prose style pass over all five Kochergina methodichka files — it rewrote the
administrative phrasing of the visa notes but changed no number and no verdict.

## Per-item disposition (verified 29-07-2026)

| item_id | Vote | What MG's note asked for | Where it lives now |
|---|---|---|---|
| `razdel-1-frame` | approve | "фактически точен — вряд ли": 750+ typos in the 2015 printing, ≥50 in 2024, plus in-lesson material reordering | KOMMENTARII § "Что покрывает и чего не покрывает вердикт «фактически точен»"; routed to `errata.yml` + a v2 note. Index: **DEFERRED** (`errata.yml` still empty — no print sheet, K-1 edition pin unresolved) |
| `zan-06` | approve | count how many of the described cases are unaccented, so the rule's real reach is known; useless in practice since almost everything is in śloka | KOMMENTARII Занятие VI open question. Index: **DEFERRED** — DCS surface IAST carries zero accent marks (full `0.csv` scan), no accent flag in `verify_claims_dcs.py` |
| `zan-10` | **reject** | «Обе формулировки не очень понятны, хотя я учебник читал 60 раз» | Both notes (-ā gender; imperfect-as-narrative) headed `⟦MG-viza: REJECT, H1258 — не готово в печать⟧` in разделы I and II. **Not rewritten** — draft candidates A/B parked and put to a fresh one-card visa, [`sanskritgrammar-metodichka-kochergina-zan10-rewrite_26.07.26`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/sanskritgrammar-metodichka-kochergina-zan10-rewrite_26.07.26_review.html), still unvoted. Index: **re-sheeted** |
| `zan-12` | approve | footnote naming which three frequency strata really build the feminine | KOMMENTARII Занятие XII open question + committed ending-proxy probe [`hk16_feminine_ending_probe_h1454.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/hk16_feminine_ending_probe_h1454.json). Index: **DEFERRED** — the three morphological layers are not derivable from DCS `lemma.grammar`, so the footnote is not printed |
| `zan-16` | approve | (empty note) | Nothing owed. KOMMENTARII Занятие XVI stands as written; no index row, matching the convention for empty-note items |
| `zan-18` | approve | «Согласен ли Талмуд, что тут нет четкого распределения?» | KOMMENTARII Занятие XVIII § "Сверка с «Талмудом»". Index: **APPLIED** — Talmud gives a cascade of rules 18–29 plus root lists, i.e. **not** "no rule"; the note was corrected accordingly |
| `zan-21` | approve | every such claim must carry a reference to the FULL list — long-vowel roots going periphrastic, and the aniṭ class ("десятки, not несколько") | KOMMENTARII Занятие XXI, both halves: Whitney §§ 1070–1071 and §§ 797–801 cited as the exhaustive lists, plus Gasuns-2014 and [WhitneyRoots](https://github.com/gasyoun/WhitneyRoots). Index: **APPLIED** |
| `zan-22` | approve | is this mainly a causative phenomenon, or do other derived stems matter too? | KOMMENTARII Занятие XXII § "Разбивка по типу основы" + committed [`hk_peri_formation_share_h1454.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/hk_peri_formation_share_h1454.json): ≈93 % class-10/-aya, ≈4 % denominative, desiderative/intensive ≈ 0. Index: **APPLIED** |
| `zan-30` | approve | «пользовать» is not a Russian word — here «употреблять» is best | KOMMENTARII Занятие XXX: «Пользуйтесь правилом посуффиксно» → «Употребляйте правило посуффиксно». Index: **APPLIED** |
| `zan-32` | approve | Leitan published a critique of exactly these samāsa lessons; far from the only inaccuracy there | KOMMENTARII Занятие XXXII: the *dvigu* locus citing Kochergina 1994 Занятие XXXII located in `SamasaChakram/leitan/…konspekt…txt`. Index: **APPLIED**, with a residual escalation to the author if the critique he means is a wider publication |
| `zan-37` | approve | agreed, but no need to memorize — outside the Ṛgveda these never turn up | KOMMENTARII Занятие XXXVII: rarity caveat added (0,31 % of verbal word-forms; roots beyond gam/sthā/dā/bhū almost exclusively Vedic/Ṛgvedic; recognize the type, don't drill the list). Index: **APPLIED** |
| `zan-39` | approve | Kochergina's own doctoral dissertation covers this, plus the 1990 monograph built on it | Citation-only entry in OTSYLKI Занятие XXXIX (dissertation 1983; *Словообразование…*, МГУ 1990) + a pointer in KOMMENTARII. The monograph's **content** was not checked against the wording — no text in the org. Index: **APPLIED** |
| `razdel-3-otsylki` | approve | Конспект-2004 by section **and** page number; later add Miller | OTSYLKI header § "Пункты визы автора (H1258…)". Index: **ESCALATED** on both halves — (a) no paginated Konspekt PDF/scan exists in the repo, shadow assets, or `DATA_LAYERS_CENSUS.md`, so page numbers cannot be derived; (b) which Miller and which work is unspecified, and guessing is barred |

## What could NOT be applied, and why

Nothing was blocked by this session's own reading of the votes — the rejected item and the
deferred/escalated halves of approved items are blocked on inputs no model can supply:

1. **`zan-10` (the one reject)** — MG's note diagnoses both formulations as unclear but does
   not say what they should say. Visa mode does not re-author; the rewrite went to its own
   one-card sheet and is **still unvoted**. This is the sheet's only genuinely open verdict.
2. **`razdel-1-frame`, `zan-06`, `zan-12`** — deferred on missing data: an errata source
   sheet / edition pin, an accented Vedic layer, and a morphological three-way split that
   DCS does not carry. Each has committed evidence of the attempt rather than a fabricated
   answer.
3. **`razdel-3-otsylki` (both halves)** — escalated to the author: a paginated Konspekt
   source, and the identity of "Миллер".

## Leftovers

No pipeline work is owed. The human residuals are already listed in KOMMENTARII
§ "Открытые вопросы визы (H1258) — residual после H1454" (two `@DO` for sources, three
`@DECIDE`), and the live decision is the unvoted `zan10-rewrite` sheet. The only gap this
session closed is the missing audit record itself.

## Reproduce

From a checkout of `main`, against
[`review/sanskritgrammar-metodichka-kochergina-v1_16.07.26_decisions.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/sanskritgrammar-metodichka-kochergina-v1_16.07.26_decisions.json):

```
grep -n "H1258\|MG-viza" KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_V1_KOMMENTARII_2026.md \
                         KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_V1_OTSYLKI_2026.md \
                         KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_V1_UPRAZHNENIIA_2026.md
grep "kochergina-v1_16.07.26" review/EDITORIAL_NOTE_INDEX.tsv | cut -f3,6
```

Expected: a residue anchor for each of the 12 noted items in the manuscripts (`zan-16`
carries no note and owes none), and 12 index rows whose `applied_status` column reads
6 × `APPLIED`, 3 × `DEFERRED`, 1 × `re-sheeted`, 2 × `ESCALATED`.

_Dr. Mārcis Gasūns_
