_Created: 19-07-2026 · Last updated: 19-07-2026_

# Where Bühler got his exercise sentences — provenance adjudication (H1212)

**For:** anyone citing the quotation/adaptation/invention split of Bühler's *Leitfaden*
exercises, or extending the matcher. This is the judgment record behind
[`scripts/data/buhler_provenance.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/buhler_provenance.json)
— what the mechanical pass got wrong, what was ruled by hand, and what the numbers may
and may not be used to claim.

Answers Q1 of
[`TEXTBOOK_SENTENCE_REUSE_BUHLER_KNAUER_KOCHERGINA.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TEXTBOOK_SENTENCE_REUSE_BUHLER_KNAUER_KOCHERGINA.md)
(comparison axis #6), deferred there by
[H1211](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1211-Opus_SanskritGrammar_buhler-knauer-kochergina-fidelity-axis-pedagogy_17.07.26.md).

## The result

Of Bühler's **603** Devanāgarī exercise entries, 18 (all of Lesson XLVIII) are alphabet
chart rows, not prose. Of the remaining **585 exercise sentences**:

| Verdict | n | share | meaning |
|---|---:|---:|---|
| `quotation` | 51 | 8.7 % | occurs verbatim in an attested text |
| `adapted` | 17 | 2.9 % | a real verse with a word changed for the grammar point |
| `invented` | 515 | 88.0 % | no attested source; constructed to drill a paradigm |
| `unknown` | 2 | 0.3 % | verbatim hit too short to be evidence (`evaṃ vadanti`) |

_Figures are the H1344 three-corpus run (DCS + Indische Sprüche + GRETIL). The H1212
two-corpus pass gave 50 / 16 / 518 / 1 — see "The corpus-expansion test" below for why the
difference is itself the most useful result here._

**So ~12 % of Bühler's exercises are literature and ~88 % are his own drill prose.** MG's
Q1 intuition — that sentences like `त्वं जीव शरदः शतम्` and `लोभात्क्रोधः प्रभवति…` come
from real literature — is borne out in kind but split in verdict: `लोभात्क्रोधः…` is a
verbatim *Hitopadeśa* quotation, while `त्वं जीव शरदः शतम्` is **adapted, not quoted** (see
the hand-adjudicated cases below). Either way both are the minority case.

## Three findings the raw split does not show

**1. Attestation is a late-book phenomenon.** Nothing before Lesson XII is attested at
all. Lessons I–XXIV run 7.2 % attested (25/347); lessons XXV–XLII run 18.1 % (43/238) —
a 2.5× jump. Bühler writes his own sentences while the student is learning paradigms and
switches to real literature once the student can read it. Provenance is therefore a
*curricular* variable, not a stylistic one, and any per-lesson claim must control for it.

**2. 82 % of attested sentences sit in consecutive runs.** 56 of the 68 attested sentences
(82.4 %) are adjacent to another attested sentence, forming 20 multi-sentence runs. `buhler-XIII-304` +
`-305` are the two lines of *Hitopadeśa* I's `lobhāt krodhaḥ prabhavati…`; `-341`/`-342`
and `-464`/`-465` likewise. Bühler splits a verse across consecutive exercise numbers, one
pāda-pair each.

Not every run is a pair: 12 runs are 2 long, two are 3, five are 4 (`-447`–`-450` is two
verses back to back), and `-824`–`-829` runs to six. **The unit of borrowing is the verse,
not the sentence** — so "68 attested sentences" is really **~41 borrowed verses**
(Σ⌈run/2⌉ over all 32 runs, 12 of which are singletons), and counting sentences
double-counts the borrowing.

**3. The source profile is nīti, not Veda or kāvya.** Of the 68:

| Source | n |
|---|---:|
| Böhtlingk, *Indische Sprüche* (subhāṣita/nīti) | 28 |
| Hitopadeśa | 8 |
| Manusmṛti | 5 |
| Mahābhārata | 4 |
| Baudhāyanadharmasūtra | 4 |
| Śatakatraya (Bhartṛhari) | 4 |
| Vasiṣṭhadharmasūtra | 3 |
| Kūrmapurāṇa, Atharvaveda (Paipp.) | 2 each |
| Kāvyādarśa, Harṣacarita, Rāmāyaṇa, AVŚ, Gautamadharmasūtra, Garuḍapurāṇa | 1 each |
| Bhaṭṭi, *Rāvaṇavadha* (GRETIL), Manusmṛti (GRETIL) | 1 each |

Gnomic literature (Sprüche + Hitopadeśa + Śatakatraya = 40, 59 %) plus dharmaśāstra
(Manu/Baudhāyana/Vasiṣṭha/Gautama = 14, 21 %) account for four fifths. Kāvya is nearly
absent — and stayed that way after 56 kāvya texts were added (below) — and the Veda
contributes 3. Bühler drills on *maxims* — short, syntactically
complete, morally unobjectionable in a colonial classroom, and quotable in one line.

Note the trap: the sentences that *name* Kālidāsa (`कालिदासस्य काव्यं…`) and Pāṇini
(`शास्त्रस्य कर्त्रे पाणिनये नमः`) are **invented** — they are *about* the authors, not
*from* them. Author-name presence is not attestation.

## What the mechanical pass got wrong (and why the thresholds are what they are)

Three false-positive classes were found by reading the output, not by testing, and each
one changed the headline number. They are recorded here because a future re-run that
loosens any of these will silently reinflate the "adapted" bucket.

1. **Token containment without adjacency (56 → 28 rows).** The first pass scored
   candidates by IDF-weighted overlap. `adya jīvāmaḥ` ("today we live", Lesson I) scored
   0.64 because its two tokens both occur — scattered, unrelated — in a long
   Aṣṭāṅgahṛdaya sentence. Overlap cannot distinguish a quotation from a coincidence of
   vocabulary. Replaced by *longest attested contiguous token run*; containment is still
   reported but no longer votes.
2. **`nfold` nasal-folding artefacts (28 → 16 rows).** `sanskrit_util.nfold` maps every
   nasal to `n`, which is what makes sandhi-tolerant recall possible — and which also
   folded Bühler's `janānāṃ dhanaṃ` onto the unrelated `yājamānaṃ dhānaṃjayyaḥ`. Every
   run is now re-verified on `norm` (m/n distinct) before it counts.
3. **Two-word collocations.** `duḥkhaṃ bhavati` is attested everywhere and means nothing.
   A run of exactly two tokens now needs ≥ 70 % of the sentence to count.

Lesson XLVIII was likewise excluded *by lesson*, not by string length: a length floor was
keeping `ṣa ṣaṭtriṃśat` (12 chars) while dropping `a akṣa` (5 chars), i.e. splitting one
homogeneous alphabet chart on an irrelevant axis.

## Hand-adjudicated cases

The `adapted` rows were read individually (16 at H1212, 17 after the corpus extension).
All stand; the interesting ones are real
editorial interventions by Bühler, which is itself the evidence that he adapted knowingly:

| Sentence | Attested form | Bühler's change |
|---|---|---|
| `buhler-XXXVI-829` | `aśeṣadoṣaduṣṭo 'pi` (Hitop. 2) | → `anekadoṣaduṣṭo 'pi` |
| `buhler-XXXVI-826` | `śubhaṃ vā dvijasattama` (MBh 3, 200) | → `śubhaṃ vā yadi sattama` |
| `buhler-XXXVII-845` | `nirloṭhitena` (Rājataraṅgiṇī 5) | → `nirluṇṭhitena` |
| `buhler-XXV-539` | `vidyā lambhyate sarvaṃ` (Sprüche) | → `vidyayā labhyate sarvaṃ` |
| `buhler-XX-457` | `tvaṃ jīva śaradaḥ suvarcā` (AVP 1, 13) | → `tvaṃ jīva śaradaḥ śatam` |

The last is the sentence MG named. It is **adapted, not quoted**: the benediction formula
`jīva śaradaḥ śatam` is genuinely Vedic and recurs across the gṛhya literature, but
Bühler's exact line matches no attested text — he has assembled the standard formula from
its stock parts. That is the honest verdict, and a stricter one than "Vedic blessing".

## The corpus-expansion test (H1344) — the invention finding is robust

The first pass rested on two corpora and carried an honest worry: `invented` might just mean
*absent from DCS*. In particular "kāvya is nearly absent" was suspect, because **DCS carries
no Raghuvaṃśa and no Śiśupālavadha** — the finding could have been an artefact of corpus
composition rather than a fact about Bühler.

So a third corpus was added: GRETIL plaintext, **85,401 verse lines** across kāvya (56
texts — Kālidāsa, Māgha, Bhāravi, Bhaṭṭi, Bāṇa, Daṇḍin, Aśvaghoṣa, Jayadeva…), subhāṣita
(Vidyākara's *Subhāṣitaratnakośa*), smṛti, purāṇa, epic and stotra. That is an **11 %
expansion of the haystack, aimed squarely at the register the first pass said was missing.**

**It moved three sentences.**

| Sentence | was | now | evidence |
|---|---|---|---|
| `buhler-XIII-312` `ratho dhyaṣṭhīyata rāmeṇa` | invented | adapted | Bhaṭṭi, *Rāvaṇavadha* |
| `buhler-XXXV-806` `ācārādvicyuto vipro…` | invented | quotation | Manusmṛti (GRETIL) |
| `buhler-XXXVIII-889` `yadā sa devo` | invented | unknown | Manusmṛti, 10 chars |

88.5 % invented → 88.0 % invented. **The invention finding survives a targeted attempt to
break it**, which is a much stronger claim than the original "upper bound" caveat. And the
kāvya finding survives in the sharpest possible way: 56 kāvya texts yielded **exactly one**
new attestation — Bhaṭṭi's *Rāvaṇavadha*, which is the one kāvya composed to illustrate
Pāṇinian grammar. The single poem Bühler drew on is the poem that is itself a grammar.

`buhler-XXXV-806` is methodologically the interesting one. DCS stores it as
`ācārāt vicyutaḥ vipraḥ na veda phalam aśnute` — **analyzed word forms, not the sandhied
surface** — while GRETIL has the true `ācārād vicyuto vipro na vedaphalam aśnute`. The DCS
column is named `text_sandhied` but is not reliably sandhied, which silently downgrades
verbatim quotations to partial matches. Any pipeline matching printed text against DCS
inherits this; it is logged as a cross-repo gotcha in
[FINDINGS](https://github.com/gasyoun/SanskritLexicography/blob/master/FINDINGS.md).

## The IAST subset (H1344) — apparatus, not exercises

H1212 scoped itself to the 603 Devanāgarī entries and left "extend to the 765 IAST-script
sentences" as mechanical follow-up. **It is not mechanical, and it should not be run as
stated.** Classifying those 765 entries:

| Content type | n |
|---|---:|
| root + conjugation-class annotations (`mā III. Ā`) | 337 |
| fragments < 3 tokens (`guṇa - e`) | 241 |
| explicit grammatical labels (`Part. praes. Ātm`) | 109 |
| derivation / alternation pairs (`dhū -- dhuva`) | 36 |
| residue after classification | 42 (5.5 %) |
| **…of which actually scored** (6 more drop on the length/token floor — `brū P. Ā` and
  five siblings the class regex misses for lacking a Roman numeral) | **36** (4.7 %) |

They are Bühler's **grammatical apparatus**, not exercise prose. Running provenance over
them wholesale would have produced a ~99 % "invented" figure that reads like a finding and
is an artefact of the input. `--scripts deva,iast` runs them; the default stays `deva`,
because 585 exercise sentences is the only denominator that means anything.

And the 36 genuine prose entries are **not attributable even in principle**, which exposes a
third false-positive class the Devanāgarī pass never hit: **grammatical metalanguage
collides with commentarial metalanguage.** All three IAST "adapted" hits are formula
collisions, not borrowings —

- `udgataṃ mukhaṃ yasya saḥ` matched `dṛḍhaṃ mukhaṃ yasyāḥ sā` (Mugdhāvabodhinī). Both are
  the standard **bahuvrīhi vigraha formula** `X mukhaṃ yasya saḥ`, which recurs throughout
  commentarial Sanskrit *because it is the analytical formula*.
- `jāgṛ jāgarāṃ cakāra` (a periphrastic-perfect drill) matched `prajāgarāṃcakāra` in Bhaṭṭi.
- `brāhmaṇaśca kṣatriyaśca vaiśyaśca` (a dvandva illustration) matched scattered varṇa
  vocabulary in the Śatapathabrāhmaṇa.

A sentence whose purpose is to *display a grammatical pattern* will match any text that uses
that pattern. That is not evidence of a source, and no threshold fixes it — it is a category
error about what the string is.

## Corrections to the H1212 write-up

Three claims in the first pass were wrong and are corrected here rather than quietly edited:

1. **"GRETIL is gated by an open rights @DECIDE (SamudraManthanam D5)."** False. D5 gates the
   **Russian-translation** sourcing budget; its Sanskrit/GRETIL side is marked converted.
   There is no D-numbered GRETIL rights decision anywhere in the org. The real constraint is
   a house convention recorded in
   [PROJECT_INTERLINKS](https://github.com/gasyoun/Uprava/blob/main/PROJECT_INTERLINKS.md):
   GRETIL plaintext is CC BY-NC-SA 4.0, so **do not commit raw source text — commit derived
   summaries only**. This pass honours that: it reads the gitignored raw dirs and emits
   verdicts plus short evidence snippets, and copies no corpus file into the repo.
2. **"Pañcatantra is absent from the local DCS export."** False — inherited from a stale
   comment in a kosha script. The Pañcatantra's Kashmirian recension is present under its own
   name, **Tantrākhyāyikā**, DCS `text_id` 391. It was in the haystack the whole time.
3. **"The 765 IAST sentences are a mechanical extension."** False, per the section above.

## Limitations — read before citing

- **Absence of evidence.** `invented` means *not found in these three corpora*, never
  "Bühler composed it". The 88.0 % remains an **upper bound** on invention — but a
  well-tested one: an 11 % corpus expansion aimed at the weakest spot moved it by 0.5 pp
  (see the corpus-expansion test above). Sanskrit gnomic verse still circulated in
  florilegia far beyond DCS (270 texts), Böhtlingk (7,537 sayings) and GRETIL.
- **Bühler is the 1923 Stockholm reprint**, a proxy for 1878 (the standing MG `@DO`,
  SanskritGrammar D4). The exercises are believed unrevised; unverified.
- **The IAST subset is apparatus, not exercises** — 42 of 765 entries survive
  classification and 36 clear the length floor to be scored; those are grammatical
  metalanguage that cannot be attributed even in principle (above).
- **Kāvya coverage is now broad, which is what makes the kāvya finding stand.** The GRETIL
  set tested includes Raghuvaṃśa and Kumārasaṃbhava (the latter also in DCS, `text_id` 390),
  Māgha, Bhāravi, Bāṇa, Daṇḍin, Aśvaghoṣa and Jayadeva. Bühler drew on none of them. The
  residual gap is minor court poetry and the commentarial literature, where a drill-sentence
  source is a priori unlikely.
- The matcher is **substring-based**, so it finds quotation and light adaptation. It will
  miss **paraphrase** (same verse, rewritten) exactly as the H311/H327 concordance does.
- **Verse-line granularity differs by corpus.** DCS rows are sentences, GRETIL rows are
  verse lines, *Indische Sprüche* rows are whole 2-line sayings. A needle spanning a GRETIL
  line break cannot match, so GRETIL recall is slightly conservative relative to DCS.

## Reproduce

```
python scripts/buhler_provenance.py
```

```
python scripts/buhler_provenance.py --no-gretil        # reproduce the H1212 two-corpus pass
python scripts/buhler_provenance.py --scripts deva,iast  # include the IAST apparatus residue
```

Reads [`scripts/data/sentences.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/sentences.json)
and three local corpora — DCS 2026 (`dcs_full.sqlite`, provenance-pinned to
`gasyoun/dcs-conllu` @ `04e0778d`, 754,726 sandhied sentences), Böhtlingk's *Indische
Sprüche* (`archive.sqlite`, table `subhashita`, 7,537 sayings), and GRETIL plaintext
(`SanskritSpellCheck/detectors/gretil_*_raw/`, 85,401 verse lines). **GRETIL is CC BY-NC-SA
4.0 and gitignored where it lives — this script reads it and emits derived verdicts, and
never copies a corpus file into the repo.** Transliteration is `sanskrit-util` throughout,
never hand-rolled. Runtime ~5 min, ~2.5 GB RAM.

_Analysis by Opus 4.8 (`claude-opus-4-8`), 19-07-2026 (H1212; corpus extension, IAST subset and corrections H1344)._

_Dr. Mārcis Gasūns_
