# H5690 — урок XXXIX: свежепроцессный спот-чек — 08-10-2026

_Repo: gasyoun/SanskritGrammar · Worker: OxAlpha (opencode/z-ai/glm-5.3-flash)_

Метод: независимый fresh-process прогон (не тот процесс, что генератор) — все спот-фразы
XXXIX против живых файлов источников; 9 HB-утверждений урока против фактических строк
Buhler_Unicode.mdx; reuse-находка токен-в-токен; смонтированная секция каталога.
DeepSeek-лейн — auth-store без ключа на боксе (20-й прецедент серии H5676→H5699) →
фолбэк свежепроцессной верификации по прецеденту серии.

## Результат: 13/13 PASS

- Споты против источников: kochergina «ghnanti, aghnan, ghnantu» PASS;
  kochergina «dvéṣṭi/dviṣṭé - II» (Приложение II) PASS; knauer «na kaçcid vetti» PASS;
  knauer «dviṣmas tam ebhir mantrair hanāma» PASS; z-1978 «√vaç *желать* (vaç-/uç-)» PASS;
  z-1978 «У неполноизменяемых корней, например, √ad» PASS; dhatu «Идея Зализняка проста
  и мощна» PASS; sangram thematic-present «атематические классы концентрируются именно в» PASS.
- 9 HB (HB-299…307) против фактических строк mdx: §6=5649, парадигма=5651, §7=5653,
  3pl-дефектность=5669, §8=5671, veda=5703, §10=5753, īś=5785, vaś=5787, mṛj=5789 — все тексты
  утверждений PASS. NB: registry loc-строки HB-299…307 систематически −2 от фактических
  (mdx правился после минта реестра) — контент верен, локусы устарели; @DO-остаток заведён в GTD.
- Reuse-находка: деванагари mdx 5853 содержит द्विष्मस्तमेभिर्मन्त्रैर्हनाम, Knauer Nr.11 п.5 —
  «dviṣmas tam ebhir mantrair hanāma» токен-в-токен PASS.
- Catalog: заголовок урока, 5 тем, споты в :~:text-фрагментах (URL-encoded), бэклинк «УРОК XXXIX»
  в src/lesson-backlinks.json — PASS.

## Гон

`python3 scripts/build_lesson_concordance.py` — PASS (spots 489 local OK / 34 external);
`typed_link_lint.py` — OK all clean; 20 TSV-строк XXXIX; 42 урока / 785 строк.

_Гасунс_
