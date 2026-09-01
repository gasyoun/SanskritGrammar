#!/usr/bin/env python
"""Learn Your Way lesson-pack generator + validator (wave 1: Kochergina занятие 1).

H3521 / PLAN_LEARN_YOUR_WAY_SANSKRIT_SYSTEMA_WAVE1_25-08-2026.

Split of labor (ARCHITECTURE_LEARN_YOUR_WAY_LESSON_PACKS): the deterministic
assembler/validator is THIS committed script; the *prose* transformations
(re-leveling, interest swaps, quiz/mnemonic drafting) were authored by the
executing agent session (H3521-OxAlpha) and live in the CONTENT tables below,
so a regeneration reproduces the committed packs byte-for-byte.

Inputs (read-only):
    KocherginaUchebnik_1998/Kochergina_unicode.mdx   занятие-1 source slice
    KocherginaUchebnik_1998/claims.yml               verified-claims register
    KocherginaUchebnik_1998/LessonPacks/srs_aggregate.json  k-anon SRS fixture

Outputs (committed, byte-deterministic):
    KocherginaUchebnik_1998/LessonPacks/zan1/<profile>/
        manifest.json · personalized_text.md · views/mindmap.mmd · quizzes.json

Usage:
    python scripts/build_lessonpack.py --zan 1              # validate + summary
    python scripts/build_lessonpack.py --zan 1 --check      # validate-only (tests/CI)
    python scripts/build_lessonpack.py --zan 1 --build      # (re)generate the packs
    python scripts/build_lessonpack.py --zan 1 --emit-checklist  # agent-pass prompts
"""

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "KocherginaUchebnik_1998"
SOURCE_MDX = BOOK / "Kochergina_unicode.mdx"
CLAIMS_YML = BOOK / "claims.yml"
PACKS_ROOT = BOOK / "LessonPacks"
FIXTURE_PATH = PACKS_ROOT / "srs_aggregate.json"

SCHEMA = "lyw-pack-v1"
QUIZ_SCHEMA = "lyw-quiz-v1"
GENERATED_DATE = "25-08-2026"
SESSION_TAG = "H3521-OxAlpha"

LEVELS = ("nol", "prodolzhayushchiy")
INTERESTS = ("yoga", "ayurveda", "kino", "palomnichestvo")
INTEREST_RU = {
    "base": "базовый",
    "yoga": "йога",
    "ayurveda": "аюрведа",
    "kino": "индийское кино",
    "palomnichestvo": "паломничество",
}
LEVEL_RU = {"base": "база", "nol": "ноль", "prodolzhayushchiy": "продолжающий"}

ROMAN = {1: ("Занятие I", "Занятие II")}

BANDS = ("low", "mid", "high")
FIXTURE_FORBIDDEN_FIELDS = {
    "user", "user_id", "username", "email", "phone", "tg_id", "telegram_id",
    "name", "first_name", "last_name", "student_id", "group_member",
}

# --------------------------------------------------------------------------- #
# Source extraction + concept inventory (no-fabrication gate)
# --------------------------------------------------------------------------- #

LATIN_TOKEN_RE = re.compile(r"[A-Za-z\u0100-\u024F\u1E00-\u1EFF']+")
DEVA_TOKEN_RE = re.compile(r"[\u0900-\u097F]+")
ANSWER_LETTERS = "ABCDEFGH"


def normalize_token(tok: str) -> str:
    d = unicodedata.normalize("NFD", tok)
    d = "".join(c for c in d if not unicodedata.combining(c))
    return d.lower().strip("'’-")


def lesson_slice(zan: int) -> str:
    """Source text of one занятие, sliced from the mdx by its roman markers."""
    if zan not in ROMAN:
        raise SystemExit(f"zan={zan} out of wave-1 scope (supported: {sorted(ROMAN)})")
    marker, next_marker = ROMAN[zan]
    lines = SOURCE_MDX.read_text(encoding="utf-8").splitlines()
    start = end = None
    for i, ln in enumerate(lines):
        s = ln.strip()
        if start is None and s == marker:
            start = i
        elif start is not None and s == next_marker:
            end = i
            break
    if start is None or end is None:
        raise SystemExit(f"cannot locate source slice «{marker}»..«{next_marker}»")
    return "\n".join(lines[start:end])


def claims_entries():
    import yaml

    data = yaml.safe_load(CLAIMS_YML.read_text(encoding="utf-8"))
    return data.get("entries") or []


def lesson_claims(zan: int) -> list:
    """HK entries whose loc names this занятие exactly (none for занятие I yet)."""
    marker = ROMAN[zan][0]
    out = []
    for e in claims_entries():
        loc = str(e.get("loc", ""))
        if loc.split("/")[0].strip() == marker:
            out.append(e)
    return out


def claims_sha256() -> str:
    return hashlib.sha256(CLAIMS_YML.read_bytes()).hexdigest()


class Context:
    """Everything validators need about the source side of one занятие."""

    def __init__(self, zan: int):
        self.zan = zan
        self.slice_text = lesson_slice(zan)
        self.claims = lesson_claims(zan)
        self.claims_sha = claims_sha256()
        self.lesson_marker = ROMAN[zan][0]
        self.inventory = self._build_inventory()

    def _build_inventory(self):
        inv = set()
        for m in LATIN_TOKEN_RE.findall(self.slice_text):
            inv.add(m.lower())
            inv.add(normalize_token(m))
        for m in DEVA_TOKEN_RE.findall(self.slice_text):
            inv.add(m)
        for e in self.claims:
            eid = str(e.get("id", ""))
            inv.add(eid)
            inv.add(normalize_token(eid))
        return inv

    def knows(self, token: str) -> bool:
        t = str(token).strip()
        return t in self.inventory or normalize_token(t) in self.inventory


# --------------------------------------------------------------------------- #
# Authored content (agent pass H3521-OxAlpha) — the prose transformations
# --------------------------------------------------------------------------- #

SECTIONS = [
    {"id": "devanagari-script", "title": "Письмо devanāgarī",
     "concepts": ["devanāgarī"]},
    {"id": "sparsa-varga", "title": "Группа sparśa и пять рядов (varga)",
     "concepts": ["sparśa", "varga"]},
    {"id": "five-rows", "title": "Пять рядов: от горла к губам",
     "concepts": ["ka", "kha", "ga", "gha", "ṅa", "ca", "cha", "ja", "jha", "ña",
                  "ṭa", "ṭha", "ḍa", "ḍha", "ṇa", "ta", "tha", "da", "dha", "na",
                  "pa", "pha", "ba", "bha", "ma"]},
    {"id": "pronunciation", "title": "Произнесение согласных",
     "concepts": ["c", "j", "ṭ", "ḍ"]},
    {"id": "writing-rules", "title": "Правила написания и знаки daṇḍa",
     "concepts": ["daṇḍa"]},
]

SECTION_BODIES = {
    "devanagari-script": {
        "nol": (
            "В Индии большинство древних текстов записано письмом **devanāgarī** "
            "(«городское письмо богов»). Им же записан современный хинди — выучите "
            "одну графику, прочитаете два языка.\n\nГлавное правило: devanāgarī — письмо "
            "**слоговое**. Один знак передаёт целый слог, и каждый такой знак — это "
            "согласная **уже вместе с присущим ей гласным „а“**. Знак क — не «к», а «ка». "
            "Поэтому когда в учебнике написано *ka* — это уже произнесённый слог.\n\n"
            "Не спешите запоминать все знаки сразу: сегодня достаточно понять принцип "
            "«согласная + а»."
        ),
        "prodolzhayushchiy": (
            "Письмо **devanāgarī** обслуживает большинство памятников на древнеиндийских "
            "языках и современный хинди. Системно это абугида: графикой передаётся слог, "
            "но внутри каждого слога-знака читается структура «согласная + присущий "
            "гласный *a*»; отменяется он специальными значками — об этом следующие "
            "занятия.\n\nДля сравнения: русская буква «к» — фонема без гласного; "
            "санскритское क — уже открытый слог *ka*. Держите эту асимметрию в голове: "
            "она объясняет и словарные формы вида *kaṭa*, и то, почему транслитерация "
            "всегда снабжает согласную «а»."
        ),
    },
    "sparsa-varga": {
        "nol": (
            "Не пугайтесь терминов ниже — под каждым стоит простое телесное ощущение, "
            "и вы уже умеете его замечать (как позу или дыхание в практике).\n\n"
            "Попробуйте прямо сейчас: скажите вслух «к», потом «т», потом «п». Заметьте, "
            "что каждый раз воздух на мгновение полностью перекрывается — языком, зубами "
            "или губами — и звук получается коротким «щелчком». Это и есть то, что "
            "древнеиндийские фонетисты (за две тысячи лет до современной лингвистики) "
            "назвали **sparśa** — «прикосновение»: орган речи буквально прикасается и "
            "перекрывает воздух.\n\nТеперь скажите «к» и «г» подряд, прислушиваясь к "
            "горлу: «г» гудит (голос включён), «к» — нет. Это и есть второе, чему учит "
            "занятие: у каждого «щелчка» есть **четыре версии** (глухая/звонкая × "
            "с выдохом/без) плюс отдельная «носовая» версия, где воздух вместо рта идёт "
            "в нос (сравните «н» и «т»). Четыре версии плюс носовая — вот откуда берётся "
            "**пять** в каждом «ряду» (**varga**)."
        ),
        "prodolzhayushchiy": (
            "Группа **sparśa** («прикосновение») объединяет шумные взрывные и носовые "
            "сонанты; классификация физиологическая, восходящая к традиционной индийской "
            "фонетике (śikṣā). Деление на пять **varga** — рядов — задаёт двухпризнаковую "
            "матрицу: голос (глухость/звонкость) × придыхание, замыкаемую носовым.\n\n"
            "Эта системность — не учебная условность, а живая организация варга-таблиц, "
            "которую вы будете видеть в любой грамматике санскрита."
        ),
    },
    "five-rows": {
        "nol": (
            "Сделайте маленький эксперимент — пройдитесь языком по пяти точкам во рту "
            "«сзади наперёд», по одной букве на пробу:\n\n"
            "- **к** — самая глубокая точка, у мягкого нёба (там, где зевота);\n"
            "- **ч** — язык подходит ближе, к твёрдому нёбу;\n"
            "- **т, но с кончиком языка загнутым назад** — непривычная точка, знакомая "
            "разве что по слову «ложка», когда кончик языка случайно заворачивается;\n"
            "- **т** обычное — кончик языка у верхних зубов, как в русском;\n"
            "- **п** — совсем впереди, губами.\n\n"
            "Вот и все пять «мест во рту», которые санскритская фонетика различает — "
            "движение спереди назад вы только что почувствовали сами. Формальные "
            "названия этих пяти точек нужны только чтобы их называть, не более:\n\n"
            "1. **Заднеязычные** (та самая точка зевка): क ka · ख kha · ग ga · घ gha · "
            "ङ ṅa\n"
            "2. **Палатальные** (чуть впереди): च ca · छ cha · ज ja · झ jha · ञ ña\n"
            "3. **Церебральные**, или ретрофлексные (язык загнут назад — «ложка»): "
            "ट ṭa · ठ ṭha · ड ḍa · ढ ḍha · ण ṇa\n"
            "4. **Зубные** (у верхних зубов, как русское т/д): त ta · थ tha · द da · "
            "ध dha · न na\n"
            "5. **Губные** (губами): प pa · फ pha · ब ba · भ bha · म ma\n\n"
            "Заметьте: порядок внутри ряда всегда один и тот же — глухой, глухой "
            "придыхательный, звонкий, звонкий придыхательный, носовой."
        ),
        "prodolzhayushchiy": (
            "Матрица повторяется ряд за рядом — усвойте её один раз:\n\n"
            "1. **Заднеязычные**: क ka · ख kha · ग ga · घ gha · ङ ṅa\n"
            "2. **Палатальные**: च ca · छ cha · ज ja · झ jha · ञ ña\n"
            "3. **Церебральные** (ретрофлексные): ट ṭa · ठ ṭha · ड ḍa · ढ ḍha · ण ṇa\n"
            "4. **Зубные**: त ta · थ tha · द da · ध dha · न na\n"
            "5. **Губные**: प pa · फ pha · ब ba · भ bha · म ma\n\n"
            "Церебральный ряд — главная типологическая примета санскритского звучания для "
            "носителя русского: контраст т/т-ретрофлексный (рус. *т* vs хинди ट) здесь "
            "фонематичен."
        ),
    },
    "pronunciation": {
        "nol": (
            "Как это читать вслух:\n\n"
            "- **k, g, t, d, p, b** — почти как русские *к, г, т, д, п, б*.\n"
            "- **c** — как русское **ч** («чашка», «час»).\n"
            "- **j** — слитное **дж**, как в английском *age*, *magic*.\n"
            "- **Придыхательные** (kh, gh, ch, jh…) звучат со слабым **h**: после глухих — "
            "глухой выдох, после звонких — звонкий.\n"
            "- **Церебральные ṭ, ḍ** — как английские *t, d*, только кончик языка завёрнут "
            "назад.\n"
            "- Носовые: **ṅ** — как англ./нем. *ng*; **ñ** — мягкое «нь»; **ṇ** — "
            "церебральное «н»; **m, n** — как русские *м, н*."
        ),
        "prodolzhayushchiy": (
            "Чтение:\n\n"
            "- **k, g, t, d, p, b** ≈ русские соответствия.\n"
            "- **c** = рус. **ч**; **j** = слитное **дж** (англ. *age*).\n"
            "- Аспиранты (kh, gh, ch, jh…) — со слабым **h**: глухим после глухих, звонким "
            "после звонких взрывных.\n"
            "- Ретрофлексия: **ṭ, ḍ** — кончик языка завёрнут назад, нижняя сторона "
            "касается твёрдого нёба (≈ альвеолярные англ. *t, d*).\n"
            "- Носовые: **ṅ** = ŋ; **ñ** = мягкое «нь»; **ṇ** = церебральное «н»; "
            "**m, n** ≈ русские."
        ),
    },
    "writing-rules": {
        "nol": (
            "Письмо и знаки препинания:\n\n"
            "- Начертания знаков тренируйте по образцу из учебника: строгие горизонтальные "
            "строки, петли не вылезают за линейку.\n"
            "- Знаков препинания два, оба называются **daṇḍa** («палочка», «стержень»): "
            "одинарная палочка **।** работает как наша точка, двойная **॥** закрывает "
            "раздел или стих."
        ),
        "prodolzhayushchiy": (
            "Начертания отрабатываются по учебной схеме (горизонтальная шкапа, единый "
            "базовый штрих). Пунктуация исчерпывается двумя **daṇḍa**: одинарный **।** "
            "завершает предложение, двойной **॥** — раздел или стих."
        ),
    },
}

# Interest swaps — cultural framing around LESSON words only; grammar stays native.
SWAPS = {
    "yoga": [
        {"after": "five-rows",
         "text": "Слово **gaṇa** («множество») начинается с ग — первой строки таблицы "
                 "(заднеязычный ряд). Вы могли встретить этот корень в имени Gaṇeśa, "
                 "«господин свиты»: тот же корень, та же буква. Прочитайте ग как «га» — "
                 "и имя читается само."},
        {"after": "writing-rules",
         "text": "**Patha** («путь») — слово урока: путь практики начинается с первой "
                 "строки письма devanāgarī. Одна палочка । — выдох, двойная ॥ — завершение "
                 "цикла."},
    ],
    "ayurveda": [
        {"after": "five-rows",
         "text": "В уроке есть слова **dhana** («богатство») и **bhaga** («счастье»). "
                 "Аюрведа считает здоровье главным богатством: āyu- («жизнь») + veda — "
                 "\"знание жизни\". Буквы ध dha и भ bha — из зубного и губного рядов."},
        {"after": "pronunciation",
         "text": "Тренируйте церебральное ṇ на слове **nakha** («ноготь») — в аюрведических "
                 "текстах о care за телом оно встречается постоянно: кончик языка назад — "
                 "и звук правильный."},
    ],
    "kino": [
        {"after": "five-rows",
         "text": "Слово **naṭaka** из урока значит «танцор, актёр»: индийское кино выросло "
                 "из naṭaka-традиции. Обратите внимание на церебральное ण (ṇ) — этот "
                 "«завёрнутый» звук придаёт слову характерное санскритское звучание."},
        {"after": "pronunciation",
         "text": "Кассовые сборы считают словом **gaṇana** — «счёт»: ga-ṇa-na, три открытых "
                 "слога, как и положено словам этого занятия."},
    ],
    "palomnichestvo": [
        {"after": "five-rows",
         "text": "**Patha** («путь») — ключевое слово урока для паломника: маршрут к храму "
                 "в старину записывали именно devanāgarī. Прочитайте: pa-tha, два слога."},
        {"after": "writing-rules",
         "text": "После долгого patha паломник возвращается в свой **dama** («дом, "
                 "жилище»), а в дороге остаётся **gata** — «идущий». Три слова урока — и "
                 "целое путешествие."},
    ],
}

MNEMONICS_SHARED = [
    {"for": "devanāgarī",
     "sentence": "Каждая буква devanāgarī — слог-костюм: согласная уже одета в «а» (क = "
                 "к+а), раздевать её научат позже."},
    {"for": "varga",
     "sentence": "Ряды идут от горла к губам: К → Ч → Т(завёрнут.) → Т(зубн.) → П; в ряду "
                 "глухой шепчет, звонкий гудит, «+h» добавляет выдох, носовой замыкает."},
    {"for": "daṇḍa",
     "sentence": "Одна палочка । — точка, две палочки ॥ — конец главы: daṇḍa = дорожный "
                 "столбик текста."},
]

MNEMONICS_BY_LEVEL = {}

# Quiz bank: 6 core MCQs + one per-profile seventh.
CORE_QUIZ = [
    {"key": "01", "concept": ["sparśa", "varga"],
     "prompt": {"nol": "Сколько рядов (varga) в группе sparśa?",
                "prodolzhayushchiy": "Сколько варг (рядов) образуют группу sparśa?"},
     "options": ["Три", "Четыре", "Пять", "Десять"], "answer_index": 2},
    {"key": "02", "concept": ["ka"],
     "prompt": {"nol": "Какой гласный уже «спрятан» в каждой согласной букве devanāgarī, "
                       "например в क ka?",
                "prodolzhayushchiy": "Какой присущий гласный несёт каждая согласная "
                                     "графема (ср. ka, ga, pa)?"},
     "options": ["i", "a", "u", "никакой"], "answer_index": 1},
    {"key": "03", "concept": ["ca"],
     "prompt": {"nol": "В каком ряду стоит буква च ca?",
                "prodolzhayushchiy": "वर्ग какой: च ca открывает ряд…"},
     "options": ["заднеязычного", "палатального", "церебрального", "зубного"],
     "answer_index": 1},
    {"key": "04", "concept": ["daṇḍa"],
     "prompt": {"nol": "Что означает двойная палочка ॥?",
                "prodolzhayushchiy": "Двойной daṇḍa ॥ маркирует…"},
     "options": ["запятую", "конец раздела или стиха", "вопрос", "перенос звука"],
     "answer_index": 1},
    {"key": "05", "concept": ["j"],
     "prompt": {"nol": "Как произносится j?",
                "prodolzhayushchiy": "Рефлекс палатального j в чтении:"},
     "options": ["как русское й", "как русское ж", "как слитное дж", "как английское g"],
     "answer_index": 2},
    {"key": "06", "concept": ["ṭ", "ḍ"],
     "prompt": {"nol": "Чем церебральные ṭ, ḍ отличаются от зубных t, d?",
                "prodolzhayushchiy": "Артикуляционная база ретрофлексных ṭ/ḍ:"},
     "options": ["ничем, это разные записи одного звука",
                 "произносятся тише",
                 "кончик языка завёрнут назад и касается нёба",
                 "произносятся с придыханием всегда"], "answer_index": 2},
]

BASE_EXTRA_QUIZ = {"key": "07", "concept": ["devanāgarī"],
                   "prompt": {"nol": "Что передаёт один графический знак (графема) письма "
                                     "devanāgarī?",
                              "prodolzhayushchiy": "Единица, кодируемая одной графемой "
                                                   "devanāgarī:"},
                   "options": ["одну букву без гласного", "одно слово",
                               "один звук", "целый слог (согласная + гласный)"],
                   "answer_index": 3}

INTEREST_EXTRA_QUIZ = {
    "yoga": {"concept": ["gaṇa"],
             "prompt": {"nol": "Какое слово урока спрятано в имени Gaṇeśa?",
                        "prodolzhayushchiy": "Лексема урока, отражённая в теофорном имени "
                                             "Gaṇeśa:"},
             "options": ["patha", "gaja", "gaṇa", "dhana"], "answer_index": 2},
    "ayurveda": {"concept": ["dhana"],
                 "prompt": {"nol": "Какое слово урока значит «богатство» (здоровье — "
                                   "главное богатство аюрведы)?",
                            "prodolzhayushchiy": "«Богатство» по-санскритски (урок):"},
                 "options": ["bhaga", "dhana", "dama", "khana"], "answer_index": 1},
    "kino": {"concept": ["naṭaka"],
             "prompt": {"nol": "Какое слово урока значит «актёр»?",
                        "prodolzhayushchiy": "Лексема урока со значением «актёр, танцор»:"},
             "options": ["naṭaka", "kathaka", "janaka", "gaṇaka"], "answer_index": 0},
    "palomnichestvo": {"concept": ["patha"],
                       "prompt": {"nol": "Какое слово урока значит «путь»?",
                                  "prodolzhayushchiy": "«Путь» (урок; маршрут паломника):"},
                       "options": ["pada", "dama", "patha", "gata"], "answer_index": 2},
}

GLOWS_GROWS_MESSAGES = {
    "glow_top": "Отлично! Графика и звуковой состав занятия освоены — можно читать "
                "упражнение III без подсказок.",
    "grow_mid": "Хорошее начало: базу видите, но перепутаны детали рядов. Перечитайте "
                "таблицу пяти рядов и повторите попытку.",
    "grow_low": "Нормально для первого захода: вернитесь к разделу про varga и "
                "произнесение, прочитайте текст вслух — и снова сюда.",
}


# --------------------------------------------------------------------------- #
# Deterministic assembly
# --------------------------------------------------------------------------- #

def profile_tag(level: str, interest: str) -> str:
    return "base" if level == "base" else f"{level}-{interest}"


def quiz_bank(level: str, interest: str):
    reg = level if level in LEVELS else "nol"
    core = [dict(q, prompt=q["prompt"][reg]) for q in CORE_QUIZ]
    extra_src = BASE_EXTRA_QUIZ if interest == "base" else INTEREST_EXTRA_QUIZ[interest]
    extra = dict(extra_src, key="07", prompt=extra_src["prompt"][reg])
    items = []
    answer_keys = {}
    tag = profile_tag(level, interest)
    for q in core + [extra]:
        qid = f"zan1-{tag}-{q['key']}"
        items.append({
            "id": qid,
            "type": "mcq",
            "concept": q["concept"],
            "prompt": q["prompt"],
            "options": q["options"],
            "answer_index": q["answer_index"],
        })
        answer_keys[qid] = ANSWER_LETTERS[q["answer_index"]]
    top = len(items)
    glows_grows = {
        "scale": {"min_score": 0, "max_score": top},
        "bands": [
            {"min_score": max(0, top - 1), "max_score": top, "kind": "glow",
             "message": GLOWS_GROWS_MESSAGES["glow_top"]},
            {"min_score": int(top * 0.5), "max_score": top - 2, "kind": "grow",
             "message": GLOWS_GROWS_MESSAGES["grow_mid"]},
            {"min_score": 0, "max_score": int(top * 0.5) - 1, "kind": "grow",
             "message": GLOWS_GROWS_MESSAGES["grow_low"]},
        ],
    }
    return {"schema": QUIZ_SCHEMA, "items": items, "answer_keys": answer_keys,
            "glows_grows": glows_grows}


def embedded_map(quizzes):
    """Semantic placement: quiz id -> owning lesson section."""
    by_suffix = {}
    for it in quizzes["items"]:
        suffix = it["id"].rsplit("-", 1)[-1]
        by_suffix[suffix] = it["id"]
    extra = by_suffix["07"]
    extra_section = "devanagari-script" if extra.endswith("base-07") else "five-rows"
    return {
        "devanagari-script": [by_suffix["02"]] + ([extra] if extra_section ==
                                                  "devanagari-script" else []),
        "sparsa-varga": [by_suffix["01"]],
        "five-rows": [by_suffix["03"]] + ([extra] if extra_section == "five-rows"
                                          else []),
        "pronunciation": [by_suffix["05"], by_suffix["06"]],
        "writing-rules": [by_suffix["04"]],
    }


def weak_spots_block(fixture, level: str) -> str:
    highs = [l["lemma"] for l in fixture["lemmas"] if l["miss_rate_band"] == "high"][:3]
    words = ", ".join(f"**{w}**" for w in highs)
    if level == "nol":
        return ("### Ваши слабые слова (анонимная SRS-статистика группы)\n\n"
                f"Чаще всего ошибаются в словах: {words}. Пропишите каждое один раз "
                "знаками devanāgarī и прочитайте вслух.")
    return ("### SRS-агрегат группы (анонимный)\n\nРискованные лексемы этой недели: "
            f"{words}. Проверьте себя чтением упражнения III.")


def render_personalized_text(level, interest, fixture, quizzes, emb, ctx) -> str:
    reg = level if level in LEVELS else "nol"
    tag = profile_tag(level, interest)
    title = "Занятие I · Learn Your Way"
    banner = (f"*Уровень:* **{LEVEL_RU[level]}** · *Интерес:* **{INTEREST_RU[interest]}** · "
              f"*профиль:* `{tag}`")
    parts = [f"# {title}", "", banner, ""]
    for sec in SECTIONS:
        parts.append(f"## {sec['title']}")
        parts.append("")
        parts.append(SECTION_BODIES[sec["id"]][reg])
        parts.append("")
        if interest != "base":
            for swap in SWAPS.get(interest, []):
                if swap["after"] == sec["id"]:
                    parts.append(f"> 🎯 **Ваш интерес — {INTEREST_RU[interest]}.** "
                                 f"{swap['text']}")
                    parts.append("")
        for qid in emb.get(sec["id"], []):
            item = next(i for i in quizzes["items"] if i["id"] == qid)
            opts = " · ".join(f"{ANSWER_LETTERS[i]}) {o}"
                              for i, o in enumerate(item["options"]))
            parts.append(f"❓ **Вопрос ({qid})** — {item['prompt']}")
            parts.append(f"> {opts}")
            parts.append("(отметьте свой ответ — проверка и разбор на занятии)")
            parts.append("")
        if sec["id"] == "five-rows":
            parts.append(weak_spots_block(fixture, reg))
            parts.append("")
    parts.append("## Мнемоники")
    parts.append("")
    mnemos = MNEMONICS_SHARED + MNEMONICS_BY_LEVEL.get(level, [])
    for m in mnemos:
        parts.append(f"- **{m['for']}** — {m['sentence']}")
    parts.append("")
    parts.append("---")
    parts.append(
        f"Источник: Kochergina, Учебник санскрита (1998), {ctx.lesson_marker} "
        f"(mdx) · claims.yml sha256 {ctx.claims_sha[:12]}… · сгенерировано "
        f"scripts/build_lessonpack.py (Learn Your Way wave 1, {SESSION_TAG}, "
        f"{GENERATED_DATE})"
    )
    return "\n".join(parts) + "\n"


def render_mindmap(level, interest) -> str:
    root = f"Занятие I · {LEVEL_RU[level]} / {INTEREST_RU[interest]}"
    lines = [
        f"%% LYW wave-1 grammar hierarchy — zan1, профиль {profile_tag(level, interest)}",
        "flowchart TD",
        f'  Z["{root}"] --> P["Письмо devanāgarī"]',
        '  Z --> S["Звуковой состав: группа sparśa"]',
        '  Z --> W["Правила написания · знаки daṇḍa । ॥"]',
        '  P --> P1["графема = слог"]',
        '  P1 --> P2["согласная + присущий гласный a"]',
        '  S --> V["5 рядов (varga): голос × придыхание"]',
        '  V --> R1["заднеязычные: क ख ग घ ङ"]',
        '  V --> R2["палатальные: च छ ज झ ञ"]',
        '  V --> R3["церебральные: ट ठ ड ढ ण"]',
        '  V --> R4["зубные: त थ द ध न"]',
        '  V --> R5["губные: प फ ब भ म"]',
        '  W --> W1["одинарный daṇḍa । = точка"]',
        '  W --> W2["двойной daṇḍa ॥ = конец раздела"]',
    ]
    return "\n".join(lines) + "\n"


def build_pack_files(level, interest, fixture, ctx):
    quizzes = quiz_bank(level, interest)
    emb = embedded_map(quizzes)
    sections_manifest = []
    for sec in SECTIONS:
        sections_manifest.append({
            "id": sec["id"],
            "title": sec["title"],
            "source_concepts": list(sec["concepts"]),
            "embedded_questions": list(emb.get(sec["id"], [])),
        })
    mnemos = MNEMONICS_SHARED + MNEMONICS_BY_LEVEL.get(level, [])
    manifest = {
        "schema": SCHEMA,
        "zan": ctx.zan,
        "profile": {"level": level, "interest": interest},
        "source": {"claims_yml_sha256": ctx.claims_sha,
                   "lesson_marker": ctx.lesson_marker},
        "sections": sections_manifest,
        "views": {"mindmap": "views/mindmap.mmd"},
        "quizzes": "quizzes.json",
        "mnemonics": [dict(m) for m in mnemos],
        "generated": {"date": GENERATED_DATE, "session": SESSION_TAG},
    }
    files = {
        "manifest.json": json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        "personalized_text.md": render_personalized_text(
            level, interest, fixture, quizzes, emb, ctx),
        "views/mindmap.mmd": render_mindmap(level, interest),
        "quizzes.json": json.dumps(quizzes, ensure_ascii=False, indent=2) + "\n",
    }
    return files


def build_all(dest_root=None, zan: int = 1):
    """Assemble every pack. dest_root=None writes into the repo (LessonPacks/zanN)."""
    ctx = Context(zan)
    fixture = load_fixture(ctx)
    base = (dest_root or (PACKS_ROOT / f"zan{zan}"))
    written = {}
    for rel_dir, (level, interest) in iter_profiles():
        files = build_pack_files(level, interest, fixture, ctx)
        for rel_path, content in files.items():
            path = base / rel_dir / rel_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            written[f"{rel_dir}/{rel_path}"] = content
    return ctx, fixture, written


def iter_profiles():
    yield "base", ("base", "base")
    for lv in LEVELS:
        for it in INTERESTS:
            yield f"{lv}/{it}", (lv, it)


def expected_profile_dirs():
    return {rel for rel, _ in iter_profiles()}


# --------------------------------------------------------------------------- #
# Fixture
# --------------------------------------------------------------------------- #

def load_fixture(ctx=None):
    raw = FIXTURE_PATH.read_text(encoding="utf-8")
    data = json.loads(raw)
    errors = validate_fixture(data, raw, ctx)
    if errors:
        raise SystemExit("srs_aggregate.json invalid:\n  - " + "\n  - ".join(errors))
    return data


def validate_fixture(data, raw_text, ctx=None):
    errors = []
    note = str(data.get("_fixture_note", ""))
    flat = note.upper().replace("-", " ").replace("_", " ")
    if "SYNTHETIC" not in flat or "ANONYMIZED" not in flat:
        errors.append("_fixture_note must declare SYNTHETIC k-anonymized status")
    if data.get("zan") != 1:
        errors.append("fixture zan must be 1")
    k = data.get("k_anonymity_min_group")
    if not isinstance(k, int) or k < 2:
        errors.append("k_anonymity_min_group must be an integer >= 2")
    vocab = data.get("band_vocab") or []
    if sorted(vocab) != sorted(BANDS):
        errors.append(f"band_vocab must be {list(BANDS)}")
    lemmas = data.get("lemmas")
    if not isinstance(lemmas, list) or not lemmas:
        errors.append("lemmas must be a non-empty list")
    else:
        for l in lemmas:
            if set(l.keys()) != {"lemma", "miss_rate_band"}:
                errors.append(f"lemma entry has wrong keys: {l}")
            elif l["miss_rate_band"] not in BANDS:
                errors.append(f"bad band for {l['lemma']}: {l['miss_rate_band']}")
            elif ctx is not None and not ctx.knows(l["lemma"]):
                errors.append(f"fixture lemma not traceable to занятие-1 source: {l['lemma']}")
    low = raw_text.lower()
    for field in FIXTURE_FORBIDDEN_FIELDS:
        if f'"{field}"' in low:
            errors.append(f"fixture contains forbidden identifier-like field: {field}")
    return errors


# --------------------------------------------------------------------------- #
# Validators (--check / contract suite)
# --------------------------------------------------------------------------- #

MANIFEST_REQUIRED_KEYS = {"schema", "zan", "profile", "source", "sections",
                          "views", "quizzes", "mnemonics", "generated"}
SECTION_REQUIRED_KEYS = {"id", "title", "source_concepts", "embedded_questions"}

MERMAID_HEAD_RE = re.compile(r"^\s*(flowchart|graph|mindmap)\b")


def validate_mermaid(text: str):
    errors = []
    lines = text.splitlines()
    body = [ln for ln in lines if ln.strip() and not ln.strip().startswith("%%")]
    if not body or not MERMAID_HEAD_RE.match(body[0]):
        errors.append("mermaid: first non-comment line must open a flowchart/graph/mindmap")
    depth = 0
    for ln in body:
        if "\t" in ln:
            errors.append("mermaid: tab character in line")
        depth += ln.count('"') % 2
    if depth % 2 != 0:
        errors.append("mermaid: unbalanced double quotes")
    arrow_lines = sum(1 for ln in body if "-->" in ln)
    node_lines = sum(1 for ln in body if re.search(r'\w+\["', ln))
    if arrow_lines < 5 or node_lines < 5:
        errors.append("mermaid: too few nodes/arrows for a grammar hierarchy")
    return errors


def validate_quizzes(qdata, manifest, pack_dir: Path, ctx):
    errors = []
    if qdata.get("schema") != QUIZ_SCHEMA:
        errors.append(f"quizzes schema must be {QUIZ_SCHEMA}")
    items = qdata.get("items") or []
    keys = qdata.get("answer_keys") or {}
    if not (5 <= len(items) <= 10):
        errors.append(f"quiz item count {len(items)} outside 5..10")
    ids = set()
    for it in items:
        iid = it.get("id", "")
        ids.add(iid)
        if set(it.keys()) < {"id", "type", "concept", "prompt", "options", "answer_index"}:
            errors.append(f"quiz item missing fields: {iid}")
        opts = it.get("options") or []
        ai = it.get("answer_index")
        if not isinstance(ai, int) or not (0 <= ai < len(opts)):
            errors.append(f"quiz item bad answer_index: {iid}")
        elif keys.get(iid) != ANSWER_LETTERS[ai]:
            errors.append(f"answer key mismatch for {iid}: "
                          f"{keys.get(iid)!r} vs {ANSWER_LETTERS[ai]}")
        for c in it.get("concept") or []:
            if not ctx.knows(c):
                errors.append(f"fabricated concept in quiz {iid}: {c}")
    if ids != set(keys.keys()):
        errors.append("answer_keys must cover exactly the quiz item ids")
    gg = qdata.get("glows_grows") or {}
    bands = gg.get("bands") or []
    scale = gg.get("scale") or {}
    if scale.get("min_score") != 0 or scale.get("max_score") != len(items):
        errors.append("glows_grows scale must span 0..len(items)")
    covered = []
    kinds_ok = all(b.get("kind") in {"glow", "grow"} and str(b.get("message", "")).strip()
                   for b in bands)
    if not kinds_ok:
        errors.append("glows_grows band with bad kind or empty message")
    for b in bands:
        lo, hi = b.get("min_score"), b.get("max_score")
        if not isinstance(lo, int) or not isinstance(hi, int) or lo > hi:
            errors.append("glows_grows band with bad score range")
            continue
        covered.extend(range(lo, hi + 1))
    if covered:
        want_scores = list(range(0, int(scale.get("max_score", -1)) + 1))
        if sorted(set(covered)) != want_scores or len(covered) != len(set(covered)):
            errors.append("glows_grows bands must cover 0..max_score without overlap/gaps")
    if not any(b.get("kind") == "glow" for b in bands):
        errors.append("glows_grows needs at least one glow band")
    return errors


def validate_pack(pack_dir: Path, ctx, fixture) -> list:
    errors = []
    mpath = pack_dir / "manifest.json"
    if not mpath.exists():
        return [f"{pack_dir.name}: manifest.json missing"]
    try:
        m = json.loads(mpath.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{pack_dir.name}: manifest.json not valid JSON: {e}"]

    if m.get("schema") != SCHEMA:
        errors.append(f"schema must be {SCHEMA}")
    missing = MANIFEST_REQUIRED_KEYS - set(m.keys())
    if missing:
        errors.append(f"manifest missing keys: {sorted(missing)}")

    prof = m.get("profile") or {}
    lv, intr = prof.get("level"), prof.get("interest")
    if lv not in {"base"} | set(LEVELS):
        errors.append(f"bad profile.level: {lv}")
    if intr not in {"base"} | set(INTERESTS):
        errors.append(f"bad profile.interest: {intr}")
    if lv == "base":
        if intr != "base":
            errors.append("base pack must have interest=base")
    else:
        if intr == "base":
            errors.append("matrix pack must carry a real interest")

    src = m.get("source") or {}
    if src.get("claims_yml_sha256") != ctx.claims_sha:
        errors.append("manifest claims_yml_sha256 drifts from current claims.yml — "
                      "regenerate the packs")
    if src.get("lesson_marker") != ctx.lesson_marker:
        errors.append("manifest lesson_marker mismatch")

    if m.get("zan") != ctx.zan:
        errors.append("manifest zan mismatch")

    gen = m.get("generated") or {}
    if gen.get("date") != GENERATED_DATE or gen.get("session") != SESSION_TAG:
        errors.append("generated block must pin date+session for byte-stable rebuilds")

    sections = m.get("sections") or []
    if not sections:
        errors.append("sections empty")
    embedded_ids = []
    for s in sections:
        if SECTION_REQUIRED_KEYS - set(s.keys()):
            errors.append(f"section missing keys: {s.get('id')}")
            continue
        for c in s.get("source_concepts") or []:
            if not ctx.knows(c):
                errors.append(f"FABRICATED GRAMMAR concept {c!r} in section {s['id']}")
        embedded_ids.extend(s.get("embedded_questions") or [])

    views = m.get("views") or {}
    mm_rel = views.get("mindmap")
    if not mm_rel or not (pack_dir / mm_rel).exists():
        errors.append("views.mindmap file missing")
    else:
        errors.extend(validate_mermaid((pack_dir / mm_rel).read_text(encoding="utf-8")))

    q_rel = m.get("quizzes")
    if not q_rel or not (pack_dir / q_rel).exists():
        errors.append("quizzes.json missing")
    else:
        try:
            qdata = json.loads((pack_dir / q_rel).read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"quizzes.json not valid JSON: {e}")
            qdata = None
        if qdata is not None:
            errors.extend(validate_quizzes(qdata, m, pack_dir, ctx))

    mnemos = m.get("mnemonics") or []
    if not (2 <= len(mnemos) <= 4):
        errors.append("mnemonics count outside 2..4")
    for mn in mnemos:
        if set(mn.keys()) < {"for", "sentence"}:
            errors.append("mnemonic missing for/sentence")
        elif not ctx.knows(mn["for"]):
            errors.append(f"mnemonic tied to fabricated concept: {mn['for']}")

    text_path = pack_dir / "personalized_text.md"
    if not text_path.exists():
        errors.append("personalized_text.md missing")
    else:
        text = text_path.read_text(encoding="utf-8")
        declared = set(embedded_ids)
        unanchored = [qid for qid in sorted(declared) if qid not in text]
        if unanchored:
            errors.append(f"embedded_questions never anchored in text: {unanchored}")
        if interest_needs_swaps(lv, intr) and "🎯" not in text:
            errors.append("interest pack text lacks highlighted swap blocks")
        if f"{ctx.lesson_marker}" not in text:
            errors.append("personalized text lost the source lesson marker")

    return errors


def interest_needs_swaps(level, interest):
    return interest != "base"


def validate_matrix(packs_root: Path):
    errors = []
    actual = set()
    if packs_root.exists():
        for p in packs_root.iterdir():
            if not p.is_dir():
                continue
            if p.name in LEVELS:
                for sub in sorted(x.name for x in p.iterdir() if x.is_dir()):
                    actual.add(f"{p.name}/{sub}")
            elif (p / "manifest.json").exists():
                actual.add(p.name)
            else:
                errors.append(f"stray directory without manifest: {p.name}")
    want = expected_profile_dirs()
    if actual != want:
        errors.append(f"matrix mismatch: missing={sorted(want - actual)} "
                      f"unexpected={sorted(actual - want)}")
    return errors


def check_everything(zan: int):
    problems = []
    try:
        ctx = Context(zan)
    except SystemExit as e:
        return [str(e)]
    fixture_raw = None
    if not FIXTURE_PATH.exists():
        problems.append(f"fixture missing: {FIXTURE_PATH}")
    else:
        fixture_raw = FIXTURE_PATH.read_text(encoding="utf-8")
        try:
            fixture = json.loads(fixture_raw)
        except json.JSONDecodeError as e:
            problems.append(f"fixture JSON broken: {e}")
            fixture = None
        if fixture is not None:
            problems.extend(validate_fixture(fixture, fixture_raw, ctx))

    packs_root = PACKS_ROOT / f"zan{zan}"
    problems.extend(validate_matrix(packs_root))
    fixture = json.loads(fixture_raw) if fixture_raw else {}
    for rel, (_lv, _intr) in iter_profiles():
        pd = packs_root / rel
        if (pd / "manifest.json").exists():
            problems.extend(f"{rel}: {p}" for p in validate_pack(pd, ctx, fixture))
    return problems


# --------------------------------------------------------------------------- #
# Checklist emitter (documents the agent transformation pass)
# --------------------------------------------------------------------------- #

CHECKLIST = """
LEARN YOUR WAY — transformation checklist (занятие {zan})
==========================================================
For each profile (base + {levels} x {interests}):

1. RE-LEVEL  — rewrite each section for the level register:
   nol    -> short paragraphs, every term glossed, reassurance steps;
   prodolzhayushchiy -> denser academic register, comparative notes.
2. SWAP      — insert >=2 interest-swap blockquotes (marker "> 🎯") framed on
   LESSON vocabulary only; grammar concepts stay source-native.
3. EMBED     — anchor each quiz id once as "[[q:<id>]]"/inline question line;
   list ids under the owning section in manifest.embedded_questions.
4. QUIZ      — 5..10 MCQs, 4 options, answer_index + answer_keys letter agree;
   add glows_grows bands covering 0..len(items) contiguously, top band glow.
5. MNEMONIC  — 2..4 mnemonics, each tied to an inventory concept ("for").
6. MINDMAP   — flowchart of the lesson hierarchy, quoted labels, no tabs.
7. WEAK SPOTS— pull top high-band lemmas from srs_aggregate.json into the text.

Every emitted artifact must survive: python scripts/build_lessonpack.py --check
(no fabricated concepts; sha256(claims.yml) pinned in manifests).
"""


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LYW lessonpack builder/validator")
    ap.add_argument("--zan", type=int, default=1, help="занятие number (wave 1: only 1)")
    ap.add_argument("--check", action="store_true", help="validate-only, exit code form")
    ap.add_argument("--build", action="store_true", help="(re)generate packs deterministically")
    ap.add_argument("--emit-checklist", action="store_true",
                    help="print the agent-pass transformation checklist")
    args = ap.parse_args(argv)

    if args.emit_checklist:
        print(CHECKLIST.format(levels="+".join(LEVELS),
                               interests="+".join(INTERESTS), zan=args.zan))
        return 0

    if args.build:
        ctx, _fixture, written = build_all(None, args.zan)
        print(f"built {len(written)} files under {PACKS_ROOT / f'zan{args.zan}'} "
              f"(claims sha {ctx.claims_sha[:12]}…)")
        problems = check_everything(args.zan)
        if problems:
            print("POST-BUILD CHECK FAILED:", file=sys.stderr)
            for p in problems:
                print(f"  - {p}", file=sys.stderr)
            return 1
        print("post-build check OK")
        return 0

    problems = check_everything(args.zan)
    if problems:
        print(f"--check FAILED ({len(problems)} problem(s)):", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    n_dirs = len(expected_profile_dirs())
    print(f"--check OK: zan{args.zan} matrix {n_dirs}/9 profiles schema-valid, "
          f"fixture k-anon shape ok, no fabricated concepts, mermaid sane")
    return 0


if __name__ == "__main__":
    sys.exit(main())
