#!/usr/bin/env python3
"""Build the LessonConcordance/ page — the per-lesson cross-source concordance of
Bühler's «Руководство к элементарному курсу санскритского языка» (1923, 48 уроков).

This is the LESSON counterpart to SubjectConcordance/ (subject spine) and
Concordance/ (shared exercise sentences): for each Bühler lesson and each curated
topic inside it, it lists the matching locus in every other digitized source on
the site (Whitney §§, Kochergina занятие, Knauer Nr., Zaliznyak §§, Sangram,
Apte/Speyer/dhatu/talmud/frish where applicable), plus the lemma-coverage layer
(D2 vote) and the per-topic exception-coverage verdicts testing MG's hypothesis.

Inputs (hand-curated or register-seeded):
  - LessonConcordance/topics.yml — topic vocabulary, exception verdicts, lemma table
  - LessonConcordance/typed_link_buhler_lessons.tsv — Type-D link rows (10 columns,
    TYPED_LINK_ID_GRAMMAR.md §1 shape), linted by kosha/scripts/typed_link_lint.py

Generated — do NOT hand-edit LessonConcordance/catalog.mdx; re-run this script.
"""
import json
import os
import re
import sys
import urllib.parse
from collections import defaultdict

import yaml

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "LessonConcordance")
TSV = os.path.join(OUT_DIR, "typed_link_buhler_lessons.tsv")
TOPICS = os.path.join(OUT_DIR, "topics.yml")
CLAIMS = os.path.join(ROOT, "BuhlerLeitfaden_1923", "claims.yml")
BACKLINKS_JSON = os.path.join(ROOT, "src", "lesson-backlinks.json")

GH = "https://github.com/gasyoun/SanskritGrammar/blob/main"
CLAIMS_BLOB = GH + "/BuhlerLeitfaden_1923/claims.yml"
WITNESS_DOC = GH + "/WHITNEY_CONCORDANCE_SANGRAM_KOCHERGINA_2026.md"
CROSSWALK_CSV = GH + "/TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv"

# Страницы-источники, в конец которых попадает <LessonBacklinks page="…"/> (E3–E4).
SOURCE_PAGES = {
    "kochergina": "KocherginaUchebnik_1998/Kochergina_unicode",
    "knauer": "KnauerFrazy_1908/Frazy-Knauer-03.05.2023",
    "ocherk": "ZalizniakOcherk_1978/Zalizniak-Ocherk_29-11-20-aligned",
    "dhatu-glava7": "GasunsDhatu_2014/07_glava7_ukazatel-zaliznyaka",
    "sangram-thematic-present": "sangram/articles/thematic-present",
    "sangram-conjugation-overview": "sangram/articles/conjugation-overview",
    "buhler": "BuhlerLeitfaden_1923/Buhler_Unicode",
}

TARGET_LABELS = {
    "whitney-sec": "Уитни 1889",
    "zalizniak-1978-sec": "Зализняк, Очерк 1978",
    "zalizniak-1975": "Зализняк 1975",
    "zalizniak-2004": "Зализняк, Конспект 2004",
    "kochergina-lesson": "Кочергина 1998",
    "knauer-fraza": "Кнауэр, Frazy 1908",
    "sangram-article": "Sangram",
    "apte": "Apte 1885 (синтаксис)",
    "speyer": "Speyer 1886 (синтаксис)",
    "dhatu": "Гасунс, Dhātu 2014",
    "talmud": "Толчельников 2026 (morphoclass)",
    "frish": "Фриш, хрестоматия",
}


SITE = "https://gasyoun.github.io/SanskritGrammar/grammars"
GH = "https://github.com/gasyoun/SanskritGrammar/blob/main"

# Whitney § → глава (диапазоны глав — спайн whitney_sections.json). На сайте
# страницы глав Уитни НЕ сервятся (только 404), §-ссылки в mdx ведут на
# Wikisource с якорями заголовков — глубокая ссылка = Wikisource Chapter#§.
WHITNEY_CHAPTERS = [
    (1, 18, "I"), (19, 97, "II"), (98, 260, "III"), (261, 320, "IV"),
    (321, 474, "V"), (475, 489, "VI"), (490, 526, "VII"), (527, 598, "VIII"),
    (599, 779, "IX"), (780, 823, "X"), (824, 930, "XI"), (931, 950, "XII"),
    (951, 995, "XIII"), (996, 1068, "XIV"), (1069, 1095, "XV"),
    (1096, 1135, "XVI"), (1136, 1245, "XVII"), (1246, 1316, "XVIII"),
]
WIKISOURCE = "https://en.wikisource.org/wiki/Sanskrit_Grammar_(Whitney)"

# Точная фраза на странице источника для подсветки (:~:text=) — первое вхождение.
KOCHERGINA_SPOTS = {
    "VI": "В конце предложения или стихотворной строки",
    "VIII": "Для образования форм настоящего времени",
    "XV": "Есть несколько глаголов I класса",
}
KNAUER_SPOTS = {
    "Nr.1": "личныя окончанія",
    "Nr.2": "ṛṣir duḥkhāt",
}


def frag(s):
    """Scroll-To-Text fragment — браузер сам подсвечивает фоном найденную фразу."""
    return "#:~:text=" + urllib.parse.quote(s, safe="")


# Локальные файлы источников для build-валидации spot-фраз (E12): фраза должна
# существовать в тексте источника — дрейф текста валит сборку, а не остаётся
# тихо пропавшей подсветкой. Внешние (Wikisource, GitHub CSV) не валидируются.
LOCAL_SOURCE_FILES = {
    "kochergina": "KocherginaUchebnik_1998/Kochergina_unicode.mdx",
    "knauer": "KnauerFrazy_1908/Frazy-Knauer-03.05.2023.mdx",
    "ocherk": "ZalizniakOcherk_1978/Zalizniak-Ocherk_29-11-20-aligned.mdx",
    "dhatu-glava7": "GasunsDhatu_2014/07_glava7_ukazatel-zaliznyaka.mdx",
    "sangram-conjugation-overview": "sangram/articles/conjugation-overview/index.mdx",
}


def target_url(locus, spot=None):
    """Глубокая ссылка: страница источника на сайте + текст-фрагмент, подсвечивающий
    куда именно смотреть (E10: spot = курируемая фраза-утверждение из topics.yml,
    не номер параграфа — МГ 02-10; fallback — §/занятие, если фразы для локуса
    нет). Для данных без страницы на сайте — файл в репо (GitHub)."""
    prefix, _, tail = locus.partition(":")
    if prefix == "whitney-sec":
        lo = tail.split("-")[0]
        chapter = next((rn for a, b, rn in WHITNEY_CHAPTERS if a <= int(lo) <= b), None)
        if chapter:
            # <>-обёртка обязательна: в URL Wikisource есть скобки (Whitney)
            return (f"<{WIKISOURCE}/Chapter_{chapter}#{lo}>",
                    "§§ " + tail.replace("-", "–"))
        return f"{GH}/WhitneyGrammar_1889/", "§§ " + tail.replace("-", "–")
    if prefix == "zalizniak-1978-sec":
        first = tail.split("-")[0]
        phrase = spot or "§ " + first
        return (f"{SITE}/ZalizniakOcherk_1978/Zalizniak-Ocherk_29-11-20-aligned{frag(phrase)}",
                "§§ " + tail.replace("-", "–"))
    if prefix == "zalizniak-1975" or prefix == "zalizniak-2004":
        return f"{GH}/{'ZalizniakMorphology_1975' if prefix == 'zalizniak-1975' else 'ZalizniakKonspekt_2004'}/", tail
    if prefix == "kochergina-lesson":
        phrase = spot or KOCHERGINA_SPOTS.get(tail, "Занятие " + tail)
        return (f"{SITE}/KocherginaUchebnik_1998/Kochergina_unicode{frag(phrase)}",
                "Занятие " + tail)
    if prefix == "knauer-fraza":
        phrase = spot or KNAUER_SPOTS.get(tail, tail)
        return (f"{SITE}/KnauerFrazy_1908/Frazy-Knauer-03.05.2023{frag(phrase)}",
                tail)
    if prefix == "sangram-article":
        return (f"{SITE}/sangram/articles/{tail}{frag(spot) if spot else ''}", tail)
    if prefix == "apte" or prefix == "speyer":
        return f"{GH}/{'ApteSyntax_1885' if prefix == 'apte' else 'SpeyerSyntax_1886'}/", "§ " + tail
    if prefix == "dhatu":
        if tail.startswith("glava"):
            return (f"{SITE}/GasunsDhatu_2014/{tail.replace('-', '_', 1)}{frag(spot) if spot else ''}", tail)
        return f"{GH}/GasunsDhatu_2014/", tail
    if prefix == "talmud":
        if tail == "morphoclass-crosswalk-1975-2014-2026":
            return (f"{GH}/TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv", tail)
        return f"{GH}/TolchelnikovTalmud_2026/", tail
    if prefix == "subject":
        return f"{SITE}/SubjectConcordance/catalog{frag('Present, a-class')}", tail
    if prefix == "frish":
        return f"{GH}/BibliothecaSanscritica/", tail
    return None, locus


def load_rows():
    rows = []
    with open(TSV, encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            rows.append(dict(zip(header, line.split("\t"))))
    return rows


def claims_line_index():
    """{HB-id: строка claims.yml} — для GitHub #L-якорей указателей (E5)."""
    index = {}
    hid = None
    with open(CLAIMS, encoding="utf-8") as fh:
        for ln, line in enumerate(fh, 1):
            m = re.match(r"  - id:\s*(HB-\d+)", line)
            if m:
                hid = m.group(1)
                index[hid] = ln
    return index


def locus_page(prefix, tail):
    """target_locus → ключ страницы-источника для бэклинка (страниц нет у
    Wikisource-Уитни и talmud-CSV)."""
    if prefix == "kochergina-lesson":
        return "kochergina"
    if prefix == "knauer-fraza":
        return "knauer"
    if prefix == "zalizniak-1978-sec":
        return "ocherk"
    if prefix == "dhatu" and tail.startswith("glava"):
        return "dhatu-glava7"
    if prefix == "sangram-article":
        return "sangram-" + tail
    return None


def main():
    with open(TOPICS, encoding="utf-8") as fh:
        topics_doc = yaml.safe_load(fh)

    by_anchor = defaultdict(list)
    for row in load_rows():
        by_anchor[row["anchor_id"]].append(row)

    claim_lines = claims_line_index()

    def claim_link(hid):
        line = claim_lines.get(hid)
        return f"[{hid}]({CLAIMS_BLOB}#L{line})" if line else hid

    # Карта обратных ссылок (E3–E4): страница источника → темы уроков.
    backlinks = {"pages": defaultdict(list)}

    out = []
    out.append("---")
    out.append('title: "Поурочный конкорданс Бюлера: урок × все источники"')
    out.append('sidebar_label: "Поурочный конкорданс Бюлера"')
    out.append("---")
    out.append("")
    out.append("# Поурочный конкорданс Бюлера: урок × все источники")
    out.append("")
    out.append("Для каждого урока [Бюлера-1923](https://gasyoun.github.io/SanskritGrammar/grammars/BuhlerLeitfaden_1923/Buhler_Unicode/)"
               " и каждой темы внутри него — соответствующий локус в остальных оцифрованных"
               " источниках сайта; план и решения D1–D16 + адденда перелинковки E1–E9: "
               "[BUHLER_LESSON_CONCORDANCE_PLAN_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/BUHLER_LESSON_CONCORDANCE_PLAN_2026.md)."
               " Гипотеза МГ об исключениях проверяется по каждой теме (блок «Исключения»);"
               " карта связей книг — [GrammarRelations](https://gasyoun.github.io/SanskritGrammar/grammars/GrammarRelations/grammar-relations-map).")
    out.append("")
    n_all = 48
    landed = ", ".join(f"**{rn}**" for rn in topics_doc["lessons"])
    out.append(f"*Уроки ({n_all}): {landed} — остальные по мере batch-минта (E8: каркас на 48).*")
    out.append("")

    for rn, lesson in topics_doc["lessons"].items():
        out.append(f"## Урок {rn} — {lesson['title']}")
        out.append("")
        out.append(f"*Локус текста:* {lesson['mdx']}")
        out.append("")
        # бэклинк со страницы самого Бюлера (E3)
        backlinks["pages"]["buhler"].append(
            {"label": f"урок {rn} — конкорданс", "spot": f"УРОК {rn}."})
        topic_list = [t["key"] for t in lesson["topics"]]
        for ti, topic in enumerate(lesson["topics"]):
            anchor_id = f"buhler-topic:{rn}.{topic['key']}"
            rows = by_anchor.get(anchor_id, [])
            for row in rows:
                prefix, _, tail = row["target_locus"].partition(":")
                page = locus_page(prefix, tail)
                if page:
                    backlinks["pages"][page].append(
                        {"label": f"урок {rn} — {topic['key']}",
                         "spot": topic["title"][:60]})
            out.append(f"### {topic['title']}")
            out.append("")
            out.append(f"*Бюлер:* {topic['buhler_locus']}")
            out.append("")
            out.append("*Темы урока (" + f"{ti + 1}/{len(topic_list)}):* "
                       + " · ".join(
                           (f"**{k}**" if k == topic["key"] else
                            f"[{k}]({frag(t['title'][:40])})")
                           for k, t in zip(topic_list, lesson["topics"])))
            out.append("")
            if rows:
                spots = topic.get("spots") or {}
                out.append("| Источник | Локус | Уверенность | Строк-доказательств |")
                out.append("|---|---|---|---|")
                for row in rows:
                    prefix, _, tail = row["target_locus"].partition(":")
                    label = TARGET_LABELS.get(prefix, prefix)
                    spot = spots.get(row["target_locus"])
                    url, display = target_url(row["target_locus"], spot)
                    loc = f"[{display}]({url})" if url else display
                    ev = row.get("evidence_count") or "—"
                    out.append(f"| {label} | {loc} | {row['confidence']} | {ev} |")
                out.append("")
            exc = topic.get("exceptions", {})
            if exc:
                out.append("**Исключения** (гипотеза: «у Бюлера много, у Зализняка-1978 нет, у Уитни всегда?»):"
                           f" **{exc.get('verdict', '—')}**")
                out.append("")
                for who in ("buhler", "whitney", "zalizniak-1978", "kochergina"):
                    if exc.get(who):
                        out.append(f"- **{who}**: {exc[who]}")
                out.append("")
                out.append(f"*Свидетели по теме (4-witness сетка):* [{os.path.basename(WITNESS_DOC)}]({WITNESS_DOC})")
                out.append("")
            if topic.get("lemmas"):
                out.append(f"*Лемма-слой (ряды — только у Зализняка; у Кочергиной класс при глаголе, МГ 02-10):* "
                           f"[crosswalk 1975↔2014↔2026]({CROSSWALK_CSV})")
                out.append("")
                out.append("| Корень | Глосса | З-1975 | З-1978 | crosswalk |")
                out.append("|---|---|---|---|---|")
                for lem in topic["lemmas"]:
                    out.append(f"| {lem['root']} | {lem['gloss']} | {lem['z1975']} | {lem['z1978']} | {lem['crosswalk']} |")
                out.append("")
            tc = topic.get("topic_claims") or []
            if tc:
                out.append("*HB-утверждения темы:* " + ", ".join(claim_link(c) for c in tc)
                           + f" (реестр — [{os.path.basename(CLAIMS)}]({CLAIMS_BLOB}))")
                out.append("")
            if topic.get("notes"):
                out.append(f"*Примечание:* {topic['notes']}")
                out.append("")
        reg = lesson.get("claims") or []
        if reg:
            cl = ", ".join(claim_link(c) for c in reg)
            out.append(f"*Регистр утверждений урока:* {cl}")
            out.append("")

    # Техническая плашка — в самый низ, серым и мельче (МГ, 02-10-2026: «в самый
    # вниз, всегда, серым и мельче кегль… они не настолько важны»).
    out.append("")
    out.append('<small style={{color: "var(--ifm-color-emphasis-600)"}}>Сгенерировано '
               '<a href="https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_lesson_concordance.py">'
               'scripts/build_lesson_concordance.py</a> из '
               '<a href="https://github.com/gasyoun/SanskritGrammar/blob/main/LessonConcordance/topics.yml">topics.yml</a>'
               ' + <a href="https://github.com/gasyoun/SanskritGrammar/blob/main/LessonConcordance/'
               'typed_link_buhler_lessons.tsv">typed_link_buhler_lessons.tsv</a> — не редактировать руками; '
               'перегенерация: <code>python3 scripts/build_lesson_concordance.py</code>. '
               'Ссылки локусов ведут на точное место источника с подсветкой (:~:text-фрагмент, '
               'Chrome/Firefox/Safari 18.2+).</small>')
    out.append("")

    page = "\n".join(out) + "\n"
    with open(os.path.join(OUT_DIR, "catalog.mdx"), "w", encoding="utf-8") as fh:
        fh.write(page)

    os.makedirs(os.path.dirname(BACKLINKS_JSON), exist_ok=True)
    with open(BACKLINKS_JSON, "w", encoding="utf-8") as fh:
        json.dump({"pages": dict(backlinks["pages"])}, fh, ensure_ascii=False, indent=2)

    # E12: build-валидация spot-фраз против локальных текстов источников.
    ok, external = 0, 0
    cache = {}
    for rn, lesson in topics_doc["lessons"].items():
        for topic in lesson["topics"]:
            for locus, phrase in (topic.get("spots") or {}).items():
                page = locus_page(*locus.partition(":")[::2])
                if page not in LOCAL_SOURCE_FILES:
                    external += 1
                    continue
                if page not in cache:
                    cache[page] = open(os.path.join(ROOT, LOCAL_SOURCE_FILES[page]),
                                       encoding="utf-8").read()
                if phrase not in cache[page]:
                    print(f"SPOT-FAIL: фраза не найдена в {LOCAL_SOURCE_FILES[page]}: «{phrase}» "
                          f"(локус {locus}, урок {rn})", file=sys.stderr)
                    sys.exit(1)
                ok += 1
    print(f"spots validated: {ok} local OK, {external} external (Wikisource/CSV — якоря заголовков/файл)")

    n_rows = sum(len(v) for v in by_anchor.values())
    print(f"LessonConcordance/catalog.mdx written: {len(topics_doc['lessons'])} lesson(s), {n_rows} link rows")
    print(f"src/lesson-backlinks.json written: {', '.join(sorted(backlinks['pages']))}")


if __name__ == "__main__":
    main()
