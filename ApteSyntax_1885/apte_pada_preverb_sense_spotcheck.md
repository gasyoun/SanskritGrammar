_Created: 25-08-2026 · Last updated: 05-09-2026_

# H3113 (zan-29) -- preverb-conditioned pada extraction + sense spot-check

_Created: 18-08-2026._ Resolves the escalated, unvoted `zan-29` card
(review sheet `sanskritgrammar-metodichka-apte-v1_17.07.26`; source of truth
[H1090 follow-up 2b](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1090-Opus_SanskritGrammar_apte-methodichka-commentary_17.07.26.md)).
Instrument: [`apte_pada_preverb_stats.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/apte_pada_preverb_stats.py),
extending the H1081 root-default instrument `apte_pada_stats.py` (APT-26..30)
to the fifteen preverb-compound / fine-sense voice rules of Apte lessons 29-30.

## The curator's note, taken at face value

> DCS не размечает ни P/Ā (только пассив), ни семантическое условие -- не
> размечает ни P/Ā можно извлечь данные из непосредственно наблюдаемых форм,
> ни семантическое условие -- можно извлечь из разметки санскритско-русского
> корпуса

Read literally this names two separately-recoverable layers. Both were tried.

## Layer 1 -- pada from observed endings (DCS-2021, `dcs_full.sqlite`)

DCS's `token.lemma` already encodes the preverb (`saṃgam`, `vinī`, `upasthā`,
`bodhay` are each their own lemma), so the same finite-present ending
classifier that drained APT-26..29 (root-default voice) runs unchanged on the
preverb-compound lemma. One correction was needed and applied: several of
these compounds have a substantial share of `-ya-` **passive** present forms
(`bhujyate`, `upasthīyate`, `vikrīyate`, `bodhyate`) that end exactly like an
Ātmanepada form but are separately tagged `feat_voice='Pass'` in DCS. The
original `apte_pada_stats.py` does not filter these; this instrument does
(`AND (feat_voice IS NULL OR feat_voice != 'Pass')`) -- a real correction, not
a scope divergence. For `bhuj` alone this removed 97 misattributed forms; for
`nī`/`unnī`/`upanī`/`vinī` combined it removed most of the counted "Ā" mass
(182 -> 43), which **reverses the observed default** from lean-P to
strongly-P.

### Extraction table (finite present-indicative, passives excluded)

| id | preverb+root | Apte's claim | P | A | n | observed | verdict |
|---|---|---|---:|---:|---:|---|---|
| APT-H-601 | kram (bare) | Ā when duration/intensity implied | 77 | 80 | 157 | both (49.0/51.0) | OVERSTATED |
| APT-H-603 | sam+gam | Ā, sense 'join with' | 5 | 22 | 27 | -- | UNTESTABLE-thin (n<40) |
| APT-H-604 | ud+car | Ā when transitive | 10 | 1 | 11 | -- | UNTESTABLE-thin (n<40) |
| APT-H-605 | vi/parā+ji | Ā, sense 'conquer/rout' | 16 | 66 | 82 | A (19.5/80.5) | **TRUE** |
| APT-H-606 | vi/ud+tap | Ā when intransitive/body-part obj. | 1 | 0 | 1 | -- | UNTESTABLE-thin (n<40) |
| APT-H-607 | nī bare/+ud/upa/vi | Ā | 541 | 43 | 584 | P (92.6/7.4) | **OVERSTATED** |
| APT-H-608 | vi+nī | P, sense 'teach/train/tame' | 15 | 3 | 18 | -- | UNTESTABLE-thin (n<40, but 83.3% P descriptively -- see spot-check below) |
| APT-H-610 | upa+sthā | Ā, sense 'worship/wait upon' | 72 | 558 | 630 | A (11.4/88.6) | **TRUE** (pada only -- see spot-check for the sense itself) |
| APT-H-611 | anu+hṛ | Ā='practice' / P='resemble' | 6 | 0 | 6 | -- | UNTESTABLE-thin (n<40) |
| APT-H-613 | sam+śru | P if transitive / Ā if intransitive | 2 | 2 | 4 | -- | UNTESTABLE-thin (n<40) |
| APT-H-614 | bhuj | Ā except sense 'protect/rule' | 52 | 421 | 473 | A (11.0/89.0) | **TRUE** |
| APT-H-615 | pra/upa+yuj | Ā except re sacrificial vessels | 66 | 95 | 161 | both (41.0/59.0) | OVERSTATED |
| APT-H-616 | jñā desiderative | always Ā | 2 | 6 | 8 | -- | UNTESTABLE-thin (n<40) |
| APT-H-617 | causatives (budh/yudh/naś/jan/adhi+i/dru/sru) | P, no sense condition | 584 | 52 | 636 | P (91.8/8.2) | **TRUE** -- cleanest confirmed rule; no sense condition to begin with |
| APT-H-619 | pari/vi/ava+krī | Ā, sense 'buy' | 19 | 23 | 42 | both (45.2/54.8) | OVERSTATED (heterogeneous: parikrī 86.7% P, vikrī 77.8% A, avakrī no data -- see JSON `per_lemma`) |

Full per-lemma breakdown: [`apte_pada_preverb_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/apte_pada_preverb_stats.json) / [`.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/apte_pada_preverb_stats.csv).

**Transitivity check** (APT-H-604, 606, 613 condition on transitivity, which
DCS's sparse dependency layer (`deprel='obj'/'iobj'`) can approximate): all
three came back too thin to report (n=11, 1, 4 classified occurrences,
respectively -- below the 15-occurrence floor set for this check). This is
itself the finding: DCS's UD-style parse covers too small a fraction of
tokens (~29k `root` relations against 5.46M total tokens, ~0.5%) for a
per-lemma transitivity split at any usable n.

### Hand spot-check (15 forms, ending classification only)

| form | lemma | ending | classified | correct? |
|---|---|---|---|---|
| kramanti | kram | -anti | P | yes |
| kramante | kram | -ante | A | yes |
| vijayati | viji | -ati | P | yes |
| vijayate | viji | -ate | A | yes |
| parājayati | parāji | -ati | P | yes |
| parājayante | parāji | -ante | A | yes |
| nayati | nī | -ati | P | yes |
| nayate | nī | -ate | A | yes |
| vinayati | vinī | -ati | P | yes |
| upatiṣṭhate | upasthā | -ate | A | yes |
| bhunakti | bhuj | -ti | P | yes |
| bhuñjate | bhuj | -ate | A | yes |
| bodhayati | bodhay | -ati | P | yes |
| adhyāpayati | adhyāpay | -ati | P | yes |
| parikrīṇāti | parikrī | -āti | P | yes |

15/15 correct (ending regex reused verbatim from the already-reviewed
`apte_pada_stats.py`; the only change in this pass is the passive exclusion
described above, independently verified against `feat_voice` in the same
query).

## Layer 2 -- semantic condition (Sanskrit-Russian parallel corpus)

`SanskritLexicography/RussianTranslation/src/corpus_lexicon.jsonl` (1.09M
Sa-Ru word-aligned gloss rows, the corpus behind SamudraManthanam /
samskrtam.ru) DOES carry enough per-occurrence sense information to check a
sample by hand -- this is a genuine, if manual and small-sample, positive
result for the escalation's second half. It is not a scalable per-token
signal (no shared token ids with DCS; matching is by surface form only, and
coverage per specific inflected form is thin), so it is used here as a
spot-check, not a new automated instrument.

**nī (bare) vs vi+nī** -- Apte's contrast (607 vs 608) is that bare nī
defaults Ā ('lead') while vi+nī in the 'teach/train' sense is P:

- `nayati`/`nayanti` (bare nī, n=8 occurrences sampled): glosses are "ведет"
  / "ведут" (leads/lead) x6, plus two idiomatic outliers ("ищет", "лишила",
  "нарекли", "провести" -- extended senses of the same 'lead/conduct' root
  meaning). **No 'teach' sense in the sample.**
- `vinayanti` (vi+nī, n=1 occurrence found): gloss "приучают" (they
  train/accustom) -- exactly the 'teach/train' sense, and morphologically P
  (`-anti`). **Confirms APT-H-608's specific pairing** (train-sense -> P) in
  the one attested instance, consistent with the 83.3% P lean in the pada
  table above.

**upa+sthā 'worship' sense (APT-H-610)** -- of 8 sampled `upatiṣṭhate(-nte)`
occurrences, only 2 clearly carry the claimed 'worship/venerate' sense
("чтит" = venerates, "почитания" = reverence); the other 6 are the more
generic 'approach / stand near / be present / arrive' sense ("приближается",
"находятся рядом", "присутствуют", "пришли", "стекаются", "восходит") with no
devotional content. **The pada-level Ā-dominance (88.6%) is real and
confirmed, but the specific 'worship' gloss Apte gives is a minority use in
this sample, not the driver of the voice choice** -- the claim as stated
(worship -> Ā) overstates how narrowly conditioned the Ā default actually is;
Ā is simply upasthā's default voice across senses, worship included.

## What this settles for zan-29

1. **P/Ā itself is extractable for preverb-compound lemmas**, exactly as the
   curator's note said, via the same ending-recovery method as APT-26..29 --
   confirmed testable for 8/15 rules at n>=40 (4 TRUE, 4 OVERSTATED/mixed),
   with a real passive-tagging correction along the way.
2. **7/15 rules stay UNTESTABLE-thin even at the pada layer** -- not enough
   attested finite-present forms of that specific preverb-compound in
   DCS-2021, independent of the sense question.
3. **The semantic condition itself (why a given token takes that pada) is
   recoverable only by hand, from the Sanskrit-Russian corpus, one gloss at a
   time** -- feasible at spot-check scale (done here for 2 of the 15 rules,
   17 total glosses read), not as an automated per-lemma instrument. Where
   checked, the corpus glosses show a real semantic mix under a single
   pada-dominant lemma (upasthā), meaning even a confirmed pada default does
   not by itself validate Apte's narrower sense-gloss.

This is a genuine data pass, not a re-vote: it neither fully vindicates nor
fully refutes the lesson-29-30 appendix, and that mixed, itemized result is
the honest close for zan-29.

_Dr. Mārcis Gasūns_
