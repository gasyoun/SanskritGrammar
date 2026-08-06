#!/usr/bin/env python3
"""H1913 Slice C0 — freeze the SG-MO-021 future-article scholarly/data invariants.

Computes the pre-migration invariant record for the SG-MO-021 vertical pilot
(docs/IMPLEMENTATION_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION.md § C0):

  - per-file sha256 (raw + LF-normalized for text) of the generator script,
    article manifest, article MDX, and both generated datasets;
  - stable IDs (article id, toc_ref, example ids, revision entries);
  - every published number: the full denominator/CI/person/number/mood/top-forms
    block from coverage_summary.json, embedded verbatim;
  - sample seed, sample size, and the universe (SQL predicates), parsed from the
    generator source so a drifted predicate is visible as a diff;
  - source-DB provenance (repo, commit pin, sha256) as recorded at generation;
  - validation-sample row count and hash;
  - site route + heading/anchor list for the article page;
  - ledger state: SG-MO-021 / art:future mention counts + hashes of the ledger
    and claims surfaces that cite the article's numbers;
  - consumer census (code-level and repo-wide reference counts);
  - issue-563 gate: assert no PWG–Pāṇini crosswalk path appears in the
    generator's declared inputs.

Writes docs/architecture/baseline/h1913_c0_invariants.json. Re-run and diff to
verify nothing drifted before the C3 hard cutover; any diff other than the
`frozen_at_commit` field means an invariant moved and C3 must not proceed.
"""

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
ART_DIR = "sangram/articles/future"
GENERATOR = "scripts/sg_mo_021_future.py"
OUT = REPO / "docs" / "architecture" / "baseline" / "h1913_c0_invariants.json"

ROLES = {
    "sg_mo_021_future.py": "generator-script",
    "article.manifest.json": "hand-edited-manifest",
    "index.mdx": "authored-article",
    "coverage_summary.json": "generated-dataset",
    "validation_sample.tsv": "generated-dataset",
}

LEDGER_SURFACES = [
    "DCS_DERIVED_NUMBERS_LEDGER_2026.md",
    "sangram/editorial/data/consolidation_ledger.json",
]

CROSSWALK_TOKENS = ("crosswalk", "panini", "pwg_panini", "sutra_map")


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, text=True,
        encoding="utf-8", check=True,
    ).stdout.strip()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_record(rel: str) -> dict:
    data = (REPO / rel).read_bytes()
    name = rel.split("/")[-1]
    rec = {
        "path": rel,
        "role": ROLES.get(name, "unclassified"),
        "bytes": len(data),
        "sha256": sha256_bytes(data),
    }
    if name.endswith((".mdx", ".md", ".json", ".tsv", ".py", ".yml")):
        rec["sha256_lf_normalized"] = sha256_bytes(data.replace(b"\r\n", b"\n"))
    return rec


def headings(text: str) -> list:
    out = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            out.append({"level": len(m.group(1)), "text": m.group(2).strip()})
    return out


def main() -> None:
    tracked = [
        p for p in git("ls-files", "--", ART_DIR, GENERATOR).splitlines() if p.strip()
    ]
    files = [file_record(p) for p in sorted(tracked)]

    manifest = json.loads((REPO / ART_DIR / "article.manifest.json").read_text(encoding="utf-8"))
    art = manifest["article"]
    example_ids = [e["id"] for e in art.get("examples", [])]

    coverage = json.loads(
        (REPO / ART_DIR / "data" / "coverage_summary.json").read_text(encoding="utf-8")
    )

    gen_src = (REPO / GENERATOR).read_text(encoding="utf-8")
    seed = int(re.search(r"^SEED = (\d+)", gen_src, re.M).group(1))
    sample_size = int(re.search(r"^SAMPLE_SIZE = (\d+)", gen_src, re.M).group(1))
    fin = re.search(r'^FIN = \((.*?)\)\n', gen_src, re.M | re.S).group(1)
    universe_fin = " ".join(s.strip().strip('"') for s in fin.splitlines())
    default_db = re.search(r'^DEFAULT_DB = (.+)$', gen_src, re.M).group(1).strip()

    tsv_lines = (
        (REPO / ART_DIR / "data" / "validation_sample.tsv")
        .read_text(encoding="utf-8")
        .splitlines()
    )

    mdx_text = (REPO / ART_DIR / "index.mdx").read_text(encoding="utf-8")

    root_changelog = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")
    repo_version = (re.findall(r"^## \[(\d+\.\d+\.\d+)\]", root_changelog, re.M) or ["?"])[0]

    ledger_state = []
    for rel in LEDGER_SURFACES:
        p = REPO / rel
        if not p.exists():
            ledger_state.append({"path": rel, "exists": False})
            continue
        text = p.read_text(encoding="utf-8")
        ledger_state.append({
            "path": rel,
            "exists": True,
            "sha256_lf_normalized": sha256_bytes(
                p.read_bytes().replace(b"\r\n", b"\n")
            ),
            "sg_mo_021_mentions": len(re.findall(r"SG-MO-021", text)),
            "art_future_mentions": len(re.findall(r"art:future", text)),
        })

    code_consumers = sorted(
        p
        for p in git(
            "grep", "-l", "-e", "articles/future", "-e", "sg_mo_021", "-e", "art:future",
            "--", "scripts/", "src/", "tests/", "sangram/",
        ).splitlines()
        if p.strip() and not p.startswith(ART_DIR) and p != GENERATOR
    )
    all_referencing = [
        p
        for p in git(
            "grep", "-l", "-e", "SG-MO-021", "-e", "articles/future",
            "--", f":!{ART_DIR}", f":!{GENERATOR}",
        ).splitlines()
        if p.strip()
    ]

    gen_low = gen_src.lower()
    crosswalk_hits = [t for t in CROSSWALK_TOKENS if t in gen_low]

    record = {
        "handoff": "H1913",
        "slice": "C0",
        "article": ART_DIR,
        "frozen_at_commit": git("rev-parse", "HEAD"),
        "files": files,
        "stable_ids": {
            "article_id": art["id"],
            "toc_ref": art["toc_ref"],
            "contract_version": manifest.get("contract_version"),
            "canonical_script": manifest.get("canonical_script"),
            "as_of": art.get("as_of"),
            "example_ids": example_ids,
            "revisions": len(art.get("revisions", [])),
        },
        "published_numbers": coverage,
        "sampling": {
            "seed": seed,
            "sample_size": sample_size,
            "universe_finite_predicate": universe_fin,
            "future_restriction": "feat_tense='Fut'",
            "validation_sample_rows": max(0, len(tsv_lines) - 1),
        },
        "source_db": {
            "default_path_expr": default_db,
            "snapshot": coverage.get("snapshot"),
        },
        "site": {
            "base_url": "/SanskritGrammar/",
            "routes": [f"/SanskritGrammar/{ART_DIR}/"],
            "anchors": {"index.mdx": headings(mdx_text)},
        },
        "ledger_state": ledger_state,
        "release_provenance": {"repo_version": repo_version},
        "consumers": {
            "code_level": code_consumers,
            "repo_files_referencing_outside_context": len(all_referencing),
        },
        "issue_563_gate": {
            "declared_inputs": ["the pinned DCS sqlite snapshot (see source_db)"],
            "crosswalk_tokens_in_generator": crosswalk_hits,
            "clean": not crosswalk_hits,
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {OUT.relative_to(REPO)}")
    print(
        f"files={len(files)} examples={len(example_ids)} "
        f"code_consumers={len(code_consumers)} outside_refs={len(all_referencing)} "
        f"issue563_clean={not crosswalk_hits}"
    )


if __name__ == "__main__":
    main()
