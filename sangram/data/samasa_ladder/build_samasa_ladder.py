#!/usr/bin/env python3
"""Sangram W2-add-c — samāsa right-to-left ladder generator (H1298).

kosha's shipped samāsa trainer (W1c, H948) drills *identify the type* and *split the
compound*. This builder feeds a different surface: the **resolution method** — the
head-first (right-to-left) vigraha ladder the ``/klammeruebersetzung`` skill encodes —
over **corpus-attested** compounds, with Russian constituent glosses.

    https://github.com/gasyoun/claude-config/blob/main/commands/klammeruebersetzung.md

The method in one line: in a determinative compound the syntactic head is the **last**
member, so the analysis runs right -> left. You name the head, then ask the question it
leaves open, and the next member leftwards answers it.

Deterministic join, no model in the loop:

  VisualDCS names.csv          168 880 corpus-attested compounds: surface, member split,
                               member count, total DCS frequency
  x SanskritRussian            lemma_glossary.tsv -- per-lemma RU gloss (SLP1-keyed,
                               corpus-derived, top variant by attestation count)
  x kosha lemma_frequency.tsv  constituent frequency band (optional, for grading)

**What this script asserts and what it refuses to assert.** The rung *sequence* (which
member joins at which step, the accumulated tail, each member's gloss) is mechanical and
is emitted. The *driving question* at each rung and the *vigraha sentence* are NOT
derivable without knowing the compound's type, and the type is exactly what this trainer
does not own (that is H948's). So the generator emits a **question slot** -- the candidate
RU case-questions for that rung -- and never picks one. A single ratified question chain
plus vigraha and smooth rendering exist only in the hand-checked gold set
(``gold_ladder_30.tsv``), which the regression test pins.

**Member order is verified, not trusted.** ``names.csv`` carries rows whose split is
scrambled relative to the surface (``rājakule; kula rājan`` -- reversed; ``ūrdhvaṁ; daśan
rātra`` -- unrelated). A right-to-left ladder is *only* meaningful if the last member is
really the last, so every row passes an ordered consonant-skeleton check against its own
surface before it can become a ladder; failures are counted and reported, never silently
dropped or silently reordered.

Stdlib-only except ``indic_transliteration`` (the IAST->SLP1 join key; its absence is a
hard error, not a silent partial run).

Read-only on every input. Regenerate:

    python sangram/data/samasa_ladder/build_samasa_ladder.py

Outputs (all under this directory unless noted):
    samasa_ladder_items.tsv    the ladder corpus (one row per compound)
    integrity_report.json      per-gate counts, incl. the rejected-split census
    COVERAGE_REPORT.md         the human-readable report
    ../../../src/components/talmud/samasaLadderData.js   widget subset

Corpus numbers are DCS (Oliver Hellwig) via the pinned VisualDCS snapshot; Russian
glosses are corpus-derived (SanskritRussian lemma_glossary.tsv, public site tier).
Attribute accordingly wherever they surface.
"""
import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
GITHUB = REPO.parent

DEFAULT_NAMES = GITHUB / "VisualDCS" / "derived-data" / "Kompozity" / "names.csv"
DEFAULT_GLOSS = GITHUB / "SanskritRussian" / "lemma_glossary.tsv"
DEFAULT_FREQ = GITHUB / "kosha" / "data" / "frequency" / "lemma_frequency.tsv"
WIDGET_OUT = REPO / "src" / "components" / "talmud" / "samasaLadderData.js"

# Frequency bands over the compound's own DCS total, matching the banding the G2
# coverage README uses for lemmas (same cut points, different denominator).
BANDS = ((100, "ядро"), (30, "частые"), (10, "средние"), (0, "редкие"))

SLP1_VOWELS = set("aAiIuUfFxXeEoO")
SLP1_MARKS = set("MH~")

# Candidate driving questions per rung, by the rung's distance from the head. The
# generator offers the slot; the learner (or the gold set) picks. Deliberately NOT
# resolved here -- picking one would assert a compound type this layer does not know.
HEAD_QUESTION = "что? (голова — последний член)"
MODIFIER_QUESTIONS = [
    "какой? / какая?",
    "чей? / чего?",
    "кого? / чего?",
    "где? / когда?",
    "как? каким образом?",
]

WIDGET_PER_BAND = 40


def skeleton(slp1: str) -> str:
    """Consonant skeleton of an SLP1 string — vowels, anusvāra and visarga dropped."""
    return "".join(c for c in slp1 if c not in SLP1_VOWELS and c not in SLP1_MARKS)


def order_ok(surface_slp1: str, member_slp1s) -> bool:
    """Do the members occur in the surface **in their given order**?

    Matching is on the first two consonants of each member's skeleton: a compound member
    is reshaped at its *right* edge by sandhi and by stem-final loss (``rājan`` -> ``rāja-``),
    and at its *left* edge only by vowel sandhi (``indra`` -> ``-endra``), which the
    consonant skeleton is blind to by construction. Two consonants is the shortest probe
    that still discriminates; single-consonant members fall back to one.
    """
    hay = skeleton(surface_slp1)
    pos = 0
    for m in member_slp1s:
        probe = skeleton(m)[:2]
        if not probe:
            return False
        hit = hay.find(probe, pos)
        if hit < 0:
            return False
        pos = hit + len(probe)
    return True


def band_of(freq: int) -> str:
    for cut, name in BANDS:
        if freq >= cut:
            return name
    return BANDS[-1][1]


GLOSS_VARIANTS = 3


def load_glosses(path: Path):
    """lemma_slp1 -> [(ru, n), ...] — the best-attested Russian variants, n desc.

    The source layer is *corpus-derived*: its Russian side is the aligned translation
    surface, so variants are frequency-ranked and often case-inflected (``ratha`` ->
    «колесницу», ``bāhu`` -> «руки»). Carrying the top few instead of one keeps that
    honest — the widget shows the range, and only the hand-checked gold set commits to a
    single citation-form gloss.
    """
    per_lemma = {}
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            lemma = row["lemma_slp1"]
            try:
                n = int(row["n"])
            except (TypeError, ValueError):
                continue
            ru = (row.get("ru") or "").strip()
            if not ru:
                continue
            per_lemma.setdefault(lemma, []).append((ru, n))
    return {
        lemma: sorted(vs, key=lambda v: (-v[1], v[0]))[:GLOSS_VARIANTS]
        for lemma, vs in per_lemma.items()
    }


def load_lemma_freq(path: Path):
    """lemma_slp1 -> count_all, for constituent grading. Optional input."""
    if not path.exists():
        return {}
    out = {}
    with path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        key = "lemma_slp1" if "lemma_slp1" in (reader.fieldnames or []) else None
        cnt = "count_all" if "count_all" in (reader.fieldnames or []) else None
        if not key or not cnt:
            return {}
        for row in reader:
            try:
                out[row[key]] = int(row[cnt])
            except (TypeError, ValueError):
                continue
    return out


def build_ladder(members, glosses_ru, variants=None):
    """The mechanical part: rungs from the head leftwards.

    Rung 1 is the head (rightmost member). Rung k adds the member k-1 steps to its left
    and shows the accumulated tail. ``questions`` is a *slot* — candidates, unresolved.
    """
    rungs = []
    n = len(members)
    for step in range(n):
        idx = n - 1 - step
        tail = members[idx:]
        rungs.append(
            {
                "step": step + 1,
                "member": members[idx],
                "ru": glosses_ru[idx],
                "ru_variants": (variants or [[]] * n)[idx],
                "tail": "-".join(tail),
                "questions": [HEAD_QUESTION]
                if step == 0
                else MODIFIER_QUESTIONS[: 3 if n <= 3 else 5],
            }
        )
    return rungs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--names", type=Path, default=DEFAULT_NAMES)
    ap.add_argument("--gloss", type=Path, default=DEFAULT_GLOSS)
    ap.add_argument("--lemma-freq", type=Path, default=DEFAULT_FREQ)
    ap.add_argument("--min-freq", type=int, default=5,
                    help="minimum DCS total frequency of the compound (default 5)")
    ap.add_argument("--max-members", type=int, default=4)
    ap.add_argument("--out-dir", type=Path, default=HERE)
    ap.add_argument("--widget-out", type=Path, default=WIDGET_OUT)
    ap.add_argument("--no-widget", action="store_true")
    args = ap.parse_args()

    try:
        from indic_transliteration import sanscript
    except ImportError:  # hard error by design — the join cannot be keyed without it
        print("FATAL: indic_transliteration is required (IAST->SLP1 join key).",
              file=sys.stderr)
        return 2

    def to_slp1(text: str) -> str:
        return sanscript.transliterate(text, sanscript.IAST, sanscript.SLP1)

    for p in (args.names, args.gloss):
        if not p.exists():
            print(f"FATAL: missing input {p}", file=sys.stderr)
            return 2

    glosses = load_glosses(args.gloss)
    lemma_freq = load_lemma_freq(args.lemma_freq)

    gates = Counter()
    rejected_order_examples = []
    missing_gloss = Counter()
    items = []

    with args.names.open(encoding="utf-8") as fh:
        for line in fh:
            cols = line.split(";")
            if len(cols) < 4:
                gates["malformed row"] += 1
                continue
            surface = cols[0].strip()
            split = cols[1].strip()
            try:
                freq = int(cols[3])
            except ValueError:
                gates["malformed row"] += 1
                continue
            gates["rows read"] += 1

            members = split.split()
            if len(members) < 2:
                gates["single-member (not a compound)"] += 1
                continue
            if len(members) > args.max_members:
                gates["deeper than --max-members"] += 1
                continue
            if freq < args.min_freq:
                gates["below --min-freq"] += 1
                continue
            gates["frequency + depth ok"] += 1

            surf_slp1 = to_slp1(surface)
            mem_slp1 = [to_slp1(m) for m in members]
            if not order_ok(surf_slp1, mem_slp1):
                gates["REJECTED: member order not verifiable in surface"] += 1
                if len(rejected_order_examples) < 25:
                    rejected_order_examples.append(
                        {"surface": surface, "split": split, "freq": freq})
                continue
            gates["member order verified"] += 1

            ru = []
            ru_variants = []
            gap = False
            for m_iast, m_slp1 in zip(members, mem_slp1):
                hit = glosses.get(m_slp1)
                if not hit:
                    gap = True
                    missing_gloss[m_iast] += 1
                    break
                ru.append(hit[0][0])
                ru_variants.append([v[0] for v in hit])
            if gap:
                gates["no RU gloss for some member"] += 1
                continue
            gates["SHIPPED"] += 1

            rungs = build_ladder(members, ru, ru_variants)
            items.append(
                {
                    "surface": surface,
                    "surface_slp1": surf_slp1,
                    "members": members,
                    "members_ru": ru,
                    "depth": len(members),
                    "freq": freq,
                    "band": band_of(freq),
                    "member_freq": [lemma_freq.get(k, 0) for k in mem_slp1],
                    "rungs": rungs,
                }
            )

    items.sort(key=lambda it: (-it["freq"], it["surface"]))

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    tsv = out_dir / "samasa_ladder_items.tsv"
    with tsv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["surface", "surface_slp1", "depth", "freq", "band",
                    "members", "members_ru", "ladder_tails", "rungs_json"])
        for it in items:
            w.writerow([
                it["surface"], it["surface_slp1"], it["depth"], it["freq"], it["band"],
                "|".join(it["members"]), "|".join(it["members_ru"]),
                "|".join(r["tail"] for r in it["rungs"]),
                json.dumps(it["rungs"], ensure_ascii=False),
            ])

    depth_hist = Counter(it["depth"] for it in items)
    band_hist = Counter(it["band"] for it in items)
    report = {
        "generated_by": "sangram/data/samasa_ladder/build_samasa_ladder.py (H1298)",
        "inputs": {
            "compounds": str(args.names),
            "ru_gloss": str(args.gloss),
            "lemma_frequency": str(args.lemma_freq) if lemma_freq else None,
        },
        "parameters": {"min_freq": args.min_freq, "max_members": args.max_members},
        "gates": dict(gates),
        "shipped": len(items),
        "depth_histogram": dict(sorted(depth_hist.items())),
        "band_histogram": dict(band_hist),
        "rejected_order_examples": rejected_order_examples,
        "top_missing_gloss_members": missing_gloss.most_common(25),
    }
    (out_dir / "integrity_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    write_coverage_report(out_dir / "COVERAGE_REPORT.md", report, items)

    if not args.no_widget:
        write_widget(args.widget_out, items)

    print(f"shipped {len(items)} ladders -> {tsv}")
    for k, v in gates.most_common():
        print(f"  {k}: {v}")
    return 0


def write_coverage_report(path: Path, report, items):
    g = report["gates"]
    lines = [
        "# Samāsa ladder corpus — coverage & integrity report",
        "",
        "_Auto-generated by [`build_samasa_ladder.py`]"
        "(https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/data/samasa_ladder/build_samasa_ladder.py)"
        " — do not hand-edit._",
        "",
        "## Gates",
        "",
        "| gate | rows |",
        "|---|---:|",
    ]
    for k, v in sorted(g.items(), key=lambda kv: -kv[1]):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        f"**Shipped: {report['shipped']} ladders.**",
        "",
        "## Depth",
        "",
        "| members | ladders |",
        "|---:|---:|",
    ]
    for d, n in report["depth_histogram"].items():
        lines.append(f"| {d} | {n} |")
    lines += ["", "## Frequency band", "", "| band | ladders |", "|---|---:|"]
    for b, n in sorted(report["band_histogram"].items(), key=lambda kv: -kv[1]):
        lines.append(f"| {b} | {n} |")
    lines += [
        "",
        "## Rejected splits (member order not verifiable in the surface)",
        "",
        "A right-to-left ladder is only meaningful if the **last member is really the "
        "last**. These `names.csv` rows fail an ordered consonant-skeleton check against "
        "their own surface form — the split is scrambled, reversed, or belongs to a "
        "different word. They are dropped, not reordered.",
        "",
        "| surface | split as given | DCS freq |",
        "|---|---|---:|",
    ]
    for ex in report["rejected_order_examples"]:
        lines.append(f"| {ex['surface']} | {ex['split']} | {ex['freq']} |")
    lines += [
        "",
        "## Most frequent members with no Russian gloss",
        "",
        "| member | compounds lost |",
        "|---|---:|",
    ]
    for m, n in report["top_missing_gloss_members"]:
        lines.append(f"| {m} | {n} |")
    lines += [
        "",
        "## Provenance",
        "",
        "Compounds and frequencies: DCS (Oliver Hellwig) via the pinned VisualDCS "
        "snapshot, [`derived-data/Kompozity/names.csv`]"
        "(https://github.com/gasyoun/VisualDCS/blob/main/derived-data/Kompozity/names.csv). "
        "Russian constituent glosses: corpus-derived "
        "[`SanskritRussian/lemma_glossary.tsv`]"
        "(https://github.com/gasyoun/SanskritRussian/blob/main/lemma_glossary.tsv) "
        "(public site tier — no in-copyright dictionary text).",
        "",
        "_Dr. Mārcis Gasūns_",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_widget(path: Path, items):
    """Top ladders per band, so every difficulty tier is reachable in the widget."""
    by_band = {}
    for it in items:
        by_band.setdefault(it["band"], []).append(it)
    subset = []
    for band in (name for _, name in BANDS):
        subset.extend(by_band.get(band, [])[:WIDGET_PER_BAND])
    payload = [
        {
            "surface": it["surface"],
            "band": it["band"],
            "depth": it["depth"],
            "freq": it["freq"],
            "members": it["members"],
            "membersRu": it["members_ru"],
            "rungs": it["rungs"],
        }
        for it in subset
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "// GENERATED by sangram/data/samasa_ladder/build_samasa_ladder.py — do not hand-edit.\n"
        "// Samāsa right-to-left ladder data (H1298). Corpus-attested compounds only;\n"
        "// member order verified against the surface form. Corpus: DCS (Oliver Hellwig)\n"
        "// via the pinned VisualDCS snapshot. RU glosses: SanskritRussian corpus layer.\n"
        "// `questions` is a SLOT, not an answer — the compound type is not asserted here.\n\n"
        "export const SAMASA_LADDERS = "
        + json.dumps(payload, ensure_ascii=False, indent=1)
        + ";\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
