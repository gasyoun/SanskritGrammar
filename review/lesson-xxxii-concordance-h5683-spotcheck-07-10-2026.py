#!/usr/bin/env python3
"""Fresh-process spot-check for H5683 — LessonConcordance урок XXXII (степени сравнения).
Independent re-verification (DeepSeek-лейн недоступен — KEY_ABSENT, прецедент H5659…H5682):
читает данные из первичных файлов наново, ничего не берёт на веру из курации."""
import json, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")

FAIL = []
def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (" — " + detail if detail else ""))
    if not cond:
        FAIL.append(name)

# 1. Урок-сегмент в Buhler_Unicode.mdx
b = open("BuhlerLeitfaden_1923/Buhler_Unicode.mdx", encoding="utf-8").read().splitlines()
check("buhler header 4579", b[4578].strip() == "# УРОК XXXII.", repr(b[4578]))
seg = "\n".join(b[4578:4656])
for frag in ["сравнительную степень", "iṣṭha", "udarciṣṭara", "gajatama", "uccaistarām",
             "kṣepīyas", "draḍhīyas", "srajīyas", "nedīyas", "varṣīyas",
             "Сравнительная степень сочетается с Аbl.", "garīyān", "jyeṣṭha"]:
    check("mdx §-фрагмент «%s»" % frag, frag in seg)

# 2. Claims: 7 строк урока XXXII
cl = open("BuhlerLeitfaden_1923/claims.yml", encoding="utf-8").read()
for hid in ["HB-47", "HB-252", "HB-253", "HB-254", "HB-255", "HB-256", "HB-257"]:
    m = re.search(r"- id: %s\n.*?loc: \"Урок XXXII" % hid, cl, re.S)
    check("claims %s loc=XXXII" % hid, bool(m))

# 3. Спот-фразы: 9 новых — независимый re-read источников
spots = {
 "KocherginaUchebnik_1998/Kochergina_unicode.mdx": [
   "образуется путем прибавления к основе прилагательного вторичных суффиксов -tara",
   "Реже употребляется первичный суффикс -(ī)yaṃs",
   "к корню, при этом гласная корня выступает в ступени guṇa",
   "Ряд прилагательных употребляется только в сравнительной или превосходной степени",
   "Прилагательные в сравнительной степени употребляются с существительным в отложительном падеже",
   "Прилагательное в превосходной степени употребляется с существительным в родительном или местном падежах"],
 "ZalizniakOcherk_1978/Zalizniak-Ocherk_29-11-20-aligned.mdx": [
   "Обычные суффиксы --- -tara- (сравнит.), -tama- (превосходн.)",
   "присоединяются не к основе прилагательного, а к его корню",
   "Образец: kanīyaṁs- (m, n)"],
 "KnauerFrazy_1908/Frazy-Knauer-03.05.2023.mdx": [
   "कनीयांसो भ्रातरो रामस्याभवन्",
   "मोक्षाय ज्ञानं यज्ञेभ्यः साधीय इति पुराणैरुक्तम्"],
}
n_spots = 0
for f, phr in spots.items():
    t = open(f, encoding="utf-8").read()
    for p in phr:
        check("spot «%s…» в %s" % (p[:28], f.split("/")[-1]), p in t); n_spots += 1

# 4. Kochergina: раздел сравнения в Занятии XXIX (между делимитерами XXIX и XXX)
k = open("KocherginaUchebnik_1998/Kochergina_unicode.mdx", encoding="utf-8").read().splitlines()
i29 = next(i for i, l in enumerate(k) if l.strip() == "Занятие XXIX")
i30 = next(i for i, l in enumerate(k) if i > i29 and re.match(r"^Занятие XXX\b", l.strip()))
sec29 = "\n".join(k[i29:i30])
check("kochergina XXIX границы", i30 > i29, f"строки {i29+1}–{i30}")
for frag in ["вторичных суффиксов -tara", "первичный суффикс -(ī)yaṃs", "отложительном падеже",
             "родительном или местном падежах", "nédīyaṃs", "śréyaṃs", "laghīyas"]:
    check("XXIX содержит «%s»" % frag, frag in sec29)

# 5. Очерк: §185/§93
o = open("ZalizniakOcherk_1978/Zalizniak-Ocherk_29-11-20-aligned.mdx", encoding="utf-8").read()
check("ocherk span s185", 'id="s185"' in o and "Степени сравнения. Обычные суффиксы" in o)
check("ocherk §93 kanīyaṁs", re.search(r'id="s93".{0,200}kanīyaṁs', o, re.S) is not None)

# 6. Уитни §§ в локальном файле (466–473, 292b)
w = open("WhitneyGrammar_1889/05_Nouns_and_Adjectives.mdx", encoding="utf-8").read()
w4 = open("WhitneyGrammar_1889/04_Declension.mdx", encoding="utf-8").read()
for s in [466, 467, 468, 469, 470, 471, 472, 473]:
    check("whitney §%d exists" % s, "[**§%d**]" % s in w)
check("whitney §292 ablative-of-comparison", "The ablative of comparison" in w4 and "[**§292**]" in w4)
check("whitney §470 irregular canon", all(x in w for x in ["bhū́yas", "bhū́yiṣṭha", "jyéṣṭha"]))
check("whitney §473 adverbs -tarām", "-tarā́m" in w or "nīcāistarām" in w or "tarā́m" in w)

# 7. Reuse: 2 exact-совпадения из matches.json
mj = json.load(open("scripts/data/matches.json", encoding="utf-8"))
xxxii = [r for r in mj if "XXXII" in json.dumps(r, ensure_ascii=False)]
pairs = sorted((r["a"]["id"], r["b"]["id"], float(r["score"])) for r in xxxii)
check("reuse 2 exact", pairs == [("buhler-1923.XXXII.726", "knauer-1908.8.159", 1.0),
                                 ("buhler-1923.XXXII.728", "knauer-1908.7.147", 1.0)], str(pairs))

# 8. TSV: 13 строк урока XXXII, 10 колонок, lint
tsv = open("LessonConcordance/typed_link_buhler_lessons.tsv", encoding="utf-8").read().splitlines()
rows = [l.split("\t") for l in tsv if l.startswith("buhler-topic\tbuhler-topic:XXXII.")]
check("tsv 13 rows", len(rows) == 13, str(len(rows)))
check("tsv 10 cols everywhere", all(len(r) == 10 for r in rows))
check("tsv anchor keys", sorted({r[1].split(".")[1] for r in rows}) ==
      ["comparative-irregular", "comparative-iyas-istha", "comparative-tara-tama", "comparison-syntax"])
r = subprocess.run([sys.executable, "/Users/mac/Documents/GitHub/kosha/scripts/typed_link_lint.py",
                    "LessonConcordance/typed_link_buhler_lessons.tsv"], capture_output=True, text=True)
check("typed_link_lint clean", r.returncode == 0 and "all clean" in r.stdout, (r.stdout + r.stderr).strip()[-60:])

# 9. Каталог: секция XXXII, 4 темы, build-выход
c = open("LessonConcordance/catalog.mdx", encoding="utf-8").read()
i32 = c.find("## Урок XXXII —")
i33 = c.find("\n## Урок", i32 + 1)
if i33 < 0: i33 = len(c)  # XXXII — последняя секция (порядок вставки topics.yml)
check("catalog §XXXII present", i32 > 0 and i33 > i32)
check("catalog 4 topic headings", c[i32:i33].count("\n### ") == 4)
for t in ["comparative-tara-tama", "comparative-iyas-istha", "comparative-irregular", "comparison-syntax"]:
    check("catalog topic key %s" % t, t in c[i32:i33])
for hid in ["HB-47", "HB-252", "HB-253", "HB-254", "HB-255", "HB-256", "HB-257"]:
    check("catalog claim chip %s" % hid, hid in c[i32:i33])

# 10. Corpus-layer: 0 строк урока — честно
cor = open("BuhlerLeitfaden_1923/corpus_layer/corpus_layer.tsv", encoding="utf-8").read()
check("corpus_layer XXXII = 0 rows (честно)", "XXXII" not in cor)

print("\nSUMMARY: %d FAIL, %d checks" % (len(FAIL), 0 if FAIL else 1))
print("FAILURES:", FAIL if FAIL else "none")
sys.exit(1 if FAIL else 0)
