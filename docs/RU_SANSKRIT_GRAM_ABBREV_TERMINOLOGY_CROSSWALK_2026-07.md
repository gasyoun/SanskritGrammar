# Russian Sanskrit grammar abbreviation terminology crosswalk

_Created: 31-07-2026 · Last updated: 04-08-2026_

**Handoff:** [H2048](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2048-Fable_SanskritGrammar_ru-sanskrit-gram-abbrev-crosswalk_31.07.26.md)  
**Executor this pass:** Grok 4.5 (`grok-4.5`) — **explicit override** of the Fable filename lock; dual-run so a later Fable pass can compare.  
**✅ Fable dual-run confirm (H2053, 04-08-2026):** Fable 5 (`claude-fable-5`) independently re-opened every load-bearing citation below (legend line numbers, footnote-tag counts, §-cites, dictionary-text fetch) — **all verified, zero conflicting cells**; the non-case Latin-stay + tooltip policy was re-derived independently and stands. Net-new folded in this pass: `U.` (Ubhayapada) row, Knauer `denom.` de-tentativized. Full comparison: [RU_SANSKRIT_GRAM_ABBREV_TERMINOLOGY_CROSSWALK_H2053_FABLE_COMPARE_2026-08.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RU_SANSKRIT_GRAM_ABBREV_TERMINOLOGY_CROSSWALK_H2053_FABLE_COMPARE_2026-08.md).  
**Stop condition:** durable table: every high-frequency PWG grammatical `<ab>` family **except cases** (number/gender · voice/stem · tense/mood · non-finite/POS) has ≥1 attested form from a **named** source below — not agent invention. Cases filled for completeness; **recommended visible = Latin (locked MG 31-07)**.

---

## Locked (MG 31-07-2026) — do not re-open

**Cases in visible pwg_ru article text stay Latin:** `Acc.` / `Loc.` / `Instr.` / `Dat.` / `Abl.` / `Gen.` / `Nom.` / `Voc.` (and case-folded variants). Not `акк.` / `лок.` / `инстр.` as the visible token.

- Tooltip / legend: full Latin + Russian category name (Kochergina textbook model: `A. - accusativus - винительный падеж`).
- [LES-1990](https://samskrtam.ru/sanskrit-lexicon/les-1990/006b.html) (`акк.`, `вин. п.`, …) is **encyclopedia metalanguage**, not a dictionary stylesheet. Prior art [ABBREV_LES1990_SRAVNENIE_2026-07.md](https://github.com/gasyoun/SanskritLexicography/blob/master/RussianTranslation/pwg_ru/ABBREV_LES1990_SRAVNENIE_2026-07.md) that *sanctioned* visible `акк.` via LES is **overruled for visible tokens** by MG 31-07.
- H2047 must not re-vote cases; this report does not either.

---

## Method

1. Prefer each book’s **legend / front-matter / explicit inventory** over hunting prose.
2. Cell = attested short form or explicit full name used as a tag; else `—` with where we looked.
3. Three genres kept separate: **grammar textbook** · **encyclopedia (LES)** · **dictionary article text**.
4. No attested RU short form in the grammar corpus → recommend **Latin-stay + full RU in tooltip** (except cases: Latin-stay already locked).
5. Never invent `фут.` / `прекат.` / `конъ.` without a quote.

**Prior art (not re-derived):**

- [ABBREV_UNIFIED_LIST_PROPOSAL_2026-07.md](https://github.com/gasyoun/SanskritLexicography/blob/master/RussianTranslation/pwg_ru/ABBREV_UNIFIED_LIST_PROPOSAL_2026-07.md) — H1303 inventory + proposed RU forms (proposals, not votes).
- [ABBREV_LES1990_SRAVNENIE_2026-07.md](https://github.com/gasyoun/SanskritLexicography/blob/master/RussianTranslation/pwg_ru/ABBREV_LES1990_SRAVNENIE_2026-07.md) — LES comparison (case LES→акк. **not** to be applied as visible).
- [ABBREVIATIONS_RU.md](https://github.com/gasyoun/SanskritLexicography/blob/master/RussianTranslation/ABBREVIATIONS_RU.md) — 10-07 “grammar labels stay Latin” baseline.

---

## Corpus inventory (every required source)

| # | Path / source | Legend / list found? | What we use |
|---|---|---|---|
| 1 | `KocherginaUchebnik_1998` | **Yes** — «Условные сокращения» in [`Kochergina_unicode.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/Kochergina_unicode.mdx) L168–227 | Full Latin-short + Latin full + RU name triad |
| 2 | `KnauerFrazy_1908` | **No** dedicated list | Inline footnote tags in [`Frazy-Knauer-03.05.2023.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/KnauerFrazy_1908/Frazy-Knauer-03.05.2023.mdx): `impf.`, `caus.`, `opt.`, `pass.`, `med.`, `imper.`, `aor.`, `pp.`, `ger.`, `part.`, `sg.`, `pl.`, `loc. abs.` |
| 3 | `Elizarenkova_2004` | **No** abbreviation legend | Local tree has PDF only (`Indoarian_27_01_04_Sanskrit-part.pdf`, 70 pp., «Языки мира» 2004). Prose uses Russian full terms (*именительный падеж*, *причастие*, *деепричастие*, *род. п.*, *местн. п.*). Not a compact tag system |
| 4 | `BuhlerLeitfaden_1923` | **No** abbreviation legend | Front matter is editor’s preface only ([`Buhler_Unicode.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/Buhler_Unicode.mdx) L1–32). Урок I names tenses in Latin full + Russian: *indicativus (настоящее время)*, *imperfectum*, *imperativus*, *optativus (potentialis)*, *perfectum*, *аорист*, *parasmaipada*, *ātmanepada* |
| 5 | `ApteSyntax_1885` | List exists but **source-sigla only** | [`Apte-unicode.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/Apte-unicode.mdx) L88–163: *A. R.*, *Bg.*, *Mb.* … — literary sources, **not** grammatical categories. EN contrast book; no PWG-family grammar abbrev legend |
| 6 | `GasunsDhatu_2014` | **Partial** — «Принятые сокращения» | [`02_gasuns-dhatu-PhD-text2.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/02_gasuns-dhatu-PhD-text2.mdx) L3165–3227: mostly bibliographic; grammar hits: `Abl.`, `Nom.`, `Ind.`, `praes.`, `sg.` |
| 7 | `TolchelnikovTalmud_2026` | **No** grammar-abbrev legend | Morphological position codes (МП / Поз.); not PWG-style case/tense tags |
| 8 | `ZalizniakMorphology_1975` | **No** | English morphophonology paper only in tree; no RU legend |
| 9 | `ZalizniakOcherk_1978` | **Inline inventory** (not a front list) | [`Zalizniak-Ocherk_29-11-20-aligned.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/Zalizniak-Ocherk_29-11-20-aligned.mdx) §71 cases, §109 conjugation: `Nom.`/`N.`, `Acc.`/`A.`, … + `sg`/`du`/`pl`, `act.`/`med.`/`pass.`, `impf.`/`aor.`/`perf.`, `indic.`/`imper.`/`opt.` |
| 10 | `ZalizniakKonspekt_2004` | **No** list | Dense paradigms; Latin tags in body (`3 sg act`, `v/g`) without a separate legend |
| 11 | `WhitneyGrammar_1889` | EN baseline, **no RU** | Full English category names / Latin technical terms in continuous prose; not a Russian tag system |
| L | LES-1990 | **Yes** | [samskrtam.ru LES abbreviations](https://samskrtam.ru/sanskrit-lexicon/les-1990/006b.html) — general linguistics; **no** aorist/causative/medium |
| D | Dict text (named) | **Kochergina 1987** (required minimum) | [samskrtam.ru Kochergina small](https://samskrtam.ru/sanskrit-lexicon/small/kochergina_sm.html): visible tags **Latin** — `Acc.`, `Abl.`, `Dat.`, `Loc.`, `Gen.`, `P.`/`A.` (pada), `pr.`, `fut.`, `pf.`, `aor.`, `pp.`, `inf.`, `caus.` Also listed on sources page: Kossovich 1854, Frish 1956, Knauer dict, Kudriavsky 1908 (not fully re-sampled this pass) |

### Seed quote — Kochergina textbook legend (do not re-OCR)

Source: [`Kochergina_unicode.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/Kochergina_unicode.mdx) L168–227:

```
A. - accusativus - винительный падеж
Abl. - ablativus - отложительный падеж
adj. - adjectivum - прилагательное
aor. - aoristus - аорист
Ā. - Ātmanepada - средний залог
caus. - causativum - каузативный глагол
des. - desiderativum - желательный глагол
den. - denominativum - отыменный глагол
du. - dualis - двойственное число
fut. - futurum - будущее время
ger. - gerundium - деепричастие
imp. - imperativus - повелительное наклонение
impf. - imperfectum - прошедшее время
int. - intensivum - интенсивный глагол
inf. - infinitivum - инфинитив
opt. - optativus - желательное наклонение
P. - parasmaipada - действительный залог
p. - passivum - страдательный залог
part. - participium - причастие
pf. - perfectum - прошедшее время
pl. - pluralis - множественное число
pr. - praesens - настоящее время
sg. - singularis - единственное число
*m* / *f* / *n* - masculinum / femininum / neutrum
…
```

---

## Crosswalk tables

Cells use short citations: `K:L###` = KocherginaUchebnik line; `Z§n` = Zalizniak Ocherk section; `B:L###` = Bühler; `Kn:fn` = Knauer footnote pattern; `G:L###` = Gasuns; `LES`; `D-Koch` = Kochergina dictionary article text. Empty = not attested as a **tag** in that source’s apparatus.

**Recommended visible pwg_ru** = what the article column should show.  
**Recommended tooltip** = hover / legend string.

### 1) Cases (recommendation locked Latin)

| PWG surface (folded) | Latin full | KocherginaUch_1998 | Knauer | Elizar. | Bühler | Apte | Gasuns | Talmud | Zal.Morph | Zal.Ocherk | Zal.Kons | Whitney | LES-1990 | Dict text (Kochergina 1987) | **Recommended visible** | **Recommended tooltip** | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Acc. / acc. | accusativus | `A.` K:L170 | — | full RU *вин.* in prose | full RU *винительный* B:L307 area | — | — | — | — | `Acc.`/`A.` Z§71 | inline | Accusative | `акк.` · `вин. п.` | `Acc.` D-Koch | **`Acc.`** | accusativus — винительный падеж | LOCK Latin |
| Nom. / nom. | nominativus | `N.` K:L205 | — | *имен. п.* prose | *именительный* | — | `Nom.` G:L3196 | — | — | `Nom.`/`N.` Z§71 | inline | Nominative | `им. п.` | (paradigm labels) | **`Nom.`** | nominativus — именительный падеж | LOCK |
| Gen. / gen. | genetivus | `G.` K:L190 | — | *род. п.* | full | — | — | — | — | `Gen.`/`G.` Z§71 | inline | Genitive | `ген.` · `род. п.` | `Gen.` D-Koch | **`Gen.`** | genetivus — родительный падеж | LOCK |
| Dat. / dat. | dativus | `D.` K:L182 | — | *дат.* | full | — | — | — | — | `Dat.`/`D.` Z§71 | inline | Dative | `дат. п.` | `Dat.` D-Koch | **`Dat.`** | dativus — дательный падеж | LOCK |
| Abl. / abl. | ablativus | `Abl.` K:L173 | — | *отлож.* | full | — | `Abl.` G:L3169 | — | — | `Abl.` Z§71 | inline | Ablative | `абл.` | `Abl.` D-Koch | **`Abl.`** | ablativus — отложительный падеж | LOCK |
| Instr. / instr. | instrumentalis | `I.` K:L196 | — | *твор.* | full | — | — | — | — | `Instr.`/`I.` Z§71 | inline | Instrumental | `тв. п.` | (gov. labels) | **`Instr.`** | instrumentalis — творительный падеж | LOCK |
| Loc. / loc. | locativus | `L.` K:L200 | `loc. abs.` Kn:fn | *местн. п.* | full | — | — | — | — | `Loc.`/`L.` Z§71 | inline | Locative | `лок.` | `Loc.` D-Koch | **`Loc.`** | locativus — местный падеж | LOCK |
| Voc. / voc. | vocativus | `V.` K:L222 | — | — | — | — | — | — | — | `Voc.`/`V.` Z§71 | inline | Vocative | — | — | **`Voc.`** | vocativus — звательная форма | LOCK |

### 2) Number · gender · person

| PWG surface (folded) | Latin full | KocherginaUch | Knauer | Elizar. | Bühler | Apte | Gasuns | Talmud | Zal.Morph | Zal.Ocherk | Zal.Kons | Whitney | LES-1990 | Dict (Koch.) | **Recommended visible** | **Recommended tooltip** | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sg. / Sg. / sing. | singularis | `sg.` K:L218 | `sg.` Kn:fn | *ед. ч.* prose | *ед. ч.* B:L134 | — | `sg.` G:L3214 | — | — | `sg` Z§71/§109 | `sg` inline | singular | `ед. ч.` | — | **`sg.`** | singularis — единственное число | LES +«ч.» is encyclopedia density; Koch/Zal use bare `sg.` |
| pl. / Pl. | pluralis | `pl.` K:L212 | `pl.` Kn:fn | *мн. ч.* | *мн. ч.* | — | — | — | — | `pl` Z§71 | `pl` | plural | `мн. ч.` | — | **`pl.`** | pluralis — множественное число | |
| du. / Du. | dualis | `du.` K:L185 | — | *дв. ч.* | *дв. ч.* | — | — | — | — | `du` Z§71 | — | dual | `дв. ч.` | — | **`du.`** | dualis — двойственное число | |
| masc. / m. | masculinum | `*m*` K:L201 | — | *муж. р.* | — | — | — | — | — | `m` Z§71 | — | masculine | `муж. род` | — | **`m.`** or Latin-stay `masc.` | masculinum — мужской род | Koch italic *m*; LES long form |
| fem. / f. | femininum | `*f*` K:L188 | — | *жен. р.* | — | — | — | — | — | `f` Z§71 | — | feminine | `жен. род` | — | **`f.`** / `fem.` | femininum — женский род | |
| neutr. / n. | neutrum | `*n*` K:L202 | — | *ср. р.* | — | — | — | — | — | `n` Z§71 | — | neuter | `ср. род` | — | **`n.`** / `neutr.` | neutrum — средний род | not bare `ср.` (collides with `ср.` = vgl.) |
| pers. / 1./2./3. | persona | — | `2. sg.` etc. | *лицо* | *1/2/3 л.* | — | — | — | — | `1 sg`, `3 pl` Z§109 | `3 sg act` | person | `л.` | — | Latin person digit + number | e.g. 3. sg. — 3-е лицо ед. ч. | LES `л.` for person |

### 3) Voice · secondary stems

| PWG surface (folded) | Latin full | KocherginaUch | Knauer | Elizar. | Bühler | Apte | Gasuns | Talmud | Zal.Morph | Zal.Ocherk | Zal.Kons | Whitney | LES-1990 | Dict (Koch.) | **Recommended visible** | **Recommended tooltip** | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| act. / Act. / P. (pada) | activum / parasmaipada | `P.` K:L207 | — | *действ. залог* | *parasmaipada* B:L116 | — | — | — | — | `act.` · parasmaipada Z§109 | `act` | active | — | `P.` D-Koch | **`act.`** or **`P.`** (pada sense) | activum / parasmaipada — действительный залог | PWG `act.` ≠ Medizin |
| pass. / Pass. / p. | passivum | `p.` K:L209 | `pass.` Kn:fn | *страд.* | *passivi* prose | — | — | — | — | `pass.` Z§109 | — | passive | — | (pp. labels) | **`pass.`** | passivum — страдательный залог | |
| Med. / med. (voice) / Ā. | medium / ātmanepada | `Ā.` K:L177 | `med.` Kn:fn | *средн. залог* | *ātmanepada* B:L116 | — | — | — | — | `med.` · ātmanepada Z§109 | — | middle | — | `A.` D-Koch (Ātmanepada) | **`Med.`** (capital) / **`Ā.`** | medium / ātmanepada — средний залог | **Register:** capital `Med.` = voice; lower `med.` = Medizin (H1303) |
| caus. / Caus. | causativum | `caus.` K:L179 | `caus.` Kn:fn | *каузатив* prose | *causativ* B:L2302 | — | — | — | — | (prose *каузатив*) | — | causative | — | `caus.` D-Koch | **`caus.`** | causativum — каузативный глагол | N8 had proposed `кауз.`; **no RU short tag** in Koch/Zal legends — Latin is the attested textbook tag |
| desid. / Desid. / des. | desiderativum | `des.` K:L184 | — | — | — | — | — | — | — | — | — | desiderative | — | — | **`des.`** / **`desid.`** | desiderativum — желательный глагол | Koch `des.`; PWG often `desid.` |
| intens. / Intens. / int. | intensivum | `int.` K:L199 | — | — | *intensive* B lessons | — | — | — | — | — | — | intensive | — | — | **`int.`** / **`intens.`** | intensivum — интенсивный глагол | |
| denom. / den. | denominativum | `den.` K:L183 | `denom.` Kn:fn (×1, H2053-verified) | — | — | — | — | — | — | — | — | denominative | — | — | **`den.`** / **`denom.`** | denominativum — отыменный глагол | |
| U. / ubhay. | ubhayapada | `U.` K:L221 | — | — | — | — | — | — | — | — | — | both padas | — | `U.` D-Koch | **`U.`** | ubhayapada — имеющий оба залога | Third pada member beside `P.`/`Ā.`; attested in legend AND dict text (H2053 net-new) |

### 4) Tense · mood

| PWG surface (folded) | Latin full | KocherginaUch | Knauer | Elizar. | Bühler | Apte | Gasuns | Talmud | Zal.Morph | Zal.Ocherk | Zal.Kons | Whitney | LES-1990 | Dict (Koch.) | **Recommended visible** | **Recommended tooltip** | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| praes. / Praes. / pr. | praesens | `pr.` K:L215 | — | *наст. вр.* | *indicativus praesentis* B:L147 | — | `praes.` G:L3205 | — | — | *настоящее* Z§109 | — | present | `наст. вр.` | `pr.` D-Koch | **`pr.`** / **`praes.`** | praesens — настоящее время | LES Russian; textbooks Latin |
| aor. / Aor. | aoristus | `aor.` K:L176 | `aor.` Kn:fn | *аорист* | *аорист* B:L127 | — | — | — | — | `aor.` Z§109 | — | aorist | — | `aor.` D-Koch | **`aor.`** | aoristus — аорист | LES silent — not under LES jurisdiction |
| perf. / Perf. / pf. | perfectum | `pf.` K:L210 | — | *перфект* | *perfectum* B:L125 | — | — | — | — | `perf.` Z§109 | — | perfect | — | `pf.` D-Koch | **`pf.`** / **`perf.`** | perfectum — перфект | |
| fut. / Fut. | futurum | `fut.` K:L189 | — | *буд. вр.* | *будущее* B:L119–121 | — | — | — | — | *будущее* Z§109 | — | future | `буд. вр.` | `fut.` D-Koch | **`fut.`** | futurum — будущее время | Reject unattested visible `фут.` |
| imperf. / impf. | imperfectum | `impf.` K:L198 | `impf.` Kn:fn | *имперфект* | *imperfectum* B:L121 | — | — | — | — | `impf.` Z§109 | — | imperfect | — | — | **`impf.`** | imperfectum — имперфект (прошедшее) | |
| imperat. / imp. / imper. | imperativus | `imp.` K:L197 | `imper.` Kn:fn | *повел.* | *imperativus* B:L123 | — | — | — | — | `imper.` Z§109 | — | imperative | — | — | **`imp.`** / **`imperat.`** | imperativus — повелительное наклонение | |
| opt. / Opt. | optativus | `opt.` K:L206 | `opt.` Kn:fn | *оптатив* | *optativus (potentialis)* B:L125 | — | — | — | — | `opt.` Z§109 | — | optative | — | — | **`opt.`** | optativus — желательное / оптатив | |
| Conj. / conj. | conjunctivus | `conj.` = *союз* K:L180 | — | *конъюнктив* (Vedic note Z§109 n.) | — | — | — | — | — | *конъюнктив* Z§109 note | — | subjunctive | — | — | **`Conj.`** (mood) carefully | conjunctivus — конъюнктив | **Collision:** Koch `conj.` = conjunction; PWG mood needs tooltip; rare in classical PWG |
| prec. / Prec. / precat. | precativus | — | — | — | *precativus (benedictivus)* B:L125 | — | — | — | — | *прекатив* Z§109 | — | precative | — | — | **`prec.`** | precativus — прекатив / бенедиктив | No RU short form attested → **not** `прекат.` without inventing |
| potent. / pot. | potentialis | — | — | — | *(potentialis)* as opt. alias B:L125 | — | — | — | — | (folded into opt.) | — | potential | — | — | **`potent.`** or stay with `opt.` | potentialis — потенциалис (≈ opt.) | Bühler equates with optative |
| ind. / indic. | indicativus | `ind.` K:L195 | — | *изъявит.* | *indicativus* B:L119 | — | `Ind.` G:L3180 | — | — | `indic.` Z§109 | — | indicative | — | — | **`ind.`** | indicativus — изъявительное наклонение | |

### 5) Non-finite · POS sample

| PWG surface (folded) | Latin full | KocherginaUch | Knauer | Elizar. | Bühler | Apte | Gasuns | Talmud | Zal.Morph | Zal.Ocherk | Zal.Kons | Whitney | LES-1990 | Dict (Koch.) | **Recommended visible** | **Recommended tooltip** | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| partic. / part. | participium | `part.` K:L208 | `part.` Kn:fn | *причастие* | *причастие* | — | — | — | — | *причастия* Z§109 | — | participle | `прич.` | `pp.` for PPP | **`part.`** / **`partic.`** | participium — причастие | LES `прич.` OK for tooltip genre |
| pp. | part. perf. pass. | `pp.` K:L214 | `pp.` Kn:fn | *прич. прош.* | — | — | — | — | — | — | — | PPP | — | `pp.` D-Koch | **`pp.`** | participium perfecti passivi | |
| infin. / inf. | infinitivus | `inf.` K:L193 | — | *инфинитив* | — | — | — | — | — | *инфинитив* Z§109 | — | infinitive | `инф.` | `inf.` D-Koch | **`inf.`** / **`infin.`** | infinitivum — инфинитив | |
| absol. / Absol. / gerund. | absolutivus / gerundium | `ger.` K:L191 | `ger.` Kn:fn | *деепричастие* / *абсолютив* | — | — | — | — | — | *деепричастия (абсолютивы)* Z§109 | — | gerund / absolutive | `дееприч.` | — | **`ger.`** or **`absol.`** | gerundium / absolutivus — деепричастие / абсолютив | PWG *Gerundium* = Skt absolute; prefer not bare `герунд.` without note |
| subst. / S. | substantivum | `S.` K:L219 | — | *сущ.* | — | — | — | — | — | — | — | noun | — | — | **`subst.`** / **`S.`** | substantivum — существительное | |
| adj. | adjectivum | `adj.` K:L174 | — | *прил.* | — | — | — | — | — | — | — | adjective | `прил.` | — | **`adj.`** | adjectivum — прилагательное | |
| intrans. / trans. | intransitivum / transitivum | — | — | *неперех./перех.* | — | — | — | — | — | — | — | in-/transitive | `неперех.` / `перех.` | — | **`intrans.`** / **`trans.`** | … | LES matches school Russian |
| impers. | impersonale | — | — | — | — | — | — | — | — | — | — | impersonal | — | — | **`impers.`** | impersonale — безличное | LES silent; optional tooltip `безл.` only if human ratifies |

---

## Synthesis for pwg_ru (non-case)

### What Russian Indology actually tags

1. **Kochergina textbook + Kochergina dictionary + Knauer footnotes + Zalizniak Ocherk** converge on **Latin short forms** for the Sanskrit-specific verbal system (`aor.`, `caus.`, `opt.`, `impf.`, `pp.`, `Ā.`/`P.`, …). The Russian half of the Koch triad is the **full category name in the legend**, not a second short-token layer.
2. **LES-1990** is authoritative for *general* linguistics (`ед. ч.`, `прич.`, `инф.`, `наст. вр.`, `буд. вр.`, case Latinisms `акк.`/`лок.`). It does **not** cover aorist, perfect, causative, desiderative, medium, precative. Using LES as a force to invent `фут.`/`аор.`/`кауз.` as **visible dictionary tokens** over-extends its genre (confirmed in ABBREV_LES1990_SRAVNENIE §5).
3. **H1303 proposed RU shorts** (`кауз.`, `аор.`, `фут.`, `прекат.`, `конъ.`) are **agent-side proposals** for voting, **not** forms harvested from the eleven-grammar legends. This crosswalk therefore defaults non-case high-frequency tags to **Latin-stay + Koch-style tooltip**, unless a human later ratifies a RU short that LES or school metalanguage already owns (`прич.`, `инф.`, `ед.`…).

### Recommended policy (Grok dual-run)

| Band | Visible pwg_ru | Tooltip |
|---|---|---|
| **Cases** | Latin (locked) | Latin full + RU case name (Koch) |
| **Number / gender** | Latin `sg.`/`pl.`/`du.` · `m.`/`f.`/`n.` | LES-style full RU OK (`ед. ч.`, `муж. род`) |
| **Sanskrit verb system** (aor, perf, fut, impf, opt, imperat, prec, caus, desid, intens, denom, act/pass/med) | **Latin short** as in Koch/Knauer/Zal/dict | Latin full + RU full name; **do not** invent `фут.`/`прекат.`/`кауз.` without human vote |
| **POS with LES hit** (partic, infin, trans/intrans) | Prefer Latin or LES (`прич.`/`инф.`) — human pick; both attested | Either |
| **Encyclopedia-only forms** | Never as sole justification for visible case RU | LES forms may appear in tooltips |

### Feed-forward

- **H2047:** cases already lock; non-case sheet rows without a quote in this table should not offer agent-invented RU as the default approve option.
- **H1303 / `RU_MAP` / `ABBREVIATIONS_RU.md`:** cite this file; LES→`акк.` **must not** be applied to visible tokens.
- **CONTRADICTIONS §7:** cases side → Latin-stay (MG 31-07).

---

## Non-goals (this pass)

- Not regenerating the HTML sheet (H2047).
- Not content-grade voting standard (H2046).
- Not re-arguing cases.
- Not treating LES as a dictionary stylesheet.
- Not full OCR of Elizarenkova beyond PDF text layer (no abbreviation legend present).
- Not exhaustive re-sampling of every named СЯР dictionary on samskrtam.ru beyond Kochergina 1987 (minimum D satisfied; others named on [sources page](https://samskrtam.ru/sanskrit-lexicography-sources/)).

---

## Provenance

| Field | Value |
|---|---|
| Handoff | H2048 |
| Intended executor (filename) | Fable 5 (`claude-fable-5`) |
| Actual executor | Grok 4.5 (`grok-4.5`), human “run anyway / dual-run for Fable comparison” |
| Date | 31-07-2026 |
| Worktree | `SanskritGrammar-h2048-32116` branch `h2048-gram-abbrev-crosswalk` |
| Dual-run confirm | Fable 5 (`claude-fable-5`), 04-08-2026, [H2053](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2053-Fable_SanskritGrammar_h2048-grok-crosswalk-fable-compare_01.08.26.md) — all citations verified, 0 conflicts; compare memo: […H2053_FABLE_COMPARE_2026-08.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RU_SANSKRIT_GRAM_ABBREV_TERMINOLOGY_CROSSWALK_H2053_FABLE_COMPARE_2026-08.md) |

_Dr. Mārcis Gasūns_
