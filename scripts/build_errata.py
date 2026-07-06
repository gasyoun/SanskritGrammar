#!/usr/bin/env python
"""Generate per-book ERRATA.md (and a root index) from each book's errata.yml.

Design: `<Book>/errata.yml` is the hand-edited structured source; `<Book>/ERRATA.md`
is generated and must never be edited by hand — same "source + generate" pattern the
repo already uses for `.docx -> .mdx`.

What it does
------------
1. Finds every `<Book>/errata.yml` (or the one book passed as an argument).
2. De-duplicates entries: rows with the same (page, line, read, instead) are merged
   into one, unioning their `found_by` sources (an erratum reported by both the 1908
   print and the 2023 errata list becomes a single row citing both).
3. Sorts by page, then top-lines (св.) before bottom-lines (сн.), then line number.
4. Cross-references CHANGELOG.md: an entry with `fixed_in: vX.Y.Z` is rendered as
   "fixed" and the version is confirmed to exist in the changelog; changelog lines
   that mention a book + a correction keyword print a reminder to set `fixed_in`.
5. Writes `<Book>/ERRATA.md` and a root `ERRATA.md` index.

Usage:
    python scripts/build_errata.py            # all books
    python scripts/build_errata.py KnauerFrazy_1908
"""

import sys
import re
import datetime
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
TODAY = datetime.date.today()
# Fix-VERBS only, so a changelog line that merely *catalogues* errata ("25 errata
# added") does not trip the "did you set fixed_in?" reminder — only lines that say
# something was actually corrected in the digital source do.
CORRECTION_KEYWORDS = ("fixed", "corrected", "исправл")


def ddmmyyyy(d: datetime.date) -> str:
    return d.strftime("%d-%m-%Y")


def line_sort_key(line: str):
    """Sort key for a Russian line-ref like '8 сн.' / '13 св.' / '14, 12 сн.'."""
    nums = re.findall(r"\d+", line or "")
    n = int(nums[0]) if nums else 0
    top = 0 if "св" in (line or "") else 1  # from-top (св.) before from-bottom (сн.)
    return (top, n)


def dedup_key(e: dict):
    return (str(e.get("page", "")), str(e.get("line", "")).strip(),
            str(e.get("read", "")).strip(), str(e.get("instead", "")).strip())


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def load_book(yml: Path):
    data = yaml.safe_load(yml.read_text(encoding="utf-8")) or {}
    work = data.get("work", yml.parent.name)
    raw = data.get("entries", []) or []

    merged: dict = {}
    for e in raw:
        k = dedup_key(e)
        if k in merged:
            # union found_by; keep earliest date_added; keep any fixed_in / note
            m = merged[k]
            for src in as_list(e.get("found_by")):
                if src not in m["found_by"]:
                    m["found_by"].append(src)
            d_new, d_old = str(e.get("date_added", "")), m["date_added"]
            if d_new and (not d_old or d_new < d_old):
                m["date_added"] = d_new
            m["fixed_in"] = m.get("fixed_in") or e.get("fixed_in")
            m["note"] = m.get("note") or e.get("note")
        else:
            merged[k] = {
                "page": e.get("page", ""),
                "line": str(e.get("line", "")).strip(),
                "read": str(e.get("read", "")).strip(),
                "instead": str(e.get("instead", "")).strip(),
                "found_by": as_list(e.get("found_by")),
                "date_added": str(e.get("date_added", "")).strip(),
                "fixed_in": e.get("fixed_in"),
                "note": e.get("note"),
            }

    def page_key(e):
        p = e["page"]
        try:
            return (0, int(p))
        except (TypeError, ValueError):
            return (1, str(p))

    entries = sorted(merged.values(),
                     key=lambda e: (page_key(e), line_sort_key(e["line"])))
    return work, entries


def changelog_versions(changelog: Path):
    """Map version string -> date string from CHANGELOG.md '## [x.y.z] - YYYY-MM-DD'."""
    if not changelog.exists():
        return {}
    out = {}
    for m in re.finditer(r"^##\s*\[([^\]]+)\]\s*(?:-\s*(\S+))?",
                         changelog.read_text(encoding="utf-8"), re.M):
        out[m.group(1)] = m.group(2) or ""
    return out


def changelog_hints(changelog: Path, book_dir: str):
    """Changelog lines mentioning this book AND a correction keyword."""
    if not changelog.exists():
        return []
    hits = []
    for ln in changelog.read_text(encoding="utf-8").splitlines():
        low = ln.lower()
        if book_dir.lower() in low and any(k in low for k in CORRECTION_KEYWORDS):
            hits.append(ln.strip("- ").strip())
    return hits


def md_cell(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ")


def render_book(work, entries, versions, book_dir):
    n = len(entries)
    fixed = sum(1 for e in entries if e.get("fixed_in"))
    openc = n - fixed
    lines = [
        f"# Errata — {work}",
        "",
        "_Auto-generated from [`errata.yml`](errata.yml) by "
        "[`scripts/build_errata.py`](../scripts/build_errata.py). "
        "Do not edit this file by hand — edit `errata.yml` and re-run `npm run errata`._",
        "",
        f"_Generated: {ddmmyyyy(TODAY)} · {n} errata "
        f"({openc} open · {fixed} fixed in the digital edition)_",
        "",
        "**read** = the correct form · **instead of** = what the print shows. "
        "Line refs use the sources' Russian shorthand: `св.` = from the top "
        "(сверху), `сн.` = from the bottom (снизу).",
        "",
        "| # | Page | Line | Read | Instead of | Found by | Added | Status |",
        "|--:|--:|--|--|--|--|--|--|",
    ]
    for i, e in enumerate(entries, 1):
        fx = e.get("fixed_in")
        if fx:
            dt = versions.get(str(fx).lstrip("v"), versions.get(str(fx), ""))
            status = f"✓ fixed in {fx}" + (f" ({dt})" if dt else "")
        else:
            status = "open"
        found = md_cell("; ".join(e["found_by"]))
        row = (f"| {i} | {md_cell(str(e['page']))} | {md_cell(e['line'])} | "
               f"{md_cell(e['read'])} | {md_cell(e['instead'])} | {found} | "
               f"{md_cell(e['date_added'])} | {status} |")
        lines.append(row)
        if e.get("note"):
            lines.append(f"| | | | | | | | _{md_cell(str(e['note']))}_ |")

    hints = changelog_hints(ROOT / "CHANGELOG.md", book_dir)
    if hints:
        lines += ["", "> **CHANGELOG mentions a correction to this book** — if an "
                  "erratum below was fixed in the source, set its `fixed_in` in "
                  "`errata.yml`:"]
        lines += [f"> - {md_cell(h)}" for h in hints]

    lines += ["", f"_Auto-generated by [`scripts/build_errata.py`]"
              f"(../scripts/build_errata.py) on {ddmmyyyy(TODAY)}._", ""]
    return "\n".join(lines), n, openc, fixed


def render_index(rows):
    lines = [
        "# Errata index",
        "",
        "_Auto-generated by [`scripts/build_errata.py`](scripts/build_errata.py). "
        "Do not edit by hand._",
        "",
        f"_Generated: {ddmmyyyy(TODAY)}_",
        "",
        "Per-book errata lists — printed-page corrections gathered from the "
        "editions' own errata sheets and later readers, each row tagged with who "
        "found it and when it entered this list.",
        "",
        "| Book | Errata | Open | Fixed |",
        "|--|--:|--:|--:|",
    ]
    for book, n, openc, fixed in rows:
        lines.append(f"| [{book}]({book}/ERRATA.md) | {n} | {openc} | {fixed} |")
    lines += ["", f"_Auto-generated by [`scripts/build_errata.py`]"
              f"(scripts/build_errata.py) on {ddmmyyyy(TODAY)}._", ""]
    return "\n".join(lines)


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg:
        ymls = [ROOT / arg / "errata.yml"]
        if not ymls[0].exists():
            sys.exit(f"No errata.yml in {arg}")
    else:
        ymls = sorted(ROOT.glob("*/errata.yml"))
        if not ymls:
            sys.exit("No */errata.yml found.")

    versions = changelog_versions(ROOT / "CHANGELOG.md")
    index_rows = []
    for yml in ymls:
        book_dir = yml.parent.name
        work, entries = load_book(yml)
        md, n, openc, fixed = render_book(work, entries, versions, book_dir)
        (yml.parent / "ERRATA.md").write_text(md, encoding="utf-8")
        index_rows.append((book_dir, n, openc, fixed))
        print(f"  {book_dir}: {n} errata ({openc} open, {fixed} fixed) -> "
              f"{book_dir}/ERRATA.md")

    # Refresh the root index over every book that currently has an errata.yml.
    all_rows = []
    for yml in sorted(ROOT.glob("*/errata.yml")):
        work, entries = load_book(yml)
        fixed = sum(1 for e in entries if e.get("fixed_in"))
        all_rows.append((yml.parent.name, len(entries), len(entries) - fixed, fixed))
    (ROOT / "ERRATA.md").write_text(render_index(all_rows), encoding="utf-8")
    print(f"  index -> ERRATA.md ({len(all_rows)} book(s))")


if __name__ == "__main__":
    main()
