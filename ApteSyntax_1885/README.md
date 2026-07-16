# ApteSyntax_1885 — Apte, *The Student's Guide to Sanskrit Composition* (1885)

_Created: 06-07-2026 · Last updated: 16-07-2026_

Raw-source archive and faithful [`.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/Apte-unicode.mdx)
extraction of **Vaman Shivaram Apte's** *The Student's Guide to Sanskrit
Composition* (a syntax / composition manual, reprint reference 1885), together
with the full working archive behind the Russian translation by **N. P.
Likhushina** (*Учебник по санскритскому синтаксису*, version 3.0, 2021), the
1923 Composition Key, Brendan Gillon's syntactic parse of the prose exercises,
and the scanned English↔Sanskrit vocabularies.

This folder is one book directory of the
[SanskritGrammar](https://github.com/gasyoun/SanskritGrammar) archive — see the
[repo README](https://github.com/gasyoun/SanskritGrammar/blob/main/README.md)
for how every `.mdx` is produced (the org-wide `/docx-to-md` skill) and for the
rendered [Docusaurus page](https://gasyoun.github.io/SanskritGrammar/grammars/ApteSyntax_1885/Apte-unicode).

---

## What is here — top level

| File | What it is |
|---|---|
| [Apte-unicode.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/Apte-unicode.mdx) | **The main deliverable** — the full Russian translation of Apte's syntax (Likhushina v3.0, 2021), 15 lessons + introduction + abbreviations, in build-ready MDX |
| [Apte-unicode.docx](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/Apte-unicode.docx) · [Apte-unicode.doc](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/Apte-unicode.doc) | Source Word documents the `.mdx` is extracted from (the `.docx` is authoritative) |
| [01_Apte.zip](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/01_Apte.zip) | The complete original working archive (~101 MB), unpacked under [`src/01_Apte/`](https://github.com/gasyoun/SanskritGrammar/tree/main/ApteSyntax_1885/src/01_Apte) |
| [ERRATA.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/ERRATA.md) · [errata.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/errata.yml) | Per-book errata list (empty so far) — regenerate via the `/errata` skill |

## Реестр проверенных утверждений (H1055, seed — фаза 2)

Пятая книга двухосевого конвейера проверки утверждений (после Кочергиной, Бюлера и
Зализняка ×2) и **первый синтаксический учебник** в реестре. Каждое фальсифицируемое
утверждение оценивается по двум осям — `verdict_fact` (истинно ли относительно корпуса
DCS-2021 + Уитни 1889, с числом) и `verdict_pedagogy` (оправданна ли подача).

**Жанровая проверка (сделана до жатвы, 16-07-2026):** `.mdx` — русский перевод (Лихушина
v3.0, 2021) *Руководства по санскритской композиции* Апте, 30 занятий. В отличие от четырёх
книг, уже в конвейере, Апте — **синтаксический**, а не морфологический: большинство правил —
это управление падежами, согласование и позиция частиц, проверяемые по зависимостному
(head/deprel) слою DCS через инструмент
[`ZalizniakOcherk_1978/treebank_syntax_stats.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/treebank_syntax_stats.py),
а не по поверхностной частотности. Это честно помечено в шапке `claims.yml`, а не втиснуто
в схему силой.

Файлы реестра:

- [claims.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/claims.yml) — верифицированный реестр (APT-1..APT-31: **21 TRUE · 8 OVERSTATED · 1 FALSE · 1 UNTESTABLE**), источник правды;
- [claims_harvest.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/claims_harvest.yml) — бэклог жатвы, **115 кандидатов** (все 30 занятий сжаты; 28 продвинуты);
- [apte_treebank_stats.py](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/apte_treebank_stats.py) → [.json](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/apte_treebank_stats.json) — инструмент дренажа (H1059): позиция частиц, согласование, падеж цели по зависимостному слою DCS;
- [apte_classical_government_stats.py](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/apte_classical_government_stats.py) → [.json](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/apte_classical_government_stats.json) — инструмент управления падежами (H1062): оконная совстречаемость + подъём над базовой линией по ВСЕМУ корпусу, с контролями;
- [apte_pada_stats.py](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/apte_pada_stats.py) → [.json](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/apte_pada_stats.json) — инструмент залога (H1081): Parasmaipada/Ātmanepada по окончаниям презенса (DCS feat_voice кодирует только пассив, не P/Ā), корневой залог по умолчанию;
- [CLAIMS_VERIFIED.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/CLAIMS_VERIFIED.md) + [claims.json](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/claims.json) — генерируются из `claims.yml` скриптом [scripts/build_claims.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_claims.py) (`npm run claims`), руками не править.

**Дренаж backlog treebank-инструментом (H1059, 16-07-2026):** реестр 8 → 24. Позиционные и
согласовательные утверждения дренируются надёжно (согласование глагола с подлежащим по числу
98,21% на n=10 672; `ca`/`tu`/`ced`/`iva`/`eva`/`kila` — почти никогда не в начале предложения),
кроме `uta` — **первый корпусный флаг** (в начале предложения 23,66% против <1% у настоящих
постпозитивов → OVERSTATED). Правила управления делятся натрое: страх/отвращение → аблатив
**подтверждено** (APT-16/17); «бросать» → местный и «править/помнить» → родительный **OVERSTATED**
(в корпусе лидирует конкурирующий падеж); гнев/любовь → **UNTESTABLE** (<10 размеченных аргументов
в ведийски-смещённом срезе). Падеж цели движения: винительный 85,91% против неаккузативного 14,09%
(n=873) — число под флаг APT-5.

**Инструмент управления падежами по классическому корпусу (H1062, 16-07-2026):** там, где
ведийски-смещённый зависимостный срез был слишком тонок для лексемных правил управления,
оконная совстречаемость с подъёмом над базовой линией по всему корпусу закрыла обе строки
UNTESTABLE и **исправила один вердикт**: `ruc` → дательный **подтверждён** (подъём 3,06× над
базовой линией 3,9%; на treebank стоял OVERSTATED из-за ведийского смещения — исправлено);
глаголы гнева → дательный **OVERSTATED** (подъём 0,91×, не обогащён — панинийское правило
дательного гнева предписательно, а не частотно); любовь → местный слабо (1,08×). Метод
проверен контролями: `bhī`/`jugups` → аблатив воспроизводятся (5,52×/3,96×), отрицательный
контроль `dṛś` «видеть» не даёт ложного управления (подъём дательного 0,23×).

**Занятия 26–30 сжаты и дренированы (H1081, 17-07-2026):** пробел покрытия закрыт (все 30
занятий, бэклог 79 → 115). Занятия 29–30 — панинийское назначение залога (Parasmaipada/
Ātmanepada); **DCS feat_voice кодирует только пассив, не P/Ā**, поэтому построен инструмент
[apte_pada_stats.py](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/apte_pada_stats.py),
восстанавливающий залог по окончаниям презенса. Корневой залог по умолчанию дренируется
чисто: `ram` → Ātm. 95,5%, `han` → Paras. 89,9%, `bhāṣ` → Ātm. 97,9%, `nam` → Paras. 83,1%
(все TRUE), `kṛ`/`duh` — оба залога (TRUE); но `krīḍ` «обычно Parasmaipada» на деле почти
поровну (57,6/42,4 → OVERSTATED). Тонкие правила «приставка + значение» (~15 штук) сигнала в
корпусе не имеют (не размечены ни P/Ā, ни семантическое условие) → UNTESTABLE, честно
задокументировано (APT-30).

**Адъюдикация по Уитни — первый FALSE реестра (H1084, 17-07-2026):** APT-31 (Урок 19) — Апте
§210 утверждает, что аорист «выражает идею длительности», а имперфект «не может» — опровергнуто
Уитни §§927-929 (классический аорист «просто претерит, равнозначный имперфекту и перфекту»;
старый аорист — *завершительный*, «завершённое относительно настоящего», противоположность
длительности). Двойная проверка: (1) сверен английский оригинал §210 — ошибка **самого Апте**,
а не перевода Лихушиной; (2) Апте сам себе противоречит (§207-208: прошедшие времена стали
употребляться «беспорядочно» — та же равнозначность Уитни §927).

**Главный вывод seed'а:** фактическая точность Апте высока, а где он расходится с другими
грамматиками — расхождение в **калибровке**, не в истине. Тот же клитико-позиционный факт,
что оценил Кочергину OVERSTATED (её «личная форма глагола никогда не ударна» перегибает с
энклитик на все финитные глаголы, HK-10), оценивает Апте TRUE (APT-8): он ограничивает
правило «никогда в начале предложения» именно энклитическими местоимениями, где оно верно, и
теми же словами — про `ca` (APT-3) и `tu` (APT-4). Та же частотная щель описательного и
простого будущего (14:1), что оценила Бюлера ORDER-QUESTIONABLE (он учит редкую форму первой,
HB-58), оценивает Апте JUSTIFIED (APT-6): он прямо говорит «намного реже». Единственный флаг —
ожидаемое сверхобобщение: «Все глаголы движения управляют винительным» (APT-5, OVERSTATED) —
винительный цели есть умолчание, но дательный и местный цели тоже засвидетельствованы (Уитни
§274, §285d). Бэклог из правил управления — это список инструментов: каждое становится
конкретным treebank-запросом при дренаже.

## The working archive — [`src/01_Apte/`](https://github.com/gasyoun/SanskritGrammar/tree/main/ApteSyntax_1885/src/01_Apte)

Every `.doc`/`.docx` below now has a sibling `.mdx` (97 in total, all converted
by `/docx-to-md`; the `.doc` are kept only as legacy source). PDFs, RTFs,
`.htm`, `.jpg` and data files are left as-is.

### Primary editions and reference PDFs

| File | What it is |
|---|---|
| [Apte-Composition1885.pdf](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/Apte-Composition1885.pdf) | Scan of Apte's *Guide to Sanskrit Composition* (1885 reference) |
| [Apte-CompKey1923.pdf](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/Apte-CompKey1923.pdf) | The 1923 **Key** to the exercises (answer book) |
| [Apte-Sanskrit-Syntax_Russian.pdf](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/Apte-Sanskrit-Syntax_Russian.pdf) | PDF of the Russian syntax translation |
| [Samskrit Nibandh Path Pradarsak - VS Apte 1951.pdf](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/Samskrit%20Nibandh%20Path%20Pradarsak%20-%20VS%20Apte%201951.pdf) | Apte's *Saṃskṛta-Nibandha-Pāṭha-Pradarśaka* (1951 ed.), a related composition reader |
| [Apte-Composition-Complete-17thed.1945-18.11.2015.docx](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/Apte-Composition-Complete-17thed.1945-18.11.2015.docx) | Complete text of the 17th ed. (1945), typed 2015 |
| [Apte-Composition-PayerSolved.docx](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/Apte-Composition-PayerSolved.docx) | Payer's solved-exercises edition |
| [Apte-Composition1885-final-lessons.docx](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/Apte-Composition1885-final-lessons.docx) | Final lesson set of the 1885 text |
| [END-Apte-Composition1885.pdf](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/END-Apte-Composition1885.pdf) · [.rtf](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/END-Apte-Composition1885.rtf) · [Pages from ….rtf](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/Pages%20from%20Apte-Composition1885.rtf) | End-matter / page extracts of the 1885 composition |

### Chapter documents — [`Apte-doc/`](https://github.com/gasyoun/SanskritGrammar/tree/main/ApteSyntax_1885/src/01_Apte/Apte-doc)

`Apte-00.doc` … `Apte-19.doc` — the book split one chapter per file (00 =
front matter, 01–19 = lessons). A nested [`Apte-doc/Apte-doc/`](https://github.com/gasyoun/SanskritGrammar/tree/main/ApteSyntax_1885/src/01_Apte/Apte-doc/Apte-doc)
holds a **duplicate** copy of the same 20-chapter set (kept as archived).

### Publication set — [`Апте для публикации/`](https://github.com/gasyoun/SanskritGrammar/tree/main/ApteSyntax_1885/src/01_Apte/%D0%90%D0%BF%D1%82%D0%B5%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8)

"Apte for publication" — the print-ready chapter set `Apte-00` … `Apte-15`
plus two glossaries:
[`Apte-40-sanskrit_glossary`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/%D0%90%D0%BF%D1%82%D0%B5%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8/Apte-40-sanskrit_glossary.mdx)
and
[`Apte-41-russian_glossary`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/%D0%90%D0%BF%D1%82%D0%B5%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8/Apte-41-russian_glossary.mdx).

### Finished lessons — [`Апте_Готовые уроки/`](https://github.com/gasyoun/SanskritGrammar/tree/main/ApteSyntax_1885/src/01_Apte/%D0%90%D0%BF%D1%82%D0%B5_%D0%93%D0%BE%D1%82%D0%BE%D0%B2%D1%8B%D0%B5%20%D1%83%D1%80%D0%BE%D0%BA%D0%B8)

"Apte finished lessons" — the teaching build, each lesson `Урок N` in two
files: `-unit` (the lesson unit) and `-metod` (the methodological / teacher
notes), for lessons 1–15, plus a few sentence-alignment working files
(`apte14_150_157`, `apte15_158_161`, `apte15_sent_a2s`).

### Other archive material

| Path | What it is |
|---|---|
| [`Интернет-версия-Апте/`](https://github.com/gasyoun/SanskritGrammar/tree/main/ApteSyntax_1885/src/01_Apte/%D0%98%D0%BD%D1%82%D0%B5%D1%80%D0%BD%D0%B5%D1%82-%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D1%8F-%D0%90%D0%BF%D1%82%D0%B5) | "Internet version" — `apte00.htm` … `apte16.htm`, an earlier HTML web edition |
| [`Сканы словариков/`](https://github.com/gasyoun/SanskritGrammar/tree/main/ApteSyntax_1885/src/01_Apte/%D0%A1%D0%BA%D0%B0%D0%BD%D1%8B%20%D1%81%D0%BB%D0%BE%D0%B2%D0%B0%D1%80%D0%B8%D0%BA%D0%BE%D0%B2) | "Dictionary scans" — [English→Sanskrit](https://github.com/gasyoun/SanskritGrammar/tree/main/ApteSyntax_1885/src/01_Apte/%D0%A1%D0%BA%D0%B0%D0%BD%D1%8B%20%D1%81%D0%BB%D0%BE%D0%B2%D0%B0%D1%80%D0%B8%D0%BA%D0%BE%D0%B2/%D0%90%D0%BD%D0%B3%D0%BB%D0%BE-%D1%81%D0%B0%D0%BD%D1%81%D0%BA%D1%80-%D1%81%D0%BB%D0%BE%D0%B2%D0%B0%D1%80%D1%8C) (voc404–416, 7 jpg) and [Sanskrit→English](https://github.com/gasyoun/SanskritGrammar/tree/main/ApteSyntax_1885/src/01_Apte/%D0%A1%D0%BA%D0%B0%D0%BD%D1%8B%20%D1%81%D0%BB%D0%BE%D0%B2%D0%B0%D1%80%D0%B8%D0%BA%D0%BE%D0%B2/%D0%A1%D0%B0%D0%BD%D1%81%D0%BA%D1%80-%D0%B0%D0%BD%D0%B3%D0%BB%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D0%B9%20%D1%81%D0%BB%D0%BE%D0%B2%D0%B0%D1%80%D1%8C) (pp. 373–403, 16 jpg) vocabulary scans |
| [Синтаксические деревья.docx](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/%D0%A1%D0%B8%D0%BD%D1%82%D0%B0%D0%BA%D1%81%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5%20%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D1%8C%D1%8F.docx) → [.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/%D0%A1%D0%B8%D0%BD%D1%82%D0%B0%D0%BA%D1%81%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5%20%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D1%8C%D1%8F.mdx) | "Syntactic trees" — 23 parse-tree tables |
| [Apte_Glossary_English-Sanskrit.docx](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/Apte_Glossary_English-Sanskrit.docx) → [.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/Apte_Glossary_English-Sanskrit.mdx) | Consolidated English→Sanskrit glossary |

### Gillon syntactic parse (data files)

| File | What it is |
|---|---|
| [apte syntax.dat](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/apte%20syntax.dat) · [apte91-gillon.txt](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/apte91-gillon.txt) · [apte-verified.txt](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/src/01_Apte/apte-verified.txt) | **Brendan Gillon's** syntactic parse of the prose-exercise sentences from Apte's *Student's Guide* (begun 1986 at Deccan College). Each sentence carries a syntactic parse, an English translation, and annotations. `apte-verified.txt` is the verified pass. Gillon holds copyright to this material. |

## Regenerating the `.mdx`

All `.mdx` here are reproducible from the Word sources with the org-wide
`/docx-to-md` skill (Pandoc + LibreOffice for legacy `.doc`, grid tables
wrapped in ```` ```rst-table ````, MDX-safety pass). To rebuild after editing a
source:

```
python scripts/docx_to_md.py C:\Users\user\Documents\GitHub\SanskritGrammar\ApteSyntax_1885 --force
```

A conversion pass on 06-07-2026 produced 96 `.mdx` from the archive (0
encoding-damaged files, 0 stray angle brackets) with Opus 4.8
(`claude-opus-4-8`).

_Dr. Mārcis Gasūns_
