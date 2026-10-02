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
import os
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

# Whitney § → глава-файл (диапазоны глав — спайн SubjectConcordance).
WHITNEY_CHAPTERS = [
    (1, 18, "01_Alphabet"), (19, 97, "02_System_of_Sounds_Pronunciation"),
    (98, 260, "03_Rules_of_Euphonic_Combination"), (261, 320, "04_Declension"),
    (321, 474, "05_Nouns_and_Adjectives"), (475, 489, "06_Numerals"),
    (490, 526, "07_Pronouns"), (527, 598, "08_Conjugation"),
    (599, 779, "09_The_Present_System"), (780, 823, "10_The_Perfect_System"),
    (824, 930, "11_The_Aorist_Systems"),
]

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


def target_url(locus):
    """Глубокая ссылка: страница источника на сайте + текст-фрагмент, подсвечивающий
    куда именно смотреть (МГ, ревью 02-10-2026: любое упоминание источника ведёт не
    просто на страницу, а на максимально конкретный якорь с подсветкой). Для данных
    без страницы на сайте (crosswalk-CSV) — файл в репо (GitHub)."""
    prefix, _, tail = locus.partition(":")
    if prefix == "whitney-sec":
        lo = int(tail.split("-")[0])
        chapter = next((f for a, b, f in WHITNEY_CHAPTERS if a <= lo <= b), None)
        if chapter:
            return (f"{SITE}/WhitneyGrammar_1889/{chapter}{frag('§' + tail.split('-')[0])}",
                    "§§ " + tail.replace("-", "–"))
        return f"{GH}/WhitneyGrammar_1889/", "§§ " + tail.replace("-", "–")
    if prefix == "zalizniak-1978-sec":
        first = tail.split("-")[0]
        return (f"{SITE}/ZalizniakOcherk_1978/Zalizniak-Ocherk_29-11-20-aligned{frag('§ ' + first)}",
                "§§ " + tail.replace("-", "–"))
    if prefix == "zalizniak-1975" or prefix == "zalizniak-2004":
        return f"{GH}/{'ZalizniakMorphology_1975' if prefix == 'zalizniak-1975' else 'ZalizniakKonspekt_2004'}/", tail
    if prefix == "kochergina-lesson":
        spot = KOCHERGINA_SPOTS.get(tail, "Занятие " + tail)
        return (f"{SITE}/KocherginaUchebnik_1998/Kochergina_unicode{frag(spot)}",
                "Занятие " + tail)
    if prefix == "knauer-fraza":
        return (f"{SITE}/KnauerFrazy_1908/Frazy-Knauer-03.05.2023{frag(KNAUER_SPOTS.get(tail, tail))}",
                tail)
    if prefix == "sangram-article":
        return f"{SITE}/sangram/articles/{tail}", tail
    if prefix == "apte" or prefix == "speyer":
        return f"{GH}/{'ApteSyntax_1885' if prefix == 'apte' else 'SpeyerSyntax_1886'}/", "§ " + tail
    if prefix == "dhatu":
        if tail.startswith("glava"):
            return f"{SITE}/GasunsDhatu_2014/{tail.replace('-', '_', 1)}", tail
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


def main():
    with open(TOPICS, encoding="utf-8") as fh:
        topics_doc = yaml.safe_load(fh)

    by_anchor = defaultdict(list)
    for row in load_rows():
        by_anchor[row["anchor_id"]].append(row)

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
               " источниках сайта; план и решения D1–D16: "
               "[BUHLER_LESSON_CONCORDANCE_PLAN_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/BUHLER_LESSON_CONCORDANCE_PLAN_2026.md)."
               " Гипотеза МГ об исключениях проверяется по каждой теме (блок «Исключения»).")
    out.append("")

    for rn, lesson in topics_doc["lessons"].items():
        out.append(f"## Урок {rn} — {lesson['title']}")
        out.append("")
        out.append(f"*Локус текста:* {lesson['mdx']}")
        out.append("")
        for topic in lesson["topics"]:
            anchor_id = f"buhler-topic:{rn}.{topic['key']}"
            rows = by_anchor.get(anchor_id, [])
            out.append(f"### {topic['title']}")
            out.append("")
            out.append(f"*Бюлер:* {topic['buhler_locus']}")
            out.append("")
            if rows:
                out.append("| Источник | Локус | Уверенность | Строк-доказательств |")
                out.append("|---|---|---|---|")
                for row in rows:
                    prefix, _, tail = row["target_locus"].partition(":")
                    label = TARGET_LABELS.get(prefix, prefix)
                    url, display = target_url(row["target_locus"])
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
            if topic.get("lemmas"):
                out.append("| Корень | Глосса | З-1975 | З-1978 | crosswalk |")
                out.append("|---|---|---|---|---|")
                for lem in topic["lemmas"]:
                    out.append(f"| {lem['root']} | {lem['gloss']} | {lem['z1975']} | {lem['z1978']} | {lem['crosswalk']} |")
                out.append("")
            if topic.get("notes"):
                out.append(f"*Примечание:* {topic['notes']}")
                out.append("")
        reg = lesson.get("claims") or []
        if reg:
            cl = ", ".join(f"[{c}](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims.yml)"
                           for c in reg)
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
    n_rows = sum(len(v) for v in by_anchor.values())
    print(f"LessonConcordance/catalog.mdx written: {len(topics_doc['lessons'])} lesson(s), {n_rows} link rows")


if __name__ == "__main__":
    main()
