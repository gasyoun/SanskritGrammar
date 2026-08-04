# H2053 Fable dual-run compare — RU Sanskrit grammar abbreviation crosswalk

_Created: 04-08-2026 · Last updated: 04-08-2026_

**Handoff:** [H2053](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2053-Fable_SanskritGrammar_h2048-grok-crosswalk-fable-compare_01.08.26.md) — dual-run residual after the [H2048](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H2048-Fable_SanskritGrammar_ru-sanskrit-gram-abbrev-crosswalk_31.07.26.md) model-lock override.
**Lane A (override):** Grok 4.5 (`grok-4.5`), 31-07-2026 — [RU_SANSKRIT_GRAM_ABBREV_TERMINOLOGY_CROSSWALK_2026-07.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RU_SANSKRIT_GRAM_ABBREV_TERMINOLOGY_CROSSWALK_2026-07.md), [PR #570](https://github.com/gasyoun/SanskritGrammar/pull/570), release [v0.116.1](https://github.com/gasyoun/SanskritGrammar/releases/tag/v0.116.1).
**Lane B (intended tier, this file):** Fable 5 (`claude-fable-5`), 04-08-2026 — independent re-run of the H2048 corpus inventory + the load-bearing non-case cells, then class-by-class compare per [/dual-run-salvage](https://github.com/gasyoun/claude-config/blob/main/commands/dual-run-salvage.md) discipline.

---

## Verdict up front

**CONFIRM with minor net-new.** Every load-bearing citation in the Grok crosswalk was independently re-opened and re-read on this pass; **all verified exactly** (line numbers included). **Zero conflicting cells** — no adjudication between lanes was needed anywhere. Fable's independently derived recommendation for the non-case verb system is the same as Grok's: **Latin-stay visible + Kochergina-style tooltip** (Latin full + Russian category name), because the Russian Indological tradition itself — textbook legend, dictionary article text, reader footnotes, and academic grammar alike — tags these categories in Latin. The canonical crosswalk stands; this pass patched it only with the net-new items below.

## What Fable independently re-verified (Phase A)

Method identical to H2048: legend / front-matter first, no prose-hunting; every non-empty cell requires path + line (or PDF page). Spot-check set: the handoff-mandated load-bearing families — caus / desid / intens / aor / fut / opt / prec / act-pass-med / partic-absol / number — across all 11 corpus paths + L + D.

| # | Source | Grok's claim | Fable re-check | Class |
|---|---|---|---|---|
| 1 | [`KocherginaUchebnik_1998/Kochergina_unicode.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/Kochergina_unicode.mdx) | «Условные сокращения» L168–227, Latin-short + Latin-full + RU triad; ~30 line cites (`caus.` L179, `des.` L184, `int.` L199, `aor.` L176, `fut.` L189, `opt.` L206, `imp.` L197, `impf.` L198, `pf.` L210, `pr.` L215, `P.` L207, `p.` L209, `Ā.` L177, `part.` L208, `pp.` L214, `inf.` L193, `ger.` L191, `sg.` L218, `pl.` L212, `du.` L185, cases…) | **All line cites verified byte-exact** on the fresh `origin/main` worktree. Legend spans L168–227 as claimed | Identical |
| 2 | [`KnauerFrazy_1908/Frazy-Knauer-03.05.2023.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/KnauerFrazy_1908/Frazy-Knauer-03.05.2023.mdx) | No dedicated list; inline footnote tags `impf.`, `caus.`, `opt.`, `pass.`, `med.`, `imper.`, `aor.`, `pp.`, `ger.`, `part.`, `sg.`, `pl.`, `loc. abs.`; `denom.?` tentative | Confirmed with counts: `pass.`×22, `impf.`×22, `pp.`×19, `opt.`×15, `med.`×11, `caus.`×7, `part.`×4, `loc. abs.`×3, `imper.`×3, `ger.`×3, `sg.`×1, `pl.`×1, `aor.`×1 — **and `denom.`×1 is real** (tentative `?` can be dropped). No `des.`/`fut.`/`prec.` anywhere | Identical + net-new (denom. upgraded) |
| 3 | `Elizarenkova_2004` | Local tree PDF-only (`Indoarian_27_01_04_Sanskrit-part.pdf`, 70 pp.); prose RU full terms, not a tag system | Confirmed: directory is **gitignored** (`.gitignore` L157), PDF-only, 70 pp. Text-layer census: *аорист*×29, *каузатив*×14, *оптатив*×10, *причаст-*×38, `вин. п.`×28, `род. п.`×17, `местн. п.`×16 — full-RU / school-RU prose metalanguage. Nuance: **`pl.` does occur ×5** (occasional Latin number tag in typological glosses); `sg.`/`Acc.`/`акк.` ×0 | Identical + minor net-new (pl. nuance) |
| 4 | [`BuhlerLeitfaden_1923/Buhler_Unicode.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/Buhler_Unicode.mdx) | Front matter = editor's preface only; Урок I names tenses Latin-full + RU: *indicativus (настоящее время)*, *imperfectum*, *imperativus*, *optativus (potentialis)*, *perfectum*, *аорист*, *parasmaipada*, *ātmanepada*; `prec.` row cite *precativus (benedictivus)* | Confirmed — the ten-form Урок I table (~L119–127) carries exactly those Latin full names, including **precativus (benedictivus)** and *conditionalis* + описательное/простое будущее; *Indicativus praesentis* at ~L147 | Identical |
| 5 | [`ApteSyntax_1885/Apte-unicode.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/Apte-unicode.mdx) | «Список условных сокращений» L88–163 is source-sigla only (A. R., Bg., Mb. …), not grammar categories | Confirmed at L88 ff. (A. R., Bg., Bh., Bk., B.R., C., Dk., G.M., H. — all literary sources) | Identical |
| 6 | [`GasunsDhatu_2014/02_gasuns-dhatu-PhD-text2.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/02_gasuns-dhatu-PhD-text2.mdx) | «Принятые сокращения» L3165–3227, mostly bibliographic; grammar hits `Abl.`, `Nom.`, `Ind.`, `praes.`, `sg.` | Confirmed byte-exact: `Abl.` L3169, `Ind.` L3180, `Nom.` L3196, `praes.` L3205, `sg.` L3214; the rest of the legend is sigla (EWA, KEWA, MW., PWG, PWK…) | Identical |
| 7 | `TolchelnikovTalmud_2026` | Own positional metalanguage (МП / Поз.), not PWG-style tags | Confirmed in substance: **0 hits** of `aor.`/`caus.`/`opt.`/`impf.` in [`talmud-09-glagolnaya-sistema.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/talmud-09-glagolnaya-sistema.mdx) — no Latin tag apparatus. (The literal «МП» siglum was not re-located this pass; immaterial to the cell, which is `—`) | Equivalent |
| 8 | `ZalizniakMorphology_1975` | English morphophonology paper only | Confirmed: tree holds only `A. Zalizniak Morphophonological Classification (English).mdx`/`.docx` | Identical |
| 9 | [`ZalizniakOcherk_1978/Zalizniak-Ocherk_29-11-20-aligned.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/Zalizniak-Ocherk_29-11-20-aligned.mdx) | §71 cases (`Nom.`/`N.` … `Voc.`/`V.`), m/f/n, sg/du/pl; §109 `indic.`/`imper.`/`opt.`, `impf.`/`aor.`/`perf.`, `act.`/`med.`/`pass.` + parasmaipada/ātmanepada; *прекатив*/*конъюнктив* prose-only | Confirmed byte-exact: §71 at L940–948 (cases with both long and short Latin), §109 at L1792–1816 — `indic.`/`imper.`/`opt.` L1800, `impf.`/`aor.`/`perf.` L1806, `act.`/`med.`/`pass.` L1812; *прекатив* L1800/1802 and ведийский *конъюнктив* note L1804 carry **no short tag**, exactly as the crosswalk's `prec.`/`Conj.` rows state | Identical |
| 10 | [`ZalizniakKonspekt_2004/zalizniak-konspekt-2015-11-X_bd_t.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakKonspekt_2004/zalizniak-konspekt-2015-11-X_bd_t.mdx) | Dense paradigms, inline `3 sg act` / `v/g`, no legend | Confirmed: 7 inline hits, no front list | Identical |
| 11 | `WhitneyGrammar_1889` | EN baseline, no RU tag system | Confirmed structurally — chapters are generated English prose from [WhitneyRoots](https://github.com/gasyoun/WhitneyRoots) | Identical |
| L | [LES-1990 abbreviations](https://samskrtam.ru/sanskrit-lexicon/les-1990/006b.html) | General-linguistics only; **no** aorist / causative / medium jurisdiction | Confirmed via the prior-art memo [ABBREV_LES1990_SRAVNENIE_2026-07.md](https://github.com/gasyoun/SanskritLexicography/blob/master/RussianTranslation/pwg_ru/ABBREV_LES1990_SRAVNENIE_2026-07.md) rows: *causativum → нет в ЛЭС*, *medium → нет в ЛЭС*, §5 «Глагольная система — за пределами юрисдикции ЛЭС» | Identical |
| D | [Kochergina 1987 dictionary text](https://samskrtam.ru/sanskrit-lexicon/small/kochergina_sm.html) | Visible tags **Latin**: `Acc.` … `Voc.`, `pr.`, `fut.`, `pf.`, `aor.`, `pp.`, `inf.`, `caus.`, `P.`/`A.` | Confirmed by live fetch 04-08-2026: Latin case tags, `pr.`/`fut.`/`pf.`/`aor.`/`pp.`/`inf.`/`ger.`/`caus.`/`den.`/`imp.`, pada `P.`/`A.`/**`U.`**, `m.`/`f.`/`n.`, `sg.`/`pl.` — e.g. «अध्यापय् /adhyāpay/ (caus. от अधी)». **Net-new: `U.` (Ubhayapada) and `den.`, `imp.` also live in the dictionary text**, strengthening the Latin-stay case | Identical + net-new (U.) |

## Class totals (dual-run-salvage scheme)

| Class | Count | Notes |
|---|---|---|
| **Identical** | 11 of 13 source columns; all recommendation cells | Same evidence, same recommendation |
| **Equivalent** | 1 (Talmud) | Same cell value (`—`), slightly different wording of why |
| **Conflicting** | **0** | No adjudication needed anywhere |
| **Net-new (Fable lane)** | 4 items, all minor | See below — folded into the canonical doc this pass |

## Net-new items (patched into the canonical crosswalk this pass)

1. **`U.` (Ubhayapada) row** — `U. - Ubhayapada - имеющий оба залога` in the Kochergina legend (K:L221) **and** attested in the Kochergina-1987 dictionary text alongside `P.`/`A.`. The voice/pada family was P./Ā.-only in the Grok table; PWG's `Ubhayapada`-class verbs need the third member. Added to table 3.
2. **Knauer `denom.` de-tentativized** — Grok wrote `denom.?`; the tag is attested ×1 in the Knauer footnotes. `?` dropped in table 3.
3. **Elizarenkova occasional `pl.`** (×5 in the PDF text layer) — does not change the cell's character (prose RU metalanguage), recorded as a nuance note only.
4. **Kochergina legend extras relevant to future rows** — `pfph.` (perfectum periphrasticum, K:L211), `pn.` (participium necessitatis, K:L213), `U.` (K:L221): all Latin-short, further evidence the textbook tag layer is Latin end-to-end. `pfph.`/`pn.` left as a backlog note (no PWG-frequency case made yet).

## What this does NOT change

- The MG case Latin-stay lock (31-07-2026) — untouched, not re-argued.
- The Grok non-case policy bands (Latin short for the Sanskrit verb system; LES forms tooltip-only; H1303 `фут.`/`прекат.`/`кауз.` remain unattested proposals) — **independently confirmed**, not merely accepted.
- H2047 HTML sheet — out of scope (non-goal).

## Provenance

| Field | Value |
|---|---|
| Handoff | [H2053](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2053-Fable_SanskritGrammar_h2048-grok-crosswalk-fable-compare_01.08.26.md) |
| Executor | Fable 5 (`claude-fable-5`), 04-08-2026 |
| Compared against | Grok 4.5 (`grok-4.5`) lane of 31-07-2026, [PR #570](https://github.com/gasyoun/SanskritGrammar/pull/570) |
| Worktree | `SanskritGrammar-h2053-1065252b` branch `h2053-fable-dual-run-compare` off `origin/main` @ `092fce3` |

_Dr. Mārcis Gasūns_
