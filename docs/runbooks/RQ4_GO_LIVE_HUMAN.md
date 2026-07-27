# RQ4 go-live — human operator checklist (n≈5 pilot)

_Created: 27-07-2026 · Last updated: 27-07-2026_

> **Fence, read first:** agents prepare docs and code only. **No agent recruits, contacts, or
> enrols a participant. No agent flips the production `RQ4_STUDY` flag. No agent alters the
> consent wording below — it is reproduced byte-identical from the approved protocol.** This
> document is an operator checklist for a **human**, not an execution script an agent may run
> unattended.

This is the **execution runbook** for the already-ruled RQ4 pilot (on-ramp-first vs
Талмуд-first). It does not redesign the study — every decision below is already closed in
[docs/RQ4_EVALUATION_PROTOCOL_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RQ4_EVALUATION_PROTOCOL_2026.md)
§6 and the go-live ruling
[H1261](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1261-Sonnet_Systema-Sanscriticum_rq4-study-go-live_18.07.26.md).
This runbook only sequences the human steps that ruling still requires.

## Preflight

1. **R20 cabinet non-collision window — hard sequencing gate.** Systema's student-cabinet
   hybrid (R29/R20) began its ≥14-day production baseline on **21-07-2026**
   ([DEPLOY_QUEUE #25](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/DEPLOY_QUEUE.md)),
   closing **04-08-2026**. RQ4 recruitment must **not** open before that baseline window closes,
   and must never draw from the **28-08-2026 R20 marathon cohort** — that population is reserved
   for the cabinet-baseline measurement and is off-limits as an RQ4 recruitment source (R-5,
   [PLAN_SYSTEMA_GETCOURSE_PARITY_WAVE1_2026H2.md](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/docs/PLAN_SYSTEMA_GETCOURSE_PARITY_WAVE1_2026H2.md)).
   No arm-aware RQ4 segmentation may leak into R20 analytics, in either direction. This is a hard
   gate, not a preference — do not flip the flag while the baseline window is open or while the
   marathon cohort is the only reachable population.
2. **Cohort = Kochergina-stage only.** Recruitment population is Systema-Sanscriticum's own
   Kochergina-stage students (finished or nearly finished a first-year course, not yet exposed to
   Zaliznyak's classification) — ruled §6.1, reconfirmed 16-07-2026 against the "open call"
   alternative. No other population substitutes.
3. **Consent — verbatim, no revisions.** Approved 16-07-2026 (MG),
   [H1009](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1009-Sonnet_SanskritGrammar_rq4-consent-approved-gates-closed_16.07.26.md):

   > Это исследование — часть работы Общества ревнителей санскрита над тем, как лучше учить
   > санскриту. Вам будет показан один из двух вариантов введения в тему рядов/типов корней, затем
   > короткий тест (несколько вопросов), и ещё раз — через 4 недели, без дополнительных материалов
   > между тестами. Участие добровольное, результаты используются обезличенно (для анализа, не для
   > оценки успеваемости). В любой момент можно выйти без объяснения причин.

   Byte-identical to protocol §6.4. Do not edit a word of it, in either repo.
4. **Harness flag currently OFF.** `features.rq4_study` reads `env('RQ4_STUDY', false)` in
   [config/features.php](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/config/features.php) —
   default OFF, unset on prod as of this writing. Route `/rq4-study` 404s until a human sets it.
5. **Item bank.** [`TolchelnikovTalmud_2026/data/rq4_item_bank.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/rq4_item_bank.json)
   (built by [`build_rq4_item_bank.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/tools/build_rq4_item_bank.py),
   H984) — 24 items, 3 phases × 8, 4 on-ramp rows, 2 per row per phase, zero shortfall. This is the
   vendored copy Systema's harness reads; do not regenerate it as part of go-live.

## Day-of (human)

1. **Flag key:** `RQ4_STUDY` (env var) → `config('features.rq4_study')`. **Who may flip:** whoever
   holds prod SSH/deploy credentials (Ivan, per [H478](https://github.com/gasyoun/Uprava/blob/main/GTD_NEXT_ACTIONS.md));
   agents do not have this access (a permissions restriction, not a hosting limitation).
2. **Staging → prod order** (exact commands, from
   [DEPLOY_QUEUE #26](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/DEPLOY_QUEUE.md)
   and [Systema issue #599](https://github.com/gasyoun/Systema-Sanscriticum/issues/599)):
   1. `php artisan migrate` — additive `rq4_participants`/`rq4_responses` tables (safe alongside
      the rest of the deploy batch; no data loss risk to existing tables).
   2. Set `RQ4_STUDY=true` in `.env`.
   3. `php artisan config:clear`.
   4. Confirm server cron invokes `schedule:run` (already a dependency of several other live
      features — same check as DEPLOY_QUEUE items #4/#5/#13/#16/#21).
   5. Smoke-test with **one throwaway account not from the 28-08 marathon cohort**: `/rq4-study`
      loads consent → intake → arm assignment; `/admin/rq4-study-dashboard` (admin/super_admin)
      shows the new participant.
3. **Recruit → enrol → pre/post diagnostic** (cite protocol, nothing invented here): a human
   contacts eligible Kochergina-stage students per the approved consent text above; each accepted
   participant is randomised 1:1 stratified by prior-exposure at intake
   ([protocol §2](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RQ4_EVALUATION_PROTOCOL_2026.md#2-design));
   the harness administers the pre-test at intake and the post-test immediately after the arm
   completes, both drawn from the vendored 24-item bank
   ([protocol §4](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RQ4_EVALUATION_PROTOCOL_2026.md#4-the-diagnostic-instrument)).
   No new metric or item may be introduced at this step — the instrument is frozen.

## Retention T+4 weeks

- Retention window is **4 weeks** (§6.2, ruled 15-07-2026) — not 2, not both.
- Reminder path: the scheduled command
  [`rq4:send-retention-reminders`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/app/Console/Commands/SendRq4RetentionReminders.php),
  already registered in `Kernel.php` to run daily at 09:00; it fires automatically once server
  cron calls `schedule:run` (step 2.4 above) — no separate human action needed to schedule it,
  only to confirm the cron dependency is live.
- The retention-test diagnostic draws a **different** held-out item set from the same 4 rows,
  same difficulty band (protocol §4) — administered with no further study material sent in
  between, per the consent text.

## Stop rules

- **Target n≈5** for this wave — a pilot, not a powered study
  ([protocol §7](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RQ4_EVALUATION_PROTOCOL_2026.md#7-recommended-first-step-a-pilot-not-the-full-study)).
  Do not over-recruit past this target chasing significance — the honest power calculation
  (protocol §5) needs ~64/arm, which this pilot is not attempting.
- **Abort conditions** (from the deploy rollback contract, DEPLOY_QUEUE #26): migration failure,
  duplicate enrolment, missing item bank, scheduler silence, or any sign of cohort-isolation
  breach (an R20 marathon-cohort account appearing as an RQ4 participant). On any of these:
  `RQ4_STUDY=false` in `.env` → `php artisan config:clear` — the route 404s again immediately.
  **Do not roll back the migration** — already-collected `rq4_participants`/`rq4_responses` rows
  are study data, not deploy artifacts, and must not be dropped.
- Never claim a powered confirmatory result from this wave, in any interim report.

## After

- Pilot results (completion rate, floor/ceiling effects on the instrument, rough
  time-on-task/effect-size estimates) land in **A32**
  ([Uprava/ARTICLES.md](https://github.com/gasyoun/Uprava/blob/main/ARTICLES.md) row — "P6
  Frequency-graded reading layer", elevated as RQ4's evaluation paper) and in a RESULTS doc in
  this repo, reported explicitly as a **pilot**, never as a powered confirmatory result
  (protocol §5, §7).
- Close the GTD `@DO` row for the prod flag flip
  ([Uprava/GTD_NEXT_ACTIONS.md](https://github.com/gasyoun/Uprava/blob/main/GTD_NEXT_ACTIONS.md))
  once the flip + smoke-test above are confirmed done, citing the deploy evidence (migration
  output, smoke-test result, dashboard screenshot/URL).

---

_Dr. Mārcis Gasūns_
