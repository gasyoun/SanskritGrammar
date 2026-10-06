I'll verify this by reading the actual files. Let me start by locating the key files.
Let me read the Buhler lesson XVI section and the claims file in parallel.
Item 1 verified against the source. Now the claims.
Now the concordance topics and the crosswalk CSV.
Let me find the lesson XVI section of topics.yml.
Now let me verify the CSV rows for lesson I correction (rakṣ 613, jīv 260) and the typed links file.
Now the witness files. Let me grep the claimed strings.
Let me confirm section/lesson numbering for the Zalizniak and Kochergina loci.
Let me rigorously count the XVI anchor rows and confirm no others exist.
All checks executed against the actual files. Verdict below.

**1. Локусы урока XVI в `BuhlerLeitfaden_1923/Buhler_Unicode.mdx` (строки 2071–2196)** — ✅ **OK, дословно**
- (a) строка 2073: «Optativus (Potentials) образуется от основы наст. вр. посредством присоединения ī, за которым следуют окончания имперфекта… вместо окончания an появляется uḥ (r). С конечным a основы наст. вр. I, IV, VI и X классов оптативный ī сливается в e.» ✓
- (b) строка 2087: «Optativus обыкновенно выражает возможность, желание или приказание; он также имеет значение и будущего времени.» ✓
- (c) строка 2089: «…обращают свое ṛ в N. V. Du. pl. и Асc. sing., du. в guṇa вместо vṛddhi. nṛ кроме того образует в Gen. pl. nṛṇām или nṝṇām.» ✓
- (d) строка 2108: «Существительные на o; go f. m. корова или бык.» ✓ (урок XVII начинается строкой 2197 — диапазон 2071–2196 точен)

**2. claims.yml HB-23/24/25/130/131** — ✅ **OK**
Все `loc: "Урок XVI…"`, все пять `verdict_fact: TRUE`. `claim_ru` дословно покрывает: HB-23+HB-130 → 1a; HB-24 → 1b; HB-25+HB-131 → 1c. Примеры: HB-23 «…присоединения ī… вместо окончания an появляется uḥ (r)»; HB-131 «nṛ кроме того образует в Gen. pl. nṛṇām или nṝṇām.»
⚠️ Мелкое замечание (не влияет на вердикт): у HB-24 loc стоит `line 2085`, у HB-25/HB-131 — `line 2087`, тогда как §2 фактически на 2087, §3 на 2089 (сдвиг −2 строки, локус остаётся внутри XVI).

**3. topics.yml, XVI / lesson-roots vs crosswalk CSV** — ✅ **OK, 5/5**
- car: `A₁ (conf medium)` → `R₂ (z-series)` + `R? (index-unknown)` — CSV строки с `220,car,,move,A₁…R?` и `…R₂` ✓
- man: N₁/N₁ (`546,man,,think,N₁…N₁`) ✓
- mud: U₁/U₁ (`566,mud,,be merry,U₁…U₁`) ✓
- śaṃs: A₁/A₁, две строки (`766,śaṃs,,praise,A₁…A₁` ×2) ✓
- smṛ: R₁/R₁ (`894,smṛ,,remember,R₁…R₁`) ✓
Покрытие 5/5 (все корни урока присутствуют).

**4. Правка урока I (śaṃs 766, rakṣ 613, jīv 260 → «yes»)** — ✅ **OK**
- CSV стр. 107: `613,rakṣ,,protect,A₁,medium…`; стр. 380: `260,jīv,,live,I₂,high…`; стр. 526–527: `766,śaṃs,,praise,A₁,medium…` (две строки). Все три строки реально есть.

**5. Свидетели** — ✅ **OK (все 4)**
- (a) Zalizniak §115 (`<span id="s115">`, стр. 1870): «…В оптативе между основой (первичной, § 27) и окончаниями выступает суффикс ī (а + ī → e…)»; §122 (`id="s122"`, стр. 2000): «…выступает суффикс yā/ī…» ✓
- (b) §99 (`id="s99"`, стр. 1602): «2. С чередованием ступеней: go- (m, f) *бык, корова*…» ✓
- (c) Kochergina Занятие XII (с 2287): стр. 2310 «…-a- + -ī- → e.»; стр. 2295 «Optativus в санскрите употребляется для выражения:»; Занятие XIX (с 4531): стр. 4558 «а имена родства - в ступени guṇa (a)» ✓
- (d) Knauer `Frazy-Knauer-03.05.2023.mdx`: стр. 42 «गोः क्षीरेण शिशवो मोदन्ताम्» и «हे स्वसः पित्रोर्गृहे तिष्ठेः», стр. 90 «हे शिशवः पितॄन्सेवध्वं भ्रातॄणां स्निह्यत» ✓

**6. typed_link_buhler_lessons.tsv** — ✅ **OK**
Ровно 22 строки с `anchor_id`, начинающимся `buhler-topic:XVI.`: optative 8, optative-semantics 4, r-stems-kinship 5, go-stems 3, lesson-roots 2. Все пять якорей имеют одноимённые темы в topics.yml (ключи XVI: optative, optative-semantics, r-stems-kinship, go-stems, lesson-roots).

---

**OVERALL: PASS** — все 6 пунктов подтверждены по первоисточникам; единственное замечание — незначительный сдвиг (−2 строки) в полях `loc` клеймов HB-24/HB-25/HB-131, локус урока при этом верен.
