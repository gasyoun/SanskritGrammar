# Verification — Digital Sanskrit Pedagogy

_Created: 14-07-2026 · Last updated: 21-07-2026_

Acceptance criteria per wave-1 deliverable, the exact check that proves each, and the risks/spikes
register. Plan cover [here](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md).

## Acceptance criteria

| Deliverable | Done when | Proof (the exact check) |
|---|---|---|
| **W1a** difficulty/ordering | `build_difficulty_ordering.py` runs green; result doc has the τ table + ≥1 divergence with a pedagogical reading; A63 skeleton at readiness-2 with a data-inventory table | run the script → non-empty `difficulty_ordering.tsv` + stats JSON; result numbers reproduced by re-running |
| **W1b** A62 draft | outline at readiness-2; survey + hypotheses (RQ1–4) + evaluation-design sections present; venue line; dashboard regen | `python Uprava/tools/build_dashboard_data.py` regenerates; A62 row shows readiness 2 |
| **W1c** Zaliznyak on-ramp | on-ramp `.mdx` builds; graded sequence renders; "one tap deeper" links resolve to Талмуд chapters | `npm run build` → SUCCESS, 0 new broken links; spot-check the deep links |
| **W1d** last-mile spec | spec complete; kosha↔Systema contract defined; one-rung demo path specified; **no Systema production code changed** | `git diff` touches only the spec doc; contract section names inputs/outputs of each hop |
| **W2-add-a** attested drills ([H1296](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1296-Opus_SanskritGrammar_sangram-attested-cell-declension-drills_19.07.26.md)) | joiner fixture test green; drill items carry ONLY attested cells (spot-check 20 vs `lemma_cell_coverage.csv`); generated-vs-attested disagreements flagged, never silently picked; per-class coverage report present | run the join script → `attested_drill_items.tsv` + coverage report; fixture test |
| **W2-add-b** corpus-linked methodichka ([H1297](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1297-Fable_SanskritGrammar_metodichka-corpus-linked-kochergina-apte_19.07.26.md)) | every companion lemma carries band + DCS locus; restricted-rendering rows ship Sanskrit-only with the marker; both metadocs ticked | banding regression on 20 lemmas; grep zero restricted-layer text in the published section |
| **W2-add-c** bracket trainer ([H1298](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1298-Opus_SanskritGrammar_sangram-samasa-bracket-method-trainer_19.07.26.md)) | 30-compound gold ladder set committed + regression green; widget builds; H948 cross-linked not duplicated | `npm run build` SUCCESS; gold regression |
| **Registration** | MEGABOOK §2.10 present + §2.9 strengthened; A62 in ARTICLES with bumped marker; GTD straddle tier row; ROADMAP_INDEX entry; handoffs registered | `crosslink_weave_check.py MEGABOOK.md` passes; A62 marker → A63; registry counts add up |

### Verified

- **W2-add-a ✅ 19-07-2026** (Opus 4.8 `claude-opus-4-8`, [H1296](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1296-Opus_SanskritGrammar_sangram-attested-cell-declension-drills_19.07.26.md)).
  [`tests/test_attested_drills.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/tests/test_attested_drills.py)
  green (6 tests): joiner fixture over 20 lemmas, the 20-item spot-check of the real
  corpus against `lemma_cell_coverage.csv` bitstrings, a bit-index↔`cells_order` guard,
  and a check that every flagged disagreement ships **both** sides. Corpus:
  **5 838 lemmas · 45 045 drill items**, mean 7.72 attested cells of 24;
  `match` 33 886 / `variant` 6 977 / `mismatch` 4 152 / `no_generation` 30 —
  `mismatch` cells are excluded from drilling (no authoritative answer to grade against)
  and shown as evidence instead. Per-class report:
  [`COVERAGE_REPORT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/data/attested_drills/COVERAGE_REPORT.md).
  Site page [`sangram/articles/attested-drills`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/attested-drills/index.mdx)
  builds. Incidental finding: the `mismatch` flag doubles as a DCS annotation-error
  detector (`artha` Voc.Sing attests *arthaiḥ*, an instrumental plural, n=6).

- **W2-add-b ✅ 21-07-2026** (Fable 5 `claude-fable-5`, [H1297](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1297-Fable_SanskritGrammar_metodichka-corpus-linked-kochergina-apte_19.07.26.md)).
  [`tests/test_corpus_layer.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/tests/test_corpus_layer.py)
  green (5 tests): the 20-lemma banding regression (fixture pinned + live cross-check
  against kosha `lemma_frequency.tsv`), band-boundary pins (100/101, 1000/1001), a
  DCS-locus check on every published example, the rights gate (every rendering
  `authored`/`public-glossary`; a `restricted` row must ship Sanskrit-only with the
  marker — zero such rows in this edition, and no restricted layer was opened at all),
  and a manuscript↔TSV drift guard (band + rank + locus per lemma). Corpus layer:
  **31 lemmas / 9 занятий** for Kochergina
  ([`METODICHKA_KOCHERGINA_CORPUS_LAYER_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_CORPUS_LAYER_2026.md)),
  **34 lemmas / 7 разделов** for Apte
  ([`METODICHKA_APTE_CORPUS_LAYER_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/METODICHKA_APTE_CORPUS_LAYER_2026.md));
  bands from kosha `lemma_frequency.tsv` `rank_all`, examples from the DCS-2026 import
  (`dcs_full.sqlite`, source commit `04e0778`), lesson-matched forms via DCS features
  (`tense=Fut` for Занятие XVIII futures, `formation=root` for Занятие XXXVII root
  aorists, `formation=peri` for the periphrastic perfect). Both metadocs ticked.
  Incidental finding: the DCS lemma string `hā` conflates the verb «покидать» with the
  interjection «увы» (the generic query returned only verb forms; the interjection is
  tagged `upos=ADV`), and kosha frequency rows inherit the conflation — banded rows for
  `hā`/`vara` carry an upper-bound footnote in the Apte manuscript.

- **W2-add-c ✅ 19-07-2026** (Opus 4.8 `claude-opus-4-8`, [H1298](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1298-Opus_SanskritGrammar_sangram-samasa-bracket-method-trainer_19.07.26.md)).
  [`tests/test_samasa_ladder.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/tests/test_samasa_ladder.py)
  green (20 tests) and `npm run build` **SUCCESS**; the widget was exercised in a served
  build (head graded, ladder unfolds right→left, question slots keep ≥2 candidates).
  Corpus: **5 443 ladders** from 168 880 upstream rows (gates: 156 762 below freq 5,
  5 799 deeper than 4 members, 209 rejected on member order, 635 missing a RU gloss).
  Gold set: **30 hand-checked** analyses in
  [`gold_ladder_30.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/data/samasa_ladder/gold_ladder_30.tsv),
  each with question chain, vigraha and smooth RU; bahuvrīhi rows carry the extra
  `…yasya saḥ` rung, and the genuinely ambiguous `dharmarāja-` keeps **both** readings.
  H948 is cross-linked, not duplicated: type and split drills stay kosha's, and no rung
  here asserts a compound type. Report:
  [`COVERAGE_REPORT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/data/samasa_ladder/COVERAGE_REPORT.md).
  Incidental finding: **209 upstream `names.csv` rows carry a split that is reversed,
  rotated, over-repeated or lifted from a different word** — invisible to a type-drill
  (which never depends on member order) but fatal to a head-first ladder; the ordered
  consonant-skeleton gate is what catches them. Gold-set ratification is agent-side
  (Opus 4.8) — a human philological sign-off has not been taken.

## Risks & spikes register

- **RQ1 may return a null result** — the `core_rank` "learn-these-first" order might *not* beat textbook order. **Spike before committing:** correlate `core_rank` with an independent difficulty proxy (rare-form density, first-attestation era). If the correlation is weak, RQ1 reports the null honestly — a negative result is still a result, not a failure to hide.
- **Accent-dependent ambiguity** — class I/VI and IV/passive are not recoverable from unaccented DCS. Morphology drills and difficulty signals must **surface** the ambiguity, never fabricate certainty.
- **Rights** — papers touching in-copyright sources (Kochergina) stay `.md` with **aggregate numbers only**, never built as site pages. (A60 already follows this.)
- **Audio scope-creep** — §3.7 audio is explicitly Wave 4. Do not let W1c/W1d pull audio into wave-1.
- **Systema fence** — W1d is **spec-only**; touching Systema production code in wave-1 violates the straddle-tier boundary.
- **Concurrent-session / watcher contention** (SanskritGrammar) — an EmEditor watcher and other sessions have reverted uncommitted edits here before. Build in a **worktree**, commit with **explicit pathspec**, land+commit atomically.
- **MDX validity** — only `npm run build` proves a page compiles (grep pre-checks pass on files that still fail at compile). Never mark a site page done on a grep alone.
- **Publish gate** — nothing goes public (Pages/visibility) and no rights-gated corpus is published without a human GO/NO-GO via [`/publish-safety-check`](https://github.com/gasyoun/claude-config/blob/main/commands/publish-safety-check.md), independent of the build fence.

## The measurement bar (why the field is falsifiable)

Every wave-1 result carries its date, model tier+version, and the committed asset that backs it. No
deliverable is ✅ without its proof-check above passing. RQ4 (evaluation methodology, A32) is the
field's backbone: until a learning-gain metric exists, "this teaches better" stays a hypothesis, and
the roadmap treats it as one.

---

_Dr. Mārcis Gasūns_
