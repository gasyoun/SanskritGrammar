#!/usr/bin/env python3
"""commentary_corpus.py — thematic search over the Pāṇinian commentary corpus.

Backs the /panini-commentary-corpus skill. This is the LAYER ABOVE
panini_sutra.py (H413): panini_sutra.py resolves a sūtra by *number* and prints
its per-sūtra commentaries; this tool searches the commentary corpus by
*root or concept* — "which sūtras discuss X, and what did Kātyāyana / Patañjali /
the Kāśikā say about it" — and synthesizes a commentator frame (school, the
sūtra→vārttika→bhāṣya→Kāśikā chain, who contested/extended, and which authorities
stand behind the classification), with a secondary-literature pointer to
Cardona 1997 / Staal 1985 / Scharfe 1977 for the topic.

Answers the RWS `lidova-commentary` edit (RWS_REPORT.md §6.7): "указать школу,
показать, как бхашьи/варттики развивали или оспаривали взгляды на корни, какие
авторитеты стояли за классификациями" — которая вручную неописуема.

Canonical data (no scraping):
  - ashtadhyayi-com/data sutraani/{data,bhashya,kashika,vartika}.txt — the same
    dataset panini_sutra.py caches under panini_cache/.
  - secondary_lit.json (sibling file) — the curated topic→bibliography pointer
    index (pointers only, not full text — rights).

Modes:
  --search TERM     which sūtras' commentary/sūtra-text contain TERM (Devanagari
                    or roman — IAST/HK/SLP1 auto-detected and transliterated).
  --frame  TERM     the synthesized commentator frame for the top hits + the
                    secondary-literature pointers for the topic.
  --biblio [TOPIC]  the secondary-literature pointer index (all, or one topic).

TERM may be Devanagari (धातु), IAST (dhātu), Harvard-Kyoto (dhAtu), or SLP1.
"""
import sys
import os
import json
import argparse

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))

# Reuse the H413 fetch/cache/util layer instead of re-deriving it.
sys.path.insert(0, HERE)
from panini_sutra import fetch, strip_html, sid  # noqa: E402

CACHE = os.path.join(HERE, "panini_cache")
LIT = os.path.join(HERE, "secondary_lit.json")

# Layers keyed by 5-digit sūtra id (schema: {"11001": "text", ...}).
PERSUTRA = {
    "bhashya": ("Mahābhāṣya (Patañjali)", "bhashya.txt"),
    "kashika": ("Kāśikā-vṛtti", "kashika.txt"),
}
# Vārttika layer has its own schema: {"data":[{"sutra":"1.1.9","vartika":"…"}]}.
VARTIKA_FILE = "vartika.txt"


def load_core():
    """Sūtra id -> {a,p,n,s,e} from data.txt."""
    raw = fetch("data.txt")
    if raw is None:
        return {}
    obj = json.loads(raw)
    idx = {}
    for row in obj.get("data", []):
        if isinstance(row, dict) and row.get("i"):
            idx[str(row["i"])] = row
    return idx


def load_persutra(fname):
    """Commentary keyed by 5-digit id -> plain text."""
    raw = fetch(fname)
    if raw is None:
        return {}
    obj = json.loads(raw)
    out = {}
    for k, v in obj.items():
        if k in ("name", "data"):
            continue
        if isinstance(v, str):
            out[str(k)] = strip_html(v)
    return out


def load_vartika():
    """Vārttikas grouped by 5-digit sūtra id -> list[str].

    vartika.txt is {"data":[{"sutra":"1.1.9","vartika":"…"}]} — keyed by the
    a.p.n reference string, NOT the 5-digit id used by the other layers, so it
    needs its own loader (panini_sutra.load_json_list mis-handles this schema
    and silently indexes nothing — that is why --commentary vārttika came back
    empty in H413).
    """
    raw = fetch(VARTIKA_FILE)
    if raw is None:
        return {}
    obj = json.loads(raw)
    out = {}
    for row in obj.get("data", []):
        if not isinstance(row, dict):
            continue
        ref = str(row.get("sutra", "")).strip()
        txt = strip_html(str(row.get("vartika", "")).strip())
        if not ref or not txt:
            continue
        parts = ref.replace(",", ".").split(".")
        if len(parts) != 3:
            continue
        try:
            key = sid(*parts)
        except (ValueError, TypeError):
            continue
        out.setdefault(key, []).append(txt)
    return out


def to_devanagari(term):
    """Return the Devanagari form of a roman term (idempotent for Devanagari)."""
    try:
        from vidyut.lipi import detect, transliterate, Scheme
    except ImportError:
        return None
    try:
        scheme = detect(term)
    except Exception:  # noqa: BLE001
        scheme = None
    if scheme == Scheme.Devanagari:
        return term
    if scheme is None:
        return None
    try:
        return transliterate(term, scheme, Scheme.Devanagari)
    except Exception:  # noqa: BLE001
        return None


def search_variants(term):
    """The Devanagari needles to match: the term as given, its Devanagari
    transliteration, and that form with a trailing virāma stripped (so a cited
    root like भू matches भू in-word)."""
    needles = []
    is_deva = any("ऀ" <= c <= "ॿ" for c in term)
    if is_deva:
        needles.append(term)
    deva = to_devanagari(term)
    if deva and deva not in needles:
        needles.append(deva)
    # strip trailing virāma for looser stem matching
    for n in list(needles):
        if n.endswith("्"):
            stem = n[:-1]
            if stem and stem not in needles:
                needles.append(stem)
    # de-dup, keep order
    seen, out = set(), []
    for n in needles:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out


def snippet(text, needle, width=90):
    i = text.find(needle)
    if i < 0:
        return text[:width].strip() + ("…" if len(text) > width else "")
    a = max(0, i - width // 2)
    b = min(len(text), i + len(needle) + width // 2)
    return ("…" if a else "") + text[a:b].strip() + ("…" if b < len(text) else "")


def cite(a, p, n):
    return f"{a}.{p}.{n}"


def do_search(term, layers, limit):
    core = load_core()
    if not core:
        print("Нет данных сутр — проверьте сеть/кэш.", file=sys.stderr)
        sys.exit(1)
    needles = search_variants(term)
    if not needles:
        print(f"Не удалось интерпретировать «{term}» "
              f"(нужна деванагари, IAST, HK или SLP1; vidyut не найден?).",
              file=sys.stderr)
        sys.exit(2)

    corpus = {}
    if "bhashya" in layers:
        corpus["bhashya"] = load_persutra("bhashya.txt")
    if "kashika" in layers:
        corpus["kashika"] = load_persutra("kashika.txt")
    if "vartika" in layers:
        corpus["vartika"] = load_vartika()

    hits = []  # (key, {layer: snippet}, matched_sutra_text_bool)
    for key, row in core.items():
        matched = {}
        # sūtra text itself
        stext = f"{row.get('s', '')} {row.get('e', '')}"
        if any(nd in stext for nd in needles):
            matched["sūtra"] = snippet(row.get("s", ""), needles[0])
        for layer, idx in corpus.items():
            entry = idx.get(key)
            if entry is None:
                continue
            texts = entry if isinstance(entry, list) else [entry]
            joined = "\n".join(texts)
            for nd in needles:
                if nd in joined:
                    matched[layer] = snippet(joined, nd)
                    break
        if matched:
            hits.append((key, row, matched))

    # rank: more layers matched first, then by sūtra order
    hits.sort(key=lambda h: (-len(h[2]), h[0]))

    label = ", ".join(needles)
    print(f"_{len(hits)} сутр(ы) с обсуждением «{term}» "
          f"(деванагари-иглы: {label}); показаны первые "
          f"{min(limit, len(hits))}._\n")
    layer_names = {
        "sūtra": "сутра", "bhashya": "Mahābhāṣya", "kashika": "Kāśikā",
        "vartika": "Vārttika (Kātyāyana)",
    }
    for key, row, matched in hits[:limit]:
        c = cite(row["a"], row["p"], row["n"])
        print(f"### Aṣṭādhyāyī {c} — {row.get('s', '')}")
        print(f"- **IAST:** {row.get('e', '')}")
        print(f"- **цитата:** `ср. Aṣṭādhyāyī {c}` · "
              f"https://ashtadhyayi.com/sutraani/{row['a']}/{row['p']}/{row['n']}")
        for layer in ("sūtra", "vartika", "bhashya", "kashika"):
            if layer in matched:
                print(f"- **{layer_names[layer]}:** {matched[layer]}")
        print()
    return hits


def load_lit():
    with open(LIT, encoding="utf-8") as f:
        return json.load(f)


def match_topic(term, lit):
    """Best topic match for a term (roman lower-cased or Devanagari substring)."""
    tl = term.strip().lower()
    deva = to_devanagari(term) or ""
    best = None
    for topic in lit["topics"]:
        for m in topic["match"]:
            ml = m.lower()
            if ml == tl or ml in tl or tl in ml or (deva and m in deva) \
                    or (any("ऀ" <= c <= "ॿ" for c in m)
                        and m in (deva or term)):
                return topic
    return best


def do_frame(term, limit):
    lit = load_lit()
    topic = match_topic(term, lit)
    hits = do_search(term, {"bhashya", "kashika", "vartika"}, limit)

    print("---\n")
    print(f"## Комментаторская рамка: «{term}»\n")
    print("**Школа.** Пāṇинийская грамматика (vyākaraṇa). Цепь толкования на "
          "каждое правило: **сутра (Pāṇini)** → **вартика (Kātyāyana)** — "
          "критическое замечание (ukta / anukta / durukta) → **бхашья "
          "(Patañjali, Mahābhāṣya)** — разбор pūrvapakṣa/siddhānta, "
          "выносящий итоговый взгляд школы → **Kāśikā-vṛtti** — сводная "
          "поздняя вритти.\n")

    if topic:
        print(f"**Тема ({topic['id']}).** {topic['frame_note']}\n")
        print("**Что развивали/оспаривали комментаторы.** Вартики Катьяяны на "
              "сутры выше показывают, где правило Панини уточнялось или "
              "оспаривалось; бхашья Патанджали адъюдицирует спор и фиксирует "
              "siddhānta — именно этот слой отвечает на вопрос «какой взгляд "
              "стоит за классификацией».\n")
        print("**Авторитеты за классификацией (secondary literature — "
              "указатели, сверить постранично по печатному экземпляру):**\n")
        print(f"- **Cardona 1997:** {topic['cardona1997']}. — _cр._ "
              f"Cardona, George (1997). *Pāṇini: A Survey of Research*. "
              f"Delhi: Motilal Banarsidass.")
        print(f"- **Staal 1985**: {topic['staal1985']}. — _cр._ Staal, J. F. "
              f"(ed.) (1985). *A Reader on Sanskrit Grammarians*. Delhi: MLBD.")
        print(f"- **Scharfe 1977**: {topic['scharfe1977']}. — _cр._ Scharfe, "
              f"Hartmut (1977). *Grammatical Literature*. Wiesbaden: "
              f"Harrassowitz (HIL V.2).")
        print()
        print("_Пример сноски для диссертации:_ «В пāṇинийской традиции "
              f"понятие обсуждается в цепи сутра→вартика→бхашья (см. сутры "
              f"выше); ср. Cardona 1997, {topic['cardona1997']}.»\n")
    else:
        print(f"_Тема «{term}» не сопоставлена с курируемым указателем "
              f"secondary_lit.json — приведены только корпусные совпадения "
              f"выше. Для библио-указателя запустите "
              f"`--biblio` и выберите ближайшую тему; общий обзор — "
              f"Cardona, George (1997). Pāṇini: A Survey of Research._\n")


def do_biblio(topic_id):
    lit = load_lit()
    print("## Указатель вторичной литературы (пойнтеры, не полный текст)\n")
    print(f"_{lit['_about']}_\n")
    for w in ("cardona1997", "staal1985", "scharfe1977"):
        print(f"- {lit['_works'][w]}")
    print()
    shown = 0
    for topic in lit["topics"]:
        if topic_id and topic_id.lower() not in (
                [topic["id"].lower()] + [m.lower() for m in topic["match"]]):
            continue
        shown += 1
        print(f"### {topic['id']}\n")
        print(f"- **Cardona 1997:** {topic['cardona1997']}")
        print(f"- **Staal 1985:** {topic['staal1985']}")
        print(f"- **Scharfe 1977:** {topic['scharfe1977']}")
        print(f"- **рамка:** {topic['frame_note']}")
        print()
    if topic_id and not shown:
        ids = ", ".join(t["id"] for t in lit["topics"])
        print(f"Тема «{topic_id}» не найдена. Доступны: {ids}.")


def main():
    ap = argparse.ArgumentParser(
        description="Тематический поиск по корпусу пāṇинийских комментаторов.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--search", metavar="TERM",
                   help="какие сутры обсуждают TERM (деванагари/IAST/HK/SLP1)")
    g.add_argument("--frame", metavar="TERM",
                   help="синтез комментаторской рамки + библио-указатели")
    g.add_argument("--biblio", nargs="?", const="", metavar="TOPIC",
                   help="указатель вторичной литературы (весь / по теме)")
    ap.add_argument("--layer", default="all",
                    help="слои для --search: all | bhashya,vartika,kashika")
    ap.add_argument("--limit", type=int, default=8, help="макс. число сутр")
    args = ap.parse_args()

    if args.search is not None:
        if args.layer == "all":
            layers = {"bhashya", "vartika", "kashika"}
        else:
            layers = {x.strip() for x in args.layer.split(",") if x.strip()}
        do_search(args.search, layers, args.limit)
    elif args.frame is not None:
        do_frame(args.frame, args.limit)
    else:
        do_biblio(args.biblio or None)


if __name__ == "__main__":
    main()
