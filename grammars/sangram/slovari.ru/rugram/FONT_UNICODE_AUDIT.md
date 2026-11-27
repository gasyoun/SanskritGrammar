# Fonts vs Unicode — audit (27-11-2026)

**Question:** the source warns that fonts must be installed "для правильного
отображения алфавитов". Can Unicode conversion remove the need for the fonts?

**Answer:** for *content correctness*, yes — and it is already done. The two
TTFs are ordinary Unicode fonts, not symbol-encoded fonts; no harvested
character depends on them being installed. They are shipped as WOFF2 for
*typographic fidelity* only.

## Font evidence (fontTools 4.68)

| Font | Family | cmap | Cyrillic | PUA |
|---|---|---:|---:|---|
| `Gramn.ttf` | Grammatica Normal | 1,120 | 98 | 4 (U+F001 fi, U+F002 fl, U+F004/U+F005 comma accents) |
| `TIMENRC4.TTF` | Times New Roman CyrAC Italic | 223 | 94 | 0 |

Both have proper Unicode `cmap` tables. The old site's instruction was about
rendering the phonetic alphabets with the publisher's glyph shapes, not about
a non-Unicode encoding. None of the 4 PUA code points occurs in the harvest.

## Artefacts found and fixed

| Artefact | Where | Count | Fix |
|---|---|---:|---|
| `U+0096` (cp1252 en dash decoded as C1) | `derived/text/` | **34,434** | → `U+2013` EN DASH |
| `U+0007` BEL (phoneme-table separator) | `derived/doc/` | **693** | → `U+2013`; the same table in the HTML harvest uses an en dash between `\|з\|` and `\|з’\|` |
| `U+FFFD` truncated final letter | `derived/doc/` | **9** | → СССР / АББРЕВИАТУРЫ / АББРЕВИАТУР / ОБЗОР / ПАР, confirmed against the HTML harvest |

`normalize_unicode.py` applied these and recomputed every page's `chars` and
SHA-256 in `manifest.json`, adding a `unicode_normalization` provenance block.

**Deliberately not converted:** 5 ambiguous C1 characters (`U+0082`, `U+008F`
×2, `U+009A`, `U+009F`) are rare diacritic/quote-like glyphs in bibliographies.
There is no evidence for a specific mapping, so they are documented, not
guessed. They are not part of the main grammar text.

## Web font delivery

- `make_webfonts.py` converts both TTFs to WOFF2 (`html/fonts/Gramn.woff2`
  66 KB, `html/fonts/TIMENRC4.woff2` 27 KB).
- `build_html.py` emits `@font-face` with correct relative paths from both
  `html/index.html` and `html/pNNN/*.html`.
- The 21 converted DOC pages use **Grammatica** (plain vowels, verified by
  rendering `а о е и аас` in both fonts). Chapter pages use Georgia.
- **TIMENRC4 / Times New Roman CyrAC is deliberately NOT applied.** Its vowel
  glyphs carry a built-in acute: rendered samples show `а о е и` as `á ó é í`.
  Applying it as a body font puts a stress mark on every vowel — exactly the
  defect reported against the web edition. The original DOC used that font in
  separate runs for *intentionally* stressed vowels; `antiword` output loses
  that run information, and the text has only 1 `U+0301` across all pages. A
  global font swap cannot reconstruct the distinction, so the font ships in
  `html/fonts/` but has no `@font-face` rule.
- Verified over HTTP before that correction: `document.fonts.status` =
  `loaded` for both fonts on their respective pages, zero console errors.
  After the correction: 9,480 relative links checked, 0 broken.
- **Caveat:** Chromium blocks `@font-face` loads from `file://` (CORS). Opening
  the HTML directly from disk falls back to Georgia — Cyrillic still renders
  correctly because the text is Unicode. Serve over HTTP to see Grammatica.

## Font-encoded phonetic glyphs at CJK code points

This is the one place where plain Unicode conversion was **not** enough.
The corpus contains 4,236 characters in the U+3000–30FF range that are not
CJK punctuation at all: Grammatica maps its long-consonant glyphs there.
Rendering the TTF and checking the surrounding text identified four of them:

| Source | Rendered glyph | Meaning | Unicode replacement |
|---|---|---|---|
| `U+3019` `〙` | Ш̄ | long ш (soft with `'` → `[ɕː]`) | `ш` + `U+0304` |
| `U+3007` `〇` | Ж̄ | long ж | `ж` + `U+0304` |
| `U+300E` `『` | Н̄ | long н (soft → `весе[н̄']ий`) | `н` + `U+0304` |
| `U+3017` `〗` | Ц̄ | long ц (`о[ц̄]а`) | `ц` + `U+0304` |

Applied by `normalize_phonetic_glyphs.py` (1,706 / 462 / 27 / 12 occurrences).

By request, **all 71 code points are now mapped** by `map_all_font_glyphs.py`
(4,778 further occurrences). The method is shape-faithful transcription from
the actual TTF glyphs: letters with macron/acute/diaeresis become letter +
combining mark; Greek letters become Greek; tone bars, arcs and slashes become
spacing marks; superscript digits become digit + superscript. Every entry is
recorded in `manifest.json → font_glyph_map` with a confidence label: `high`
for unambiguous letters/digits, `medium` for tone marks and Greek letters in
bibliographies whose scholarly reading is context-dependent. **Zero CJK-range
characters remain** in `derived/text`. Medium-confidence entries are flagged
for human review rather than presented as settled phonetics.

Stress itself is recoverable separately: the source wraps each stressed vowel
in `<span style="font-family: Times New Roman CyrAC">а</span>`; `recover_stress.py`
appends `U+0301` to those vowels only, producing a parallel `derived/stress/`
layer used by the HTML edition.

## Verdict

Unicode solves the *encoding* problem, but font-mapped glyphs need an explicit,
evidence-backed mapping — done above. Keep the WOFF2 files for typographic
fidelity only; the 5 ambiguous C1 code points stay as-is until a printed
witness settles them.
