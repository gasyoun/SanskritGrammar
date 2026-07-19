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
| `quotation` | 50 | 8.5 % | occurs verbatim in an attested text |
| `adapted` | 16 | 2.7 % | a real verse with a word changed for the grammar point |
| `invented` | 518 | 88.5 % | no attested source; constructed to drill a paradigm |
| `unknown` | 1 | 0.2 % | verbatim hit too short to be evidence (`evaṃ vadanti`) |

**So ~11 % of Bühler's exercises are literature and ~89 % are his own drill prose.** MG's
Q1 intuition — that sentences like `त्वं जीव शरदः शतम्` and `लोभात्क्रोधः प्रभवति…` come
from real literature — is borne out in kind but split in verdict: `लोभात्क्रोधः…` is a
verbatim *Hitopadeśa* quotation, while `त्वं जीव शरदः शतम्` is **adapted, not quoted** (see
the hand-adjudicated cases below). Either way both are the minority case.

## Three findings the raw split does not show

**1. Attestation is a late-book phenomenon.** Nothing before Lesson XII is attested at
all. Lessons I–XXIV run 6.9 % attested (24/347); lessons XXV–XLVII run 17.6 % (42/238) —
a 2.5× jump. Bühler writes his own sentences while the student is learning paradigms and
switches to real literature once the student can read it. Provenance is therefore a
*curricular* variable, not a stylistic one, and any per-lesson claim must control for it.

**2. 85 % of attested sentences sit in consecutive runs.** 56 of the 66 attested sentences
(84.8 %) are adjacent to another attested sentence, forming 20 runs. `buhler-XIII-304` +
`-305` are the two lines of *Hitopadeśa* I's `lobhāt krodhaḥ prabhavati…`; `-341`/`-342`
and `-464`/`-465` likewise. Bühler splits a verse across consecutive exercise numbers, one
pāda-pair each.

Not every run is a pair: 12 runs are 2 long, two are 3, five are 4 (`-447`–`-450` is two
verses back to back), and `-824`–`-829` runs to six. **The unit of borrowing is the verse,
not the sentence** — so "66 attested sentences" is really **~39 borrowed verses**
(Σ⌈run/2⌉ over the 20 runs plus 10 singletons), and counting sentences double-counts the
borrowing.

**3. The source profile is nīti, not Veda or kāvya.** Of the 66:

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

Gnomic literature (Sprüche + Hitopadeśa + Śatakatraya = 40, 61 %) plus dharmaśāstra
(Manu/Baudhāyana/Vasiṣṭha/Gautama = 13, 20 %) account for four fifths. Kāvya is nearly
absent, and the Veda contributes 3. Bühler drills on *maxims* — short, syntactically
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

The 16 `adapted` rows were read individually. All 16 stand; the interesting ones are real
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

## Limitations — read before citing

- **Absence of evidence.** `invented` means *not found in these two corpora*, never
  "Bühler composed it". Sanskrit gnomic verse circulated in florilegia far beyond DCS
  (270 texts) and Böhtlingk (7,537 sayings). The 88.5 % is an **upper bound** on
  invention; the true quotation share can only rise as corpora are added.
- **GRETIL was deliberately not ingested** — the org's GRETIL rights budget is an open
  `@DECIDE` (SamudraManthanam D5). The obvious next corpus is also the gated one.
- **Pañcatantra is absent from the local DCS export**, and it is exactly the register
  that dominates the hits. Several *Indische Sprüche* attributions point at Pañcatantra
  editions, so direct Pañcatantra matching would likely move the number.
- **Bühler is the 1923 Stockholm reprint**, a proxy for 1878 (the standing MG `@DO`,
  SanskritGrammar D4). The exercises are believed unrevised; unverified.
- **The 765 IAST-script Bühler sentences were not processed** — this pass covers the 603
  Devanāgarī entries only, per the handoff scope. Extending to them is mechanical.
- The matcher is **substring-based**, so it finds quotation and light adaptation. It will
  miss **paraphrase** (same verse, rewritten) exactly as the H311/H327 concordance does.

## Reproduce

```
python scripts/buhler_provenance.py
```

Reads [`scripts/data/sentences.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/sentences.json)
and two rights-settled local corpora — DCS 2026 (`dcs_full.sqlite`, provenance-pinned to
`gasyoun/dcs-conllu` @ `04e0778d`, 754,726 sandhied sentences) and Böhtlingk's *Indische
Sprüche* (`archive.sqlite`, table `subhashita`, 7,537 sayings). Transliteration is
`sanskrit-util` throughout, never hand-rolled. Runtime ~4 min, ~2 GB RAM.

_Analysis by Opus 4.8 (`claude-opus-4-8`), 19-07-2026 (H1212)._

_Dr. Mārcis Gasūns_
