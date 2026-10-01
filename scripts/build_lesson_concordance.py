#!/usr/bin/env python3
"""Build the LessonConcordance/ page — поурочный конкорданс Бюлера (H5595 pilot: урок I).

Модель — scripts/build_subject_concordance.py: датафайлы в каталоге-«книге»,
генератор пишет catalog.mdx, руками страницу не правят. Источники:

  * LessonConcordance/typed_link_buhler_lessons.tsv — typed-link строки
    (TYPED_LINK_ID_GRAMMAR.md §1 shape, anchor buhler-topic:<RN>.<topic>);
  * LessonConcordance/topics.yml — словарь тем (D13) + per-topic
    exception-coverage (голос D2: гипотеза MG про списки исключений);
  * BuhlerLeitfaden_1923/Buhler_Unicode.mdx — реестр уроков (# УРОК N.;
    урок V — жирным делимитером, нормализуем — риск №1 плана);
  * BuhlerLeitfaden_1923/claims.yml — HB-утверждения урока (loc: «Урок I /…»);
  * WhitneyRoots/crosswalk/roots.csv — класс корня по Уитни, частота DCS;
  * TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv —
    ряд/класс З-1975 (арбитр морфокласса, шапка claims.yml);
  * Concordance/catalog.mdx — reuse-кластеры с колонкой урока Бюлера.

Generated — do NOT hand-edit LessonConcordance/catalog.mdx; re-run this script.
"""
import csv
import glob
import re
import sys
import unicodedata
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
LC = ROOT / "LessonConcordance"
GH = "https://github.com/gasyoun/SanskritGrammar/blob/main"
GH_WR = "https://github.com/gasyoun/WhitneyRoots/blob/main"

TSV = LC / "typed_link_buhler_lessons.tsv"
TOPICS = LC / "topics.yml"
BUHLER = ROOT / "BuhlerLeitfaden_1923" / "Buhler_Unicode.mdx"
CLAIMS = ROOT / "BuhlerLeitfaden_1923" / "claims.yml"
ROOTS_CSV = ROOT.parent / "WhitneyRoots" / "crosswalk" / "roots.csv"
CROSSWALK = ROOT / "TolchelnikovTalmud_2026" / "data" / "morphoclass_crosswalk_1975_2014_2026.csv"
REUSE = ROOT / "Concordance" / "catalog.mdx"
OUT = LC / "catalog.mdx"

PILOT_LESSON = "I"

# 13 корней I класса урока I — списано с Buhler_Unicode.mdx:112-252 (пилотный
# курируемый посев; при регенерации не пересматривать молча — сверять с mdx).
LESSON_I_ROOTS = [
    ("pat", "падать, лететь"), ("dah", "гореть, жечь"), ("yaj", "приносить жертву"),
    ("śaṃs", "прославлять"), ("vas", "жить, обитать"), ("rakṣ", "защищать"),
    ("jīv", "жить"), ("car", "ходить, совершать, пастись"), ("nam", "кланяться (D.), почитать"),
    ("pac", "варить, готовить"), ("dhāv", "бежать"), ("tyaj", "покидать"),
    ("vah", "нести, течь, дуть, веять"),
]

# Читаемые подписи target-локусов урока I (курируемо; незнакомый локус = warning).
LOCUS_LABELS = {
    "subject:sanskritgrammar:present_a": "спайн SubjectConcordance, категория present_a",
    "whitney-sec:733-750": "Уитни §§733-750 — Present, a-class (I / bhū-class)",
    "whitney-sec:144-148": "Уитни §§144-148 — конечные r/s → висарга; висарга как субститут s/r",
    "whitney-sec:170-173": "Уитни §§170-173 — висарга перед последующими звуками; §171a/§173 — исключения",
    "kochergina-lesson:VIII": "Кочергина, Занятие VIII — спряжение в настоящем времени (Parasmaipada/Ātmanepada)",
    "kochergina-lesson:VI": "Кочергина, Занятие VI — висарга: -s/-r → ḥ (строки 1259-1265)",
    "knauer-fraza:Nr.1": "Кнауэр, Nr. 1 (§§ 45-47) — фразы на настоящем: devā narān rakṣanti…",
    "knauer-fraza:Nr.2": "Кнауэр, Nr. 2 (§§ 48-51) — çaṅsanti / patati / vasati…",
    "zalizniak-1978-sec:114": "Зализняк-1978, § 114 — тематическое vs атематическое спряжение",
    "zalizniak-1978-sec:32-46": "Зализняк-1978, §§ 32-46 — правила сандхи (разделы по § 31)",
    "zalizniak-2004:klassy-prezensa": "Зализняк-2004, «Классы презенса» (Конспект)",
    "zalizniak-2004:morfonologija": "Зализняк-2004, «Морфонология» (внешние/внутренние сандхи)",
    "sangram-article:thematic-present": "Sangram, статья thematic-present",
    "talmud:morphoclass-crosswalk-1975-2014-2026": "Толчельников-Талмуд-2026, crosswalk морфоклассов 1975/2014/2026",
}

LESSON_HEAD = re.compile(r"^#{1,2}\s*УРОК\s+([IVXL]+)\.?\s*$", re.M)
LESSON_BOLD = re.compile(r"^\*\*Урок\s+([IVXL]+)\.?\*\*\s*$", re.M)
CLAIM_LOC = re.compile(r'loc:\s*"Урок\s+(I)\s+/\s+mdx line (\d+)"')
CLAIM_ID = re.compile(r"^  - id:\s*(HB-\d+)")


def lesson_registry():
    text = BUHLER.read_text(encoding="utf-8")
    found = {}
    for m in LESSON_HEAD.finditer(text):
        found.setdefault(m.group(1), ("header", text[: m.start()].count("\n") + 1))
    for m in LESSON_BOLD.finditer(text):
        found.setdefault(m.group(1), ("bold", text[: m.start()].count("\n") + 1))
    order = {r: i for i, r in enumerate(
        ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"] +
        [f"X{i}" for i in range(1, 9)] + ["XIX", "XX"] +
        [f"XX{i}" for i in range(1, 10)] + ["XXX"] +
        [f"XXX{i}" for i in range(1, 10)] + ["XL", "XLI", "XLII", "XLIII", "XLIV",
         "XLV", "XLVI", "XLVII", "XLVIII"])}
    return found, order


def lesson_i_claims():
    rows, cur_id = [], None
    for line in CLAIMS.read_text(encoding="utf-8").splitlines():
        idm = CLAIM_ID.match(line)
        if idm:
            cur_id = idm.group(1)
        lm = CLAIM_LOC.search(line)
        if lm and lm.group(1) == PILOT_LESSON:
            rows.append((cur_id, int(lm.group(2))))
    return rows


def read_tsv():
    with open(TSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def ascii_fold(s):
    base = unicodedata.normalize("NFD", s)
    return "".join(c for c in base if not unicodedata.combining(c)).replace("ṃ", "m").lower()


def load_roots():
    if not ROOTS_CSV.exists():
        return {}
    with open(ROOTS_CSV, encoding="utf-8", newline="") as f:
        out = {}
        for row in csv.DictReader(f):
            out.setdefault(row["root_iast"], []).append(row)
        return out


def load_crosswalk():
    if not CROSSWALK.exists():
        return {}
    with open(CROSSWALK, encoding="utf-8", newline="") as f:
        out = {}
        for row in csv.DictReader(f):
            out.setdefault(ascii_fold(row.get("root", "")), []).append(row)
        return out


def reuse_clusters_for_lesson():
    if not REUSE.exists():
        return 0
    count = 0
    for line in REUSE.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\| C\d+ ", line) and re.search(r"\|\s*I\s*\|", line):
            count += 1
    return count


def root_rows():
    roots, crosswalk = load_roots(), load_crosswalk()
    rows, misses = [], []
    for riast, gloss in LESSON_I_ROOTS:
        wr = roots.get(riast, [])
        classes = sorted({c for r in wr for c in r.get("class", "").split("|") if c})
        wnos = sorted({r["whitney_no"] for r in wr}, key=int)
        freqs = sorted({int(r["dcs_freq"]) for r in wr if r.get("dcs_freq", "").isdigit()}, reverse=True)
        cw = crosswalk.get(ascii_fold(riast), [])
        ryads = sorted({r.get("ryad_1978", "") for r in cw if r.get("ryad_1978", "")})
        if not wr and not cw:
            misses.append(riast)
        rows.append((riast, gloss, ", ".join(wnos) or "—", "|".join(classes) or "—",
                     f"{freqs[0]:,}" if freqs else "—",
                     ", ".join(ryads) or "—", len(cw)))
    return rows, misses


def main():
    topics = yaml.safe_load(TOPICS.read_text(encoding="utf-8"))
    tsv_rows = read_tsv()
    claims = lesson_i_claims()
    registry, order = lesson_registry()
    r_rows, r_misses = root_rows()
    reuse_n = reuse_clusters_for_lesson()

    L = []
    L.append("---")
    L.append('title: "Поурочный конкорданс Бюлера"')
    L.append('sidebar_label: "Поурочный конкорданс"')
    L.append("---")
    L.append("")
    L.append("# Поурочный конкорданс Бюлера — урок I (пилот)")
    L.append("")
    L.append(f"_Сгенерировано [`scripts/build_lesson_concordance.py`]({GH}/scripts/build_lesson_concordance.py) "
             f"из [`typed_link_buhler_lessons.tsv`]({GH}/LessonConcordance/typed_link_buhler_lessons.tsv) + "
             f"[`topics.yml`]({GH}/LessonConcordance/topics.yml) — не редактировать руками._")
    L.append("")
    L.append("Поурочное сшивание «урок [Бюлера-1923](../BuhlerLeitfaden_1923/Buhler_Unicode) ↔ каждый источник "
             "сайта» по плану "
             f"[BUHLER_LESSON_CONCORDANCE_PLAN_2026.md]({GH}/BUHLER_LESSON_CONCORDANCE_PLAN_2026.md) "
             "(решения D1-D16; пилот — урок I). Это finding-aid: строка = связь "
             "«урок+тема → локус-источник», `match_method=curated`, confidence 0.7-0.97.")
    L.append("")

    L.append("## Связи урока I")
    L.append("")
    current = None
    for row in tsv_rows:
        topic = row["anchor_id"].split(".", 1)[1]
        if topic != current:
            if current is not None:
                L.append("")
            current = topic
            t = topics["topics"][topic]
            L.append(f"### Тема `{topic}` — {t['label_ru']}")
            L.append("")
            L.append(f"Спайн: {t['spine']}. Локус у Бюлера: {t['buhler_locus']}")
            L.append("")
            L.append("| target_locus | что это | link_type | confidence | evidence |")
            L.append("|---|---|---|---|---|")
        label = LOCUS_LABELS.get(row["target_locus"], "⚠ неизвестный локус")
        ev = row["evidence_count"] or "—"
        conf = row["confidence"] or "—"
        L.append(f"| `{row['target_locus']}` | {label} | {row['link_type']} | {conf} | {ev} |")
    L.append("")

    L.append("## Гипотеза MG: кто даёт списки исключений (голос D2)")
    L.append("")
    for topic, t in topics["topics"].items():
        L.append(f"### `{topic}`")
        L.append("")
        for who, verdict in t["exception_coverage"].items():
            L.append(f"- **{who}:** {verdict}")
        L.append("")
        lc = t.get("lemma_coverage", {})
        for k, v in lc.items():
            L.append(f"- **lemma/{k}:** {v}")
        L.append("")

    L.append("## Корни I класса урока I — сшивка с регистрами")
    L.append("")
    L.append(f"Класс и частота — [`roots.csv`]({GH_WR}/crosswalk/roots.csv) (ростер Уитни), "
             "ряд З-1975 — crosswalk морфоклассов (арбитр по шапке claims.yml).")
    L.append("")
    L.append("| корень | у Бюлера | Уитни № | класс | DCS частота | ряд З-1975 | строк crosswalk |")
    L.append("|---|---|---|---|---|---|---|")
    for riast, gloss, wnos, cls, freq, ryads, ncw in r_rows:
        L.append(f"| {riast} | {gloss} | {wnos} | {cls} | {freq} | {ryads} | {ncw} |")
    L.append("")
    if r_misses:
        L.append(f"⚠ Не сшились ни с одним регистром: {', '.join(r_misses)}.")
        L.append("")
    L.append("⚠ **Омонимия корней:** «vas - жить, обитать» у Бюлера = vas-3 (roots.csv №717, gloss «dwell», "
             "класс I) — класс-I чтение подтверждена; омонимы vas-1 «shine» / vas-2 «clothe» (№715/716, II|VI) "
             "к уроку I не относятся. Ряды З-1975 (jīv → I₂, nam → M₁, car → R?) — значения crosswalk как есть, "
             "арбитраж морфокласса за talmud-регистром.")
    L.append("")

    L.append(f"## HB-указатель урока {PILOT_LESSON} (claims.yml)")
    L.append("")
    if claims:
        L.append("| id | mdx line |")
        L.append("|---|---|")
        for cid, ln in claims:
            L.append(f"| {cid} | {ln} |")
    else:
        L.append("_(утверждений с loc «Урок I /» не найдено)_")
    L.append("")
    L.append(f"## Reuse-кластеры [Concordance/catalog.mdx]({GH}/Concordance/catalog.mdx)")
    L.append("")
    L.append(f"Кластеров общих предложений с уроком I: **{reuse_n}**"
             + (" — упражнения урока I элементарны и общих предложений с Кнауэром/Кочергиной не дают."
                if reuse_n == 0 else "") + "")
    L.append("")

    L.append("## Реестр уроков (парсер, не один паттерн)")
    L.append("")
    L.append(f"Найдено уроков: **{len(registry)}** из 48. Парсер нормализует заголовочный "
             "делимитер (`# УРОК N.`) и жирный (`**Урок N.**`) — риск №1 плана.")
    odd = {r: v for r, v in registry.items() if v[0] == "bold"}
    if odd:
        detail = ", ".join(f"{r} (строка {v[1]})" for r, v in sorted(odd.items(), key=lambda kv: order.get(kv[0], 99)))
        L.append(f" Нестандартный делимитер: {detail}.")
    L.append("")
    L.append(f"Пилот: урок **{PILOT_LESSON}**. Остальные 45 — batch-минт после ревью MG.")
    L.append("")

    OUT.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {OUT}", file=sys.stderr)
    print(f"rows={len(tsv_rows)} claims={len(claims)} lessons={len(registry)} reuse_I={reuse_n} "
          f"root_misses={r_misses or 'none'}", file=sys.stderr)


if __name__ == "__main__":
    main()
