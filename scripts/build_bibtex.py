#!/usr/bin/env python3
"""Generate per-book BibTeX + bulk all.bib for the digitized corpus (Angle-B B3).

Reads scripts/data/books.yml (the citation registry — the ONLY hand-edited
input) and regenerates static/bibtex/<key>.bib (one entry per book) plus
static/bibtex/all.bib (bulk, all books). The files are served verbatim by the
Docusaurus static dir, so /SanskritGrammar/bibtex/all.bib makes the whole
corpus citable in one fetch — the ACL Anthology's per-page-BibTeX + bulk
model (https://aclanthology.org/faq/), as roadmap §3 Angle-B B3 specifies.

Deterministic by construction: no timestamps, LF endings, key-sorted bulk
order — so `--check` is a byte-stable freshness gate (CI validators step,
same contract as consolidation_ledger_refresh --check).

Bibliographic facts live in books.yml, transcribed from each book's own
evidence (README.md / errata.yml `work:` / mdx title page); the script adds
only the derived `url` field. It also re-derives the publishable-book-dir set
from the tracked .mdx inventory (dir-level mirror of src/discovery.mjs: skip
dirs + deny segments, see DEFAULT_SKIP_DIRS/DENY_SEGMENTS there) and refuses
a registry entry whose dir is not a publishable book dir — a book that stops
being discovered can't keep a stale citation, and a dir-year mismatch (name
says 1923, registry says 1919) is a transcription error, not a style choice.
"""

import subprocess
import sys
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "scripts" / "data" / "books.yml"
OUT_DIR = ROOT / "static" / "bibtex"
REPO_URL = "https://github.com/gasyoun/SanskritGrammar"

# Dir-level mirror of src/discovery.mjs — keep in sync with that module
# (the site build is the authority; this check only needs to refuse a
# registry entry whose book folder the site would not publish).
SKIP_DIRS = {
    "node_modules", "build", ".docusaurus", "src", ".git", ".github",
    "scripts", "tests", "docs", "data", "pipelines", "packages", "apps",
}
DENY_SEGMENTS = {
    "raw", "_raw", "private", "_private", "source", "sources", "review",
    "_review", "reviews", "draft", "drafts", "_draft", "archive", "archives",
    "_archive", "scratch", "_scratch", "cache", "_cache", "ignored",
    "_ignored", "worktree", "worktrees", "node_modules", "build",
    ".docusaurus", ".git", "fixtures", "__pycache__",
}

# Emission order is the citation's reading order; `url` is always last.
FIELD_ORDER = ["author", "title", "school", "address", "edition", "year", "note", "url"]


def publishable_book_dirs() -> set[str]:
    """Top-level dirs holding tracked .mdx the site could publish.

    `ls-files -z` + filter in Python: a naive `git ls-files '*.mdx'` C-quotes
    non-ASCII paths so they stop matching the glob — the same trap
    src/discovery.mjs documents (265 vs 203 files). Front-matter deny flags
    are per-FILE and irrelevant at dir level: a dir is a candidate if ANY
    tracked .mdx survives the segment rules, matching discoverBookDirs'
    input contract.
    """
    proc = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git ls-files failed: {proc.stderr.decode()[:200]}")
    tracked = [p for p in proc.stdout.decode("utf-8").split("\0") if p.endswith(".mdx")]
    dirs: set[str] = set()
    for rel in tracked:
        parts = rel.split("/")
        top = parts[0]
        if len(parts) < 2 or not top or top.startswith(".") or top in SKIP_DIRS:
            continue
        if any(seg.lower() in DENY_SEGMENTS for seg in parts[:-1]):
            continue
        dirs.add(top)
    return dirs


def load_registry() -> list[dict]:
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    books = data.get("books") if isinstance(data, dict) else None
    if not isinstance(books, list) or not books:
        raise ValueError(f"{REGISTRY.relative_to(ROOT)}: no `books:` list")
    return books


def validate(books: list[dict]) -> None:
    errors: list[str] = []
    keys = [b.get("key") for b in books]
    dirs = [b.get("dir") for b in books]
    if len(set(keys)) != len(keys):
        errors.append("duplicate `key` values")
    if len(set(dirs)) != len(dirs):
        errors.append("duplicate `dir` values")
    discovered = publishable_book_dirs()
    for b in books:
        where = f"[{b.get('key') or b.get('dir') or '?'}]"
        for field in ("dir", "key", "type", "author", "title", "year"):
            if not b.get(field):
                errors.append(f"{where} missing `{field}`")
        if b.get("type") not in ("book", "phdthesis", "misc"):
            errors.append(f"{where} unknown type {b.get('type')!r}")
        name, _, year = str(b.get("dir", "")).rpartition("_")
        if name and year.isdigit() and str(b.get("year")) != year:
            errors.append(f"{where} dir suffix year {year} != registry year {b.get('year')}")
        if b.get("dir") and b["dir"] not in discovered:
            errors.append(f"{where} dir {b['dir']} is not a publishable book dir")
    if errors:
        raise ValueError("books.yml invalid:\n  - " + "\n  - ".join(errors))


def render_entry(book: dict) -> str:
    fields: list[tuple[str, str]] = [
        (f, str(book[f])) for f in FIELD_ORDER if f in book and book[f] not in (None, "")
    ]
    fields.append(("url", f"{REPO_URL}/tree/main/{book['dir']}"))
    body = ",\n".join(f"  {f} = {{{v}}}" for f, v in fields)
    return f"@{book['type']}{{{book['key']},\n{body}\n}}\n"


def render_all(books: list[dict]) -> dict[str, str]:
    ordered = sorted(books, key=lambda b: b["key"])
    files = {f"{b['key']}.bib": render_entry(b) for b in ordered}
    files["all.bib"] = "".join(render_entry(b) for b in ordered)
    return files


def main(argv: list[str]) -> int:
    check = "--check" in argv
    books = load_registry()
    validate(books)
    expected = render_all(books)

    on_disk = {p.name: p.read_text(encoding="utf-8").replace("\r\n", "\n")
               for p in sorted(OUT_DIR.glob("*.bib"))} if OUT_DIR.is_dir() else {}
    drift = []
    for name, text in sorted(expected.items()):
        # EOL-insensitive: a Windows autocrlf checkout (CRLF on disk) must
        # still compare fresh — drift means content, not line endings.
        if on_disk.get(name) != text:
            drift.append(name)
    stale = [n for n in on_disk if n not in expected]

    if check:
        if drift or stale:
            for n in drift:
                print(f"bibtex: DRIFT {n} (rerun: python scripts/build_bibtex.py)")
            for n in stale:
                print(f"bibtex: STALE {n} (not in books.yml; remove it)")
            return 1
        print(f"bibtex: fresh ({len(books)} books, {len(expected)} files)")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, text in sorted(expected.items()):
        (OUT_DIR / name).write_bytes(text.encode("utf-8"))
    for name in stale:
        (OUT_DIR / name).unlink()
    print(f"bibtex: {len(books)} entries -> {OUT_DIR.relative_to(ROOT)}/"
          f"all.bib + {len(books)} per-book files")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
