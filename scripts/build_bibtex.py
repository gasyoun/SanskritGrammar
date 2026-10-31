#!/usr/bin/env python3
"""Generate per-book BibTeX + bulk all.bib and the ID-representation layer.

Angle-B B3: scripts/data/books.yml (the citation registry — the ONLY
hand-edited input) -> static/bibtex/<key>.bib (one entry per book) plus
static/bibtex/all.bib (bulk). The ACL Anthology's per-page-BibTeX + bulk
model (https://aclanthology.org/faq/).

Angle-B B4 — multi-representation URLs, "one ID, many representations"
(https://aclanthology.org/info/ids/): every corpus ID also gets
  static/id/<key>.json  machine-readable metadata (self-describing: lists
                          its own representations)
  static/id/<key>.html   human landing served at /SanskritGrammar/id/<key>
                          (GitHub Pages serves foo.html at the clean URL
                          /foo), carrying <link rel=alternate> entries for
                          the BibTeX and JSON representations.
  static/id/index.json   the ID inventory (bulk discovery).
B3's published paths (bibtex/<key>.bib, all.bib) are byte-stable — B4 only
adds the id/ layer on top of the same registry and the same gate.

Deterministic by construction: no timestamps, LF endings, key-sorted bulk
order — so `--check` is a byte-stable freshness gate (CI validators step,
same contract as consolidation_ledger_refresh --check). JSON is
ensure_ascii=False + sorted keys; HTML is entity-escaped UTF-8.

Bibliographic facts live in books.yml, transcribed from each book's own
evidence (README.md / errata.yml `work:` / mdx title page); the script adds
only derived URLs. SITE_BASE mirrors docusaurus.config.mjs (url + baseUrl) —
if the site moves, update both. The script also re-derives the
publishable-book-dir set from the tracked .mdx inventory (dir-level mirror
of src/discovery.mjs: skip dirs + deny segments) and refuses a registry
entry whose dir is not a publishable book dir — a book that stops being
discovered can't keep a stale citation, and a dir-year mismatch (name says
1923, registry says 1919) is a transcription error, not a style choice.
"""

import html
import json
import subprocess
import sys
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "scripts" / "data" / "books.yml"
PEOPLE_REGISTRY = ROOT / "scripts" / "data" / "people.yml"
OUT_DIR = ROOT / "static" / "bibtex"
ID_DIR = ROOT / "static" / "id"
PEOPLE_DIR = ROOT / "static" / "people"
REPO_URL = "https://github.com/gasyoun/SanskritGrammar"
# Mirror of docusaurus.config.mjs url + baseUrl — keep both in sync.
SITE_BASE = "https://gasyoun.github.io/SanskritGrammar"

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


def load_people() -> list[dict]:
    data = yaml.safe_load(PEOPLE_REGISTRY.read_text(encoding="utf-8"))
    people = data.get("people") if isinstance(data, dict) else None
    if not isinstance(people, list) or not people:
        raise ValueError(f"{PEOPLE_REGISTRY.relative_to(ROOT)}: no `people:` list")
    return people


def validate_people(people: list[dict], books: list[dict]) -> None:
    """Cross-registry consistency (B6): every work key exists in books.yml,
    slugs are unique, and every book's author is the canonical name of some
    person claiming that work — a book whose author string matches no person
    record is an identity gap, not a formatting choice."""
    errors: list[str] = []
    slugs = [p.get("slug") for p in people]
    if len(set(slugs)) != len(slugs):
        errors.append("duplicate `slug` values")
    book_keys = {b["key"]: b for b in books}
    for p in people:
        where = f"[{p.get('slug', '?')}]"
        for field in ("slug", "name", "roles", "works"):
            if not p.get(field):
                errors.append(f"{where} missing `{field}`")
        for w in p.get("works", []):
            if w not in book_keys:
                errors.append(f"{where} unknown work key {w!r}")
    for b in books:
        claimed = any(
            b["key"] in (p.get("works") or []) and p.get("name") == b.get("author")
            for p in people
        )
        if not claimed:
            errors.append(
                f"[{b.get('key', '?')}] author {b.get('author')!r} is no person's "
                f"canonical name for that work"
            )
    if errors:
        raise ValueError("people.yml invalid:\n  - " + "\n  - ".join(errors))


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


def plain(text: str) -> str:
    """Strip BibTeX case-protection braces for display surfaces (json/html) —
    `{C}ursus` is .bib syntax, not part of the title a human or a JSON
    consumer should see."""
    return str(text).replace("{", "").replace("}", "")


def representations(key: str) -> dict[str, str]:
    return {
        "html": f"{SITE_BASE}/id/{key}",
        "bibtex": f"{SITE_BASE}/bibtex/{key}.bib",
        "json": f"{SITE_BASE}/id/{key}.json",
    }


def render_meta(book: dict) -> str:
    meta = {
        "id": book["key"],
        "type": book["type"],
        "dir": book["dir"],
        "author": plain(book["author"]),
        "title": plain(book["title"]),
        "year": book["year"],
        "representations": representations(book["key"]),
        "site_section": f"{SITE_BASE}/grammars",
        "source": f"{REPO_URL}/tree/main/{book['dir']}",
    }
    if book.get("note"):
        meta["note"] = plain(book["note"])
    return json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def render_landing(book: dict) -> str:
    key = book["key"]
    title, author, year = plain(book["title"]), plain(book["author"]), book["year"]
    reps = representations(key)
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>{html.escape(key)} — {html.escape(title)}</title>
<link rel="alternate" type="application/x-bibtex" href="{reps['bibtex']}">
<link rel="alternate" type="application/json" href="{reps['json']}">
</head>
<body>
<h1>{html.escape(title)}</h1>
<p>{html.escape(author)} · {year} · identifier <code>{html.escape(key)}</code></p>
<ul>
<li><a href="{reps['bibtex']}">BibTeX</a></li>
<li><a href="{reps['json']}">Metadata (JSON)</a></li>
<li><a href="{SITE_BASE}/grammars">Site section</a></li>
<li><a href="{REPO_URL}/tree/main/{book['dir']}">Source in repository</a></li>
</ul>
</body>
</html>
"""


def render_all(books: list[dict], people: list[dict]) -> dict[str, str]:
    """Every generated artifact, as ROOT-relative path -> file text."""
    ordered = sorted(books, key=lambda b: b["key"])
    books_by_key = {b["key"]: b for b in ordered}
    files: dict[str, str] = {}
    for b in ordered:
        files[f"bibtex/{b['key']}.bib"] = render_entry(b)
        files[f"id/{b['key']}.json"] = render_meta(b)
        files[f"id/{b['key']}.html"] = render_landing(b)
    files["bibtex/all.bib"] = "".join(render_entry(b) for b in ordered)
    files["id/index.json"] = json.dumps(
        {"count": len(ordered), "ids": [b["key"] for b in ordered]},
        ensure_ascii=False, indent=2, sort_keys=True,
    ) + "\n"
    for p in sorted(people, key=lambda p: p["slug"]):
        files[f"people/{p['slug']}.json"] = render_person_meta(p, books_by_key)
        files[f"people/{p['slug']}.html"] = render_person_page(p, books_by_key)
    files["people/index.json"] = json.dumps(
        {"count": len(people), "people": [p["slug"] for p in sorted(people, key=lambda q: q["slug"])]},
        ensure_ascii=False, indent=2, sort_keys=True,
    ) + "\n"
    return files


def render_person_meta(person: dict, books_by_key: dict[str, dict]) -> str:
    slug = person["slug"]
    works = []
    for key in person["works"]:
        b = books_by_key[key]
        works.append({
            "id": key,
            "title": plain(b["title"]),
            "year": b["year"],
            "representations": representations(key),
        })
    meta = {
        "slug": slug,
        "name": plain(person["name"]),
        "variants": person.get("variants", []),
        "roles": person["roles"],
        "works": works,
        "representations": {
            "html": f"{SITE_BASE}/people/{slug}",
            "json": f"{SITE_BASE}/people/{slug}.json",
        },
    }
    return json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def render_person_page(person: dict, books_by_key: dict[str, dict]) -> str:
    slug = person["slug"]
    name = plain(person["name"])
    variants = person.get("variants", [])
    works = "".join(
        f'<li><a href="{SITE_BASE}/id/{key}">{html.escape(plain(books_by_key[key]["title"]))}</a> '
        f'({books_by_key[key]["year"]}) · <a href="{SITE_BASE}/bibtex/{key}.bib">BibTeX</a></li>'
        for key in person["works"]
    )
    variant_items = "".join(
        "<li>" + html.escape(v["form"])
        + (" — not used here: " + html.escape(v.get("note", "")) if v.get("rejected") else "")
        + "</li>"
        for v in variants
    ) or "<li>(no recorded variants)</li>"
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>{html.escape(name)}</title>
<link rel="alternate" type="application/json" href="{SITE_BASE}/people/{slug}.json">
</head>
<body>
<h1>{html.escape(name)}</h1>
<p>{", ".join(person["roles"])} · identifier <code>{html.escape(slug)}</code></p>
<h2>Name variants</h2>
<ul>
{variant_items}
</ul>
<h2>Works</h2>
<ul>
{works}
</ul>
</body>
</html>
"""


def scan_disk() -> dict[str, str]:
    out: dict[str, str] = {}
    for base, pattern in (
        (OUT_DIR, "*.bib"),
        (ID_DIR, "*.json"), (ID_DIR, "*.html"),
        (PEOPLE_DIR, "*.json"), (PEOPLE_DIR, "*.html"),
    ):
        if base.is_dir():
            for p in sorted(base.glob(pattern)):
                out[f"{base.name}/{p.name}"] = (
                    p.read_text(encoding="utf-8").replace("\r\n", "\n")
                )
    return out


def main(argv: list[str]) -> int:
    check = "--check" in argv
    books = load_registry()
    people = load_people()
    validate(books)
    validate_people(people, books)
    expected = render_all(books, people)
    on_disk = scan_disk()

    drift = [n for n, text in sorted(expected.items()) if on_disk.get(n) != text]
    stale = [n for n in sorted(on_disk) if n not in expected]

    if check:
        if drift or stale:
            for n in drift:
                print(f"bibtex: DRIFT {n} (rerun: python scripts/build_bibtex.py)")
            for n in stale:
                print(f"bibtex: STALE {n} (not in books.yml; remove it)")
            return 1
        print(f"bibtex: fresh ({len(books)} books, {len(expected)} files)")
        return 0

    for rel in sorted(expected):
        path = ROOT / "static" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(expected[rel].encode("utf-8"))
    for rel in stale:
        (ROOT / "static" / rel).unlink()
    print(f"bibtex: {len(books)} entries + {len(people)} people -> "
          f"static/bibtex/ + static/id/ + static/people/ "
          f"({len(expected)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
