#!/usr/bin/env python
"""Generate per-book CLAIMS_VERIFIED.md (and a root index) from each book's claims.yml.

Sibling of scripts/build_errata.py, same "hand-edited source + generated output" pattern:
`<Book>/claims.yml` is the structured source; `<Book>/CLAIMS_VERIFIED.md` is generated and must
never be edited by hand.

Distinct register from errata (H768): errata.yml catalogues *typos in the print*; claims.yml
catalogues *falsifiable grammatical assertions* and grades each on two axes —
`verdict_fact` (true vs. corpus + reference grammars, with the number) and `verdict_pedagogy`
(is the presentation defensible). The verified numbers come from the ground-truth triangulation
described in each book's claims.yml header (DCS corpus + Whitney + Talmud); for Kochergina the
DCS figures are reproduced by `KocherginaUchebnik_1998/verify_claims_dcs.py`.

Usage:
    python scripts/build_claims.py                         # regenerate all books
    python scripts/build_claims.py KocherginaUchebnik_1998 # regenerate one book
"""

import sys
import json
import datetime
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
TODAY = datetime.date.today()

FACT_BADGE = {
    "TRUE": "✅ TRUE",
    "OVERSTATED": "🟠 OVERSTATED",
    "FALSE": "❌ FALSE",
    "UNTESTABLE": "⚪ UNTESTABLE",
}
PED_BADGE = {
    "JUSTIFIED": "✅ justified",
    "MISLEADING": "🟠 misleading",
    "RARE-AS-CENTRAL": "🔶 rare-as-central",
    "FREQUENCY-HIDDEN": "🔶 frequency-hidden",
    "ORDER-QUESTIONABLE": "🔶 order-questionable",
}


def ddmmyyyy(d: datetime.date) -> str:
    return d.strftime("%d-%m-%Y")


def md_cell(s) -> str:
    return (str(s) if s is not None else "").replace("|", "\\|").replace("\n", " ").strip()


def norm_fact(v):
    """YAML reads unquoted TRUE/FALSE as booleans — coerce back to the verdict vocabulary."""
    if v is True:
        return "TRUE"
    if v is False:
        return "FALSE"
    return v


def load_book(yml: Path):
    data = yaml.safe_load(yml.read_text(encoding="utf-8")) or {}
    work = data.get("work", yml.parent.name)
    entries = data.get("entries", []) or []
    synthesis = (data.get("synthesis") or "").strip()
    return work, entries, synthesis


def _norm(s):
    return " ".join((s or "").split())


def load_harvest(book_dir: Path, verified):
    """Bulk harvested candidates awaiting verification (claims_harvest.yml), minus any already
    promoted into the verified register. Matched on (loc, claim text) — a single loc can carry
    several distinct claims (H797 Phase 2), so loc alone would hide unpromoted siblings."""
    hy = book_dir / "claims_harvest.yml"
    if not hy.exists():
        return []
    data = yaml.safe_load(hy.read_text(encoding="utf-8")) or {}
    pairs = [(e.get("loc"), _norm(e.get("claim_ru"))) for e in verified]

    def promoted(c):
        cl = _norm(c.get("claim_ru"))
        return any(c.get("loc") == loc and (cl in vcl or vcl in cl)
                   for loc, vcl in pairs)

    return [c for c in (data.get("candidates") or []) if not promoted(c)]


def counts(entries):
    n = len(entries)
    verdicted = sum(1 for e in entries if e.get("verdict_fact") is not None)
    flagged = sum(1 for e in entries
                  if norm_fact(e.get("verdict_fact")) in ("OVERSTATED", "FALSE")
                  or e.get("verdict_pedagogy") in
                  ("MISLEADING", "RARE-AS-CENTRAL", "FREQUENCY-HIDDEN", "ORDER-QUESTIONABLE"))
    return n, verdicted, flagged


def gives_number(c):
    """The harvest tag is per-book (`kochergina_gives_number`, `buhler_gives_number`, …) —
    accept any `*gives_number` key so the renderer stays grammar-agnostic (H797 Phase 2)."""
    return any(v for k, v in c.items() if k.endswith("gives_number"))


def render_backlog(harvest):
    """Render the harvest backlog (candidates pending verification) as its own section."""
    if not harvest:
        return []
    n = len(harvest)
    with_num = sum(1 for c in harvest if gives_number(c))
    lines = [
        "", f"## Harvest backlog — {n} candidates pending verification", "",
        f"Falsifiable assertions swept from the full textbook but not "
        f"yet verdicted. {with_num} state a number of their own (verify it); the rest give none "
        f"(add an M.G. frequency footnote where computable). As each is verified it is promoted into "
        f"the table above and removed here. Source: "
        f"[`claims_harvest.yml`](claims_harvest.yml).",
        "",
        "| Location | Claim (abridged) | Kind | Author gives №? | Falsifiable as |",
        "|--|--|--|--|--|",
    ]
    for c in harvest:
        claim = md_cell(c.get("claim_ru", ""))
        if len(claim) > 130:
            claim = claim[:127] + "…"
        gn = "yes" if gives_number(c) else "—"
        lines.append(f"| {md_cell(c.get('loc'))} | {claim} | {md_cell(c.get('kind'))} | {gn} | "
                     f"{md_cell(c.get('falsifiable_as'))} |")
    return lines


def render_book(work, entries, book_dir, synthesis="", harvest=None):
    n, verdicted, flagged = counts(entries)
    header = [
        f"# Claims verified — {work}",
        "",
        "_Auto-generated from [`claims.yml`](claims.yml) by "
        "[`scripts/build_claims.py`](../scripts/build_claims.py). "
        "Do not edit this file by hand — edit `claims.yml` and re-run `npm run claims`._",
        "",
    ]
    if n == 0:
        return "\n".join(header + [
            f"_Generated: {ddmmyyyy(TODAY)} · no claims registered yet._",
            "",
            "No verifiable assertions have been registered for this book yet. Add them to "
            "[`claims.yml`](claims.yml) (see the four seed hypotheses HK-* for the entry shape).",
            "",
        ]), 0, 0, 0, 0

    nb = len(harvest or [])
    # Point at the book's own DCS battery if it has one, else at the shared Kochergina one
    # (the corpus metrics are book-agnostic; H797 Phase 2 reuses them across grammars).
    if (ROOT / book_dir / "verify_claims_dcs.py").exists():
        battery = "[`verify_claims_dcs.py`](verify_claims_dcs.py)"
    else:
        battery = ("the shared battery [`KocherginaUchebnik_1998/verify_claims_dcs.py`]"
                   "(../KocherginaUchebnik_1998/verify_claims_dcs.py)")
    lines = header + [
        f"_Generated: {ddmmyyyy(TODAY)} · {n} verified · {flagged} flagged (overstated/false or "
        f"presentation issue) · {nb} in the harvest backlog · {n + nb} claims total_",
        "",
        "Each claim is graded on **two axes**: **fact** (true vs. the DCS corpus + Whitney 1889 + "
        "Tolchelnikov-Talmud, with the actual number) and **pedagogy** (is the *presentation* "
        f"defensible). DCS figures reproduced by {battery}.",
        "",
        "| ID | Location | Claim (abridged) | Kind | Fact | Number | Pedagogy | Ref |",
        "|--|--|--|--|--|--|--|--|",
    ]
    for e in entries:
        claim = md_cell(e.get("claim_ru", ""))
        if len(claim) > 160:
            claim = claim[:157] + "…"
        vf = norm_fact(e.get("verdict_fact"))
        fact = FACT_BADGE.get(vf, md_cell(vf or "—"))
        ped = PED_BADGE.get(e.get("verdict_pedagogy"), md_cell(e.get("verdict_pedagogy") or "—"))
        row = (f"| **{md_cell(e.get('id'))}** | {md_cell(e.get('loc'))} | {claim} | "
               f"{md_cell(e.get('kind'))} | {fact} | {md_cell(e.get('number'))} | {ped} | "
               f"{md_cell(e.get('ref'))} |")
        lines.append(row)

    if synthesis:
        lines += ["", "## Methodology synthesis — are the author's presentation principles justified?",
                  ""]
        for para in synthesis.split("\n\n"):
            para = " ".join(para.split())
            if para:
                lines += [para, ""]

    # M.G. frequency footnotes — corpus numbers added by M.G. where the author states none.
    mgf = [(e.get("id"), e.get("mg_footnote")) for e in entries if e.get("mg_footnote")]
    if mgf:
        lines += ["", "## M.G. frequency footnotes",
                  "", "_Corpus frequencies **added by M.G.** (Dr. Mārcis Gasūns) where "
                  "the author's text gives no number — scholarly apparatus over the reading "
                  "site, not part of the printed text._", ""]
        for cid, fn in mgf:
            lines.append(f"- **{md_cell(cid)}** — {md_cell(fn)} _— M.G._")

    # Per-claim notes below the table (the two-axis reasoning that a cell can't hold)
    notes = [(e.get("id"), e.get("note")) for e in entries if e.get("note")]
    if notes:
        lines += ["", "## Notes", ""]
        for cid, note in notes:
            lines.append(f"- **{md_cell(cid)}** — {md_cell(note)}")

    lines += render_backlog(harvest or [])

    lines += ["", f"_Auto-generated by [`scripts/build_claims.py`]"
              f"(../scripts/build_claims.py) on {ddmmyyyy(TODAY)}._", ""]
    return "\n".join(lines), n, verdicted, flagged, len(harvest or [])


def render_index(rows):
    lines = [
        "# Claims index",
        "",
        "_Auto-generated by [`scripts/build_claims.py`](scripts/build_claims.py). "
        "Do not edit by hand._",
        "",
        f"_Generated: {ddmmyyyy(TODAY)}_",
        "",
        "Per-book registers of *verifiable grammatical assertions* (distinct from the "
        "typo-level [errata](ERRATA.md)), each claim graded on a fact axis and a pedagogy axis.",
        "",
        "| Book | Claims | Verdicted | Flagged |",
        "|--|--:|--:|--:|",
    ]
    for book, n, verdicted, flagged in rows:
        lines.append(f"| [{book}]({book}/CLAIMS_VERIFIED.md) | {n} | {verdicted} | {flagged} |")
    lines += ["", f"_Auto-generated by [`scripts/build_claims.py`]"
              f"(scripts/build_claims.py) on {ddmmyyyy(TODAY)}._", ""]
    return "\n".join(lines)


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg:
        ymls = [ROOT / arg / "claims.yml"]
        if not ymls[0].exists():
            sys.exit(f"No claims.yml in {arg}")
    else:
        ymls = sorted(ROOT.glob("*/claims.yml"))
        if not ymls:
            sys.exit("No */claims.yml found.")

    for yml in ymls:
        book_dir = yml.parent.name
        work, entries, synthesis = load_book(yml)
        harvest = load_harvest(yml.parent, entries)
        md, n, verdicted, flagged, nb = render_book(work, entries, book_dir, synthesis, harvest)
        (yml.parent / "CLAIMS_VERIFIED.md").write_text(md, encoding="utf-8")
        # Machine-readable twin for the reading-site overlay (P4) — normalise the
        # YAML-boolean verdict_fact and keep only the fields the badge panel needs.
        payload = {
            "work": work,
            "generated": ddmmyyyy(TODAY),
            "synthesis": synthesis,
            "claims": [{
                "id": e.get("id"), "loc": e.get("loc"),
                "claim_ru": e.get("claim_ru"), "kind": e.get("kind"),
                "verdict_fact": norm_fact(e.get("verdict_fact")),
                "number": e.get("number"), "ref": e.get("ref"),
                "verdict_pedagogy": e.get("verdict_pedagogy"), "note": e.get("note"),
                "mg_footnote": e.get("mg_footnote"),
            } for e in entries],
        }
        (yml.parent / "claims.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  {book_dir}: {n} claims ({verdicted} verdicted, {flagged} flagged) -> "
              f"{book_dir}/CLAIMS_VERIFIED.md + claims.json")

    # Refresh the root index over every book that currently has a claims.yml.
    all_rows = []
    for yml in sorted(ROOT.glob("*/claims.yml")):
        work, entries, _ = load_book(yml)
        n, verdicted, flagged = counts(entries)
        all_rows.append((yml.parent.name, n, verdicted, flagged))
    (ROOT / "CLAIMS_VERIFIED.md").write_text(render_index(all_rows), encoding="utf-8")
    print(f"  index -> CLAIMS_VERIFIED.md ({len(all_rows)} book(s))")


if __name__ == "__main__":
    main()
