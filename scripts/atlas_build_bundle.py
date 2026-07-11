#!/usr/bin/env python3
"""Build the sanitised public Sangram atlas bundle (slot B1, H623).

Reads the private Uprava registries (MEGABOOK.md sections 6/9/11.2 and
interlinks_edges.tsv) plus curated structural constants, applies the
sanitisation denylist, and emits sangram/atlas/data/atlas.bundle.json.

Temperature split (see sangram/atlas/SANGRAM_ATLAS_DATA_CONTRACT.mdx):
  structural — stable explanatory structure, curated constants below with
               section references (source ontology, asset families, views);
  assessed   — dated author/registry assessments parsed live at build time
               (thesis scores/verdicts/gates, repo-edge statuses);
  volatile   — queues, claims, PR states, counters: NEVER emitted.

Usage:
  python scripts/atlas_build_bundle.py \
      [--uprava ../Uprava] [--out sangram/atlas/data/atlas.bundle.json] \
      [--generated-by "Fable 5 (claude-fable-5)"] [--date YYYY-MM-DD]

The private sources are named (label only) in bundle provenance; no private
URL, path, or registry content ever enters the bundle. Validate the output
with scripts/atlas_validate_bundle.py before committing.
"""

import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

CONTRACT_VERSION = "1.0.0"
DENYLIST_VERSION = "2026-07-11"

# ---------------------------------------------------------------------------
# Sanitisation: repos that never enter the public bundle.
# private  = GitHub-private repos (visibility checked 11-07-2026);
# local    = local-only working dirs with no public remote;
# unresolved = names in source registries with no resolvable public repo.
PRIVATE_REPOS = {"Uprava", "github-spine", "RuWritingStyles-corpus", "telegram-sanskrit-corpus"}
LOCAL_ONLY_REPOS = {"Sundara-commentaries", "prefaces_ieg", "samskrutam-crossword"}
UNRESOLVED_REPOS = {"YAT"}
DROP_REPOS = PRIVATE_REPOS | LOCAL_ONLY_REPOS | UNRESOLVED_REPOS

# Substrings that must never appear anywhere in the serialized bundle.
LEAKAGE_PATTERNS = [
    "github.com/gasyoun/Uprava",
    "github.com/gasyoun/github-spine",
    "RuWritingStyles-corpus",
    "telegram-sanskrit-corpus",
    "C:/Users",
    "C:\\Users",
    "GTD_NEXT_ACTIONS",
    "BOTTLENECKS.md",
    "NEXT_TASK_QUEUE",
    "@DECIDE",
    "@WAITING",
    "\U0001f512",  # 🔒 private-tier marker: private-tier rows must be dropped, not marked
]

# GitHub org per repo name for every public repo the source registries name.
SANSKRIT_LEXICON = {
    "ACC", "AMAR", "AP", "AP90", "ApteES", "BHS", "BOP", "BOR", "BUR", "CAE",
    "CCS", "DCS", "FRI", "GRA", "INM", "KNA", "KOW", "KRM", "LRV", "MCI", "MD",
    "MW72", "MWS", "PUI", "PWG", "PWK", "SCH", "SHS", "SKD", "STC", "VCP",
    "VEI", "Wil", "COLOGNE", "CORRECTIONS", "MWinflect", "cologne-skills",
    "csl-apidev", "csl-app", "csl-atlas", "csl-corrections", "csl-devanagari",
    "csl-doc", "csl-guides", "csl-inflect", "csl-newsletter", "csl-observatory",
    "csl-orig", "csl-pywork", "csl-santam", "csl-standards", "csl-websanlexicon",
    "sanskrit-lexicon.github.io", "sanskrit-util",
}
ORG_OVERRIDES = {
    "SanskritSpellCheck": "drdhaval2785",
    "buhler-sanskrit-book": "alexander-myltsev",
}
GASYOUN = {
    "AfanasiyNikitin", "BookIndex", "CommentaryStrategies", "IndologyScholars",
    "ORS-FAQ", "Retrieval-based-Voice-Conversion-WebUI", "RussianRamayana",
    "RuWritingStyles", "SamudraManthanam", "SanskritGrammar", "SanskritKaraoke",
    "SanskritLexicography", "SanskritRussian", "SOCKS5-VPS",
    "Systema-Sanscriticum", "VisualDCS", "WhitneyRoots", "ZettelkastenWiki",
    "kosha",
}


def repo_org(name):
    if name in ORG_OVERRIDES:
        return ORG_OVERRIDES[name]
    if name in SANSKRIT_LEXICON:
        return "sanskrit-lexicon"
    if name in GASYOUN:
        return "gasyoun"
    return None


def slug(name):
    s = name.lower().replace("_", "-")
    s = re.sub(r"[^a-z0-9.-]+", "-", s).strip("-")
    return s


def internal_evidence(label_ru):
    return {"label_ru": label_ru, "visibility": "internal"}


def public_evidence(label_ru, url):
    return {"label_ru": label_ru, "url": url, "visibility": "public"}


# ---------------------------------------------------------------------------
# Structural constants — the closed source ontology (MEGABOOK §1.4, decision of
# 11-07-2026, H617), the value chain (§1.2) and the provenance chain (§8).
# These are stable explanatory structure; re-deriving them by parsing Russian
# prose would add fragility, not fidelity. Section refs are the provenance.

SOURCE_CLASSES = [
    ("class:dictionaries", "Словари: CDSL (csl-orig + словарные репозитории)", "top", ["2.1"], None),
    ("class:corpora", "Корпуса: ядро DCS + дополнительные свидетели", "top", ["2.4"], None),
    ("class:grammars", "Грамматики", "top", ["2.7"], None),
    ("class:grammars-traditional", "Традиционные трактаты (Pāṇini, dhātupāṭha, комментаторская традиция)", "top", ["2.7"], "class:grammars"),
    ("class:grammars-modern", "Современные учебные грамматики — главный акцент (Sangram)", "top", ["2.7"], "class:grammars"),
    ("class:grammars-machine", "Машиночитаемые правила и парадигмы", "top", ["2.7"], "class:grammars"),
    ("class:commentaries", "Комментарии (питающий слой)", "feeding", ["2.8"], None),
    ("class:translations", "Переводы (питающий слой)", "feeding", ["2.5", "3.4"], None),
    ("class:scans", "Сканы, издания и архивы (питающий слой)", "feeding", ["3.3", "3.4"], None),
]

VALUE_STAGES = [
    ("stage:sources", "Источники: словари, корпуса, грамматики", "value"),
    ("stage:verified-data", "Проверенные данные и методы", "value"),
    ("stage:research-pubs", "Исследования и публикации", "value"),
    ("stage:edu-products", "Образовательные продукты", "value"),
    ("stage:authority", "Научный авторитет и партнерства", "value"),
    ("stage:revenue", "Выручка и аудитория", "value"),
    ("stage:agents", "Агенты, навыки и организационная память", "value"),
]

PROVENANCE_STAGES = [
    ("stage:derived-dict", "Производные словарные данные: XML, headwords, roots", "provenance"),
    ("stage:derived-corpus", "Производные корпусные данные: SQLite, frequency, concordance", "provenance"),
    ("stage:derived-grammar", "Производные грамматические данные: правила, парадигмы, root crosswalks", "provenance"),
    ("stage:crosswalks", "Crosswalks и typed links", "provenance"),
    ("stage:assembly", "kosha / API / учебные карточки", "provenance"),
    ("stage:research", "Исследования и статьи", "provenance"),
    ("stage:learning-surfaces", "LMS, FAQ, free funnel", "provenance"),
    ("stage:citable-releases", "Цитируемые releases и DH-интерфейсы", "provenance"),
]

ONTOLOGY_EDGES = [
    # (source, target, kind) — closed relation set of MEGABOOK §1.4 applied in §8.
    ("class:commentaries", "class:corpora", "replenishes"),
    ("class:translations", "class:corpora", "replenishes"),
    ("class:scans", "class:dictionaries", "replenishes"),
    ("class:scans", "class:corpora", "replenishes"),
    ("class:scans", "class:grammars", "replenishes"),
    ("class:dictionaries", "stage:derived-dict", "generates"),
    ("class:corpora", "stage:derived-corpus", "generates"),
    ("class:grammars", "stage:derived-grammar", "generates"),
    ("class:corpora", "class:dictionaries", "attests"),
    ("class:corpora", "class:grammars", "attests"),
    ("stage:derived-dict", "stage:crosswalks", "crosslinks"),
    ("stage:derived-corpus", "stage:crosswalks", "crosslinks"),
    ("stage:derived-grammar", "stage:crosswalks", "crosslinks"),
    ("stage:crosswalks", "stage:assembly", "fills"),
    ("stage:crosswalks", "stage:research", "fills"),
    ("stage:assembly", "stage:learning-surfaces", "fills"),
    ("stage:research", "stage:citable-releases", "fills"),
]

VALUE_EDGES = [
    ("stage:sources", "stage:verified-data", "generates"),
    ("stage:verified-data", "stage:research-pubs", "fills"),
    ("stage:verified-data", "stage:edu-products", "fills"),
    ("stage:research-pubs", "stage:authority", "creates"),
    ("stage:edu-products", "stage:revenue", "creates"),
    ("stage:authority", "stage:verified-data", "strengthens"),
    ("stage:revenue", "stage:verified-data", "funds"),
    ("stage:agents", "stage:verified-data", "scales"),
    ("stage:agents", "stage:research-pubs", "scales"),
    ("stage:agents", "stage:edu-products", "scales"),
]

SURFACES = [
    ("surface:edu-funnel", "Учебные и funnel-поверхности"),
    ("surface:org-wide", "Все репозитории организации"),
]

# Asset families — MEGABOOK §12.2 (slot A3, H619), public slice only.
# 🔒 private-tier assets (Uprava hubs, RuWritingStyles-corpus, raw Telegram,
# corpus_lexicon bytes, kosha guhya) are intentionally ABSENT, per §12.3.
# Fields: id, label_ru, asset_types, owner repo, url, rights, prohibition_ru,
# rule_refs, consumers (repo names / surface ids).
ASSET_FAMILIES = [
    ("asset:transliteration", "Транскодирование IAST⇄SLP1⇄Devanāgarī + ключи нормализации",
     ["code"], "sanskrit-util", "https://github.com/sanskrit-lexicon/sanskrit-util",
     "quarantine", "Не перепечатывать SLP1-таблицу и не пере-выводить ловушки нормализации; iast_to_devanagari — только композиция to_slp1 → slp1_to_devanagari.",
     ["7.10"], ["csl-apidev", "csl-guides", "csl-atlas", "WhitneyRoots", "SanskritSpellCheck"]),
    ("asset:correction-pipeline", "Коррекционный конвейер словарей (updateByLine, make_xml, generate_dict.sh)",
     ["code", "workflow"], "csl-pywork", "https://github.com/sanskrit-lexicon/csl-pywork",
     "rights-gated", "Не форкать-и-править; исправление = change-файл + месячный пакетный PR; прямые пуши агентов в csl-orig запрещены.",
     ["7.7", "7.8"], ["csl-corrections", "csl-orig"]),
    ("asset:php-endpoints", "PHP dict-web endpoints (getword/servepdf/serveimg)",
     ["code"], "csl-websanlexicon", "https://github.com/sanskrit-lexicon/csl-websanlexicon",
     "open", "Чинить шаблон и регенерировать, не править пословарные копии; XSS/SQLi-hardening принадлежит шаблону.",
     ["7.11"], ["csl-apidev"]),
    ("asset:entry-render", "Python-рендер статей Cologne",
     ["code"], "kosha", "https://github.com/gasyoun/kosha/blob/main/app/render.py",
     "open", "Не ре-портировать PHP display-движок.",
     ["7.12"], ["kosha"]),
    ("asset:site-generator", "Генератор note/FAQ/wiki-сайтов",
     ["code"], "ZettelkastenWiki", "https://github.com/gasyoun/ZettelkastenWiki",
     "open", "Не писать генератор №5; csl-guides остается Docusaurus (lane split).",
     [], ["ORS-FAQ", "surface:edu-funnel"]),
    ("asset:translation-kit", "RU-переводческий кит (PWG→RU/EN, MW→RU) — один параметризуемый кит",
     ["code", "workflow"], "SanskritLexicography", "https://github.com/gasyoun/SanskritLexicography/tree/master/RussianTranslation",
     "rights-gated", "Не клонировать третий кит; дорогие окна только после preflight; TM/TMX-экспорт не публикуется.",
     ["7.22", "7.23"], ["SanskritRussian", "SanskritKaraoke"]),
    ("asset:cdsl-source-texts", "Тексты словарей CDSL (source spine, v02/<dict>/<dict>.txt)",
     ["data"], "csl-orig", "https://github.com/sanskrit-lexicon/csl-orig",
     "open", "Не редактировать напрямую; не строить второй коррекционный конвейер.",
     ["7.6", "7.7", "7.8"], ["csl-pywork", "csl-atlas", "kosha", "SanskritSpellCheck", "csl-websanlexicon", "csl-apidev", "csl-app"]),
    ("asset:dcs-corpus", "DCS-корпус: SQLite + lemma frequency (канонический ingest)",
     ["data"], "VisualDCS", "https://github.com/gasyoun/VisualDCS",
     "quarantine", "Не ре-парсить CoNLL-U (пять ingest-путей сведены к одному); частотности потреблять, не пересчитывать; UD Tense=Past смешивает аорист/перфект — слой-кандидат.",
     ["7.13", "7.14"], ["kosha", "WhitneyRoots", "MWS", "csl-apidev", "csl-atlas", "SanskritGrammar", "CommentaryStrategies", "SanskritKaraoke", "SanskritLexicography"]),
    ("asset:mw-roots", "Инвентарь MW-корней (mw_roots.tsv, count-locked)",
     ["data"], "csl-orig", "https://github.com/sanskrit-lexicon/csl-orig/blob/main/v02/mw/mw_roots.tsv",
     "open", "Никогда не ре-сканировать mw.txt под инвентарь корней; не путать с mw_etymology.tsv (деривация, не инвентарь).",
     ["7.16"], ["WhitneyRoots", "MWS"]),
    ("asset:union-headwords", "Union headwords (per-dict provenance)",
     ["data"], "SanskritLexicography", "https://github.com/gasyoun/SanskritLexicography/blob/master/HeadwordLists/union/union_headwords.tsv",
     "open", "Не пересобирать headword master.",
     ["7.15"], ["SanskritSpellCheck", "kosha"]),
    ("asset:mw-heritage-crosswalk", "MW↔Heritage crosswalk",
     ["data"], "SanskritLexicography", "https://github.com/gasyoun/SanskritLexicography/blob/master/HeadwordLists/mw_heritage_crosswalk.tsv",
     "rights-gated", "Не ре-хитить сайты INRIA; источник — GitHub-mirror darkone23 (LGPLLR).",
     ["7.17"], ["csl-guides"]),
    ("asset:dcs-cdsl-crosswalk", "DCS↔CDSL crosswalk",
     ["data"], "csl-apidev", "https://github.com/sanskrit-lexicon/csl-apidev/blob/main/simple-search/dcs_xref/dcs_cdsl_xref.tsv",
     "open", "Не пере-выводить joins DCS↔CDSL.",
     ["7.18"], ["csl-apidev"]),
    ("asset:sa-ru-alignment", "Sa→Ru выравнивание + TM/TMX (builders публичны, данные — нет)",
     ["data"], "SanskritLexicography", "https://github.com/gasyoun/SanskritLexicography/blob/master/RussianTranslation/src/build_corpus_lexicon.py",
     "rights-gated", "Не пере-выравнивать и не пере-переводить; не писать второй TMX-эмиттер или грейдер; JSONL/TMX не публикуются.",
     [], ["SanskritRussian", "SanskritKaraoke"]),
    ("asset:data-hub", "Data-hub: манифест datasets.json + data-v* релизы",
     ["data", "schema"], "kosha", "https://github.com/gasyoun/kosha/blob/main/data/manifest/datasets.json",
     "rights-gated", "Не встраивать копию dataset без строки манифеста; публичный tier отделен от закрытого; перед релизом — publish-safety.",
     ["7.21", "7.26"], ["csl-guides", "surface:org-wide"]),
    ("asset:typed-link-grammar", "Type-D link-ID grammar (устойчивые типизированные ссылки)",
     ["schema"], "SanskritGrammar", "https://github.com/gasyoun/SanskritGrammar/blob/main/TYPED_LINK_ID_GRAMMAR.md",
     "open", "Не минтить per-pilot ID; схема расширяет concordance_core, а не форкает его.",
     ["7.20"], ["CommentaryStrategies"]),
    ("asset:concordance-core", "Конкорданс словарь↔корпус (ядро matcher + stable locus ID)",
     ["schema", "code"], "kosha", "https://github.com/gasyoun/kosha/blob/main/scripts/concordance_core.py",
     "quarantine", "Не писать второй matcher; stable locus ID не зависит от web-хоста; relaxed/fuzzy match — кандидат до проверки.",
     ["7.19", "7.20"], ["kosha", "CommentaryStrategies"]),
    ("asset:ci-fanout", "CI и репо-гигиена fan-out (config-driven batch deploy)",
     ["workflow"], "COLOGNE", "https://github.com/sanskrit-lexicon/COLOGNE",
     "open", "Не писать CI руками per repo; PHP-репо анализирует Semgrep (в CodeQL нет PHP).",
     [], ["surface:org-wide"]),
    ("asset:docx-mdx-pipeline", "Word/PDF → MDX книжный конвейер (docx-to-md + rstTable)",
     ["workflow", "code"], "buhler-sanskrit-book", "https://github.com/alexander-myltsev/buhler-sanskrit-book",
     "open", "Не писать еще один Pandoc→MDX конвертер или grid-table рендерер; копии rstTable синхронизируются байт-в-байт.",
     [], ["buhler-sanskrit-book", "csl-guides", "SanskritGrammar"]),
]

# External stacks — MEGABOOK §12.3, public slice.
EXTERNAL_STACKS = [
    ("ext:samsaadhanii", "Samsaadhanii / SCL", "https://sanskrit.uohyd.ac.in/scl/", "GPL",
     "Живые JSON-API; кросс-валидация собственных данных.", "Не клонировать исходники (GPL)."),
    ("ext:heritage", "Heritage (INRIA)", "https://github.com/darkone23/Heritage_Resources", "LGPLLR",
     "Потреблять через GitHub-mirror darkone23.", "Не скрейпить sanskrit.inria.fr / gitlab.inria.fr (бот-стена)."),
    ("ext:dharmamitra", "DharmaMitra", "https://dharmamitra.org/", None,
     "GPU-морфология как поставщик; их MT-таксономия ошибок уже вшита в judges.", "Не изобретать собственную MT-таксономию."),
    ("ext:vedaweb", "VedaWeb", "https://vedaweb.uni-koeln.de/rigveda/", "CC BY 4.0",
     "Один bulk-export на всех потребителей.", "Не хитить API из каждого потребителя отдельно."),
    ("ext:gretil", "GRETIL (corpustei)", "https://gretil.sub.uni-goettingen.de/", "CC BY-NC-SA",
     "Локальный ingest для meter-QA и typo-проверок.", "Не включать в публичные релизы и bundles (NC)."),
    ("ext:vidyut", "vidyut (Ambuda)", "https://github.com/ambuda-org/vidyut", None,
     "Вендорить как движок флексии/лемматизации.", "Не писать собственную флексию."),
    ("ext:nagari", "Nagari (JS-транскодер)", "https://github.com/virtualvinodh/aksharamukha", None,
     "Вендоренная копия там, где уже вшита.", "Не добавлять новые вендоренные копии без строки в реестре."),
    ("ext:samskrtam-ru", "samskrtam.ru", "https://samskrtam.ru/", None,
     "Статические deep links (например, корневой указатель /z/).", "Не дублировать контент сайта в репозиториях."),
]

# tsv `ext:` name → node id above.
EXT_NAME_MAP = {
    "Heritage": "ext:heritage",
    "DharmaMitra": "ext:dharmamitra",
    "VedaWeb": "ext:vedaweb",
    "GRETIL": "ext:gretil",
    "vidyut": "ext:vidyut",
    "Samsaadhanii": "ext:samsaadhanii",
    "Nagari": "ext:nagari",
    "samskrtam.ru": "ext:samskrtam-ru",
}

VERDICT_MAP = {"усилить": "amplify", "поддерживать": "sustain"}
IMPORTANCE_MAP = {"\U0001f534": "key", "\U0001f7e0": "mid", "\U0001f7e1": "aux"}
STATE_MAP = {"\U0001f534": "blocked", "\U0001f7e1": "partial", "\U0001f535": "stable"}


def build_views(as_of):
    def seed(label, section, slot):
        d = {"source_label_ru": label, "series_slot": slot, "visibility": "internal"}
        if section:
            d["megabook_section"] = section
        return d

    return [
        {
            "id": "attention",
            "title_ru": "Распределение внимания и приоритетов",
            "question_ru": "Куда направлять следующую единицу внимания — человеческого и агентного — и какой тип ворот ее запирает?",
            "node_kinds": ["thesis", "repo"],
            "edge_kinds": ["anchors"],
            "seed": seed("Карта внимания MEGABOOK §11 (внутренний Uprava)", "§11", "A2"),
            "route": {"slug": "/sangram/atlas/attention", "owner_slot": "B2"},
        },
        {
            "id": "reuse",
            "title_ru": "Переиспользование готовых активов",
            "question_ru": "У кого уже есть нужный актив, кто его потребляет и что запрещено пересоздавать?",
            "node_kinds": ["repo", "asset", "external-stack", "surface"],
            "edge_kinds": ["owns", "feeds", "consumes", "vendors", "produces", "cites"],
            "seed": seed("Карта переиспользования MEGABOOK §12 (внутренний Uprava)", "§12", "A3"),
            "route": {"slug": "/sangram/atlas/reuse", "owner_slot": "B3"},
        },
        {
            "id": "value-chain",
            "title_ru": "Движение от исследования к продуктам",
            "question_ru": "Как источники превращаются в проверенные данные, публикации, продукты и выручку — и что возвращается обратно?",
            "node_kinds": ["stage"],
            "edge_kinds": ["generates", "fills", "creates", "strengthens", "funds", "scales"],
            "seed": seed("Цепочка ценности MEGABOOK §1.2; карта research→product (слот A4)", "§1.2", "A4"),
            "route": {"slug": "/sangram/atlas/value-chain", "owner_slot": "B4"},
        },
        {
            "id": "dependencies",
            "title_ru": "Зависимости репозиториев",
            "question_ru": "Какие репозитории питают, потребляют, вендорят и цитируют друг друга?",
            "node_kinds": ["repo", "external-stack", "surface"],
            "edge_kinds": ["feeds", "consumes", "vendors", "produces", "cites"],
            "seed": seed("Типизированный список ребер interlinks_edges.tsv (внутренний Uprava)", None, "A1"),
            "route": {"slug": "/sangram/atlas/dependencies", "owner_slot": "B5"},
        },
        {
            "id": "provenance",
            "title_ru": "Происхождение данных",
            "question_ru": "Из каких классов источников рождается каждый производный слой и по каким типизированным отношениям он движется к продуктам?",
            "node_kinds": ["source-class", "stage"],
            "edge_kinds": ["replenishes", "generates", "attests", "crosslinks", "fills"],
            "seed": seed("Онтология источников §1.4 и карта происхождения §8 (внутренний Uprava)", "§8", "A1"),
            "route": {"slug": "/sangram/atlas/provenance", "owner_slot": "B6"},
        },
    ]


# ---------------------------------------------------------------------------
# Parsers for the assessed layer.

def md_table_rows(lines, start_idx):
    """Yield split cell lists for a markdown table starting at its header row."""
    rows = []
    i = start_idx
    while i < len(lines) and lines[i].lstrip().startswith("|"):
        cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        rows.append(cells)
        i += 1
    return rows[2:]  # skip header + separator


def find_section(lines, heading_prefix):
    for i, line in enumerate(lines):
        if line.startswith(heading_prefix):
            return i
    raise SystemExit(f"section not found: {heading_prefix}")


def next_table(lines, from_idx):
    i = from_idx
    while i < len(lines) and not lines[i].lstrip().startswith("|"):
        i += 1
    return i


def parse_theses(lines, as_of):
    """MEGABOOK §6 matrix + §11.2 gates -> thesis nodes."""
    idx = next_table(lines, find_section(lines, "## §6."))
    theses = {}
    for cells in md_table_rows(lines, idx):
        if len(cells) < 9:
            continue
        section, name, imp, state, e, z, p, k, verdict = cells[:9]
        verdict_slug = "pause" if verdict.startswith("пауза") else VERDICT_MAP.get(verdict)
        if verdict_slug is None:
            raise SystemExit(f"unknown verdict in §6: {verdict!r}")
        theses[section] = {
            "id": f"thesis:{section}",
            "kind": "thesis",
            "label_ru": name,
            "section": section,
            "importance": IMPORTANCE_MAP[imp],
            "state": STATE_MAP[state],
            "scores": {"e": int(e), "z": int(z), "p": int(p),
                       "k": float(k.replace(",", "."))},
            "verdict": verdict_slug,
            "gates": [],
            "temperature": "assessed",
            "as_of": as_of,
            "evidence": internal_evidence("MEGABOOK §6 — оценка автора (внутренний Uprava)"),
        }

    idx = next_table(lines, find_section(lines, "### §11.2."))
    for cells in md_table_rows(lines, idx):
        if len(cells) < 6 or cells[0] not in theses:
            continue
        gate_text = cells[4]
        gates = []
        if "\U0001f464" in gate_text:
            gates.append({"type": "human"})
        if "\U0001f310" in gate_text:
            gates.append({"type": "external"})
        theses[cells[0]]["gates"] = gates
        summary = gate_text.replace("\U0001f464", "").replace("\U0001f310", "").strip(" —·")
        if summary and gates:
            theses[cells[0]]["gates_summary_ru"] = summary.strip()
    return theses


def parse_anchors(lines):
    """MEGABOOK §9.1–§9.6 tables -> (thesis_section, repo_name) pairs."""
    pairs = []
    start = find_section(lines, "## §9.")
    end = find_section(lines, "## §10.")
    i = start
    while i < end:
        if lines[i].lstrip().startswith("| Основной тезис"):
            for cells in md_table_rows(lines, i):
                if len(cells) < 2:
                    continue
                sections = [s.strip().lstrip("§") for s in cells[0].split("/")]
                repos = [r.strip() for r in cells[1].split(",")]
                for sec in sections:
                    for repo in repos:
                        # "Wil-YAT" is the WIL…YAT dictionary pair in one cell.
                        names = ["Wil", "YAT"] if repo == "Wil-YAT" else [repo]
                        for n in names:
                            pairs.append((sec, n))
        i += 1
    return pairs


def parse_tsv(path):
    edges = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#") or line.startswith("source\t"):
            continue
        parts = line.split("\t")
        if len(parts) < 6:
            raise SystemExit(f"malformed tsv row: {line!r}")
        edges.append(dict(zip(["source", "target", "asset", "kind", "status", "evidence"], parts)))
    return edges


def git_short_sha(repo_dir, rel_path):
    try:
        out = subprocess.run(
            ["git", "-C", str(repo_dir), "log", "-1", "--format=%h", "--", rel_path],
            capture_output=True, encoding="utf-8", check=True)
        return out.stdout.strip() or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--uprava", default="../Uprava")
    ap.add_argument("--out", default="sangram/atlas/data/atlas.bundle.json")
    ap.add_argument("--generated-by", default="manual run")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    args = ap.parse_args()

    uprava = Path(args.uprava)
    megabook = uprava / "MEGABOOK.md"
    tsv = uprava / "interlinks_edges.tsv"
    lines = megabook.read_text(encoding="utf-8").splitlines()
    as_of = args.date

    nodes = {}
    edges = []
    dropped_nodes = set()
    dropped_edges = 0

    def add_node(node):
        nodes[node["id"]] = node

    def ensure_repo(name):
        """Return node id for a repo name, or None if sanitised away."""
        if name in DROP_REPOS:
            dropped_nodes.add(name)
            return None
        org = repo_org(name)
        if org is None:
            dropped_nodes.add(name)
            return None
        nid = f"repo:{slug(name)}"
        if nid not in nodes:
            add_node({
                "id": nid, "kind": "repo", "label_ru": name,
                "org": org, "name": name,
                "url": f"https://github.com/{org}/{name}",
                "temperature": "structural",
            })
        return nid

    # Structural: source classes, stages, surfaces, externals, ontology edges.
    for nid, label, tier, refs, parent in SOURCE_CLASSES:
        node = {"id": nid, "kind": "source-class", "label_ru": label,
                "tier": tier, "thesis_refs": refs, "temperature": "structural",
                "evidence": internal_evidence("Онтология источников MEGABOOK §1.4, решение автора 11-07-2026 (внутренний Uprava)")}
        if parent:
            node["parent"] = parent
        add_node(node)
    for nid, label, chain in VALUE_STAGES + PROVENANCE_STAGES:
        add_node({"id": nid, "kind": "stage", "label_ru": label, "chain": chain,
                  "temperature": "structural"})
    for nid, label in SURFACES:
        add_node({"id": nid, "kind": "surface", "label_ru": label,
                  "temperature": "structural"})
    for nid, label, url, license_, rule, prohibition in EXTERNAL_STACKS:
        node = {"id": nid, "kind": "external-stack", "label_ru": label, "url": url,
                "consume_rule_ru": rule, "prohibition_ru": prohibition,
                "temperature": "structural"}
        if license_:
            node["license"] = license_
        add_node(node)

    for i, (s, t, k) in enumerate(ONTOLOGY_EDGES):
        edges.append({"id": f"e:ont-{i:02d}", "source": s, "target": t, "kind": k,
                      "temperature": "structural",
                      "evidence": internal_evidence("MEGABOOK §1.4/§8 (внутренний Uprava)")})
    for i, (s, t, k) in enumerate(VALUE_EDGES):
        edges.append({"id": f"e:val-{i:02d}", "source": s, "target": t, "kind": k,
                      "temperature": "structural",
                      "evidence": internal_evidence("MEGABOOK §1.2 (внутренний Uprava)")})

    # Structural: asset families + owns / feeds edges.
    for (nid, label, types, owner, url, rights, prohibition, rules, consumers) in ASSET_FAMILIES:
        owner_id = ensure_repo(owner)
        if owner_id is None:
            raise SystemExit(f"asset owner sanitised away: {owner}")
        add_node({"id": nid, "kind": "asset", "label_ru": label,
                  "asset_types": types, "owner": owner_id, "url": url,
                  "rights": rights, "prohibition_ru": prohibition,
                  "rule_refs": rules, "temperature": "structural",
                  "evidence": internal_evidence("Карта переиспользования MEGABOOK §12.2 (внутренний Uprava)")})
        edges.append({"id": f"e:owns-{slug(nid.split(':', 1)[1])}",
                      "source": owner_id, "target": nid, "kind": "owns",
                      "temperature": "structural"})
        for cons in consumers:
            cid = cons if cons.startswith("surface:") else ensure_repo(cons)
            if cid is None:
                dropped_edges += 1
                continue
            edges.append({"id": f"e:reuse-{slug(nid.split(':', 1)[1])}-{slug(cid.split(':', 1)[1])}",
                          "source": nid, "target": cid, "kind": "feeds",
                          "temperature": "structural"})

    # Assessed: theses (§6 + §11.2) and anchors (§9).
    theses = parse_theses(lines, as_of)
    for node in theses.values():
        add_node(node)
    seen_anchor = set()
    for sec, repo in parse_anchors(lines):
        rid = ensure_repo(repo)
        if rid is None:
            dropped_edges += 1
            continue
        eid = f"e:anchor-{sec.replace('.', '-')}-{slug(repo)}"
        if eid in seen_anchor:
            continue
        seen_anchor.add(eid)
        edges.append({"id": eid, "source": f"thesis:{sec}", "target": rid,
                      "kind": "anchors", "temperature": "structural",
                      "evidence": internal_evidence("MEGABOOK §9 — смысловой дом репозитория (внутренний Uprava)")})

    # Assessed: repo dependency edges from interlinks_edges.tsv.
    seen_dep = {}
    for row in parse_tsv(tsv):
        def resolve(name):
            if name == "*":
                return "surface:org-wide"
            if name.startswith("ext:"):
                ext_id = EXT_NAME_MAP.get(name[4:])
                if ext_id is None:
                    raise SystemExit(f"unmapped external stack: {name}")
                return ext_id
            return ensure_repo(name)

        sid, tid = resolve(row["source"]), resolve(row["target"])
        if sid is None or tid is None:
            dropped_edges += 1
            continue
        base = f"e:dep-{slug(sid.split(':', 1)[1])}-{row['kind']}-{slug(tid.split(':', 1)[1])}"
        n = seen_dep.get(base, 0)
        seen_dep[base] = n + 1
        eid = base if n == 0 else f"{base}-{n + 1}"
        edges.append({"id": eid, "source": sid, "target": tid, "kind": row["kind"],
                      "asset_ru": row["asset"], "status": row["status"],
                      "temperature": "assessed", "as_of": as_of,
                      "evidence": internal_evidence(f"interlinks_edges.tsv: {row['evidence']} (внутренний Uprava)")})

    bundle = {
        "$schema": "./atlas.schema.json",
        "contract_version": CONTRACT_VERSION,
        "provenance": {
            "generated": as_of,
            "generator": "scripts/atlas_build_bundle.py",
            "generated_by": args.generated_by,
            "series_slot": "B1 (H623)",
            "sources": [
                {"name": "MEGABOOK.md (Uprava, приватный hub)",
                 "commit": git_short_sha(uprava, "MEGABOOK.md"),
                 "sections": ["§1.2", "§1.4", "§6", "§8", "§9", "§11.2", "§12.2", "§12.3"],
                 "visibility": "internal"},
                {"name": "interlinks_edges.tsv (Uprava, приватный hub)",
                 "commit": git_short_sha(uprava, "interlinks_edges.tsv"),
                 "visibility": "internal"},
            ],
            "sanitisation": {
                "denylist_version": DENYLIST_VERSION,
                "dropped_nodes": len(dropped_nodes),
                "dropped_edges": dropped_edges,
            },
        },
        "nodes": sorted(nodes.values(), key=lambda n: n["id"]),
        "edges": edges,
        "views": build_views(as_of),
    }
    for src in bundle["provenance"]["sources"]:
        if src.get("commit") is None:
            src.pop("commit", None)

    serialized = json.dumps(bundle, ensure_ascii=False, indent=2)
    for pattern in LEAKAGE_PATTERNS:
        if pattern in serialized:
            raise SystemExit(f"LEAKAGE: banned pattern in bundle: {pattern!r}")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(serialized + "\n", encoding="utf-8")
    print(f"wrote {out}: {len(bundle['nodes'])} nodes, {len(bundle['edges'])} edges, "
          f"{len(bundle['views'])} views; dropped {len(dropped_nodes)} nodes / {dropped_edges} edges")


if __name__ == "__main__":
    main()
