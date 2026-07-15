_Created: 15-07-2026 · Last updated: 15-07-2026_

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

A short (recommend 8–10 item) held-out derivation test: given a root's citation form + tense/mood
target, the learner names its Ряд, Тип, and seṭ/aniṭ status (the on-ramp's own "one derivation"
success criterion). Items drawn from **DCS-attested roots outside** the on-ramp's worked set (the
on-ramp uses the 4 high-frequency A₁/I₁/U₁/R₁ rows) and outside talmud-02's own worked examples —
a genuinely novel-to-both-arms item pool, so neither arm has a memorisation advantage from its own
material. Same instrument (fresh item draw, matched difficulty) at pre-test, post-test, and
retention-test — three item sets total, item-response-matched (same Ряд/Тип distribution across
sets), not the identical items (avoids simple repetition effects).

**Item bank build:** derivable now from Appendix 1's 65 DCS-top roots (already Ряд/Тип/seṭ-tagged)
— excluding the on-ramp's and talmud-02's worked examples — no new data collection needed for the
item pool itself.

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

## 6. Open `@DECIDE` items (a human should decide before recruitment starts)

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
   Society's own voice, not a generic boilerplate).

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
| 65 DCS-top roots, Ряд/Тип/seṭ-tagged (item-bank source) | Talmud Appendix 1 |
| RQ4 is the field's falsifiability backbone | [`docs/VERIFICATION_DIGITAL_SANSKRIT_PEDAGOGY.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_DIGITAL_SANSKRIT_PEDAGOGY.md) |
| Site has zero analytics/instrumentation today | checked `docusaurus.config.mjs` while scoping this protocol (15-07-2026) |
| Systema has real user accounts + contact channel | [Systema-Sanscriticum `StudentController`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/app/Http/Controllers/StudentController.php) et al. |

---

_Dr. Mārcis Gasūns_
