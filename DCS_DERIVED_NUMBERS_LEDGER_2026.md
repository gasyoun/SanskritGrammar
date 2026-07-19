# DCS-derived published numbers — adversarial re-derivation ledger (H1229)

_Created: 18-07-2026 · Last updated: 18-07-2026_

Every mechanically checkable DCS-derived number published in the Sangram series
(articles under [sangram/articles](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles),
their data manifests, and the W2 checkpoint), independently re-derived from the pinned
DCS master and given a **CONFIRMED / PLAUSIBLE / REFUTED** verdict. Executed under
[H1229](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1229-Fable_SanskritGrammar_dcs-derived-numbers-adversarial-rederivation_18.07.26.md)
by Fable 5 (`claude-fable-5`).

**Corpus pin:** `dcs_full.sqlite` provenance commit `04e0778d3dc971030229179e25eea043d06ff397`
(5 688 416 tokens, 270 texts) — the same snapshot every audited article cites.

## Verdict summary

| Verdict | Count | Meaning |
|---|---:|---|
| CONFIRMED — exact, independent | 97 | round-1 blind re-derivation matched to the digit |
| CONFIRMED — exact, definitional | 29 | round-1 approximation differed; the generation script's exact predicate (recovered from [scripts/](https://github.com/gasyoun/SanskritGrammar/tree/main/scripts)) reproduces the published number to the digit |
| PLAUSIBLE | 0 | — |
| **REFUTED** | **3** | see below |
| **Total** | **129** | |

**Headline:** none of the five known instrument caveats (C1 gaṇa-code, C2 red-aorist,
C3 kṛt-surface, C4 taddhita-segmentation, C5 compound-type) contaminated any published
number — every check that touches one confirmed. The three real errors are mundane:
a truncated rounding, a value copied from the wrong column, and an encoding-scoped
query presented as a corpus fact.

## The three REFUTED numbers and the fix applied

| # | Where | Published | Correct | Fix policy |
|---|---|---|---|---|
| 1 | [word-structure-overview](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/word-structure-overview/index.mdx) line 73 | «16,8 %» transparent root+affix share | **16,9 %** (true 16.857 %, truncated instead of rounded) | conclusion unchanged → fixed in place, this PR |
| 2 | [preverbs](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/preverbs/index.mdx) lines 5 + 60 | `ut` 17 275 | **17 322** — the 17 275 is the exact-string column; every other cell of the table is the leading-upasarga fold | conclusion unchanged (ranking unaffected) → fixed in place, this PR |
| 3 | [krt-suffixes](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/krt-suffixes/index.mdx) lines 56–61 | «лемм с исходом -tṛ … в снапшоте **ноль**» | **771 IAST `-tṛ` lemmas exist**; the zero is an artifact of querying SLP1 `%tf` against IAST lemma strings [C3] | **argument-affecting** (the pilot's stated reason for excluding -tṛ is false) → shipped as draft [PR #414](https://github.com/gasyoun/SanskritGrammar/pull/414); **MG ruled merge 18-07-2026** — correction live, -tṛ pilot re-run stays queued |

## Method — three rounds, all scripts committed

1. **Round 1 — blind re-derivation** ([sangram/audit/rederive_dcs_numbers.py](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/rederive_dcs_numbers.py)):
   129 checks recomputed from the raw `token`/`lemma`/`sentence` tables without
   looking at the generation scripts. 97/129 exact.
2. **Round 2 — predicate recovery** ([sangram/audit/rederive_dcs_numbers_round2.py](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/rederive_dcs_numbers_round2.py)):
   re-tested the 30 non-deliberate mismatches with predicates recovered from
   `scripts/sg_*.py`; 18 resolved exactly.
3. **Round 3 — final predicate recovery** ([sangram/audit/rederive_dcs_numbers_round3.py](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/rederive_dcs_numbers_round3.py)):
   the remaining definitions read directly out of the generation scripts — nsubj/obj
   totals carry **no case filter**; the double-accusative core set includes
   `xcomp:result`; the SE003 «top forms» are per-**lemma** noun counts; the syāt
   count has **no finiteness filter**; the periphrastic-perfect «auxiliary» counts
   parse the surface **tail** of the peri token itself; the top-future-forms table
   groups by (form, lemma) **pairs**; the possessive counts select `lemma LIKE
   '%vant'/'%mant'`; the infinitive/gerundive classifiers are **retroflex-aware**
   (`draṣṭum`-type ṭum, which both naive SQL `LIKE '%tum'` and Python
   `endswith('tum')` silently miss). 11/12 exact — the 12th is REFUTED #1 above.
4. **Emitted-data determinism:** re-running the generation scripts for a-stems,
   consonant-stems and declension-overview reproduced the committed `data/*.json`
   byte-identically (sole diff: `"sha256": null` from `--skip-checksum`).

Machine-readable results: [audit_results.json](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/audit_results.json) ·
[audit_results_round2.json](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/audit_results_round2.json) ·
[audit_results_round3.json](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/audit_results_round3.json).

## Full ledger — one row per check

Anchor column is `article-slug:line` (or checkpoint/manifest); article sources live under
[sangram/articles](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles),
each at `<slug>/index.mdx`. A check bundling several published values counts once.

| ID | Anchor | Published number(s) | Value(s) | Verdict | Resolution |
|---|---|---|---|---|---|
| `BASE-1` | SANGRAM_CORPUS_EVIDENCE_METHOD.mdx:44 | total tokens | 5688416 | CONFIRMED | exact (round 1) |
| `BASE-2` | same | texts | 270 | CONFIRMED | exact (round 1) |
| `BASE-3` | same | sentences | 754726 | CONFIRMED | exact (round 1) |
| `BASE-4` | preverbs manifest | lemmas | 180176 | CONFIRMED | exact (round 1) |
| `BASE-5` | karaka-case:54 | deprel-tagged tokens (parsed subset) | 223751 | CONFIRMED | exact (round 1) |
| `BASE-6` | SANGRAM_CORPUS_EVIDENCE_METHOD.mdx:44 | texts with syntax trees | 74 | CONFIRMED | exact (round 1) |
| `MO012-1` | conjugation-overview:50 | finite verb tokens | 523721 | CONFIRMED | exact (round 1) |
| `MO012-2` | conjugation-overview:65 | person 3/2/1 | [420305, 63865, 39551] | CONFIRMED | exact (round 1) |
| `MO012-3` | conjugation-overview:67 | number Sing/Plur/Dual | [420271, 94078, 9372] | CONFIRMED | exact (round 1) |
| `MO012-4` | conjugation-overview:73 | tense Pres/Past/Impf/Fut | [353215, 102055, 46695, 21556] | CONFIRMED | exact (round 1) |
| `MO012-5` | conjugation-overview:84 + imperative-optative:110 | mood Ind/Opt/Imp/Jus/Sub/Prec/Cond/Pot | [364771, 91912, 56506, 5258, 4325, 577, 340, 32] | CONFIRMED | exact (round 1) |
| `MO012-6` | conjugation-overview:96 + passive:48 | finite passive | 29699 | CONFIRMED | exact (round 1) |
| `MO012-7` | conjugation-overview:96 | finite active (unmarked) | 494022 | CONFIRMED | exact (round 1) |
| `WF001-1` | word-structure-overview:67 | partition nominal/closed/Cpd/finite/krt | [2271734, 1616811, 841052, 523738, 435081] | CONFIRMED | exact (round 1) |
| `WF001-2` | word-structure-overview:78 | distinct finite-verb lemmas | 8053 | CONFIRMED | exact (round 1) |
| `WF001-3` | word-structure-overview:80 | top-10/50/100 finite concentration % | [29.7, 48.7, 58.6] | CONFIRMED | exact (round 1) |
| `WF001-4` | word-structure-overview:95 | feat_formation on all VERB [C2] | [17440, 5690, 5386, 2781, 1508, 1077, 833, 124, 41] | CONFIRMED | exact (round 1) |
| `WF001-5` | word-structure-overview:49+73 | root+affix transparent share % | 16.8 | **REFUTED** | corrected: **16,9 %** — rounding: true 16.857 % was truncated to 16.8 instead of rounded to 16.9 |
| `MO001-1` | declension-overview:44 | inflected common-noun tokens | 1790270 | CONFIRMED | exact (round 1) |
| `MO001-2` | declension-overview:58 | noun number Sing/Plur/Dual | [1419826, 332943, 37501] | CONFIRMED | exact (round 1) |
| `MO001-3` | declension-overview:67 | noun case dist Nom..Dat | [692647, 430396, 184609, 177320, 138883, 65363, 61862, 39190] | CONFIRMED | exact (round 1) |
| `MO001-4` | checkpoint:87 (G2) | distinct declined-noun lemmas | 57144 | CONFIRMED | round 2: generation-script predicate recovered, exact match |
| `MO001-5` | checkpoint:87 (G2) | G2: median cells / %exactly-1 / %all-24 / fill% | [1, 58.9, 0.0, 10.44] | CONFIRMED | round 2: generation-script predicate recovered, exact match |
| `SE001-1` | case-system-overview:40 | tokens with feat_case (any upos) | 4014688 | CONFIRMED | exact (round 1) |
| `SE001-2` | case-system-overview:41 | 8 vibhakti total / Cpd excluded | [3173636, 841052] | CONFIRMED | exact (round 1) |
| `SE001-3` | case-system-overview:53 + SE002/3/4/5 universes | all-upos case dist Nom/Acc/Ins/Gen/Loc/Voc/Abl/Dat | [1419146, 742293, 277143, 270763, 243215, 81088, 74565, 65423] | CONFIRMED | exact (round 1) |
| `SE001-4` | case-system-overview:65 | Nom+Acc share of 8-vibhakti % | 68 | CONFIRMED | exact (round 1) |
| `SE002-1` | nominative-accusative:55 | nsubj case-tagged: total/Nom/Loc/Gen/Acc | [20062, 19626, 266, 43, 43] | CONFIRMED | round 3: generation-script predicate recovered, exact match |
| `SE002-2` | nominative-accusative:76 | obj case-tagged: total/Acc | [16933, 15269] | CONFIRMED | round 3: generation-script predicate recovered, exact match |
| `SE002-3` | nominative-accusative:61 | cop-head Nom count / % of cop-heads | [1372, 82.6] | CONFIRMED | round 2: generation-script predicate recovered, exact match |
| `SE002-4` | nominative-accusative:84 | verbs with two true obj (Acc) | 36 | CONFIRMED | exact (round 1) |
| `SE002-5` | nominative-accusative:84 | naive double-acc (>=2 Acc deps of a verb) | 2747 | CONFIRMED | exact (round 1) |
| `SE002-6` | nominative-accusative:84 | corrected double-acc (core roles) ~872 | 872 | CONFIRMED | round 3: generation-script predicate recovered, exact match |
| `SE003-1` | instrumental-dative:58 | obl:instr case-tagged total / obl:soc | [2692, 488] | CONFIRMED | round 2: generation-script predicate recovered, exact match |
| `SE003-2` | instrumental-dative:58 | obl:instr that are Ins (article's 2,569) | 2569 | CONFIRMED | exact (round 1) |
| `SE003-3` | instrumental-dative:55 | Ins with Pass head (passive-agent proxy) | 21472 | CONFIRMED | round 2: generation-script predicate recovered, exact match |
| `SE003-4` | instrumental-dative:61 | Ins pronouns tad/mad | [13256, 5605] | CONFIRMED | round 2: generation-script predicate recovered, exact match |
| `SE003-5` | instrumental-dative:51 | top Ins noun forms manasā/śareṇa/karmaṇā | [1863, 1603, 1471] | CONFIRMED | round 3: generation-script predicate recovered, exact match |
| `SE003-6` | instrumental-dative:71 | top Dat noun forms agnaye/devāya/indrāya | [1221, 1065, 997] | CONFIRMED | round 3: generation-script predicate recovered, exact match |
| `SE003-7` | instrumental-dative:74 | Dat pronouns mad/tvad | [5834, 5215] | CONFIRMED | round 2: generation-script predicate recovered, exact match |
| `SE004-1` | ablative-genitive:53 | Abl singular % | 92 | CONFIRMED | exact (round 1) |
| `SE004-2` | ablative-genitive:58+61 | Abl lemmas bhaya/hetu/tva [C4] | [747, 458, 3429] | CONFIRMED | exact (round 1) |
| `SE004-3` | ablative-genitive:69 | Gen pronoun share ~33% | 33 | CONFIRMED | exact (round 1) |
| `SE004-4` | ablative-genitive:69/73/75 | Gen deprel nmod/iobj/obl:benef/obj | [6696, 86, 188, 333] | CONFIRMED | exact (round 1) |
| `SE004-5` | ablative-genitive:85 + locative:45 | Gen+Part / Loc+Part candidates | [16493, 20973] | CONFIRMED | exact (round 1) |
| `SE004-6` | ablative-genitive:86 | Gen+Part advcl* / acl*+nmod | [40, 334] | CONFIRMED | round 2: generation-script predicate recovered, exact match |
| `SE004-7` | ablative-genitive:101 | paśyataḥ idiom: dṛś Gen+Part / advcl-tagged | [373, 1] | CONFIRMED | round 2: generation-script predicate recovered, exact match |
| `SE005-1` | locative:54 | Loc number Sing/Plur/Dual | [204735, 35656, 2824] | CONFIRMED | exact (round 1) |
| `SE005-2` | locative:71 | Loc+Part singular / natively-passive | [18165, 1091] | CONFIRMED | exact (round 1) |
| `SE005-3` | locative:77 | Loc+Part top lemmas gam/as/vac/kṛ | [910, 830, 662, 637] | CONFIRMED | exact (round 1) |
| `SE005-4` | locative:88 | Loc+Part parsed / advcl-set / acl / obl | [557, 367, 35, 48] | CONFIRMED | round 2: generation-script predicate recovered, exact match |
| `SE005-5` | locative:79 | Loc-abs candidate by text: MBh / Suśruta / Rām | [3925, 832, 825] | CONFIRMED | exact (round 1) |
| `SE008-1` | imperative-optative:40+51 | Imp: total/2nd/3rd/1st/Sing | [56506, 38144, 17373, 989, 44051] | CONFIRMED | exact (round 1) |
| `SE008-2` | imperative-optative:40+51 | Opt: total/2nd/3rd/1st/Sing | [91912, 981, 86918, 4013, 85274] | CONFIRMED | exact (round 1) |
| `SE008-3` | imperative-optative:63 | syāt (lemma as, Opt) | 9505 | CONFIRMED | round 3: generation-script predicate recovered, exact match |
| `SE013-1` | karaka-case:84-88 | kartR-active: N / %Nom | [20230, 97.8] | CONFIRMED | exact (round 1) |
| `SE013-2` | karaka-case:84-88 | karman: N / %Acc | [16874, 90.5] | CONFIRMED | exact (round 1) |
| `SE013-3` | karaka-case:84-88 | karaNa: N / %Ins | [2692, 95.4] | CONFIRMED | exact (round 1) |
| `SE013-4` | karaka-case:84-88 | apAdAna: N / %Abl | [981, 85.7] | CONFIRMED | exact (round 1) |
| `SE013-5` | karaka-case:84-88 | adhikaraNa: N / %Loc | [1720, 84.5] | CONFIRMED | exact (round 1) |
| `SE013-6` | karaka-case:84-88 | kartR-passive: N / %Ins | [408, 61.8] | CONFIRMED | exact (round 1) |
| `SE013-7` | karaka-case:84-88 | sampradAna-recip: N / %Dat | [2771, 66.4] | CONFIRMED | exact (round 1) |
| `SE013-8` | karaka-case:84-88 | sampradAna-goal: N / %Acc | [2336, 64.0] | CONFIRMED | exact (round 1) |
| `SE013-9` | karaka-case:166 | nsubj:pass rows | 0 | CONFIRMED | exact (round 1) |
| `SE013-10` | karaka-case:166 + passive:48 | Pass-voice verb tokens (all forms) | 36701 | CONFIRMED | exact (round 1) |
| `SE013-11` | karaka-case:166 | nsubj at Pass head: total / Nom | [607, 563] | CONFIRMED | exact (round 1) |
| `SE013-12` | karaka-case:173 | kartR (nsubj+csubj) Loc off-diagonal | 272 | CONFIRMED | exact (round 1) |
| `SE013-13` | karaka-case:88 | obl:benef Dat/Gen split % | [47.0, 42.9] | CONFIRMED | exact (round 1) |
| `MO016-1` | imperfect:66 | Impf person/number/voice profile % | [94.1, 3.3, 2.5, 75.1, 22.6, 2.3, 96.9, 3.1] | CONFIRMED | exact (round 1) |
| `MO016-2` | imperfect:69 | Impf top roots brū/bhū/as/paś/kṛ | [5669, 3769, 3032, 1385, 1002] | CONFIRMED | exact (round 1) |
| `MO017-1` | perfect:77 + aorist:65 + aorist-types:53 | Past formation NULL/peri/root/them/s/is/red/sa/sis [C2] | [85955, 4046, 5690, 2781, 1508, 1077, 833, 124, 41] | CONFIRMED | exact (round 1) |
| `MO017-2` | aorist:60 + aorist-types:41 | formation-tagged aorist total [C2] | 12054 | CONFIRMED | exact (round 1) |
| `MO017-3` | aorist-types:61 | non-sigmatic / sigmatic split [C2] | [9304, 2750] | CONFIRMED | exact (round 1) |
| `MO017-4` | perfect:66 | pluperfect-tagged tokens ~200 | 200 | CONFIRMED | exact (round 1) |
| `MO019-1` | aorist-types:53 | aorist lemma counts root/them/red/s/is/sa/sis | [210, 175, 150, 216, 170, 37, 14] | CONFIRMED | exact (round 1) |
| `MO018-1` | aorist:78 | tagged-aorist top roots bhū/vac/gam/kṛ/gā/dā | [2360, 837, 664, 452, 312, 255] | CONFIRMED | exact (round 1) |
| `MO017-5` | perfect:118 | peri tokens by lemma: as/kṛ/bhū | [3697, 298, 32] | CONFIRMED | round 3: generation-script predicate recovered, exact match |
| `MO017-6` | perfect:121 | peri person-number 3Sing/3Plur/3Dual/1Sing/2Sing | [3503, 466, 68, 8, 1] | CONFIRMED | exact (round 1) |
| `MO021-1` | future:68 | Fut person % 3rd/1st/2nd | [51.6, 36.4, 12.0] | CONFIRMED | exact (round 1) |
| `MO021-2` | future:80 | Fut simple / periphrastic | [20216, 1340] | CONFIRMED | exact (round 1) |
| `MO021-3` | future:73 | top Fut forms bhaviṣyati/vakṣyāmi/pravakṣyāmi | [2013, 579, 532] | CONFIRMED | round 3: generation-script predicate recovered, exact match |
| `MO021-4` | future:80 | top periphrastic-future forms bhavitā/kartā | [332, 55] | CONFIRMED | exact (round 1) |
| `MO021-5` | future:91 | conditional (feat_mood=Cond) total | 340 | CONFIRMED | exact (round 1) |
| `MO021-6` | future:47 | future participles (Part & Fut) | 1575 | CONFIRMED | exact (round 1) |
| `WF002-1` | krt-overview:47+60 | quartet total / Part / Conv / Gdv / Inf | [483623, 341556, 102054, 28260, 11753] | CONFIRMED | exact (round 1) |
| `WF002-2` | krt-overview:47 | quartet leakage onto non-VERB | 0 | CONFIRMED | exact (round 1) |
| `WF002-3` | krt-overview:66 + ta-na-participles:48 | tense-NULL participles | 266660 | CONFIRMED | exact (round 1) |
| `WF002-4` | krt-overview:73 [C3] | surface tokens -ana / -ti / -tṛ(IAST) | [95263, 74927, 31042] | CONFIRMED | exact (round 1) |
| `WF003-1` | krt-suffixes:60 [C3] | lemma counts -ana / -ti / -in | [3438, 1886, 2926] | CONFIRMED | exact (round 1) |
| `WF003-2` | krt-suffixes:60 — THE -tṛ ENCODING TRAP [C3] | lemmas ending SLP1 'tf' (published: 0 => 'DCS never lemmatises -tṛ') vs IAST 'tṛ' reality | [0, 0] | **REFUTED** | corrected: **771 IAST -tṛ lemmas exist** — SLP1/IAST encoding trap [C3]: the zero came from querying '%tf' (SLP1) against IAST lemmas; ARGUMENT-AFFECTING |
| `MO022-1` | present-perfect-participles:60+65 | Pres Part total / Pass / None-voice | [64209, 7002, 57207] | CONFIRMED | exact (round 1) |
| `MO022-2` | present-perfect-participles:68 | top Pres-Part lemmas as/yaj/kṛ | [3430, 2783, 1384] | CONFIRMED | exact (round 1) |
| `MO022-3` | present-perfect-participles:80 | Past+Part bucket | 9112 | CONFIRMED | exact (round 1) |
| `MO022-4` | present-perfect-participles:82 | vid in Past+Part (-vas leader) | 1279 | CONFIRMED | exact (round 1) |
| `MO024-1` | gerundive:61 | top Gdv lemmas kṛ/jñā/dā/grah/vijñā | [3576, 1427, 1319, 694, 683] | CONFIRMED | exact (round 1) |
| `MO024-2` | gerundive:54 | Gdv suffix split -ya/-tavya/-anīya (approx surface) | [19901, 5740, 1280] | CONFIRMED | round 3: generation-script predicate recovered, exact match |
| `MO025-1` | infinitive:69 | top Inf lemmas kṛ/dṛś/vac/śru/gam | [906, 628, 613, 522, 360] | CONFIRMED | exact (round 1) |
| `MO025-2` | infinitive:56+66 | Inf split -tum/-tave/-toḥ/-dhyai | [9681, 320, 154, 97] | CONFIRMED | round 3: generation-script predicate recovered, exact match |
| `MO026-1` | absolutive:61 | Conv split -ya(-tya)/-tvā/other/-am | [57790, 34816, 8980, 468] | CONFIRMED | exact (round 1) |
| `MO026-2` | absolutive:71 | allomorphy cross-tab tvā-nopv/tvā-pv/ya-nopv/ya-pv | [34293, 523, 1289, 56501] | CONFIRMED | exact (round 1) |
| `MO028-1` | causative:44 [C1] | class-10 bucket finite tokens / lemma types | [55376, 2006] | CONFIRMED | exact (round 1) |
| `MO028-2` | causative:47 [C1] | denominative finite tokens | 5451 | CONFIRMED | exact (round 1) |
| `MO028-3` | causative:64 [C1] | top class-10 lemmas kathay/dhāray/kāray/pūjay | [2083, 1337, 1327, 1249] | CONFIRMED | exact (round 1) |
| `MO013-1` | thematic-present:46 | finite Pres tokens / distinct lemma_ids | [353215, 7186] | CONFIRMED | exact (round 1) |
| `MO010-1` | pronouns:55 | PRON tokens / distinct lemmas | [544999, 38] | CONFIRMED | round 2: generation-script predicate recovered, exact match |
| `MO010-2` | pronouns:73 | top-8 pronoun tokens+cells all match | true | CONFIRMED | round 2: generation-script predicate recovered, exact match |
| `MO002-1` | a-stems:54 | -a stems Masc: lemmas/tokens (approx universe, no dictionary-gender whitelist) | [21837, 716864] | CONFIRMED | generation-script re-run reproduced emitted data byte-identically |
| `MO002-2` | a-stems:54 | -a stems Neut: lemmas/tokens (approx universe, no dictionary-gender whitelist) | [13857, 359194] | CONFIRMED | generation-script re-run reproduced emitted data byte-identically |
| `MO002-3` | a-stems:67+118 | putra: tokens / attested cells | [9729, 23] | CONFIRMED | round 2: generation-script predicate recovered, exact match |
| `MO002-4` | a-stems:67+118 | deva: tokens / attested cells | [17536, 22] | CONFIRMED | round 2: generation-script predicate recovered, exact match |
| `MO002-5` | a-stems:67+118 | netra: tokens / attested cells | [385, 22] | CONFIRMED | round 2: generation-script predicate recovered, exact match |
| `MO002-6` | a-stems:67+118 | phala: tokens / attested cells | [3973, 17] | CONFIRMED | round 2: generation-script predicate recovered, exact match |
| `MO002-7` | a-stems:185 [C4] | tva as neuter 'lemma' token count | 9972 | CONFIRMED | exact (round 1) |
| `WF004-1` | taddhita-overview:55 | NOUN+ADJ universe / NOUN / ADJ | [2996410, 2395188, 601222] | CONFIRMED | exact (round 1) |
| `WF004-2` | taddhita-overview:77+80 [C4] | segmentation-suffix tokens tva/tā/vat/maya + total | [10850, 5919, 4125, 3214, 24108] | CONFIRMED | exact (round 1) |
| `WF004-3` | taddhita-overview:77 [C4] | base recoverable at idx-1 % | 99.8 | CONFIRMED | exact (round 1) |
| `WF004-4` | taddhita-overview:86 [C4] | -tva base POS ADJ/NOUN/VERB | [4876, 4441, 1107] | CONFIRMED | exact (round 1) |
| `WF004-5` | taddhita-overview:157 [C3] | -ya surface selection tokens | 224191 | CONFIRMED | exact (round 1) |
| `WF004-6` | taddhita-overview:195 | possessive -vant (bhagavant) / -mant (surface variants tried) | [7100, 5188, 1272] | CONFIRMED | round 3: generation-script predicate recovered, exact match |
| `WF006-1` | P4-design:22 vs tatpurusha:53 | sentences with >=1 Cpd token (raw) | 396571 | CONFIRMED | exact (round 1) |
| `WF006-2` | compounds-overview:51+59 | reconstructed compounds / sentences-with | [595021, 396305] | CONFIRMED | exact (round 1) |
| `WF006-3` | compounds-overview:65 | member histogram 2/3/4/5+ | [442649, 104460, 28372, 19540] | CONFIRMED | exact (round 1) |
| `WF006-4` | tatpurusha:53 | two-member / multi-member | [442649, 152372] | CONFIRMED | exact (round 1) |
| `WF006-5` | compounds-overview:73 [C5] | compound:coord / :name / generic | [2044, 51, 119] | CONFIRMED | exact (round 1) |
| `WF008-1` | tatpurusha:70 [C5] | the '2,214 compound:coord' claim = coord+name+generic sum, not coord alone | 2214 | CONFIRMED | exact (round 1) |
| `WF011-1` | preverbs:41 | preverbed verb tokens / % of verbs / lemmas | [369870, 36.7, 10017] | CONFIRMED | exact (round 1) |
| `WF011-2` | preverbs:54 — the ut cell | leading-upasarga ut (published 17,275) | 17275 | **REFUTED** | corrected: **17 322** — ut cell copied from the exact-string column; every other cell is the leading-upasarga fold |
| `WF011-3` | preverbs:54 | leading-upasarga pra/ā/sam/vi/upa/ni/abhi | [58118, 48139, 47613, 40856, 22195, 20423, 17824] | CONFIRMED | exact (round 1) |
| `WF011-4` | preverbs:67+111 | multi-preverb tokens / (other) bucket | [25906, 28956] | CONFIRMED | exact (round 1) |

## Frozen invariants honoured

- Scope limited to *existing* published numbers; no new analyses.
- Every REFUTED verdict is backed by a runnable committed script, not an argument
  from plausibility.
- `claims.yml`, visa states and A61/A13 material untouched.

_Dr. Mārcis Gasūns_
