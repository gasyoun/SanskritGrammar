_Created: 15-07-2026 · Last updated: 16-07-2026_

# RQ4 evaluation protocol — does the Zaliznyak on-ramp teach faster and retain better than Талмуд-first?

Full study design for [RQ4](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md)
("A tool's teaching effect is measurable via learning-gain + retention user studies"), the digital-Sanskrit-pedagogy
field's falsifiability backbone per [`docs/VERIFICATION_DIGITAL_SANSKRIT_PEDAGOGY.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_DIGITAL_SANSKRIT_PEDAGOGY.md).
First concrete arm, per the [A62 outline](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/DigitalPedagogyAgenda_A62/OUTLINE_digital-sanskrit-pedagogy-agenda_A62.md)
§4: **on-ramp-first vs Талмуд-first**, over the already-built testbed
([`TolchelnikovTalmud_2026/onramp/`](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026/onramp), W1c/H915).

> **This is a protocol spec, not a running study.** Per the field's own build-vs-reuse verdict
> ("Evaluation harness (user study) — BUILD"), this document specifies the design; the harness
> (instrumentation) and the actual recruitment/run are separate, later steps — several of which
> are `@DECIDE` items for a human (§6).

> **§6 FULLY RULED — recruitment = Systema-Sanscriticum's own Kochergina-stage students, not open
> call** (§6.1, RULED 15-07-2026, MG reconfirmed 16-07-2026 after a re-ask against the "open call"
> option — the harness at [H987](https://github.com/gasyoun/Uprava/blob/main/handoffs/H987-Sonnet_Systema-Sanscriticum_rq4-study-harness_15.07.26.md)
> already assumes real, retention-contactable Systema accounts, so the ruling stands); retention
> window N = **4 weeks** (§6.2, RULED 15-07-2026); hosting/instrumentation home = **Systema-hosted
> flow** (§6.3, RULED 15-07-2026) — harness built and merged, [Systema PR #536](https://github.com/gasyoun/Systema-Sanscriticum/pull/536).
> **§6.4 (consent wording) APPROVED 16-07-2026 (MG)** — the draft in [H987](https://github.com/gasyoun/Uprava/blob/main/handoffs/H987-Sonnet_Systema-Sanscriticum_rq4-study-harness_15.07.26.md)
> is finalised as-is, no revisions ([H1009](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1009-Sonnet_SanskritGrammar_rq4-consent-approved-gates-closed_16.07.26.md)).
> **All four §6 `@DECIDE` gates are now closed — nothing blocks recruitment except flipping the
> `features.rq4_study` flag on (a separate launch decision, not yet made).** §6 items below are
> kept as the historical record of the decision; the ruling lives at the top of each.

## 1. Hypothesis (falsifiable)

**H0:** Learners who start with the on-ramp (3 steps, minimal-notation, 4 high-frequency rows)
before the full Талмуд show **no difference** in (a) time-to-first-correct-derivation and
(b) retention at N weeks, compared to learners who start directly with the full Талмуд.

**H1:** On-ramp-first learners reach first-correct-derivation faster and/or retain better at N
weeks than Талмуд-first learners.

Falsification condition: H1 is rejected if the on-ramp-first cohort shows no statistically
significant improvement on either metric (§3) at the pre-registered α.

## 2. Design

**Between-subjects, two-arm, matched cohorts** (not within-subject — the on-ramp's whole point is
first-contact framing, which a learner can't experience twice naively).

| Arm | Path |
|---|---|
| **A — On-ramp-first** | `onramp/index` → step-1 → step-2 → step-3 → (bridge) full Талмуд §II (talmud-02) |
| **B — Талмуд-first** | Full Талмуд §I–II directly (talmud-00/01/02), on-ramp never shown |

**Matching variable:** prior Sanskrit exposure, self-reported on intake (none / Kochergina-stage /
beyond). Per the on-ramp's own design doc, the on-ramp targets **Kochergina-stage learners
specifically** — a complete beginner has no Ряд/Тип/seṭ vocabulary to "ramp" from, and an
already-advanced learner has nothing to gain from either arm. **Recommended inclusion criterion:
Kochergina-stage learners only** (finished or nearly finished a first-year Sanskrit course, not yet
exposed to Zaliznyak's classification) — this is itself an `@DECIDE` (§6.1).

**Assignment:** randomised at intake, stratified by the matching variable, 1:1 allocation.

## 3. Metrics

1. **Time-to-first-correct-derivation** — wall-clock time from arm start to the first fully
   correct derivation of a held-out root's Ряд/Тип/seṭ triple on the diagnostic instrument (§4),
   for a root **not** used as a worked example in either arm's material (avoids teaching-to-the-test).
2. **Retention @ N weeks** — accuracy on the same diagnostic instrument (different held-out roots,
   same difficulty band), administered again after a fixed delay with no further study material sent.
   **N is an `@DECIDE`** (§6.2) — the field's own research-agenda doc gives no default; 2 and 4
   weeks are the common L2-acquisition-literature range and are the recommended options.

Both metrics are diagnostic-instrument scores, not self-report — self-reported confidence is
explicitly *not* a primary metric (a known confound in L2 pedagogy studies: on-ramp material may
raise confidence without raising accuracy).

## 4. The diagnostic instrument

A short (8 item) held-out derivation test: given a root's citation form, the learner names its
Ряд, Тип, and seṭ/aniṭ status (the on-ramp's own "one derivation" success criterion). Same
instrument shape (fresh item draw per phase, matched difficulty) at pre-test, post-test, and
retention-test — three item sets total, item-response-matched (same 2-per-row distribution across
the 4 rows in every set), not the identical items (avoids simple repetition effects).

**Scope restriction (documented, not hidden):** items are drawn **only from the 4 ablaut rows the
on-ramp itself teaches** (A₁/I₁/U₁/R₁ — `AblautMachine`'s `rows` whitelist for the on-ramp).
Testing a row the on-ramp never covers would not be a fair on-ramp-vs-Талмуд comparison, since
only the Талмуд-first arm would have seen material for it — this instrument measures "did the
on-ramp's framing help you learn/retain *this specific, on-ramp-scoped* content faster," not
generalisation to the full 13-row matrix (a separate, harder question, out of scope for this
first arm).

**Item bank ✅ BUILT 15-07-2026 (H984):**
[`TolchelnikovTalmud_2026/data/rq4_item_bank.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/rq4_item_bank.json),
built by [`TolchelnikovTalmud_2026/tools/build_rq4_item_bank.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/tools/build_rq4_item_bank.py)
from the full 745-root Приложение 1 catalogue (`data/talmud_appendix1.json`), restricted to the 4
on-ramp rows, **excluding** every root already used in the on-ramp's/talmud-02's own worked
material (`data/widget_roots.json`'s `ablaut_examples` + `set_examples`), requiring complete
Ряд+Тип+seṭ tags and no homonym ambiguity. 307 eligible candidates found; 24 items drawn (8 per
phase × 3 phases, 2 per row), frequency-sorted via kosha's `lemma_frequency.tsv` `rank_all` within
each row so the most plausibly-already-encountered roots are used first. Zero shortfall on any
row.

## 5. Analysis plan (pre-registered, per falsifiability)

- **Metric 1 (time-to-first-correct):** two-sample test (Mann-Whitney U, since completion-time
  distributions are typically right-skewed — not assumed normal) on arm A vs arm B.
- **Metric 2 (retention accuracy):** two-sample test on post-delay diagnostic score, controlling
  for post-test (immediately-after) score as a covariate (ANCOVA) — isolates *retention decay*
  from *initial learning gain*, since the two arms may differ on one metric but not the other.
- **Effect size** reported alongside p-values (Cohen's d or rank-biserial correlation) — a
  significant-but-tiny effect should be reported as such, not oversold.
- **Attrition:** retention-test non-completion is itself a data point (differential attrition
  between arms would bias the retention comparison) — report completion rate per arm, don't just
  drop non-completers silently.
- **Sample size:** not computed here — depends on the recruitment population size (§6.1), which is
  an open `@DECIDE`. A rough power-analysis placeholder: detecting a medium effect (d≈0.5) at
  α=0.05, power=0.8, two-tailed, needs ~64 per arm (128 total) for metric 1; retention (metric 2,
  ANCOVA-adjusted) typically needs somewhat fewer for the same power given the covariate. **This
  is almost certainly more participants than a first pilot will recruit** — treat wave 1 as a
  **pilot** (§7), not a properly powered confirmatory study, and say so honestly in any resulting
  paper (A32).

## 6. `@DECIDE` items — ✅ ALL RULED (nothing blocks recruitment but the launch flag)

**§6.1–6.3 RULED 15-07-2026 (MG):** Systema-hosted, Systema's own Kochergina-stage students
(not open call — reconfirmed 16-07-2026), 4-week retention. **§6.4 APPROVED 16-07-2026 (MG):**
the draft consent text below (from the harness handoff,
[H987](https://github.com/gasyoun/Uprava/blob/main/handoffs/H987-Sonnet_Systema-Sanscriticum_rq4-study-harness_15.07.26.md))
is finalised as-is.

1. **Recruitment population + channel** — Systema-Sanscriticum's own Kochergina-stage students
   (has real accounts + a channel to reach them, but conflates "student of this specific school"
   with "Sanskrit learner" as a construct) vs Общество ревнителей санскрита's broader course
   population vs an open call. This also decides feasibility of retention follow-up (an existing
   student account can be re-contacted; an anonymous public respondent may not return).
2. **Retention window N** — 2 weeks vs 4 weeks vs both (adds a third measurement wave, more power
   needed).
3. **Hosting / instrumentation home** — the on-ramp lives on SanskritGrammar's **static** Docusaurus
   site (no accounts, no backend, zero instrumentation today, confirmed while scoping this
   protocol). Three options: (a) build a minimal standalone diagnostic-quiz tool (e.g. a small
   Systema-hosted flow reusing its existing account system, since Systema already has real user
   accounts and a channel for follow-up contact — mirrors the last-mile pipeline's own kosha↔Systema
   division of labour: SanskritGrammar/kosha hold the *content*, Systema is the *product* surface
   that can actually run a study with real, contactable users); (b) an external tool (Google Forms
   / Typeform) for the diagnostic + a manual email-based retention follow-up, fastest to stand up
   but weaker instrumentation (no automatic timing capture for metric 1); (c) do nothing until a
   human picks (a) or (b) — **recommended default is (a)** for the reasons above, but this is the
   single highest-leverage `@DECIDE` in this protocol, since it determines what code (if any) gets
   built next.
4. **Consent / ethics framing** — this is a small-scale pedagogical study, not clinical research,
   but participants should still see a plain-language one-paragraph explanation of what's measured
   and that participation is voluntary/anonymous-to-analysis. Exact wording is a human call (the
   Society's own voice, not a generic boilerplate). **APPROVED 16-07-2026 (MG), no revisions:**

   > Это исследование — часть работы Общества ревнителей санскрита над тем, как лучше учить
   > санскриту. Вам будет показан один из двух вариантов введения в тему рядов/типов корней, затем
   > короткий тест (несколько вопросов), и ещё раз — через 4 недели, без дополнительных материалов
   > между тестами. Участие добровольное, результаты используются обезличенно (для анализа, не для
   > оценки успеваемости). В любой момент можно выйти без объяснения причин.

## 7. Recommended first step: a pilot, not the full study

Given the sample-size gap (§5) and the open `@DECIDE`s (§6), the honest recommendation is a
**small pilot** (target: whatever the chosen recruitment channel can plausibly deliver in one
cohort, likely well under the ~64/arm power target) to (a) validate the diagnostic instrument
doesn't have floor/ceiling effects or ambiguous items, (b) get a real completion-rate and
time-on-task estimate to size a follow-up confirmatory run, and (c) surface any on-ramp UX issues
before a larger run. Report the pilot honestly as a pilot in A32 — not as a powered confirmatory
result.

## 8. Traceability

| Claim in this protocol | Backing |
|---|---|
| On-ramp testbed exists, 3 steps, targets Kochergina-stage | [`ZALIZNYAK_ONRAMP_DESIGN.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/ZALIZNYAK_ONRAMP_DESIGN.md) |
| 745-root catalogue, Ряд/Тип/seṭ-tagged (item-bank source) | [`data/talmud_appendix1.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/talmud_appendix1.json) |
| Item bank (24 items, 3 phases, 4 rows, 0 shortfall) | [`data/rq4_item_bank.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/rq4_item_bank.json) (H984) |
| RQ4 is the field's falsifiability backbone | [`docs/VERIFICATION_DIGITAL_SANSKRIT_PEDAGOGY.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_DIGITAL_SANSKRIT_PEDAGOGY.md) |
| Site has zero analytics/instrumentation today | checked `docusaurus.config.mjs` while scoping this protocol (15-07-2026) |
| Systema has real user accounts + contact channel | [Systema-Sanscriticum `StudentController`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/app/Http/Controllers/StudentController.php) et al. |

---

_Dr. Mārcis Gasūns_
