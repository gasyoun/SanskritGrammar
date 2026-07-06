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

Two ways errata get INTO a book's errata.yml:
  A. transcribe a printed errata/opechatki sheet (e.g. Knauer's 1908 + 2011/2015/2023 sheets);
  B. **edition diff** — for a book with no printed errata sheet (e.g. Kochergina), compare two
     versions of the book's own text file over time. Every folder has an errata.yml, seeded
     empty, and future edits become errata by diffing old vs new. Run:
         python scripts/build_errata.py diff <Book> <old-git-ref> [<new-git-ref>]
     which writes <Book>/errata.candidates.yml (read=new text, instead=old text, tagged with
     the diff + today's date) for a human to review and fold into errata.yml.

Usage:
    python scripts/build_errata.py                         # regenerate all books
    python scripts/build_errata.py KnauerFrazy_1908        # regenerate one book
    python scripts/build_errata.py diff KocherginaUchebnik_1998 HEAD~1   # edition-diff candidates
"""

import sys
import re
import difflib
import datetime
import subprocess
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
    header = [
        f"# Errata — {work}",
        "",
        "_Auto-generated from [`errata.yml`](errata.yml) by "
        "[`scripts/build_errata.py`](../scripts/build_errata.py). "
        "Do not edit this file by hand — edit `errata.yml` and re-run `npm run errata`._",
        "",
    ]
    if n == 0:
        body = [
            f"_Generated: {ddmmyyyy(TODAY)} · no errata recorded yet._",
            "",
            "No corrections have been catalogued for this book yet. Two ways to add them:",
            "",
            "- **A printed errata/opechatki sheet** — transcribe it into "
            "[`errata.yml`](errata.yml) (`/errata` skill, Phase 1).",
            "- **Edition diff** — when this book's text file changes, compare the old and new "
            "versions to surface corrections:",
            "  ```",
            f"  python scripts/build_errata.py diff {book_dir} <old-git-ref> [<new-git-ref>]",
            "  ```",
            "  Review the emitted `errata.candidates.yml` and fold real corrections into "
            "`errata.yml`.",
            "",
            f"_Auto-generated by [`scripts/build_errata.py`](../scripts/build_errata.py) "
            f"on {ddmmyyyy(TODAY)}._",
            "",
        ]
        return "\n".join(header + body), 0, 0, 0
    lines = header + [
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


def book_text_file(book_dir: str):
    """The book's canonical human-readable text file (the .mdx, else a .md), not ERRATA.md."""
    d = ROOT / book_dir
    cands = sorted(d.glob("*.mdx")) or sorted(
        p for p in d.glob("*.md") if p.name.upper() != "ERRATA.MD")
    return cands[0] if cands else None


def git_show(ref: str, relpath: str):
    r = subprocess.run(["git", "show", f"{ref}:{relpath}"], cwd=ROOT,
                       capture_output=True, encoding="utf-8")
    return r.stdout if r.returncode == 0 else None


def diff_candidates(book_dir: str, old_ref: str, new_ref: str = None):
    """Emit <Book>/errata.candidates.yml from a text diff of two editions of the book file."""
    f = book_text_file(book_dir)
    if not f:
        sys.exit(f"No .mdx/.md text file found in {book_dir} to diff.")
    rel = f.relative_to(ROOT).as_posix()
    old = git_show(old_ref, rel)
    if old is None:
        sys.exit(f"Could not read {rel} at {old_ref} (git show failed).")
    new = git_show(new_ref, rel) if new_ref else f.read_text(encoding="utf-8")
    if new is None:
        sys.exit(f"Could not read {rel} at {new_ref} (git show failed).")

    old_lines, new_lines = old.splitlines(), new.splitlines()
    sm = difflib.SequenceMatcher(a=old_lines, b=new_lines, autojunk=False)
    src = f"edition diff {old_ref}→{new_ref or 'working tree'}"
    cands = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "replace":
            continue  # pure insertions/deletions are structural, not typo corrections
        a, b = old_lines[i1:i2], new_lines[j1:j2]
        for k in range(max(len(a), len(b))):
            was = a[k].strip() if k < len(a) else ""
            now = b[k].strip() if k < len(b) else ""
            if was == now or not (was and now):
                continue
            cands.append({"page": "", "line": "", "read": now, "instead": was,
                          "found_by": src, "date_added": str(TODAY),
                          "note": "auto-detected edition change — review before folding in"})

    out = ROOT / book_dir / "errata.candidates.yml"
    payload = ("# AUTO-GENERATED candidate errata from an edition diff — REVIEW, do not ship as-is.\n"
               f"# Source: {src} · file: {rel} · {ddmmyyyy(TODAY)}\n"
               "# Move genuine corrections into errata.yml (add page/line), then delete this file.\n\n")
    if cands:
        payload += yaml.safe_dump({"candidates": cands}, allow_unicode=True,
                                  sort_keys=False, width=1000)
    else:
        payload += "candidates: []   # no line-level text replacements detected\n"
    out.write_text(payload, encoding="utf-8")
    print(f"  {book_dir}: {len(cands)} candidate erratum/errata from {src}")
    print(f"  -> {book_dir}/errata.candidates.yml  (review, then fold into errata.yml)")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "diff":
        if len(sys.argv) < 4:
            sys.exit("usage: build_errata.py diff <Book> <old-git-ref> [<new-git-ref>]")
        diff_candidates(sys.argv[2], sys.argv[3],
                        sys.argv[4] if len(sys.argv) > 4 else None)
        return

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
