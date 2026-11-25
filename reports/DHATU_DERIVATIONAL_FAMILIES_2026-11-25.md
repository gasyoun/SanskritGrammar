# Деривационные гнёзда dhātu: размер против частотности (25-11-2026)

_Created: 25-11-2026 · Last updated: 25-11-2026_
_к.ф.н. М.Ю. Гасунс_

H6256 · OxAlpha (MiMo v2.6 Flash, `ollama-cloud/mimo-v2.6-flash`) · датасет и отчёт в csl-observatory-формате: [families.json](https://github.com/gasyoun/SanskritGrammar/blob/main/data/dhatu_families/families.json), [families.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/data/dhatu_families/families.tsv), [root_stats.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/data/dhatu_families/root_stats.tsv). Скрипт: [build_dhatu_families.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_dhatu_families.py).

## Что построено

Гнёздо = канонический dhātu (SLP1) → множество substantives (существительные / прилагательные / неизменяемые), приписанных ему MW-деривационными данными. Это НЕ парность dhatupatha-источников (H4741 / Q4.4): структуру дают [MWderivations](https://github.com/gasyoun/MWderivations) + MW, а частоты — [DCS lemma frequency](https://github.com/gasyoun/kosha/blob/main/data/frequency/lemma_frequency.tsv).

| Канал (все из MW / MWderivations) | Ребёр |
|---|---:|
| `mw_pfxderiv` | 10,107 |
| `mw_etymology` | 8,308 |
| `root_oracle[mw]` | 7,818 |
| `mw_deriv` | 4,819 |
| `analysis2_decomp` | 4,305 |

## Покрытие

| Метрика | Значение |
|---|---:|
| Корней в инвентаре (канонический dhātu + MW) | 5,745 |
| Из них в строгом множестве атрибуции (MW genuineroot без upasarga) | 701 |
| Корней с >=1 производным | 608 |
| Корней с >=5 производными | 500 |
| Уникальных производных | 23,545 |
| Производных с частотой DCS > 0 | 11,742 |
| Доля производных с DCS-частотой | 49.9% |
| Суммарных рёбер root→derivative | 24,353 |

## Распределение размеров гнёзд против корпусной частотности

| Размер гнезда | Корней | Доля корней | Производных | Есть в DCS | Медиана токенов гнезда | Медиана log10(1+частота) |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 5,137 | 89.4% | 0 | 0.0% | 0 | 0.00 |
| 1 | 30 | 0.5% | 30 | 36.7% | 0 | 0.00 |
| 2–3 | 53 | 0.9% | 133 | 45.1% | 20 | 0.30 |
| 4–7 | 81 | 1.4% | 432 | 44.9% | 59 | 0.15 |
| 8–15 | 120 | 2.1% | 1,324 | 49.0% | 228 | 0.15 |
| 16–31 | 113 | 2.0% | 2,572 | 52.0% | 772 | 0.15 |
| 32+ | 211 | 3.7% | 19,862 | 50.8% | 4,641 | 0.30 |

Zipf-подобие: наклон log10(count) ~ log10(rank) по всем 11,742 произведениям, встреченным в DCS — **-1.971** (эталон ~−1). Spearman ρ между размером гнезда и суммарной частотой гнезда — **0.831** (n=608 корней с хотя бы одним производным).

## Крупнейшие гнёзда

| Корень (IAST) | Размер | В DCS | Токенов DCS | Пример производного (IAST) |
|---|---:|---:|---:|---|
| kṛ (`kf`) | 943 | 476 | 180,484 | kṛ |
| bhū (`BU`) | 668 | 245 | 82,355 | bhū |
| dhā (`DA`) | 404 | 216 | 30,034 | vidhi |
| kṛt (`kft`) | 371 | 101 | 5,160 | kṛt |
| śrī (`SrI`) | 365 | 88 | 5,747 | śrī |
| han (`han`) | 348 | 130 | 26,101 | han |
| hṛ (`hf`) | 320 | 183 | 16,283 | hṛ |
| sad (`sad`) | 306 | 115 | 7,295 | prasāda |
| vṛt (`vft`) | 262 | 143 | 17,083 | vrata |
| vid (`vid`) | 262 | 72 | 14,259 | vid |
| i (`i`) | 252 | 149 | 123,788 | eva |
| gam (`gam`) | 241 | 148 | 50,055 | gam |
| nī (`nI`) | 237 | 109 | 18,433 | loka |
| sthā (`sTA`) | 232 | 127 | 37,705 | sthā |
| dā (`dA`) | 217 | 104 | 57,102 | ādi |
| car (`car`) | 207 | 118 | 14,591 | vrata |
| vas (`vas`) | 198 | 113 | 15,983 | deśa |
| yā (`yA`) | 198 | 112 | 17,136 | yā |
| pad (`pad`) | 195 | 103 | 17,425 | pāda |
| bhuj (`Buj`) | 193 | 83 | 7,560 | bhuj |

## Канари: 10 корней, сверенных с MW вручную

Строки — [canary_10.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/data/dhatu_families/canary_10.tsv); 10 корней выбраны равноотстоящими по алфавиту среди корней с явной MW-атрибуцией `fr. √ root` у substantives; сниппет взят из СЫРОЙ записи `mw.txt` с тем же `L`, что и атрибуция в `mw_etymology.tsv`.

| Корень | Производное | MW L | Сниппет MW | Вердикт | Примечание |
|---|---|---|---|---|---|
| āp (`Ap`) | āpra | 25098 | &lt;hom&gt;1.&lt;/hom&gt; &lt;s&gt;Apra/&lt;/s&gt; ¦ &lt;lex&gt;mfn.&lt;/lex&gt; (&lt;ab&gt;fr.&lt;/ab&gt; √ &lt;hom&gt;1.&lt;/hom&gt; &lt;s&gt;Ap&lt;/s&gt;, &lt;ls&gt;Sāy.&lt;/ls&gt; on &lt;ls&gt;RV. i, 132, 2&lt;/ls&gt;), getting at [enemies in order to kill them] (?)&lt;info lex="m:f:n"/&gt; | AGREE | MW L25098: `<lex>mfn.</lex> (fr. √ 1. Ap)` — прямое совпадение, substantivum |
| śṝ (`SF`) | śīrṇa | 218551 | &lt;s&gt;SIrRa/&lt;/s&gt; ¦ &lt;lex&gt;mfn.&lt;/lex&gt; (&lt;ab&gt;fr.&lt;/ab&gt; √ &lt;s&gt;SF&lt;/s&gt;) broken or rent asunder, shivered, crushed, shattered, injured, &lt;ls&gt;ŚBr.&lt;/ls&gt; &amp;c. &amp;c.&lt;info lex="m:f:n"/&gt;&lt;info hui="a"/&gt; | AGREE | MW L218551: `<lex>mfn.</lex> (fr. √ SF)` — прямое совпадение |
| ac (`ac`) | vyac | 208354 | &lt;hom&gt;1.&lt;/hom&gt; &lt;s&gt;vyac&lt;/s&gt; ¦ (&lt;ab&gt;cf.&lt;/ab&gt; √ &lt;s&gt;vic&lt;/s&gt;; &lt;ab&gt;prob.&lt;/ab&gt; &lt;ab&gt;orig.&lt;/ab&gt; identical with &lt;hom&gt;2.&lt;/hom&gt; &lt;s&gt;vy-√ ac&lt;/s&gt;) &lt;ab&gt;cl.&lt;/ab&gt; 6. &lt;ab&gt;P.&lt;/ab&gt; (&lt;ls&gt;Dhātup. xxviii, 12&lt;/ls&gt;) &lt;s&gt;vicati&lt;/s&gt; (only in &lt;ab&gt;cl.&lt;/ab&gt; 3. &lt;ab&gt;pr.&lt;/ab&gt; &lt;s&gt;vivyakti&lt;/s&gt;, 3. &lt;ab&gt;du.&lt;/ab&gt; &lt;s&gt;vivikta/s&lt;/s&gt;, &lt;ab&gt;Subj | DISCREPANCY | MW L208354: запись ГЛАГОЛ cl.6 P.; корень ac взят из кросс-ссылки `prob. orig. identical with vy-√ ac` (MW же сравнивает с √ vic), а не из деривации substantivum; форма vyac просочилась в analysis2 как омоним |
| dyut (`dyut`) | ādyota | 24085 | &lt;s&gt;A-dyota&lt;/s&gt; ¦ &lt;lex&gt;m.&lt;/lex&gt; (&lt;ab&gt;fr.&lt;/ab&gt; √ &lt;hom&gt;1.&lt;/hom&gt; &lt;s&gt;dyut&lt;/s&gt;), light, brilliance, &lt;ls&gt;L.&lt;/ls&gt;&lt;info lex="m"/&gt; | AGREE | MW L24085: `<lex>m.</lex> (fr. √ 1. dyut)` — прямое совпадение |
| kāṅkṣ (`kANkz`) | vikāṅkṣā | 192892 | &lt;s&gt;vi—kANkza&lt;/s&gt; ¦ (&lt;ls&gt;MBh.&lt;/ls&gt;) &lt;lex&gt;mfn.&lt;/lex&gt; free from desire&lt;info lex="m:f:n"/&gt; | DISCREPANCY | MW L192892 даёт `<lex>mfn.</lex> vi—kANkza` (без долгого ā), а в TSV атрибуции headword = `vikANkzA`; несовпадение поверхности, root kANkz правдоподобен, но нужна нормализация key1 |
| lih (`lih`) | avaleha | 18081 | &lt;s&gt;ava-leha&lt;/s&gt; ¦ &amp;c. See &lt;s&gt;ava-√ lih&lt;/s&gt;.&lt;info hui="b"/&gt; | WEAK-EVIDENCE | MW L18081: только кросс-ссылка `See ava-√ lih`, без `<lex>` и без явного `(fr. √)`; корень выведен из префигированного глагола, не из substantivum |
| muṣ (`muz`) | āmoṣa | 25610 | &lt;s&gt;A-moza&lt;/s&gt; ¦ &amp;c. See under &lt;s&gt;A-√ muz&lt;/s&gt;.&lt;info hui="b"/&gt; | WEAK-EVIDENCE | MW L25610: только `See under A-√ muz`, без `<lex>`; атрибуция слабая, форма Amoza в MW — кросс-ссылка |
| raṇ (`raR`) | virāṇin | 199262 | &lt;s&gt;vi-rARin&lt;/s&gt; ¦ See under &lt;s&gt;vi-√ raR&lt;/s&gt;.&lt;info hui="b"/&gt; | WEAK-EVIDENCE | MW L199262: только `See under vi-√ raR`, без `<lex>`; то же, что у muz |
| siv (`siv`) | sūci | 251025 | &lt;s&gt;sUci&lt;/s&gt; or &lt;s&gt;sUcI/&lt;/s&gt;, ¦ &lt;lex&gt;f.&lt;/lex&gt; (&lt;ab&gt;prob.&lt;/ab&gt; to be connected with &lt;s&gt;sUtra&lt;/s&gt;, &lt;s&gt;syUta&lt;/s&gt; &amp;c. &lt;ab&gt;fr.&lt;/ab&gt; √ &lt;s&gt;siv&lt;/s&gt;, ‘to sew’, &lt;ab&gt;cf.&lt;/ab&gt; &lt;s&gt;sUkzma&lt;/s&gt;; in &lt;ls&gt;R.&lt;/ls&gt; once &lt;s&gt;sUcinA&lt;/s&gt; &lt;ab&gt;instr.&lt;/ab&gt;), a needle or any sharp-pointed instrument (&lt;ab&gt;e.g.&lt;/ab&gt; ‘a needle used | AGREE-HEDGED | MW L251025: `<lex>f.</lex> sUci ... (prob. ... fr. √ siv)` — MW сам помечает гипотезу `prob.`, но корень указан явно |
| vai (`vE`) | upavāta | 35782 | &lt;hom&gt;1.&lt;/hom&gt; &lt;s&gt;u/pa-vAta&lt;/s&gt; ¦ (for &lt;hom&gt;2.&lt;/hom&gt; See &lt;s&gt;upa-√ vE&lt;/s&gt;) &lt;lex&gt;mfn.&lt;/lex&gt; blown upon, &lt;ls&gt;ŚBr. iv, 1, 3, 7.&lt;/ls&gt;&lt;info lex="m:f:n"/&gt; | DISCREPANCY | MW L35782: upavAta `blown upon` — это √vA (`vA`), а ссылка `upa-√ vE` в записи относится ко ВТОРОМУ омониму (`for hom. 2. See ...`); атрибуция vE ошибочна |

Итог ручной сверки: AGREE — 4, DISCREPANCY — 3, WEAK — 3. Расхождения и слабые случаи оставлены в датасете с исходными тегами — это честная оценка точности канала `mw_etymology`, а не скрытая чистка.

## Ограничения

- Инвентарь датасета — 5,745 канонических dhātu (vidyut + m4 + MW + local); атрибуция производных идёт только по строгому множеству MW `genuineroot` без upasarg (чтобы `su-`, `pra-`, `vi-` не создавали гигантские ложные гнёзда). Остальные корни остаются гнёздом размера 0 — покрытие измеряется явно.
- Все каналы требуют, чтобы производное присутствовало в `analysis2.txt` (то есть было substantivum в MWderivations), так что глагольные формы и не-substantive записи MW в гнёзда не попадают.
- Частоты — лемматизированного DCS-conllu (5.7M токенов); `count_all=0` означает не отсутствие слова в языке, а отсутствие в выборке DCS.
- Атрибуция по `analysis2_decomp` требует точного совпадения компонента разбора с каноническим корнем (длина ≥2), чтобы не путать префиксы `a`, `na` с корнями.
- Разные каналы могут приписать одну форму двум корням (омонимия корней); такие ребра сохранены с обоими тегами и видимы в `families.tsv`.
