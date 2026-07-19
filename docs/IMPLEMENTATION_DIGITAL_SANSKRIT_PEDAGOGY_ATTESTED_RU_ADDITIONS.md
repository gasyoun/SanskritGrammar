_Created: 19-07-2026 · Last updated: 19-07-2026_

# Implementation — attested-cell drills, corpus-linked methodichka, samāsa bracket trainer (Wave-2 additions)

File-level steps for the three Wave-2 additions staged 19-07-2026 via
[`/ask-batch`](https://github.com/gasyoun/claude-config/blob/main/commands/ask-batch.md)
(Fable 5 `claude-fable-5`; interview rulings in
[`ASK_BATCH_STAGING_PEDAGOGY_2026-07.md`](https://github.com/gasyoun/Uprava/blob/main/ASK_BATCH_STAGING_PEDAGOGY_2026-07.md)).
Parent plan:
[`docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md);
wave table:
[`docs/ROADMAP_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md)
§ Wave 2 additions; acceptance:
[`docs/VERIFICATION_DIGITAL_SANSKRIT_PEDAGOGY.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_DIGITAL_SANSKRIT_PEDAGOGY.md)
§ Wave-2 additions.

Shared rights gate: published Russian glosses only from the
[SanskritRussian](https://github.com/gasyoun/SanskritRussian) public site-tier subset
(restricted bulk layers and `corpus_lexicon` are local-only inputs);
`/publish-safety-check` before any public page. Attribute DCS (Hellwig) wherever
corpus-derived numbers surface.

---

## W2-add-a — Attested-cell declension drill generator ([H1296](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1296-Opus_SanskritGrammar_sangram-attested-cell-declension-drills_19.07.26.md), Opus)

**The delta vs everything shipped:** kosha's W1a morphology drills (H946) drill the
*paradigm engine's* forms; nothing anywhere exploits the G2 finding that only **10.44 %**
of the noun lemma × 24-cell space is ever corpus-attested
([`sangram/data/declension_cell_coverage/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/data/declension_cell_coverage),
57,144 lemmas, `cells_bits24`; consumers today: SG-MO articles only). This build teaches
"what you'll actually meet": drills present **only attested cells**, ordered by lemma
frequency, grouped by stem class.

1. **Join script** `sangram/data/attested_drills/build_attested_declension_drills.py`
   (stdlib-only): [`lemma_cell_coverage.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/data/declension_cell_coverage/lemma_cell_coverage.csv)
   × kosha [`lemma_frequency.tsv`](https://github.com/gasyoun/kosha/blob/main/data/frequency/lemma_frequency.tsv)
   (`core_rank`) × the Zaliznyak grammar index stem classes
   (`zaliznyak-grammar-index`, [`kosha/data/manifest/datasets.json`](https://github.com/gasyoun/kosha/blob/main/data/manifest/datasets.json)).
   Emit `attested_drill_items.tsv`: lemma · stem class · attested cell (case×number) ·
   corpus count · frequency band · expected form.
2. **Expected forms** come from vidyut-prakriyā generation, *checked against* attested
   surface forms where the corpus provides them; disagreement rows carry a flag column,
   never a silent pick (kosha R1/R2 risk discipline).
3. **Drill surface**: a sangram interactive widget (the P10 family pattern —
   SandhiCollider siblings) at `sangram/atlas/` or the widgets home the repo uses;
   modes: type-the-form, pick-the-cell; RU interface.
4. **Coverage instrumentation**: per stem class report "N attested cells of 24 ·
   top-band coverage %" — the learn-N→meet-X% metric this field runs on.
5. **Tests + registration**: joiner unit test on a 20-lemma fixture; dataset row in
   kosha's manifest if the TSV is consumed cross-repo; changelog + release.

## W2-add-b — Corpus-linked methodichka ([H1297](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1297-Fable_SanskritGrammar_metodichka-corpus-linked-kochergina-apte_19.07.26.md), Fable)

**The delta vs H1258/H1275 (explicitly ruled distinct at mint, `--allow-dup`):** those
apply *author review notes* to the existing companions. This build adds a **new data
layer**: for each vocabulary item / paradigm in the Kochergina companion
([`KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_COMPANION_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_COMPANION_2026.md))
and the Apte companion
([`ApteSyntax_1885/METODICHKA_APTE_KOMMENTARII_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/METODICHKA_APTE_KOMMENTARII_2026.md)),
its DCS **frequency band** and **one corpus-attested example sentence with a Russian
rendering** — turning static textbook companions into corpus-linked ones.

1. **Vocabulary extraction**: parse each companion's lemma inventory (per-lesson) into a
   working TSV; log unparseable rows loudly.
2. **Frequency banding**: join kosha `lemma_frequency.tsv` `core_rank`/`coverage_pct`;
   band labels (топ-100 / топ-1000 / редкое) chosen once, documented in the file header.
3. **Attested example + RU gloss**: for each lemma pick one short corpus sentence
   attested in DCS whose Russian rendering exists in the org's aligned layers —
   **rights-gated**: published output uses only public-tier renderings; where only a
   restricted rendering exists, the example ships Sanskrit-only with a "перевод в
   закрытом слое" marker. The Fable judgment is the *selection* (short, self-contained,
   lesson-appropriate) and the RU register of any freshly authored glosses.
4. **Landing**: a new "Корпусный слой" section per companion (kept in the companion's
   own file or a sibling `*_CORPUS_LAYER.md`, whichever the companion's metadoc rules) +
   backlog ticks in both metadocs.
5. **Tests**: banding join regression on 20 known lemmas; every example sentence carries
   its DCS locus.

## W2-add-c — Samāsa right-to-left bracket-method trainer ([H1298](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1298-Opus_SanskritGrammar_sangram-samasa-bracket-method-trainer_19.07.26.md), Opus)

**The delta vs kosha's shipped W1c samāsa trainer (H948):** H948 drills identify-type +
split. This trainer teaches the **resolution method** — the head-first (right-to-left)
vigraha ladder the [`/klammeruebersetzung`](https://github.com/gasyoun/claude-config/blob/main/commands/klammeruebersetzung.md)
skill encodes — over **corpus-attested** compounds with Russian constituent glosses.

1. **Data**: sample graded compounds from the DCS compound dictionary
   (`dcs-compound-dictionary`, 168,880 attested splits, VisualDCS
   `derived-data/Kompozity/` — `names.csv`/`cmps.csv`), stratified by depth (2-member →
   3+ member) and frequency; constituent RU glosses from the SanskritRussian public
   lemma layer.
2. **Ladder generator**: for each compound emit the step-by-step right-to-left
   resolution (head → modifier → vigraha sentence), machine-built from the split +
   glosses, hand-checked on a 30-compound gold set committed with provenance.
3. **Widget**: sangram interactive (P10 family): learner reorders/unfolds the ladder;
   reveal shows the vigraha + smooth RU rendering; cross-link kosha's H948 trainer for
   type drills rather than duplicating them.
4. **Instrumentation**: per-depth accuracy events (the RQ2 drill-generation evidence
   line); report top-N compound coverage of real text.
5. **Tests**: ladder generator regression on the 30-compound gold set.

---

## Build discipline (all three)

Worktree + PR per deliverable (SanskritGrammar is main-tree-guarded); stdlib-only
scripts with UTF-8 reconfigure; `npm run build` green where a widget lands in the
Docusaurus tree; changelog + release per ship; hub sweep (`/artifact-propagate`) on
completion.

_Dr. Mārcis Gasūns_
