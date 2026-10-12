#!/usr/bin/env python
"""H6456 / WHEEL6 pilot — Process-Sanskrit (DCS-word2vec-scored splits) vs our
induced sandhi rules (sandhi-scaffold family), on the Bhagavadgītā sandhi gold.

Bench: junction items derived from DCS CoNLL-U (dcs-conllu/files, texts
Aṣṭāvakragīta + Gītagovinda — the machine-verifiable gold of the kosha
sandhi-scaffold programme; every token carries the sandhied FORM and the
pre-sandhi `Unsandhied=`). Two item families, mirroring
kosha/scripts/dcs_sandhi_induce.py modes 1/2:
  edge — adjacent tokens whose facing edge changed: joined = FORM_i+FORM_{i+1}
  MWT  — coalesced multi-word-token surface over exactly 2 components.

Systems compared (same items, same metric):
  ours   — rule-lookup splitter over the induced/hand rule tables
           (gita_sandhi.tsv + astavakragita_sandhi.tsv, `X Y → Z` schema):
           every rule whose surface form Z occurs in the joined string yields a
           candidate split; candidates ranked by corpus frequency mass.
  upstream — Process-Sanskrit 1.5.2 vendored sanskrit_parser splitter
           (pip install process-sanskrit; DCS word2vec model bundled as
           splitter/data/w2v.npz), top-ranked split.

Metrics: exact-2 junction accuracy, first-token agreement, mean ms/item.

Usage:
  <venv-with-process-sanskrit>/bin/python scripts/pilot_process_sanskrit_vs_rules.py \
      [--n 250] [--seed 42] [--out reports/...]

Public/MIT, credit Dr. Mārcis Gasūns. Data inputs read-only (kosha + this repo).
"""
import argparse
import csv
import json
import random
import sys
import time
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
KOSHA = Path.home() / "Documents/GitHub/kosha"
DCS_FILES = Path.home() / "Documents/GitHub/dcs-conllu/files"
DCS_TEXTS = ["Aṣṭāvakragīta", "Gītagovinda"]
RULE_TABLES = [
    KOSHA / "data/gita/gita_sandhi.tsv",
    KOSHA / "data/sandhi/astavakragita_sandhi.tsv",
]

OK_CHARS = set("aāiīuūṛṝḷḹeaioueo'ṃṁḥkgcjṭḍtdpbphśṣsyrlvñm-")


def nfc(s):
    return unicodedata.normalize("NFC", s or "")


def canon(s):
    """Comparison canonical: NFC + anusvāra variants (ṃ/ṁ) unified to m."""
    return nfc(s).replace("ṃ", "m").replace("ṁ", "m").lower()


def load_rules():
    """Induced/hand rule tables (kosha sandhi-scaffold family): `X Y → Z`."""
    rules = {}
    for path in RULE_TABLES:
        if not path.exists():
            continue
        with open(path, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                rule = nfc(row.get("rule", "")).strip()
                if "→" not in rule:
                    continue
                try:
                    lhs, surface = rule.split("→")
                    left, right = lhs.split()
                    left, right, surface = left.strip(), right.strip(), surface.strip()
                except ValueError:
                    continue
                count = int(row.get("count", "0") or 0)
                key = (left, right, surface)
                rules[key] = rules.get(key, 0) + max(count, 1)
    return rules


def _clean_word(w):
    return nfc(w).strip().strip("|/.,;:!?'\"()")


def build_bench(n, seed):
    items = []
    for text in DCS_TEXTS:
        tdir = DCS_FILES / text
        if not tdir.is_dir():
            continue
        for path in sorted(tdir.glob("*.conllu")):
            lines = path.read_text(encoding="utf-8").splitlines()
            i = 0
            while i < len(lines):
                line = lines[i]
                if not line or line.startswith("#"):
                    i += 1
                    continue
                cols = line.split("\t")
                if len(cols) >= 2 and "-" in cols[0]:  # MWT range line
                    comps = []
                    j = i + 1
                    while j < len(lines) and lines[j]:
                        c = lines[j].split("\t")
                        if len(c) < 10 or "-" in c[0] or "." in c[0]:
                            break
                        misc = dict(kv.split("=", 1) for kv in c[9].split("|") if "=" in kv)
                        comps.append(_clean_word(misc.get("Unsandhied", "")))
                        j += 1
                    joined = _clean_word(cols[1])
                    if (len(comps) == 2 and all(comps)
                            and all(set(w) <= OK_CHARS and len(w) >= 2 for w in comps)
                            and joined and set(joined) <= OK_CHARS and len(joined) <= 28):
                        items.append({"text": text, "family": "mwt",
                                      "joined": joined, "gold": comps})
                    i = j
                    continue
                if len(cols) >= 10:  # regular token — check edge sandhi with next
                    if i + 1 < len(lines) and lines[i + 1]:
                        nxt = lines[i + 1].split("\t")
                        if len(nxt) >= 10 and "-" not in nxt[0] and "." not in nxt[0]:
                            m = dict(kv.split("=", 1) for kv in cols[9].split("|") if "=" in kv)
                            m2 = dict(kv.split("=", 1) for kv in nxt[9].split("|") if "=" in kv)
                            f1, u1 = _clean_word(cols[1]), _clean_word(m.get("Unsandhied", ""))
                            f2 = _clean_word(nxt[1])
                            if (f1 and f2 and u1 and f1 != u1
                                    and set(f1) <= OK_CHARS and set(f2) <= OK_CHARS
                                    and len(f1) >= 2 and len(f2) >= 2
                                    and len(f1 + f2) <= 28):
                                items.append({"text": text, "family": "edge",
                                              "joined": f1 + f2, "gold": [f1, f2]})
                    i += 1
                    continue
                i += 1
    # dedupe by joined (keep first)
    seen, uniq = set(), []
    for it in items:
        if it["joined"] not in seen:
            seen.add(it["joined"])
            uniq.append(it)
    rng = random.Random(seed)
    rng.shuffle(uniq)
    return uniq[:n]


def ours_split(joined, rules):
    """Rule-lookup splitter: surface-form occurrence + frequency ranking."""
    cands = {}
    for (left, right, surface), count in rules.items():
        start = 0
        while True:
            i = joined.find(surface, start)
            if i < 0:
                break
            cand = (joined[:i] + left, right + joined[i + len(surface):])
            if all(cand) and cand != (joined, ""):
                cur = cands.get(cand)
                if cur is None or count > cur:
                    cands[cand] = count
            start = i + 1
    if not cands:
        return [(joined,)], 0
    best = max(cands, key=cands.get)
    return [best], cands[best]


def upstream_split(parser, joined):
    from indic_transliteration import sanscript
    splits = parser.split(joined, limit=5)
    if not splits:
        return None
    top = splits[0].split
    return [sanscript.transliterate(o.canonical(), sanscript.SLP1, sanscript.IAST)
            for o in top]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=250)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default=str(ROOT / "reports" / "h6456_pilot_metrics.json"))
    args = ap.parse_args()

    rules = load_rules()
    bench = build_bench(args.n, args.seed)
    print(f"rules loaded: {len(rules)}; bench items: {len(bench)}")

    from process_sanskrit.splitter import Parser
    parser = Parser()

    res = {"ours": {"exact": 0, "first": 0, "t": 0.0, "errs": 0},
           "upstream": {"exact": 0, "first": 0, "t": 0.0, "errs": 0, "none": 0}}
    examples = {"ours": [], "upstream": []}
    rows = []

    for k, item in enumerate(bench):
        gold = tuple(canon(w) for w in item["gold"])
        # ours
        t0 = time.perf_counter()
        try:
            pred, score = ours_split(item["joined"], rules)
            pred0 = tuple(canon(w) for w in pred[0])
            ok = pred0 == gold
            okf = pred0[:1] == gold[:1]
        except Exception:
            pred0, ok, okf, score = None, False, False, 0
            res["ours"]["errs"] += 1
        res["ours"]["t"] += time.perf_counter() - t0
        res["ours"]["exact"] += ok
        res["ours"]["first"] += okf
        if not ok and len(examples["ours"]) < 5:
            examples["ours"].append({"joined": item["joined"], "gold": list(gold),
                                     "pred": list(pred0) if pred0 else None})
        # upstream
        t0 = time.perf_counter()
        try:
            up = upstream_split(parser, item["joined"])
            if up is None:
                res["upstream"]["none"] += 1
                upok = upokf = False
                up0 = None
            else:
                up0 = tuple(canon(w) for w in up)
                upok = up0 == gold
                upokf = up0[:1] == gold[:1]
        except Exception:
            up0, upok, upokf = None, False, False
            res["upstream"]["errs"] += 1
        res["upstream"]["t"] += time.perf_counter() - t0
        res["upstream"]["exact"] += upok
        res["upstream"]["first"] += upokf
        if not upok and len(examples["upstream"]) < 5:
            examples["upstream"].append({"joined": item["joined"], "gold": list(gold),
                                         "pred": list(up0) if up0 else None})
        rows.append({"text": item["text"], "family": item["family"],
                     "joined": item["joined"],
                     "gold": item["gold"], "ours_ok": ok, "upstream_ok": upok})
        if (k + 1) % 25 == 0:
            print(f"  {k+1}/{len(bench)} done — ours {res['ours']['exact']}, "
                  f"upstream {res['upstream']['exact']}", flush=True)

    n = len(bench)
    summary = {
        "n_items": n,
        "seed": args.seed,
        "n_rules": len(rules),
        "rule_tables": [str(p) for p in RULE_TABLES],
        "gold_source": f"DCS CoNLL-U: {DCS_FILES} texts={DCS_TEXTS}",
        "upstream_desc": "Process-Sanskrit 1.5.2 (vendored sanskrit_parser + DCS word2vec, bundled w2v.npz)",
        "ours": {
            "exact_acc": round(res["ours"]["exact"] / n, 4),
            "first_tok_acc": round(res["ours"]["first"] / n, 4),
            "mean_ms_per_item": round(res["ours"]["t"] / n * 1000, 1),
            "errors": res["ours"]["errs"],
        },
        "upstream": {
            "exact_acc": round(res["upstream"]["exact"] / n, 4),
            "first_tok_acc": round(res["upstream"]["first"] / n, 4),
            "mean_ms_per_item": round(res["upstream"]["t"] / n * 1000, 1),
            "errors": res["upstream"]["errs"],
            "no_split_found": res["upstream"]["none"],
        },
        "examples_of_misses": examples,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"summary": summary, "per_item": rows},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
