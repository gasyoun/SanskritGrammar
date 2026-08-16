# ГОСТ-проход по библиографии M03 — сухой прогон

_Created: 17-08-2026 · Last updated: 17-08-2026_

Отчет генератора [gost_bibliography_check.py](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/gost_bibliography_check.py) ([H2871](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2871-Opus_SanskritGrammar_m03-freeze-harness-gost-numbers-prebuild_16.08.26.md)), Opus 5 (`claude-opus-5`). **Сухой прогон: рукопись не изменялась.** Находки — инвентарь к предподачному проходу, а не правки: текст рукописи авторский (H275), review-docx H1259 под автором и не перегенерируется.

**Охват:** 525 записей библиографии, 1049 внутритекстовых ссылок в 4 файлах рукописи из 9; источниковых сокращений в «Принятых сокращениях» — 21.

## Принятые умолчания (политика default-and-log)

| Неоднозначность | Принято | Основание |
|---|---|---|
| Форма тире в рукописи | pandoc-овское `--` считается за `—` | исходник — `.mdx`, тире набирается двумя дефисами во всем тексте |
| Профиль описания | одноуровневое описание монографии; аналитическое — при `//` | ГОСТ Р 7.0.100-2018, 5 и 7 |
| Ключ ссылки | «фамилия(и) + год» сиглы `**Автор** ГОД` | ссылочный аппарат рукописи авторский, номерных ссылок в тексте нет |
| Диапазон годов | `1953--61` разворачивается в `1953-1961` | ГОСТ Р 7.0.100-2018, 5.4.6 (полная форма года) |
| Пропуск номера в списке | считается находкой, а не нормой | номер — точка входа для ссылки и для верстки |

## Сводка находок

| Код | Класс | Находок |
|---|---|---:|
| `R1` | Ссылка без записи в библиографии | 76 |
| `G2` | Год сиглы против года выходных данных | 14 |
| `G6` | Завершающая точка записи | 10 |
| `G8` | Аналитическое описание без локализации части | 44 |
| `G9` | Издательство не указано | 65 |
| `G10` | HTML-сущности из конвертации 2014 г. | 3 |
| `G12` | Разрыв полужирного выделения сиглы | 11 |
| `G3` | Двоеточие без пробела слева (предписанная пунктуация) | 449 |
| `G4` | Разделитель области «. --» | 17 |
| `G5` | Пробел между инициалами | 48 |
| `G7` | Внутрисловное «--» (артефакт конвертации) | 130 |
| `R3` | Ссылка разрешается только после нормализации | 5 |
| `R2` | Запись библиографии без ссылок в тексте | 88 |
| **Итого** | | **960** |

**Зелено (0 находок):** `A1` Сокращение без записи в библиографии · `A2` Год ссылки вне диапазона сокращения · `G0` Запись не разбирается как «сигла -- описание» · `G1` Нумерация списка · `G11` Сигла не выделена полужирным.

## `R1` — Ссылка без записи в библиографии (76)

> Основание: ГОСТ Р 7.0.5-2008, 6.2 — ссылка должна разрешаться в список

- `02_gasuns-dhatu-PhD-text2.mdx:289` — ссылка [Aklujkar 1997] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1166` — ссылка [Antilla 1989] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:2412` — ссылка [Apte 1885] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1134`, `02_gasuns-dhatu-PhD-text2.mdx:632` — ссылка [Apte 1958] не имеет записи в библиографии (2 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:373` — ссылка [Aṣṭāṅgahṛdayasaṃhitā 1998] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:303` — ссылка [Bechert 1979] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:3065`, `02_gasuns-dhatu-PhD-text2.mdx:3067` — ссылка [Boethlingk 1887] не имеет записи в библиографии (4 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:736` — ссылка [Bopp 1916] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:810` — ссылка [Brugman 1908] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:2152`, `02_gasuns-dhatu-PhD-text2.mdx:2170` — ссылка [Böhtlingk 1845] не имеет записи в библиографии (2 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:2074`, `02_gasuns-dhatu-PhD-text2.mdx:2076` — ссылка [Böhtlingk 1855] не имеет записи в библиографии (5 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:2078`, `02_gasuns-dhatu-PhD-text2.mdx:2080` — ссылка [Böhtlingk 1879] не имеет записи в библиографии (4 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1156` — ссылка [Bühler 1927] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:804` — ссылка [Cardona 2004] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:289` — ссылка [Cardona 2008] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1302` — ссылка [Colebrook 1805] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:4331` — ссылка [Goldstücker 1965] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:628` — ссылка [Grassmann 1872] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:417` — ссылка [Grassmann 1875] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:698`, `02_gasuns-dhatu-PhD-text2.mdx:726`, `02_gasuns-dhatu-PhD-text2.mdx:730`, `02_gasuns-dhatu-PhD-text2.mdx:740` — ссылка [Hirt 1928] не имеет записи в библиографии (4 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1290`, `02_gasuns-dhatu-PhD-text2.mdx:2022` — ссылка [Huet 2013] не имеет записи в библиографии (2 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1134` — ссылка [Iyer 1989] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:419` — ссылка [Kielhorn 1886] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:742` — ссылка [Kuryłowicz 1956] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:2338` — ссылка [Lanman 1883] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:2142` — ссылка [Lassen 1838] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:2410` — ссылка [Liebich 1920] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:411` — ссылка [Liebich 1921] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:698` — ссылка [MacDonell 1899] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1148` — ссылка [Macdonell 1899] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:896`, `02_gasuns-dhatu-PhD-text2.mdx:906` — ссылка [Macdonnel 1910] не имеет записи в библиографии (3 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:628` — ссылка [Mayrhofer 1963] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1222`, `02_gasuns-dhatu-PhD-text2.mdx:321` — ссылка [Mayrhofer 1978] не имеет записи в библиографии (2 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1318`, `02_gasuns-dhatu-PhD-text2.mdx:455` — ссылка [Mayrhofer 1986-1996] не имеет записи в библиографии (2 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:628`, `02_gasuns-dhatu-PhD-text2.mdx:630` — ссылка [Mayrhofer 1992] не имеет записи в библиографии (2 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:2070` — ссылка [Monier 1899] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1296`, `02_gasuns-dhatu-PhD-text2.mdx:1734`, `02_gasuns-dhatu-PhD-text2.mdx:932` — ссылка [Monier-Williams 1846] не имеет записи в библиографии (3 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1316`, `02_gasuns-dhatu-PhD-text2.mdx:1318`, `02_gasuns-dhatu-PhD-text2.mdx:1322`, `02_gasuns-dhatu-PhD-text2.mdx:1734`, `02_gasuns-dhatu-PhD-text2.mdx:704`, `02_gasuns-dhatu-PhD-text2.mdx:836` … — ссылка [Monier-Williams 1851] не имеет записи в библиографии (8 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:2024`, `02_gasuns-dhatu-PhD-text2.mdx:836` — ссылка [Monier-Williams 1899] не имеет записи в библиографии (2 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:836` — ссылка [Murti 1984] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:636` — ссылка [Mylius 1988] не имеет записи в библиографии (2 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:930` — ссылка [Narten 1969] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:938` — ссылка [Oldenburg 1890] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1734`, `02_gasuns-dhatu-PhD-text2.mdx:1772`, `02_gasuns-dhatu-PhD-text2.mdx:1986`, `02_gasuns-dhatu-PhD-text2.mdx:1998`, `02_gasuns-dhatu-PhD-text2.mdx:4665`, `02_gasuns-dhatu-PhD-text2.mdx:608` … — ссылка [Renou 1952] не имеет записи в библиографии (7 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:728` — ссылка [Scharfe 1977] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:698` — ссылка [Speyer 1886] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:375` — ссылка [Staal 1965] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:4331` — ссылка [Stchoupak, Nitti, Luigia, Renou 1932] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1326` — ссылка [Stenzler 1847] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1332` — ссылка [Sturtevant 1948] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1734` — ссылка [Szemerényi 1990] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:2082` — ссылка [Turner 1962-1966] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:2735` — ссылка [Uhlenbeck 1908] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1998`, `02_gasuns-dhatu-PhD-text2.mdx:447` — ссылка [Wackernagel 1896] не имеет записи в библиографии (2 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:944` — ссылка [Warder 1967] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:353` — ссылка [Watkins 1969] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:2747` — ссылка [Werba 2013] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:2046`, `02_gasuns-dhatu-PhD-text2.mdx:2048` — ссылка [Whitney 1886] не имеет записи в библиографии (2 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:836` — ссылка [Whitney 1971] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:403` — ссылка [Windisch 1920] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1298`, `02_gasuns-dhatu-PhD-text2.mdx:948` — ссылка [Zimmermann 2006] не имеет записи в библиографии (2 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:736` — ссылка [de Saussure 1922] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:736` — ссылка [de Saussure 1985] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:4331` — ссылка [ndra Dīkshitar 1951-1955] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:439` — ссылка [Арискина 2006] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1326` — ссылка [Блумфилд 2002] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:447` — ссылка [Военец 2005] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1770` — ссылка [Гамкрелидзе 1984] не имеет записи в библиографии (2 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1164`, `02_gasuns-dhatu-PhD-text2.mdx:608`, `02_gasuns-dhatu-PhD-text2.mdx:620` — ссылка [Елизаренкова 1987] не имеет записи в библиографии (3 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:311`, `02_gasuns-dhatu-PhD-text2.mdx:936` — ссылка [Елизаренкова 1993] не имеет записи в библиографии (2 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:381` — ссылка [Звегинцев 1964-1965] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:351`, `02_gasuns-dhatu-PhD-text2.mdx:461` — ссылка [Иванов 1981] не имеет записи в библиографии (2 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:816` — ссылка [Кочергина 2001] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:838` — ссылка [Куртенэ 1963] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:2022` — ссылка [Лихушина 2012] не имеет записи в библиографии (1 вхожд.)
- `02_gasuns-dhatu-PhD-text2.mdx:1160`, `02_gasuns-dhatu-PhD-text2.mdx:1334`, `02_gasuns-dhatu-PhD-text2.mdx:4418` — ссылка [Топоров, Иванов 1960] не имеет записи в библиографии (3 вхожд.)

## `G2` — Год сиглы против года выходных данных (14)

> Основание: ГОСТ Р 7.0.100-2018, 5.4.6

- `02_gasuns-dhatu-PhD-text2.mdx:3343` — запись 64: сигла «2004a» не совпадает ни с одним годом в описании (2004) — Красухин 2004a -- Красухин К. Г. Аспекты индоевропейской реконструкции: Акцентология. Морф
- `02_gasuns-dhatu-PhD-text2.mdx:3345` — запись 65: сигла «2004b» не совпадает ни с одним годом в описании (2004) — Красухин 2004b -- Красухин К. Г. Введение в индоевропейское языкознание: Курс лекций. -- М
- `02_gasuns-dhatu-PhD-text2.mdx:3547` — запись 369: сигла «1919-1966» не совпадает ни с одним годом в описании (1927, 2009) — Mahabharata 1919--1966 -- (= MBh) The Mahabharata Vishnu Sitaram Sukthankar; Shripad Krish
- `02_gasuns-dhatu-PhD-text2.mdx:3567` — запись 471: сигла «2013» не совпадает ни с одним годом в описании (1998) — Skandapurāṇa 2013 -- (= SkPur) The Skandapurāṇa. Vol. 3, Adhyāyas 34.1--61, 53--69 : 
- `02_gasuns-dhatu-PhD-text2.mdx:3785` — запись 188: сигла «1906» не совпадает ни с одним годом в описании (1897) — Brugmann 1906 -- Brugmann K. Grundriß der vergleichenden Grammatik der indogermanischen Sp
- `02_gasuns-dhatu-PhD-text2.mdx:3807` — запись 224: сигла «1968» не совпадает ни с одним годом в описании (1965) — Coseriu 1968 -- Coseriu E. Sincronía, diacronía y tipología (1965) // XI Congreso Internac
- `02_gasuns-dhatu-PhD-text2.mdx:3901` — запись 320: сигла «1970a» не совпадает ни с одним годом в описании (1970) — Jucquois 1970a -- Jucquois G. La théorie de la racine en Indo--Européen, dans : La Linguis
- `02_gasuns-dhatu-PhD-text2.mdx:3903` — запись 321: сигла «1970b» не совпадает ни с одним годом в описании (1970) — Jucquois 1970b -- Jucquois G. La théorie de la racine en Indo--Européen (suite), dans : La
- `02_gasuns-dhatu-PhD-text2.mdx:3905` — запись 322: сигла «1971a» не совпадает ни с одним годом в описании (1971) — Jucquois 1971a -- Jucquois G. La théorie de la racine chez Antoine Meillet, dans : Le Musé
- `02_gasuns-dhatu-PhD-text2.mdx:3907` — запись 323: сигла «1971b» не совпадает ни с одним годом в описании (1971) — Jucquois 1971b -- Jucquois G. La théorie de la racine en Indo--Européen (suite et fin), da
- `02_gasuns-dhatu-PhD-text2.mdx:3945` — запись 359: сигла «1995» не совпадает ни с одним годом в описании (1985) — Levin 1995 -- Levin S. Semitic and Indo--European: The Principal Etymologies: with Observa
- `02_gasuns-dhatu-PhD-text2.mdx:4063` — запись 185: сигла «1951» не совпадает ни с одним годом в описании (1931) — Brough 1951 -- Brough J. Theories of general linguistics in the Sanskrit grammarians // Tr
- `02_gasuns-dhatu-PhD-text2.mdx:4077` — запись 207: сигла «1972» не совпадает ни с одним годом в описании (1976) — Cardona 1972 -- Cardona G. Some Features of Pāṇinian Derivations // Ed. Parret H. History 
- `02_gasuns-dhatu-PhD-text2.mdx:4307` — запись 429: сигла «1989» не совпадает ни с одним годом в описании (1997) — Rasmussen 1989 -- Rasmussen J. E. Studien zur Morphophonemik der indogermanischen Grundspr

## `G6` — Завершающая точка записи (10)

> Основание: ГОСТ Р 7.0.100-2018, 4.5.4

- `02_gasuns-dhatu-PhD-text2.mdx:3431` — запись 28 не закрыта точкой — Гасунс 2011 -- Dhātu // Учебник санскритскаго языка. Грамматика, хрестоматия, словарь. 2-е
- `02_gasuns-dhatu-PhD-text2.mdx:3449` — запись 48 не закрыта точкой — Зализняк 2015 -- (= Zl.) А. А. Зализняк. Санскрит: конспект грамматических сведений // Нов
- `02_gasuns-dhatu-PhD-text2.mdx:3471` — запись 75 не закрыта точкой — Лихушина 2015 -- (= Lh.) Лихушина Н. П. Новая книга для чтения на санскрите / Сост. Н. П. 
- `02_gasuns-dhatu-PhD-text2.mdx:3503` — запись 45 не закрыта точкой — Зализняк 1975 -- Зализняк А. А. Морфонологическая классификация древнеиндийских глагольных
- `02_gasuns-dhatu-PhD-text2.mdx:3557` — запись 435 не закрыта точкой — Rig-Veda 1965 -- (= RV) Müller F. M. The hymns of the Rig-Veda in the Samhita and Pada te
- `02_gasuns-dhatu-PhD-text2.mdx:3567` — запись 471 не закрыта точкой — Skandapurāṇa 2013 -- (= SkPur) The Skandapurāṇa. Vol. 3, Adhyāyas 34.1--61, 53--69 : 
- `02_gasuns-dhatu-PhD-text2.mdx:3993` — запись 430 не закрыта точкой — Rasmussen 1999 -- Rasmussen J. E. Selected Papers on Indo--European Linguistics: With a Se
- `02_gasuns-dhatu-PhD-text2.mdx:4143` — запись 329 не закрыта точкой — Katre 1991 -- Katre S.M. Lexicography of Old Indo--Aryan: Vedic and Sanskrit // Wörterbüch
- `02_gasuns-dhatu-PhD-text2.mdx:4295` — запись 335 не закрыта точкой — Kilbury 1976 -- Kilbury J. The Development of Morphophonemic Theory. -- Amsterdam: John Be
- `02_gasuns-dhatu-PhD-text2.mdx:4313` — запись 461 не закрыта точкой — Ségéral 2004 -- Ségéral Ph. Théorie de l'apophonie et organisation des schèmes en sémitiqu

## `G8` — Аналитическое описание без локализации части (44)

> Основание: ГОСТ Р 7.0.100-2018, 7

- `02_gasuns-dhatu-PhD-text2.mdx:3299` — запись 20: аналитическое описание без указания местоположения части («-- С. x--y») — Булыгина 1964 -- Булыгина Т. В. Пражская школа // Основные направления структурализма. -- 
- `02_gasuns-dhatu-PhD-text2.mdx:3305` — запись 23: аналитическое описание без указания местоположения части («-- С. x--y») — Винокур 1959 -- Винокур Г.О. Заметки по русскому словообразованию // Винокур Г.О. Избранны
- `02_gasuns-dhatu-PhD-text2.mdx:3341` — запись 63: аналитическое описание без указания местоположения части («-- С. x--y») — Красухин 2004 -- Красухин К. Г. Внутренняя реконструкция, относительная хронология и разви
- `02_gasuns-dhatu-PhD-text2.mdx:3353` — запись 72: аналитическое описание без указания местоположения части («-- С. x--y») — Левковская 1955 -- Левковская К. А. О специфике префиксации в системе словообразования (На
- `02_gasuns-dhatu-PhD-text2.mdx:3373` — запись 92: аналитическое описание без указания местоположения части («-- С. x--y») — Поспелов 1955 -- Поспелов Н. С. Соотношение между грамматическими категориями и частями ре
- `02_gasuns-dhatu-PhD-text2.mdx:3375` — запись 93: аналитическое описание без указания местоположения части («-- С. x--y») — Пятаева 2004 -- Пятаева Н. В. От лексического гнезда к генетической парадигме: к проблеме 
- `02_gasuns-dhatu-PhD-text2.mdx:3387` — запись 104: аналитическое описание без указания местоположения части («-- С. x--y») — Соссюр 1977 -- Соссюр де Ф. Курс общей лингвистики // Соссюр Ф. де. Труды по языкознанию. 
- `02_gasuns-dhatu-PhD-text2.mdx:3407` — запись 120: аналитическое описание без указания местоположения части («-- С. x--y») — Щерба 1915 -- Щерба Л. В. Некоторые выводы из моих диалектологических лужицких наблюдений 
- `02_gasuns-dhatu-PhD-text2.mdx:3421` — запись 10: аналитическое описание без указания местоположения части («-- С. x--y») — Бархударов 1979 -- Бархударов А. С. Санскритизация индоарийских языков в лингво--историчес
- `02_gasuns-dhatu-PhD-text2.mdx:3427` — запись 24: аналитическое описание без указания местоположения части («-- С. x--y») — Волошина 2001 -- Волошина О. А. Изучение терминологии Aṣṭādhyāyī Pāṇini как способ знакомс
- `02_gasuns-dhatu-PhD-text2.mdx:3431` — запись 28: аналитическое описание без указания местоположения части («-- С. x--y») — Гасунс 2011 -- Dhātu // Учебник санскритскаго языка. Грамматика, хрестоматия, словарь. 2-е
- `02_gasuns-dhatu-PhD-text2.mdx:3445` — запись 43: аналитическое описание без указания местоположения части («-- С. x--y») — Елизаренкова 2004 -- Елизаренкова Т. Я. Древнеиндийские языки // Языки мира: Индоарийские 
- `02_gasuns-dhatu-PhD-text2.mdx:3449` — запись 48: аналитическое описание без указания местоположения части («-- С. x--y») — Зализняк 2015 -- (= Zl.) А. А. Зализняк. Санскрит: конспект грамматических сведений // Нов
- `02_gasuns-dhatu-PhD-text2.mdx:3461` — запись 58: аналитическое описание без указания местоположения части («-- С. x--y») — Катенина, Рудой 1980 -- Катенина Т. Е., Рудой В. И. Лингвистические знания в Древней Индии
- `02_gasuns-dhatu-PhD-text2.mdx:3469` — запись 69: аналитическое описание без указания местоположения части («-- С. x--y») — Куликов 1993 -- Куликов Л.И. Синтаксическая классификация глаголов и «залоговая ориентиров
- `02_gasuns-dhatu-PhD-text2.mdx:3479` — запись 88: аналитическое описание без указания местоположения части («-- С. x--y») — Парибок 1983 -- Парибок А. В. Преемственность, изменчивость и прогресс в грамматике (на пр
- `02_gasuns-dhatu-PhD-text2.mdx:3511` — запись 110: аналитическое описание без указания местоположения части («-- С. x--y») — Трубецкой 1967 -- Трубецкой Н.С. Некоторые соображения относительно морфонологии / Пер. с 
- `02_gasuns-dhatu-PhD-text2.mdx:3739` — запись 140: аналитическое описание без указания местоположения части («-- С. x--y») — Aronoff 1994 -- Aronoff M. Morphology by itself: stems and inflectional classes // Volume 
- `02_gasuns-dhatu-PhD-text2.mdx:3759` — запись 160: аналитическое описание без указания местоположения части («-- С. x--y») — Berent, Shimron 2003 -- Berent I., Shimron J. What is a root? // Language Processing and A
- `02_gasuns-dhatu-PhD-text2.mdx:3777` — запись 182: аналитическое описание без указания местоположения части («-- С. x--y») — Brandenstein 1952 -- Brandenstein W. Studien zur indogermanischen Grundsprache // Arbeiten
- `02_gasuns-dhatu-PhD-text2.mdx:3797` — запись 204: аналитическое описание без указания местоположения части («-- С. x--y») — Cantineau 1950 -- Cantineau J. Racines et schèmes // Mélanges Milliam Marśais. -- Paris: A
- `02_gasuns-dhatu-PhD-text2.mdx:3807` — запись 224: аналитическое описание без указания местоположения части («-- С. x--y») — Coseriu 1968 -- Coseriu E. Sincronía, diacronía y tipología (1965) // XI Congreso Internac
- `02_gasuns-dhatu-PhD-text2.mdx:3881` — запись 300: аналитическое описание без указания местоположения части («-- С. x--y») — Hockett 2004 -- Hockett Ch. F. Two models of grammatical description // Morphology: Critic
- `02_gasuns-dhatu-PhD-text2.mdx:3895` — запись 316: аналитическое описание без указания местоположения части («-- С. x--y») — Jasanoff 1997 -- Jasanoff J.H. Gathic Avestan cikõitərəš // A. Lubotsky, ed., Sound Law an
- `02_gasuns-dhatu-PhD-text2.mdx:3999` — запись 443: аналитическое описание без указания местоположения части («-- С. x--y») — Rousseau 1984 -- Rousseau, J. La racine arabe et son traitement par les grammairiens europ
- `02_gasuns-dhatu-PhD-text2.mdx:4029` — запись 499: аналитическое описание без указания местоположения части («-- С. x--y») — Watkins 1991 -- Watkins C. Etymologies, equations, and comparanda: Types and values, and c
- `02_gasuns-dhatu-PhD-text2.mdx:4043` — запись 128: аналитическое описание без указания местоположения части («-- С. x--y») — Aklujkar 2008 -- Aklujkar A. Traditions of language study in South Asia // Language in Sou
- `02_gasuns-dhatu-PhD-text2.mdx:4045` — запись 150: аналитическое описание без указания местоположения части («-- С. x--y») — Beauzée 1786 -- Beauzée N. Samskret // Encyclopédie méthodique, ou par ordre de matières, 
- `02_gasuns-dhatu-PhD-text2.mdx:4061` — запись 183: аналитическое описание без указания местоположения части («-- С. x--y») — Bronkhorst 1981 -- Bronkhorst J. Meaning Entries in Panini's Dhatupatha // Journal of Indi
- `02_gasuns-dhatu-PhD-text2.mdx:4071` — запись 195: аналитическое описание без указания местоположения части («-- С. x--y») — Bühler 1972 -- Bühler G. The Roots of the Dhātupāṭha not Found in Literature // Staal, Joh
- `02_gasuns-dhatu-PhD-text2.mdx:4077` — запись 207: аналитическое описание без указания местоположения части («-- С. x--y») — Cardona 1972 -- Cardona G. Some Features of Pāṇinian Derivations // Ed. Parret H. History 
- `02_gasuns-dhatu-PhD-text2.mdx:4083` — запись 210: аналитическое описание без указания местоположения части («-- С. x--y») — Cardona 2003 -- Cardona G. Sanskrit // The Indo--Arian Languages. Ed. G. Cardona, Dh. Jain
- `02_gasuns-dhatu-PhD-text2.mdx:4101` — запись 231: аналитическое описание без указания местоположения части («-- С. x--y») — Deshpande 1983 -- Deshpande M.M. Pāṇini as a frontier grammarian // Chicago Linguistic Soc
- `02_gasuns-dhatu-PhD-text2.mdx:4109` — запись 235: аналитическое описание без указания местоположения части («-- С. x--y») — Devasthali 1973 -- Devasthali G. V. Etymology and Historical Dictionary of Sanskrit // Stu
- `02_gasuns-dhatu-PhD-text2.mdx:4143` — запись 329: аналитическое описание без указания местоположения части («-- С. x--y») — Katre 1991 -- Katre S.M. Lexicography of Old Indo--Aryan: Vedic and Sanskrit // Wörterbüch
- `02_gasuns-dhatu-PhD-text2.mdx:4153` — запись 336: аналитическое описание без указания местоположения части («-- С. x--y») — Killingley, Killingley 1995 -- Killingley S. -- Y., Killingley D. Sanskrit. Languages of t
- `02_gasuns-dhatu-PhD-text2.mdx:4157` — запись 351: аналитическое описание без указания местоположения части («-- С. x--y») — Lazzeroni 1998 -- Lazzeroni R. Sanskrit // The Indo--Arian Languages. Ed. G. Cardona, Dh. 
- `02_gasuns-dhatu-PhD-text2.mdx:4189` — запись 409: аналитическое описание без указания местоположения части («-- С. x--y») — Oldenberg 1890 -- Oldenberg H. The Study of Sanskrit // Comparative Philology, Psychology,
- `02_gasuns-dhatu-PhD-text2.mdx:4197` — запись 424: аналитическое описание без указания местоположения части («-- С. x--y») — Radicchi 2002 -- Radicchi A. Two Buddhist Grammarians: Candragomin and Jayaditya // Indian
- `02_gasuns-dhatu-PhD-text2.mdx:4207` — запись 442: аналитическое описание без указания местоположения части («-- С. x--y») — Roth 1876 -- Roth R. Zur Geschichte des Sanskrit--Worterbuchs. (Gesprochen in der Versamml
- `02_gasuns-dhatu-PhD-text2.mdx:4277` — запись 279: аналитическое описание без указания местоположения части («-- С. x--y») — Grassegger 2004 -- Grassegger H. Phonetik, Phonologie // BWT, Basiswissen Therapie. Ausgab
- `02_gasuns-dhatu-PhD-text2.mdx:4279` — запись 293: аналитическое описание без указания местоположения части («-- С. x--y») — Hellwig 2010 -- Hellwig O. Performance of a Lexical and POS Tagger for Sanskrit // Sanskri
- `02_gasuns-dhatu-PhD-text2.mdx:4305` — запись 400: аналитическое описание без указания местоположения части («-- С. x--y») — Müller 2007 -- Müller S. Zum Germanischen aus laryngaltheoretischer Sicht: mit einer Einfü
- `02_gasuns-dhatu-PhD-text2.mdx:4329` — запись 519: аналитическое описание без указания местоположения части («-- С. x--y») — Wujastyk 1996 -- Wujastyk D. Review of: Dhātu--Pāṭha: The Roots of Language: The Foundatio

## `G9` — Издательство не указано (65)

> Основание: ГОСТ Р 7.0.100-2018, 5.4.5

- `02_gasuns-dhatu-PhD-text2.mdx:3285` — запись 5: издательство не указано — по ГОСТ ставится «[б. и.]» — Арно, Лансло 1991 -- Арно А., Лансло К. Всеобщая рациональная грамматика (Грамматика Пор--
- `02_gasuns-dhatu-PhD-text2.mdx:3289` — запись 12: издательство не указано — по ГОСТ ставится «[б. и.]» — Бенвенист 1955 -- Бенвенист Э. Индоевропейское именное словообразование / Пер. с франц. Н.
- `02_gasuns-dhatu-PhD-text2.mdx:3295` — запись 16: издательство не указано — по ГОСТ ставится «[б. и.]» — Богородицкий 1914 -- Богородицкий В. А. Сравнительная грамматика арio‑европейских языков. 
- `02_gasuns-dhatu-PhD-text2.mdx:3297` — запись 19: издательство не указано — по ГОСТ ставится «[б. и.]» — Булич 1904 -- Булич С. Очерк истории языкознания в России. Т. 1. -- СПб, 1904.
- `02_gasuns-dhatu-PhD-text2.mdx:3307` — запись 25: издательство не указано — по ГОСТ ставится «[б. и.]» — Вяселева 2002 -- Вяселева Р. Р. Истоки и развитие лингвистической теории У. Д. Уитни: дисс
- `02_gasuns-dhatu-PhD-text2.mdx:3309` — запись 26: издательство не указано — по ГОСТ ставится «[б. и.]» — Гамкерлидзе, Иванов 1984 -- Гамкерлидзе Т. В., Иванов Вяч. Вс. Индоевропейский язык и индо
- `02_gasuns-dhatu-PhD-text2.mdx:3313` — запись 31: издательство не указано — по ГОСТ ставится «[б. и.]» — Герценберг 2010 -- Герценберг Л.Г. Краткое введение в индоевропеистику. -- СПб.: Нестор--И
- `02_gasuns-dhatu-PhD-text2.mdx:3319` — запись 34: издательство не указано — по ГОСТ ставится «[б. и.]» — Дельбрюк 1904 -- Дельбрюк Б. Введение в изучение языка (Einleitung in das Sprachstudium: И
- `02_gasuns-dhatu-PhD-text2.mdx:3321` — запись 35: издательство не указано — по ГОСТ ставится «[б. и.]» — Демьянков 1994 -- Демьянков В. З. Морфологическая интерпретация текста и ее моделирование.
- `02_gasuns-dhatu-PhD-text2.mdx:3329` — запись 49: издательство не указано — по ГОСТ ставится «[б. и.]» — Зарайский 1999 -- Зарайский А.А. Истоки британской контенсивной лингвистики XX века: диссе
- `02_gasuns-dhatu-PhD-text2.mdx:3339` — запись 62: издательство не указано — по ГОСТ ставится «[б. и.]» — Красухин 1999 -- Красухин К. Г. Аспекты индоевропейской реконструкции: Акцентология, морфо
- `02_gasuns-dhatu-PhD-text2.mdx:3353` — запись 72: издательство не указано — по ГОСТ ставится «[б. и.]» — Левковская 1955 -- Левковская К. А. О специфике префиксации в системе словообразования (На
- `02_gasuns-dhatu-PhD-text2.mdx:3359` — запись 78: издательство не указано — по ГОСТ ставится «[б. и.]» — Маслов 2007 -- Маслов Ю.С. Введение в языкознание. -- М., 2007.
- `02_gasuns-dhatu-PhD-text2.mdx:3371` — запись 90: издательство не указано — по ГОСТ ставится «[б. и.]» — Поляков 1984 -- Поляков О. В. Сравнительно--историческое (индоевропейское) языкознание в Р
- `02_gasuns-dhatu-PhD-text2.mdx:3373` — запись 92: издательство не указано — по ГОСТ ставится «[б. и.]» — Поспелов 1955 -- Поспелов Н. С. Соотношение между грамматическими категориями и частями ре
- `02_gasuns-dhatu-PhD-text2.mdx:3379` — запись 99: издательство не указано — по ГОСТ ставится «[б. и.]» — Ромашко 1983 -- Ромашко С. А. Лингвистическая концепция романтизма (К истории европейского
- `02_gasuns-dhatu-PhD-text2.mdx:3383` — запись 102: издательство не указано — по ГОСТ ставится «[б. и.]» — Смирницкий 1952 -- Смирницкий А. И. К вопросу о слове (Проблема «отдельности» слова), С. 1
- `02_gasuns-dhatu-PhD-text2.mdx:3407` — запись 120: издательство не указано — по ГОСТ ставится «[б. и.]» — Щерба 1915 -- Щерба Л. В. Некоторые выводы из моих диалектологических лужицких наблюдений 
- `02_gasuns-dhatu-PhD-text2.mdx:3409` — запись 121: издательство не указано — по ГОСТ ставится «[б. и.]» — Щерба 1957 -- Щерба Л. В. Избранные работы по русскому языку. -- М., 1957.
- `02_gasuns-dhatu-PhD-text2.mdx:3413` — запись 123: издательство не указано — по ГОСТ ставится «[б. и.]» — Юлдашев 1958 -- Юлдашев А. А. Система словообразования и спряжения глагола в башкирском яз
- `02_gasuns-dhatu-PhD-text2.mdx:3419` — запись 9: издательство не указано — по ГОСТ ставится «[б. и.]» — Барроу 1976 -- Барроу Т. Санскрит. / Пер. с английского Н. Лариной. Ред. и комм. Т.Я. Елиз
- `02_gasuns-dhatu-PhD-text2.mdx:3425` — запись 15: издательство не указано — по ГОСТ ставится «[б. и.]» — Богатырева 1991 -- Богатырева И. И. Система физиологических терминов санскрита: авторефера
- `02_gasuns-dhatu-PhD-text2.mdx:3427` — запись 24: издательство не указано — по ГОСТ ставится «[б. и.]» — Волошина 2001 -- Волошина О. А. Изучение терминологии Aṣṭādhyāyī Pāṇini как способ знакомс
- `02_gasuns-dhatu-PhD-text2.mdx:3435` — запись 36: издательство не указано — по ГОСТ ставится «[б. и.]» — Десницкая 2009 -- Десницкая Е. А. Методологические основания индийской лингвофилософской т
- `02_gasuns-dhatu-PhD-text2.mdx:3437` — запись 37: издательство не указано — по ГОСТ ставится «[б. и.]» — Димри 1972 -- Димри Дж. П. Индийская и русская филологическая традиция (опыт сравнения на 
- `02_gasuns-dhatu-PhD-text2.mdx:3441` — запись 40: издательство не указано — по ГОСТ ставится «[б. и.]» — Елизаренкова 1960 -- Елизаренкова Т. Я. Аорист в «Ригведе». -- М., 1960.
- `02_gasuns-dhatu-PhD-text2.mdx:3451` — запись 50: издательство не указано — по ГОСТ ставится «[б. и.]» — Захарьин 1981 -- Захарьин Б. А. Строй и типология языка кашмири. М.: Изд--во Моск. ун--та,
- `02_gasuns-dhatu-PhD-text2.mdx:3465` — запись 61: издательство не указано — по ГОСТ ставится «[б. и.]» — Кочергина 1997 -- Кочергина В. А. Санскрит. В кн.: Программы курсов «Сравнительно--историч
- `02_gasuns-dhatu-PhD-text2.mdx:3467` — запись 68: издательство не указано — по ГОСТ ставится «[б. и.]» — Куликов 1989 -- Куликов Л. И. Каузатив в санскрите: автореферат дис... кандидата филологич
- `02_gasuns-dhatu-PhD-text2.mdx:3479` — запись 88: издательство не указано — по ГОСТ ставится «[б. и.]» — Парибок 1983 -- Парибок А. В. Преемственность, изменчивость и прогресс в грамматике (на пр
- `02_gasuns-dhatu-PhD-text2.mdx:3481` — запись 89: издательство не указано — по ГОСТ ставится «[б. и.]» — Парибок 2004 -- Парибок А. В. Система палийского глагола (Глагольные формы и их значения в
- `02_gasuns-dhatu-PhD-text2.mdx:3485` — запись 101: издательство не указано — по ГОСТ ставится «[б. и.]» — Семененко 2011 -- Семененко А. А. Изучение Ригведы в дореволюционной России : 1830 -- 1917
- `02_gasuns-dhatu-PhD-text2.mdx:3487` — запись 106: издательство не указано — по ГОСТ ставится «[б. и.]» — Тавастшерна 2009 -- Тавастшерна С. С. Становление и развитие лингвистической традиции в Др
- `02_gasuns-dhatu-PhD-text2.mdx:3497` — запись 17: издательство не указано — по ГОСТ ставится «[б. и.]» — Бодуэн де Куртенэ 1963 -- Куртенэ И. А. Опыт теории фонетических альтернаций // В кн.: Бод
- `02_gasuns-dhatu-PhD-text2.mdx:3501` — запись 41: издательство не указано — по ГОСТ ставится «[б. и.]» — Елизаренкова 1974 -- Елизаренкова Т. Я. Исследования по диахронической фонологии индоарийс
- `02_gasuns-dhatu-PhD-text2.mdx:3523` — запись 153: издательство не указано — по ГОСТ ставится «[б. и.]» — Belvalkar 1924 -- Belvalkar S.K. Dandin. Kavyadarsa. -- Poona, 1924.
- `02_gasuns-dhatu-PhD-text2.mdx:3535` — запись 259: издательство не указано — по ГОСТ ставится «[б. и.]» — Forthomme 1993 -- Forthomme D. Le Dhatukavya de Narayanabhatta. Un poème didactique Sanskr
- `02_gasuns-dhatu-PhD-text2.mdx:3537` — запись 294: издательство не указано — по ГОСТ ставится «[б. и.]» — Hemacandra 1960 -- Hemacandra. Śabdānuśāsana. Hg. von Vijayalāvaṇya Sūri. -- Bombay, 1960.
- `02_gasuns-dhatu-PhD-text2.mdx:3539` — запись 327: издательство не указано — по ГОСТ ставится «[б. и.]» — Kāmasūtra 1900 -- Vātsyāyana. Kāmasūtram with commentary of Yasodhara, dvitiyam samskarana
- `02_gasuns-dhatu-PhD-text2.mdx:3545` — запись 363: издательство не указано — по ГОСТ ставится «[б. и.]» — Liebich 1930 -- Liebich B. Kommentar zu Panini's Dhatupatha. Zum ersten Mal herausgegeben 
- `02_gasuns-dhatu-PhD-text2.mdx:3563` — запись 450: издательство не указано — по ГОСТ ставится «[б. и.]» — Sāyaṇa 1897 -- Sāyaṇa. Mādhavīya--Dhatuvṛtti. -- Benares, 1897.
- `02_gasuns-dhatu-PhD-text2.mdx:3571` — запись 507: издательство не указано — по ГОСТ ставится «[б. и.]» — Whitney 1863 -- Whitney W.D. The Taittirīya--Prātiśākhya. With its Commentary the Tribhāṣy
- `02_gasuns-dhatu-PhD-text2.mdx:3613` — запись 205: издательство не указано — по ГОСТ ставится «[б. и.]» — Cappeller 1887 -- Cappeller C. Sanskrit--Wörterbuch nach den Petersburger Wörterbüchern Be
- `02_gasuns-dhatu-PhD-text2.mdx:3617` — запись 220: издательство не указано — по ГОСТ ставится «[б. и.]» — Cohen 1976 -- Cohen D. Dictionnaire des Racines Sémitiques out attestées das les langues s
- `02_gasuns-dhatu-PhD-text2.mdx:3659` — запись 392: издательство не указано — по ГОСТ ставится «[б. и.]» — Mish 1991 -- Mish F. Webster's Ninth New Collegiate Dictionary. -- Springfield: Merriam--W
- `02_gasuns-dhatu-PhD-text2.mdx:3719` — запись 515: издательство не указано — по ГОСТ ставится «[б. и.]» — Wilson 1851 -- Wilson H. H. Grammars & Dictionaries of the Sanskrit Language / Ed. Reinhol
- `02_gasuns-dhatu-PhD-text2.mdx:3725` — запись 126: издательство не указано — по ГОСТ ставится «[б. и.]» — Adelung 1781 -- Adelung J. Ch. Über den Ursprung der Sprache und den Bau der Wörter, beson
- `02_gasuns-dhatu-PhD-text2.mdx:3743` — запись 146: издательство не указано — по ГОСТ ставится «[б. и.]» — Baayen, Schreuder 2003 -- Baayen R. H., Schreuder R. Morphological Structure in Language P
- `02_gasuns-dhatu-PhD-text2.mdx:3785` — запись 188: издательство не указано — по ГОСТ ставится «[б. и.]» — Brugmann 1906 -- Brugmann K. Grundriß der vergleichenden Grammatik der indogermanischen Sp
- `02_gasuns-dhatu-PhD-text2.mdx:3803` — запись 219: издательство не указано — по ГОСТ ставится «[б. и.]» — Chomsky 1978 -- Chomsky N. Topics in the Theory of Generative Grammar. -- Walter de Gruyte
- `02_gasuns-dhatu-PhD-text2.mdx:3829` — запись 248: издательство не указано — по ГОСТ ставится «[б. и.]» — Elgin 1973 -- Elgin S. H. What is Linguistics? -- New York: Prentice--Hall, 1973.
- `02_gasuns-dhatu-PhD-text2.mdx:3863` — запись 285: издательство не указано — по ГОСТ ставится «[б. и.]» — Gusdorf 1973 -- Gusdorf G. L'avénement des sciences humaines au siede des lumieres. (Les s
- `02_gasuns-dhatu-PhD-text2.mdx:3941` — запись 356: издательство не указано — по ГОСТ ставится «[б. и.]» — Lehmann, Malkiel 1982 -- Lehmann W. Ph., Malkiel Y. Perspectives on Historical Linguistics
- `02_gasuns-dhatu-PhD-text2.mdx:4007` — запись 459: издательство не указано — по ГОСТ ставится «[б. и.]» — Schottelius 1663 -- Schottelius J. G. Ausführliche Arbeit von der teutschen Haubt Sprache.
- `02_gasuns-dhatu-PhD-text2.mdx:4035` — запись 517: издательство не указано — по ГОСТ ставится «[б. и.]» — Windischmann 1844 -- Windischmann F.H.H. Der Fortschritt der Sprachenkunde und ihre gegenw
- `02_gasuns-dhatu-PhD-text2.mdx:4061` — запись 183: издательство не указано — по ГОСТ ставится «[б. и.]» — Bronkhorst 1981 -- Bronkhorst J. Meaning Entries in Panini's Dhatupatha // Journal of Indi
- `02_gasuns-dhatu-PhD-text2.mdx:4101` — запись 231: издательство не указано — по ГОСТ ставится «[б. и.]» — Deshpande 1983 -- Deshpande M.M. Pāṇini as a frontier grammarian // Chicago Linguistic Soc
- `02_gasuns-dhatu-PhD-text2.mdx:4111` — запись 244: издательство не указано — по ГОСТ ставится «[б. и.]» — Edgerton 1909 -- Edgerton F. The Sanskrit K--Suffixes. -- Baltimore, 1909.
- `02_gasuns-dhatu-PhD-text2.mdx:4141` — запись 326: издательство не указано — по ГОСТ ставится «[б. и.]» — Kale 1894 -- Kale M. R. A Higher Sanskrit Grammar: For the Use of School and College Stude
- `02_gasuns-dhatu-PhD-text2.mdx:4159` — запись 352: издательство не указано — по ГОСТ ставится «[б. и.]» — Lebedev 1801 -- Lebedev G. S. A Grammar of the Pure and Mixed East Indian Dialects. -- Lon
- `02_gasuns-dhatu-PhD-text2.mdx:4207` — запись 442: издательство не указано — по ГОСТ ставится «[б. и.]» — Roth 1876 -- Roth R. Zur Geschichte des Sanskrit--Worterbuchs. (Gesprochen in der Versamml
- `02_gasuns-dhatu-PhD-text2.mdx:4211` — запись 454: издательство не указано — по ГОСТ ставится «[б. и.]» — Schlegel 1808 -- Schlegel von F. Über die Sprache und die Weisheit der Indier. Nebst metri
- `02_gasuns-dhatu-PhD-text2.mdx:4275` — запись 223: издательство не указано — по ГОСТ ставится «[б. и.]» — Corssen 1868 -- Corssen W. P. Über Aussprache, Vokalismus und Betonung der lateinischen Sp
- `02_gasuns-dhatu-PhD-text2.mdx:4277` — запись 279: издательство не указано — по ГОСТ ставится «[б. и.]» — Grassegger 2004 -- Grassegger H. Phonetik, Phonologie // BWT, Basiswissen Therapie. Ausgab
- `02_gasuns-dhatu-PhD-text2.mdx:4289` — запись 309: издательство не указано — по ГОСТ ставится «[б. и.]» — Hulst, Ritter 1999 -- Hulst H. van der, Ritter N. A. The Syllable: Views and Facts. -- Wal

## `G10` — HTML-сущности из конвертации 2014 г. (3)

> Основание: оформительский дефект

- `02_gasuns-dhatu-PhD-text2.mdx:3547` — запись 369: HTML-сущности из конвертации 2014 г. (&gt;, &lt;) — наборщик воспроизведет их буквально
- `02_gasuns-dhatu-PhD-text2.mdx:3627` — запись 269: HTML-сущности из конвертации 2014 г. (&gt;, &lt;) — наборщик воспроизведет их буквально
- `02_gasuns-dhatu-PhD-text2.mdx:3657` — запись 384: HTML-сущности из конвертации 2014 г. (&gt;, &lt;) — наборщик воспроизведет их буквально

## `G12` — Разрыв полужирного выделения сиглы (11)

> Основание: оформительский дефект конвертации 2014 г.

- `02_gasuns-dhatu-PhD-text2.mdx:3335` — запись 57: полужирное выделение сиглы разорвано (`**История** **отечественного...** 1990 -- История отечествен`) — верстка воспроизведет разрыв
- `02_gasuns-dhatu-PhD-text2.mdx:3343` — запись 64: полужирное выделение сиглы разорвано (`**Красухин** 2004a** **-- Красухин К. Г. Аспекты индоевропей`) — верстка воспроизведет разрыв
- `02_gasuns-dhatu-PhD-text2.mdx:3345` — запись 65: полужирное выделение сиглы разорвано (`**Красухин** 2004b** **-- Красухин К. Г. Введение в индоевро`) — верстка воспроизведет разрыв
- `02_gasuns-dhatu-PhD-text2.mdx:3497` — запись 17: полужирное выделение сиглы разорвано (`**Бодуэн** **де Куртенэ** 1963 -- Куртенэ И. А. Опыт теории `) — верстка воспроизведет разрыв
- `02_gasuns-dhatu-PhD-text2.mdx:3599` — запись 170: полужирное выделение сиглы разорвано (`**Böhtlingk** 1879--1889** **-- (=PWK) Böhtlingk O. Sanskrit`) — верстка воспроизведет разрыв
- `02_gasuns-dhatu-PhD-text2.mdx:3601` — запись 172: полужирное выделение сиглы разорвано (`**Böhtlingk**, **Roth** 1855--1875** **-- (=PWG) Böhtlingk O`) — верстка воспроизведет разрыв
- `02_gasuns-dhatu-PhD-text2.mdx:3663` — запись 395: полужирное выделение сиглы разорвано (`**Monier**--**Williams** 1872 -- Williams M. A Sanskṛit--En`) — верстка воспроизведет разрыв
- `02_gasuns-dhatu-PhD-text2.mdx:3791` — запись 197: полужирное выделение сиглы разорвано (`**Bulletin** **des sciences** 1828 -- Bulletin des sciences `) — верстка воспроизведет разрыв
- `02_gasuns-dhatu-PhD-text2.mdx:3875` — запись 297: полужирное выделение сиглы разорвано (`**Hirt** 1921--1937** **-- Hirt H. Indogermanische Grammatik`) — верстка воспроизведет разрыв
- `02_gasuns-dhatu-PhD-text2.mdx:3901` — запись 320: полужирное выделение сиглы разорвано (`**Jucquois** 1970a** **-- Jucquois G. La théorie de la racin`) — верстка воспроизведет разрыв
- `02_gasuns-dhatu-PhD-text2.mdx:3903` — запись 321: полужирное выделение сиглы разорвано (`**Jucquois** 1970b** **-- Jucquois G. La théorie de la racin`) — верстка воспроизведет разрыв

## `G3` — Двоеточие без пробела слева (предписанная пунктуация) (449)

> Основание: ГОСТ Р 7.0.100-2018, 4.5.4 (предписанная пунктуация)

- `02_gasuns-dhatu-PhD-text2.mdx:3263` — запись 91: 1 двоеточие без пробела слева («СПб.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3265` — запись 94: 1 двоеточие без пробела слева («Baroda:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3267` — запись 111: 1 двоеточие без пробела слева («СПб.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3271` — запись 77: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3273` — запись 95: 1 двоеточие без пробела слева («языков:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3279` — запись 2: 2 двоеточий без пробела слева («учений:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3281` — запись 3: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3283` — запись 4: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3285` — запись 5: 1 двоеточие без пробела слева («Л.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3287` — запись 8: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3289` — запись 12: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3291` — запись 13: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3293` — запись 14: 1 двоеточие без пробела слева («Новосибирск:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3295` — запись 16: 1 двоеточие без пробела слева («Казань:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3299` — запись 20: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3301` — запись 21: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3305` — запись 23: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3307` — запись 25: 1 двоеточие без пробела слева («Уитни:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3311` — запись 30: 1 двоеточие без пробела слева («Л.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3313` — запись 31: 1 двоеточие без пробела слева («СПб.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3315` — запись 32: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3317` — запись 33: 2 двоеточий без пробела слева («языков:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3319` — запись 34: 1 двоеточие без пробела слева («Sprachstudium:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3321` — запись 35: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3323` — запись 39: 2 двоеточий без пробела слева («М.:»; «Classica:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3325` — запись 46: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3329` — запись 49: 1 двоеточие без пробела слева («века:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3331` — запись 53: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3333` — запись 55: 2 двоеточий без пробела слева («тысячелетия:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3335` — запись 57: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3337` — запись 60: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3339` — запись 62: 2 двоеточий без пробела слева («реконструкции:»; «синтаксис:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3341` — запись 63: 2 двоеточий без пробела слева («языков:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3343` — запись 64: 2 двоеточий без пробела слева («реконструкции:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3345` — запись 65: 2 двоеточий без пробела слева («языкознание:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3347` — запись 66: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3349` — запись 70: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3351` — запись 71: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3355` — запись 73: 3 двоеточий без пробела слева («века:»; «языка:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3357` — запись 74: 2 двоеточий без пробела слева («Текстология:»; «СПб.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3361` — запись 80: 1 двоеточие без пробела слева («Л.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3363` — запись 81: 3 двоеточий без пробела слева («индоевропеистике:»; «Редкол.:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3365` — запись 83: 3 двоеточий без пробела слева («индоевропеистике:»; «Редкол.:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3367` — запись 84: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3369` — запись 85: 1 двоеточие без пробела слева («Л.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3375` — запись 93: 6 двоеточий без пробела слева («парадигме:»; «филология:»; «перспективы:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3377` — запись 97: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3381` — запись 100: 2 двоеточий без пробела слева («языков:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3383` — запись 102: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3385` — запись 103: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3387` — запись 104: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3389` — запись 105: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3393` — запись 108: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3395` — запись 113: 1 двоеточие без пробела слева («Л.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3397` — запись 114: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3399` — запись 116: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3401` — запись 117: 2 двоеточий без пробела слева («Языковедение:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3403` — запись 118: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3405` — запись 119: 3 двоеточий без пробела слева («индоевропеистике:»; «Редкол.:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3407` — запись 120: 1 двоеточие без пробела слева («кн.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3411` — запись 122: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3413` — запись 123: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3415` — запись 124: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3419` — запись 9: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3421` — запись 10: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3423` — запись 11: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3425` — запись 15: 1 двоеточие без пробела слева («санскрита:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3427` — запись 24: 2 двоеточий без пробела слева («образования:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3429` — запись 27: 1 двоеточие без пробела слева («Новосибирск:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3431` — запись 28: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3433` — запись 29: 1 двоеточие без пробела слева («Л.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3435` — запись 36: 1 двоеточие без пробела слева («защиты:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3443` — запись 42: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3445` — запись 43: 2 двоеточий без пробела слева («мира:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3447` — запись 44: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3449` — запись 48: 3 двоеточий без пробела слева («Санскрит:»; «Санскрит:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3451` — запись 50: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3453` — запись 51: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3455` — запись 52: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3457` — запись 54: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3459` — запись 56: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3461` — запись 58: 1 двоеточие без пробела слева («Л.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3463` — запись 59: 1 двоеточие без пробела слева («Лейпциг:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3465` — запись 61: 2 двоеточий без пробела слева («кн.:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3467` — запись 68: 1 двоеточие без пробела слева («санскрите:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3469` — запись 69: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3471` — запись 75: 2 двоеточий без пробела слева («Санскрит:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3473` — запись 76: 3 двоеточий без пробела слева («индоевропеистике:»; «Редкол.:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3475` — запись 82: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3477` — запись 86: 1 двоеточие без пробела слева («Л.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3481` — запись 89: 1 двоеточие без пробела слева («диахронии):») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3483` — запись 98: 1 двоеточие без пробела слева («Харьков:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3485` — запись 101: 1 двоеточие без пробела слева («защиты:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3487` — запись 106: 2 двоеточий без пробела слева («Индии:»; «защиты:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3489` — запись 109: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3491` — запись 115: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3495` — запись 7: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3497` — запись 17: 1 двоеточие без пробела слева («кн.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3503` — запись 45: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3505` — запись 67: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3507` — запись 87: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3509` — запись 96: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3511` — запись 110: 2 двоеточий без пробела слева («кружок:»; «М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3513` — запись 112: 1 двоеточие без пробела слева («М.:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3521` — запись 143: 1 двоеточие без пробела слева («Bonn:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3525` — запись 171: 2 двоеточий без пробела слева («Grammatik:»; «Leipzig:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3527` — запись 203: 1 двоеточие без пробела слева («Poona:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3529` — запись 216: 1 двоеточие без пробела слева («Rajshahi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3531` — запись 236: 1 двоеточие без пробела слева («[Haryana]:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3541` — запись 328: 2 двоеточий без пробела слева («Pāṇini:»; «Austin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3543` — запись 345: 1 двоеточие без пробела слева («[Haryana]:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3547` — запись 369: 1 двоеточие без пробела слева («Poona:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3551` — запись 388: 1 двоеточие без пробела слева («Leiden:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3553` — запись 404: 1 двоеточие без пробела слева («Cambridge:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3555` — запись 432: 1 двоеточие без пробела слева («Paris:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3559` — запись 446: 1 двоеточие без пробела слева («Varanasi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3561` — запись 449: 1 двоеточие без пробела слева («Mysore:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3565` — запись 467: 1 двоеточие без пробела слева («Varanasi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3569` — запись 492: 1 двоеточие без пробела слева («Allahabad:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3571` — запись 507: 1 двоеточие без пробела слева («Tribhāṣyaratna:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3575` — запись 125: 1 двоеточие без пробела слева («Baroda:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3577` — запись 135: 1 двоеточие без пробела слева («Poona:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3579` — запись 136: 1 двоеточие без пробела слева («Poona:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3581` — запись 137: 1 двоеточие без пробела слева («Bombay:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3583` — запись 138: 1 двоеточие без пробела слева («Poona:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3585` — запись 141: 1 двоеточие без пробела слева («Oxford:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3587` — запись 144: 1 двоеточие без пробела слева («Leipzig:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3589` — запись 147: 1 двоеточие без пробела слева («Cambrdidge:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3591` — запись 148: 1 двоеточие без пробела слева («Strassburg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3593` — запись 154: 2 двоеточий без пробела слева («dictionary:»; «London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3595` — запись 162: 2 двоеточий без пробела слева («Vācaspatyam:»; «Vārāṇasī:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3597` — запись 163: 2 двоеточий без пробела слева («lexicon:»; «Calcutta:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3599` — запись 170: 1 двоеточие без пробела слева («Petersburg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3601` — запись 172: 1 двоеточие без пробела слева («Petersburg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3603` — запись 177: 1 двоеточие без пробела слева («Berolini:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3605` — запись 181: 1 двоеточие без пробела слева («Calcutta:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3607` — запись 191: 2 двоеточий без пробела слева («Languages:»; «Chicago:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3611` — запись 202: 1 двоеточие без пробела слева («Edinburgh:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3615` — запись 206: 2 двоеточий без пробела слева («dictionary:»; «Strassburg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3617` — запись 220: 1 двоеточие без пробела слева («sémitiques:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3619` — запись 225: 1 двоеточие без пробела слева («Boulder:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3621` — запись 245: 1 двоеточие без пробела слева («Haven:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3623` — запись 264: 1 двоеточие без пробела слева («Praha:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3625` — запись 265: 1 двоеточие без пробела слева («Halle:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3627` — запись 269: 1 двоеточие без пробела слева («Poona:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3629` — запись 274: 2 двоеточий без пробела слева («English:»; «Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3633` — запись 287: 2 двоеточий без пробела слева («Language:»; «London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3635` — запись 289: 1 двоеточие без пробела слева («Hyderabad:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3637` — запись 292: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3639` — запись 315: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3641` — запись 338: 1 двоеточие без пробела слева («Heidelberg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3643` — запись 365: 2 двоеточий без пробела слева («dictionary:»; «London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3645` — запись 367: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3647` — запись 368: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3649` — запись 371: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3651` — запись 372: 2 двоеточий без пробела слева («encyclopaedia:»; «Delhi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3653` — запись 378: 1 двоеточие без пробела слева («Heidelberg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3655` — запись 381: 1 двоеточие без пробела слева («Heidelberg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3657` — запись 384: 1 двоеточие без пробела слева («Pune:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3659` — запись 392: 1 двоеточие без пробела слева («Springfield:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3661` — запись 394: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3663` — запись 395: 1 двоеточие без пробела слева («Oxford:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3665` — запись 396: 1 двоеточие без пробела слева («Oxford:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3667` — запись 411: 1 двоеточие без пробела слева («Poona:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3669` — запись 415: 1 двоеточие без пробела слева («York:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3671` — запись 417: 2 двоеточий без пробела слева («Band:»; «Band:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3673` — запись 423: 1 двоеточие без пробела слева («Kalikātā:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3675` — запись 425: 1 двоеточие без пробела слева («Madras:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3677` — запись 426: 1 двоеточие без пробела слева («Madrās:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3679` — запись 431: 1 двоеточие без пробела слева («Paris:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3681` — запись 436: 1 двоеточие без пробела слева («Wiesbaden:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3683` — запись 437: 1 двоеточие без пробела слева («Wiesbaden:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3685` — запись 440: 1 двоеточие без пробела слева («Berolini:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3687` — запись 447: 1 двоеточие без пробела слева («Madras‑1:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3689` — запись 448: 2 двоеточий без пробела слева («Upasargārthacandrikā:»; «Dillī:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3691` — запись 458: 1 двоеточие без пробела слева («Leipzig:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3693` — запись 465: 1 двоеточие без пробела слева («Calcutta:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3695` — запись 466: 1 двоеточие без пробела слева («Delhi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3697` — запись 470: 1 двоеточие без пробела слева («Delhi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3699` — запись 474: 1 двоеточие без пробела слева («Delhi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3701` — запись 480: 1 двоеточие без пробела слева («Paris:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3703` — запись 489: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3705` — запись 501: 1 двоеточие без пробела слева («Boston:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3707` — запись 502: 1 двоеточие без пробела слева («Wiesbaden:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3709` — запись 503: 2 двоеточий без пробела слева («Indoarica:»; «Wien:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3711` — запись 504: 1 двоеточие без пробела слева («Rhenum:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3713` — запись 509: 1 двоеточие без пробела слева («Leipzig:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3715` — запись 512: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3717` — запись 513: 1 двоеточие без пробела слева («Calcutta:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3721` — запись 521: 2 двоеточий без пробела слева («English:»; «Calcutta:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3727` — запись 127: 1 двоеточие без пробела слева («Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3729` — запись 131: 1 двоеточие без пробела слева («California:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3731` — запись 132: 1 двоеточие без пробела слева («York:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3733` — запись 133: 1 двоеточие без пробела слева («Innsbruck:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3735` — запись 134: 1 двоеточие без пробела слева («Amsterdam:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3737` — запись 139: 1 двоеточие без пробела слева («Freiburg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3739` — запись 140: 2 двоеточий без пробела слева («itself:»; «Cambridge:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3741` — запись 145: 2 двоеточий без пробела слева («sciences:»; «Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3743` — запись 146: 1 двоеточие без пробела слева («Processing:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3745` — запись 149: 2 двоеточий без пробела слева («Papers:»; «Amsterdam:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3747` — запись 152: 2 двоеточий без пробела слева («Linguistics:»; «Amsterdam:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3749` — запись 155: 1 двоеточие без пробела слева («München:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3751` — запись 156: 2 двоеточий без пробела слева («indo--européenes:»; «Paris:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3753` — запись 157: 1 двоеточие без пробела слева («Paris:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3755` — запись 158: 1 двоеточие без пробела слева («Paris:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3757` — запись 159: 1 двоеточие без пробела слева («words:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3759` — запись 160: 1 двоеточие без пробела слева («Philadelphia:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3761` — запись 165: 2 двоеточий без пробела слева («Morphemes:»; «Wiesbaden:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3763` — запись 167: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3765` — запись 168: 2 двоеточий без пробела слева («Theory:»; «Philadelphia:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3767` — запись 169: 1 двоеточие без пробела слева («Petersburg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3769` — запись 173: 2 двоеточий без пробела слева («Macrofamily:»; «Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3771` — запись 174: 2 двоеточий без пробела слева («Morphologie:»; «Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3773` — запись 178: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3775` — запись 180: 2 двоеточий без пробела слева («Grammar:»; «Cambridge:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3777` — запись 182: 1 двоеточие без пробела слева («Vienna:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3779` — запись 184: 1 двоеточие без пробела слева («Paris:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3781` — запись 186: 1 двоеточие без пробела слева («Strassburg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3783` — запись 187: 1 двоеточие без пробела слева («Munich:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3789` — запись 190: 1 двоеточие без пробела слева («Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3791` — запись 197: 1 двоеточие без пробела слева («Paris:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3793` — запись 200: 2 двоеточий без пробела слева («Morphology:»; «Amsterdam:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3795` — запись 201: 2 двоеточий без пробела слева («Linguistics:»; «Edinburgh:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3797` — запись 204: 1 двоеточие без пробела слева («Paris:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3799` — запись 215: 2 двоеточий без пробела слева («Language:»; «Cambridge:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3801` — запись 218: 2 двоеточий без пробела слева («Chomsky:»; «London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3805` — запись 222: 1 двоеточие без пробела слева («Amsterdam:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3807` — запись 224: 1 двоеточие без пробела слева («Madrid:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3809` — запись 226: 1 двоеточие без пробела слева («Leipzig:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3811` — запись 228: 1 двоеточие без пробела слева («Genève:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3813` — запись 229: 1 двоеточие без пробела слева («Paris:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3815` — запись 238: 2 двоеточий без пробела слева («Tradition:»; «München:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3817` — запись 239: 1 двоеточие без пробела слева («Rīga:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3819` — запись 240: 1 двоеточие без пробела слева («York:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3821` — запись 241: 2 двоеточий без пробела слева («Structuralism:»; «Minneapolis:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3823` — запись 242: 1 двоеточие без пробела слева («Genève:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3825` — запись 243: 2 двоеточий без пробела слева («Philology:»; «York:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3827` — запись 247: 1 двоеточие без пробела слева («Cambridge:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3829` — запись 248: 1 двоеточие без пробела слева («York:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3831` — запись 251: 1 двоеточие без пробела слева («Innsbruck:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3833` — запись 252: 2 двоеточий без пробела слева («Europas:»; «Göttingen:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3835` — запись 255: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3837` — запись 256: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3839` — запись 257: 2 двоеточий без пробела слева («Linguistics:»; «Amsterdam:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3841` — запись 260: 2 двоеточий без пробела слева («Culture:»; «Oxford:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3843` — запись 261: 2 двоеточий без пробела слева («Language:»; «London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3845` — запись 262: 2 двоеточий без пробела слева («Reconstruction:»; «Oxford:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3847` — запись 266: 1 двоеточие без пробела слева («Amsterdam:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3849` — запись 267: 1 двоеточие без пробела слева («Hague:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3851` — запись 270: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3853` — запись 271: 2 двоеточий без пробела слева («Romantik:»; «Tübingen:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3855` — запись 272: 1 двоеточие без пробела слева («York:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3857` — запись 281: 2 двоеточий без пробела слева («Language:»; «Alto:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3859` — запись 282: 1 двоеточие без пробела слева («Bonn:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3861` — запись 284: 1 двоеточие без пробела слева («Poona:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3865` — запись 286: 2 двоеточий без пробела слева («Linguistics:»; «Oxford:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3867` — запись 288: 1 двоеточие без пробела слева («Cambridge:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3869` — запись 291: 2 двоеточий без пробела слева («Chomsky:»; «York:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3871` — запись 295: 1 двоеточие без пробела слева («York:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3873` — запись 296: 1 двоеточие без пробела слева («Strassburg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3875` — запись 297: 1 двоеточие без пробела слева («Heidelberg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3877` — запись 298: 2 двоеточий без пробела слева («Indogermanica:»; «(Saale):») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3879` — запись 299: 2 двоеточий без пробела слева («Relationship:»; «Hague:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3881` — запись 300: 1 двоеточие без пробела слева («Morphology:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3883` — запись 302: 2 двоеточий без пробела слева («Arabic:»; «Georgetown:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3885` — запись 308: 2 двоеточий без пробела слева («Language:»; «York:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3887` — запись 310: 2 двоеточий без пробела слева («Sprachbaues:»; «Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3889` — запись 311: 2 двоеточий без пробела слева («Speech:»; «York:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3891` — запись 313: 2 двоеточий без пробела слева («Writings:»; «Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3893` — запись 314: 1 двоеточие без пробела слева («Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3895` — запись 316: 1 двоеточие без пробела слева («Atlanta:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3897` — запись 317: 2 двоеточий без пробела слева («Morphology:»; «Amsterdam:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3899` — запись 318: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3913` — запись 330: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3915` — запись 337: 1 двоеточие без пробела слева («(Michigan):») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3917` — запись 339: 2 двоеточий без пробела слева («Reviewed:»; «Oxford:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3919` — запись 340: 2 двоеточий без пробела слева («Sciences:»; «Amsterdam:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3921` — запись 341: 2 двоеточий без пробела слева («Sciences:»; «Oxford:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3923` — запись 342: 1 двоеточие без пробела слева («Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3925` — запись 343: 2 двоеточий без пробела слева («Grammar:»; «Cambridge:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3927` — запись 344: 2 двоеточий без пробела слева («Series:»; «London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3929` — запись 346: 1 двоеточие без пробела слева («Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3931` — запись 347: 1 двоеточие без пробела слева («Kraków:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3933` — запись 348: 2 двоеточий без пробела слева («Structure:»; «York:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3935` — запись 350: 1 двоеточие без пробела слева («Cambridge:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3937` — запись 354: 2 двоеточий без пробела слева («Linguistics:»; «London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3939` — запись 355: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3941` — запись 356: 1 двоеточие без пробела слева («Linguistics:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3943` — запись 358: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3945` — запись 359: 3 двоеточий без пробела слева («Indo--European:»; «Etymologies:»; «Amsterdam:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3947` — запись 360: 1 двоеточие без пробела слева («Amsterdam:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3949` — запись 376: 1 двоеточие без пробела слева («Harmondsworth:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3951` — запись 377: 1 двоеточие без пробела слева («Cambridge:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3953` — запись 385: 2 двоеточий без пробела слева («2.:»; «Paris:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3955` — запись 386: 1 двоеточие без пробела слева («Alabama:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3957` — запись 387: 1 двоеточие без пробела слева («Leipzig:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3959` — запись 389: 2 двоеточий без пробела слева («Griechischen:»; «Hamburg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3963` — запись 391: 2 двоеточий без пробела слева («Large:»; «London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3965` — запись 398: 1 двоеточие без пробела слева («Leipzig:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3967` — запись 399: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3969` — запись 403: 2 двоеточий без пробела слева («Language:»; «London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3971` — запись 405: 2 двоеточий без пробела слева («Docenti:»; «Arbor:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3973` — запись 406: 2 двоеточий без пробела слева («Systematization:»; «Helsinki:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3975` — запись 407: 1 двоеточие без пробела слева («York:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3977` — запись 413: 2 двоеточий без пробела слева («Jahrhundert:»; «Tübingen:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3979` — запись 414: 2 двоеточий без пробела слева («Language:»; «Bloomington:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3981` — запись 416: 2 двоеточий без пробела слева («Sprachwissenschaft:»; «Bern:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3983` — запись 418: 2 двоеточий без пробела слева («Works:»; «Hague:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3985` — запись 419: 2 двоеточий без пробела слева («Indo--Europea:»; «Washington:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3987` — запись 420: 1 двоеточие без пробела слева («Lemgo:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3989` — запись 421: 1 двоеточие без пробела слева («York:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3991` — запись 428: 2 двоеточий без пробела слева («Indogermanica:»; «København:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3993` — запись 430: 2 двоеточий без пробела слева («Linguistics:»; «København:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3995` — запись 434: 1 двоеточие без пробела слева («Pforzheim:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:3997` — запись 438: 2 двоеточий без пробела слева («Linguistics:»; «London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4001` — запись 445: 2 двоеточий без пробела слева («Language:»; «York:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4003` — запись 451: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4005` — запись 456: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4009` — запись 460: 1 двоеточие без пробела слева («Hague:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4011` — запись 468: 2 двоеточий без пробела слева («History:»; «Amsterdam:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4013` — запись 469: 2 двоеточий без пробела слева («Language:»; «Cambridge:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4015` — запись 472: 1 двоеточие без пробела слева («York:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4017` — запись 483: 1 двоеточие без пробела слева («Haven:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4019` — запись 484: 1 двоеточие без пробела слева («Darmstadt:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4021` — запись 486: 1 двоеточие без пробела слева («Saale:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4023` — запись 491: 2 двоеточий без пробела слева («idéologies:»; «Bruxelles:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4025` — запись 494: 1 двоеточие без пробела слева («Leiden:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4027` — запись 498: 1 двоеточие без пробела слева («Tübingen:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4029` — запись 499: 3 двоеточий без пробела слева («comparanda:»; «Patterns:»; «Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4031` — запись 500: 1 двоеточие без пробела слева («Innsbruck:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4037` — запись 522: 2 двоеточий без пробела слева («Science:»; «Amsterdam:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4039` — запись 523: 1 двоеточие без пробела слева («Oxford:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4043` — запись 128: 1 двоеточие без пробела слева («Cambridge:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4045` — запись 150: 2 двоеточий без пробела слева («d'artistes:»; «Paris--Liège:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4047` — запись 151: 2 двоеточий без пробела слева («Indologie:»; «Darmstadt:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4049` — запись 161: 1 двоеточие без пробела слева («Bombay:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4051` — запись 164: 1 двоеточие без пробела слева («Calcutta:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4053` — запись 166: 1 двоеточие без пробела слева («Strassburg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4055` — запись 175: 1 двоеточие без пробела слева («Main:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4057` — запись 176: 1 двоеточие без пробела слева («[Berolini]:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4059` — запись 179: 1 двоеточие без пробела слева («Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4065` — запись 192: 1 двоеточие без пробела слева («Delhi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4071` — запись 195: 1 двоеточие без пробела слева («Cambridge:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4073` — запись 196: 2 двоеточий без пробела слева («Sanskrit:»; «Darmstadt:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4075` — запись 198: 1 двоеточие без пробела слева («Varanasi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4077` — запись 207: 2 двоеточий без пробела слева («Linguistics:»; «Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4079` — запись 208: 2 двоеточий без пробела слева («Pāṇini:»; «Hauge:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4081` — запись 209: 1 двоеточие без пробела слева («Delhi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4083` — запись 210: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4087` — запись 212: 1 двоеточие без пробела слева («Serampore:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4089` — запись 213: 1 двоеточие без пробела слева («Calcutta:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4091` — запись 214: 1 двоеточие без пробела слева («Louvain:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4093` — запись 217: 1 двоеточие без пробела слева («Calcutta:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4095` — запись 221: 1 двоеточие без пробела слева («Calcutta:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4097` — запись 227: 1 двоеточие без пробела слева («Leiden:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4099` — запись 230: 1 двоеточие без пробела слева («Halle:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4103` — запись 232: 2 двоеточий без пробела слева («Prakrit:»; «Delhi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4107` — запись 234: 1 двоеточие без пробела слева («Poona:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4109` — запись 235: 1 двоеточие без пробела слева («Poona:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4115` — запись 249: 1 двоеточие без пробела слева («Berkeley:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4119` — запись 253: 1 двоеточие без пробела слева («Wien:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4121` — запись 254: 1 двоеточие без пробела слева («Paris:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4123` — запись 258: 1 двоеточие без пробела слева («Calcutta:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4125` — запись 273: 2 двоеточий без пробела слева («Pāṇini:»; «Varanasi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4127` — запись 275: 1 двоеточие без пробела слева («Leiden:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4131` — запись 278: 1 двоеточие без пробела слева («Petersburg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4133` — запись 283: 1 двоеточие без пробела слева («Firenze:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4135` — запись 290: 2 двоеточий без пробела слева («l'Avesta:»; «Paris:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4137` — запись 301: 1 двоеточие без пробела слева («Heidelberg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4139` — запись 304: 2 двоеточий без пробела слева («Sanskrit:»; «Leiden:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4141` — запись 326: 1 двоеточие без пробела слева («Grammar:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4143` — запись 329: 3 двоеточий без пробела слева («Indo--Aryan:»; «Wörterbücher:»; «Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4145` — запись 331: 1 двоеточие без пробела слева («Wiesbaden:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4147` — запись 332: 1 двоеточие без пробела слева («Wiesbaden:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4149` — запись 333: 2 двоеточий без пробела слева («Language:»; «Allahabad:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4151` — запись 334: 1 двоеточие без пробела слева («Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4153` — запись 336: 1 двоеточие без пробела слева («München:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4155` — запись 349: 1 двоеточие без пробела слева («Cambridge:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4157` — запись 351: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4161` — запись 357: 1 двоеточие без пробела слева («[Adyar]:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4165` — запись 362: 1 двоеточие без пробела слева («Heidelberg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4169` — запись 366: 2 двоеточий без пробела слева («appendixes:»; «Oxford:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4171` — запись 370: 1 двоеточие без пробела слева («Baroda:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4173` — запись 375: 1 двоеточие без пробела слева («Cambridge:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4175` — запись 379: 1 двоеточие без пробела слева («Wien:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4179` — запись 393: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4181` — запись 397: 2 двоеточий без пробела слева («Sanskrit:»; «Leipzig:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4183` — запись 401: 1 двоеточие без пробела слева («Wiesbaden:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4185` — запись 402: 1 двоеточие без пробела слева («Wien:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4187` — запись 408: 2 двоеточий без пробела слева («Language:»; «Delhi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4189` — запись 409: 1 двоеточие без пробела слева («Chicago:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4191` — запись 410: 1 двоеточие без пробела слева («Chicago:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4193` — запись 412: 1 двоеточие без пробела слева («Poona:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4195` — запись 422: 1 двоеточие без пробела слева («Bombay:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4197` — запись 424: 3 двоеточий без пробела слева («Grammarians:»; «Studies:»; «Delhi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4199` — запись 427: 2 двоеточий без пробела слева («Zend--avesta:»; «Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4201` — запись 433: 1 двоеточие без пробела слева («Lyon:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4203` — запись 439: 1 двоеточие без пробела слева («Dordrecht:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4209` — запись 452: 2 двоеточий без пробела слева («Philosophy:»; «Collingdale:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4213` — запись 455: 1 двоеточие без пробела слева («Bonn:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4215` — запись 462: 1 двоеточие без пробела слева («Hyderabad:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4217` — запись 463: 1 двоеточие без пробела слева («Delhi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4219` — запись 464: 1 двоеточие без пробела слева («Delhi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4221` — запись 473: 1 двоеточие без пробела слева («Moscow:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4223` — запись 475: 1 двоеточие без пробела слева («Leiden:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4225` — запись 476: 1 двоеточие без пробела слева («Strassburg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4227` — запись 477: 1 двоеточие без пробела слева («Description:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4229` — запись 478: 1 двоеточие без пробела слева («Massachusetts:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4231` — запись 479: 2 двоеточий без пробела слева («Universals:»; «Chicago:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4233` — запись 481: 1 двоеточие без пробела слева («Giessen:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4235` — запись 482: 1 двоеточие без пробела слева («Heidelberg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4237` — запись 485: 1 двоеточие без пробела слева («Allahabad:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4239` — запись 487: 2 двоеточий без пробела слева («Teil:»; «Heidelberg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4241` — запись 488: 2 двоеточий без пробела слева («Teil:»; «Heidelberg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4243` — запись 493: 1 двоеточие без пробела слева («Dordrecht:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4245` — запись 495: 3 двоеточий без пробела слева («Wiesbaden:»; «(Vorträge:»; «Wissenschaften:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4247` — запись 496: 1 двоеточие без пробела слева («Göttingen:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4249` — запись 497: 1 двоеточие без пробела слева («Göttingen:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4251` — запись 508: 1 двоеточие без пробела слева («York:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4253` — запись 510: 1 двоеточие без пробела слева («Leipzig:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4255` — запись 511: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4257` — запись 514: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4259` — запись 516: 1 двоеточие без пробела слева («Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4261` — запись 518: 1 двоеточие без пробела слева («Delhi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4263` — запись 520: 1 двоеточие без пробела слева («Calcutta:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4265` — запись 524: 1 двоеточие без пробела слева («Sonepat:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4267` — запись 525: 1 двоеточие без пробела слева («Wiesbaden:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4271` — запись 129: 1 двоеточие без пробела слева («London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4273` — запись 130: 2 двоеточий без пробела слева («Century:»; «Chicago:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4277` — запись 279: 1 двоеточие без пробела слева («Idstein:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4279` — запись 293: 1 двоеточие без пробела слева («Delhi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4283` — запись 305: 1 двоеточие без пробела слева («Amsterdam:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4287` — запись 307: 1 двоеточие без пробела слева («Delhi:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4289` — запись 309: 1 двоеточие без пробела слева («Syllable:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4291` — запись 312: 1 двоеточие без пробела слева («Stuttgart:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4295` — запись 335: 1 двоеточие без пробела слева («Amsterdam:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4297` — запись 353: 1 двоеточие без пробела слева («Austin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4299` — запись 374: 2 двоеточий без пробела слева («Phonology:»; «London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4301` — запись 380: 1 двоеточие без пробела слева («Heidelberg:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4303` — запись 382: 1 двоеточие без пробела слева («Wien:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4305` — запись 400: 2 двоеточий без пробела слева («Sicht:»; «Berlin:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4307` — запись 429: 1 двоеточие без пробела слева («Innsbruck:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4311` — запись 453: 1 двоеточие без пробела слева («Providence:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4313` — запись 461: 2 двоеточий без пробела слева («Morphology:»; «London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4315` — запись 490: 2 двоеточий без пробела слева («Phonetics:»; «London:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4321` — запись 263: 2 двоеточий без пробела слева («Indoarica:»; «I:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4323` — запись 268: 2 двоеточий без пробела слева («Indoarica:»; «I:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4325` — запись 277: 1 двоеточие без пробела слева («Review:») — предписанная пунктуация требует «X : Y»
- `02_gasuns-dhatu-PhD-text2.mdx:4329` — запись 519: 3 двоеточий без пробела слева («of:»; «Dhātu--Pāṭha:»; «Language:») — предписанная пунктуация требует «X : Y»

## `G4` — Разделитель области «. --» (17)

> Основание: ГОСТ Р 7.0.100-2018, 4.5.4

- `02_gasuns-dhatu-PhD-text2.mdx:3331` — запись 53: 1 разделитель области без предшествующей точки (нужно «. -- ») — Звегинцев 1964--1965 -- Звегинцев В. А. История языкознания ХIХ--ХХ веков в очерках и извл
- `02_gasuns-dhatu-PhD-text2.mdx:3335` — запись 57: 1 разделитель области без предшествующей точки (нужно «. -- ») — История отечественного... 1990 -- История отечественного востоковедения до середины XIX ве
- `02_gasuns-dhatu-PhD-text2.mdx:3371` — запись 90: 1 разделитель области без предшествующей точки (нужно «. -- ») — Поляков 1984 -- Поляков О. В. Сравнительно--историческое (индоевропейское) языкознание в Р
- `02_gasuns-dhatu-PhD-text2.mdx:3379` — запись 99: 1 разделитель области без предшествующей точки (нужно «. -- ») — Ромашко 1983 -- Ромашко С. А. Лингвистическая концепция романтизма (К истории европейского
- `02_gasuns-dhatu-PhD-text2.mdx:3485` — запись 101: 1 разделитель области без предшествующей точки (нужно «. -- ») — Семененко 2011 -- Семененко А. А. Изучение Ригведы в дореволюционной России : 1830 -- 1917
- `02_gasuns-dhatu-PhD-text2.mdx:3583` — запись 138: 1 разделитель области без предшествующей точки (нужно «. -- ») — Apte 1957--1959 -- Apte V. Sh. Revised and enlarged edition of Prin. V. S. Apte's The Prac
- `02_gasuns-dhatu-PhD-text2.mdx:3627` — запись 269: 1 разделитель области без предшествующей точки (нужно «. -- ») — Ghatage, Joshi, Ranade, Bhatta, Gandhe 1976--&lt;2009&gt; -- Ghatage, A. M., Joshi, S. D.,
- `02_gasuns-dhatu-PhD-text2.mdx:3785` — запись 188: 1 разделитель области без предшествующей точки (нужно «. -- ») — Brugmann 1906 -- Brugmann K. Grundriß der vergleichenden Grammatik der indogermanischen Sp
- `02_gasuns-dhatu-PhD-text2.mdx:3787` — запись 189: 1 разделитель области без предшествующей точки (нужно «. -- ») — Brugmann 1908 -- Brugmann K. Formans oder Formativum? // Indogermanische Forschungen. Zeit
- `02_gasuns-dhatu-PhD-text2.mdx:3829` — запись 248: 1 разделитель области без предшествующей точки (нужно «. -- ») — Elgin 1973 -- Elgin S. H. What is Linguistics? -- New York: Prentice--Hall, 1973.
- `02_gasuns-dhatu-PhD-text2.mdx:3839` — запись 257: 1 разделитель области без предшествующей точки (нужно «. -- ») — Fleischman 2000 -- Fleischman S. Methodologies and Ideologies in Historical Linguistics: O
- `02_gasuns-dhatu-PhD-text2.mdx:3953` — запись 385: 1 разделитель области без предшествующей точки (нужно «. -- ») — Meillet 1938 -- Meillet A. Linguistique historique et linguistique générale. Tom. (1) -- 2
- `02_gasuns-dhatu-PhD-text2.mdx:4013` — запись 469: 1 разделитель области без предшествующей точки (нужно «. -- ») — Silverstein 1971 -- Silverstein M. Whitney on Language: Selected Writings of William Dwigh
- `02_gasuns-dhatu-PhD-text2.mdx:4143` — запись 329: 1 разделитель области без предшествующей точки (нужно «. -- ») — Katre 1991 -- Katre S.M. Lexicography of Old Indo--Aryan: Vedic and Sanskrit // Wörterbüch
- `02_gasuns-dhatu-PhD-text2.mdx:4233` — запись 481: 2 разделителей области без предшествующей точки (нужно «. -- ») — Stenzler 1915 -- Stenzler A. F. Elementarbuch der Sanskrit--Sprache (Grammatik -- Texte --
- `02_gasuns-dhatu-PhD-text2.mdx:4235` — запись 482: 1 разделитель области без предшествующей точки (нужно «. -- ») — Stiehl 2004 -- Stiehl U. Sanskrit--Kompendium. Ein Lehr--, Übungs -- und Nachschlagewerk. 
- `02_gasuns-dhatu-PhD-text2.mdx:4259` — запись 516: 1 разделитель области без предшествующей точки (нужно «. -- ») — Windisch 1917 -- Windisch E. Geschichte der Sanskrit--Philologie und Indischen Altertumsku

## `G5` — Пробел между инициалами (48)

> Основание: ГОСТ Р 7.0.100-2018, 4.5.4

- `02_gasuns-dhatu-PhD-text2.mdx:3267` — запись 111: инициалы без пробела (Ф.Ф.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3293` — запись 14: инициалы без пробела (О.Н.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3303` — запись 22: инициалы без пробела (В.В.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3305` — запись 23: инициалы без пробела (Г.О.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3313` — запись 31: инициалы без пробела (Л.Г.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3317` — запись 33: инициалы без пробела (М.М.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3327` — запись 47: инициалы без пробела (А.А.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3329` — запись 49: инициалы без пробела (А.А.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3351` — запись 71: инициалы без пробела (В.А.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3355` — запись 73: инициалы без пробела (Е.А.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3359` — запись 78: инициалы без пробела (Ю.С.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3363` — запись 81: инициалы без пробела (В.А., Д.Г.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3365` — запись 83: инициалы без пробела (В.А.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3369` — запись 85: инициалы без пробела (Ю.В.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3383` — запись 102: инициалы без пробела (В.В., Г.Ф., И.В.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3405` — запись 119: инициалы без пробела (В.А.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3411` — запись 122: инициалы без пробела (Ю.А.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3419` — запись 9: инициалы без пробела (Т.Я.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3453` — запись 51: инициалы без пробела (М.В.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3455` — запись 52: инициалы без пробела (М.В.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3469` — запись 69: инициалы без пробела (Л.И.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3473` — запись 76: инициалы без пробела (В.А.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3497` — запись 17: инициалы без пробела (И.А.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3509` — запись 96: инициалы без пробела (А.А.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3511` — запись 110: инициалы без пробела (Н.С.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3513` — запись 112: инициалы без пробела (Ф.Ф.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3523` — запись 153: инициалы без пробела (S.K.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3551` — запись 388: инициалы без пробела (E.J.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3553` — запись 404: инициалы без пробела (B.A.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3571` — запись 507: инициалы без пробела (W.D.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3587` — запись 144: инициалы без пробела (F.A.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3589` — запись 147: инициалы без пробела (H.W.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3637` — запись 292: инициалы без пробела (F.C., R.R.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3699` — запись 474: инициалы без пробела (P.C.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3711` — запись 504: инициалы без пробела (N.L.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3895` — запись 316: инициалы без пробела (J.H.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3915` — запись 337: инициалы без пробела (J.L.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:3949` — запись 376: инициалы без пробела (P.H.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:4015` — запись 472: инициалы без пробела (D.I.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:4035` — запись 517: инициалы без пробела (F.H.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:4049` — запись 161: инициалы без пробела (R.G.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:4101` — запись 231: инициалы без пробела (M.M.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:4103` — запись 232: инициалы без пробела (M.M.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:4115` — запись 249: инициалы без пробела (B.A., M.B.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:4139` — запись 304: инициалы без пробела (E.J.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:4143` — запись 329: инициалы без пробела (S.M.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:4275` — запись 223: инициалы без пробела (B.G.) — требуется «Фамилия И. О.»
- `02_gasuns-dhatu-PhD-text2.mdx:4291` — запись 312: инициалы без пробела (A.V.) — требуется «Фамилия И. О.»

## `G7` — Внутрисловное «--» (артефакт конвертации) (130)

> Основание: оформительский дефект, не предусмотренный ГОСТ Р 7.0.100-2018

- `02_gasuns-dhatu-PhD-text2.mdx:3267` — запись 111: 2 внутрисловных «--» — артефакт конвертации (Самаведа--араньяка)
- `02_gasuns-dhatu-PhD-text2.mdx:3285` — запись 5: 2 внутрисловных «--» — артефакт конвертации (Изд--во, Пор--Рояля)
- `02_gasuns-dhatu-PhD-text2.mdx:3289` — запись 12: 1 внутрисловное «--» — артефакт конвертации (Изд--во)
- `02_gasuns-dhatu-PhD-text2.mdx:3295` — запись 16: 2 внутрисловных «--» — артефакт конвертации (Им--го, Ун--та)
- `02_gasuns-dhatu-PhD-text2.mdx:3301` — запись 21: 1 внутрисловное «--» — артефакт конвертации (Сравнительно--историческое)
- `02_gasuns-dhatu-PhD-text2.mdx:3309` — запись 26: 2 внутрисловных «--» — артефакт конвертации (I--II, историко--типологический)
- `02_gasuns-dhatu-PhD-text2.mdx:3313` — запись 31: 1 внутрисловное «--» — артефакт конвертации (Нестор--История)
- `02_gasuns-dhatu-PhD-text2.mdx:3317` — запись 33: 1 внутрисловное «--» — артефакт конвертации (Историко--типологическая)
- `02_gasuns-dhatu-PhD-text2.mdx:3321` — запись 35: 1 внутрисловное «--» — артефакт конвертации (Изд--во)
- `02_gasuns-dhatu-PhD-text2.mdx:3331` — запись 53: 1 внутрисловное «--» — артефакт конвертации (ХIХ--ХХ)
- `02_gasuns-dhatu-PhD-text2.mdx:3341` — запись 63: 1 внутрисловное «--» — артефакт конвертации (Сравнительно--историческое)
- `02_gasuns-dhatu-PhD-text2.mdx:3343` — запись 64: 1 внутрисловное «--» — артефакт конвертации (Ин--т)
- `02_gasuns-dhatu-PhD-text2.mdx:3347` — запись 66: 1 внутрисловное «--» — артефакт конвертации (Ин--т)
- `02_gasuns-dhatu-PhD-text2.mdx:3353` — запись 72: 2 внутрисловных «--» — артефакт конвертации (Изд--во, Ин--т)
- `02_gasuns-dhatu-PhD-text2.mdx:3355` — запись 73: 1 внутрисловное «--» — артефакт конвертации (Изд--во)
- `02_gasuns-dhatu-PhD-text2.mdx:3357` — запись 74: 2 внутрисловных «--» — артефакт конвертации (X--XVII, Ин--т)
- `02_gasuns-dhatu-PhD-text2.mdx:3361` — запись 80: 2 внутрисловных «--» — артефакт конвертации (ун--тов, фак--тов)
- `02_gasuns-dhatu-PhD-text2.mdx:3371` — запись 90: 2 внутрисловных «--» — артефакт конвертации (Сравнительно--историческое, сравнительно--исторических)
- `02_gasuns-dhatu-PhD-text2.mdx:3373` — запись 92: 2 внутрисловных «--» — артефакт конвертации (Изд--во, Ин--т)
- `02_gasuns-dhatu-PhD-text2.mdx:3375` — запись 93: 2 внутрисловных «--» — артефакт конвертации (Изд--во, ун--та)
- `02_gasuns-dhatu-PhD-text2.mdx:3383` — запись 102: 1 внутрисловное «--» — артефакт конвертации (Изд--воАкадемии)
- `02_gasuns-dhatu-PhD-text2.mdx:3393` — запись 108: 2 внутрисловных «--» — артефакт конвертации (ун--та, фак--тов)
- `02_gasuns-dhatu-PhD-text2.mdx:3395` — запись 113: 4 внутрисловных «--» — артефакт конвертации (Научно--исслед, ин--т, ин--та, лит--ры)
- `02_gasuns-dhatu-PhD-text2.mdx:3413` — запись 123: 1 внутрисловное «--» — артефакт конвертации (Изд--во)
- `02_gasuns-dhatu-PhD-text2.mdx:3419` — запись 9: 1 внутрисловное «--» — артефакт конвертации (Изд--во)
- `02_gasuns-dhatu-PhD-text2.mdx:3421` — запись 10: 1 внутрисловное «--» — артефакт конвертации (лингво--историческом)
- `02_gasuns-dhatu-PhD-text2.mdx:3427` — запись 24: 2 внутрисловных «--» — артефакт конвертации (Изд--во, Ун--та)
- `02_gasuns-dhatu-PhD-text2.mdx:3435` — запись 36: 2 внутрисловных «--» — артефакт конвертации (Санкт--Петербург, ун--т)
- `02_gasuns-dhatu-PhD-text2.mdx:3451` — запись 50: 2 внутрисловных «--» — артефакт конвертации (Изд--во, ун--та)
- `02_gasuns-dhatu-PhD-text2.mdx:3453` — запись 51: 2 внутрисловных «--» — артефакт конвертации (Ин--т, Ун--т)
- `02_gasuns-dhatu-PhD-text2.mdx:3455` — запись 52: 2 внутрисловных «--» — артефакт конвертации (Ин--т, Ун--т)
- `02_gasuns-dhatu-PhD-text2.mdx:3459` — запись 56: 1 внутрисловное «--» — артефакт конвертации (Навья--Ньяя)
- `02_gasuns-dhatu-PhD-text2.mdx:3465` — запись 61: 2 внутрисловных «--» — артефакт конвертации (Диалог--МГУ, Сравнительно--историческое)
- `02_gasuns-dhatu-PhD-text2.mdx:3467` — запись 68: 1 внутрисловное «--» — артефакт конвертации (Ин--т)
- `02_gasuns-dhatu-PhD-text2.mdx:3485` — запись 101: 1 внутрисловное «--» — артефакт конвертации (ун--т)
- `02_gasuns-dhatu-PhD-text2.mdx:3487` — запись 106: 2 внутрисловных «--» — артефакт конвертации (Санкт--Петербург, ун--т)
- `02_gasuns-dhatu-PhD-text2.mdx:3529` — запись 216: 6 внутрисловных «--» — артефакт конвертации (Dhātu--pradeepa, Dhātu--prādīpaḥ, Maitreya--rakṣita, mahāmahopādhyayā--śrī)
- `02_gasuns-dhatu-PhD-text2.mdx:3563` — запись 450: 1 внутрисловное «--» — артефакт конвертации (Mādhavīya--Dhatuvṛtti)
- `02_gasuns-dhatu-PhD-text2.mdx:3571` — запись 507: 1 внутрисловное «--» — артефакт конвертации (Taittirīya--Prātiśākhya)
- `02_gasuns-dhatu-PhD-text2.mdx:3577` — запись 135: 1 внутрисловное «--» — артефакт конвертации (English--Sanskrit)
- `02_gasuns-dhatu-PhD-text2.mdx:3579` — запись 136: 1 внутрисловное «--» — артефакт конвертации (Sanskrit--English)
- `02_gasuns-dhatu-PhD-text2.mdx:3581` — запись 137: 1 внутрисловное «--» — артефакт конвертации (English--Sanskrit)
- `02_gasuns-dhatu-PhD-text2.mdx:3583` — запись 138: 1 внутрисловное «--» — артефакт конвертации (Sanskrit--English)
- `02_gasuns-dhatu-PhD-text2.mdx:3593` — запись 154: 2 внутрисловных «--» — артефакт конвертации (Anglo--Saxon, Sanskrit--English)
- `02_gasuns-dhatu-PhD-text2.mdx:3597` — запись 163: 2 внутрисловных «--» — артефакт конвертации (Sanskrit--English)
- `02_gasuns-dhatu-PhD-text2.mdx:3601` — запись 172: 1 внутрисловное «--» — артефакт конвертации (Sanskrit--Wörterbuch)
- `02_gasuns-dhatu-PhD-text2.mdx:3605` — запись 181: 1 внутрисловное «--» — артефакт конвертации (English--Sanskrit)
- `02_gasuns-dhatu-PhD-text2.mdx:3607` — запись 191: 1 внутрисловное «--» — артефакт конвертации (Indo--European)
- `02_gasuns-dhatu-PhD-text2.mdx:3609` — запись 199: 1 внутрисловное «--» — артефакт конвертации (sanscrit--franc)
- `02_gasuns-dhatu-PhD-text2.mdx:3613` — запись 205: 1 внутрисловное «--» — артефакт конвертации (Sanskrit--Wörterbuch)
- `02_gasuns-dhatu-PhD-text2.mdx:3615` — запись 206: 1 внутрисловное «--» — артефакт конвертации (Sanskrit--English)
- `02_gasuns-dhatu-PhD-text2.mdx:3629` — запись 274: 1 внутрисловное «--» — артефакт конвертации (English--Sanskrit)
- `02_gasuns-dhatu-PhD-text2.mdx:3631` — запись 280: 1 внутрисловное «--» — артефакт конвертации (Rig--veda)
- `02_gasuns-dhatu-PhD-text2.mdx:3643` — запись 365: 1 внутрисловное «--» — артефакт конвертации (Sanskrit--English)
- `02_gasuns-dhatu-PhD-text2.mdx:3653` — запись 378: 1 внутрисловное «--» — артефакт конвертации (I--IV)
- `02_gasuns-dhatu-PhD-text2.mdx:3659` — запись 392: 1 внутрисловное «--» — артефакт конвертации (Merriam--Webster)
- `02_gasuns-dhatu-PhD-text2.mdx:3663` — запись 395: 3 внутрисловных «--» — артефакт конвертации (Anglo--Saxon, Indo--European, it--English)
- `02_gasuns-dhatu-PhD-text2.mdx:3665` — запись 396: 2 внутрисловных «--» — артефакт конвертации (Indo--European, Sanskrit--English)
- `02_gasuns-dhatu-PhD-text2.mdx:3673` — запись 423: 27 внутрисловных «--» — артефакт конвертации (a--dravyagun, a--prayoga, a--roganida, a--tantra)
- `02_gasuns-dhatu-PhD-text2.mdx:3679` — запись 431: 1 внутрисловное «--» — артефакт конвертации (I--III)
- `02_gasuns-dhatu-PhD-text2.mdx:3691` — запись 458: 1 внутрисловное «--» — артефакт конвертации (Sanskrit--Wo)
- `02_gasuns-dhatu-PhD-text2.mdx:3701` — запись 480: 2 внутрисловных «--» — артефакт конвертации (Adrien--Maisonneuve, Sanskrit--Franśais)
- `02_gasuns-dhatu-PhD-text2.mdx:3705` — запись 501: 1 внутрисловное «--» — артефакт конвертации (Indo--European)
- `02_gasuns-dhatu-PhD-text2.mdx:3707` — запись 502: 1 внутрисловное «--» — артефакт конвертации (Arabisch--Deutsch)
- `02_gasuns-dhatu-PhD-text2.mdx:3709` — запись 503: 1 внутрисловное «--» — артефакт конвертации (Sanskrit--Sprache)
- `02_gasuns-dhatu-PhD-text2.mdx:3713` — запись 509: 1 внутрисловное «--» — артефакт конвертации (Verb--Forms)
- `02_gasuns-dhatu-PhD-text2.mdx:3729` — запись 131: 2 внутрисловных «--» — артефакт конвертации (Proto--Indo)
- `02_gasuns-dhatu-PhD-text2.mdx:3747` — запись 152: 1 внутрисловное «--» — артефакт конвертации (Indo--European)
- `02_gasuns-dhatu-PhD-text2.mdx:3751` — запись 156: 2 внутрисловных «--» — артефакт конвертации (indo--européenes, indo--européennes)
- `02_gasuns-dhatu-PhD-text2.mdx:3753` — запись 157: 2 внутрисловных «--» — артефакт конвертации (Adrien--Maisonneuve, indo--européen)
- `02_gasuns-dhatu-PhD-text2.mdx:3759` — запись 160: 1 внутрисловное «--» — артефакт конвертации (Root--based)
- `02_gasuns-dhatu-PhD-text2.mdx:3761` — запись 165: 1 внутрисловное «--» — артефакт конвертации (Indo--European)
- `02_gasuns-dhatu-PhD-text2.mdx:3805` — запись 222: 1 внутрисловное «--» — артефакт конвертации (Indo--European)
- `02_gasuns-dhatu-PhD-text2.mdx:3829` — запись 248: 1 внутрисловное «--» — артефакт конвертации (Prentice--Hall)
- `02_gasuns-dhatu-PhD-text2.mdx:3841` — запись 260: 1 внутрисловное «--» — артефакт конвертации (Indo--European)
- `02_gasuns-dhatu-PhD-text2.mdx:3889` — запись 311: 1 внутрисловное «--» — артефакт конвертации (Root--determinatives)
- `02_gasuns-dhatu-PhD-text2.mdx:3901` — запись 320: 1 внутрисловное «--» — артефакт конвертации (Indo--Européen)
- `02_gasuns-dhatu-PhD-text2.mdx:3903` — запись 321: 1 внутрисловное «--» — артефакт конвертации (Indo--Européen)
- `02_gasuns-dhatu-PhD-text2.mdx:3907` — запись 323: 1 внутрисловное «--» — артефакт конвертации (Indo--Européen)
- `02_gasuns-dhatu-PhD-text2.mdx:3909` — запись 324: 1 внутрисловное «--» — артефакт конвертации (indo--européen)
- `02_gasuns-dhatu-PhD-text2.mdx:3919` — запись 340: 1 внутрисловное «--» — артефакт конвертации (Historical--comparative)
- `02_gasuns-dhatu-PhD-text2.mdx:3931` — запись 347: 1 внутрисловное «--» — артефакт конвертации (indo--européennes)
- `02_gasuns-dhatu-PhD-text2.mdx:3939` — запись 355: 1 внутрисловное «--» — артефакт конвертации (Indo--European)
- `02_gasuns-dhatu-PhD-text2.mdx:3945` — запись 359: 2 внутрисловных «--» — артефакт конвертации (Afro--Asiatic, Indo--European)
- `02_gasuns-dhatu-PhD-text2.mdx:3955` — запись 386: 1 внутрисловное «--» — артефакт конвертации (indo--européennes)
- `02_gasuns-dhatu-PhD-text2.mdx:3961` — запись 390: 1 внутрисловное «--» — артефакт конвертации (Indo--European)
- `02_gasuns-dhatu-PhD-text2.mdx:3971` — запись 405: 1 внутрисловное «--» — артефакт конвертации (Indo--European)
- `02_gasuns-dhatu-PhD-text2.mdx:3973` — запись 406: 1 внутрисловное «--» — артефакт конвертации (Data--oriented)
- `02_gasuns-dhatu-PhD-text2.mdx:3985` — запись 419: 2 внутрисловных «--» — артефакт конвертации (Indo--Europea, Indo--European)
- `02_gasuns-dhatu-PhD-text2.mdx:3987` — запись 420: 1 внутрисловное «--» — артефакт конвертации (Indo--Germanischen)
- `02_gasuns-dhatu-PhD-text2.mdx:3991` — запись 428: 3 внутрисловных «--» — артефакт конвертации (Historisk--filosofiske, Indo--European)
- `02_gasuns-dhatu-PhD-text2.mdx:3993` — запись 430: 1 внутрисловное «--» — артефакт конвертации (Indo--European)
- `02_gasuns-dhatu-PhD-text2.mdx:4005` — запись 456: 1 внутрисловное «--» — артефакт конвертации (Indo--European)
- `02_gasuns-dhatu-PhD-text2.mdx:4023` — запись 491: 1 внутрисловное «--» — артефакт конвертации (Indo--Européen)
- `02_gasuns-dhatu-PhD-text2.mdx:4045` — запись 150: 1 внутрисловное «--» — артефакт конвертации (Paris--Liège)
- `02_gasuns-dhatu-PhD-text2.mdx:4053` — запись 166: 1 внутрисловное «--» — артефакт конвертации (Indo--Aryan)
- `02_gasuns-dhatu-PhD-text2.mdx:4059` — запись 179: 1 внутрисловное «--» — артефакт конвертации (Sanskrita--Sprache)
- `02_gasuns-dhatu-PhD-text2.mdx:4065` — запись 192: 1 внутрисловное «--» — артефакт конвертации (Quick--Reference)
- `02_gasuns-dhatu-PhD-text2.mdx:4069` — запись 194: 1 внутрисловное «--» — артефакт конвертации (Indo--arischen)
- `02_gasuns-dhatu-PhD-text2.mdx:4083` — запись 210: 1 внутрисловное «--» — артефакт конвертации (Indo--Arian)
- `02_gasuns-dhatu-PhD-text2.mdx:4091` — запись 214: 1 внутрисловное «--» — артефакт конвертации (indo--européenes)
- `02_gasuns-dhatu-PhD-text2.mdx:4111` — запись 244: 1 внутрисловное «--» — артефакт конвертации (K--Suffixes)
- `02_gasuns-dhatu-PhD-text2.mdx:4119` — запись 253: 1 внутрисловное «--» — артефакт конвертации (Sanskrit--Sprache)
- `02_gasuns-dhatu-PhD-text2.mdx:4131` — запись 278: 1 внутрисловное «--» — артефакт конвертации (Sanskrit--Verbum)
- `02_gasuns-dhatu-PhD-text2.mdx:4143` — запись 329: 1 внутрисловное «--» — артефакт конвертации (Indo--Aryan)
- `02_gasuns-dhatu-PhD-text2.mdx:4151` — запись 334: 1 внутрисловное «--» — артефакт конвертации (Sanskrit--Sprache)
- `02_gasuns-dhatu-PhD-text2.mdx:4157` — запись 351: 1 внутрисловное «--» — артефакт конвертации (Indo--Arian)
- `02_gasuns-dhatu-PhD-text2.mdx:4163` — запись 361: 2 внутрисловных «--» — артефакт конвертации (Cāndra--Vyākaraṇa, Philologisch--historische)
- `02_gasuns-dhatu-PhD-text2.mdx:4173` — запись 375: 1 внутрисловное «--» — артефакт конвертации (Indo--Aryan)
- `02_gasuns-dhatu-PhD-text2.mdx:4175` — запись 379: 1 внутрисловное «--» — артефакт конвертации (Grosscorpus--Sprache)
- `02_gasuns-dhatu-PhD-text2.mdx:4199` — запись 427: 3 внутрисловных «--» — артефакт конвертации (Zend--alphabets, Zend--avesta, Zend--sprache)
- `02_gasuns-dhatu-PhD-text2.mdx:4207` — запись 442: 2 внутрисловных «--» — артефакт конвертации (Sanskrit--Worterbuchs, St--Pétersbourg)
- `02_gasuns-dhatu-PhD-text2.mdx:4225` — запись 476: 1 внутрисловное «--» — артефакт конвертации (Sanskrit--Syntax)
- `02_gasuns-dhatu-PhD-text2.mdx:4233` — запись 481: 1 внутрисловное «--» — артефакт конвертации (Sanskrit--Sprache)
- `02_gasuns-dhatu-PhD-text2.mdx:4235` — запись 482: 2 внутрисловных «--» — артефакт конвертации (Devanagari--Ausgabe, Sanskrit--Kompendium)
- `02_gasuns-dhatu-PhD-text2.mdx:4245` — запись 495: 1 внутрисловное «--» — артефакт конвертации (Nordrhein--Westfälische)
- `02_gasuns-dhatu-PhD-text2.mdx:4259` — запись 516: 1 внутрисловное «--» — артефакт конвертации (Sanskrit--Philologie)
- `02_gasuns-dhatu-PhD-text2.mdx:4265` — запись 524: 1 внутрисловное «--» — артефакт конвертации (vyākaraṇa--śāstra)
- `02_gasuns-dhatu-PhD-text2.mdx:4277` — запись 279: 1 внутрисловное «--» — артефакт конвертации (Schulz--Kirchner)
- `02_gasuns-dhatu-PhD-text2.mdx:4281` — запись 303: 1 внутрисловное «--» — артефакт конвертации (Indo--European)
- `02_gasuns-dhatu-PhD-text2.mdx:4287` — запись 307: 2 внутрисловных «--» — артефакт конвертации (Indo--Aryan, Lexicon--directed)
- `02_gasuns-dhatu-PhD-text2.mdx:4293` — запись 319: 1 внутрисловное «--» — артефакт конвертации (indo--européen)
- `02_gasuns-dhatu-PhD-text2.mdx:4297` — запись 353: 2 внутрисловных «--» — артефакт конвертации (Proto--Indo)
- `02_gasuns-dhatu-PhD-text2.mdx:4303` — запись 382: 1 внутрисловное «--» — артефакт конвертации (Indo--Iranischen)
- `02_gasuns-dhatu-PhD-text2.mdx:4309` — запись 444: 1 внутрисловное «--» — артефакт конвертации (Saṅgaṇaka--yantrīyopayogāya)
- `02_gasuns-dhatu-PhD-text2.mdx:4315` — запись 490: 1 внутрисловное «--» — артефакт конвертации (Mother--language)
- `02_gasuns-dhatu-PhD-text2.mdx:4317` — запись 506: 1 внутрисловное «--» — артефакт конвертации (Atharva--Veda)
- `02_gasuns-dhatu-PhD-text2.mdx:4321` — запись 263: 1 внутрисловное «--» — артефакт конвертации (Sanskrit--Sprache)
- `02_gasuns-dhatu-PhD-text2.mdx:4323` — запись 268: 1 внутрисловное «--» — артефакт конвертации (Sanskrit--Sprache)
- `02_gasuns-dhatu-PhD-text2.mdx:4329` — запись 519: 2 внутрисловных «--» — артефакт конвертации (Dhātu--Pāṭha, Indo--European)

## `R3` — Ссылка разрешается только после нормализации (5)

> Основание: ГОСТ Р 7.0.5-2008, 6.2

- `02_gasuns-dhatu-PhD-text2.mdx:962` — ссылка [Curtius 1879] разрешается в библиографию только после нормализации (состав фамилий) — сверить вручную
- `02_gasuns-dhatu-PhD-text2.mdx:4424`, `02_gasuns-dhatu-PhD-text2.mdx:4425` — ссылка [Killingley 1995] разрешается в библиографию только после нормализации (состав фамилий) — сверить вручную
- `02_gasuns-dhatu-PhD-text2.mdx:4377` — ссылка [Stchoupak, Nitti, Luigia, Renou 1959] разрешается в библиографию только после нормализации (состав фамилий) — сверить вручную
- `02_gasuns-dhatu-PhD-text2.mdx:568` — ссылка [Арно 1991] разрешается в библиографию только после нормализации (состав фамилий) — сверить вручную
- `02_gasuns-dhatu-PhD-text2.mdx:1948` — ссылка [Катенина 1980] разрешается в библиографию только после нормализации (состав фамилий) — сверить вручную

## `R2` — Запись библиографии без ссылок в тексте (88)

> Основание: ГОСТ Р 7.0.100-2018, 4.2 — список содержит использованные источники

- `02_gasuns-dhatu-PhD-text2.mdx:3259` — запись 6 [Атхарваведа 1962-1965] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3261` — запись 79 [Мегхадхута 1969] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3265` — запись 94 [Рамаяна 1960-1975] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3271` — запись 77 [Марузо 1960] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3301` — запись 21 [Бурлак 2005] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3307` — запись 25 [Вяселева 2002] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3315` — запись 32 [Гийом 1992] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3323` — запись 39 [Дыбо, Старостин 2007] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3331` — запись 53 [Звегинцев 1964] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3335` — запись 57 [История отечественного... 1990] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3361` — запись 80 [Мейе 1938] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3367` — запись 84 [Основные направления... 1964] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3379` — запись 99 [Ромашко 1983] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3421` — запись 10 [Бархударов 1979] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3441` — запись 40 [Елизаренкова 1960] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3449` — запись 48 [Зализняк 2015] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3471` — запись 75 [Лихушина 2015] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3479` — запись 88 [Парибок 1983] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3487` — запись 106 [Тавастшерна 2009] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3497` — запись 17 [Бодуэн де Куртенэ 1963] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3519` — запись 142 [Aṣṭāṅgahṛdayasaṃhitā 1998] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3547` — запись 369 [Mahabharata 1919-1966] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3549` — запись 373 [Manusmṛti 1983] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3557` — запись 435 [Rig-Veda 1965] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3559` — запись 446 [Sastri 1900] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3561` — запись 449 [Sastri, Rangacharya 1984] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3563` — запись 450 [Sāyaṇa 1897] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3567` — запись 471 [Skandapurāṇa 2013] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3671` — запись 417 [Pokorny 1989] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3675` — запись 425 [Ramachandra Dīkshitar 1951-1955] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3715` — запись 512 [Wilkins 1815] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3731` — запись 132 [Anttila 1972] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3737` — запись 139 [Arens 1969] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3779` — запись 184 [Brosses 1765] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3781` — запись 186 [Brugmann 1885] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3783` — запись 187 [Brugmann 1890] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3785` — запись 188 [Brugmann 1906] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3791` — запись 197 [Bulletin des sciences 1828] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3799` — запись 215 [Carroll 1953] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3811` — запись 228 [Saussure 1922] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3813` — запись 229 [Saussure 1985] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3815` — запись 238 [Diderichsen 1976] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3819` — запись 240 [Dinneen 1967] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3829` — запись 248 [Elgin 1973] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3831` — запись 251 [Erhart 1993] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3843` — запись 261 [Fowler 1974] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3851` — запись 270 [Giles 1901] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3855` — запись 272 [Gleason 1955] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3871` — запись 295 [Hill 1969] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3873` — запись 296 [Hirt 1905] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3903` — запись 321 [Jucquois 1970b] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3909` — запись 324 [Jucquois 1973] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3913` — запись 330 [Katzner 2002] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3923` — запись 342 [Krahe 1943] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3933` — запись 348 [Langacker 1968] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3941` — запись 356 [Lehmann, Malkiel 1982] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3963` — запись 391 [Minnis 1971] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3969` — запись 403 [Nerlich 1990] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3971` — запись 405 [Nussbaum 2007] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3975` — запись 407 [Oertel 1901] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3977` — запись 413 [Pankow 2002] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:3985` — запись 419 [Polomé 1999] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4013` — запись 469 [Silverstein 1971] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4021` — запись 486 [Thomsen 1927] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4023` — запись 491 [Vanséveren, Descharneux, Dubuisson 2000] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4027` — запись 498 [Wartburg 1970] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4047` — запись 151 [Bechart 1979] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4059` — запись 179 [Bopp 1868] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4067` — запись 193 [Bucknell 2011] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4075` — запись 198 [Burnell 1875] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4077` — запись 207 [Cardona 1972] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4089` — запись 213 [Carey 1810] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4091` — запись 214 [Carnoy 1937] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4125` — запись 273 [Goldstücker 1965] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4139` — запись 304 [Houben 1996] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4145` — запись 331 [Kellens 1984] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4147` — запись 332 [Kellens 1995] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4149` — запись 333 [Kellogg 1876] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4159` — запись 352 [Lebedev 1801] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4173` — запись 375 [Masica 1991] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4179` — запись 393 [Monier--Williams 1846] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4191` — запись 410 [Oldenberg 1896] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4195` — запись 422 [Puri 1957] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4199` — запись 427 [Rask 1826] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4245` — запись 495 [Vogel 1999] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4255` — запись 511 [Wilkins 1808] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4259` — запись 516 [Windisch 1917] не цитируется в рукописи
- `02_gasuns-dhatu-PhD-text2.mdx:4309` — запись 444 [Saṅkā 2014] не цитируется в рукописи

## Воспроизведение

```
cd GasunsDhatu_2014/revision-2026 && python gost_bibliography_check.py
```

_Dr. Mārcis Gasūns_
