# LessonConcordance — поурочный конкорданс Бюлера (урок × источники)

_Created: 01-10-2026 · Last updated: 01-10-2026_

`catalog.mdx` — студент-facing страница, **генерируется** — не редактировать руками:

```bash
python3 scripts/build_lesson_concordance.py
```

Typed-link датасет: [`typed_link_buhler_lessons.tsv`](typed_link_buhler_lessons.tsv) —
каноническая форма `TYPE_D_RECORD_FIELDS` (10 колонок) по
[`TYPED_LINK_ID_GRAMMAR.md`](https://github.com/gasyoun/Uprava/blob/main/TYPED_LINK_ID_GRAMMAR.md)
§1; anchor-типы `buhler-lesson:<RN>` / `buhler-topic:<RN>.<topic>` и 12
target-локусов зарегистрированы в §2/§3 (коммит
`31748b38c4` в Uprava, 01-10-2026), lint-таблицы —
[`kosha/scripts/typed_link_lint.py`](https://github.com/gasyoun/kosha/blob/main/scripts/typed_link_lint.py)
(PRS #657). Проверка:

```bash
python3 /Users/mac/Documents/GitHub/kosha/scripts/typed_link_lint.py LessonConcordance/typed_link_buhler_lessons.tsv
```

**Регистрация (§5, D2b — пер-репо):** датасет живёт здесь; в kosha-манифест
(`data/manifest/datasets.json`) не добавляется до Q2.1 unified release —
прецедент D2b/H540, решение D15 плана.

**Словарь тем (D13):** [`topics.yml`](topics.yml), `meta.version` растёт при
расширении; v1 = спайновая категория `present_a` + расширение `sandhi-visarga`
(фонетика вне 41 морфологической категории — `spine: none`). Ключ темы входит в
anchor `buhler-topic:<RN>.<topic>` — одна строка TSV = связь «урок+тема → локус».

**Пер-тематические заметки об исключениях** (голос D2, гипотеза MG «списки
исключений — много у Бюлера, нет у Зализняка-1978, всегда у Уитни?») живут в
`topics.yml` с цитатами локусов и попадают на страницу при регенерации.

**Разрывы, зафиксированные честно (пилот, урок I):**

- `corpus_layer.tsv` не имеет строк урока I (покрыты XVIII, XXVIII, XXXIV-XLV) — леммный слой урока I строит batch-минт, сейчас корни сшиты с `WhitneyRoots/crosswalk/roots.csv` + talmud-crosswalk;
- `vas` «жить» = vas-3 (roots.csv №717, «dwell», класс I) — омонимия разрешена ростером; ряды З-1975 у jīv (I₂) / nam (M₁) / car (R?) идут на странице как есть, арбитраж за talmud-регистром;
- прямая строка `zalizniak-1975:<slug>` не выдана: в классификации 1975 нет верифицированного инвентаря titled-block слагов; ряд З-1975 идёт через talmud-crosswalk (`talmud:`);
- `frish:` / `apte:` / `speyer:` к уроку I не применимы по матрице плана (синтаксис/хрестоматия — уроки IX+, упражнения I элементарны);
- reuse-кластеров с уроком I в `Concordance/catalog.mdx` — 0.

_Гасунс_
