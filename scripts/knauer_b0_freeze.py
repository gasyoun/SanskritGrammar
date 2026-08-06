#!/usr/bin/env python3
"""H1912 Slice B0 — freeze the KnauerFrazy_1908 bounded-context invariants.

Computes the pre-migration invariant record for the Knauer vertical pilot
(docs/IMPLEMENTATION_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION.md § B0):

  - authoritative-source identity + sha256 (.docx authoritative, .doc legacy);
  - generated-output raw and LF-normalized sha256 (MDX, ERRATA.mdx,
    PARSE_AUDIT.md, ERRATA_PRINT_SHEET.html);
  - media inventory (explicitly recorded, even when empty);
  - route + heading/anchor list for the site pages;
  - errata and parse-audit entry counts and verdict histogram;
  - release/changelog provenance (book version, repo version, HEAD commit);
  - consumer census (code-level and repo-wide reference counts).

Writes docs/architecture/baseline/h1912_b0_invariants.json. Re-run and diff to
verify nothing drifted before the B3 hard cutover; any diff other than the
`frozen_at_commit` field means an invariant moved and B3 must not proceed.
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
WORK_DIR = "KnauerFrazy_1908"
OUT = REPO / "docs" / "architecture" / "baseline" / "h1912_b0_invariants.json"

ROLES = {
    "Frazy-Knauer-03.05.2023.docx": "source-authoritative",
    "Frazy-Knauer-03.05.2023.doc": "source-legacy",
    "Frazy-Knauer-03.05.2023.mdx": "generated-mdx",
    "ERRATA.mdx": "generated-errata",
    "ERRATA_PRINT_SHEET.html": "generated-print-sheet",
    "PARSE_AUDIT.md": "generated-parse-audit",
    "errata.yml": "hand-edited-source",
    "parse_audit.yml": "hand-edited-source",
    "build_parse_audit.py": "generator-script",
    "CHANGELOG.md": "provenance",
    "README.md": "doc",
}

MEDIA_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".mp3", ".mp4", ".pdf"}


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
    if name.endswith((".mdx", ".md", ".html", ".yml")):
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
        p for p in git("ls-files", "--", WORK_DIR).splitlines() if p.strip()
    ]
    files = [file_record(p) for p in sorted(tracked)]
    media = [f for f in files if Path(f["path"]).suffix.lower() in MEDIA_EXT]

    errata_text = (REPO / WORK_DIR / "errata.yml").read_text(encoding="utf-8")
    errata_entries = len(re.findall(r"^\s+- \{ page:", errata_text, re.M))

    audit_text = (REPO / WORK_DIR / "parse_audit.yml").read_text(encoding="utf-8")
    audit_ids = re.findall(r"^\s*- id: (KN-\d+)", audit_text, re.M)
    verdicts: dict = {}
    for v in re.findall(r"^\s*verdict: (\S+)", audit_text, re.M):
        verdicts[v] = verdicts.get(v, 0) + 1

    mdx_text = (REPO / WORK_DIR / "Frazy-Knauer-03.05.2023.mdx").read_text(
        encoding="utf-8"
    )
    errata_mdx_text = (REPO / WORK_DIR / "ERRATA.mdx").read_text(encoding="utf-8")

    book_changelog = (REPO / WORK_DIR / "CHANGELOG.md").read_text(encoding="utf-8")
    book_version = (re.findall(r"^## \[(\d+\.\d+\.\d+)\]", book_changelog, re.M) or ["?"])[0]
    root_changelog = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")
    repo_version = (re.findall(r"^## \[(\d+\.\d+\.\d+)\]", root_changelog, re.M) or ["?"])[0]

    code_consumers = sorted(
        p
        for p in git("grep", "-l", WORK_DIR, "--", "scripts/", "src/", "tests/").splitlines()
        if p.strip()
    )
    all_referencing = [
        p
        for p in git("grep", "-l", "-i", "knauer", "--", f":!{WORK_DIR}").splitlines()
        if p.strip()
    ]

    record = {
        "handoff": "H1912",
        "slice": "B0",
        "work": WORK_DIR,
        "frozen_at_commit": git("rev-parse", "HEAD"),
        "files": files,
        "media_inventory": media,
        "site": {
            "base_url": "/SanskritGrammar/",
            "routes": [
                f"/SanskritGrammar/{WORK_DIR}/Frazy-Knauer-03.05.2023",
                f"/SanskritGrammar/{WORK_DIR}/ERRATA",
            ],
            "anchors": {
                "Frazy-Knauer-03.05.2023.mdx": headings(mdx_text),
                "ERRATA.mdx": headings(errata_mdx_text),
            },
        },
        "errata": {
            "source": f"{WORK_DIR}/errata.yml",
            "raw_yml_rows": errata_entries,
            "generated_merged_entries": len(
                re.findall(r"`knauer-frazy-1908\.\d+\.\d+(?:\.v\d+)?`", errata_mdx_text)
            ),
        },
        "parse_audit": {
            "source": f"{WORK_DIR}/parse_audit.yml",
            "ids": len(audit_ids),
            "first_id": audit_ids[0] if audit_ids else None,
            "last_id": audit_ids[-1] if audit_ids else None,
            "verdicts": verdicts,
        },
        "release_provenance": {
            "book_version": book_version,
            "repo_version": repo_version,
        },
        "consumers": {
            "code_level": code_consumers,
            "repo_files_referencing_knauer_outside_context": len(all_referencing),
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {OUT.relative_to(REPO)}")
    print(
        f"files={len(files)} media={len(media)} errata={errata_entries} "
        f"parse_audit_ids={len(audit_ids)} verdicts={verdicts}"
    )


if __name__ == "__main__":
    main()
