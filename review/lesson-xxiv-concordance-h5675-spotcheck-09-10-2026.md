# H5675 — спот-чек урока XXIV (свежепроцессная независимая верификация)

_Дата: 09-10-2026 · executor: OxAlpha (opencode/z-ai/glm-5.3-flash) · хендофф: [H5675](https://github.com/gasyoun/Uprava/blob/main/handoffs/H5675-OxAlpha_SanskritGrammar_buhler-concordance-XXIV_02.10.26.md)_

DeepSeek-лейн — без ключа на боксе (24-й прецедент серии H5659→H5674; на боксе только openrouter-алиас модели, прямого API-ключа нет) → фолбэк по прецеденту: независимая свежепроцессная проверка (отдельный python-процесс вне репо, re-read сырых файлов, не переиспользует состояние build).

Скоуп: 13 локальных спот-фраз байт-в-байт (4 файла-источника) + 2 негативных проба, 19 TSV-строк × 10 колонок × дата, каталог (заголовок/5 тем/исключения ×5/45 уроков), backlinks (knauer ≥3 / kochergina ≥3), crosswalk csv-парсером (chid=I₁ ×1, mṛj=R₁ ×1, vij=I₁ ×1, varṇ NO-negative + ловушка vṛ-гомонимов, han present), claims.yml 7/7 HB-176…182 + 7/7 loci «Урок XXIV», вердикты 5/5 с 4-свидетельскими ключами, reuse-кластеры matches.json (2 exact: 523↔7.143, 533↔6.125).

Первичные прогоны: 3 дефекта чекера подряд (прецедент H5674: FAIL первичного = дефект чекера, не данных) — (1) негативный проба «\*śrīmantī» матчил собственное упоминание never-формы в topics.yml; (2) колонка CSV — `ryad_derived`, не `ryad_1975`; (3) проба «śrīmantī только в negated-форме» — префикс «не \*» с астериском не матчился срезом 4 символов. Финальный прогон: **61 PASS / 0 FAIL — дефектов данных нет** (прецедент H5687).

```
PASS  spot ZalizniakOcherk «в N.V.A.du n keçavatī…»
PASS  spot ZalizniakOcherk «склоняется как keçavant-, но bhavant-…»
PASS  spot ZalizniakOcherk «в слабейших формах a перед n сохраняется…»
PASS  spot ZalizniakOcherk «Конечные k, ṭ, t, p озвончаются перед всяк…»
PASS  spot KocherginaUchebnik «имеют сильную основу на -ant и слабую ос…»
PASS  spot KocherginaUchebnik «при вежливом обращении - в N. sg. *m* имее…»
PASS  spot KocherginaUchebnik «и другие на -man и -van в слабых формах со…»
PASS  spot KocherginaUchebnik «Конечные k, ṭ, t и p озвончаются перед гла…»
PASS  spot KnauerFrazy «bhṛtyā balavantaṁ rājānam āyuṣmann…»
PASS  spot KnauerFrazy «māsān bhavān…»
PASS  spot KnauerFrazy «ब्रह्मा जगतः स्रष्टा वेदेषु श्रूयते…»
PASS  spot sangram consonant-stems «`rājan`, `ātman`, `karman`, `brahman`…»
PASS  spot GasunsDhatu «Идея Зализняка проста и мощна…»
PASS  negative probe «dhīmantī» in kochergina IS present (witness drift — ожидаемо)
PASS  negative probe «śrīmantī» only in negated form («не *śrīmantī»)
PASS  TSV XXIV rows == 19
PASS  TSV XXIV all 10 columns
PASS  TSV XXIV 5 topic anchors
PASS  TSV XXIV date 09-10-2026
PASS  TSV header == TYPE_D_RECORD_FIELDS shape (10)
PASS  catalog has Урок XXIV header
PASS  catalog XXIV.mant-vat-yat-stems content
PASS  catalog XXIV.bhavat-honorific content
PASS  catalog XXIV.an-man-van-stems content
PASS  catalog XXIV.sandhi-voiced-mutes content
PASS  catalog XXIV.lesson-roots content
PASS  catalog 45 lessons marker
PASS  catalog XXIV exceptions blocks == 5
PASS  backlinks knauer XXIV rows >= 3
PASS  backlinks kochergina XXIV rows >= 3
PASS  crosswalk chid == 1 row (I₁)
PASS  crosswalk mṛj == 1 row (R₁)
PASS  crosswalk vij == 1 row (I₁)
PASS  crosswalk varṇ absent (denom — correct NO)
PASS  crosswalk trap: vṛ present as homonyms (NOT varṇ)
PASS  crosswalk han present (vocab-derived hantar note)
PASS  claims.yml has HB-176 … HB-182 (7/7)
PASS  claims.yml Урок XXIV loci == 7
PASS  verdict XXIV.* non-empty × 5
PASS  verdict XXIV.* 4-witness keys × 5
PASS  matches.json XXIV == 2 exact (523↔knauer-1908.7.143, 533↔knauer-1908.6.125)

TOTAL: 61 PASS / 0 FAIL (local spots 13, checker defects runs 1–3: 3 — чекер, не данные)
```
