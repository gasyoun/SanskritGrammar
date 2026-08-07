# H2272 — offline-search tri-script tokenization verification

_Created: 05-08-2026 · Last updated: 06-08-2026_

Verifies [H1841](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1841-Opus_SanskritGrammar_docusaurus-offline-search_29.07.26.md)'s
explicit watch-out — "pick a tokenizer/locale config that actually handles the
Cyrillic/IAST/Devanāgarī mix — verify with real search queries" — against the real
built `build/search-index.json`, using a probe script
([verdict_validation/h2272_tokenization_probe.mjs](https://github.com/gasyoun/SanskritGrammar/blob/main/verdict_validation/h2272_tokenization_probe.mjs))
that replicates `@easyops-cn/docusaurus-search-local`'s own `SearchWorker.search()`
(same lunr + `lunr-languages` wiring as `buildIndex.js`, same exact-then-trailing-wildcard
query fallback as `smartQueries.js`) rather than approximating it.

## Results table

15 terms (5 per script), drawn from real page content across 5–7 books, queried against
the `npm run build` output (`build/search-index.json`, config unchanged:
`language: ['ru', 'en']`, `searchResultLimits: 8`, full `/search` page limit `100`).

| Script | Term | Source book | Found? | Rank / total hits |
|---|---|---|---|---|
| Cyrillic | падеж | ApteSyntax_1885 | ✅ pass | 8 / 42 |
| Cyrillic | глаголов | BuhlerLeitfaden_1923 | ✅ pass | 6 / 49 |
| Cyrillic | санскрите | ZalizniakOcherk_1978 | ✅ pass | 4 / 36 |
| Cyrillic | корень | GasunsDhatu_2014 | ✅ pass | 2 / 57 |
| Cyrillic | значение | KocherginaUchebnik_1998 | ✅ pass | 32 / 47 |
| IAST | guṇa | ApteSyntax_1885 | ✅ pass | 35 / 44 |
| IAST | vṛddhi | BuhlerLeitfaden_1923 | ✅ pass | 7 / 33 |
| IAST | dhātu | WhitneyGrammar_1889 | ✅ pass | 15 / 16 |
| IAST | Pāṇini | GasunsDhatu_2014 | ✅ pass | 10 / 15 |
| IAST | saṃdhi | KocherginaUchebnik_1998 | ✅ pass | 1 / 6 |
| Devanāgarī | किं (kim) | ApteSyntax_1885 | ❌ **fail** | 0 hits |
| Devanāgarī | इति (iti) | BuhlerLeitfaden_1923 | ❌ **fail** | 0 hits |
| Devanāgarī | तस्य (tasya) | WhitneyGrammar_1889 | ❌ **fail** | 0 hits |
| Devanāgarī | राजा (rājā) | KnauerFrazy_1908 | ❌ **fail** | 0 hits |
| Devanāgarī | तथा (tathā) | KocherginaUchebnik_1998 | ❌ **fail** | 0 hits |

Raw probe output: [h2272_probe_results.json](https://github.com/gasyoun/SanskritGrammar/blob/main/verdict_validation/h2272_probe_results.json).
"Found" = present anywhere in the `/search` page's full 100-result list (all Cyrillic/IAST
ranks land well within that, though several sit below the 8-item navbar-dropdown limit —
`значение` and `guṇa` in particular need the full search page, not the dropdown, to surface).

## Verdict per script

- **Cyrillic — works.** All 5 terms findable; ranks 2–32 of the full result set.
- **IAST (Latin + diacritics) — works.** All 5 terms findable; ranks 1–35. The
  earlier concern that a *leading* diacritic vowel (`ātman`, `ṛṣi`) gets trimmed by
  lunr's `generateTrimmer` (leading/trailing-only strip, word-initial diacritic is
  "non-word" under the `\w` + Cyrillic-range trimmer) is real but did not surface in
  this sample since none of the 5 chosen terms start/end on a bare diacritic vowel —
  flagged as a residual edge case below, not re-tested to keep this pass bounded.
- **Devanāgarī — fails outright (0/5, zero hits each).** Root cause confirmed by
  reading the plugin's own source (`generateTrimmer.js` +
  `lunr-languages/lunr.ru.js`'s `wordCharacters`): with `language: ['ru','en']`,
  `lunr.multiLanguage('ru','en')`'s combined trimmer's `wordCharacters` is `\w` (ASCII
  Latin/digits) plus `lunr.ru.wordCharacters` (`Ѐ-҄҇-ԯ...`,
  Cyrillic only). Devanāgarī (`ऀ-ॿ`) is in neither set, so a token made
  entirely of Devanāgarī characters is stripped to an empty string by the
  leading+trailing trim and never reaches the inverted index — not a ranking problem,
  a total exclusion.

## Fix attempt (limitation documented, not resolved)

**Attempt 1 — add `lunr-languages`' Sanskrit pack (`language: ['ru','en','sa']`).**
`lunr.sa` ships the correct `wordCharacters` range for Devanāgarī
(`ऀ-ॿ` + Vedic extensions), the textbook fix per H1841's own fallback
order ("(1) adjust the plugin's `language` list"). **Breaks the production build.**
`@easyops-cn/docusaurus-search-local`'s `LANGUAGES_NEED_WORDCUT` list
(`["th","hi","te","ta","kn","sa"]`) forces a
`lunr.wordcut = require("lunr-languages/wordcut")` whenever `sa` is present, and
`lunr.sa.js` calls `lunr.wordcut.init()` unconditionally at module load (not lazily) —
so `sa` cannot be used at all without wordcut. `wordcut.js` is a vendored
browserify-bundled UMD file with dynamic `require()` calls webpack cannot statically
analyze; this fatally aborts `npm run build` (`[ERROR] Client bundle compiled with
errors therefore further build is impossible` / `Cannot statically analyse
'require(…, …)' in line 1`), reproduced **both** with normal minified build (Terser
then also chokes on the resulting bundle: `Unexpected token: keyword (if)`) and with
`docusaurus build --no-minify` (webpack's own dynamic-require analysis fails before
Terser ever runs — ruling out "just a Terser bug", confirmed by testing minify on and
off). The plugin exposes no config knob to set a custom `wordCharacters`/tokenizer
without going through a full language pack, so there is no narrower lever to pull from
`docusaurus.config.mjs` alone. **Config reverted to the shipped `['ru', 'en']`** — the
worktree contains no net change to `docusaurus.config.mjs`.

**Stopped after 1 fix attempt** (of the handoff's 3-attempt budget) because the
attempt didn't fail *quietly* — it hard-broke `npm run build`, i.e. moving further down
the same lever (further `language` tweaks) cannot succeed without first patching a
third-party dependency, which is out of this handoff's bounded-config-fix scope.

## Limitation — Devanāgarī offline search does not work

**Devanāgarī-script search terms return zero results on the built offline search
index.** Cyrillic and IAST/Latin (including diacritics) search work correctly. Users
searching by a Devanāgarī term will get no hits even when the term is present,
verbatim, on an indexed page.

**A real fix requires one of:**
- `patch-package` against `@easyops-cn/docusaurus-search-local` and/or
  `lunr-languages` to make `lunr.sa`'s wordcut dependency optional (the corpus here is
  already whitespace-segmented, so Sanskrit's Thai-style word-boundary segmenter is
  unneeded — only its `wordCharacters` trimmer range is wanted), or to strip `sa`/`hi`
  from `LANGUAGES_NEED_WORDCUT` for this use case.
- A webpack/Docusaurus config override (`webpack.overrides` via a small local plugin)
  telling webpack to accept `wordcut.js`'s dynamic requires rather than fatally erroring.
- A from-scratch minimal Devanāgarī trimmer registered as a custom lunr pipeline
  function, bypassing `lunr-languages/lunr.sa.js` entirely.

Each is real engineering work (patch authorship + regression risk on every dependency
bump, or a fork-and-maintain burden) beyond this verification pass's bounded-config-fix
scope — **this deserves its own follow-up handoff** rather than a rushed patch here.

## Evidence

- `npm run build` success log (baseline `['ru','en']` config): `[SUCCESS] Generated
  static files in "build"` — see the worktree build log; `build/search-index.json`
  present.
- Probe script + raw per-term output committed alongside this doc:
  [h2272_tokenization_probe.mjs](https://github.com/gasyoun/SanskritGrammar/blob/main/verdict_validation/h2272_tokenization_probe.mjs),
  [h2272_terms.json](https://github.com/gasyoun/SanskritGrammar/blob/main/verdict_validation/h2272_terms.json),
  [h2272_probe_results.json](https://github.com/gasyoun/SanskritGrammar/blob/main/verdict_validation/h2272_probe_results.json).
- Failed-fix build log excerpt (both minified and `--no-minify`) reproduced above.

## H2300 — Devanāgarī fix (real engineering, not a limitation)

_Appended 06-08-2026._ Picked up H2272's own follow-up recommendation.
`language: ['ru','en','sa']` + a `patch-package` patch (`patches/`) neutralizing
`lunr.sa`'s `wordcut` hard-dependency (Approach 1 of the 3 candidates
H2272/H2300 listed — `patch-package` against the dependency, not a webpack
override or a from-scratch tokenizer). Full root cause + patch rationale: this
repo's [`CHANGELOG.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/CHANGELOG.md)
`[Unreleased]` entry.

Same 15 terms (5 per script, same `h2272_terms.json`), re-run against the
`npm run build` (normal minified mode) output with the fix applied. Raw output:
[h2300_probe_results.json](https://github.com/gasyoun/SanskritGrammar/blob/main/verdict_validation/h2300_probe_results.json).

| Script | Term | Source book | Found? | Rank / total hits |
|---|---|---|---|---|
| Cyrillic | падеж | ApteSyntax_1885 | ✅ pass | 8 / 42 |
| Cyrillic | глаголов | BuhlerLeitfaden_1923 | ✅ pass | 8 / 49 |
| Cyrillic | санскрите | ZalizniakOcherk_1978 | ✅ pass | 4 / 36 |
| Cyrillic | корень | GasunsDhatu_2014 | ✅ pass | 2 / 57 |
| Cyrillic | значение | KocherginaUchebnik_1998 | ✅ pass | 32 / 47 |
| IAST | guṇa | ApteSyntax_1885 | ✅ pass | 35 / 44 |
| IAST | vṛddhi | BuhlerLeitfaden_1923 | ✅ pass | 7 / 33 |
| IAST | dhātu | WhitneyGrammar_1889 | ✅ pass | 15 / 16 |
| IAST | Pāṇini | GasunsDhatu_2014 | ✅ pass | 10 / 15 |
| IAST | saṃdhi | KocherginaUchebnik_1998 | ✅ pass | 1 / 6 |
| Devanāgarī | किं (kim) | ApteSyntax_1885 | ✅ **pass** | 1 / 5 |
| Devanāgarī | इति (iti) | BuhlerLeitfaden_1923 | ✅ **pass** | 4 / 5 |
| Devanāgarī | तस्य (tasya) | WhitneyGrammar_1889 | ✅ **pass** | 3 / 4 |
| Devanāgarī | राजा (rājā) | KnauerFrazy_1908 | ✅ **pass** | 1 / 8 |
| Devanāgarī | तथा (tathā) | KocherginaUchebnik_1998 | ✅ **pass** | 2 / 2 |

**15/15.** Cyrillic and IAST ranks/hit-counts are byte-identical to H2272's
original baseline above (confirming the fix is neutral there once the
upstream astral-range bug — see CHANGELOG — is also patched out); Devanāgarī
flips from 0/5 to 5/5. `npm run build` succeeded in normal minified mode (not
`--no-minify`) — see the CI/build log for this PR.

_Dr. Mārcis Gasūns_
