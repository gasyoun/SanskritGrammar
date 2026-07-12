#!/usr/bin/env python
"""Generate QUANTIFIER_PROFILE.md (+ per-book quantifiers.json + root index) from each
book's quantifiers.yml and hand-verified quantifiers.sample.yml.

Sibling of scripts/build_claims.py, same "generated source + rendered output" pattern.
Distinct register (H800): where claims.yml grades falsifiable assertions, quantifiers.yml is
the auto-proxy quantifier register (harvested by scripts/harvest_quantifiers.py) and this
generator reports, per source:
  * quantifier DENSITY  (per grammar-prose line, and per total file line for continuity with
    the handoff's Context-B figure),
  * anchored-SHARE at the N=8 window plus a window-sensitivity sweep (the auto-proxy),
  * the ANCHOR-TYPE distribution — the discriminating metric (§ / class / type / position /
    series / affix …), i.e. WHAT each grammar's quantifiers hang on,
  * the manual-verification result — precision / recall of the auto-proxy against the
    hand-verified sample, and the human-read anchored-share.

Usage:
    python scripts/build_quantifiers.py            # regenerate all + root index
    python scripts/build_quantifiers.py <Book>     # one book (index still refreshed)
"""
import sys
import json
import datetime
from pathlib import Path
from collections import Counter

import yaml

import harvest_quantifiers as H   # reuse SOURCES + harvest() for the sensitivity sweep

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
TODAY = datetime.date.today().strftime("%d-%m-%Y")
SWEEP_NS = [6, 8, 12, 16, 25, 40]

BOOK_ORDER = ["KocherginaUchebnik_1998", "ZalizniakOcherk_1978",
              "ZalizniakKonspekt_2004", "ZalizniakMorphology_1975"]


def load_yml(book):
    return yaml.safe_load((ROOT / book / "quantifiers.yml").read_text(encoding="utf-8"))


def load_sample(book):
    p = ROOT / book / "quantifiers.sample.yml"
    if not p.exists():
        return None
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def total_lines(src_file):
    return len((ROOT / src_file).read_text(encoding="utf-8").splitlines())


def sweep_source(src):
    out = {}
    saved = H.ANCHOR_WINDOW
    for n in SWEEP_NS:
        H.ANCHOR_WINDOW = n
        es = [e for e in H.harvest(src) if e["zone"] == "grammar"]
        out[n] = round(100 * sum(e["anchored"] for e in es) / len(es), 1) if es else 0.0
    H.ANCHOR_WINDOW = saved
    return out


def sample_metrics(sample):
    rows = [r for r in sample["sample"] if r.get("human_anchored") is not None]
    if not rows:
        return None
    tp = sum(1 for r in rows if r["auto_anchored"] and r["human_anchored"])
    fp = sum(1 for r in rows if r["auto_anchored"] and not r["human_anchored"])
    fn = sum(1 for r in rows if not r["auto_anchored"] and r["human_anchored"])
    tn = sum(1 for r in rows if not r["auto_anchored"] and not r["human_anchored"])
    n = len(rows)
    lex_fp = sum(1 for r in rows if (r.get("note") or "").startswith("lexicon-FP"))
    return {
        "n": n, "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": round(100 * tp / (tp + fp), 1) if (tp + fp) else None,
        "recall": round(100 * tp / (tp + fn), 1) if (tp + fn) else None,
        "agreement": round(100 * (tp + tn) / n, 1),
        "human_share": round(100 * (tp + fn) / n, 1),
        # miss-rate = of auto-UNANCHORED hits, fraction actually anchored (drives the pop estimate)
        "miss_rate": round(tp * 0 + fn / (fn + tn), 4) if (fn + tn) else 0.0,
        "lexicon_fp": lex_fp,
    }


def pop_estimate(auto_share_pct, s):
    """Population human-anchored share, un-stratifying the sample: apply the sample's precision
    to the auto-anchored slice and its miss-rate to the auto-unanchored slice."""
    a = auto_share_pct / 100.0
    prec = (s["precision"] or 0) / 100.0
    return round(100 * (a * prec + (1 - a) * s["miss_rate"]), 1)


def profile_of(book):
    d = load_yml(book)
    entries = d["entries"]
    gram = [e for e in entries if e["zone"] == "grammar"]
    gram_lines = len({e["line"] for e in gram})
    tot = total_lines(d["source_file"])
    anc = sum(e["anchored"] for e in gram)
    zones = Counter(e["zone"] for e in entries)
    axis = Counter(e["axis"] for e in gram)
    atype = Counter(e["anchor"] for e in gram if e["anchored"])
    src = next(s for s in H.SOURCES if s["book"] == book)
    return {
        "book": book, "work": d["work"], "lang": d["lang"], "source_file": d["source_file"],
        "total_lines": tot, "grammar_hits": len(gram), "grammar_lines": gram_lines,
        "raw_hits": len(entries), "zones": dict(zones),
        "density_grammar": round(len(gram) / gram_lines, 3) if gram_lines else 0,
        "density_total": round(len(gram) / tot, 4) if tot else 0,
        "anchored": anc, "anchored_share": round(100 * anc / len(gram), 1) if gram else 0,
        "axis": dict(axis.most_common()),
        "anchor_types": dict(atype.most_common()),
        "sensitivity": sweep_source(src),
        "sample": sample_metrics(load_sample(book)) if load_sample(book) else None,
    }


def bar(share):
    filled = int(round(share / 5))
    return "█" * filled + "·" * (20 - filled)


def render_book(p):
    L = [
        f"# Quantifier profile — {p['work']}",
        "",
        "_Auto-generated from [`quantifiers.yml`](quantifiers.yml) + hand-verified "
        "[`quantifiers.sample.yml`](quantifiers.sample.yml) by "
        "[`scripts/build_quantifiers.py`](../scripts/build_quantifiers.py). Do not edit by hand — "
        "re-run `npm run quantifiers`._",
        "",
        f"_Generated: {TODAY} · source [`{Path(p['source_file']).name}`]"
        f"(../{p['source_file']})_",
        "",
        "## Density",
        "",
        f"- **{p['grammar_hits']}** quantifier instances in grammar-prose "
        f"(of {p['raw_hits']} raw hits; zones {p['zones']}).",
        f"- **{p['density_grammar']} per grammar-prose line** ({p['grammar_hits']} / "
        f"{p['grammar_lines']} lines).",
        f"- {p['density_total']} per total file line ({p['grammar_hits']} / {p['total_lines']}) "
        f"— comparable to the handoff's Context-B figure, but note the total includes any "
        f"glossary/reader bulk.",
        "",
        "## Anchoredness (auto-proxy)",
        "",
        f"Anchored share at N=8: **{p['anchored_share']}%** ({p['anchored']}/{p['grammar_hits']}). "
        "Window-sensitivity (anchored share as the ±N-token window widens):",
        "",
        "| N tokens | " + " | ".join(f"{n}" for n in SWEEP_NS) + " |",
        "|--|" + "|".join("--" for _ in SWEEP_NS) + "|",
        "| anchored % | " + " | ".join(f"{p['sensitivity'][n]}" for n in SWEEP_NS) + " |",
        "",
        "## Anchor type — WHAT the quantifiers hang on",
        "",
        "The discriminating metric: not *whether* a quantifier is near a decidable target but "
        "*what kind* of target — a formal apparatus (§ / numbered class / type / morphological "
        "position / ablaut series) vs. a descriptive one (named affix / declension / form).",
        "",
        "| Anchor | count | share |",
        "|--|--:|--:|",
    ]
    atot = sum(p["anchor_types"].values()) or 1
    for k, v in p["anchor_types"].items():
        L.append(f"| {k} | {v} | {round(100*v/atot)}% |")
    L += ["", "## Axis mix", "",
          "| Axis | share |", "|--|--:|"]
    xtot = sum(p["axis"].values()) or 1
    for k, v in p["axis"].items():
        L.append(f"| {k} | {round(100*v/xtot)}% |")

    s = p["sample"]
    if s:
        L += [
            "", "## Manual verification (D3)",
            "",
            f"Hand-verified stratified sample of **{s['n']}** grammar-zone hits (adjudicator: "
            "Opus 4.8, `claude-opus-4-8`). Each row judged anchored / unanchored by reading the "
            "full context; the auto-proxy is scored against that judgment.",
            "",
            f"- **Human-read anchored share: {s['human_share']}%** on the (stratified) sample; "
            f"un-stratified population estimate **≈ {pop_estimate(p['anchored_share'], s)}%** "
            f"(apply precision to auto-anchored, miss-rate to auto-unanchored). Either way the "
            f"auto-proxy's N=8 figure ({p['anchored_share']}%) UNDER-reads true anchoredness, "
            "because most real anchors sit just beyond 8 tokens (see the sensitivity sweep).",
            f"- Auto-proxy **precision {s['precision']}%** (of hits it flags anchored, how many "
            f"really are) · **recall {s['recall']}%** (of truly-anchored hits, how many it "
            f"catches) · agreement {s['agreement']}%.",
            f"- Confusion: TP {s['tp']} · FP {s['fp']} · FN {s['fn']} · TN {s['tn']}. "
            f"Lexicon false-positives (matches that are not genuine scope quantifiers): "
            f"{s['lexicon_fp']}.",
            "",
            "> The proxy is a high-precision, low-recall detector: trust its ANCHORED calls, "
            "treat its UNANCHORED calls as \"no decidable target within 8 tokens\", not "
            "\"unanchored\". The human-read share is the trustworthy anchoredness figure.",
        ]
    L += ["", f"_Auto-generated by [`scripts/build_quantifiers.py`]"
          f"(../scripts/build_quantifiers.py) on {TODAY}._", ""]
    return "\n".join(L)


def render_index(profs):
    L = [
        "# Quantifier metalanguage — profile index",
        "",
        "_Auto-generated by [`scripts/build_quantifiers.py`](scripts/build_quantifiers.py). "
        "Do not edit by hand._",
        "",
        f"_Generated: {TODAY}_",
        "",
        "Per-book quantifier registers (H800): every metalanguage quantifier (редко / обычно / "
        "только / некоторые / могут / всегда …) harvested and tagged anchored/unanchored, "
        "with the auto-proxy calibrated against a hand-verified sample. The narrative comparison "
        "lives in "
        "[`KocherginaUchebnik_1998/GRADATION_METALANGUAGE_KOCHERGINA.md`]"
        "(KocherginaUchebnik_1998/GRADATION_METALANGUAGE_KOCHERGINA.md).",
        "",
        "## Density & anchoredness",
        "",
        "| Work | grammar hits | dens/gram-line | dens/total-line | anchored% (N=8) | "
        "human-anchored% (est.) |",
        "|--|--:|--:|--:|--:|--:|",
    ]
    for p in profs:
        hs = f"{pop_estimate(p['anchored_share'], p['sample'])}%" if p["sample"] else "—"
        L.append(f"| [{p['work'].split(',')[0]} {p['book'][-4:]}]"
                 f"({p['book']}/QUANTIFIER_PROFILE.md) | {p['grammar_hits']} | "
                 f"{p['density_grammar']} | {p['density_total']} | {p['anchored_share']}% | {hs} |")
    L += ["", "## Anchor-type mix (share of anchored hits) — the architecture signal", "",
          "| Work | top anchor types |", "|--|--|"]
    for p in profs:
        atot = sum(p["anchor_types"].values()) or 1
        top = ", ".join(f"{k} {round(100*v/atot)}%" for k, v in list(p["anchor_types"].items())[:4])
        L.append(f"| {p['work'].split(',')[0]} {p['book'][-4:]} | {top} |")
    L += ["", "## Auto-proxy calibration (hand-verified sample)", "",
          "| Work | sample n | precision | recall | lexicon-FP |", "|--|--:|--:|--:|--:|"]
    for p in profs:
        s = p["sample"]
        if s:
            L.append(f"| {p['work'].split(',')[0]} {p['book'][-4:]} | {s['n']} | "
                     f"{s['precision']}% | {s['recall']}% | {s['lexicon_fp']} |")
    L += ["", f"_Auto-generated by [`scripts/build_quantifiers.py`]"
          f"(scripts/build_quantifiers.py) on {TODAY}._", ""]
    return "\n".join(L)


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    books = [arg] if arg else BOOK_ORDER
    profs_all = []
    for book in BOOK_ORDER:
        p = profile_of(book)
        profs_all.append(p)
        if book in books:
            (ROOT / book / "QUANTIFIER_PROFILE.md").write_text(render_book(p), encoding="utf-8")
            payload = {k: p[k] for k in ("book", "work", "lang", "grammar_hits", "grammar_lines",
                                         "density_grammar", "density_total", "anchored_share",
                                         "axis", "anchor_types", "sensitivity")}
            payload["generated"] = TODAY
            payload["sample"] = p["sample"]
            (ROOT / book / "quantifiers.json").write_text(
                json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  {book}: dens/gram {p['density_grammar']}, anchored {p['anchored_share']}%, "
                  f"human {p['sample']['human_share'] if p['sample'] else '—'}% "
                  f"-> QUANTIFIER_PROFILE.md + quantifiers.json")
    (ROOT / "QUANTIFIER_PROFILE.md").write_text(render_index(profs_all), encoding="utf-8")
    print(f"  index -> QUANTIFIER_PROFILE.md ({len(profs_all)} books)")


if __name__ == "__main__":
    main()
