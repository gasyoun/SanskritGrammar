#!/usr/bin/env python3
"""dcs_text_phonostats.py — H382 (GasunsDhatu 2026), пересчёт Таблиц 1-3 и
«слогов на слово» (§2.5) издания 2014 г. на открытом корпусе DCS-2026.

Читает поверхностные (сандхированные) строки ``# text = …`` из закреплённого
зеркала DCS CoNLL-U, отбирает главы по названию текста (chapter-info.xml
<textName>), транслитерирует IAST → SLP1 (один ASCII-символ на фонему) и
считает по каждому целевому тексту:

  * V   — гласные (aAiIuUfFxXeEoO)
  * C   — согласные + анусвара M + висарга H + чандрабинду ~
          (в издании 2014 г.: «вирама и анусвара считались как согласные»;
           вирама в поверхностной SLP1-записи — это голый согласный, уже
           учтённый в C)
  * консонантный коэффициент  = C / V  (среднее согласных на гласный)
  * aksharas — орфографические слоги (C* V M*  либо конечная согласная кода)
  * слогов на слово = aksharas / words

и для консонантных кластеров (лигатур, максимальных согласных цепочек длины ≥2):
  * частоту каждого кластера по тексту + по два примера-слова (IAST).

Таблица 1  — V, C, коэффициент по 4 текстам издания 2014 г.
Таблицы 2-3 — топ-кластеры Ригведы и Рамаяны (+ полный список в CSV).
§2.5       — слогов на слово по текстам и по всему корпусу.

Источник: DCS CoNLL-U (Oliver Hellwig), CC BY 4.0; закрепление 2026-03-05
(commit 04e0778…, см. VisualDCS/src/DCS-data-2026/conllu/PROVENANCE.md).
Тот же корпусный пин, что у varga_shares.py (Таблица 5).

Usage:  python dcs_text_phonostats.py [DCS_CONLLU_ROOT]
Writes (рядом со скриптом): table1_consonant_coefficient.csv,
        table2_rigveda_clusters.csv, table3_ramayana_clusters.csv,
        syllables_per_word.csv, dcs_phonostats_provenance.json
"""
import sys, os, re, csv, json, glob, time, unicodedata, collections
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate as tr

HERE = Path(__file__).resolve().parent
DEFAULT_ROOT = HERE.parents[2] / "VisualDCS" / "src" / "DCS-data-2026" / "conllu"

# --- SLP1 phoneme classes (identical to build_akshara_ligature_freq.py) -----
VOWELS = set("aAiIuUfFxXeEoO")
CONS = set("kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzshL")
MODIF = set("MH~")   # anusvāra, visarga, candrabindu — считаем согласными (2014)
_SPLIT = re.compile(r"[^kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzshLaAiIuUfFxXeEoOMH~]+")

# Целевые тексты Таблицы 1 (4 текста издания 2014 г.) + Ригведа для Табл. 2.
# Ключ — метка для вывода; значение — точное <textName> в chapter-info.xml.
TABLE1_TEXTS = [
    ("Атхарваведа",  "Atharvaveda (Śaunaka)"),
    ("Мегхадута",    "Meghadūta"),
    ("Рамаяна",      "Rāmāyaṇa"),
    ("Махабхарата",  "Mahābhārata"),
]
CLUSTER_TEXTS = [
    ("Ригведа",  "Ṛgveda",   "table2_rigveda_clusters.csv"),
    ("Рамаяна",  "Rāmāyaṇa", "table3_ramayana_clusters.csv"),
]
# NFC-нормализуем эталонные названия — chapter-info.xml тоже читается в NFC,
# иначе Ṛ (R + комб. точка) != Ṛ (прекомпозиция) и текст не находится.
_NFC = lambda s: unicodedata.normalize("NFC", s)
TABLE1_TEXTS = [(lbl, _NFC(tn)) for lbl, tn in TABLE1_TEXTS]
CLUSTER_TEXTS = [(lbl, _NFC(tn), fn) for lbl, tn, fn in CLUSTER_TEXTS]

# все тексты, которые надо прочитать
WANTED = {v for _, v in TABLE1_TEXTS} | {v for _, v, _ in CLUSTER_TEXTS}


def slp1_words(text_iast):
    slp = tr(text_iast, sanscript.IAST, sanscript.SLP1)
    return [c for c in _SPLIT.split(slp) if c]


def segment(word):
    """(aksharas, v_count, c_count, ligatures) для одного SLP1-слова.

    akshara = максимальная цепочка согласных + гласная + модификаторы,
              либо конечная согласная кода без гласной.
    ligature = согласная цепочка длины >= 2.
    """
    aksharas, ligs = [], []
    vc = cc = 0
    i, n = 0, len(word)
    while i < n:
        c = word[i]
        if c in CONS:
            j = i
            while j < n and word[j] in CONS:
                j += 1
            cluster = word[i:j]
            cc += len(cluster)
            if len(cluster) >= 2:
                ligs.append(cluster)
            if j < n and word[j] in VOWELS:
                k = j + 1
                while k < n and word[k] in MODIF:
                    k += 1
                aksharas.append(word[i:k])
                vc += 1
                cc += sum(1 for m in word[j + 1:k])   # M/H/~ считаем согласными
                i = k
            else:
                aksharas.append(cluster)               # конечная кода
                i = j
        elif c in VOWELS:
            k = i + 1
            while k < n and word[k] in MODIF:
                k += 1
            aksharas.append(word[i:k])
            vc += 1
            cc += sum(1 for m in word[i + 1:k])
            i = k
        else:
            if c in MODIF:
                cc += 1
            i += 1
    return aksharas, vc, cc, ligs


def load_textname_map(root):
    """basename(.conllu) -> textName из chapter-info.xml."""
    txt = open(root / "lookup" / "chapter-info.xml", encoding="utf-8").read()
    m = {}
    for chap in re.finditer(r"<path>(.*?)</path>.*?<textName>(.*?)</textName>", txt, re.S):
        base = unicodedata.normalize("NFC", os.path.basename(chap.group(1)))
        m[base] = unicodedata.normalize("NFC", chap.group(2))
    return m


def main():
    t0 = time.time()
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ROOT
    name_of = load_textname_map(root)
    files = glob.glob(str(root / "files" / "**" / "*.conllu"), recursive=True)
    print(f"conllu files: {len(files)}; целевых текстов: {len(WANTED)}", file=sys.stderr)

    # per-text аккумуляторы
    per_text = {v: {"V": 0, "C": 0, "words": 0, "aksharas": 0} for v in WANTED}
    clusters = {tn: collections.Counter() for _, tn, _ in CLUSTER_TEXTS}
    examples = {tn: collections.defaultdict(list) for _, tn, _ in CLUSTER_TEXTS}
    cluster_texts = {tn for _, tn, _ in CLUSTER_TEXTS}

    read = 0
    for path in files:
        base = unicodedata.normalize("NFC", os.path.basename(path))
        tn = name_of.get(base)
        if tn not in WANTED:
            continue
        read += 1
        for line in open(path, encoding="utf-8"):
            if not line.startswith("# text = "):
                continue
            for w in slp1_words(line[9:]):
                ak, vc, cc, lg = segment(w)
                d = per_text[tn]
                d["V"] += vc
                d["C"] += cc
                d["words"] += 1
                d["aksharas"] += len(ak)
                if tn in cluster_texts:
                    seen = set()
                    for cl in lg:
                        clusters[tn][cl] += 1
                        if cl not in seen and len(examples[tn][cl]) < 2:
                            examples[tn][cl].append(tr(w, sanscript.SLP1, sanscript.IAST))
                            seen.add(cl)
    print(f"прочитано целевых .conllu: {read}, {time.time()-t0:.0f}s", file=sys.stderr)

    def iast(slp):
        return tr(slp, sanscript.SLP1, sanscript.IAST)

    # --- Таблица 1: V, C, консонантный коэффициент -------------------------
    with (HERE / "table1_consonant_coefficient.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["текст", "dcs_textName", "V_гласные", "C_согласные",
                    "консонантный_коэффициент", "слов", "слогов_на_слово"])
        tot_v = tot_c = tot_w = tot_a = 0
        for label, tn in TABLE1_TEXTS:
            d = per_text[tn]
            coef = d["C"] / d["V"] if d["V"] else 0
            spw = d["aksharas"] / d["words"] if d["words"] else 0
            w.writerow([label, tn, d["V"], d["C"], f"{coef:.2f}", d["words"], f"{spw:.2f}"])
            tot_v += d["V"]; tot_c += d["C"]; tot_w += d["words"]; tot_a += d["aksharas"]
        coef = tot_c / tot_v if tot_v else 0
        spw = tot_a / tot_w if tot_w else 0
        w.writerow(["ИТОГО (4 текста)", "", tot_v, tot_c, f"{coef:.2f}", tot_w, f"{spw:.2f}"])

    # --- Таблицы 2-3: кластеры по текстам ----------------------------------
    for label, tn, fn in CLUSTER_TEXTS:
        cnt = clusters[tn]
        total = sum(cnt.values())
        with (HERE / fn).open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["ранг", "кластер_iast", "кластер_slp1", "частота", "доля_%",
                        "пример1", "пример2"])
            for rank, (cl, c) in enumerate(cnt.most_common(), 1):
                ex = examples[tn][cl] + ["", ""]
                w.writerow([rank, iast(cl), cl, c, f"{100*c/total:.3f}", ex[0], ex[1]])
        print(f"{label}: {len(cnt)} различных кластеров, {total} вхождений", file=sys.stderr)

    # --- §2.5 слогов на слово ----------------------------------------------
    with (HERE / "syllables_per_word.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["текст", "dcs_textName", "слов", "слогов_aksharas", "слогов_на_слово"])
        for label, tn in TABLE1_TEXTS + [("Ригведа", "Ṛgveda")]:
            d = per_text[tn]
            spw = d["aksharas"] / d["words"] if d["words"] else 0
            w.writerow([label, tn, d["words"], d["aksharas"], f"{spw:.2f}"])
        gw = sum(per_text[v]["words"] for v in WANTED)
        ga = sum(per_text[v]["aksharas"] for v in WANTED)
        w.writerow(["ИТОГО (5 текстов)", "", gw, ga, f"{ga/gw:.2f}" if gw else "0"])

    prov = {
        "generated_by": "dcs_text_phonostats.py (H382)",
        "source": "DCS CoNLL-U (Oliver Hellwig), CC BY 4.0",
        "pin": "2026-03-05 (commit 04e0778…), см. VisualDCS/src/DCS-data-2026/conllu/PROVENANCE.md",
        "input": "# text = поверхностные (сандхированные) строки, files/**/*.conllu",
        "text_filter": "chapter-info.xml <textName>",
        "counting": "V = гласные; C = согласные + M(анусвара) + H(висарга) + ~(чандрабинду); коэффициент = C/V",
        "syllable": "akshara = C* V M* либо конечная согласная кода; слогов/слово = aksharas/words",
        "cluster": "максимальная согласная цепочка длины >= 2 (конъюнкт/лигатура)",
        "per_text": {tn: per_text[tn] for tn in WANTED},
        "conllu_files_read": read,
        "seconds": round(time.time() - t0, 1),
    }
    json.dump(prov, (HERE / "dcs_phonostats_provenance.json").open("w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("DONE", file=sys.stderr)


if __name__ == "__main__":
    main()
