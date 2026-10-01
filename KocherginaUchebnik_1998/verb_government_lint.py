#!/usr/bin/env python3
"""Verb-government lint for the Kochergina answer keys against NKRYa (H5400).

Step 4 of H5285 (NKRYa gloss lint), which linted single-word glosses; this lints the
*syntax* of the Russian answer keys: for every verb + dependent noun phrase in a key,
is the case/preposition the verb takes still the modern government, or a rare /
XIX-century-only one that a beginner would learn wrong?

Pipeline:

  1. harvest the key texts (METODICHKA ... UPRAZHNENIIA «Ключи» + «Переводы чтений»,
     LessonPacks quizzes.json correct options) -> one row per key snippet;
  2. extract (verb, preposition, case, dependent noun) quadruples with pymorphy3,
     resolving case ambiguity against the preposition's own case set;
  3. ask NKRYa for the verb's government profile:
       tier A  sketch(verb, "V")        - the word-sketch syntactic relations (1 call/verb)
       tier B  concordance lex+dist     - verb ... preposition within 1-3 words, counted
                                          in a modern (1950+) and a XIX-century slice
                                          (2 calls per verb+preposition pair)
     modern 0 + 19c > 0 -> `c19_only`; modern 0 + 19c 0 -> `zero_modern`; a pair whose
     modern hits are under `--rare-hits` -> `rare`;
  4. write a lint TSV + a compact evidence cache; `--offline` re-runs from the cache
     only and reports every uncached pair as `unknown` (never as "no flag").

Teacher wording is never rewritten here (grill 23-09-2026 Q3): the lint flags, and a
modern hint reaches a key only after a human vote, so flagged pairs go out as a review
sheet spec of at most 10 cards (`--sheet`).

Rate limit (measured 23-09-2026, H5285): ~60 successful calls an hour per ACCOUNT,
shared by every session holding the key. The evidence cache is saved every 20 lookups
and every run is resumable, so a stopped run loses nothing.

  python verb_government_lint.py --offline            # cache only, safe anywhere
  python verb_government_lint.py                      # live, resumable
  python verb_government_lint.py --max-lookups 40     # bounded live slice
  python verb_government_lint.py --selftest           # no network, no repo files

A live run needs the NKRYa token: env `NKRYA_TOKEN`, or the macOS keychain entry the
shared client reads (`csl_pyutil.nkrya.load_token`). This Windows box has neither as of
25-09-2026, which is why the committed TSV carries `unknown` in the NKRYa columns.
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
KEYS_MD = HERE / "METODICHKA_KOCHERGINA_V1_UPRAZHNENIIA_2026.md"
LESSONPACKS = HERE / "LessonPacks"
OUT_TSV = HERE / "verb_government_kochergina_keys.tsv"
EVIDENCE_TSV = HERE / "verb_government_evidence.tsv"
SHEET_SPEC = REPO / "review" / "specs" / "sanskritgrammar-kochergina-verb-government.json"

MODERN = {"fieldName": "created", "intRange": {"begin": 1950, "end": 2026}}
C19 = {"fieldName": "created", "intRange": {"begin": 1800, "end": 1899}}

CYR = re.compile(r"[А-Яа-яЁё]+(?:-[А-Яа-яЁё]+)*")
TOKEN = re.compile(r"[А-Яа-яЁё]+(?:-[А-Яа-яЁё]+)*|[,;:—–()«»\".!?]")
SENT_END = {".", "!", "?", ";", "»", "«", "(", ")", "—", "–", ":"}

VERBAL = {"VERB", "INFN", "GRND", "PRTF", "PRTS"}
NOMINAL = {"NOUN", "NPRO"}
CASES = ["nomn", "gent", "datv", "accs", "ablt", "loct", "gen2", "acc2", "loc2", "voct"]
CASE_RU = {"nomn": "И.", "gent": "Р.", "datv": "Д.", "accs": "В.", "ablt": "Т.",
           "loct": "П.", "gen2": "Р.2", "acc2": "В.2", "loc2": "П.2", "voct": "Зв."}
# pymorphy3 splits the second genitive/locative off; fold them onto the main case so a
# government profile is not split between `gent` and `gen2`.
CASE_FOLD = {"gen2": "gent", "acc2": "accs", "loc2": "loct"}

# Which cases each preposition governs — used to disambiguate the noun's parse.
PREP_CASES = {
    "в": {"accs", "loct"}, "во": {"accs", "loct"},
    "на": {"accs", "loct"}, "за": {"accs", "ablt"},
    "под": {"accs", "ablt"}, "подо": {"accs", "ablt"},
    "перед": {"ablt"}, "передо": {"ablt"}, "пред": {"ablt"}, "предо": {"ablt"},
    "над": {"ablt"}, "надо": {"ablt"},
    "с": {"gent", "accs", "ablt"}, "со": {"gent", "accs", "ablt"},
    "из": {"gent"}, "изо": {"gent"}, "из-за": {"gent"}, "из-под": {"gent"},
    "от": {"gent"}, "ото": {"gent"}, "до": {"gent"}, "у": {"gent"},
    "для": {"gent"}, "без": {"gent"}, "безо": {"gent"}, "ради": {"gent"},
    "около": {"gent"}, "возле": {"gent"}, "вокруг": {"gent"}, "кроме": {"gent"},
    "после": {"gent"}, "против": {"gent"}, "среди": {"gent"}, "вместо": {"gent"},
    "сверх": {"gent"}, "вследствие": {"gent"}, "ввиду": {"gent"}, "насчет": {"gent"},
    "насчёт": {"gent"}, "мимо": {"gent"}, "путем": {"gent"}, "путём": {"gent"},
    "к": {"datv"}, "ко": {"datv"}, "благодаря": {"datv"}, "вопреки": {"datv"},
    "согласно": {"datv"}, "навстречу": {"datv"},
    "по": {"datv", "accs", "loct"},
    "о": {"loct", "accs"}, "об": {"loct", "accs"}, "обо": {"loct", "accs"},
    "при": {"loct"}, "про": {"accs"}, "через": {"accs"}, "чрез": {"accs"},
    "сквозь": {"accs"}, "спустя": {"accs"},
    "между": {"ablt", "gent"}, "меж": {"ablt", "gent"},
}

# Auxiliaries and copulas have no government worth linting.
SKIP_VERBS = {"быть", "бывать", "стать", "становиться"}
# Surfaces pymorphy3 reads as a verb although the key uses them as something else:
# «род» (noun) is parsed only as a form of «родиться», «стоит» is стоять/стоить. They
# stay in the TSV as `ambiguous_verb` rather than silently producing a government pair.
AMBIGUOUS_SURFACES = {"род", "рода", "роду", "родом", "стоит", "стоят", "стоял",
                      "стояла", "стояли"}
# Pronouns whose case is government-relevant but whose lemma tells a reader nothing.
PRONOUN_LEMMAS = {"он", "она", "оно", "они", "я", "ты", "мы", "вы", "себя", "кто", "что",
                  "который", "этот", "тот", "весь", "такой", "какой", "чей", "сам"}

MAX_FORWARD = 6      # tokens after the verb still counted as its dependants
MAX_BACKWARD = 4     # Russian puts objects before the verb too («покой потеряла»)


# ---- harvest -------------------------------------------------------------------------
def _metodichka_keys(path=KEYS_MD):
    """Key snippets from the «Ключи» section of the methodichka (incl. «Переводы чтений»).

    Only the answer-key half of the file is read: the exercises above it are prompts, not
    keys, and the revision table below it is provenance.
    """
    rows = []
    if not Path(path).exists():
        return rows
    text = Path(path).read_text(encoding="utf-8")
    start = text.find("## Ключи")
    if start < 0:
        return rows
    end = text.find("\n## ", start + 4)
    body = text[start:end if end > 0 else len(text)]
    # Keys are «**X-1.** ...» blocks; «**Переводы чтений**» is one block of «X-1: «...»».
    # Bold inside a key («candramāḥ **м.**») is emphasis, not a new block: a label that is
    # not a locus continues the block it sits in, or the text would be split on emphasis.
    blocks = []
    for m in re.finditer(r"\*\*([^*]{1,40}?)\*\*\s*(⟦[^⟧]*⟧)?\.?\s*", body):
        label = m.group(1).strip().rstrip(".")
        chunk_start = m.end()
        nxt = body.find("**", chunk_start)
        chunk = body[chunk_start:nxt if nxt > 0 else len(body)]
        chunk = chunk.replace("\n", " ").strip()
        if not chunk or not CYR.search(chunk):
            continue
        if not (re.fullmatch(r"[IVXL]+-\d+", label) or label.startswith("Переводы")):
            if blocks:
                blocks[-1][1] = (blocks[-1][1] + " " + chunk).strip()
            continue
        blocks.append([label, chunk])
    for label, chunk in blocks:
        if label.startswith("Переводы"):
            for t in re.finditer(r"([IVXL]+-\d+(?:\s*\([^)]*\))?):\s*«([^»]+)»", chunk):
                rows.append({"source": "metodichka_translations",
                             "locus": t.group(1).replace(" ", ""), "text": t.group(2)})
        else:
            rows.append({"source": "metodichka_keys", "locus": label, "text": chunk})
    return rows


def _lessonpack_keys(root=LESSONPACKS):
    """The CORRECT option of every LessonPack MCQ (plus its prompt): the answer key text."""
    rows = []
    if not Path(root).exists():
        return rows
    for path in sorted(Path(root).rglob("quizzes.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        profile = str(path.parent.relative_to(root)).replace(os.sep, "/")
        for item in data.get("items") or []:
            opts = item.get("options") or []
            idx = item.get("answer_index")
            if not isinstance(idx, int) or not (0 <= idx < len(opts)):
                continue
            for kind, txt in (("prompt", item.get("prompt") or ""), ("answer", opts[idx])):
                if txt and CYR.search(txt):
                    rows.append({"source": "lessonpack_%s" % kind,
                                 "locus": "%s/%s" % (profile, item.get("id") or "?"),
                                 "text": txt})
    return rows


def harvest():
    """All answer-key snippets, deduplicated on (source kind, text)."""
    rows = _metodichka_keys() + _lessonpack_keys()
    seen, out = set(), []
    for r in rows:
        key = (r["source"].split("_")[0], r["text"])
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


# ---- extraction ----------------------------------------------------------------------
class Extractor:
    def __init__(self, morph=None):
        if morph is None:
            import pymorphy3
            morph = pymorphy3.MorphAnalyzer()
        self.morph = morph

    def _tag(self, token):
        return self.morph.parse(token.lower())

    @staticmethod
    def _cases(parses):
        out = set()
        for p in parses:
            for c in CASES:
                if c in p.tag:
                    out.add(CASE_FOLD.get(c, c))
        return out

    def pairs(self, text, source, locus):
        """(verb, prep, case, dependent) quadruples found in one key snippet."""
        toks = [t for t in TOKEN.findall(text)]
        parsed = [(t, self._tag(t) if CYR.fullmatch(t) else []) for t in toks]
        found = []
        for i, (tok, parses) in enumerate(parsed):
            if not parses:
                continue
            pos = parses[0].tag.POS
            verb_parses = [p for p in parses if p.tag.POS in VERBAL]
            if not verb_parses or (pos not in VERBAL and len(verb_parses) < len(parses)):
                continue          # «стали» as a noun reading too: too ambiguous to lint
            verb = verb_parses[0].normal_form
            if verb in SKIP_VERBS:
                continue
            shaky = tok.lower() in AMBIGUOUS_SURFACES
            for j in self._window(parsed, i):
                pair = self._dependant(parsed, i, j, verb, verb_parses[0].tag.POS)
                if pair:
                    if shaky:
                        pair["status"] = "ambiguous_verb"
                    pair.update({"source": source, "locus": locus,
                                 "snippet": self._snippet(toks, i, j)})
                    found.append(pair)
        return found

    @staticmethod
    def _window(parsed, i):
        """Token indices that may hold a dependant of the verb at i (clause-bounded)."""
        out = []
        for j in range(i + 1, min(i + 1 + MAX_FORWARD, len(parsed))):
            tok, parses = parsed[j]
            if tok in SENT_END or tok == ",":
                break
            if parses and parses[0].tag.POS in ("VERB", "INFN"):
                break
            out.append(j)
        for j in range(i - 1, max(i - 1 - MAX_BACKWARD, -1), -1):
            tok, parses = parsed[j]
            if tok in SENT_END or tok == ",":
                break
            if parses and parses[0].tag.POS in ("VERB", "INFN"):
                break
            out.append(j)
        return out

    def _dependant(self, parsed, i, j, verb, verb_pos):
        tok, parses = parsed[j]
        if not parses or parses[0].tag.POS not in NOMINAL:
            return None
        noun = parses[0].normal_form
        cases = self._cases([p for p in parses if p.tag.POS in NOMINAL])
        if not cases:
            return None
        prep = ""
        for k in (j - 1, j - 2, j - 3):          # «на сырую землю»: prep two tokens back
            if k < 0 or k <= i - 1 - MAX_BACKWARD:
                break
            ptok = parsed[k][0].lower()
            if ptok in PREP_CASES:
                prep = ptok
                break
            pp = parsed[k][1]
            if not pp or pp[0].tag.POS not in ("ADJF", "PRTF", "NUMR", "NPRO"):
                break
        if prep:
            cases &= PREP_CASES[prep]
            if not cases:
                return None
        else:
            cases.discard("nomn")                 # a bare nominative is the subject
            cases.discard("voct")
        if not cases:
            return None
        status = "" if len(cases) == 1 else "ambiguous_case"
        case = sorted(cases)[0] if len(cases) == 1 else "|".join(sorted(cases))
        return {"verb": verb, "verb_pos": verb_pos, "prep": prep, "case": case,
                "dependent": noun, "dependent_form": tok.lower(),
                "pronoun": "1" if noun in PRONOUN_LEMMAS else "",
                "status": status}

    @staticmethod
    def _snippet(toks, i, j):
        lo, hi = min(i, j), max(i, j)
        return " ".join(toks[max(lo - 1, 0):hi + 2])


# ---- NKRYa evidence ------------------------------------------------------------------
def gov_query(verb, prep, dist=(1, 3)):
    """lex-gramm: lemma `verb` followed within `dist` words by the preposition `prep`."""
    subsections = [{"conditionValues": [{"fieldName": "lex", "text": {"v": verb}}]}]
    subsections.append({"conditionValues": [
        {"fieldName": "lex", "text": {"v": prep}},
        {"fieldName": "dist", "intRange": {"begin": dist[0], "end": dist[1]}}]})
    return {"sectionValues": [{
        "conditionValues": [{"fieldName": "disambmod", "text": {"v": "main"}},
                            {"fieldName": "distmod", "text": {"v": "with_zeros"}}],
        "subsectionValues": subsections}]}


class Evidence:
    """Compact committed cache over the client's raw cache (same shape as H5285's)."""

    FIELDS = ["key", "value", "extra"]

    def __init__(self, path=EVIDENCE_TSV, client=None, offline=False, save_every=20,
                 max_lookups=None):
        self.path = Path(path)
        self.client = client
        self.offline = offline
        self.save_every = save_every
        self.max_lookups = max_lookups
        self.rows = {}
        self.live = 0
        self.misses = 0
        self.budget_stop = False
        if self.path.exists():
            with open(self.path, encoding="utf-8", newline="") as f:
                for r in csv.DictReader(f, delimiter="\t"):
                    self.rows[r["key"]] = r

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, self.FIELDS, delimiter="\t", lineterminator="\n")
            w.writeheader()
            for k in sorted(self.rows):
                w.writerow({x: self.rows[k].get(x, "") for x in self.FIELDS})

    def _lookup(self, key, fn, encode):
        if key in self.rows:
            return self.rows[key]
        if self.client is None:
            self.misses += 1
            return None
        if self.max_lookups is not None and self.live >= self.max_lookups:
            self.budget_stop = True
            self.misses += 1
            return None
        try:
            out = fn()
        except Exception as exc:                  # offline miss / auth / transport
            if _is_offline_miss(exc):
                self.misses += 1
                return None
            raise
        self.live += 1
        self.rows[key] = encode(key, out)
        if self.live % self.save_every == 0:
            self.save()
            print("  … %d live lookups, cache saved" % self.live, file=sys.stderr)
        return self.rows[key]

    def sketch_relations(self, verb):
        """Government relations NKRYa's word sketch reports for the verb (tier A)."""
        key = "sketch|%s" % verb
        row = self._lookup(key, lambda: self.client.sketch(verb, "V"),
                           lambda k, out: {"key": k, "value": ";".join(sorted(out or {})),
                                           "extra": str(sum(len(v) for v in (out or {}).values()))})
        return None if row is None else [r for r in (row["value"] or "").split(";") if r]

    def prep_hits(self, verb, prep, slice_name):
        """Modern / XIX-century hit counts for `verb ... prep` (tier B)."""
        key = "gov|%s|%s|%s" % (verb, prep, slice_name)
        cond = [MODERN if slice_name == "modern" else C19]
        row = self._lookup(
            key,
            lambda: self.client.concordance(gov_query(verb, prep), n=1,
                                            subcorpus_conditions=cond),
            lambda k, out: {"key": k,
                            "value": "" if out.get("hits") is None else out["hits"],
                            "extra": "" if out.get("docs") is None else out["docs"]})
        if row is None or row["value"] in ("", None):
            return None
        return int(row["value"])


def _is_offline_miss(exc):
    try:
        from csl_pyutil.nkrya import NkryaOffline
    except ImportError:
        return False
    return isinstance(exc, NkryaOffline)


def make_client(offline, cache_dir=None):
    """The shared H5282 client, or None when no token is reachable on this box."""
    from csl_pyutil import nkrya
    if not offline and not nkrya.load_token():
        print("! no NKRYa token on this box (env NKRYA_TOKEN / keychain) — offline only",
              file=sys.stderr)
        return None
    kwargs = {"offline": True} if offline else {}
    if cache_dir:
        kwargs["cache_dir"] = cache_dir
    try:
        return nkrya.NkryaClient(**kwargs)
    except TypeError:                      # older client without an `offline` kwarg
        return nkrya.NkryaClient(**({"cache_dir": cache_dir} if cache_dir else {}))


# ---- lint ----------------------------------------------------------------------------
def lint_pair(pair, ev, rare_hits):
    """Attach NKRYa columns + a flag to one extracted government pair."""
    out = dict(pair)
    out.update({"sketch_relations": "", "modern_hits": "", "c19_hits": "", "flag": ""})
    if pair["status"] in ("ambiguous_case", "ambiguous_verb"):
        out["flag"] = pair["status"]
        return out
    if ev is None:
        out["flag"] = "unknown"
        return out
    rels = ev.sketch_relations(pair["verb"])
    if rels is not None:
        out["sketch_relations"] = ";".join(rels)
    if not pair["prep"]:
        # Bare-case government: the word sketch is the only verified-shape signal we have.
        out["flag"] = "unknown" if rels is None else "case_only_review"
        return out
    modern = ev.prep_hits(pair["verb"], pair["prep"], "modern")
    c19 = ev.prep_hits(pair["verb"], pair["prep"], "c19")
    if modern is None or c19 is None:
        out["flag"] = "unknown"
        return out
    out["modern_hits"], out["c19_hits"] = modern, c19
    if modern == 0 and c19 > 0:
        out["flag"] = "c19_only"
    elif modern == 0:
        out["flag"] = "zero_modern"
    elif modern < rare_hits:
        out["flag"] = "rare"
    return out


TSV_FIELDS = ["source", "locus", "verb", "verb_pos", "prep", "case", "case_ru",
              "dependent", "dependent_form", "pronoun", "status", "sketch_relations",
              "modern_hits", "c19_hits", "flag", "snippet"]

FLAG_ORDER = ["c19_only", "zero_modern", "rare", "case_only_review", "ambiguous_case",
              "ambiguous_verb", "unknown", ""]


def run(offline, rare_hits, max_lookups, write_sheet, out_tsv=OUT_TSV,
        evidence_tsv=EVIDENCE_TSV):
    ex = Extractor()
    snippets = harvest()
    pairs = []
    for row in snippets:
        pairs.extend(ex.pairs(row["text"], row["source"], row["locus"]))
    client = make_client(offline)
    ev = Evidence(path=evidence_tsv, client=client, offline=offline,
                  max_lookups=max_lookups) if client is not None else None
    linted = [lint_pair(p, ev, rare_hits) for p in pairs]
    for r in linted:
        r["case_ru"] = "|".join(CASE_RU.get(c, c) for c in r["case"].split("|"))
    linted.sort(key=lambda r: (FLAG_ORDER.index(r["flag"]) if r["flag"] in FLAG_ORDER
                               else 99, r["verb"], r["prep"], r["case"]))
    Path(out_tsv).parent.mkdir(parents=True, exist_ok=True)
    with open(out_tsv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, TSV_FIELDS, delimiter="\t", lineterminator="\n",
                           extrasaction="ignore")
        w.writeheader()
        for r in linted:
            w.writerow(r)
    if ev is not None:
        ev.save()
    counts = {}
    for r in linted:
        counts[r["flag"] or "clean"] = counts.get(r["flag"] or "clean", 0) + 1
    summary = {"snippets": len(snippets), "pairs": len(linted),
               "verbs": len({r["verb"] for r in linted}),
               "prepositional": sum(1 for r in linted if r["prep"]),
               "counts": counts,
               "live_lookups": 0 if ev is None else ev.live,
               "cache_misses": 0 if ev is None else ev.misses,
               "budget_stop": bool(ev is not None and ev.budget_stop),
               "token": bool(client is not None and not offline)}
    flagged = [r for r in linted if r["flag"] in ("c19_only", "zero_modern", "rare")]
    if write_sheet and flagged:
        emit_sheet(flagged[:10])
        summary["sheet"] = str(SHEET_SPEC)
    return linted, summary


def emit_sheet(flagged, path=SHEET_SPEC):
    """A review-sheet spec (<=10 cards) for /review-sheet — flags only, never a rewrite."""
    cards = []
    for r in flagged:
        gov = "%s + %s%s" % (r["verb"], (r["prep"] + " ") if r["prep"] else "",
                             CASE_RU.get(r["case"], r["case"]))
        cards.append({
            "id": "%s-%s-%s" % (r["locus"], r["verb"], r["prep"] or r["case"]),
            "title": gov,
            "body": "Ключ %s: «%s». NKRYa 1950+: %s вхождений, XIX в.: %s (%s)."
                    % (r["locus"], r["snippet"], r["modern_hits"], r["c19_hits"],
                       r["flag"]),
            "question": "Оставить формулировку ключа как есть, или дать современную "
                        "подсказку рядом (формулировку учителя не переписываем)?",
            "options": ["оставить", "добавить подсказку", "отложить"],
        })
    spec = {"sheet_id": "sanskritgrammar-kochergina-verb-government",
            "title": "Управление глаголов в ключах Кочергиной (H5400)",
            "intro": "Флаги лингвистического линта: управление глагола в ключе редкое "
                     "или засвидетельствовано только в XIX в. по НКРЯ. "
                     "Голосование решает только, добавлять ли подсказку.",
            "cards": cards}
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")


# ---- selftest ------------------------------------------------------------------------
SELFTEST_TEXT = "Кони утомились и падали на землю."


class _FakeClient:
    def sketch(self, lemma, pos=None):
        return {"глагол + сущ.вин.": [("земля", 7.0)]}

    def concordance(self, lexgramm, n=1, subcorpus_conditions=None):
        begin = subcorpus_conditions[0]["intRange"]["begin"]
        return {"hits": 0 if begin == 1950 else 12, "docs": 1, "lines": []}


def selftest():
    ex = Extractor()
    pairs = ex.pairs(SELFTEST_TEXT, "selftest", "T-1")
    got = {(p["verb"], p["prep"], p["case"]) for p in pairs}
    assert ("падать", "на", "accs") in got, got
    ev = Evidence(path=Path(os.devnull + ".tsv"), client=_FakeClient())
    ev.rows = {}
    pair = next(p for p in pairs if p["prep"] == "на")
    out = lint_pair(pair, ev, rare_hits=5)
    assert out["flag"] == "c19_only", out
    assert out["modern_hits"] == 0 and out["c19_hits"] == 12, out
    clean = lint_pair(dict(pair, verb="идти"), ev, rare_hits=5)
    assert clean["flag"] == "c19_only", clean          # fake client answers 0/12 always
    amb = lint_pair(dict(pair, status="ambiguous_case"), ev, rare_hits=5)
    assert amb["flag"] == "ambiguous_case", amb
    off = lint_pair(pair, None, rare_hits=5)
    assert off["flag"] == "unknown", off               # no evidence is never "no flag"
    q = gov_query("падать", "на")
    subs = q["sectionValues"][0]["subsectionValues"]
    assert subs[0]["conditionValues"][0]["text"]["v"] == "падать"
    assert subs[1]["conditionValues"][1]["intRange"] == {"begin": 1, "end": 3}
    print("selftest OK — %d pairs from the fixture sentence" % len(pairs))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--offline", action="store_true",
                    help="cache only; uncached pairs are reported as `unknown`")
    ap.add_argument("--rare-hits", type=int, default=20,
                    help="modern hits below this count the pair as `rare` (default 20)")
    ap.add_argument("--max-lookups", type=int, default=None,
                    help="stop making live calls after N (resumable; cache is saved)")
    ap.add_argument("--sheet", action="store_true",
                    help="write a review-sheet spec for up to 10 flagged pairs")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    linted, summary = run(args.offline, args.rare_hits, args.max_lookups, args.sheet)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("wrote %s (%d rows)" % (OUT_TSV, len(linted)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
