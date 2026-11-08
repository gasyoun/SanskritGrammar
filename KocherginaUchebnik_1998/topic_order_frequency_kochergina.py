#!/usr/bin/env python3
"""topic_order_frequency_kochergina.py — data pass for dossier (i) (H7825).

Sources: Kochergina_unicode.mdx + VisualDCS/tense_case_data.json (DCS-2021,
the SAME slice as verify_claims_dcs.py / claims.yml). Outputs compact
topic_order_frequency_data.json: per-lesson counts, category×intro×DCS rows,
Spearman, lexical stats. Form/instr/gloss channels print candidates to the
console for hand adjudication; the committed JSON carries counts only
(token gate: 20 KB per new file). Full detail: re-run locally.
Provenance: GLM 5.3 (zcode/zai-individual-coding-plan/GLM-5.3), 08-11-2026, H7825.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

HERE = Path(__file__).resolve().parent
SG_ROOT = HERE.parent                      # SanskritGrammar repo root (worktree-safe via file location)
VDCS = SG_ROOT.parent / "SanskritGrammar"  # placeholder, resolved below
# VisualDCS is a SIBLING of the main SanskritGrammar checkout under GitHub/.
# Under a worktree, resolve to the canonical clones dir if the sibling is absent.
def _find_vdcs() -> Path:
    for c in (SG_ROOT.parent / "VisualDCS", Path.home() / "Documents" / "GitHub" / "VisualDCS"):
        if (c / "tense_case_data.json").exists():
            return c
    raise SystemExit("VisualDCS sibling not found")

VDCS = _find_vdcs()

MDX = HERE / "Kochergina_unicode.mdx"
OUT = HERE / "topic_order_frequency_data.json"

DEV = r"\u0900-\u097F"
DEV_RE = re.compile(f"[{DEV}]+")
DEVA_WORD_RE = re.compile(f"[{DEV}][{DEV}\u200c\u200d]*")
STRIP_CHARS = "\u0964\u0965\u0950\u200c\u200d"  # danda, double danda, om, ZWJ/ZWNJ

# The book's own roman numbering (1..40); занятие 40 is printed «XXXX».
def std_roman(n: int) -> str:
    vals = [(40, "XXXX"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    out = []
    for v, s in vals:
        while n >= v:
            out.append(s)
            n -= v
    return "".join(out)

ROMANS = {std_roman(i): i for i in range(1, 41)}
LESSON_RE = re.compile(r"^##\s+Занятие\s+([IVX]+)\.?\s*(.*)$")
TOC_RE = re.compile(r"^(?:>\s*)?(\d+)\\?\.\s*(.+?)\\?\s*$")
EX_HEAD_RE = re.compile(r"^(?:>\s*)?\**([IVX]+)\**\\?\.\**\s+(.+)$")  # «I. », «**II.** », «IV\. »
SLOVA_HEAD_RE = re.compile(r"^(?:>\s*)?Слова(\\|:)?\s*$")
SLOVA_K_HEAD_RE = re.compile(r"^(?:>\s*)?Слова к переводу\s*$")
SLOVA_ENTRY_RE = re.compile(r"^(?:>\s*)?(.+?)\s+[-—]\s+(.+?)\\?\s*$")
DICT_RE = re.compile(f"^([{DEV}]+)\\s+(\\S+)\\s*(.*)$")

ACCENTS = "\u0301\u0300\u030d\u030e\u0323\u0324\u030c\u0302\u0304\u0306\u0308\u030a\u030b"

def norm_iast(s: str) -> str:
    """Lowercase, strip combining accents/anudāta, drop non-letter tail."""
    s = unicodedata.normalize("NFC", s)
    s = "".join(ch for ch in s if ch not in ACCENTS)
    s = s.lower()
    return re.sub(r"[^a-zāīūṛṝḷḹṃḥṱḍṭṇñśṣhalkgjtdpbnmyvwrsezfqioux\-]", "", s)

def strip_quote(line: str) -> str:
    return re.sub(r"^(?:>\s*)+", "", line)

def deva_tokens(text: str):
    for m in DEVA_WORD_RE.findall(text):
        t = "".join(ch for ch in m if ch not in STRIP_CHARS)
        if len(t) >= 2:
            yield t

def deva_to_iast(tok: str) -> str:
    return transliterate(tok, sanscript.DEVANAGARI, sanscript.IAST)

# ---------------------------------------------------------------- parse mdx
def parse_lessons(lines):
    lessons = []
    cur = None
    for i, raw in enumerate(lines):
        m = LESSON_RE.match(raw)
        if m:
            roman = m.group(1)
            n = ROMANS.get(roman)
            if n is None:
                continue
            cur = {
                "n": n, "roman": roman, "title": m.group(2).strip(),
                "start": i, "toc": [], "exercise_start": None,
                "slova_blocks": [], "bg_text": False,
            }
            lessons.append(cur)
            continue
        if cur is None:
            continue
        q = strip_quote(raw).rstrip("\\").strip()
        # exercise block: strict «Упражнения» line (EXERCISE_BLOCK_COVERAGE contract)
        if cur["exercise_start"] is None and q == "Упражнения":
            cur["exercise_start"] = i
        # Слова header (exact forms only — prose lines starting with Слова excluded)
        if SLOVA_HEAD_RE.match(raw) or SLOVA_K_HEAD_RE.match(raw):
            cur["slova_blocks"].append({"head_line": i, "entries": []})
        elif cur["slova_blocks"]:
            blk = cur["slova_blocks"][-1]
            em = SLOVA_ENTRY_RE.match(raw)
            if em and not raw.startswith("#"):
                blk["entries"].append({"iast": em.group(1).strip(), "gloss": em.group(2).strip()})
            elif blk["entries"]:
                # first non-entry line after entries ends the block
                blk["end"] = i
                pass
    # second pass: TOC extraction (numbered lines in the head of each lesson)
    for L in lessons:
        body = lines[L["start"] + 1: L["start"] + 45]
        seen, nums = [], []
        for raw in body:
            q = strip_quote(raw)
            tm = TOC_RE.match(q)
            if tm:
                num = int(tm.group(1))
                nums.append(num)
                seen.append(re.sub(r"\\", "", tm.group(2)).strip())
            elif seen and (q.rstrip("\\").strip() == ""):
                break
        L["toc"] = seen
    return lessons

def parse_dictionary(lines, start_idx):
    entries = []
    for raw in lines[start_idx + 1:]:
        m = DICT_RE.match(raw)
        if m:
            entries.append({
                "deva": m.group(1), "iast": m.group(2),
                "iast_plain": norm_iast(m.group(2)),
                "rest": m.group(3).strip(),
            })
    return entries

# ------------------------------------------------------------ DCS-2021 join
def dcs_slice():
    d = json.loads((VDCS / "tense_case_data.json").read_text(encoding="utf-8"))
    total = d["total_verbal"]
    rows = d["tenses"]
    def pick(*labels):
        n = sum(r["n"] for r in rows if r["label"] in labels)
        return n, round(100.0 * n / total, 2)
    groups = {
        "present_ind": pick("Present Ind."),
        "optative": pick("Optative"),
        "imperfect": pick("Imperfect", "Imperfect Med."),
        "imperfect_secondary": pick("Imperfect"),  # the second 4442 row shares a label
        "imperative": pick("Imperative"),
        "imperative_passive": pick("Imper. Passive", "Imperative Passive"),
        "perfect": pick("Perfect"),
        "future": pick("Future Ind."),
        "periphrastic_future": pick("Periph. Future"),
        "conditional": pick("Conditional"),
        "aorist": pick("Aorist Act.", "Aorist Med."),
        "injunctive": pick("Injunctive"),
        "augmentless_imperfect": pick("Augmentless Ipf."),
        "precative_benedictive": pick("Benedictive"),
        "passive_present": pick("Pres. Passive"),
        "ppp": pick("PPP"),
        "past_active_participle": pick("Past Act. Part."),
        "present_active_participle": pick("Pres. Act. Part."),
        "gerundive_fpp": pick("Fut. Pass. Part."),
        "infinitive": pick("Infinitive"),
        "absolutive": pick("Absolutive"),
    }
    cases = {c["case"]: c["total"] for c in d["cases"]}
    nominal_total = d["total_nominal"]
    case_share = {k: round(100.0 * v / nominal_total, 2) for k, v in cases.items()}
    return {
        "total_verbal": total,
        "total_nominal": nominal_total,
        "groups": groups,
        "case_share": case_share,
        "_source": "VisualDCS/tense_case_data.json (DCS-2021, CC BY) — same slice as verify_claims_dcs.py",
    }

# ------------------------------------------------------- form-channel regexes
# Unambiguous IAST surface markers on Devanagari tokens; hits are console
# CANDIDATES for manual adjudication, never dossier rows directly.
FORM_MARKERS = {
    "future":     r"^(?:\w+)(?:sya|iṣya)(?:ti|si|mi|tha|ma|nti|ntu|nte|ntaḥ|tas)$",
    "optative":   r"^(?:\w+)(?:et|yāt|yās|yāma|yāva|yātam|yātan|yur|eyur|etām)$",
    "imperative": r"^(?:\w+)(?:tu|antu|dhi|hi|dhvam|atām)$",
    "absolutive": r"^(?:\w+)(?:tvā|itvā|yatvā|tya)$",
    "gerundive":  r"^(?:\w+)(?:tavya|anīya)$",
    "infinitive": r"^(?:\w+)(?:tum|itum)$",
}

# Instruction channel: the Russian exercise text names the category; generic
# «saṃdhi» is captured with context for variant adjudication.
INSTR_MARKERS = {
    "optative": ["желательн"], "imperative": ["повелительн"], "future": ["будущ"],
    "perfect": ["перфект"], "aorist": ["аорист"], "injunctive": ["инъюнктив"],
    "precative": ["прекатив"], "passive": ["пассив", "страдательн"],
    "causative": ["каузатив", "понудительн"], "desiderative": ["дезидератив"],
    "ppp": ["причастие прошедшего"], "gerundive": ["причастие будущего"],
    "absolutive": ["деепричаст"], "infinitive": ["инфинитив"],
    "sandhi_any": ["saṃdhi", "сандхи"], "compound": ["tatpuruṣa", "karmadhāraya", "bahuvrīhi"],
    "dict_lookup": ["по словарю", "в словаре"],
}

def instr_channel(exercise_lines):
    joined = "\n".join(strip_quote(l) for l in exercise_lines).lower()
    found = {}
    for cat, keys in INSTR_MARKERS.items():
        for k in keys:
            for m in re.finditer(re.escape(k.lower()), joined):
                ctx = joined[max(0, m.start() - 30): m.end() + 40].replace("\n", " ")
                found.setdefault(cat, []).append(ctx)
                break  # one context sample per marker key is enough for adjudication
    return found

def form_channel(text_dev: str):
    hits = {}
    toks = list(deva_tokens(text_dev))
    for t in toks:
        iast = deva_to_iast(t)
        plain = norm_iast(iast)
        if len(plain) < 4:
            continue
        for cat, pat in FORM_MARKERS.items():
            if re.match(pat, iast.lower()):
                hits.setdefault(cat, set()).add(iast)
    return hits, len(toks)

def stem_cover(p, heads):
    """Covered if equal or common prefix >= max(3, len(h)-2) (stem sans ending)."""
    for h in heads:
        if not h:
            continue
        if p == h:
            return h
        k = max(3, len(h) - 2)
        if len(p) >= k and len(h) >= k and p[:k] == h[:k]:
            return h
    return None

# Gloss channel: «Слова» glosses carry grammatical labels («деепричастие от
# jñā», «passiv: dṛśyáte») — requirement evidence, high precision.
GLOSS_MARKERS = {
    "present": [r"\bpr\.?\b"], "imperfect": [r"\bimpf\.?"], "perfect": [r"\bpf\.?"],
    "future": [r"\bfut\.?"], "optative": [r"\bopt\.?", "желательн"],
    "imperative": [r"\bimp\.?", "повелительн"], "aorist": [r"\baor\.?", "аорист"],
    "passive": [r"\bpassiv", "пассив"], "absolutive": ["деепричаст"],
    "infinitive": ["инфинитив"], "ppp": ["причастие прошедшего"], "participle": ["причаст"],
}

def gloss_channel(slova_entries):
    found = {}
    for e in slova_entries:
        g = e["gloss"].lower()
        for cat, pats in GLOSS_MARKERS.items():
            for pat in pats:
                if re.search(pat, g):
                    found.setdefault(cat, []).append(f"{e['iast']} — {e['gloss']}")
                    break
    return found

# Category → first lesson of theoretical introduction (lesson TOCs; the
# «Примечание» at VIII's exercises pins imperfectum=X). TOC citations live in
# the dossier, not here (token gate).
CATEGORY_INTRO = {
    "present_endings": 8, "imperfect": 10, "optative": 12, "imperative": 14,
    "present_stems_them": 15, "present_stems_athem": 16, "future": 18,
    "periphrastic_future": 19, "conditional": 19, "perfect": 21,
    "periphrastic_perfect": 22, "passive": 24, "aorist": 37, "injunctive": 39,
    "precative": 39, "causative": 35, "desiderative": 36,
    "infinitive": 23, "absolutive": 23, "ppp": 25, "gerundive": 25,
    "past_active_part": 26, "present_active_part": 26, "passive_present_part": 24,
    "sandhi_vowel_ext": 7, "sandhi_s_r": 6, "sandhi_int_before_s": 18,
    "sandhi_ext_noisy": 28, "sandhi_int_noisy": 23, "sandhi_int_general": 30,
    "a_stems": 9, "aa_stems": 10, "ii_uu_stems": 12, "ablaut": 13,
    "ar_tar_stems": 19, "cons_stems_3": 28, "cons_stems_2": 29, "cons_stems_0": 30,
    "parallel_stems": 31, "compounds": 32, "numerals": 31, "comparison": 29,
    "prefix_wordformation": 39,
}

# DCS-2021 category join (key = CATEGORY_INTRO key where a corpus share exists).
DCS_CATEGORY = {
    "present_endings": "present_ind", "optative": "optative", "imperfect": "imperfect",
    "imperative": "imperative", "future": "future", "periphrastic_future": "periphrastic_future",
    "conditional": "conditional", "perfect": "perfect", "periphrastic_perfect": None,
    "passive": "passive_present", "aorist": "aorist", "injunctive": "injunctive",
    "precative": "precative_benedictive", "desiderative": None, "causative": None,
    "infinitive": "infinitive", "absolutive": "absolutive", "ppp": "ppp",
    "gerundive": "gerundive_fpp", "past_active_part": "past_active_participle",
    "present_active_part": "present_active_participle", "passive_present_part": None,
}

# ------------------------------------------------------------------- main
def main():
    lines = MDX.read_text(encoding="utf-8").splitlines()

    dict_start = next(i for i, l in enumerate(lines) if l.strip() == "## Словарь")
    lessons = parse_lessons(lines)
    dictionary = parse_dictionary(lines, dict_start)
    dcs = dcs_slice()

    dict_by_plain = {}
    for e in dictionary:
        if len(e["iast_plain"]) >= 2 and e["iast_plain"] not in dict_by_plain:
            dict_by_plain[e["iast_plain"]] = e

    report = {"lessons": [], "dcs": dcs, "dictionary": {},
    "method_notes": "normalized IAST, accents stripped; dict match = exact or stem-prefix >=3; lexical scope from lesson VII; form/instr/gloss channels are console-candidates for hand adjudication (committed JSON carries counts only)"}

    seen_slova_plain = set()   # cumulative across lessons (order = lesson order)
    seen_text_plain = set()
    dict_used = set()

    for L in sorted(lessons, key=lambda x: x["n"]):
        end = min([x["start"] for x in lessons if x["n"] > L["n"]] + [dict_start])
        body = lines[L["start"] + 1: end]
        ex_start = L["exercise_start"]
        ex_lines = lines[ex_start: end] if ex_start else []
        n_ex = 0
        want = 1
        for l in ex_lines:
            m = EX_HEAD_RE.match(strip_quote(l))
            if not m:
                continue
            r = m.group(1)
            if ROMANS.get(r) == want:
                n_ex += 1
                want += 1
        slova_entries = [e for blk in L["slova_blocks"] for e in blk["entries"]]
        slova_plain = []
        for e in slova_entries:
            head = re.split(r"[,;]", e["iast"])[0].strip()
            slova_plain.append(norm_iast(head))
        slova_set = set(p for p in slova_plain if p)

        text_tokens = [t for l in body for t in deva_tokens(strip_quote(l))]
        text_plain = [norm_iast(deva_to_iast(t)) for t in text_tokens]
        text_plain = [p for p in text_plain if p]

        out_of_glossary = []
        in_glossary = 0
        if L["n"] >= 7:
            for p in set(text_plain):
                if stem_cover(p, slova_set):
                    in_glossary += 1
                else:
                    out_of_glossary.append(p)
        dict_missing = []
        for p in sorted(set(out_of_glossary)):
            key = p if p in dict_by_plain else next(
                (k for k in dict_by_plain if len(k) >= 3 and p.startswith(k)), None)
            if key is None:
                dict_missing.append(p)
            else:
                dict_used.add(key)
        # dictionary usage from glossary + matched tokens (for Q3)
        for s in slova_set:
            if s in dict_by_plain:
                dict_used.add(s)
            else:
                stem = next((k for k in dict_by_plain if len(k) >= 3 and s.startswith(k)), None)
                if stem:
                    dict_used.add(stem)
        reused = [p for p in sorted(slova_set) if p and (p in seen_slova_plain or p in seen_text_plain)]
        new_words = [p for p in sorted(slova_set) if p and p not in set(reused)]

        seen_slova_plain.update(p for p in slova_set if p)
        seen_text_plain.update(text_plain)

        scan_src = "\n".join(ex_lines) if ex_start else "\n".join(body)
        fc, tok_count = form_channel(scan_src)
        ic = instr_channel(ex_lines) if ex_start else {}
        gc = gloss_channel(slova_entries)

        report["lessons"].append({
            "n": L["n"], "roman": L["roman"], "toc_n": len(L["toc"]),
            "exercise_present": bool(ex_start), "n_exercises": n_ex,
            "slova_blocks": len(L["slova_blocks"]), "slova_entries": len(slova_entries),
            "text_token_count": tok_count, "text_types": len(set(text_plain)),
            "in_glossary_types": in_glossary, "out_of_glossary_types": len(out_of_glossary),
            "dict_missing_count": len(dict_missing),
            "reused": len(reused), "new": len(new_words),
            "reused_share_pct": round(100.0 * len(reused) / len(slova_set), 1) if slova_set else None,
        })

    # Q3 never-used: check plain IAST AND Devanagari forms as substrings of the
    # lesson range (manual sample: IAST-only sweep missed ~1/15 Devanagari-only).
    lesson_range_text = "\n".join(lines[:dict_start])
    never_used = []
    for e in dictionary:
        k = e["iast_plain"]
        if len(k) < 3:
            continue
        if k in dict_used or any(u.startswith(k) for u in dict_used):
            continue
        dev = transliterate(e["iast"], sanscript.IAST, sanscript.DEVANAGARI)
        if k in lesson_range_text or dev in lesson_range_text:
            dict_used.add(k)
            continue
        never_used.append(e["iast"])
    report["dictionary"]["never_used_count"] = len(never_used)
    report["dictionary"]["never_used_sample"] = never_used[:15]

    freq_rows = []
    for key, lesson in CATEGORY_INTRO.items():
        dg = DCS_CATEGORY.get(key)
        share = dcs["groups"][dg][1] if dg and dg in dcs["groups"] else None
        freq_rows.append({"category": key, "intro_lesson": lesson, "dcs_share_pct": share})
    try:
        from scipy.stats import spearmanr
        pts = [(r["intro_lesson"], r["dcs_share_pct"]) for r in freq_rows if r["dcs_share_pct"] is not None]
        rho, pval = spearmanr([x[0] for x in pts], [x[1] for x in pts])
        corr = {"n": len(pts), "rho": round(float(rho), 4), "p": float(pval)}
    except Exception as exc:  # pragma: no cover
        corr = {"error": str(exc)}
    report["category_intro_dcs"] = {"rows": freq_rows, "spearman_lesson_vs_share": corr}

    OUT.write_text(json.dumps(report, ensure_ascii=False, separators=(',', ':')),
                   encoding="utf-8")

    print(f"lessons={len(lessons)} dict_entries={len(dictionary)} unique_plain={len(dict_by_plain)}")
    for L in report["lessons"]:
        print(f"  {L['n']:>2} {L['roman']:<5} toc={L['toc_n']} ex={L['n_exercises']:>2}"
              f" slova={L['slova_entries']:>3} toks={L['text_token_count']:>4}"
              f" out={L['out_of_glossary_types']:>3} reuse={L['reused_share_pct']}")
    print(f"never_used={len(never_used)}")

if __name__ == "__main__":
    sys.exit(main())
