#!/usr/bin/env python3
"""Witness-grid pipeline for WHITNEY_CONCORDANCE_SANGRAM_KOCHERGINA_2026.md.

The proven H1242 conveyor (v2: Buhler 1923 + Zalizniak 1975/1978/2004), generalised
so the next witness pass (H1243: Wackernagel + Renou, PDF-gated; later SG-SE-006+
re-passes) is mechanical:

  extract  — parse the report's §4/§5 tables into a keyed claims JSON
             (tolerates any number of already-merged witness columns);
  batch    — emit per-chunk TSV batch files (KEY<TAB>CLAIM[<TAB>HINT]) for
             witness-adjudication agents (prompt contract:
             concordance_witness_agent_prompt_RU.md next to this script);
  merge    — insert ONE new witness column (VERDICT · locus) before the trailing
             Примечание column of both tables from a per-source verdict TSV
             (KEY<TAB>VERDICT<TAB>LOCUS<TAB>NOTE), validating full key coverage
             and the AGREE/DISAGREE/SILENT vocabulary.

Verdict semantics, the passage-reading rule, and locus formats live in the prompt
template; this script only moves data. Summary tables (§1) and synthesis sections
(§§6-7) stay authored judgment - not generated here.

Usage:
  python scripts/concordance_witness_grid.py extract --report WHITNEY_CONCORDANCE_SANGRAM_KOCHERGINA_2026.md --out /tmp/claims.json
  python scripts/concordance_witness_grid.py batch   --claims /tmp/claims.json --outdir /tmp/batches
  python scripts/concordance_witness_grid.py merge   --report ... --tsv witness_wack.tsv --header "В-1896" [--dry-run]
"""
import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

VALID = {"AGREE", "DISAGREE", "SILENT"}


def split_row(line):
    """Cells of a markdown table row, honouring escaped \\| pipes."""
    parts = re.split(r"(?<!\\)\|", line.strip())
    return [c.strip() for c in parts[1:-1]]


def join_row(cells):
    return "| " + " | ".join(cells) + " |"


def section_bounds(lines):
    s4 = next(i for i, l in enumerate(lines) if l.startswith("## 4."))
    s5 = next(i for i, l in enumerate(lines) if l.startswith("## 5."))
    s6 = next(i for i, l in enumerate(lines) if l.startswith("## 6."))
    return s4, s5, s6


def iter_claim_rows(lines):
    """Yield (index, kind) for every data row of §4 ('article') and §5 ('hk')."""
    s4, s5, s6 = section_bounds(lines)
    for i in range(s4, s6):
        if lines[i].startswith("| ["):
            yield i, ("article" if i < s5 else "hk")


def cmd_extract(args):
    lines = Path(args.report).read_text(encoding="utf-8").splitlines()
    claims = []
    for i, kind in iter_claim_rows(lines):
        cells = split_row(lines[i])
        key = re.match(r"\[([^\]]+)\]", cells[0]).group(1)
        if kind == "article":
            claim, hint = cells[1], ""
        else:
            claim, hint = cells[2], cells[1]
        claims.append({"key": key, "kind": kind, "mdline": i + 1,
                       "claim": claim, "hint": hint})
    dupes = [k for k, n in Counter(c["key"] for c in claims).items() if n > 1]
    if dupes:
        sys.exit(f"duplicate keys: {dupes}")
    Path(args.out).write_text(json.dumps(claims, ensure_ascii=False, indent=1),
                              encoding="utf-8")
    n_art = sum(1 for c in claims if c["kind"] == "article")
    print(f"extracted {len(claims)} claims ({n_art} article + {len(claims) - n_art} hk) -> {args.out}")


def cmd_batch(args):
    claims = json.loads(Path(args.claims).read_text(encoding="utf-8"))
    art = [c for c in claims if c["kind"] == "article"]
    hk = [c for c in claims if c["kind"] == "hk"]
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    def emit(rows, prefix, size):
        n = max(1, math.ceil(len(rows) / size))
        per = math.ceil(len(rows) / n)
        for i in range(n):
            chunk = rows[i * per:(i + 1) * per]
            p = outdir / f"batch_{prefix}{i + 1}.tsv"
            p.write_text("\n".join(f"{c['key']}\t{c['claim']}\t{c['hint']}"
                                   for c in chunk) + "\n", encoding="utf-8")
            print(f"{p.name}: {len(chunk)} rows")

    emit(art, "A", args.article_chunk)
    emit(hk, "K", args.hk_chunk)


def cmd_merge(args):
    verdicts = {}
    for line in Path(args.tsv).read_text(encoding="utf-8-sig").splitlines():
        if not line.strip() or line.startswith("key\t"):
            continue
        cells = line.split("\t")
        if len(cells) < 3:
            sys.exit(f"bad TSV line: {line[:80]!r}")
        key, verdict, locus = cells[0].strip(), cells[1].strip(), cells[2].strip()
        if verdict not in VALID:
            sys.exit(f"bad verdict {verdict!r} for {key}")
        verdicts[key] = (verdict, locus)

    path = Path(args.report)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    stats = Counter()
    seen = set()
    for i, kind in iter_claim_rows(lines):
        cells = split_row(lines[i])
        key = re.match(r"\[([^\]]+)\]", cells[0]).group(1)
        if key not in verdicts:
            sys.exit(f"TSV missing key {key}")
        v, locus = verdicts[key]
        cell = "SILENT" if v == "SILENT" else f"{v} · {locus.replace('|', chr(92) + '|')}"
        lines[i] = join_row(cells[:-1] + [cell] + [cells[-1]])
        stats[v] += 1
        seen.add(key)
    extra = set(verdicts) - seen
    if extra:
        sys.exit(f"TSV keys not in report: {sorted(extra)[:5]} ({len(extra)})")

    # widen header + separator rows of both tables by one column
    s4, s5, s6 = section_bounds(lines)
    for i in range(s4, s6):
        l = lines[i]
        if l.startswith("| Источник") or l.startswith("| ID"):
            cells = split_row(l)
            lines[i] = join_row(cells[:-1] + [args.header] + [cells[-1]])
        elif l.startswith("|") and set(l.replace("|", "").replace("-", "").strip()) == set():
            lines[i] = "|" + "---|" * (l.count("|") - 1 + 1)

    print(f"{args.header}: {dict(stats)} over {len(seen)} rows")
    if args.dry_run:
        print("dry-run: report not written")
        return
    path.write_text("\n".join(lines) + ("\n" if text.endswith("\n") else ""),
                    encoding="utf-8", newline="\n")
    print(f"merged column into {path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("extract")
    e.add_argument("--report", required=True)
    e.add_argument("--out", required=True)
    e.set_defaults(fn=cmd_extract)

    b = sub.add_parser("batch")
    b.add_argument("--claims", required=True)
    b.add_argument("--outdir", required=True)
    b.add_argument("--article-chunk", type=int, default=58)
    b.add_argument("--hk-chunk", type=int, default=65)
    b.set_defaults(fn=cmd_batch)

    m = sub.add_parser("merge")
    m.add_argument("--report", required=True)
    m.add_argument("--tsv", required=True)
    m.add_argument("--header", required=True)
    m.add_argument("--dry-run", action="store_true")
    m.set_defaults(fn=cmd_merge)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
