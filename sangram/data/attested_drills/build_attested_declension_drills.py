#!/usr/bin/env python3
"""Sangram W2-add-a — attested-cell declension drill generator (H1296).

Every drill surface shipped so far (kosha's W1a morphology drills, H946 included)
drills the *paradigm engine's* forms: all 24 case x number cells, generated. The G2
coverage asset (sangram/data/declension_cell_coverage/) measured that only **10.44 %**
of the noun lemma x 24-cell space is ever corpus-attested. This builder exploits that
finding: it emits drill items for **attested cells only**, ordered by kosha lemma
frequency and grouped by Zaliznyak stem class -- "what you will actually meet".

Three-way join (all deterministic, no model in the loop):

  lemma_cell_coverage.csv      which of the 24 cells each lemma attests (bitstring)
  x kosha lemma_frequency.tsv  core_rank / count_all -> ordering + frequency band
  x headword_index.tsv         Zaliznyak stem_class (a-stem, i-stem, consonant-stem...)

plus two per-cell enrichments:

  DCS SQLite   per-cell token count + the attested *unsandhied* surface forms
  vidyut       the generated expected form for that cell

**Hard rule (kosha R1/R2 risk discipline, restated in H1296):** where the generated
form and the attested forms disagree, the row carries an ``agreement`` flag and BOTH
sides -- never a silent pick. Vedic/classical doublets are real signal, not noise:
``deva`` Ins.Plur attests both ``devaiḥ`` and ``devebhiḥ`` while vidyut generates only
``devaiḥ``; ``agni`` Loc.Sing attests ``agnau`` and Vedic ``agnā``. A drill that
silently asserted one of those as "the" answer would be teaching a falsehood.

Stdlib-only for the join itself (csv/sqlite3/json/argparse). The two enrichment stages
import third-party packages lazily and degrade honestly:
  * ``indic_transliteration`` (IAST->SLP1 join key) -- required; the join cannot be
    keyed without it, so its absence is a hard error, not a silent partial run.
  * ``vidyut`` (expected forms) -- optional; ``--no-generate`` or an absent package
    yields ``agreement=no_generation`` rows rather than a crash.

Read-only on every input. Regenerate:

    python sangram/data/attested_drills/build_attested_declension_drills.py

Outputs (all under this directory):
    attested_drill_items.tsv        the drill corpus (one row per lemma x attested cell)
    coverage_by_stem_class.json     per-class "N attested cells of 24" instrumentation
    COVERAGE_REPORT.md              the human-readable per-class report
    ../../../src/components/talmud/attestedDrillData.js   widget subset (top lemmas)

Corpus numbers are DCS (Hellwig) via the pinned VisualDCS snapshot; attribute
accordingly wherever they surface.
"""
import argparse
import csv
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[3]
GITHUB = ROOT.parent
OUT_DIR = ROOT / "sangram" / "data" / "attested_drills"

DEFAULT_COVERAGE = ROOT / "sangram" / "data" / "declension_cell_coverage" / "lemma_cell_coverage.csv"
DEFAULT_FREQ = GITHUB / "kosha" / "data" / "frequency" / "lemma_frequency.tsv"
DEFAULT_ZALIZNYAK = GITHUB / "SanskritLexicography" / "RussianTranslation" / "src" / "headword_index.tsv"
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
DEFAULT_WIDGET_DATA = ROOT / "src" / "components" / "talmud" / "attestedDrillData.js"

CASES = ["Nom", "Acc", "Ins", "Dat", "Abl", "Gen", "Loc", "Voc"]
NUMBERS = ["Sing", "Dual", "Plur"]
# Row-major case x number -- MUST match cells_order in coverage_summary.json.
CELLS = [f"{c}.{n}" for c in CASES for n in NUMBERS]
N_CELLS = len(CELLS)

# DCS dominant-gender tag -> vidyut linga name.
GENDER_TO_LINGA = {"Masc": "Pum", "Neut": "Napumsaka", "Fem": "Stri"}

# Frequency bands over kosha count_all, matching the G2 coverage README's banding
# so the two assets' "band" columns mean the same thing.
BANDS = [(1000, "1000+"), (100, "100-999"), (10, "10-99"), (2, "2-9"), (0, "hapax")]

# The widget ships a *stratified* subset: up to this many lemmas per stem class.
# A flat "top 200 by frequency" is 151 a-stems against 2 ī-stems -- the class filter
# would offer two lemmas for ī-stem, which is not a paradigm to practise. Per-class
# quotas also bound the bundle.
WIDGET_LEMMAS_PER_CLASS = 30
# A lemma is only worth drilling if it attests enough cells to be a paradigm rather
# than a single stray token: `vac` tops the core_rank list with ONE attested cell
# (Gen.Sing, n=2), which teaches nothing about declension.
WIDGET_MIN_DRILLABLE_CELLS = 4
# Stem classes the TRAINER refuses to offer, though the TSV keeps them. 52 lemmas are
# tagged `indeclinable` by the Zaliznyak index yet carry case-marked DCS tokens. That
# contradiction is real evidence and belongs in the analytic artifact -- but presenting
# it as a declension exercise would teach that indeclinables decline. The TSV records
# the disagreement; the drill declines to dramatise it.
WIDGET_EXCLUDED_STEM_CLASSES = {"indeclinable"}


def band_for(count):
    for floor, label in BANDS:
        if count >= floor:
            return label
    return "hapax"


def load_transliterator():
    """IAST -> SLP1. Hard requirement: it is the join key between the three inputs."""
    try:
        from indic_transliteration import sanscript
    except ImportError:  # pragma: no cover - environment guard
        sys.exit(
            "FATAL: indic_transliteration is required (IAST->SLP1 is the join key "
            "between lemma_cell_coverage.csv, lemma_frequency.tsv and headword_index.tsv).\n"
            "  pip install indic_transliteration"
        )

    def iast_to_slp1(text):
        return sanscript.transliterate(text, sanscript.IAST, sanscript.SLP1)

    return iast_to_slp1


def load_detransliterator():
    """SLP1 -> IAST, for display surfaces that must not mix scripts."""
    from indic_transliteration import sanscript

    def slp1_to_iast(text):
        return sanscript.transliterate(text, sanscript.SLP1, sanscript.IAST)

    return slp1_to_iast


def load_generator():
    """Return generate(slp1_stem, gender, cell) -> list[str] in SLP1, or None."""
    try:
        from vidyut.prakriya import Linga, Pada, Pratipadika, Vacana, Vibhakti, Vyakarana
    except ImportError:
        return None

    vib_by_case = {
        "Nom": Vibhakti.Prathama,
        "Acc": Vibhakti.Dvitiya,
        "Ins": Vibhakti.Trtiya,
        "Dat": Vibhakti.Caturthi,
        "Abl": Vibhakti.Panchami,
        "Gen": Vibhakti.Sasthi,
        "Loc": Vibhakti.Saptami,
        "Voc": Vibhakti.Sambodhana,
    }
    vac_by_number = {"Sing": Vacana.Eka, "Dual": Vacana.Dvi, "Plur": Vacana.Bahu}
    linga_by_name = {"Pum": Linga.Pum, "Napumsaka": Linga.Napumsaka, "Stri": Linga.Stri}

    v = Vyakarana()
    stem_cache = {}

    def generate(stem_slp1, gender, cell):
        linga_name = GENDER_TO_LINGA.get(gender)
        if linga_name is None:
            return []
        case, number = cell.split(".")
        key = (stem_slp1, linga_name)
        pratipadika = stem_cache.get(key)
        if pratipadika is None:
            try:
                pratipadika = Pratipadika.basic(stem_slp1)
            except Exception:
                return []
            stem_cache[key] = pratipadika
        try:
            results = v.derive(
                Pada.Subanta(
                    pratipadika=pratipadika,
                    linga=linga_by_name[linga_name],
                    vibhakti=vib_by_case[case],
                    vacana=vac_by_number[number],
                )
            )
        except Exception:
            return []
        return sorted({p.text for p in results})

    return generate


def read_coverage(path):
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def read_frequency(path):
    """lemma_slp1 -> row. First occurrence wins (the file is rank-sorted)."""
    out = {}
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            out.setdefault(row["lemma_slp1"], row)
    return out


def read_stem_classes(path):
    """SLP1 headword -> stem_class. First non-empty class per headword wins."""
    out = {}
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            cls = (row.get("stem_class") or "").strip()
            if cls and row["k1"] not in out:
                out[row["k1"]] = cls
    return out


def read_attested_forms(db_path, lemma_ids):
    """(lemma_id, cell) -> [(unsandhied_form, count), ...] desc, plus per-cell totals.

    Compares against ``m_unsandhied``, never the raw ``form`` column: DCS surface
    tokens are sandhi-affected (deva Nom.Sing surfaces as devo / devaḥ / devas /
    devaś), so a raw-form comparison would flag phonology as a paradigm disagreement.
    """
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        conn.execute("CREATE TEMP TABLE want(lemma_id INTEGER PRIMARY KEY)")
        conn.executemany("INSERT OR IGNORE INTO want VALUES (?)", ((i,) for i in lemma_ids))
        rows = conn.execute(
            "SELECT t.lemma_id, t.feat_case, t.feat_number, t.m_unsandhied, COUNT(*) AS n "
            "FROM token t JOIN want w ON w.lemma_id = t.lemma_id "
            "WHERE t.upos = 'NOUN' "
            "AND t.feat_case IN ('Nom','Acc','Ins','Dat','Abl','Gen','Loc','Voc') "
            "AND t.feat_number IN ('Sing','Dual','Plur') "
            "AND t.m_unsandhied IS NOT NULL "
            "GROUP BY t.lemma_id, t.feat_case, t.feat_number, t.m_unsandhied"
        )
        forms = defaultdict(list)
        for lemma_id, case, number, form, n in rows:
            forms[(lemma_id, f"{case}.{number}")].append((form, n))
    finally:
        conn.close()
    for key in forms:
        forms[key].sort(key=lambda p: (-p[1], p[0]))
    return forms


def classify(expected_slp1, attested_iast, to_slp1):
    """Flag generated-vs-attested relationship. Never resolves it -- only names it."""
    if not expected_slp1:
        return "no_generation"
    if not attested_iast:
        return "no_attested_form"
    attested_slp1 = {to_slp1(f) for f in attested_iast}
    hit = bool(attested_slp1 & set(expected_slp1))
    if hit and attested_slp1 <= set(expected_slp1):
        return "match"
    if hit:
        return "variant"  # generated form attested, but the corpus also has others
    return "mismatch"  # generated form never attested in this cell


def build(args):
    to_slp1 = load_transliterator()
    generate = None if args.no_generate else load_generator()
    if generate is None and not args.no_generate:
        print("WARNING: vidyut unavailable -- expected forms omitted "
              "(all rows flagged no_generation)", file=sys.stderr)

    coverage = read_coverage(args.coverage)
    frequency = read_frequency(args.frequency)
    stem_classes = read_stem_classes(args.zaliznyak)
    print(f"inputs: {len(coverage)} coverage rows · {len(frequency)} frequency lemmas · "
          f"{len(stem_classes)} Zaliznyak headwords")

    # --- join ------------------------------------------------------------------
    joined = []
    for row in coverage:
        key = to_slp1(row["lemma"])
        freq = frequency.get(key)
        stem_class = stem_classes.get(key)
        if freq is None or stem_class is None:
            continue
        core_rank = (freq.get("core_rank") or "").strip()
        if args.core_only and not core_rank:
            continue
        joined.append({
            "lemma_id": int(row["lemma_id"]),
            "lemma": row["lemma"],
            "lemma_slp1": key,
            "dom_gender": row["dom_gender"],
            "stem_class": stem_class,
            "tokens": int(row["tokens"]),
            "cells_attested": int(row["cells_attested"]),
            "bits": row["cells_bits24"],
            "count_all": int(freq.get("count_all") or 0),
            "freq_band": band_for(int(freq.get("count_all") or 0)),
            "core_rank": int(core_rank) if core_rank else None,
        })

    joined.sort(key=lambda r: (r["core_rank"] is None, r["core_rank"] or 0, -r["tokens"]))
    if args.limit:
        joined = joined[: args.limit]
    print(f"joined lemmas: {len(joined)}")

    attested = read_attested_forms(args.db, [r["lemma_id"] for r in joined])
    print(f"attested (lemma, cell) groups from DCS: {len(attested)}")

    # --- emit drill items ------------------------------------------------------
    items = []
    for rec in joined:
        bits = rec["bits"]
        if len(bits) != N_CELLS:
            raise SystemExit(f"bad bitstring width for {rec['lemma']}: {len(bits)}")
        for idx, bit in enumerate(bits):
            if bit != "1":
                continue
            cell = CELLS[idx]
            pairs = attested.get((rec["lemma_id"], cell), [])
            attested_forms = [f for f, _ in pairs[: args.max_forms]]
            cell_count = sum(n for _, n in pairs)
            expected = generate(rec["lemma_slp1"], rec["dom_gender"], cell) if generate else []
            items.append({
                "lemma_id": rec["lemma_id"],
                "lemma": rec["lemma"],
                "stem_class": rec["stem_class"],
                "gender": rec["dom_gender"],
                "cell": cell,
                "corpus_count": cell_count,
                "freq_band": rec["freq_band"],
                "core_rank": rec["core_rank"] or "",
                "expected_form": "|".join(expected),
                "attested_forms": "|".join(attested_forms),
                "agreement": classify(expected, attested_forms, to_slp1),
            })

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fields = ["lemma_id", "lemma", "stem_class", "gender", "cell", "corpus_count",
              "freq_band", "core_rank", "expected_form", "attested_forms", "agreement"]
    with (OUT_DIR / "attested_drill_items.tsv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(items)
    print(f"wrote attested_drill_items.tsv: {len(items)} rows")

    report = coverage_report(joined, items)
    (OUT_DIR / "coverage_by_stem_class.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT_DIR / "COVERAGE_REPORT.md").write_text(render_report(report), encoding="utf-8")
    print("wrote coverage_by_stem_class.json + COVERAGE_REPORT.md")

    write_widget_data(args.widget_data, joined, items, load_detransliterator())
    print(f"wrote {args.widget_data.name}")
    return report


def reload_from_tsv(path):
    """Rebuild (joined, items) from a previously emitted TSV.

    The DCS pass is an ~11-minute full scan, so retuning the *presentation* layer
    (widget quotas, report shape) must not require re-deriving the corpus evidence.
    Everything the report and the widget need is already in the TSV; `tokens` is the
    one field not carried, and it is reconstructed as the sum of per-cell counts --
    equal to the coverage asset's token total by construction, since both count the
    same case x number universe.
    """
    with path.open(encoding="utf-8", newline="") as fh:
        items = list(csv.DictReader(fh, delimiter="\t"))
    for it in items:
        it["lemma_id"] = int(it["lemma_id"])
        it["corpus_count"] = int(it["corpus_count"])

    by_id = {}
    for it in items:
        rec = by_id.get(it["lemma_id"])
        if rec is None:
            core = it["core_rank"].strip()
            rec = by_id[it["lemma_id"]] = {
                "lemma_id": it["lemma_id"], "lemma": it["lemma"],
                "stem_class": it["stem_class"], "dom_gender": it["gender"],
                "freq_band": it["freq_band"],
                "core_rank": int(core) if core else None,
                "tokens": 0, "cells_attested": 0,
            }
        rec["tokens"] += it["corpus_count"]
        rec["cells_attested"] += 1

    joined = sorted(by_id.values(),
                    key=lambda r: (r["core_rank"] is None, r["core_rank"] or 0, -r["tokens"]))
    return joined, items


def coverage_report(joined, items):
    """Per stem class: 'N attested cells of 24' + top-band coverage, the learn-N->meet-X% metric."""
    by_class = defaultdict(lambda: {"lemmas": 0, "cells": 0, "tokens": 0,
                                    "top_band_lemmas": 0, "top_band_cells": 0})
    for rec in joined:
        b = by_class[rec["stem_class"]]
        b["lemmas"] += 1
        b["cells"] += rec["cells_attested"]
        b["tokens"] += rec["tokens"]
        if rec["freq_band"] == "1000+":
            b["top_band_lemmas"] += 1
            b["top_band_cells"] += rec["cells_attested"]

    agreement = defaultdict(int)
    for it in items:
        agreement[it["agreement"]] += 1

    cell_hist = defaultdict(int)
    for it in items:
        cell_hist[it["cell"]] += 1

    classes = {}
    for name, b in sorted(by_class.items(), key=lambda kv: -kv[1]["lemmas"]):
        classes[name] = {
            "lemmas": b["lemmas"],
            "attested_cells": b["cells"],
            "mean_cells_of_24": round(b["cells"] / b["lemmas"], 2),
            "cell_space_coverage_pct": round(100 * b["cells"] / (b["lemmas"] * N_CELLS), 2),
            "tokens": b["tokens"],
            "top_band_lemmas": b["top_band_lemmas"],
            "top_band_mean_cells_of_24": (
                round(b["top_band_cells"] / b["top_band_lemmas"], 2)
                if b["top_band_lemmas"] else None),
        }

    total_cells = sum(r["cells_attested"] for r in joined)
    return {
        "asset": "Sangram W2-add-a — attested-cell declension drills (H1296)",
        "method": ("lemma_cell_coverage.csv x kosha lemma_frequency.tsv x Zaliznyak "
                   "headword_index.tsv stem_class; per-cell counts and unsandhied "
                   "surface forms from the pinned DCS snapshot; expected forms from "
                   "vidyut-prakriya, disagreements flagged never resolved"),
        "corpus_attribution": "DCS (Oliver Hellwig) via the pinned VisualDCS snapshot",
        "lemmas": len(joined),
        "drill_items": len(items),
        "mean_cells_of_24": round(total_cells / len(joined), 2) if joined else 0,
        "cell_space_coverage_pct": (
            round(100 * total_cells / (len(joined) * N_CELLS), 2) if joined else 0),
        "agreement": dict(sorted(agreement.items(), key=lambda kv: -kv[1])),
        "by_stem_class": classes,
        "cells_ranked": dict(sorted(cell_hist.items(), key=lambda kv: -kv[1])),
    }


def render_report(rep):
    lines = [
        "_Created: 19-07-2026 · Last updated: 19-07-2026_",
        "",
        "# Attested-cell declension drills — per-class coverage report",
        "",
        "Generated by [`build_attested_declension_drills.py`](build_attested_declension_drills.py)"
        " (H1296). Do not hand-edit — every number here is computed.",
        "",
        f"**{rep['lemmas']} lemmas · {rep['drill_items']} drill items · "
        f"mean {rep['mean_cells_of_24']} attested cells of 24 "
        f"({rep['cell_space_coverage_pct']} % of the cell space).**",
        "",
        f"Corpus numbers: {rep['corpus_attribution']}.",
        "",
        "## Per stem class",
        "",
        "| Stem class | Lemmas | Attested cells | Mean of 24 | Cell-space % | Top-band lemmas | Top-band mean of 24 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name, c in rep["by_stem_class"].items():
        tb = c["top_band_mean_cells_of_24"]
        lines.append(
            f"| {name} | {c['lemmas']} | {c['attested_cells']} | {c['mean_cells_of_24']} | "
            f"{c['cell_space_coverage_pct']} | {c['top_band_lemmas']} | {tb if tb is not None else '—'} |")

    lines += [
        "",
        "## Generated vs attested",
        "",
        "The drill never silently picks between the paradigm engine and the corpus.",
        "",
        "| Flag | Items | Meaning |",
        "|---|---:|---|",
    ]
    meanings = {
        "match": "generated form is exactly what the corpus attests",
        "variant": "generated form is attested, but the corpus also attests others (Vedic/classical doublets)",
        "mismatch": "generated form never attested in this cell — shown side by side, flagged",
        "no_attested_form": "cell attested in the coverage bitstring but no unsandhied form recoverable",
        "no_generation": "no generated form (gender unresolved or stem rejected by the engine)",
    }
    for flag, n in rep["agreement"].items():
        lines.append(f"| `{flag}` | {n} | {meanings.get(flag, '—')} |")

    lines += [
        "",
        "## Cells by how many lemmas attest them",
        "",
        "| Cell | Lemmas |",
        "|---|---:|",
    ]
    for cell, n in list(rep["cells_ranked"].items())[:12]:
        lines.append(f"| {cell} | {n} |")
    lines += ["", "_Dr. Mārcis Gasūns_", ""]
    return "\n".join(lines)


def write_widget_data(path, joined, items, to_iast):
    """Top-ranked drillable lemmas — the widget ships a teaching subset, not the corpus.

    Two filters the analytic TSV deliberately does NOT apply:
      * expected forms are transliterated SLP1 -> IAST, so the interface never mixes
        scripts (the TSV keeps SLP1, which is what the engine emits);
      * lemmas attesting fewer than WIDGET_MIN_DRILLABLE_CELLS drillable cells are
        dropped -- a one-cell lemma is a stray token, not a paradigm to practise.
    ``mismatch`` cells stay in the payload but are marked undrillable: the widget shows
    them as evidence, never as a question with an authoritative answer.
    """
    by_lemma = defaultdict(list)
    for it in items:
        by_lemma[it["lemma_id"]].append(it)

    out = []
    per_class = defaultdict(int)
    for rec in joined:
        if rec["stem_class"] in WIDGET_EXCLUDED_STEM_CLASSES:
            continue
        if per_class[rec["stem_class"]] >= WIDGET_LEMMAS_PER_CLASS:
            continue
        cells = by_lemma.get(rec["lemma_id"]) or []
        drillable = [c for c in cells if c["agreement"] in ("match", "variant")]
        if len(drillable) < WIDGET_MIN_DRILLABLE_CELLS:
            continue
        per_class[rec["stem_class"]] += 1
        out.append({
            "lemma": rec["lemma"],
            "stemClass": rec["stem_class"],
            "gender": rec["dom_gender"],
            "coreRank": rec["core_rank"],
            "cells": [{
                "cell": c["cell"],
                "count": c["corpus_count"],
                "expected": "|".join(to_iast(f) for f in c["expected_form"].split("|") if f),
                "attested": c["attested_forms"],
                "agreement": c["agreement"],
                "drillable": c["agreement"] in ("match", "variant"),
            } for c in sorted(cells, key=lambda c: -c["corpus_count"])],
        })

    header = (
        "// GENERATED by sangram/data/attested_drills/build_attested_declension_drills.py — do not hand-edit.\n"
        "// Attested-cell declension drill data (H1296): only corpus-attested cells, up to "
        f"{WIDGET_LEMMAS_PER_CLASS} lemmas per stem class by kosha frequency.\n"
        "// Corpus: DCS (Oliver Hellwig) via the pinned VisualDCS snapshot. Forms are unsandhied.\n"
        "// `agreement` flags generated-vs-attested disagreement; the widget must show both sides.\n\n"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        header + "export const ATTESTED_DRILLS = " +
        json.dumps(out, ensure_ascii=False, indent=1) + ";\n\n" +
        "export const DRILL_LEMMA_COUNT = ATTESTED_DRILLS.length;\n",
        encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--coverage", type=Path, default=DEFAULT_COVERAGE)
    ap.add_argument("--frequency", type=Path, default=DEFAULT_FREQ)
    ap.add_argument("--zaliznyak", type=Path, default=DEFAULT_ZALIZNYAK)
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--widget-data", type=Path, default=DEFAULT_WIDGET_DATA)
    ap.add_argument("--core-only", action="store_true", default=True,
                    help="keep only lemmas with a kosha core_rank (default)")
    ap.add_argument("--all-lemmas", dest="core_only", action="store_false",
                    help="keep every joined lemma, not just the kosha core")
    ap.add_argument("--limit", type=int, default=0, help="cap lemmas (debug)")
    ap.add_argument("--max-forms", type=int, default=3,
                    help="attested surface-form variants kept per cell")
    ap.add_argument("--no-generate", action="store_true",
                    help="skip vidyut expected-form generation")
    ap.add_argument("--widget-only", action="store_true",
                    help="rebuild the report + widget data from the existing TSV "
                         "(skips the ~11-minute DCS scan; presentation retuning only)")
    args = ap.parse_args()

    if args.widget_only:
        tsv = OUT_DIR / "attested_drill_items.tsv"
        if not tsv.exists():
            sys.exit(f"FATAL: --widget-only needs an existing {tsv}")
        joined, items = reload_from_tsv(tsv)
        print(f"reloaded {len(joined)} lemmas / {len(items)} items from {tsv.name}")
        report = coverage_report(joined, items)
        (OUT_DIR / "coverage_by_stem_class.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (OUT_DIR / "COVERAGE_REPORT.md").write_text(render_report(report), encoding="utf-8")
        write_widget_data(args.widget_data, joined, items, load_detransliterator())
        print(f"wrote COVERAGE_REPORT.md + {args.widget_data.name}")
        return

    for label, path in [("coverage", args.coverage), ("frequency", args.frequency),
                        ("zaliznyak", args.zaliznyak), ("db", args.db)]:
        if not path.exists():
            sys.exit(f"FATAL: missing {label} input: {path}")

    build(args)


if __name__ == "__main__":
    main()
