"""Emit the `thematic` Type-D typed-link dataset (TYPED_LINK_ID_GRAMMAR.md §4b, H540)
for the landed SubjectConcordance fine-grained form-category spine.

One row per WhitneyRoots/src/form_section_concordance.json category: anchor = the
Whitney Sanskrit Grammar (1889) section range that category spans
(whitney-sec:<lo>[-<hi>]), target = the SubjectConcordance thematic category
(subject:sanskritgrammar:<category-key>, the concordance's own dict key, carried
verbatim per spec §0). match_method=curated -- the range->category mapping is the
concordance's own authoritative assertion, not a computed match.

Note (reported to TYPED_LINK_ID_GRAMMAR.md's parked questions, H540): the spec's own
§4b worked example anchors at the range's first section alone (whitney-sec:611) even
though its category (present_root) spans 611-641. This emitter anchors at the FULL
verbatim range (whitney-sec:611-641) when lo != hi -- ANCHOR_PATTERNS already permits
this shape and it is lossless, whereas anchoring at lo alone silently drops the
range's extent. Single-section categories (lo == hi, e.g. present_cur 775-775) emit
the bare number.
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "kosha" / "scripts"))
from concordance_core import TIER_CONFIDENCE, TYPE_D_RECORD_FIELDS  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parents[1]
CONCORDANCE_JSON = HERE.parent / "WhitneyRoots" / "src" / "form_section_concordance.json"
OUT_TSV = HERE / "SubjectConcordance" / "typed_link_thematic.tsv"

# SubjectConcordance/catalog.mdx's own creation date -- when this curated §-range ->
# category assertion (source_dataset) was landed.
LANDED_DATE = "07-07-2026"


def whitney_sec_id(lo, hi):
    return "whitney-sec:%d" % lo if lo == hi else "whitney-sec:%d-%d" % (lo, hi)


def main():
    data = json.loads(CONCORDANCE_JSON.read_text(encoding="utf-8"))
    categories = data["categories"]

    out_rows = []
    for key, cat in categories.items():
        out_rows.append({
            "anchor_type": "whitney-sec",
            "anchor_id": whitney_sec_id(cat["lo"], cat["hi"]),
            "anchor_key_slp1": "",
            "target_locus": "subject:sanskritgrammar:%s" % key,
            "link_type": "thematic",
            "source_dataset": "SanskritGrammar/SubjectConcordance/catalog.mdx",
            "match_method": "curated",
            "confidence": TIER_CONFIDENCE["curated"],
            "evidence_count": "",
            "date": LANDED_DATE,
        })

    OUT_TSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_TSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=TYPE_D_RECORD_FIELDS, delimiter="\t")
        writer.writeheader()
        writer.writerows(out_rows)

    print("categories: %d, emitted: %d" % (len(categories), len(out_rows)))


if __name__ == "__main__":
    main()
