#!/usr/bin/env python3
"""NKRYa verb-government lint for the Кочергина методичка answer keys (H5400).

Parent: H5285 (NKRYa gloss lint, Systema-Sanscriticum/scripts/nkrya_gloss_lint.py);
grill 23-09-2026 Q6 — "answer keys: verb government on the Кочергина методичка first";
Q3 — the author's wording stays: flags only, a modern hint only after a vote.

Source: the «Ключи» section of METODICHKA_KOCHERGINA_V1_UPRAZHNENIIA_2026.md (the keys
proper plus «Переводы чтений»). Nothing in the source is edited.

Per sentence of the keys:

  1. tokenize the Cyrillic words and lemmatize them with pymorphy3;
  2. for every verb form (finite, infinitive, participle, gerund) find its governed
     dependent inside the clause — a preposition + noun phrase, or a bare noun/pronoun
     in an oblique case (gen/dat/acc/ins/loc) — the nearest one to the right, else to
     the left; the frame is (verb lemma, preposition or ∅, case);
  3. a hand curation file (verb_government_curation.tsv) drops heuristic mis-pairings
     and adds pairs the window heuristic misses — every row carries a reason;
  4. per frame, count in the NKRYa main corpus how often the verb occurs with that
     preposition + case (lex-gramm concordance, the dependent in the same direction as in
     the key) in a modern (1950–2026) and a 19th-century (1800–1899) slice, and the
     verb's own total in both slices — the 19c pair only when the modern frame is
     thin (< C19_SKIP_HITS hits or < C19_SKIP_SHARE of the verb's uses);
  5. flag: `no_modern` (0 modern frame hits) · `rare_modern` (< RARE_HITS modern hits) ·
     `c19_leaning` (19c share of the verb's uses ≥ C19_RATIO × modern share, with at
     least C19_MIN 19c hits) · `soft_rare` (modern share < SOFT_SHARE — a note only).

The window heuristic counts co-occurrence, not a parse: a noun in the right case near
the verb is counted even when another word governs it. That inflates counts, so the
lint errs toward NOT flagging — a flag is a lead for a human, never a verdict.

Rate limit (memory, measured 23-09-2026): ~60 NKRYa calls an hour per ACCOUNT, shared
by every session. The evidence cache (nkrya_government/evidence_cache.tsv, committed)
is saved every few lookups; `--offline` rebuilds the lint from it exactly.

  python KocherginaUchebnik_1998/nkrya_verb_government_lint.py --extract   # pairs only
  python KocherginaUchebnik_1998/nkrya_verb_government_lint.py             # live, resumable
  python KocherginaUchebnik_1998/nkrya_verb_government_lint.py --offline   # cache only
  python KocherginaUchebnik_1998/nkrya_verb_government_lint.py --selftest
"""

import argparse
import csv
import re
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "METODICHKA_KOCHERGINA_V1_UPRAZHNENIIA_2026.md"
OUT_DIR = HERE / "nkrya_government"
PAIRS_TSV = OUT_DIR / "verb_government_pairs.tsv"
LINT_TSV = OUT_DIR / "verb_government_lint.tsv"
EVIDENCE_TSV = OUT_DIR / "evidence_cache.tsv"
CURATION_TSV = OUT_DIR / "verb_government_curation.tsv"

SECTION_START = "## Ключи"
SECTION_END = "## Ревизии"

MODERN = {"fieldName": "created", "intRange": {"begin": 1950, "end": 2026}}
C19 = {"fieldName": "created", "intRange": {"begin": 1800, "end": 1899}}
SLICES = {"modern": MODERN, "c19": C19}

RARE_HITS = 20
C19_RATIO = 3.0
C19_MIN = 5
SOFT_SHARE = 0.005
C19_SKIP_HITS = 200
C19_SKIP_SHARE = 0.02

# pymorphy3 case grammemes -> NKRYa gramm values
CASE_MAP = {"gent": "gen", "gen2": "gen", "datv": "dat", "accs": "acc", "acc2": "acc",
            "ablt": "ins", "loct": "loc", "loc2": "loc"}
OBLIQUE = set(CASE_MAP.values())
# which cases a preposition takes (the ones that matter for a government check)
PREP_CASES = {
    "в": {"acc", "loc"}, "во": {"acc", "loc"}, "на": {"acc", "loc"},
    "о": {"acc", "loc"}, "об": {"acc", "loc"}, "обо": {"acc", "loc"},
    "с": {"gen", "ins", "acc"}, "со": {"gen", "ins", "acc"},
    "к": {"dat"}, "ко": {"dat"}, "по": {"dat", "acc", "loc"},
    "из": {"gen"}, "изо": {"gen"}, "из-за": {"gen"}, "из-под": {"gen"}, "от": {"gen"},
    "до": {"gen"}, "для": {"gen"}, "без": {"gen"}, "у": {"gen"}, "около": {"gen"},
    "вокруг": {"gen"}, "после": {"gen"}, "среди": {"gen"}, "посреди": {"gen"},
    "ради": {"gen"}, "кроме": {"gen"}, "от-": {"gen"},
    "за": {"acc", "ins"}, "под": {"acc", "ins"}, "над": {"ins"}, "перед": {"ins"},
    "между": {"ins", "gen"}, "при": {"loc"}, "про": {"acc"}, "через": {"acc"},
    "сквозь": {"acc"}, "против": {"gen"}, "из-": {"gen"},
}
VERBAL = {"VERB", "INFN", "PRTF", "PRTS", "GRND"}
NOMINAL = {"NOUN", "NPRO", "ADJF", "NUMR", "PRTF"}
HEADS = {"NOUN", "NPRO"}
CYR = re.compile(r"[А-Яа-яЁё]+(?:-[А-Яа-яЁё]+)*")
CLAUSE_BREAK = re.compile(r"[,;:.!?()«»\"—–]|\s-\s")
WINDOW = 4
# auxiliaries / copulas carry no government worth checking
SKIP_VERBS = {"быть", "являться", "стать", "мочь"}


def yo(s):
    return s.replace("ё", "е").replace("Ё", "Е")


# ---- source ---------------------------------------------------------------------------
def keys_section(text):
    a = text.index(SECTION_START)
    b = text.index(SECTION_END, a)
    return text[a + len(SECTION_START):b]


def sentences(section):
    """(sid, sentence) — one per key item / translation, split on sentence ends."""
    out = []
    # strip markdown emphasis, the ⟦…⟧ tags and bold item labels like **X-1.**
    clean = re.sub(r"⟦[^⟧]*⟧", " ", section)
    clean = clean.replace("**", " ").replace("*", " ")
    clean = re.sub(r"\s+", " ", clean)
    # a key label (VI-1., XXXII-2:, X-1:) starts a new item
    parts = re.split(r"\b([IVXL]+-\d+)[.:]", clean)
    label = "intro"
    buf = parts[0]
    items = [(label, buf)]
    for i in range(1, len(parts) - 1, 2):
        items.append((parts[i], parts[i + 1]))
    counter = {}
    for label, body in items:
        for s in re.split(r"(?<=[.!?»])\s+(?=[«А-ЯЁA-Z(])", body):
            s = s.strip()
            if not CYR.search(s):
                continue
            counter[label] = counter.get(label, 0) + 1
            out.append(("%s.%d" % (label, counter[label]), s))
    return out


# ---- extraction -----------------------------------------------------------------------
class Morph:
    def __init__(self, morph=None):
        if morph is None:
            import pymorphy3
            morph = pymorphy3.MorphAnalyzer()
        self.morph = morph

    def parses(self, w):
        return self.morph.parse(w.lower())


def tokens(sentence):
    """[(token, start, clause_no)] — clause_no increments at punctuation breaks."""
    out = []
    clause = 0
    pos = 0
    for m in CYR.finditer(sentence):
        if CLAUSE_BREAK.search(sentence[pos:m.start()]):
            clause += 1
        out.append((m.group(0), m.start(), clause))
        pos = m.end()
    return out


def verb_reading(parses):
    """The best non-abbreviation reading, if it is verbal («род.» is not «родился»,
    «покой» is a noun before it is an imperative)."""
    real = [p for p in parses if "Abbr" not in p.tag.grammemes]
    if real and real[0].tag.POS in VERBAL:
        return real[0]
    return None


def verb_lemma(p):
    """Participles and gerunds are indexed under the infinitive."""
    if p.tag.POS in ("PRTF", "PRTS", "GRND"):
        for lx in p.lexeme:
            if lx.tag.POS == "INFN":
                return yo(lx.word)
    return yo(p.normal_form)


def cases_of(parses, allowed=None, pos_set=HEADS):
    got = []
    for p in parses:
        if p.tag.POS not in pos_set:
            continue
        c = CASE_MAP.get(p.tag.case)
        if c and (allowed is None or c in allowed) and c not in got:
            got.append(c)
    return got


def frame_at(toks, j, direction, morph, transitive=False):
    """A (prep, case, dependent_word, distance) found starting at token j, or None."""
    word = toks[j][0].lower()
    if word in PREP_CASES and direction > 0:
        allowed = PREP_CASES[word]
        for k in range(j + 1, min(j + 4, len(toks))):
            if toks[k][2] != toks[j][2]:
                break
            ps = morph.parses(toks[k][0])
            heads = cases_of(ps, allowed)
            if heads:
                return (word, heads[0], toks[k][0], k)
            if not cases_of(ps, allowed, NOMINAL):
                break
        return None
    if direction < 0 and j > 0 and toks[j - 1][0].lower() in PREP_CASES \
            and toks[j - 1][2] == toks[j][2]:
        prep = toks[j - 1][0].lower()
        heads = cases_of(morph.parses(toks[j][0]), PREP_CASES[prep])
        return (prep, heads[0], toks[j][0], j) if heads else None
    ps = morph.parses(toks[j][0])
    # a bare dependent: its FIRST reading decides (дом = nom, not acc), except that a
    # transitive verb takes the accusative reading of a nom=acc / gen=acc form
    # («сотворить мир», «видел девушек»)
    noun = [p for p in ps if p.tag.POS in HEADS]
    if transitive and "acc" in cases_of([p for p in noun if p.score >= 0.05]):
        heads = ["acc"]
    else:
        heads = [c for c in cases_of(noun[:1]) if c in OBLIQUE]
    if heads and not (j > 0 and toks[j - 1][0].lower() in PREP_CASES):
        return ("", heads[0], toks[j][0], j)
    return None


def extract(sents, morph):
    """[{sid, verb_form, verb, prep, case, dependent, direction, sentence}]"""
    rows = []
    for sid, s in sents:
        toks = tokens(s)
        for i, (w, _, clause) in enumerate(toks):
            vp = verb_reading(morph.parses(w))
            if vp is None:
                continue
            lemma = verb_lemma(vp)
            if lemma in SKIP_VERBS:
                continue
            found = None
            for d in (1, -1):
                rng = range(i + 1, min(i + 1 + WINDOW, len(toks))) if d > 0 \
                    else range(i - 1, max(i - 1 - WINDOW, -1), -1)
                for j in rng:
                    if toks[j][2] != clause:
                        break
                    if verb_reading(morph.parses(toks[j][0])) is not None \
                            and toks[j][0].lower() not in PREP_CASES:
                        break               # another verb: its own dependents
                    f = frame_at(toks, j, d, morph, "tran" in vp.tag.grammemes)
                    if f:
                        found = (f, d)
                        break
                if found:
                    break
            if not found:
                continue
            (prep, case, dep, _), d = found
            rows.append({"sid": sid, "verb_form": w, "verb": lemma, "prep": prep,
                         "case": case, "dependent": dep,
                         "direction": "right" if d > 0 else "left",
                         "sentence": s, "source": "auto"})
    return rows


def pair_id(r):
    return "%s|%s|%s|%s" % (r["sid"], r["verb_form"].lower(), r["prep"] or "-", r["case"])


def load_curation(path=CURATION_TSV):
    drops, adds = {}, []
    if not path.exists():
        return drops, adds
    with path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["action"] == "drop":
                drops[r["pair_id"]] = r["reason"]
            elif r["action"] == "add":
                adds.append(r)
    return drops, adds


def apply_curation(rows, sents, drops, adds):
    kept = [r for r in rows if pair_id(r) not in drops]
    by_sid = dict(sents)
    for a in adds:
        sid, form, prep, case = a["pair_id"].split("|")
        kept.append({"sid": sid, "verb_form": form, "verb": a["verb"],
                     "prep": "" if prep == "-" else prep, "case": case,
                     "dependent": a["dependent"], "direction": a["direction"],
                     "sentence": by_sid.get(sid, ""), "source": "curated"})
    unknown = set(drops) - {pair_id(r) for r in rows}
    return kept, sorted(unknown)


# ---- NKRYa ----------------------------------------------------------------------------
def frame_query(verb, prep, case, direction):
    lex = lambda v: {"fieldName": "lex", "text": {"v": v}}
    gr = lambda v: {"fieldName": "gramm", "text": {"v": v}}
    dist = lambda a, b: {"fieldName": "dist", "intRange": {"begin": a, "end": b}}
    near = (1, 3) if direction == "right" else (-3, -1)
    if prep:
        subs = [[lex(verb)], [lex(prep), dist(*near)], [gr(case), dist(1, 2)]]
    else:
        subs = [[lex(verb)], [gr("S," + case), dist(*near)]]
    return {"sectionValues": [{"subsectionValues": [{"conditionValues": s} for s in subs]}]}


def verb_query(verb):
    return {"sectionValues": [{"subsectionValues": [
        {"conditionValues": [{"fieldName": "lex", "text": {"v": verb}}]}]}]}


class Evidence:
    """key -> {hits, docs, example}; the committed cache that makes --offline exact."""
    FIELDS = ["key", "hits", "docs", "example"]

    def __init__(self, path=EVIDENCE_TSV, client=None, interval=12.0, backoff=60.0,
                 save_every=5, max_calls=None):
        self.path, self.client = path, client
        self.interval, self.backoff, self.save_every = interval, backoff, save_every
        self.max_calls = max_calls
        self.rows, self.calls, self.misses, self._last = {}, 0, 0, 0.0
        if path.exists():
            with path.open(encoding="utf-8") as f:
                for r in csv.DictReader(f, delimiter="\t"):
                    self.rows[r["key"]] = r

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=self.FIELDS, delimiter="\t",
                               lineterminator="\n")
            w.writeheader()
            for k in sorted(self.rows):
                w.writerow({x: self.rows[k].get(x, "") for x in self.FIELDS})

    def get(self, key, query, slice_name):
        if key in self.rows:
            v = self.rows[key]["hits"]
            return int(v) if v not in ("", None) else None
        if self.client is None or (self.max_calls is not None and self.calls >= self.max_calls):
            self.misses += 1
            return None
        while True:
            wait = self.interval - (time.time() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.time()
            try:
                c = self.client.concordance(query, n=1,
                                            subcorpus_conditions=[SLICES[slice_name]])
                break
            except Exception as e:          # noqa: BLE001 — classify below
                msg = str(e)
                if "429" in msg.split(" ", 2)[:2] or msg.startswith("HTTP 429") \
                        or "retries exhausted" in msg:
                    print("  rate-limited; sleeping %ds" % self.backoff, file=sys.stderr)
                    time.sleep(self.backoff)
                    continue
                raise
        self.calls += 1
        self.rows[key] = {"key": key, "hits": "" if c.get("hits") is None else c["hits"],
                          "docs": "" if c.get("docs") is None else c["docs"],
                          "example": (c.get("lines") or [""])[0][:300]}
        if self.calls % self.save_every == 0:
            self.save()
        v = self.rows[key]["hits"]
        return int(v) if v not in ("", None) else None

    def example(self, key):
        return (self.rows.get(key) or {}).get("example", "")


def frame_key(r, slice_name):
    return "frame|%s|%s|%s|%s|%s" % (yo(r["verb"]), r["prep"] or "-", r["case"],
                                      r["direction"], slice_name)


def verb_key(verb, slice_name):
    return "verb|%s|%s" % (yo(verb), slice_name)


def needs_c19(fm, vm):
    """The 19c slice is only asked when the modern frame is thin: a frame with
    C19_SKIP_HITS+ modern hits and C19_SKIP_SHARE+ of the verb's uses is plainly alive,
    and at ~1 NKRYa call a minute the budget goes to the frames that can be flagged."""
    if fm is None or vm is None:
        return False
    return fm < C19_SKIP_HITS or (vm and fm / vm < C19_SKIP_SHARE)


def lookup(r, ev):
    q = frame_query(r["verb"], r["prep"], r["case"], r["direction"])
    out = {"frame_modern": ev.get(frame_key(r, "modern"), q, "modern"),
           "verb_modern": ev.get(verb_key(r["verb"], "modern"), verb_query(r["verb"]),
                                 "modern"),
           "frame_c19": None, "verb_c19": None, "c19_asked": False}
    if needs_c19(out["frame_modern"], out["verb_modern"]):
        out["c19_asked"] = True
        out["frame_c19"] = ev.get(frame_key(r, "c19"), q, "c19")
        out["verb_c19"] = ev.get(verb_key(r["verb"], "c19"), verb_query(r["verb"]), "c19")
    else:
        # an earlier run may already hold the 19c numbers: use them, never ask for them
        for k in ("frame", "verb"):
            key = frame_key(r, "c19") if k == "frame" else verb_key(r["verb"], "c19")
            if key in ev.rows:
                out[k + "_c19"] = ev.get(key, None, "c19")
    return out


def flags_for(h):
    fm, fc, vm, vc = h["frame_modern"], h["frame_c19"], h["verb_modern"], h["verb_c19"]
    if None in (fm, vm) or (h.get("c19_asked") and None in (fc, vc)):
        return ["pending"], None, None
    share_m = fm / vm if vm else 0.0
    share_c = (fc / vc) if (fc is not None and vc) else None
    fl = []
    if fm == 0:
        fl.append("no_modern")
    elif fm < RARE_HITS:
        fl.append("rare_modern")
    if share_c is not None and fc >= C19_MIN and share_c >= C19_RATIO * max(share_m, 1e-9):
        fl.append("c19_leaning")
    if fm and share_m < SOFT_SHARE:
        fl.append("soft_rare")
    return fl or ["ok"], share_m, share_c


# ---- outputs --------------------------------------------------------------------------
PAIR_FIELDS = ["pair_id", "sid", "verb_form", "verb", "prep", "case", "dependent",
               "direction", "source", "sentence"]
LINT_FIELDS = ["pair_id", "verb", "frame", "dependent", "sentence", "frame_modern",
               "verb_modern", "share_modern", "frame_c19", "verb_c19", "share_c19",
               "flags", "example_modern"]


def frame_label(r):
    return "%s + %s%s" % (r["verb"], (r["prep"] + " ") if r["prep"] else "", r["case"])


def write_tsv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n",
                           extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def run(args):
    morph = Morph()
    sents = sentences(keys_section(SOURCE.read_text(encoding="utf-8")))
    auto = extract(sents, morph)
    drops, adds = load_curation()
    pairs, stale = apply_curation(auto, sents, drops, adds)
    for r in pairs:
        r["pair_id"] = pair_id(r)
    write_tsv(PAIRS_TSV, PAIR_FIELDS, pairs)
    print("sentences %d · auto pairs %d · dropped %d · added %d · kept %d"
          % (len(sents), len(auto), len(auto) - (len(pairs) - len(adds)), len(adds),
             len(pairs)))
    if stale:
        print("WARN curation drops matching no auto pair: %s" % ", ".join(stale),
              file=sys.stderr)
    if args.extract:
        for r in pairs:
            print("%-28s %-22s %s" % (r["pair_id"], frame_label(r), r["dependent"]))
        return 0
    client = None
    if not args.offline:
        from csl_pyutil import nkrya
        client = nkrya.NkryaClient(cache_dir=str(args.raw_cache))
    ev = Evidence(client=client, interval=args.interval, backoff=args.backoff,
                  max_calls=args.max_calls)
    out = []
    try:
        for r in pairs:
            h = lookup(r, ev)
            fl, sm, sc = flags_for(h)
            out.append({"pair_id": r["pair_id"], "verb": r["verb"], "frame": frame_label(r),
                        "dependent": r["dependent"], "sentence": r["sentence"],
                        "frame_modern": h["frame_modern"], "verb_modern": h["verb_modern"],
                        "share_modern": "" if sm is None else "%.4f" % sm,
                        "frame_c19": h["frame_c19"], "verb_c19": h["verb_c19"],
                        "share_c19": "" if sc is None else "%.4f" % sc,
                        "flags": ",".join(fl),
                        "example_modern": ev.example(frame_key(r, "modern"))})
    finally:
        if client is not None:
            ev.save()
    write_tsv(LINT_TSV, LINT_FIELDS, out)
    counts = {}
    for o in out:
        for f in o["flags"].split(","):
            counts[f] = counts.get(f, 0) + 1
    print("live calls %d · cache misses %d · flags %s"
          % (ev.calls, ev.misses, " ".join("%s=%d" % kv for kv in sorted(counts.items()))))
    return 0 if ev.misses == 0 else 3


# ---- selftest -------------------------------------------------------------------------
def selftest():
    import tempfile
    morph = Morph()
    sents = [("X-1.1", "Кони утомились и падали на землю."),
             ("X-2.1", "Жертвенным возлиянием живут боги."),
             ("X-3.1", "Ученые жаждут встречи с учеными.")]
    rows = extract(sents, morph)
    got = {(r["verb"], r["prep"], r["case"], r["direction"]) for r in rows}
    assert ("падать", "на", "acc", "right") in got, got
    assert ("жить", "", "ins", "left") in got, got
    assert any(r[0] == "жаждать" for r in got), got
    # flags
    assert flags_for({"frame_modern": 0, "verb_modern": 100, "frame_c19": 3,
                      "verb_c19": 50})[0] == ["no_modern"]
    assert flags_for({"frame_modern": 500, "verb_modern": 1000, "frame_c19": 50,
                      "verb_c19": 100})[0] == ["ok"]
    fl = flags_for({"frame_modern": 30, "verb_modern": 30000, "frame_c19": 40,
                    "verb_c19": 2000})[0]
    assert "c19_leaning" in fl and "soft_rare" in fl, fl
    assert flags_for({"frame_modern": None, "verb_modern": 1, "frame_c19": None,
                      "verb_c19": None})[0] == ["pending"]
    # evidence cache round-trip + offline miss accounting
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "ev.tsv"

        class Fake:
            def concordance(self, q, n=1, subcorpus_conditions=None):
                return {"hits": 7, "docs": 3, "lines": ["пример"]}
        ev = Evidence(path=p, client=Fake(), interval=0, save_every=1)
        assert ev.get("k", {}, "modern") == 7
        ev.save()
        ev2 = Evidence(path=p)
        assert ev2.get("k", {}, "modern") == 7 and ev2.get("k2", {}, "c19") is None
        assert ev2.misses == 1
    # the real source parses and yields pairs
    sents = sentences(keys_section(SOURCE.read_text(encoding="utf-8")))
    assert len(sents) > 20, len(sents)
    print("selftest OK (%d key sentences, %d auto pairs)"
          % (len(sents), len(extract(sents, morph))))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--extract", action="store_true", help="pairs only, no NKRYa")
    ap.add_argument("--offline", action="store_true", help="evidence cache only")
    ap.add_argument("--interval", type=float, default=12.0)
    ap.add_argument("--backoff", type=float, default=60.0)
    ap.add_argument("--max-calls", type=int, default=None)
    ap.add_argument("--raw-cache", type=Path, default=Path("/tmp/nkrya_h5400_raw"))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
