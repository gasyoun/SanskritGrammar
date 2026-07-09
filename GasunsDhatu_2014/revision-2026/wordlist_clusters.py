#!/usr/bin/env python3
"""wordlist_clusters.py — H382 (GasunsDhatu 2026), пересчёт Таблицы 4
(«Начальные и конечные консонантные кластеры слов») издания 2014 г.

В издании 2014 г. Таблица 4 считалась по невоспроизводимому «сводному словнику
из 260 000 слов» (черновик «Обратного словаря санскрита»). Здесь основой взят
открытый и воспроизводимый союзный словник —
SanskritLexicography/HeadwordLists/union/union_headwords.tsv
(323 425 заголовков из 12+ словарей CDSL, колонка slp1).

Метод (оговорён явно, как требует H382):
  * заголовок разбивается на максимальные согласные цепочки (кластеры);
    гласные и модификаторы (M/H/~) — границы кластеров;
  * кластер длины >= 2 — консонантный кластер (лигатура);
  * позиция: НАЧАЛЬНЫЙ — цепочка стоит в начале слова; КОНЕЧНЫЙ — в конце;
    прочие — срединные. «Всего» = кластер встречается в любой позиции.
  * считаются РАЗНОВИДНОСТИ (различные типы кластеров), как в 2014 г.,
    а также число заголовков-носителей (в скобках в CSV).

Замечание о сопоставимости: цифры 2014 г. (Всего *CC* 3199, *CCC* 204;
в начале CC* 1161, CCC* 90; в конце *CC 230, *CCC 25) получены на другом
словнике и другим (неописанным) инструментом; прямое совпадение не ожидается.
Ценность — воспроизводимость, а не узнаваемость исходных чисел.

Source: union_headwords.tsv (CDSL union headword list).
Usage:  python wordlist_clusters.py [path-to-union_headwords.tsv]
Writes: table4_word_clusters.csv, table4_word_clusters_full.csv,
        wordlist_clusters_provenance.json (рядом со скриптом).
"""
import sys, csv, json, collections
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate as tr

HERE = Path(__file__).resolve().parent
DEFAULT_SRC = (HERE.parents[2] / "SanskritLexicography" / "HeadwordLists"
               / "union" / "union_headwords.tsv")

CONS = set("kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzshL")
VOWELS = set("aAiIuUfFxXeEoO")
MODIF = set("MH~")


def clusters_with_pos(word):
    """Список (кластер, позиция) для одного SLP1-слова.

    позиция ∈ {initial, final, medial}; кластер = максимальная согласная
    цепочка длины >= 2. Модификаторы M/H/~ рвут цепочку (граница слога).
    """
    out = []
    i, n = 0, len(word)
    first = True
    while i < n:
        c = word[i]
        if c in CONS:
            j = i
            while j < n and word[j] in CONS:
                j += 1
            cl = word[i:j]
            at_start = (i == 0)
            at_end = (j == n)
            if len(cl) >= 2:
                pos = ("initial" if at_start else
                       "final" if at_end else "medial")
                out.append((cl, pos))
            i = j
        else:
            i += 1
    return out


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC
    # позиция -> длина -> set(кластеров);  позиция -> длина -> Counter(носителей по типу)
    types = {p: collections.defaultdict(set) for p in ("any", "initial", "final")}
    bearers = {p: collections.defaultdict(collections.Counter) for p in ("any", "initial", "final")}

    n_words = 0
    with src.open(encoding="utf-8") as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            slp = (row.get("slp1") or "").strip()
            if not slp:
                continue
            n_words += 1
            seen_any = set()
            for cl, pos in clusters_with_pos(slp):
                L = len(cl)
                if L not in (2, 3):
                    # длиннее 3 учитываем отдельным ведром '4+'
                    L = "4+"
                types["any"][L].add(cl)
                if cl not in seen_any:
                    bearers["any"][L][cl] += 1
                    seen_any.add(cl)
                if pos in ("initial", "final"):
                    types[pos][L].add(cl)
                    bearers[pos][L][cl] += 1

    def n(pos, L):
        return len(types[pos][L])

    # --- сводная Таблица 4 --------------------------------------------------
    with (HERE / "table4_word_clusters.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["показатель", "разновидностей_кластеров", "было_2014"])
        w.writerow(["Всего *CC* (2 согласных, любая позиция)",   n("any", 2),     3199])
        w.writerow(["Всего *CCC* (3 согласных, любая позиция)",  n("any", 3),     204])
        w.writerow(["Всего *CCCC+* (4+ согласных, любая позиция)", n("any", "4+"), ""])
        w.writerow(["В начале CC* (2 согласных)",   n("initial", 2), 1161])
        w.writerow(["В начале CCC* (3 согласных)",  n("initial", 3), 90])
        w.writerow(["В начале CCCC+* (4+)",         n("initial", "4+"), ""])
        w.writerow(["В конце *CC (2 согласных)",    n("final", 2),   230])
        w.writerow(["В конце *CCC (3 согласных)",   n("final", 3),   25])
        w.writerow(["В конце *CCCC+ (4+)",          n("final", "4+"), ""])
        w.writerow([])
        w.writerow(["всего заголовков (словник)", n_words, "260000 (2014, иной словник)"])

    # --- полный список типов с числом носителей ----------------------------
    def iast(slp):
        return tr(slp, sanscript.SLP1, sanscript.IAST)
    with (HERE / "table4_word_clusters_full.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["позиция", "длина", "кластер_iast", "кластер_slp1", "заголовков"])
        for pos in ("any", "initial", "final"):
            for L in (2, 3, "4+"):
                for cl, c in bearers[pos][L].most_common():
                    w.writerow([pos, len(cl), iast(cl), cl, c])

    prov = {
        "generated_by": "wordlist_clusters.py (H382)",
        "source": str(src.name) + " (SanskritLexicography union headword list, CDSL)",
        "headwords": n_words,
        "method": "максимальные согласные цепочки >= 2; M/H/~ — границы; "
                  "разновидности (типы) по позиции initial/final/any",
        "note_2014": "цифры 2014 г. получены на ином словнике (~260 000) неописанным "
                     "инструментом; воспроизводимость важнее совпадения",
        "counts_types": {p: {str(L): len(types[p][L]) for L in (2, 3, "4+")}
                         for p in ("any", "initial", "final")},
    }
    json.dump(prov, (HERE / "wordlist_clusters_provenance.json").open("w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"headwords: {n_words}", file=sys.stderr)
    print("types any:", prov["counts_types"]["any"], file=sys.stderr)
    print("types initial:", prov["counts_types"]["initial"], file=sys.stderr)
    print("types final:", prov["counts_types"]["final"], file=sys.stderr)
    print("DONE", file=sys.stderr)


if __name__ == "__main__":
    main()
