#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dhatu_families_lib -- read-only data layer for build_dhatu_families.py (H6256)."""
import argparse
import collections
import csv
import json
import math
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
REPORT_NAME = "DHATU_DERIVATIONAL_FAMILIES_2026-11-25.md"
BINS = [(0, 0, "0"), (1, 1, "1"), (2, 3, "2–3"), (4, 7, "4–7"),
        (8, 15, "8–15"), (16, 31, "16–31"), (32, 10**9, "32+")]
# upasargas are listed as roots in MW/m4 but as decomposition components they
# swallow thousands of prefixed compounds; excluded from ATTRIBUTION only.
UPASARGA = {"pra", "parA", "apa", "sam", "anu", "ava", "nis", "nir", "dus",
            "dur", "vi", "A", "AN", "ni", "aDi", "api", "ati", "su", "ud",
            "ut", "aBi", "prati", "pari", "upa", "a", "an"}

_S2I = {"A": "ā", "I": "ī", "U": "ū", "f": "ṛ", "F": "ṝ", "x": "ḷ", "X": "ḹ",
        "E": "ai", "O": "au", "M": "ṃ", "H": "ḥ", "K": "kh", "G": "gh",
        "N": "ṅ", "C": "ch", "J": "jh", "Y": "ñ", "w": "ṭ", "W": "ṭh",
        "q": "ḍ", "Q": "ḍh", "R": "ṇ", "T": "th", "D": "dh", "P": "ph",
        "B": "bh", "S": "ś", "z": "ṣ", "L": "ḻ"}


def iast(slp1):
    return "".join(_S2I.get(c, c) for c in slp1)


def path(root, *parts):
    return os.path.join(root, *parts)


def load_inventory(src):
    roots = {}
    p = path(src, "csl-orig", "v02", "etymology_stats", "dhatu_roots.txt")
    with open(p, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if ln and not ln.startswith("#"):
                roots[ln] = "dhatu_roots"
    prov = collections.Counter(roots.values())
    p = path(src, "csl-orig", "v02", "mw", "mw_roots.tsv")
    with open(p, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            k = (r.get("k1_slp1") or "").strip()
            if k and k not in roots:
                roots[k] = "mw_roots"
    prov.update(("mw_roots_new" for k, v in roots.items() if v == "mw_roots"))
    return roots, prov


def load_attr_roots(src):
    """Strict dhātu attribution set: MW verb_type=genuineroot minus upasargas."""
    p = path(src, "csl-orig", "v02", "mw", "mw_roots.tsv")
    out = set()
    with open(p, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r.get("verb_type") == "genuineroot":
                out.add((r.get("k1_slp1") or "").strip())
    return out - UPASARGA


def load_substantives(src):
    """MWderivations records are substantives (noun/adj/ind) by construction."""
    p = path(src, "MWderivations", "step4", "analysis2.txt")
    subs = set()
    with open(p, encoding="utf-8") as f:
        for ln in f:
            c = ln.rstrip("\n").split("\t")
            if len(c) == 8:
                subs.add(c[2])
    return subs


def collect(src, attr, subs):
    """root -> derivative -> set(source tags); (root,derivative) -> [MW L ids]."""
    fam = collections.defaultdict(lambda: collections.defaultdict(set))
    lid = collections.defaultdict(list)

    def add(root, form, tag, evidence=None):
        if root in attr and form in subs:
            fam[root][form].add(tag)
            if evidence:
                lid[(root, form)].append(str(evidence))

    # 1. MW's own explicit root attributions (parse="X+Y" / fr. √ root)
    p = path(src, "csl-orig", "v02", "mw", "mw_etymology.tsv")
    with open(p, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            add(r.get("root_slp1", ""), r.get("headword_slp1", ""),
                "mw_etymology", r.get("L_id", ""))

    # 2. cross-dictionary root oracle, MW-backed rows only
    p = path(src, "csl-orig", "v02", "etymology_stats", "root_oracle.tsv")
    with open(p, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if "mw" in (r.get("sources") or "").split(","):
                add(r.get("root_slp1", ""), r.get("form_slp1", ""), "root_oracle[mw]")

    # 3. MW derivational markers collected by MWderivations
    p = path(src, "MWderivations", "step4", "auxiliary", "deriv.txt")
    with open(p, encoding="utf-8") as f:
        for ln in f:
            c = ln.rstrip("\n").split("\t")
            if len(c) >= 3:
                for w in c[2].split():
                    add(c[1], w, "mw_deriv")

    # 4. prefixed-root derivations from MWderivations
    p = path(src, "MWderivations", "step4", "auxiliary", "pfxderiv.txt")
    with open(p, encoding="utf-8") as f:
        for ln in f:
            c = ln.rstrip("\n").split("\t")
            if len(c) >= 7:
                for w in c[6].split():
                    add(c[3], w, "mw_pfxderiv")

    # 5. structural decomposition of all MW substantives (MWderivations step4).
    # A component is assigned only on an EXACT canonical-root match (len >= 2),
    # so prefix/root homographs such as a/na do not create spurious family edges.
    p = path(src, "MWderivations", "step4", "analysis2.txt")
    with open(p, encoding="utf-8") as f:
        for ln in f:
            c = ln.rstrip("\n").split("\t")
            if len(c) != 8 or c[6] != "DONE":
                continue
            for part in re.split(r"[-@+~,]", c[5]):
                part = part.strip()
                if len(part) >= 2 and part in attr:
                    add(part, c[2], "analysis2_decomp")
    return fam, lid


def load_freq(src):
    p = path(src, "kosha", "data", "frequency", "lemma_frequency.tsv")
    counts, ranks = {}, {}
    with open(p, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            k = r["lemma_slp1"]
            try:
                counts[k] = int(r["count_all"] or 0)
            except ValueError:
                counts[k] = 0
            try:
                ranks[k] = int(r["rank_all"]) if r["rank_all"] else None
            except ValueError:
                ranks[k] = None
    return counts, ranks


def median(xs):
    if not xs:
        return 0.0
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2.0


def spearman(xs, ys):
    def rk(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        out = [0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                out[order[k]] = avg
            i = j + 1
        return out
    a, b = rk(xs), rk(ys)
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    da = math.sqrt(sum((x - ma) ** 2 for x in a))
    db = math.sqrt(sum((y - mb) ** 2 for y in b))
    return num / (da * db) if da and db else 0.0


def zipf_slope(counts):
    """OLS slope of log10(count) on log10(rank) over attested derivatives."""
    pts = sorted((c for c in counts.values() if c > 0), reverse=True)
    xy = xx = yy = 0.0
    n = len(pts)
    for rank, c in enumerate(pts, 1):
        x, y = math.log10(rank), math.log10(c)
        xx += x * x
        xy += x * y
        yy += y * y
    mx = sum(math.log10(i) for i in range(1, n + 1)) / n
    my = sum(math.log10(c) for c in pts) / n
    return (xy - n * mx * my) / (xx - n * mx * mx) if n > 1 else 0.0


def canary_evidence(src, fam, n=10):
    """10 spread roots with an explicit MW `fr. √ root` noun/adjective record.

    Evidence is taken from the RAW mw.txt record (not the cleaned TSV context),
    so the canary really is a check against MW itself.
    """
    etym = path(src, "csl-orig", "v02", "mw", "mw_etymology.tsv")
    cand = collections.defaultdict(list)
    with open(etym, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            root, head = r.get("root_slp1", ""), r.get("headword_slp1", "")
            if (r.get("root_via") == "fr-root" and root in fam and head in fam[root]):
                cand[root].append((head, r.get("L_id", "")))
    eligible = sorted(cand)
    if len(eligible) > n:
        stride = len(eligible) // n
        eligible = eligible[::stride][:n]
    wanted = {L for r in eligible for _h, L in cand[r] if L}
    snippets = {}
    mw = path(src, "csl-orig", "v02", "mw", "mw.txt")
    cur, rec = None, []
    with open(mw, encoding="utf-8") as f:
        for line in f:
            if line.startswith("<L>"):
                m = re.match(r"<L>([^<]*)", line)
                cur = m.group(1).strip() if m else None
                rec = []
            elif line.startswith("<LEND>"):
                if cur in wanted and cur:
                    snippets[cur] = " ".join("".join(rec).split())[:300]
                cur, rec = None, []
            elif cur is not None:
                rec.append(line.rstrip("\n"))
    out = []
    for r in eligible:
        # prefer a record that actually shows a substantive gender tag + fr. √
        choices = sorted(cand[r], key=lambda hl: (
            0 if ("<lex>" in snippets.get(hl[1], "") and "√" in snippets.get(hl[1], "")) else 1,
            hl[0]))
        head, L = choices[0]
        out.append((r, head, L, snippets.get(L, "")))
    return out


