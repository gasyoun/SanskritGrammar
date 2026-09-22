# Report — Shiva Sutras vendored as pratyāhāra reference table (H4716)

_Created: 15-09-2026 · Handoff: H4716 (OxAlpha, glm-5.3-flash) · Repo: SanskritGrammar_

## Mission

Census A11 (xwalk batch). Consume kosha `shiva-sutras-machine` (built H4471, 09-09-2026,
status `awaiting-consumer`) as the pratyāhāra reference table for the sangram morphology
programme + VisualDCS-style lookup notes. Output: vendored reference + report; verify all
14 sūtras round-trip pratyāhāra expansion; register the cross-repo edge.

## Changed

- [data/shiva_sutras/](https://github.com/gasyoun/SanskritGrammar/blob/main/data/shiva_sutras/) —
  byte-identical vendor snapshot (`cmp`-verified) of kosha `data/shiva_sutras/` @ commit
  `11a243eb`: `sutras.tsv` (14 rows), `pratyaharas.tsv` (42 rows), `shiva_sutras.json`
  (43 phonemes + 14 anubandhas = 57-token master sequence), plus
  [PROVENANCE.md](https://github.com/gasyoun/SanskritGrammar/blob/main/data/shiva_sutras/PROVENANCE.md)
  (upstream-of-truth = kosha; license MIT).
- [scripts/verify_shiva_pratyahara.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/verify_shiva_pratyahara.py) —
  deterministic offline verifier, exit 0/1.
- Edge registered in Uprava `interlinks_edges.tsv` + `PROJECT_INTERLINKS.md`
  (SanskritGrammar `vendors` kosha `shiva-sutras-machine`); kosha `datasets.json` consumer
  flip (`awaiting-consumer` → consumer recorded).

## Unchanged

Nothing else in this repo; no product/code behavior touched. The kosha dataset itself is
unchanged (this handoff consumes it, H4471 remains its builder handoff).

## Checks

```
python3 scripts/verify_shiva_pratyahara.py
# shiva_sutras: 14 sutras, 42 pratyaharas, master=71 code points (57 tokens)
# PASS: C1 sūtras well-formed · C2 14-sūtra master round-trip (43+14=57 tokens) ·
#       C3 42/42 pratyāhāra round-trip · C4 all 14 it-markers consumed · C5 classic canaries
# exit=0
```

Five check families, all PASS:

1. **C1 sūtra form** — 14 rows numbered 1..14; each `devanagari` ends with its it-marker.
2. **C2 master round-trip (the "all 14 sūtras round-trip" gate)** — concatenating the 14
   sūtra strings (TSV and JSON independently) reproduces the 71-code-point master sequence
   (43 phonemes + 14 anubandha tokens = 57 tokens); marker-stripped master == concatenated
   `letters_only`.
3. **C3 pratyāhāra round-trip 42/42** — every named span is contiguous in the master
   sequence, terminates at its it-marker, and marker-stripping reproduces `letters_only`;
   `length` column equals the span's token census (anubandha = 1 token).
4. **C4 it-marker coverage** — all 14 it-markers (ण् क् ङ् च् ट् ण् म् ञ् ष् श् व् य् र् ल्;
   ण् legitimately twice — hence `aN1`/`aN2` in the table) are consumed by ≥1 named
   pratyāhāra, so every sūtra participates in the pratyāhāra system.
5. **C5 classic canaries** — aC = exactly the 9 vowels; haL = 34 consonants, vowel-free;
   iK = इ उ ऋ ऌ; eC = ए ओ ऐ औ; aC ⊎ haL = the 43-phoneme multiset.

The first verifier draft failed loudly (71 code points vs my assumed 57-character master;
naive last-occurrence marker search broke on the double ण्) — that was verifier-assumption
error, not data corruption; the fixed assertions above all hold against the vendored data.

## Consumer notes (sangram morphology + VisualDCS lookup)

- sangram morphology: use `pratyaharas.tsv.letters_only` as the class-membership oracle
  (aC/iK/uK/eC/aiC vowel classes; haL/jhaL/… consonant classes) for rule tables that
  Pāṇinian metalanguage states over pratyāhāras.
- VisualDCS-style lookup notes: `devanagari_span` gives the display span
  (first letter through terminal marker); `length` is the token census; when expanding,
  always strip ALL anubandhas inside the span, not just the terminal one.
- Ambiguity rule inherited from the table: ण् (sū.1) vs ण् (sū.6) — the table encodes both
  readings explicitly (`aN1` = अ इ उ; `aN2` = full अ..ल span); consumers must not
  re-derive one from the other.

## Risks

- Vendor drift: if kosha's table changes, this snapshot goes stale — re-vendor + re-run the
  verifier (re-verify command in PROVENANCE.md). Single-file risk, detected by the verifier.
- The `aN1`/`aN2` naming is kosha's (H4471) disambiguation of the double ण्, not a
  Pāṇinian standard name; consumers elsewhere on the estate must be told (this report is
  that notice).

## Inspect

1. `scripts/verify_shiva_pratyahara.py` — the five check families above.
2. `data/shiva_sutras/pratyaharas.tsv` — 42 named spans (the actual reference payload).
3. `data/shiva_sutras/PROVENANCE.md` — upstream-of-truth + license + re-vendor loop.

_Гасунс_
