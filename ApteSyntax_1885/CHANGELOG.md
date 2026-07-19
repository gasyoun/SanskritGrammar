# Changelog — ApteSyntax_1885

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- **Apte-methodichka viza notes brought to final written disposition — all 8 approved notes closed (H1275, Fable 5 `claude-fable-5`).**
  New «Ревизии правок визы» table in
  [`METODICHKA_APTE_KOMMENTARII_2026.md`](METODICHKA_APTE_KOMMENTARII_2026.md) records
  APPLIED/DEFERRED/ESCALATED per `item_id`. (1) The three «оговорить в сноске» notes
  (zan-03/19/22) now use real `[^n]` Markdown footnotes (decision recorded: the manuscript takes
  true footnotes — the author asked «в сноске» three times, the site build renders GFM footnotes,
  precedent throughout `Apte-unicode.mdx`); body prose kept. (2) Likhushina direct quotes widened
  to every visaed lesson (§ 63 зан-7, full §§ 94/98 зан-9, § 113 зан-10, full § 258 зан-22) —
  still confined to the formulation of the commented rule; the closing rights paragraph untouched;
  appendix summary rows stay paraphrase (author's structural call). (3) Adversarial re-check of
  the Sherzl cross-references against
  [`government_lexicon.jsonl`](../BuhlerLeitfaden_1923/government_class_index/government_lexicon.jsonl)
  caught and fixed three H1205 citation defects: krudh «acc.» (not in the lexicon — dat./gen./loc.
  only), ruc «ТОЛЬКО» (an example-only instr. record exists, p. 121), muc's missing dat. 160
  (→acc.) + the preverb gloss («loc./acc./dat.» → loc.-example replaceable by dat.). (4) Registry
  sync: aorist rarity in зан-19 «Учащемуся» 0,31 % → ~2,3 % per the H1136 refresh already in
  `claims.yml`/`CLAIMS_VERIFIED.md` (probe `whitney_aorist_tagger.py`, H1134) — the manuscript
  lagged its own register; APT-31 verdict unchanged. Deferred with named blockers: Елизаренкова
  scan (zan-19, needs MG's file — @DO in GTD), uta dashboard (zan-22) and cross-book calibration
  list (prilozhenie) — both separate features under the 18-07-2026 consolidation freeze. zan-29
  (vote null) escalated to a re-vote @DECIDE, its section untouched.

## [0.12.0] - 2026-07-17
### Changed
- **MG viza applied to the print methodichka раздел I (8/9 approve, 1 unvoted).** Ran
  `apply_apte_methodichka_visa.py --apply` against `review/sanskritgrammar-metodichka-apte-v1_
  17.07.26_decisions.json` — every section now carries its verdict marker + a summary table.
  Substantive viza notes actioned: (razdel-1-frame) permission confirmed to cite the Likhushina
  translation more fully — Занятие 3 § 30 and Занятие 19 §§ 207/210 now carry direct quotes, not
  paraphrase; (zan-07/zan-09, «а как Шерцль?») cross-checked ruc/krudh/druh and kṣip/muc/snih
  against the `index_Shertsl_Byuler_dopoln_180721.xlsx` Sherzl/Bühler government index — Шерцль
  independently corroborates the ruc-dative and kṣip/snih-locative attestations, and shows
  krudh/druh already carrying variant government in the 19th-century index (explains the corpus's
  sub-1.0 dative uplift); (zan-10) tightened the vinительный/родительный phrasing to the explicit
  41%/30% ratio. Genuinely open notes parked as in-text backlog markers rather than invented:
  zan-19 (Елизаренкова «Аорист в Ригведе» — needs the scan from MG), zan-22 (standalone stats
  dashboard — separate build), prilozhenie (cross-book calibration table — separate handoff).

## [0.11.0] - 2026-07-17
### Changed
- **APT-31 aorist figure refreshed (H1136, Opus 4.8 `claude-opus-4-8[1m]`).** The aorist-rarity
  citation in the APT-31 note + methodichka field moves from the old **0.31%** (DCS-2021
  tense-code count) to **~2.3% of finite verbal forms** — DCS's own `feat_formation` aorist tag
  (12,054 tokens, all 7 classes), which the earlier method undercounted by omitting the root and
  thematic aorists. Verdict unchanged (APT-31 stays FALSE — the aorist is marginal either way, so
  "the durative past is the imperfect/present, never the aorist" holds). Refreshed together with
  Kochergina HK-1, via the Whitney `whitney_aorist_tagger.py` (H1134).

## [0.10.0] - 2026-07-17
### Added
- **Methodichka viza applier (H1090 follow-on, Opus 4.8 `claude-opus-4-8[1m]`).** New self-tested
  [`apply_apte_methodichka_visa.py`](apply_apte_methodichka_visa.py) folds an MG viza
  `decisions.json` (from the 9-card sheet `sanskritgrammar-metodichka-apte-v1_17.07.26`) into
  [`METODICHKA_APTE_KOMMENTARII_2026.md`](METODICHKA_APTE_KOMMENTARII_2026.md): a `## Статус визы
  автора` summary table + per-section markers (approve → `_✅ Виза MG: одобрено._`; reject/defer →
  a `>` blockquote flag for a human rewrite; unvoted → `_⏳ Виза: не голосовано._`). Dry-run by
  default, `--apply` writes; **idempotent** (re-runnable after a re-vote — verified by identical
  MD5 across two applies) and it never deletes section prose, only its own prior markers. Emits
  pure Markdown (no HTML, per repo policy). Prepared ahead of the vote so applying is one command
  the moment the reviewer saves `decisions.json`.

## [0.9.0] - 2026-07-17
### Added
- **Methodichka «Учащемуся» takeaways in the reading-site overlay (H1095, Opus 4.8
  `claude-opus-4-8[1m]`).** Closed metadoc backlog #3: each of the 10 flagged claims (8 OVERSTATED ·
  1 FALSE · 1 UNTESTABLE) now carries a `methodichka` learner-takeaway field in
  [`claims.yml`](claims.yml), threaded through [`build_claims.py`](../scripts/build_claims.py) into
  `claims.json` + a new «Методичка — учащемуся» section of
  [`CLAIMS_VERIFIED.md`](CLAIMS_VERIFIED.md), and rendered as a green «методичка» block by
  [`ApteClaims.jsx`](../src/components/ApteClaims.jsx). `claims.yml` is the single source, so the
  print methodichka's per-lesson «Учащемуся» advice and the web overlay can no longer diverge. JSX
  compiles clean (Babel/preset-react); no verdicts or numbers changed.

## [0.8.0] - 2026-07-17
### Added
- **Print methodichka — раздел I commentary (H1090, Opus 4.8 `claude-opus-4-8[1m]`).** A
  print-first companion consuming the 39-claim register, mirroring the Kochergina methodichka:
  [`METODICHKA_APTE_KOMMENTARII_2026.md`](METODICHKA_APTE_KOMMENTARII_2026.md) (+ sibling
  `.meta.md`). Per-lesson notes in the **У Апте / Что показывают корпус и Уитни / Учащемуся**
  format over all 10 flagged claims (8 OVERSTATED · 1 FALSE · 1 UNTESTABLE), plus a strengths
  appendix. Pedagogical thesis: Apte is reliable on *meaning* (particle lexicon), overreaches on
  *distribution* (APT-5/23, APT-12), *government* (APT-18/19/21), and *aspect* (APT-31, the one
  FALSE) — mapping onto the drain's three-instrument split. Every figure cited by claim id, no
  number invented in prose. Exercises (раздел II) and cross-references (раздел III) deferred to
  v2; MG viza pending before print.

## [0.7.0] - 2026-07-17
### Added
- **Particle-sense Whitney pass (H1087, Opus 4.8 `claude-opus-4-8[1m]`).** Closed the reference-
  grade indeclinable/particle-sense claims of lessons 26–28 against Whitney's indeclinables
  chapter (§§1096-1135). Register **31 → 39 verified** (APT-32..39), **all TRUE** — punaḥ
  ('again'/adversative, §1112), prāyaḥ/prāyeṇa ('usually', §1111/§1112c), muhuḥ (§1111), yataḥ
  ('whence' = yasmāt, §1098), yāvat ('until' + accusative, §510/§1129), yathā yathā…tathā tathā
  (proportional, §1101), hā (grief-interjection, §1135a), varaṃ…na (preference idiom). Tally
  **29 TRUE · 8 OVERSTATED · 1 FALSE · 1 UNTESTABLE**.
### Notes
- **Finding:** Apte's particle/indeclinable **lexicon is accurate** — every gloss checks out
  against Whitney — a clean contrast with his overreaching aspect (APT-31) and government
  (APT-18/19/21) claims. Where Apte reports what a word *means* he is reliable; his misses are in
  what a form's *distribution* or *government* is. The ApteSyntax_1885 claim register is now
  complete for all corpus- and reference-adjudicable claims across the full six-handoff arc.

## [0.6.0] - 2026-07-17
### Added
- **Whitney adjudication of APT-H-219, the aorist-durative claim (H1084, Opus 4.8
  `claude-opus-4-8[1m]`).** Register **30 → 31 verified**; the register's **first FALSE** (APT-31,
  Урок 19). Apte §210 claims the aorist «implies the idea of continuousness» and «the imperfect
  cannot be used in this sense» — contradicted by **Whitney §§927-929** (the Classical aorist is
  «simply a preterit, equivalent to the imperfect and perfect»; the older aorist is *completive*,
  «viewed as completed with reference to the present» — the opposite of durative). Two-check
  rigor: (1) the digitized English §210 was verified, confirming the error is **Apte's own, not
  the Likhushina translation's**; (2) Apte contradicts himself (§207-208: the past tenses came to
  be used «promiscuously» — Whitney §927's very equivalence). Tally **21 TRUE · 8 OVERSTATED · 1
  FALSE · 1 UNTESTABLE**; the syntax-claim backlog is now fully adjudicated except reference-grade
  particle-sense rules.

## [0.5.0] - 2026-07-17
### Added
- **Lessons 26–30 harvested and drained (H1081, Opus 4.8 `claude-opus-4-8[1m]`).** Closes the
  coverage gap carried since the seed — all 30 lessons now harvested (backlog 79 → **115
  candidates**). Register **24 → 30 verified** (APT-25..30). New self-tested
  [`apte_pada_stats.py`](apte_pada_stats.py) → [`apte_pada_stats.json`](apte_pada_stats.json)
  recovers Parasmaipada/Ātmanepada from finite present endings — necessary because **DCS
  `feat_voice` tags only `Pass`, not the P/Ā distinction** — method-validated (as/bhū → P
  100%/99.7%, labh/īś → Ā 97.6%/100%).
### Changed
- Tally **17/7/0 → 21 TRUE · 8 OVERSTATED · 1 UNTESTABLE**:
  - **APT-25 hi → never sentence-initial: TRUE** (0.77%, completes the postpositive-particle family).
  - **APT-26 ram → Ātmanepada: TRUE** (95.5%); **APT-27 han → Parasmaipada: TRUE** (89.9%);
    **APT-29 single/both-voice typology: TRUE** (bhāṣ 97.9% Ā, nam 83.1% P, kṛ/duh both).
  - **APT-28 krīḍ → Parasmaipada: OVERSTATED** — actually near-even (57.6% P / 42.4% Ā), not the
    strong default «обычно» implies.
  - **APT-30 fine preverb+sense voice rules: UNTESTABLE** — the ~15 Pāṇinian sense-conditioned
    rules of lessons 29-30 have no corpus signal (DCS tags neither P/Ā nor the semantic trigger);
    documented as an instrument gap, not force-verdicted.

## [0.4.0] - 2026-07-16
### Added
- **Classical-corpus government instrument (H1062, Opus 4.8 `claude-opus-4-8[1m]`).** New
  self-tested [`apte_classical_government_stats.py`](apte_classical_government_stats.py) closes
  the case-government gap the treebank drain left open: a windowed-cooccurrence + baseline-lift
  proxy over the FULL 5.69M-token corpus (`feat_case` on 70.6%, escaping the Vedic-skewed 3.9%
  dependency slice), method-validated by positive controls (bhī/jugups reproduce their ablative)
  and a negative control (dṛś shows no spurious government, dative lift 0.23). Output in
  [`apte_classical_government_stats.json`](apte_classical_government_stats.json).
### Changed
- **Both former UNTESTABLE government rows resolved; one verdict corrected.** Register stays 24
  verified but the tally moves to **17 TRUE · 7 OVERSTATED · 0 UNTESTABLE**:
  - **APT-20 (ruc → dative) corrected OVERSTATED → TRUE** — dative enriched **3.06×** baseline
    (n=786); the treebank's OVERSTATED was a Vedic-skew artifact, as its own caveat predicted.
  - **APT-21 (anger verbs → dative) UNTESTABLE → OVERSTATED** — dative **not** enriched (0.91×,
    n=2,798): the Pāṇinian dative-of-anger is prescriptive, not corpus-frequent.
  - **APT-22 (love verbs → locative) UNTESTABLE → OVERSTATED** — locative leads but only 1.08×.
  - APT-16/17 (fear/disgust → ablative, 5.52×/3.96×) and APT-18/19 (throw/rule, competing case
    leads at n=12k/7k) corroborated at full-corpus scale.

## [0.3.0] - 2026-07-16
### Added
- **Treebank drain of the claim backlog (H1059, Opus 4.8 `claude-opus-4-8[1m]`).** New
  [`apte_treebank_stats.py`](apte_treebank_stats.py) (self-tested) measures the syntax backlog
  against DCS's own head/deprel/feat_case dependency slice (223,751 tokens / 29,433 fully-parsed
  sentences). Register **8 → 24 verified** (APT-9..APT-24): **16 TRUE · 6 OVERSTATED · 2
  UNTESTABLE**. Honest split: particle-position and agreement claims drain robustly (subject–verb
  number agreement 98.21% over n=10,672; ca/tu/ced/iva/eva/kila all confirmed never/rarely
  sentence-initial), with **uta the first corpus flag** (23.66% sentence-initial → OVERSTATED,
  vs <1% for the true postpositives; `hi` control 0.77%). Case-government claims split three ways
  — fear/disgust → ablative **confirmed** (APT-16/17), throw → locative and rule/remember →
  genitive **OVERSTATED** (a competing case leads in the corpus), anger/love → dative/locative
  **UNTESTABLE** (<10 case-tagged arguments in the Vedic-skewed slice). Motion-goal measurement
  quantifies the APT-5 flag: accusative goal 85.91% vs non-accusative 14.09% (n=873). Output in
  [`apte_treebank_stats.json`](apte_treebank_stats.json).

## [0.2.0] - 2026-07-16
### Added
- **Claim-verification register seed (H1055, Opus 4.8 `claude-opus-4-8[1m]`).** Ported the
  two-axis (fact × pedagogy) claim pipeline to Apte — the fifth book after Kochergina, Bühler
  and Zaliznyak ×2, and the **first syntax manual** in the register. New
  [`claims.yml`](claims.yml) (APT-1..APT-8: **7 TRUE · 1 OVERSTATED**) → generated
  [`CLAIMS_VERIFIED.md`](CLAIMS_VERIFIED.md) + `claims.json` via `npm run claims`; new
  [`claims_harvest.yml`](claims_harvest.yml) — a 79-candidate backlog (lessons 1–25 from a
  5-reader parallel harvest; lessons 26–30 logged as a coverage gap). Genre-checked first: Apte
  is syntax-weighted, so most claims are case-government/agreement rules testable against the
  DCS treebank layer, not surface frequency — flagged honestly, not forced. Three seed claims
  REUSE ground truth from sibling books (APT-6 = Bühler's 14:1 periphrastic/simple-future ratio;
  APT-3/APT-8 = the enclitic-position fact behind Kochergina HK-10), yielding two direct
  cross-book calibration contrasts (Apte's honest quantifiers where Kochergina/Bühler overreach).

## [0.1.0] - 2026-07-07
### Added
- Initial mint: reprint source scan/edition (`.doc`, `.docx`) plus faithful `.mdx`
  extraction (8 grid tables preserved) via the `/docx-to-md` skill.
