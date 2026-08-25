"""SG-MO-021 «Будущее время и кондиционал» — registered pipeline generator.

Slice C2 of H1913: the pre-cutover ``scripts/sg_mo_021_future.py`` logic moved
behind the Slice-A extension points. The scholarly content (predicates,
published structure, limits prose) is unchanged — the golden tests pin the
outputs byte-for-byte against the captured pre-movement behavior.

Layer contract (architecture section 5.2):

- pure functions (``wilson_ci``, ``build_summary``, ``select_sample``) take
  values in and return values out — no I/O, directly testable;
- all filesystem/SQLite access goes through :mod:`sg_tooling.adapters.dcs`;
- the manifest-facing entry point is the single registered command
  ``sg_mo_021_future.generate`` (see ``pipelines/sg-mo-021-future.yml``).

Determinism contract: pinned snapshot + provenance pin refusal (C3 §2.1),
seeded sampling (``SEED``), fixed JSON key order, and no wall-clock or
host-specific bytes in any output.
"""
from __future__ import annotations

import csv
import json
import math
import random
import sys
from pathlib import Path

from sg_tooling.adapters.dcs import DcsMaster
from sg_tooling.contracts.validate import repo_root
from sg_tooling.generators import register

__all__ = [
    "DEFAULT_SAMPLE_SIZE",
    "DEFAULT_SEED",
    "FIN",
    "FINFUT",
    "build_summary",
    "generate",
    "run_census",
    "select_sample",
    "wilson_ci",
]

# ---------------------------------------------------------------- predicates --
# The article's universe, verbatim from the pre-cutover generator (C0 frozen):
# finite verbs with a person feature; the future restriction is natively tagged.
FIN = ("upos='VERB' AND (feat_verbform='Fin' OR feat_verbform IS NULL) "
       "AND feat_person IS NOT NULL")
FINFUT = f"{FIN} AND feat_tense='Fut'"

DEFAULT_SEED = 20260717
DEFAULT_SAMPLE_SIZE = 50

TOP_FORMS_LIMIT = 15
TOP_PERIPHRASTIC_LIMIT = 8

SAMPLE_HEADER = ["token_id", "form", "unsandhied", "lemma", "person", "number",
                 "formation", "mood", "text", "chapter_ref", "sent_counter"]

PROVENANCE_NOTE = ("pin 04e0778 orphaned; binding = provenance table + SHA-256 "
                   "+ tag c3-pin-04e0778-content")


def default_db_path(root=None) -> Path:
    """The off-Git sibling master, bound by pin+SHA not by path (C0 record)."""
    return (root or repo_root()).parent / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"


def default_out_dir(root=None) -> Path:
    return (root or repo_root()) / "content" / "sangram" / "articles" / "future" / "data"


# ------------------------------------------------------------- pure domain --
def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple:
    """Wilson score interval on a share, rounded to 4 decimals."""
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d
    return (round(centre - half, 4), round(centre + half, 4))


def select_sample(ids, seed: int, size: int):
    """The seeded future-token sample: sorted universe, Mersenne draw.

    Sorting before ``random.sample`` makes the draw independent of the engine's
    scan order; the seed pins it across runs.
    """
    rng = random.Random(seed)
    chosen = rng.sample(sorted(ids), min(size, len(ids)))
    return chosen


def build_summary(
    *,
    provenance: dict,
    sha256: str,
    fin_total: int,
    fin_fut: int,
    peri: int,
    cond: int,
    fut_part: int,
    person: dict,
    number: dict,
    mood: dict,
    top_forms: list,
    top_periphrastic: list,
    seed: int,
    sample_size: int,
) -> dict:
    """Assemble the coverage summary in its published key order.

    Key order is part of the output contract (the file is diffed byte-for-byte);
    do not reorder without re-freezing the C0 record.
    """
    simple = fin_fut - peri
    first = person.get("1", {}).get("tokens", 0)
    third = person.get("3", {}).get("tokens", 0)
    return {
        "study": "SG-MO-021 «Будущее время и кондиционал» — future + conditional (core W2 ①, content)",
        "toc_ref": "SG-MO-021",
        "kind": "content article (no kill-gate) — closes the finite tense system",
        "method": "finite verbs with Tense=Fut — natively tagged (like the imperfect); simple vs periphrastic separated by feat_formation='peri'; conditional by feat_mood='Cond'; future participle (VerbForm=Part & Tense=Fut) counted separately",
        "snapshot": {
            "source_repo": provenance.get("source_repo"),
            "source_commit": provenance.get("source_commit"),
            "imported_at": provenance.get("imported_at"),
            "sha256": sha256,
            "provenance_note": PROVENANCE_NOTE,
        },
        "denominators": {
            "finite_total": fin_total,
            "finite_future": fin_fut,
            "finite_future_share": round(fin_fut / fin_total, 4),
            "simple_future": simple,
            "periphrastic_future": peri,
            "periphrastic_share_of_future": round(peri / fin_fut, 4),
            "conditional": cond,
            "future_participle": fut_part,
        },
        "future_share_ci95": {"k": fin_fut, "n": fin_total, "ci95": wilson_ci(fin_fut, fin_total)},
        "periphrastic_share_ci95": {"k": peri, "n": fin_fut, "ci95": wilson_ci(peri, fin_fut)},
        "person": person,
        "number": number,
        "mood": mood,
        "first_person_share_ci95": {"k": first, "n": fin_fut, "ci95": wilson_ci(first, fin_fut)},
        "third_person_share_ci95": {"k": third, "n": fin_fut, "ci95": wilson_ci(third, fin_fut)},
        "top_forms": [{"form": m, "lemma": l, "tokens": c} for m, l, c in top_forms],
        "top_periphrastic": [{"form": m, "lemma": l, "tokens": c} for m, l, c in top_periphrastic],
        "validation_sample": {
            "seed": seed,
            "size": sample_size,
            "file": "validation_sample.tsv",
        },
        "limits": {
            "conditional_rare": "the conditional (feat_mood=Cond) is very rare (340); it is the counterfactual 'would have', not a plain future",
            "periphrastic_via_formation": "simple vs periphrastic rests on feat_formation='peri'; the periphrastic future (-tṛ + as) shares the -tṛ agent-noun shape with the periphrastic PERFECT — DCS separates them by Tense (Fut vs Past), the tag we trust",
            "future_participle_separate": "the future participle (VerbForm=Part & Tense=Fut) is counted apart from the finite future",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }


# ------------------------------------------------------------------ wiring --
def run_census(db_path, out_dir, *, seed: int = DEFAULT_SEED,
               sample_size: int = DEFAULT_SAMPLE_SIZE,
               expected_sha256: str | None = None) -> dict:
    """One deterministic census pass: read the pinned master, write both outputs.

    Returns the assembled summary. Raises :class:`MissingProvenancePin` on an
    unpinned master and :class:`FileNotFoundError` when the master is absent.
    """
    with DcsMaster(db_path) as master:
        prov = master.provenance()
        sha = master.sha256()
        if expected_sha256 is not None and sha != expected_sha256:
            raise ValueError(
                "sg_mo_021_future: DCS snapshot SHA-256 mismatch; "
                f"expected {expected_sha256}, got {sha}"
            )

        fin_total = master.count(FIN)
        fin_fut = master.count(FINFUT)
        peri = master.count(f"{FINFUT} AND feat_formation='peri'")
        cond = master.count(f"{FINFUT} AND feat_mood='Cond'")
        fut_part = master.count(
            "upos='VERB' AND feat_verbform='Part' AND feat_tense='Fut'"
        )

        person = master.distribution("feat_person", FINFUT, fin_fut)
        number = master.distribution("feat_number", FINFUT, fin_fut)
        mood = master.distribution("feat_mood", FINFUT, fin_fut)

        top = master.top_form_lemmas(FINFUT, TOP_FORMS_LIMIT)
        top_peri = master.top_form_lemmas(
            f"{FINFUT} AND feat_formation='peri'", TOP_PERIPHRASTIC_LIMIT
        )

        chosen = select_sample(list(master.token_ids(FINFUT)), seed, sample_size)
        sample_rows = [master.sample_context_row(tid) for tid in chosen]

    summary = build_summary(
        provenance=prov,
        sha256=sha,
        fin_total=fin_total,
        fin_fut=fin_fut,
        peri=peri,
        cond=cond,
        fut_part=fut_part,
        person=person,
        number=number,
        mood=mood,
        top_forms=top,
        top_periphrastic=top_peri,
        seed=seed,
        sample_size=len(sample_rows),
    )

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # csv's default lineterminator (\r\n) with newline="" is the pre-cutover
    # byte format; keep it so the committed TSV never shifts.
    with open(out_dir / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(SAMPLE_HEADER)
        writer.writerows(sample_rows)

    (out_dir / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    den = summary["denominators"]
    print(f"finite {fin_total:,}; finite future {fin_fut:,} ({100*fin_fut/fin_total:.2f}%)",
          file=sys.stderr)
    print(f"simple {den['simple_future']:,} ({100*den['simple_future']/fin_fut:.1f}%); "
          f"periphrastic {den['periphrastic_future']:,} "
          f"({100*den['periphrastic_future']/fin_fut:.1f}%); conditional {cond}; "
          f"future participle {fut_part:,}", file=sys.stderr)
    return summary


@register("sg_mo_021_future.generate")
def generate(step, context) -> dict:
    """Manifest step: run the SG-MO-021 census through the declared options.

    Options (all optional, declarative only):

    - ``db``: explicit master path; default is the off-Git sibling resolved
      from the repository root (bound by pin + SHA-256, never by trust);
    - ``out_dir``: explicit output directory (test seam); default is the
      article's own data directory inside the bounded context;
    - ``seed`` / ``sample_size``: must match the frozen values; a deviation is
      a changed scholarly invariant, so non-default values are refused unless
      they equal the C0 freeze.
    """
    options = step.get("options") or {}
    root = repo_root()

    seed = int(options.get("seed", DEFAULT_SEED))
    sample_size = int(options.get("sample_size", DEFAULT_SAMPLE_SIZE))
    if seed != DEFAULT_SEED or sample_size != DEFAULT_SAMPLE_SIZE:
        raise ValueError(
            "sg_mo_021_future: seed/sample_size are frozen at "
            f"{DEFAULT_SEED}/{DEFAULT_SAMPLE_SIZE} by the C0 record; refusing "
            f"{seed}/{sample_size}"
        )

    db_path = Path(options["db"]) if options.get("db") else default_db_path(root)
    out_dir = Path(options["out_dir"]) if options.get("out_dir") else default_out_dir(root)
    declared_inputs = context.get("inputs") or []
    declared_dcs = next(
        (item for item in declared_inputs if item.get("provenance_id") == "external:dcs-conllu-sqlite-c3-pin"),
        None,
    )
    expected_sha256 = declared_dcs.get("sha256") if declared_dcs else None
    return run_census(
        db_path,
        out_dir,
        seed=seed,
        sample_size=sample_size,
        expected_sha256=expected_sha256,
    )
