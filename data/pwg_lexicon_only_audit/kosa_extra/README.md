# kosa_extra — koṣas sourced by H1326, not present in `csl-orig`

_Created: 19-07-2026 · Last updated: 19-07-2026_

Companion data folder for the [PWG lexicon-only audit](../README.md). Holds koṣa headword
data acquired to fill the audit's biggest documented gap (README "Coverage gap" /
[metadoc](../pwg_lexicon_only_audit.meta.md) backlog item #1) — read **only** by
[`build_census.py`](../build_census.py)'s `KOSA_EXTRA` group, never by `csl-orig` (this data
is not part of, and is not proposed for inclusion in, the Cologne dictionaries).

## Sourced — `amar.txt` (Amarakośa / AK)

- **File:** `namalinganushasana_amarasinha/slp/namalinganushasana.txt` from
  [`sanskrit-kosha/kosha`](https://github.com/sanskrit-kosha/kosha) (commit current as of
  19-07-2026), copied verbatim (unmodified) as `amar.txt`.
- **Format:** the exact `<eid>N<syns>lemma-GEN,lemma-GEN,...` format `build_census.py`'s
  `load_syns()` already parses — the same annotation format used for `abch`/`acph`/`acsj`/`nmmb`,
  which are digitisations from this *same* upstream repo already present in `csl-orig`. No new
  parser was needed.
- **Licence:** the file's own `;METADATA` block states `;licence{GNU GPL v3.0}` explicitly
  (line ~23) — an open, redistributable licence. `;credits{}` names Prof. Amba Kulkarni /
  sanskrit.uohyd.ac.in/scl/ (original OCR/data) and Dr. Shivja S. Nair (PhD annotation) as
  the underlying data providers, with Dr. Dhaval Patel's `sanskrit-kosha/kosha` project
  producing the `<syns>` synset tagging. **Verdict: clean to ingest** — headword-only use,
  same licence class and same source project as the four koṣas already in `csl-orig`.
- **Yield:** 5,666 `<eid>` synsets → **9,788 distinct SLP1 headwords** (`load_syns_file`
  output, `norm()`-insensitive count would be slightly lower).
- **Resolves:** the `amara_gap` flagged in the v2 README/metadoc (Amara absent from the
  comparison side) — Amara (`AK`, PWG's own citation token) is now `PWG_TOKEN_TO_DICT`-mapped
  and joined like the other koṣas.

## NOT sourced — Rājanighaṇṭu (RĀJAN), Trikāṇḍaśeṣa (TRIK), generic Nighaṇṭu (NIGH)

Exhausted, in priority order, per the H1326 handoff's own pointers — **none yielded a bulk
lemma-tagged headword set**:

1. **`csl-orig/v02`** — re-confirmed absent under any code (`ls csl-orig/v02`, 19-07-2026).
2. **`sanskrit-kosha/kosha`** — has raw digitisations of both `trikandashesha_purushottamadeva`
   (109,526 bytes, SLP1) and `nighantushesha_hemachandra` (Hemacandra's Nighaṇṭuśeṣa, 43,133
   bytes), plus `haravali_purushottamadeva` (Hārāvalī, best-effort target, 30,288 bytes) and
   `nanarthashabdakosha_medinikara` (Medinīkośa, PWG's `MED` token, 244,675 bytes). **All four
   are raw, unsegmented, sandhi-joined metrical verse** (`;p{}`/`;v{}`/`;c{}` page/section
   markers around continuous verse text) — **zero** `<syns>` or `<k1>` tags. A repo-wide scan
   of all 126 reachable `dictcode.json` entries in `sanskrit-kosha/kosha` (script:
   `scan_syns.py`, run 19-07-2026) found **only 4 works have ever received `<syns>` synset
   annotation** — `abch`/`acph`/`acsj` (already in `csl-orig`) and `amar` (now added above).
   Extracting individual headwords from the raw verse would require a real Sanskrit sandhi
   splitter/segmenter (the project's own `kosha_annotator.py` + `annotation_accuracy_log.txt`
   confirm this annotation is done **by hand**, not mechanically) — building/running that
   pipeline for one dictionary is out of scope for a corpus-fill pass and was judged too
   quality-risky to fake with a regex heuristic.
3. **`cltk/sanskrit_text_dcs`** (a GitHub mirror of Digital Corpus of Sanskrit raw texts) —
   has a `Rājanighaṇṭu.txt`, but it is a **232-byte fragment** (just the opening invocation
   verses), not the full text. Related nighaṇṭus present in fuller form (`Dhanvantarinighaṇṭu.txt`
   34,557 B, `Madanapālanighaṇṭu.txt` 47,235 B, `Kaiyadevanighaṇṭu.txt` 20,646 B,
   `Aṣṭāṅganighaṇṭu.txt` 56,724 B, `Bījanighaṇṭu.txt` 9,058 B, `Nighaṇṭuśeṣa.txt` 27,446 B) are
   likewise **raw sandhi-joined IAST verse**, no per-word segmentation or lemma tags — same
   blocker as (2).
4. **Web search** for a bulk Rājanighaṇṭu/Trikāṇḍaśeṣa word index, CSV, or ethnobotanical
   synonym table turned up nothing beyond prose descriptions of the texts (WisdomLib,
   easyayurveda, generic plant-name databases with no Sanskrit-specific source).
5. **Hyderabad Amarakośa** (per-word query only, no bulk export, per
   [`Uprava/SERVER_OUTAGES.md`](https://github.com/gasyoun/Uprava/blob/main/SERVER_OUTAGES.md))
   — moot for Amara itself since (1) above supplied it, but the same per-word-only constraint
   would apply if that resource were tried for RĀJAN/TRIK/NIGH (it isn't hosted there anyway).

**Verdict: hard blocker, not a licence issue** — the data does not yet exist in
lemma-segmented form anywhere checked. Digitising these three properly needs either (a) the
`sanskrit-kosha/kosha` project's own manual annotation pipeline to reach them, or (b) a real
Sanskrit word segmenter (e.g. the Sanskrit Heritage tools) run and hand-verified against the
raw verse — both larger undertakings than this handoff's scope. Left as an open backlog item
(metadoc backlog #1, revised).

## Reproduce

```sh
curl -sL -o amar.txt "https://raw.githubusercontent.com/sanskrit-kosha/kosha/master/namalinganushasana_amarasinha/slp/namalinganushasana.txt"
```

_Dr. Mārcis Gasūns_
