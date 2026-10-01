#!/usr/bin/env python3
"""Curated Grammar Lab Wave-1 topic/exercise inventory (H2492).

This module is the authoring table. ``--emit`` writes one YAML file per topic
and exercise under data/grammar_lab/. The builder reads those YAML files; it
does not import this table at compile time.

Usage:
    python scripts/grammar_lab_inventory.py --emit
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[1]
LAB = REPO / "data" / "grammar_lab"
PIN_CSV = LAB / "pins" / "whitneyroots_roots_slice.csv"
WHITNEY_ROOTS = REPO.parent / "WhitneyRoots" / "crosswalk" / "roots.csv"
DATE = "13-08-2026"
CURATOR = "Grok 4.6 (grok-4.6) H2492"
SNAPSHOT = "WhitneyRoots@b453ce0e739c761aa0e32a1df6200d9875b148a5 roots.csv"

# Pinned roster rows used as dictionary/corpus evidence (whitney_no).
PIN_NOS = [
    22, 23, 29, 106, 120, 170, 242, 269, 293, 349, 393, 427, 494,
    528, 546, 597, 608, 699, 704, 815, 874, 908, 919,
]

# Evidence cards keyed by the topic's primary example root.
ROOT_BY_NO = {
    22: ("as", "as", "1", "be"),
    23: ("as", "as", "2", "throw"),
    29: ("i", "i", "1", "go"),
    106: ("kṛ", "kf", "1", "make"),
    120: ("krī", "krI", "", "buy"),
    170: ("gam", "gam", "", "go"),
    242: ("chid", "Cid", "", "cut off"),
    269: ("jñā", "jYA", "", "know"),
    293: ("tan", "tan", "1", "stretch"),
    349: ("dā", "dA", "1", "give"),
    393: ("dhā", "DA", "1", "put"),
    427: ("nī", "nI", "", "lead"),
    494: ("bandh", "banD", "", "bind"),
    528: ("bhū", "BU", "", "be"),
    546: ("man", "man", "", "think"),
    597: ("yaj", "yaj", "", "offer"),
    608: ("yuj", "yuj", "", "join"),
    699: ("vac", "vac", "", "speak"),
    704: ("vad", "vad", "", "speak"),
    815: ("śru", "Sru", "", "hear"),
    874: ("sthā", "sTA", "", "stand"),
    908: ("han", "han", "", "smite"),
    919: ("hu", "hu", "", "sacrifice"),
}

LIMITATION = (
    "DCS token counts from the pinned WhitneyRoots roots.csv fold "
    "(revision b453ce0e); absence is snapshot-limited, not linguistic impossibility. "
    "Homonymous roster rows may share a folded frequency."
)


def _edge(anchor_type: str, anchor_id: str, topic: str, dataset: str, slp1: str = "") -> dict:
    return {
        "anchor_type": anchor_type,
        "anchor_id": anchor_id,
        "anchor_key_slp1": slp1,
        "target_locus": topic,
        "link_type": "thematic",
        "source_dataset": dataset,
        "match_method": "curated",
        "confidence": 0.97,
        "evidence_count": None,
        "date": DATE,
    }


def _load_pin_rows() -> dict[int, dict]:
    src = WHITNEY_ROOTS if WHITNEY_ROOTS.is_file() else PIN_CSV
    if not src.is_file():
        raise SystemExit(f"missing WhitneyRoots pin source: {src}")
    out: dict[int, dict] = {}
    with src.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            n = int(row["whitney_no"])
            if n in PIN_NOS:
                out[n] = row
    missing = [n for n in PIN_NOS if n not in out]
    if missing:
        raise SystemExit(f"pin rows missing from {src}: {missing}")
    return out


def write_pin_slice(rows: dict[int, dict]) -> None:
    PIN_CSV.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "whitney_no", "root_iast", "root_slp1", "homonym", "class",
        "gloss_short", "dcs_freq", "dcs_rank", "attested_forms", "mw_id", "apte_id",
    ]
    with PIN_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for n in PIN_NOS:
            w.writerow(rows[n])


def dict_card(rows: dict[int, dict], whitney_no: int) -> dict:
    row = rows[whitney_no]
    mw = (row.get("mw_id") or "").strip()
    return {
        "kind": "dictionary",
        "dict": "mw" if mw else "whitney-roots",
        "entry_id": f"mw:{mw}" if mw else f"whitney-root:{whitney_no}",
        "root_slp1": row["root_slp1"],
        "whitney_no": whitney_no,
        "gloss": (row.get("gloss_short") or row.get("senses") or "")[:80],
        "homonym": row.get("homonym") or "",
    }


def corpus_card(rows: dict[int, dict], whitney_no: int) -> dict:
    row = rows[whitney_no]
    freq = int(row["dcs_freq"] or 0)
    rank = row.get("dcs_rank") or ""
    return {
        "kind": "corpus",
        "status": "attested" if freq > 0 else "not_attested",
        "corpus_snapshot": "WhitneyRoots/crosswalk/roots.csv@b453ce0e dcs_freq",
        "query": f"whitney_no={whitney_no} root_slp1={row['root_slp1']}",
        "dcs_freq": freq,
        "dcs_rank": int(rank) if str(rank).isdigit() else None,
        "attested_forms": (row.get("attested_forms") or "")[:160],
        "limitation": LIMITATION,
    }


# Compact topic table. Each row is expanded into a full YAML record.
# cluster: alternation | root-type | grade | attestation | homonymy | tense-stem
TOPICS: list[dict] = [
    {
        "slug": "ablaut-grades",
        "cluster": "grade",
        "title_ru": "Три ступени чередования",
        "aliases": {
            "ru": ["гуна", "вриддхи", "нулевая ступень", "три ступени"],
            "deva": ["गुण", "वृद्धि"],
            "iast": ["guṇa", "vṛddhi", "zero-grade"],
            "slp1": ["guRa", "vfdDi"],
        },
        "summary_ru": (
            "Whitney описывает guṇa и vṛddhi как последовательные усиления гласного "
            "(§§235–243) без нулевой ступени как члена той же шкалы. Зализняк 1975/1978/2004 "
            "задаёт трёхчленную шкалу слабая / guṇa / vṛddhi. Это один наблюдаемый факт "
            "(три огласовки) и две разные модели: у Уитни нет абстракции «ряда» и нет "
            "нуля как обязательного третьего члена."
        ),
        "alignment_note": "Shared phenomenon, different models. Do not equate Whitney increment with 1975 position.",
        "prereq": [],
        "difficulty": "intro",
        "whitney": ["whitney-sec:235-243"],
        "z1975": ["zalizniak-1975:three-grade-alternation", "zalizniak-1975:table-1"],
        "z1978": ["zalizniak-1978-sec:50"],
        "z2004": ["zalizniak-2004:three-grade"],
        "root": 106,
        "ex": {
            "prompt": "Какая ступень у корня kṛ в kartum (инфинитив на -tum)?",
            "choices": ["нулевая", "guṇa", "vṛddhi"],
            "answer": "guṇa",
        },
    },
    {
        "slug": "morphological-positions",
        "cluster": "grade",
        "title_ru": "Морфологические позиции 1/2/3",
        "aliases": {
            "ru": ["морфологическая позиция", "позиция 1", "позиция 2", "позиция 3"],
            "deva": ["रूपस्थान"],
            "iast": ["morphological position", "1MP", "2MP", "3MP"],
            "slp1": ["1MP", "2MP", "3MP"],
        },
        "summary_ru": (
            "Статья 1975 вводит три морфологические позиции: 1 ждёт нулевую ступень "
            "(причастие на -ta, слабый перфект), 2 — guṇa (инфинитив, будущее), 3 — vṛddhi "
            "(часть сигматического аориста и каузатива). Уитни описывает те же формы "
            "через strong/middle/weakest и отдельные правила усиления; нумерованных позиций "
            "у него нет. Очерк 1978 и конспект 2004 эту примитивацию снимают."
        ),
        "alignment_note": "1975-only primitive. Whitney/1978/2004 are descriptive counterparts, not the same calculus.",
        "prereq": ["subject:grammar-lab:ablaut-grades"],
        "difficulty": "intermediate",
        "whitney": ["whitney-sec:952-956", "whitney-sec:931-940", "whitney-sec:968"],
        "z1975": ["zalizniak-1975:morphological-positions"],
        "z1978": ["zalizniak-1978-sec:162", "zalizniak-1978-sec:157", "zalizniak-1978-sec:164"],
        "z2004": ["zalizniak-2004:morphonology"],
        "root": 106,
        "ex": {
            "prompt": "Какую ступень по Зализняку 1975 ждёт морфологическая позиция 1?",
            "choices": ["нулевую", "guṇa", "vṛddhi"],
            "answer": "нулевую",
        },
    },
    {
        "slug": "alternation-series",
        "cluster": "alternation",
        "title_ru": "Ряды чередования A–N",
        "aliases": {
            "ru": ["ряд чередования", "ряд A", "ряд I", "ряд U", "ряд R"],
            "deva": ["गुणनपङ्क्ति"],
            "iast": ["ablaut series", "A-series", "I-series", "U-series"],
            "slp1": ["A1", "I1", "U1", "R1"],
        },
        "summary_ru": (
            "Зализняк группирует корни по чередующемуся элементу: ряды A, I, U, R, L, M, N "
            "с индексами 1/2. Уитни тех же чередований касается по гласным и по отдельным "
            "корням, но ряда как классификационного ключа не строит. Подписные варианты I0/M0 "
            "из базы /z/ — ошибка обработки, не категория Зализняка."
        ),
        "alignment_note": "Series is a Zalizniak abstraction. Whitney has the vowels, not the series calculus.",
        "prereq": ["subject:grammar-lab:ablaut-grades"],
        "difficulty": "intermediate",
        "whitney": ["whitney-sec:235-243"],
        "z1975": ["zalizniak-1975:table-1", "zalizniak-1975:table-2"],
        "z1978": ["zalizniak-1978-sec:60"],
        "z2004": ["zalizniak-2004:three-grade"],
        "root": 427,
        "ex": {
            "prompt": "К какому ряду Зализняк относит корень nī «вести»?",
            "choices": ["A1", "I1", "U1", "R1"],
            "answer": "I1",
        },
    },
    {
        "slug": "root-type-i",
        "cluster": "root-type",
        "title_ru": "Тип I — полное чередование",
        "aliases": {
            "ru": ["тип I", "полное чередование"],
            "deva": ["प्रथमवर्ग"],
            "iast": ["type I", "full alternation"],
            "slp1": ["typeI"],
        },
        "summary_ru": (
            "Тип I статьи 1975 — корни, которые в позиции 1 дают нуль, в позиции 2 — guṇa "
            "(kṛtaḥ / kartum). Это не I презентный класс Уитни (тематический bhū-класс). "
            "Очерк 1978 заменяет тип перекрёстными осями; конспект 2004 буквенного типа не имеет."
        ),
        "alignment_note": "1975 type I ≠ Whitney present class I.",
        "prereq": ["subject:grammar-lab:morphological-positions"],
        "difficulty": "intermediate",
        "whitney": ["whitney-sec:235-243", "whitney-sec:952-956"],
        "z1975": ["zalizniak-1975:type-i", "zalizniak-1975:type-calculus"],
        "z1978": ["zalizniak-1978-sec:50"],
        "z2004": ["zalizniak-2004:partial-alternators"],
        "root": 106,
        "ex": {
            "prompt": "Какой тип 1975 у kṛ (kṛtaḥ / kartum)?",
            "choices": ["I", "II", "III", "IV"],
            "answer": "I",
        },
    },
    {
        "slug": "root-type-ii",
        "cluster": "root-type",
        "title_ru": "Тип II — частичное чередование",
        "aliases": {
            "ru": ["тип II", "неполноизменяемый"],
            "deva": ["द्वितीयवर्ग"],
            "iast": ["type II"],
            "slp1": ["typeII"],
        },
        "summary_ru": (
            "Тип II держит guṇa там, где тип I даёт нуль: jñātaḥ, not *jñitaḥ; gaditaḥ. "
            "Конспект 2004 называет часть таких корней неполноизменяемыми. Уитни описывает "
            "те же формы как отсутствие ослабления, без типа II."
        ),
        "alignment_note": "1975 type II ≠ Whitney present class II (root class).",
        "prereq": ["subject:grammar-lab:root-type-i"],
        "difficulty": "intermediate",
        "whitney": ["whitney-sec:952-956"],
        "z1975": ["zalizniak-1975:type-ii"],
        "z1978": ["zalizniak-1978-sec:61"],
        "z2004": ["zalizniak-2004:partial-alternators"],
        "root": 269,
        "ex": {
            "prompt": "Какой тип 1975 у jñā (jñātaḥ, не *jñitaḥ)?",
            "choices": ["I", "II", "III", "IV"],
            "answer": "II",
        },
    },
    {
        "slug": "root-type-iii",
        "cluster": "root-type",
        "title_ru": "Тип III — нуль во второй позиции",
        "aliases": {
            "ru": ["тип III"],
            "deva": ["तृतीयवर्ग"],
            "iast": ["type III"],
            "slp1": ["typeIII"],
        },
        "summary_ru": (
            "Тип III не имеет позиции 3 и в позиции 2 остаётся в нулевой ступени "
            "(bhikṣitum, cumbitum). Уитни фиксирует те же «неусиленные» инфинитивы "
            "как исключения к правилу guṇa перед -tum. Это не III презентный класс "
            "(удваивающий hu-класс)."
        ),
        "alignment_note": "1975 type III ≠ Whitney present class III.",
        "prereq": ["subject:grammar-lab:root-type-i"],
        "difficulty": "advanced",
        "whitney": ["whitney-sec:968"],
        "z1975": ["zalizniak-1975:type-iii", "zalizniak-1975:series-iur"],
        "z1978": ["zalizniak-1978-sec:164"],
        "z2004": ["zalizniak-2004:partial-alternators"],
        "root": 242,
        "ex": {
            "prompt": "Тип III в позиции 2 даёт какую ступень?",
            "choices": ["нулевую", "guṇa", "vṛddhi"],
            "answer": "нулевую",
        },
    },
    {
        "slug": "root-type-iv",
        "cluster": "root-type",
        "title_ru": "Тип IV — застывшая vṛddhi",
        "aliases": {
            "ru": ["тип IV", "застывшая вриддхи"],
            "deva": ["चतुर्थवर्г"],
            "iast": ["type IV"],
            "slp1": ["typeIV"],
        },
        "summary_ru": (
            "Тип IV в 1975 — короткий закрытый список (ḍhauk, mārg, kāṅkṣ, vāñch, dhāv, cāy): "
            "корень задан в vṛddhi и почти не чередуется. Это не IV презентный класс Уитни "
            "(ya-класс divyati). Очерк 1978 такого списка типов не ведёт."
        ),
        "alignment_note": "1975 type IV ≠ Whitney present class IV.",
        "prereq": ["subject:grammar-lab:root-type-i"],
        "difficulty": "advanced",
        "whitney": ["whitney-sec:235-243"],
        "z1975": ["zalizniak-1975:type-iv"],
        "z1978": ["zalizniak-1978-sec:60"],
        "z2004": ["zalizniak-2004:partial-alternators"],
        "root": 528,
        "ex": {
            "prompt": "Тип IV статьи 1975 — это то же, что IV класс Уитни (divyati)?",
            "choices": ["да", "нет"],
            "answer": "нет",
        },
    },
    {
        "slug": "set-anit-vet",
        "cluster": "alternation",
        "title_ru": "seṭ, aniṭ и veṭ",
        "aliases": {
            "ru": ["сеṭ", "аниṭ", "веṭ", "соединительная i"],
            "deva": ["सेट्", "अनिट्", "वेट्"],
            "iast": ["seṭ", "aniṭ", "veṭ", "union-vowel i"],
            "slp1": ["sew", "aniw", "vew"],
        },
        "summary_ru": (
            "Зализняк делит корни по наличию соединительного i перед согласным суффиксом "
            "(§63 очерка; конспект 2004). Уитни того же i называет union-vowel и описывает "
            "по формам (инфинитив, будущее, PPP), не вводя термины seṭ/aniṭ. Смешанный "
            "(veṭ) тип нельзя сводить к одному правилу."
        ),
        "alignment_note": "Same connective i; Whitney has no seṭ/aniṭ terms.",
        "prereq": ["subject:grammar-lab:ablaut-grades"],
        "difficulty": "intermediate",
        "whitney": ["whitney-sec:254", "whitney-sec:934-935", "whitney-sec:956", "whitney-sec:968"],
        "z1975": ["zalizniak-1975:set-anit"],
        "z1978": ["zalizniak-1978-sec:63"],
        "z2004": ["zalizniak-2004:set-anit"],
        "root": 528,
        "ex": {
            "prompt": "Форма bhaviṣyati показывает, что bhū в будущем ведёт себя как…",
            "choices": ["aniṭ", "seṭ", "без соединительного гласного"],
            "answer": "seṭ",
        },
    },
    {
        "slug": "samprasarana",
        "cluster": "alternation",
        "title_ru": "Саспрасарана",
        "aliases": {
            "ru": ["сампрасарана", "вокализация сонанта"],
            "deva": ["सम्प्रसारण"],
            "iast": ["samprasāraṇa", "samprasarana"],
            "slp1": ["samprasAraRa"],
        },
        "summary_ru": (
            "Саспрасарана — чередование ya/va/ra в полной ступени с i/u/ṛ в слабой "
            "(yaj / iṣṭaḥ, vac / uktaḥ, svap / suptaḥ). Уитни §252; Зализняк 1975 как "
            "ряды YA/VA/RA; очерк §50/52. Это не отдельный презентный класс."
        ),
        "alignment_note": "Same named process in both spines.",
        "prereq": ["subject:grammar-lab:alternation-series"],
        "difficulty": "intermediate",
        "whitney": ["whitney-sec:252"],
        "z1975": ["zalizniak-1975:samprasarana"],
        "z1978": ["zalizniak-1978-sec:50", "zalizniak-1978-sec:52"],
        "z2004": ["zalizniak-2004:three-grade"],
        "root": 699,
        "ex": {
            "prompt": "Слабая ступень корня vac «говорить» — это…",
            "choices": ["vac", "uc / ukta", "vāc"],
            "answer": "uc / ukta",
        },
    },
    {
        "slug": "nasal-alternation",
        "cluster": "alternation",
        "title_ru": "Носовые чередования рядов M и N",
        "aliases": {
            "ru": ["носовое чередование", "ряд M", "ряд N"],
            "deva": ["अनुनासिक"],
            "iast": ["nasal alternation", "M-series", "N-series"],
            "slp1": ["M1", "N1"],
        },
        "summary_ru": (
            "Ряды M/N Зализняка описывают gam / gataḥ, man / mataḥ, tan / tataḥ и сдвиги "
            "между носовым рядом и A1 (daṃś / daśati). Уитни даёт те же формы по классам "
            "и по PPP, не собирая их в ряды M/N. Часть корней исторически уходит в A1 — "
            "это смена нормы, не «невозможность» носовой ступени."
        ),
        "alignment_note": "Shared forms; series label is Zalizniak-only.",
        "prereq": ["subject:grammar-lab:alternation-series"],
        "difficulty": "intermediate",
        "whitney": ["whitney-sec:952-956", "whitney-sec:683-696"],
        "z1975": ["zalizniak-1975:series-mn"],
        "z1978": ["zalizniak-1978-sec:60"],
        "z2004": ["zalizniak-2004:three-grade"],
        "root": 170,
        "ex": {
            "prompt": "PPP от gam — это…",
            "choices": ["gamitaḥ", "gataḥ", "gāntaḥ"],
            "answer": "gataḥ",
        },
    },
    {
        "slug": "root-designation",
        "cluster": "homonymy",
        "title_ru": "Обозначение корня: реальное и условное",
        "aliases": {
            "ru": ["обозначение корня", "условный корень", "реальный корень"],
            "deva": ["धातुसंज्ञा"],
            "iast": ["root designation", "conventional root"],
            "slp1": ["DAtu"],
        },
        "summary_ru": (
            "Зализняк 1975 различает реальное обозначение (ru) и условное (kṛ / kṝ). "
            "Тип задаёт, какую ступень берут за заголовок: II — guṇa, III — нуль, IV — vṛddhi, "
            "I — зависит от ряда. Уитни Roots использует свой список заголовков; расхождения "
            "(krap ↔ kṛp, spardh ↔ spṛdh) — конвенция цитаты, не два корня."
        ),
        "alignment_note": "1975 states the convention; Whitney is the cited list, not a rival calculus.",
        "prereq": ["subject:grammar-lab:root-type-i"],
        "difficulty": "advanced",
        "whitney": ["whitney-sec:98-100"],
        "z1975": ["zalizniak-1975:root-designation"],
        "z1978": ["zalizniak-1978-sec:25"],
        "z2004": ["zalizniak-2004:morphonology"],
        "root": 106,
        "ex": {
            "prompt": "Заголовок smṛ (не smar) выбран потому, что корень типа I ряда R. Это…",
            "choices": ["условное обозначение", "единственный реальный алломорф"],
            "answer": "условное обозначение",
        },
    },
    {
        "slug": "root-homonymy",
        "cluster": "homonymy",
        "title_ru": "Омонимия корней",
        "aliases": {
            "ru": ["омонимия корней", "два as", "два vas"],
            "deva": ["समानधातु"],
            "iast": ["root homonymy"],
            "slp1": ["as#1", "as#2"],
        },
        "summary_ru": (
            "Одинаковое написание не есть один корень: as «быть» (тип I) и as «бросать» "
            "(тип II); vas «сиять» / vas «одевать». Уитни нумерует омонимы в Roots "
            "(whitney_no 22 vs 23). Свёртка DCS-частоты по омонимам в pin-срезе — ограничение "
            "снимка, не доказательство тождества."
        ),
        "alignment_note": "Both spines keep homonyms distinct. Do not merge frequencies into identity.",
        "prereq": ["subject:grammar-lab:root-type-i"],
        "difficulty": "intermediate",
        "whitney": ["whitney-sec:608", "whitney-sec:636"],
        "z1975": ["zalizniak-1975:homonymy"],
        "z1978": ["zalizniak-1978-sec:127"],
        "z2004": ["zalizniak-2004:morphonology"],
        "root": 22,
        "ex": {
            "prompt": "as «быть» и as «бросать» у Зализняка 1975 — это…",
            "choices": ["один корень двух типов", "два омонима разных типов"],
            "answer": "два омонима разных типов",
        },
    },
    {
        "slug": "root-variants",
        "cluster": "homonymy",
        "title_ru": "Варианты корня",
        "aliases": {
            "ru": ["вариант корня", "параллельный корень"],
            "deva": ["धातुभेद"],
            "iast": ["root variant", "dham // dhmā"],
            "slp1": ["Dam", "DmA"],
        },
        "summary_ru": (
            "1975 трактует dham // dhmā как два классификационных узла, из которых "
            "собирается одна парадигма. Уитни даёт такие пары как варианты одного корня "
            "или как отдельные статьи. Нельзя автоматически схлопывать вариант в омоним "
            "или в один тип."
        ),
        "alignment_note": "Variant ≠ homonym. Classification unit in 1975 is the variant.",
        "prereq": ["subject:grammar-lab:root-designation"],
        "difficulty": "advanced",
        "whitney": ["whitney-sec:251"],
        "z1975": ["zalizniak-1975:root-variants"],
        "z1978": ["zalizniak-1978-sec:111"],
        "z2004": ["zalizniak-2004:morphonology"],
        "root": 874,
        "ex": {
            "prompt": "dham и dhmā в классификации 1975 считаются…",
            "choices": ["одним узлом", "двумя вариантами-узлами одной парадигмы"],
            "answer": "двумя вариантами-узлами одной парадигмы",
        },
    },
    {
        "slug": "quasi-roots",
        "cluster": "homonymy",
        "title_ru": "Квазикорни",
        "aliases": {
            "ru": ["квазикорень", "вторичный корень"],
            "deva": ["गौणधातु"],
            "iast": ["quasi-root", "secondary root", "dad"],
            "slp1": ["dad"],
        },
        "summary_ru": (
            "Квазикорень 1975 (Whitney §66/§102 secondary root) извлекается из презенса "
            "и обслуживает часть парадигмы (dad от dā → dattaḥ). Это не отдельный "
            "первичный корень списка Уитни и не тип IV."
        ),
        "alignment_note": "Both spines name the phenomenon; 1975 treats it as a classification unit.",
        "prereq": ["subject:grammar-lab:root-variants"],
        "difficulty": "advanced",
        "whitney": ["whitney-sec:66", "whitney-sec:102"],
        "z1975": ["zalizniak-1975:quasi-roots"],
        "z1978": ["zalizniak-1978-sec:131"],
        "z2004": ["zalizniak-2004:morphonology"],
        "root": 349,
        "ex": {
            "prompt": "dattaḥ от dā построен от…",
            "choices": ["первичного dā без изменения", "квазикорня dad"],
            "answer": "квазикорня dad",
        },
    },
    {
        "slug": "attested-vs-predicted",
        "cluster": "attestation",
        "title_ru": "Засвидетельствованное и предсказанное",
        "aliases": {
            "ru": ["засвидетельствованная форма", "предсказанная форма"],
            "deva": ["प्रयुक्ता"],
            "iast": ["attested", "predicted", "grammarian form"],
            "slp1": ["prayukta"],
        },
        "summary_ru": (
            "И Уитни, и Зализняк 1975 опираются на засвидетельствованные формы; места, "
            "где взяты показания индийских грамматистов, оговариваются отдельно. Отсутствие "
            "формы в DCS-снимке не доказывает, что форма невозможна, и не назначает тип."
        ),
        "alignment_note": "Both spines privilege attestation. Corpus gap ≠ linguistic claim.",
        "prereq": ["subject:grammar-lab:ablaut-grades"],
        "difficulty": "intro",
        "whitney": ["whitney-sec:98-100"],
        "z1975": ["zalizniak-1975:inventory-scope"],
        "z1978": ["zalizniak-1978-sec:109"],
        "z2004": ["zalizniak-2004:morphonology"],
        "root": 815,
        "ex": {
            "prompt": "dcs_freq = 0 в pin-срезе значит…",
            "choices": ["форма невозможна", "в этом снимке нет токенов"],
            "answer": "в этом снимке нет токенов",
        },
    },
    {
        "slug": "open-vs-closed-roots",
        "cluster": "alternation",
        "title_ru": "Открытые и закрытые корни",
        "aliases": {
            "ru": ["открытый корень", "закрытый корень"],
            "deva": ["व्यक्तधातु"],
            "iast": ["open root", "closed root"],
            "slp1": ["open", "closed"],
        },
        "summary_ru": (
            "Очерк §61: открытый корень кончается чередующимся элементом (sthā, i, śru), "
            "закрытый имеет после него согласную (chid, iṣ). Конспект 2004 повторяет деление. "
            "Уитни описывает те же исходы корня без этой пары терминов. Деление важно для "
            "выбора сильной/слабой основы и для seṭ."
        ),
        "alignment_note": "1978/2004 terms; Whitney describes finals without the labels.",
        "prereq": ["subject:grammar-lab:alternation-series"],
        "difficulty": "intro",
        "whitney": ["whitney-sec:235-243"],
        "z1975": ["zalizniak-1975:series-a2"],
        "z1978": ["zalizniak-1978-sec:61"],
        "z2004": ["zalizniak-2004:open-closed"],
        "root": 815,
        "ex": {
            "prompt": "chid «рассекать» по очерку §61 — это корень…",
            "choices": ["открытый", "закрытый"],
            "answer": "закрытый",
        },
    },
    {
        "slug": "present-thematic-vs-athematic",
        "cluster": "tense-stem",
        "title_ru": "Тематическое и атематическое спряжение",
        "aliases": {
            "ru": ["тематическое спряжение", "атематическое спряжение"],
            "deva": ["विकरण"],
            "iast": ["thematic", "athematic"],
            "slp1": ["tematic", "atematic"],
        },
        "summary_ru": (
            "Уитни делит презенс на a-спряжение и не-a. Очерк §114 — та же граница. "
            "Это морфология презенса, не тип корня 1975: один корень типа I может быть "
            "и тематическим (bhavati), и атематическим (karoti)."
        ),
        "alignment_note": "Shared present-system cut. Independent of 1975 type I–IV.",
        "prereq": ["subject:grammar-lab:ablaut-grades"],
        "difficulty": "intro",
        "whitney": ["whitney-sec:599-606"],
        "z1975": ["zalizniak-1975:morphological-positions"],
        "z1978": ["zalizniak-1978-sec:114"],
        "z2004": ["zalizniak-2004:verb-overview"],
        "root": 528,
        "ex": {
            "prompt": "bhavati — форма…",
            "choices": ["тематическая", "атематическая"],
            "answer": "тематическая",
        },
    },
    {
        "slug": "present-root-class",
        "cluster": "tense-stem",
        "title_ru": "Презенс II класса (корневой)",
        "aliases": {
            "ru": ["второй класс", "корневой презенс", "класс ad"],
            "deva": ["अदादि"],
            "iast": ["root class", "class 2", "ad-class"],
            "slp1": ["adAdi"],
        },
        "summary_ru": (
            "Уитни §§611–641: основа равна корню, сильные формы с guṇa. Очерк §127. "
            "Не путать с типом II 1975. Образцы: dviṣ / dveṣṭi, as / asti."
        ),
        "alignment_note": "Whitney class 2 = 1978 class II. Not 1975 type II.",
        "prereq": ["subject:grammar-lab:present-thematic-vs-athematic"],
        "difficulty": "intermediate",
        "whitney": ["whitney-sec:611-641"],
        "z1975": ["zalizniak-1975:morphological-positions"],
        "z1978": ["zalizniak-1978-sec:127"],
        "z2004": ["zalizniak-2004:verb-overview"],
        "root": 22,
        "ex": {
            "prompt": "asti относится к презентному классу…",
            "choices": ["I", "II", "IV", "VI"],
            "answer": "II",
        },
    },
    {
        "slug": "present-reduplicating",
        "cluster": "tense-stem",
        "title_ru": "Презенс III класса (удваивающий)",
        "aliases": {
            "ru": ["третий класс", "удваивающий презенс", "класс hu"],
            "deva": ["जुहोत्यादि"],
            "iast": ["reduplicating class", "class 3", "hu-class"],
            "slp1": ["juhotyAdi"],
        },
        "summary_ru": (
            "Уитни §§642–682; очерк §130. Сильная основа juhoti, слабая juhvati. "
            "Не тип III 1975. Удвоение здесь презенсное, не перфектное (§113 очерка)."
        ),
        "alignment_note": "Whitney class 3 = 1978 class III. Not 1975 type III.",
        "prereq": ["subject:grammar-lab:present-thematic-vs-athematic"],
        "difficulty": "intermediate",
        "whitney": ["whitney-sec:642-682"],
        "z1975": ["zalizniak-1975:morphological-positions"],
        "z1978": ["zalizniak-1978-sec:130", "zalizniak-1978-sec:113"],
        "z2004": ["zalizniak-2004:verb-overview"],
        "root": 919,
        "ex": {
            "prompt": "juhoti — презенс какого традиционного класса?",
            "choices": ["I", "II", "III", "VII"],
            "answer": "III",
        },
    },
    {
        "slug": "present-nasal-infix",
        "cluster": "tense-stem",
        "title_ru": "Презенс VII класса (носовой инфикс)",
        "aliases": {
            "ru": ["седьмой класс", "носовой инфикс", "класс rudh"],
            "deva": ["रुधादि"],
            "iast": ["nasal infix", "class 7", "rudh-class"],
            "slp1": ["ruDAdi"],
        },
        "summary_ru": (
            "Уитни §§683–696; очерк §134: chinatti / chindanti. Инфикс чередуется, "
            "корень в слабой ступени. Это презентная морфология, не ряд N."
        ),
        "alignment_note": "Shared class-7 description. Distinct from M/N ablaut series.",
        "prereq": ["subject:grammar-lab:nasal-alternation"],
        "difficulty": "intermediate",
        "whitney": ["whitney-sec:683-696"],
        "z1975": ["zalizniak-1975:morphological-positions"],
        "z1978": ["zalizniak-1978-sec:134"],
        "z2004": ["zalizniak-2004:verb-overview"],
        "root": 242,
        "ex": {
            "prompt": "3 sg презенса от chid VII класса — это…",
            "choices": ["chidati", "chinatti", "chedati"],
            "answer": "chinatti",
        },
    },
    {
        "slug": "present-nu-class",
        "cluster": "tense-stem",
        "title_ru": "Презенс V/VIII классов (суффикс no/nu)",
        "aliases": {
            "ru": ["пятый класс", "восьмой класс", "класс su", "класс tan"],
            "deva": ["स्वादि", "तनादि"],
            "iast": ["nu-class", "class 5", "class 8"],
            "slp1": ["svAdi", "tanAdi"],
        },
        "summary_ru": (
            "Очерк §135 объединяет индийские V и VIII: sunoti, tanoti, аномалия karoti/kurvanti. "
            "Уитни держит классы раздельно (§§697–716). śṛṇoti от śru построено по формуле VII."
        ),
        "alignment_note": "1978 unifies V+VIII; Whitney keeps them apart. Both describe the same stems.",
        "prereq": ["subject:grammar-lab:present-thematic-vs-athematic"],
        "difficulty": "intermediate",
        "whitney": ["whitney-sec:697-716"],
        "z1975": ["zalizniak-1975:morphological-positions"],
        "z1978": ["zalizniak-1978-sec:135"],
        "z2004": ["zalizniak-2004:verb-overview"],
        "root": 815,
        "ex": {
            "prompt": "Презенс 3 sg от śru — это…",
            "choices": ["śravati", "śṛṇoti", "śṛṇāti"],
            "answer": "śṛṇoti",
        },
    },
    {
        "slug": "present-na-class",
        "cluster": "tense-stem",
        "title_ru": "Презенс IX класса (суффикс nā/nī)",
        "aliases": {
            "ru": ["девятый класс", "класс krī"],
            "deva": ["क्र्यादि"],
            "iast": ["nā-class", "class 9", "krī-class"],
            "slp1": ["kryAdi"],
        },
        "summary_ru": (
            "Уитни §§717–732; очерк §136: krīṇāti, gṛhṇāti, jānāti. Корень в слабой ступени. "
            "Не путать с каузативом на -aya."
        ),
        "alignment_note": "Shared class-9 description.",
        "prereq": ["subject:grammar-lab:present-thematic-vs-athematic"],
        "difficulty": "intermediate",
        "whitney": ["whitney-sec:717-732"],
        "z1975": ["zalizniak-1975:morphological-positions"],
        "z1978": ["zalizniak-1978-sec:136"],
        "z2004": ["zalizniak-2004:verb-overview"],
        "root": 120,
        "ex": {
            "prompt": "3 sg презенса от krī — это…",
            "choices": ["krayati", "krīṇāti", "krīṇoti"],
            "answer": "krīṇāti",
        },
    },
    {
        "slug": "present-thematic-a",
        "cluster": "tense-stem",
        "title_ru": "Простой тематический презенс (I и VI)",
        "aliases": {
            "ru": ["первый класс", "шестой класс", "тематический презенс"],
            "deva": ["भ्वादि", "तुदादि"],
            "iast": ["class 1", "class 6", "bhavati", "tudati"],
            "slp1": ["Bavati", "tudati"],
        },
        "summary_ru": (
            "Очерк §117: корень + a покрывает индийские I (ударение на корне, часто guṇa) "
            "и VI (ударение на a, часто нуль). Уитни §§733–758 держит классы раздельно. "
            "Не тип I 1975."
        ),
        "alignment_note": "1978 groups I+VI; Whitney separates them. Neither is 1975 type I.",
        "prereq": ["subject:grammar-lab:present-thematic-vs-athematic"],
        "difficulty": "intro",
        "whitney": ["whitney-sec:733-758"],
        "z1975": ["zalizniak-1975:morphological-positions"],
        "z1978": ["zalizniak-1978-sec:117"],
        "z2004": ["zalizniak-2004:verb-overview"],
        "root": 528,
        "ex": {
            "prompt": "bhavati — традиционный презентный класс…",
            "choices": ["I", "II", "IV", "X"],
            "answer": "I",
        },
    },
    {
        "slug": "present-ya-class",
        "cluster": "tense-stem",
        "title_ru": "Презенс IV класса (суффикс ya)",
        "aliases": {
            "ru": ["четвёртый класс", "класс div"],
            "deva": ["दिवादि"],
            "iast": ["ya-class", "class 4", "divyati"],
            "slp1": ["divAdi"],
        },
        "summary_ru": (
            "Уитни §§759–767; очерк §118: корень в слабой ступени + ya (manyate, nṛtyati). "
            "Не пассив на -ya (§160 очерка / Whitney §§768–774) и не тип IV 1975."
        ),
        "alignment_note": "Class 4 ≠ passive ya ≠ 1975 type IV.",
        "prereq": ["subject:grammar-lab:present-thematic-vs-athematic"],
        "difficulty": "intermediate",
        "whitney": ["whitney-sec:759-767"],
        "z1975": ["zalizniak-1975:morphological-positions"],
        "z1978": ["zalizniak-1978-sec:118"],
        "z2004": ["zalizniak-2004:verb-overview"],
        "root": 546,
        "ex": {
            "prompt": "manyate — это презенс IV класса или пассив?",
            "choices": ["IV класс от man", "пассив от man"],
            "answer": "IV класс от man",
        },
    },
    {
        "slug": "present-aya-class",
        "cluster": "tense-stem",
        "title_ru": "Презенс с -aya и X класс",
        "aliases": {
            "ru": ["десятый класс", "класс cur", "суффикс aya"],
            "deva": ["चुरादि"],
            "iast": ["aya-present", "class 10", "cur-class"],
            "slp1": ["curAdi"],
        },
        "summary_ru": (
            "Очерк §119: -aya у первичных редок (hvayati). X класс / каузатив Уитни "
            "§§775, 1041–1052 и очерк §167 — производная основа. Не смешивать hvaya- "
            "как презенс от варианта и kārayati как каузатив."
        ),
        "alignment_note": "Primary aya-present ≠ causative aya. Both spines distinguish them.",
        "prereq": ["subject:grammar-lab:present-thematic-a"],
        "difficulty": "advanced",
        "whitney": ["whitney-sec:775", "whitney-sec:1041-1052"],
        "z1975": ["zalizniak-1975:quasi-roots"],
        "z1978": ["zalizniak-1978-sec:119", "zalizniak-1978-sec:167"],
        "z2004": ["zalizniak-2004:verb-overview"],
        "root": 106,
        "ex": {
            "prompt": "kārayati — это прежде всего…",
            "choices": ["первичный X класс без каузации", "каузатив на -aya"],
            "answer": "каузатив на -aya",
        },
    },
    {
        "slug": "perfect-strong-weak",
        "cluster": "tense-stem",
        "title_ru": "Перфект: сильная и слабая основы",
        "aliases": {
            "ru": ["перфект", "слабый перфект", "сильный перфект"],
            "deva": ["लिट्"],
            "iast": ["perfect", "cakāra", "cakruḥ"],
            "slp1": ["liw", "cakAra"],
        },
        "summary_ru": (
            "Уитни §§781–823; очерк §§150–153. Сильный sg act. часто с guṇa/vṛddhi, "
            "слабые формы — с нулём или с e-заменой (seduḥ). В 1975 слабый удвоенный "
            "перфект входит в позицию 1. e-перфект (tepuḥ) — отдельное наложение, "
            "не клетка трёхступенчатой таблицы."
        ),
        "alignment_note": "Shared perfect stem facts. 1975 assigns weak reduplicated perfect to MP1.",
        "prereq": ["subject:grammar-lab:morphological-positions"],
        "difficulty": "intermediate",
        "whitney": ["whitney-sec:781-823"],
        "z1975": ["zalizniak-1975:morphological-positions"],
        "z1978": ["zalizniak-1978-sec:150", "zalizniak-1978-sec:152"],
        "z2004": ["zalizniak-2004:verb-overview"],
        "root": 106,
        "ex": {
            "prompt": "3 pl перфекта от kṛ — это…",
            "choices": ["cakāra", "cakruḥ", "akārṣīt"],
            "answer": "cakruḥ",
        },
    },
    {
        "slug": "aorist-systems",
        "cluster": "tense-stem",
        "title_ru": "Системы аориста",
        "aliases": {
            "ru": ["аорист", "сигматический аорист", "корневой аорист"],
            "deva": ["लुङ्"],
            "iast": ["aorist", "s-aorist", "root aorist"],
            "slp1": ["luN"],
        },
        "summary_ru": (
            "Уитни §§824–920 выделяет простой, удвоенный и сигматический аористы. "
            "Очерк §§139–147 нумерует семь типов. 1975 использует аорист 4/5 как "
            "диагностику позиции 3. Нумерации не совпадают один к одному: сверять "
            "по строению основы, не по номеру."
        ),
        "alignment_note": "Do not equate Whitney aorist numbers with Zalizniak 1–7 without the stem formula.",
        "prereq": ["subject:grammar-lab:morphological-positions"],
        "difficulty": "advanced",
        "whitney": ["whitney-sec:824-827", "whitney-sec:878-897"],
        "z1975": ["zalizniak-1975:morphological-positions"],
        "z1978": ["zalizniak-1978-sec:139", "zalizniak-1978-sec:144"],
        "z2004": ["zalizniak-2004:verb-overview"],
        "root": 106,
        "ex": {
            "prompt": "akārṣīt — это аорист с показателем…",
            "choices": ["нулевым (корневой)", "s (сигматический)", "тематическим -a"],
            "answer": "s (сигматический)",
        },
    },
    {
        "slug": "future-sya",
        "cluster": "tense-stem",
        "title_ru": "Будущее на -sya / -iṣya",
        "aliases": {
            "ru": ["будущее время", "суффикс sya", "простое будущее"],
            "deva": ["लृट्", "स्य"],
            "iast": ["sya-future", "bhaviṣyati", "vakṣyati"],
            "slp1": ["lfw", "sya"],
        },
        "summary_ru": (
            "Уитни §§931–940; очерк §157: корень в guṇa + sya, у seṭ — iṣya. "
            "В 1975 это морфологическая позиция 2. Наличие i — отдельная ось seṭ/aniṭ, "
            "не смена ступени."
        ),
        "alignment_note": "Shared future stem. 1975 labels it MP2.",
        "prereq": ["subject:grammar-lab:set-anit-vet"],
        "difficulty": "intro",
        "whitney": ["whitney-sec:931-940"],
        "z1975": ["zalizniak-1975:morphological-positions"],
        "z1978": ["zalizniak-1978-sec:157"],
        "z2004": ["zalizniak-2004:set-anit"],
        "root": 528,
        "ex": {
            "prompt": "Будущее от bhū — это…",
            "choices": ["bhūsyati", "bhaviṣyati", "bhavsyati"],
            "answer": "bhaviṣyati",
        },
    },
    {
        "slug": "causative-grade",
        "cluster": "grade",
        "title_ru": "Ступень каузатива",
        "aliases": {
            "ru": ["каузатив", "каузативная огласовка"],
            "deva": ["णिच्"],
            "iast": ["causative", "kārayati", "gamayati"],
            "slp1": ["Ric", "kArayati"],
        },
        "summary_ru": (
            "Уитни §§1041–1052; очерк §167: презенс каузатива = ступень 3 sg перфекта + aya. "
            "1975 относит часть каузативов к позиции 3 (vṛddhi: kārayati, śrāvayati), "
            "часть — к позиции 2. gamayati с guṇa — оговорённое исключение, не опровержение правила."
        ),
        "alignment_note": "Shared causative. 1975 splits MP2/MP3 by root shape.",
        "prereq": ["subject:grammar-lab:morphological-positions"],
        "difficulty": "intermediate",
        "whitney": ["whitney-sec:1041-1052"],
        "z1975": ["zalizniak-1975:morphological-positions"],
        "z1978": ["zalizniak-1978-sec:167"],
        "z2004": ["zalizniak-2004:verb-overview"],
        "root": 106,
        "ex": {
            "prompt": "kārayati имеет в корне ступень…",
            "choices": ["нулевую", "guṇa", "vṛddhi"],
            "answer": "vṛddhi",
        },
    },
    {
        "slug": "passive-ya",
        "cluster": "tense-stem",
        "title_ru": "Пассив на -ya",
        "aliases": {
            "ru": ["пассив", "пассив на ya"],
            "deva": ["कर्मणि", "यक्"],
            "iast": ["passive", "kriyate", "bhūyate"],
            "slp1": ["kriyate"],
        },
        "summary_ru": (
            "Уитни §§768–774; очерк §160. Основа пассива — слабая ступень + ya, окончания "
            "медиальные. В 1975 некаузативный пассив входит в позицию 1. Не IV класс "
            "(manyate) и не каузативный пассив."
        ),
        "alignment_note": "Shared passive. Distinct from class-4 ya.",
        "prereq": ["subject:grammar-lab:present-ya-class"],
        "difficulty": "intro",
        "whitney": ["whitney-sec:768-774"],
        "z1975": ["zalizniak-1975:morphological-positions"],
        "z1978": ["zalizniak-1978-sec:160"],
        "z2004": ["zalizniak-2004:verb-overview"],
        "root": 106,
        "ex": {
            "prompt": "Пассив 3 sg от kṛ — это…",
            "choices": ["karoti", "kriyate", "kāryate"],
            "answer": "kriyate",
        },
    },
    {
        "slug": "ppp-ta-na",
        "cluster": "tense-stem",
        "title_ru": "Причастие на -ta / -na",
        "aliases": {
            "ru": ["причастие на ta", "PPP", "причастие на na"],
            "deva": ["क्त"],
            "iast": ["ta-participle", "kṛta", "chinna"],
            "slp1": ["kta", "kfta"],
        },
        "summary_ru": (
            "Уитни §§952–956; очерк §162. Диагностическая форма позиции 1 в 1975 "
            "(kṛtaḥ, chinnaḥ). seṭ даёт -ita- (patitaḥ). Отсутствие токена в DCS не отменяет "
            "словарный PPP Уитни."
        ),
        "alignment_note": "Shared PPP. 1975 uses it as MP1 diagnostic.",
        "prereq": ["subject:grammar-lab:morphological-positions"],
        "difficulty": "intro",
        "whitney": ["whitney-sec:952-956"],
        "z1975": ["zalizniak-1975:morphological-positions"],
        "z1978": ["zalizniak-1978-sec:162"],
        "z2004": ["zalizniak-2004:set-anit"],
        "root": 106,
        "ex": {
            "prompt": "PPP от kṛ — это…",
            "choices": ["kārtaḥ", "kṛtaḥ", "karitaḥ"],
            "answer": "kṛtaḥ",
        },
    },
    {
        "slug": "infinitive-tum",
        "cluster": "tense-stem",
        "title_ru": "Инфинитив на -tum",
        "aliases": {
            "ru": ["инфинитив", "суффикс tum"],
            "deva": ["तुमुन्"],
            "iast": ["infinitive", "kartum", "bhavitum"],
            "slp1": ["tumun", "kartum"],
        },
        "summary_ru": (
            "Уитни §968; очерк §164: guṇa + tum / itum. В 1975 это позиция 2. "
            "Тип III как раз и виден тем, что инфинитив остаётся без guṇa (bhikṣitum)."
        ),
        "alignment_note": "Shared infinitive. 1975 labels it MP2.",
        "prereq": ["subject:grammar-lab:set-anit-vet"],
        "difficulty": "intro",
        "whitney": ["whitney-sec:968"],
        "z1975": ["zalizniak-1975:morphological-positions"],
        "z1978": ["zalizniak-1978-sec:164"],
        "z2004": ["zalizniak-2004:set-anit"],
        "root": 106,
        "ex": {
            "prompt": "Инфинитив от kṛ — это…",
            "choices": ["kṛtum", "kartum", "kārtum"],
            "answer": "kartum",
        },
    },
]

NEEDS_REVIEW = {
    "slug": "type-equals-present-class",
    "cluster": "root-type",
    "status": "needs_review",
    "needs_review_reason": (
        "A published topic that treated 1975 types I–IV as Whitney present-classes "
        "I–IV would invent equivalence. Left as needs_review so the omit-from-bundle "
        "path stays exercised."
    ),
    "title_ru": "Тип 1975 не равен презентному классу",
    "aliases": {
        "ru": ["ложная эквивалентность типа и класса"],
        "deva": ["वर्ग"],
        "iast": ["type vs class"],
        "slp1": ["typeVSclass"],
    },
    "summary_ru": (
        "Черновик-предохранитель: тип I–IV статьи 1975 описывает чередование по "
        "позициям, презентные классы Уитни — устройство основы презенса. Публиковать "
        "как одно понятие нельзя."
    ),
    "alignment_note": "Explicit non-equivalence. Not publishable as a positive identification.",
    "prereq": ["subject:grammar-lab:root-type-i"],
    "difficulty": "advanced",
    "whitney": ["whitney-sec:599-606"],
    "z1975": ["zalizniak-1975:type-calculus"],
    "z1978": ["zalizniak-1978-sec:114"],
    "z2004": ["zalizniak-2004:verb-overview"],
    "root": 528,
    "ex": None,
}


DATASETS = {
    "whitney-sec": "SanskritGrammar/WhitneyGrammar_1889",
    "zalizniak-1975": "SanskritGrammar/ZalizniakMorphology_1975",
    "zalizniak-1978-sec": "SanskritGrammar/ZalizniakOcherk_1978",
    "zalizniak-2004": "SanskritGrammar/ZalizniakKonspekt_2004",
}


def topic_id(slug: str) -> str:
    return f"subject:grammar-lab:{slug}"


def build_topic(spec: dict, rows: dict[int, dict]) -> tuple[dict, dict | None]:
    slug = spec["slug"]
    tid = topic_id(slug)
    status = spec.get("status", "published")
    sources = []
    for sec in spec["whitney"]:
        sources.append(_edge("whitney-sec", sec, tid, DATASETS["whitney-sec"]))
    for loc in spec.get("z1975", []):
        sources.append(_edge("zalizniak-1975", loc, tid, DATASETS["zalizniak-1975"]))
    for loc in spec.get("z1978", []):
        sources.append(_edge("zalizniak-1978-sec", loc, tid, DATASETS["zalizniak-1978-sec"]))
    for loc in spec.get("z2004", []):
        sources.append(_edge("zalizniak-2004", loc, tid, DATASETS["zalizniak-2004"]))
    root_no = spec["root"]
    iast, slp1, _hom, _gl = ROOT_BY_NO[root_no]
    sources.append(
        _edge("whitney-root", f"whitney-root:{root_no}", tid, "WhitneyRoots/crosswalk/roots.csv", slp1)
    )
    ex_spec = spec.get("ex")
    exercise = None
    ex_ids: list[str] = []
    if ex_spec and status == "published":
        eid = f"ex:grammar-lab:{slug}"
        ex_ids = [eid]
        choices = ex_spec["choices"]
        answer = ex_spec["answer"]
        exercise = {
            "id": eid,
            "schema_version": "1.0.0",
            "topic_id": tid,
            "risk_class": "deterministic",
            "status": "published",
            "prompt_ru": ex_spec["prompt"],
            "choices": choices,
            "answer": answer,
            "answer_normalized": answer.casefold().strip(),
            "distractors": [c for c in choices if c != answer],
            "approval_record": None,
            "source_ids": [s["anchor_id"] for s in sources[:2]],
        }
    topic = {
        "id": tid,
        "schema_version": "1.0.0",
        "status": status,
        "title_ru": spec["title_ru"],
        "cluster": spec["cluster"],
        "aliases": spec["aliases"],
        "summary_ru": spec["summary_ru"],
        "alignment_note": spec["alignment_note"],
        "prerequisites": spec["prereq"],
        "difficulty": spec["difficulty"],
        "sources": sources,
        "dictionary_evidence": [dict_card(rows, root_no)],
        "corpus_evidence": [corpus_card(rows, root_no)],
        "exercise_ids": ex_ids,
        "provenance": {
            "curated_date": DATE,
            "curator": CURATOR,
            "source_snapshot": SNAPSHOT,
            "notes": spec["alignment_note"],
        },
    }
    if status == "needs_review":
        topic["needs_review_reason"] = spec["needs_review_reason"]
    return topic, exercise


INTERPRETIVE = {
    "id": "ex:grammar-lab:type-vs-class-essay",
    "schema_version": "1.0.0",
    "topic_id": "subject:grammar-lab:root-type-i",
    "risk_class": "interpretive",
    "status": "approval-required",
    "prompt_ru": "Почему тип I Зализняка 1975 нельзя отождествлять с I презентным классом Уитни? Ответьте кратко по обеим осям.",
    "answer": "Тип описывает чередование по позициям; класс — устройство презенсной основы.",
    "answer_normalized": "type=ablaut-by-position; class=present-stem",
    "approval_record": None,
    "source_ids": ["zalizniak-1975:type-i", "whitney-sec:733-758"],
}


def emit() -> None:
    rows = _load_pin_rows()
    write_pin_slice(rows)
    topics_dir = LAB / "topics"
    ex_dir = LAB / "exercises"
    topics_dir.mkdir(parents=True, exist_ok=True)
    ex_dir.mkdir(parents=True, exist_ok=True)
    for old in list(topics_dir.glob("*.yml")) + list(ex_dir.glob("*.yml")):
        old.unlink()
    n_pub = 0
    for spec in TOPICS + [NEEDS_REVIEW]:
        topic, exercise = build_topic(spec, rows)
        path = topics_dir / f"{spec['slug']}.yml"
        path.write_text(
            yaml.safe_dump(topic, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        if topic["status"] == "published":
            n_pub += 1
        if exercise:
            (ex_dir / f"{spec['slug']}.yml").write_text(
                yaml.safe_dump(exercise, allow_unicode=True, sort_keys=False),
                encoding="utf-8",
            )
    (ex_dir / "type-vs-class-essay.yml").write_text(
        yaml.safe_dump(INTERPRETIVE, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"emitted published topics: {n_pub}; needs_review: 1; interpretive: 1")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--emit", action="store_true")
    args = p.parse_args(argv)
    if args.emit:
        emit()
        return 0
    p.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
