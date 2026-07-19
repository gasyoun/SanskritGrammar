_Created: 17-07-2026 · Last updated: 19-07-2026_

# What three Sanskrit primers copied from each other — a reuse analysis for teachers

**For:** anyone building or teaching a first-year Sanskrit course who wants to know
where the standard "model sentences" come from, which are century-tested, and which
are safe to reuse. Companion to the machine-generated
[`Concordance/catalog.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/Concordance/catalog.mdx)
(the raw 124-row list) — this doc is the *reading* of that list.

Three primers, one lineage:

| Book | Year | Language of instruction | Devanāgarī exercise sentences |
|---|---|---|---|
| **Bühler**, *Leitfaden für den Elementarcursus des Sanskrit* | 1878 (repo carries the 1923 Stockholm reprint) | German | 603 |
| **Knauer**, *Учебник санскритского языка* / *Frazy* | 1908 | German → Russian tradition | 171 |
| **Kochergina**, *Учебник санскрита* | 1998 | Russian | 647 |

They are not three independent books. Knauer's exercise sentences are largely
**Bühler's**, and Kochergina's are drawn from **both**. This document quantifies exactly
how much, how faithfully, and — the part that matters for teaching — what that tells us.

---

## The three questions, answered

### Q2 — Which of Knauer's sentences came from Bühler?

**86 shared-sentence clusters** link Bühler and Knauer (79 Bühler↔Knauer-only + 7 present in
all three books). Since Knauer has only **171** Devanāgarī exercise sentences in total, roughly
**half of Knauer's exercise material is Bühler's**, re-set 30 years later. The full list with
lesson numbers is columns *Bühler (lesson)* and *Knauer (Nr.)* of the
[concordance catalog](https://github.com/gasyoun/SanskritGrammar/blob/main/Concordance/catalog.mdx).

### Q3 — Kochergina took from both. Is there a catalogue?

Yes — the same [catalog](https://github.com/gasyoun/SanskritGrammar/blob/main/Concordance/catalog.mdx).
**45 clusters** touch Kochergina: 33 come from Bühler, 5 from Knauer, 7 from all three. Against
her **647** Devanāgarī sentences that is a much thinner borrowing rate than Knauer's — Kochergina
wrote most of her own material but kept a **canonical core** (see below).

Breakdown of all 124 shared clusters:

| Region | Clusters |
|---|---|
| All three books | 7 |
| Bühler ↔ Knauer only | 79 |
| Bühler ↔ Kochergina only | 33 |
| Knauer ↔ Kochergina only | 5 |

### Q1 — Where did **Bühler** get *his* sentences? (answered)

**He wrote about nine tenths of them himself.** Of his 585 Devanāgarī exercise sentences
(603 entries minus Lesson XLVIII's 18 alphabet-chart rows), matched against DCS 2026 and
Böhtlingk's *Indische Sprüche* by
[`scripts/buhler_provenance.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/buhler_provenance.py):

| Verdict | n | share |
|---|---:|---:|
| verbatim **quotation** | 50 | 8.5 % |
| **adapted** (real verse, a word changed) | 16 | 2.7 % |
| **invented** grammar drill | 518 | 88.5 % |
| unknown (hit too short to judge) | 1 | 0.2 % |

Three qualifications matter more than the headline:

- **Attestation is late-book.** Nothing before Lesson XII is attested; lessons I–XXIV run
  6.9 % attested, XXV–XLVII run 17.6 %. Bühler writes his own prose while paradigms are
  being learned and switches to literature once the student can read it.
- **The unit of borrowing is the verse, not the sentence.** 85 % of attested sentences sit
  in consecutive runs — Bühler splits one śloka across two exercise numbers (and sometimes
  runs several verses back to back). The 66 attested sentences are really ~39 borrowed verses.
- **The source is gnomic literature, not the Veda.** Subhāṣita/nīti (*Indische Sprüche* 28,
  Hitopadeśa 8, Bhartṛhari 4) plus dharmaśāstra (13) are four fifths of the hits; kāvya is
  nearly absent. And the sentences *naming* Kālidāsa and Pāṇini are invented — they are
  about those authors, not from them.

`लोभात्क्रोधः प्रभवति…` is confirmed a verbatim *Hitopadeśa* quotation. `त्वं जीव शरदः शतम्`
is **adapted, not quoted**: the formula is genuinely Vedic and recurs across the gṛhya
literature, but Bühler's exact line matches no attested text — he assembled it from stock
parts. Full method, the three false-positive classes that had to be eliminated, the
hand-adjudicated cases and the limitations (`invented` = *not found*, never *composed*):
[`BUHLER_SENTENCE_PROVENANCE_ADJUDICATION.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/BUHLER_SENTENCE_PROVENANCE_ADJUDICATION.md).

---

## "Are they 1-to-1 or modified?" — the fidelity axis

Computed per cluster by [`scripts/fidelity_axis.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/fidelity_axis.py)
(reuses the concordance clustering + the H327 near-match verdicts;
outputs [`scripts/data/fidelity.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/fidelity.json)
and [`.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/fidelity.csv)):

| Verdict | Clusters | Meaning |
|---|---|---|
| **Identical** | 84 (68%) | Verbatim copy, character-for-character |
| **Orthographic only** | 31 (25%) | Same sentence, different spelling convention (anusvāra vs homorganic nasal, geminate spelling, visarga dropped, त/द sandhi) |
| **Modified** | 9 (7%) | Flagged as textually different |

**The honest headline: the copying is essentially verbatim.** And the "modified" 9 overstate it —
inspection shows **6 of the 9 are sentence-splitter truncation artifacts** (one side was clipped at
a lesson/page boundary: C0001, C0047, C0063, C0078, C0113), not editorial changes. Only **three**
are genuine reworkings:

| Cluster | Earlier | Later | The change |
|---|---|---|---|
| C0114 | Bühler `हृद्येष पुमान्…` | Knauer `हृदि साधुः पुमान्…` | lexical: *this* man → the *good* man (एष → साधुः) |
| C0121 | Knauer `नानुज्ञातो जगाम…` | Kochergina `स जगाम…` | dropped the "not-permitted" opening clause |
| C0119 | Bühler `…नरः सुप्ताः` | Knauer `भुक्त्वा पीत्वा…नराः सुप्ताः` | number: *the man* → *men* slept |

Directional view — when a later author borrowed, how faithful were they:

| Transmission | Shared edges | Verbatim | Spelling-only | Reworded |
|---|---|---|---|---|
| Bühler → Knauer | 88 | 59 | 23 | 6 |
| Bühler → Kochergina | 40 | 32 | 6 | 2 |
| Knauer → Kochergina | 12 | 7 | 4 | 1 |

So across ~120 years and a change of instruction language from German to Russian, the model
sentences travelled **as fixed objects**. The real variation is not content but **orthographic
convention** — which is a normalization opportunity, not a scholarly disagreement.

---

## In how many ways can we compare the list?

Nine axes. Five are computed, four are open (the map for future work):

| # | Axis | Question it answers | Status |
|---|---|---|---|
| 1 | **Set membership** | which books share a sentence (Venn) | ✅ [catalog](https://github.com/gasyoun/SanskritGrammar/blob/main/Concordance/catalog.mdx) |
| 2 | **Fidelity / mutation** | 1:1 vs orthographic vs reworded | ✅ this doc |
| 3 | **Sequencing** | is a shared sentence taught at a comparable point? | ✅ [S1 τ result](https://github.com/gasyoun/SanskritGrammar/blob/main/S1_TEXTBOOK_SEQUENCING_TAU_RESULT.md) |
| 4 | **Selection pressure** | which Bühler sentences each successor kept vs dropped | ⚪ derivable from catalog |
| 5 | **Transmission direction / stemma** | is a later variant closer to Bühler or to the intermediary | ⚪ open |
| 6 | **Primary-source provenance** | quotation vs adapted vs invented (Q1) | ✅ [adjudication](https://github.com/gasyoun/SanskritGrammar/blob/main/BUHLER_SENTENCE_PROVENANCE_ADJUDICATION.md) |
| 7 | **Grammatical feature drilled** | which construction each sentence targets | ⚪ open |
| 8 | **Register / content** | Vedic vs nīti vs myth vs mundane drill | ⚪ open |
| 9 | **Cross-lingual gloss** | German vs Russian translations of the same sentence | ⚪ open |

---

## What it teaches — for the classroom

**1. There is a century-tested canonical core.** Seven sentences survived all three books,
1878 → 1998, across two teaching languages. These are the *load-bearing* model sentences of the
tradition — if you teach only seven "classic" Sanskrit primer sentences, teach these:

| ID | Sentence | Gloss | Grammar it drills | Bühler / Knauer / Koch. lesson |
|---|---|---|---|---|
| C0009 | अश्वेन जलं पीयते | "Water is drunk by the horse" | passive + instrumental of agent | X / 16 / XXIV |
| C0028 | क्षत्रिया युद्धे ऽरीन्मारयन्ति | "Warriors kill enemies in battle" | causative + locative | XVIII / 17 / XXXV |
| C0058 | पद्मं श्रिया वसतिः | "The lotus is Śrī's dwelling" | predicative instrumental | XIII / 3 / XIV |
| C0067 | भर्तारं…पत्नी देवानिव पूजयेत् | "A wife should honour her husband, and his father and mother, like gods" | optative + accusative + iva | XVI / 4 / XIX |
| C0070 | मधुना क्षीरेण च तुष्यन्ति बालाः | "Children are content with honey and milk" | instrumental of cause | VI / 2 / XIII |
| C0105 | सर्वे पौराः कालिदासेन रचितं नाटकं द्रष्टुमागच्छन् | "All the townsfolk came to see the play composed by Kālidāsa" | agent-instrumental + PPP + infinitive of purpose | XXX / 19 / XXIII |
| C0118 | हे स्वसः पित्रोर्गृहे तिष्ठेः | "O sister, may you stay in your parents' house" | vocative + dual genitive + optative | XVI / 4 / XIX |

Note the content: gods, kings, wives, sages, Kālidāsa. The canonical core is **culturally
loaded**, not neutral — it teaches grammar and a worldview together. That is a choice a modern
course inherits by reusing them, and one worth making consciously.

**2. Material and sequence are separable, and they were separated.** Kochergina drew more
*sentences* from Bühler (33) than from Knauer (5), yet her *ordering* tracks Knauer far more
closely — Kendall's τ = **0.83** (Knauer↔Kochergina) vs **0.45** (Bühler↔Kochergina) vs **0.24**
(Bühler↔Knauer), per the [S1 result](https://github.com/gasyoun/SanskritGrammar/blob/main/S1_TEXTBOOK_SEQUENCING_TAU_RESULT.md).
Reading: *what* to teach and *when* to teach it are independent editorial decisions, and the
Russian tradition (Knauer → Kochergina) converged on a shared **progression** even while each
author picked their own sentences. For curriculum design this is the key lesson — a good sentence
bank does not dictate a good sequence; the sequence is where the pedagogy actually lives.

**3. The tradition treats model sentences as fixed cultural objects.** 68% verbatim, 25%
spelling-only, ~2% genuinely reworded. Authors did not paraphrase or "improve" the inherited
sentences; they copied them. This is why a vetted primer sentence bank is a reusable asset — the
sentences have been classroom-tested for 120 years and the tradition itself refused to touch them.

**4. The only real drift is orthographic — a digitization opportunity, not a controversy.** The
differences between copies are anusvāra vs homorganic nasal (`ं` vs `ङ्/ञ्/ण्/न्/म्`), geminate
cluster spelling (`च्छ` vs `छ`), visarga retention, and त/द sandhi spelling. These are editorial
conventions of 1878/1908/1998, not different sentences. A digital edition can normalize them to a
single modern convention and recover a **clean, deduplicated canonical bank** — which is exactly
what the [concordance](https://github.com/gasyoun/SanskritGrammar/blob/main/Concordance/catalog.mdx)
clusters already are.

---

## Reproduce

```
python scripts/fidelity_axis.py       # -> scripts/data/fidelity.{json,csv} + summary
python scripts/buhler_provenance.py   # -> scripts/data/buhler_provenance.{json,csv} (Q1/axis 6)
```

Inputs, all already committed: [`scripts/data/matches.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/matches.json)
(235 pairwise matches), [`scripts/data/matches_review.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/matches_review.tsv)
(H327 orthographic verdicts), [`scripts/data/catalog.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/catalog.json)
(the 124 clusters).

## Limitations

- **Bühler is the 1923 Stockholm reprint**, a proxy for the 1878 first edition; the exercises are
  believed unrevised between editions but this is unverified (an MG `@DO`). Transmission *direction*
  rests on publication chronology (1878 < 1908 < 1998), which is safe for "Bühler is earliest".
- The concordance is an **automated difflib pass** (similarity ≥ 0.82). It catches near-identical
  reuse but **misses paraphrase** (same content, different wording), so the true borrowing may be
  larger than 124 clusters. The fidelity verdicts inherit this: "identical/orthographic" is
  reliable; the small "modified" bucket is contaminated by extraction-boundary truncation, hand-flagged above.
- Q1 (primary-source provenance) is now answered above; its own limitations — chiefly that
  `invented` means *not found in DCS + Indische Sprüche*, never *composed by Bühler* — are
  set out in [`BUHLER_SENTENCE_PROVENANCE_ADJUDICATION.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/BUHLER_SENTENCE_PROVENANCE_ADJUDICATION.md).

_Analysis by Opus 4.8 (`claude-opus-4-8`), 17-07-2026 (H1211); Q1/axis 6 added 19-07-2026 (H1212). Data pipeline: H311/H327._

_Dr. Mārcis Gasūns_
