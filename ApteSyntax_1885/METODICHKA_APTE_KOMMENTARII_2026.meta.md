# Metadoc — METODICHKA_APTE_KOMMENTARII_2026.md

_Created: 17-07-2026 · Last updated: 21-07-2026_

Companion record for the Apte print methodichka commentary manuscript
([`METODICHKA_APTE_KOMMENTARII_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/METODICHKA_APTE_KOMMENTARII_2026.md)).

## Purpose
A print-first commentary companion to Apte's *Student's Guide to Sanskrit Composition* (1885,
Likhushina Russian tr.), turning the 39-claim verification register into per-lesson pedagogical
notes — where Apte overreaches, what the corpus/Whitney show, and what the learner should
actually expect. Consumes the register (`claims.yml`/`claims.json`) rather than re-deriving it,
exactly as the Kochergina methodichka consumes its register.

## Audience
MG (author of record) + any future session extending the methodichka (exercises/cross-refs v2).
Russian self-study and taught learners already using Apte.

## Provenance
- Authored 17-07-2026 by Opus 4.8 (`claude-opus-4-8[1m]`) via [H1090](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1090-Opus_SanskritGrammar_apte-methodichka-commentary_17.07.26.md).
- Built directly on the completed Apte register (H1055→H1087) and its reading-site overlay (H1089).
- Every number cited by claim id; no figure invented in prose (the hybrid source-of-truth model
  from the Kochergina methodichka Decision A).

## Structure & thesis
Раздел I only (commentary/accuracy), v1. Organised by lesson, note format
**У Апте / Что показывают корпус и Уитни / Учащемуся** (the Kochergina раздел-I template). The
manuscript's pedagogical thesis: **Apte is reliable on MEANING (particle lexicon), overreaches on
DISTRIBUTION, GOVERNMENT and ASPECT** — which maps onto the three-instrument split of the drain.
Covers all 10 flagged claims (8 OVERSTATED · 1 FALSE · 1 UNTESTABLE) + a strengths appendix.

## Ranked improvement backlog
1. **Exercise appendix (раздел II)** — corpus-sourced readings + authored graded drills per
   covered lesson, matched to the flagged rules (e.g. a case-government drill for the motion-verb
   goal cases). Deferred to v2, mirrors the Kochergina exercise section.
2. **Cross-references (раздел III)** — «см. также» pointers to Whitney §§, the other Russian
   grammars (Kochergina/Bühler/Zaliznyak) where the same rule is treated, and the Talmud. Deferred.
3. ~~**Reading-site overlay of the methodichka notes** — the commentary could feed the existing
   `<ApteClaims/>` overlay as a per-claim "методичка" annotation, so print and web never diverge.~~
   ✅ **DONE (H1095, 17-07-2026).** Each of the 10 flagged claims now carries a `methodichka`
   «Учащемуся» takeaway in [`claims.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/claims.yml),
   threaded through [`build_claims.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_claims.py)
   into `claims.json` and rendered as a green «методичка» block by
   [`ApteClaims.jsx`](https://github.com/gasyoun/SanskritGrammar/blob/main/src/components/ApteClaims.jsx).
   `claims.yml` is the single source, so print (this manuscript's «Учащемуся» lines) and web can no
   longer diverge.
4. ~~**MG viza** — the commentary verdicts and learner-advice lines are human-visaed before print
   (a `/review-sheet` pass like the Kochergina methodichka v1), currently undone.~~ ✅ **DONE**
   (17-07-2026) — 8/9 approve, `apply_apte_methodichka_visa.py --apply`; substantive notes folded
   in (Likhushina direct quotes, Sherzl cross-check, tightened зан-10 ratio); zan-29 (Занятия
   29–30) still unvoted.
5. **Open from this viza round** — ~~Елизаренкова scan (зан-19, needs MG's file)~~ ✅ **DONE**
   (20-07-2026, H1373): cross-check run against the scan MG actually supplied — «Ведийский язык» /
   «Санскрит» in «Языки мира: Индоарийские языки древнего и среднего периодов» (М.: Academia,
   2004) — **not** the «Аорист в Ригведе» (1960) monograph named in the viza, which was not among
   the materials. The substitution is favourable: Apte § 210 concerns the *classical* aorist, the
   1960 monograph the Vedic one. APT-31 confirmed on both halves of Apte's claim. Scan gitignored
   as in-copyright. Residual — the 1960 monograph itself, if it ever arrives: a Vedic slice, not a
   verdict change. **Still open from this round:** a standalone uta-statistics dashboard (зан-22);
   a cross-book calibration table («что у кого лучше», приложение).
6. ~~**Corpus layer (раздел II)** — per-lemma DCS frequency band + one attested example
   with a Russian rendering for every lemma the раздел-I commentary turns on.~~
   ✅ **DONE (H1297, 21-07-2026):**
   [`METODICHKA_APTE_CORPUS_LAYER_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/METODICHKA_APTE_CORPUS_LAYER_2026.md)
   (34 lemmas over 7 разделов) backed by
   [`corpus_layer/corpus_layer.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/corpus_layer/corpus_layer.tsv)
   and pinned by [`tests/test_corpus_layer.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/tests/test_corpus_layer.py).
   Government-sensitive examples chosen to *show* the раздел-I verdicts (acc at
   druh/asūy/smṛ, gen at īś/prabhū/īrṣy, loc at kṣip/snih, dat at ruc, kim… uta).
   Residual: the freshly authored Russian renderings await the MG viza.

## Limitations
- v1 is commentary only — no exercises, no cross-references yet.
- The government-claim numbers rest on the windowed-cooccurrence proxy (a collocation
  approximation, not dependency government); this is disclosed per-claim in the register.
- Rights: the 1885 English is public domain, but the manuscript quotes the Likhushina translation
  minimally; a DOI/print release needs `/publish-safety-check` first.

## Related docs
- [`METODICHKA_KOCHERGINA_COMPANION_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_COMPANION_2026.md) — the template this follows.
- [`claims.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/claims.yml) / [`CLAIMS_VERIFIED.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/CLAIMS_VERIFIED.md) — the register consumed.
- [`src/components/ApteClaims.jsx`](https://github.com/gasyoun/SanskritGrammar/blob/main/src/components/ApteClaims.jsx) / [`CLAIMS_OVERLAY.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/CLAIMS_OVERLAY.mdx) — the reading-site overlay (H1089).

## Revision history
| Date | Model | Change |
|---|---|---|
| 17-07-2026 | Opus 4.8 (`claude-opus-4-8[1m]`) | Created v1 раздел I (commentary) + this metadoc (H1090). All 10 flagged claims covered + strengths appendix. |
| 17-07-2026 | Opus 4.8 (`claude-opus-4-8[1m]`) | Fed the «Учащемуся» takeaways into the `<ApteClaims/>` reading-site overlay via a `methodichka` field in `claims.yml` (single source) — backlog #3 closed (H1095). |
| 17-07-2026 | Sonnet 5 (`claude-sonnet-5`) | MG viza applied (8/9 approve) — backlog #4 closed. Likhushina direct quotes (Занятие 3/19), Sherzl government-index cross-check (Занятие 7/9), tightened Занятие 10 ratio; 3 open research asks parked as backlog #5. |
| 19-07-2026 | Fable 5 (`claude-fable-5`) | H1275: все 8 одобренных правок визы доведены до письменной диспозиции (таблица «Ревизии правок визы» в рукописи). Сноски-оговорки 1–3 (зан-3/19/22) — настоящие `[^n]`-сноски вместо прозы; прямая перецитата формулировок правил по Лихушиной расширена на §§ 63/94/98/113/258; контрольная сверка Шерцля по `government_lexicon.jsonl` выявила и сняла три неточности цитирования H1205 (krudh «acc.», ruc «только», пропущенный dat. 160 у muc + глосса превербов). Елизаренкова (зан-19), dashboard (зан-22) и межкнижный список (приложение) отложены с именованными блокерами; zan-29 эскалирован на повторную визу (@DECIDE). |
| 21-07-2026 | Fable 5 (`claude-fable-5`) | **Corpus layer (раздел II) authored — H1297.** 34 lemmas per занятие with DCS frequency bands + one attested DCS-2026 example each; examples selected to demonstrate the раздел-I government verdicts in living text; RU renderings freshly authored (no restricted layer opened); homonym-band caveat footnoted (hā, vara). Working TSVs under `corpus_layer/`, checks in `tests/test_corpus_layer.py`. Backlog item 6 added and closed. |
| 20-07-2026 | Opus 4.8 (`claude-opus-4-8[1m]`) | H1373: сверка зан-19 с Елизаренковой выполнена — последний открытый `LOCAL`-пункт визы закрыт. Источник: очерки «Ведийский язык» (с. 20) и «Санскрит» (с. 28, 44) в «Языки мира: Индоарийские языки древнего и среднего периодов» (М.: Academia, 2004); названной в визе монографии «Аорист в Ригведе» (1960) среди переданных материалов не было, и замена ближе к делу (§ 210 — классический аорист). Вердикт APT-31 подтверждён по обеим половинам утверждения: аорист = совершенный вид, «только что произошедшее на глазах у субъекта»; несовершенный вид/длительность закреплены за имперфектом; в классике оппозиция нивелирована, выбор стилистический — независимое подтверждение Уитни §§ 927–929 и Апте § 207. Скан внесён в `.gitignore` (авторское право, порядок H552), цитируется по страницам печатного тома. |

_Dr. Mārcis Gasūns_
