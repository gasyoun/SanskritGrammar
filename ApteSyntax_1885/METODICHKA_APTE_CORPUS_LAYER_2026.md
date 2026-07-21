# Методичка к Апте — корпусный слой: частотные полосы и живые примеры

_Created: 21-07-2026 · Last updated: 21-07-2026_

Раздел II методички-компаньона к V. S. Apte, *The Student's Guide to Sanskrit
Composition* (1885; рус. пер. Н. П. Лихушиной, 2021). Раздел I (комментарий точности):
[METODICHKA_APTE_KOMMENTARII_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/METODICHKA_APTE_KOMMENTARII_2026.md).
Слайс исполнения — [H1297](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1297-Fable_SanskritGrammar_metodichka-corpus-linked-kochergina-apte_19.07.26.md).

## Что это и как читать

Раздел I разбирает *правила* Апте — где они точны, а где завышены. Этот раздел
добавляет слой *слов*: каждой лемме, вокруг которой построен комментарий, — ее
частотную полосу в корпусе и одно засвидетельствованное предложение с русским
переводом. Там, где раздел I говорит «в корпусе лидирует другой падеж», здесь этот
падеж можно увидеть в живой фразе.

**Частотные полосы** (по рангу леммы `rank_all` в частотной таблице
[kosha lemma_frequency.tsv](https://github.com/gasyoun/kosha/blob/main/data/frequency/lemma_frequency.tsv),
построенной по Digital Corpus of Sanskrit О. Хельвига): **топ-100** — первая сотня
корпуса; **топ-1000** — первая тысяча; **редкое** — за ее пределами.[^1]

**Примеры** взяты из корпуса DCS-2026 (импорт conllu-разметки О. Хельвига,
[VisualDCS](https://github.com/gasyoun/VisualDCS), коммит источника `04e0778`); каждый
несет свой локус DCS и проверяем по корпусу. Русские переводы примеров выполнены
заново для этой методички (Fable 5, `claude-fable-5`; сверка регистра — по публичному
слою глоссария [SanskritRussian](https://github.com/gasyoun/SanskritRussian)) и ждут
визы автора.

**Правовая рамка слоя.** В печать идут только переводы, созданные для методички, либо
взятые из публичного слоя SanskritRussian; закрытые слои выравнивания при построении
раздела не открывались. Если для примера существует лишь закрытый перевод, пример
печатается на санскрите без перевода, с пометой «перевод в закрытом слое» (в текущей
редакции таких строк нет). Данные и сборка:
[corpus_layer/](https://github.com/gasyoun/SanskritGrammar/tree/main/ApteSyntax_1885/corpus_layer),
скрипт [scripts/build_corpus_layer.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_corpus_layer.py),
регресс — [tests/test_corpus_layer.py](https://github.com/gasyoun/SanskritGrammar/blob/main/tests/test_corpus_layer.py).

[^1]: Полоса считается по строке леммы в частотной таблице, а таблица ведется по
    написанию леммы — поэтому у омонимичных лемм (*hā* «увы» и *hā* «покидать»;
    *vara* «лучший» и *vara* «дар») полоса объединяет омонимы. Для таких строк полоса —
    верхняя оценка частоты именно того употребления, что стоит в примере.

---

## Занятие 3 — глаголы движения и падеж цели

Раздел I: винительный цели — правило на 86 %, не закон (APT-5/23). Первые пять
примеров показывают саму норму — винительный цели при *gam*, *yā*, *i*, *vraj*, *sṛ*;
пример *car* напоминает, что местный при глаголе движения — это место движения, а не
цель.

| Лемма | Полоса | Ранг | Пример | Локус DCS | Перевод |
|---|---|---|---|---|---|
| gam | топ-100 | 25 | tenāsau pañcatvam agamat | Hitopadeśa: Hitop, 2, 35.3 | оттого он и отошел к пяти началам [умер] |
| yā | топ-100 | 81 | sa eva nidhanaṃ yāti kīlotpāṭīva vānaraḥ | Hitopadeśa: Hitop, 2, 30.5 | тот и идет к гибели — как обезьяна, выдернувшая клин |
| i | топ-1000 | 307 | āsannataratām eti mṛtyur jantor dine dine | Hitopadeśa: Hitop, 4, 74 | день за днем смерть подходит к живому все ближе |
| car | топ-1000 | 176 | ajā siṃhaprasādena vane carati nirbhayam | Hitopadeśa: Hitop, 3, 13.2 | милостью льва коза бесстрашно бродит по лесу |
| vraj | топ-1000 | 642 | sa vināśaṃ vrajaty āśu sūcakāśucir eva ca | Manusmṛti: ManuS, 4, 71.2 | тот быстро идет к погибели, как и нечистый доносчик |
| sṛ | редкое | 3640 | tvaramāṇo janasthānaṃ sasārābhimukhas tadā | Rāmāyaṇa: Rām, Ār, 42, 21.2 | тогда, спеша, он устремился прямо к Джанастхане |
| dhāv | редкое | 1551 | rājā stenena gantavyo muktakeśena dhāvatā | Manusmṛti: ManuS, 8, 314 | вор должен бежать к царю с распущенными волосами |

## Занятие 7 — глаголы чувства

Пример *ruc* — хрестоматийный дательный (APT-20, корпус подтверждает); примеры *druh*
и *asūy* показывают, чем «дательный гнева» оборачивается в текстах: объект стоит в
винительном (APT-21, корпусный подъем дательного 0,91). *īrṣy* — родительный объекта
ревности из словарного примера дхармасутры.

| Лемма | Полоса | Ранг | Пример | Локус DCS | Перевод |
|---|---|---|---|---|---|
| ruc | редкое | 1463 | yad eva rocate yasmai bhavet tat tasya sundaram | Hitopadeśa: Hitop, 2, 53.3 | что кому нравится, то для того и прекрасно |
| krudh | топ-1000 | 416 | na jāne kruddhaḥ svāmī kiṃ vidhāsyati | Hitopadeśa: Hitop, 2, 85.14 | не знаю, что сделает разгневанный господин |
| druh | редкое | 4237 | sa mātā sa pitā jñeyas taṃ na druhyet kadācana | Manusmṛti: ManuS, 2, 144.2 | его следует чтить как мать и отца — ему пусть не вредит никогда |
| īrṣy | редкое | 35949 | idānīm evāhaṃ janaka strīṇām īrṣyāmi no purā | Āpastambadharmasūtra: ĀpDhS, 2, 13, 6.2 | лишь теперь, о Джанака, я ревную женщин — прежде нет |
| asūy | редкое | 8823 | asūyanti hi rājāno janān anṛtavādinaḥ | Mahābhārata: MBh, 4, 4, 13 | ведь цари негодуют на людей лживых |

В *taṃ na druhyet* и *janān asūyanti* объект гнева — винительный: то самое корпусное
большинство, которое панинийское правило дательного не обещает.

## Занятие 9 — «бросать» и «любить»

*apsu kṣipet* — местный цели при глаголе бросания: конструкция реальная, но редкая
(2,1 % косвенных аргументов, APT-18); *mukta-* напоминает, что *muc* чаще значит
«освобождать». *snihyed asyāṃ* — местный лица при глаголе чувства (APT-22).

| Лемма | Полоса | Ранг | Пример | Локус DCS | Перевод |
|---|---|---|---|---|---|
| kṣip | топ-1000 | 264 | gāṃ vipram ajam agniṃ vā prāśayed apsu vā kṣipet | Manusmṛti: ManuS, 3, 260.2 | пусть скормит корове, брахману, козе, огню — или бросит в воду |
| muc | топ-1000 | 162 | paśya mūṣikamitreṇa kapotā muktabandhanāḥ | Hitopadeśa: Hitop, 1, 53.4 | смотри: другом-мышью голуби освобождены от пут |
| snih | редкое | 4166 | tataś cāsyāṃ svayaṃ tasya cakṣuḥ snihyed asaṃśayam | Kathāsaritsāgara: KSS, 2, 3, 11.2 | и тогда его взгляд, без сомнения, сам потянется к ней с любовью |
| abhilaṣ | редкое | 4413 | etad bhavatām abhilaṣitam api sampannam | Hitopadeśa: Hitop, 1, 201.6 | вот и желание ваше исполнилось |
| anurañj | редкое | 3181 | anuraktaḥ śucir dakṣaḥ smṛtimān deśakālavit | Manusmṛti: ManuS, 7, 64 | преданный, честный, ловкий, памятливый, знающий место и время |

## Занятие 10 — «власть» и «память»

*īśate* и *prabhavati* — родительный объекта власти, как и учит Апте; *smarantī taṃ
bhartāram* — та самая корпусная норма «помнить + винительный», которой раздел I
поправил категоричное «управляют родительным» (винительный чаще в 1,4 раза, APT-19).

| Лемма | Полоса | Ранг | Пример | Локус DCS | Перевод |
|---|---|---|---|---|---|
| īś | редкое | 2491 | na kaścid īśate brahman svayaṃgrāhasya sattama | Mahābhārata: MBh, 3, 200, 22 | никто, о брахман, не властен над самовольным захватом |
| prabhū | редкое | 2142 | kathaṃ mṛtyuḥ prabhavati vedaśāstravidāṃ prabho | Manusmṛti: ManuS, 5, 2.2 | как смерть имеет власть над знатоками Вед, о владыка? |
| day | редкое | 9223 | dāmyata datta dayadhvam iti | Bṛhadāraṇyakopaniṣad: BĀU, 5, 2, 3.8 | «смиряйте себя, давайте, сострадайте» |
| smṛ | топ-1000 | 114 | smarantī taṃ ca bhartāraṃ muktakaṇṭhaṃ ruroda sā | Kathāsaritsāgara: KSS, 2, 1, 61.2 | вспоминая того мужа [вин.], она рыдала в голос |
| adhī | редкое | 1275 | mayā ca dharmaśāstrāṇi adhītāni | Hitopadeśa: Hitop, 1, 11 | и дхармашастры мною изучены |

Пример *day* — знаменитое «да-да-да» Брихадараньяка-упанишады: три императива, включая
*dayadhvam* «сострадайте».

## Занятие 22 — частица uta

Пример *uta* — целиком то разделительное «kim… uta…», о котором идет речь в APT-12:
частица открывает вторую половину альтернативного вопроса, а не стоит постпозитивно.

| Лемма | Полоса | Ранг | Пример | Локус DCS | Перевод |
|---|---|---|---|---|---|
| uta | топ-1000 | 363 | śṛṇu deva kim asmābhir baladarpād durgaṃ bhagnam uta tava pratāpādhiṣṭhitenopāyena | Hitopadeśa: Hitop, 4, 23 | слушай, государь: нами ли, в гордыне силы, взята крепость — или уловкой, опирающейся на твое величие? |
| kim | топ-1000 | 583 | śvā yadi kriyate rājā tat kiṃ nāśnāty upānaham | Hitopadeśa: Hitop, 3, 60.23 | если пса сделают царем — разве не станет он грызть сандалию? |

## Занятия 29–30 — назначение залога

*ramante* — Ātmanepada, как у 95 % форм *ram* (APT-26); *hanti* — Parasmaipada, как у
90 % форм *han* (APT-27); *krīḍan* — Parasmaipada глагола, который на деле распределен
почти поровну (57,6 / 42,4, APT-28): «обычно Parasmaipada» Апте здесь — завышение.

| Лемма | Полоса | Ранг | Пример | Локус DCS | Перевод |
|---|---|---|---|---|---|
| krīḍ | редкое | 1576 | tatra balavān vānarayūthaḥ krīḍann āgataḥ | Hitopadeśa: Hitop, 2, 31.5 | туда, резвясь, пришла сильная обезьянья стая |
| ram | топ-1000 | 495 | vaktā śrotā ca yatrāsti ramante tatra sampadaḥ | Hitopadeśa: Hitop, 2, 135.3 | где есть говорящий и слушающий, там обитают богатства |
| han | топ-100 | 55 | ekaś candramās tamo hanti na ca tārāgaṇair api | Hitopadeśa: Hitop, 0, 18.3 | одна луна разгоняет тьму — не [сделать этого] и сонмам звезд |

## Приложение — словарь частиц

Единственная зона книги без единого сбоя (APT-32..39). Полосы показывают, почему:
это высокочастотный костяк связной речи — *punar* и *varam* в топ-100, остальные в
первой тысяче.

| Лемма | Полоса | Ранг | Пример | Локус DCS | Перевод |
|---|---|---|---|---|---|
| punar | топ-100 | 39 | punar na tatra gamiṣyāmi | Hitopadeśa: Hitop, 3, 17.6 | снова туда не пойду |
| prāyas | редкое | 2205 | prāyaḥ samāpannavipattikāle dhiyo 'pi puṃsāṃ malinā bhavanti | Hitopadeśa: Hitop, 1, 28.3 | обычно в час нагрянувшей беды даже разум людей мутнеет |
| muhur | топ-1000 | 652 | suṣeṇaṃ tāḍayāmāsa nanāda ca muhur muhuḥ | Rāmāyaṇa: Rām, Yu, 33, 35.2 | он ударил Сушену и взревел снова и снова |
| yatas | топ-1000 | 366 | yato rājadharmaś caiṣaḥ | Hitopadeśa: Hitop, 3, 64 | ибо таков и долг царя |
| yāvat | топ-1000 | 172 | tāvad bhayasya bhetavyaṃ yāvad bhayam anāgatam | Hitopadeśa: Hitop, 1, 57.9 | бояться беды следует [лишь] до тех пор, пока беда не пришла |
| hā | топ-1000 | 190 | hā hā putraka nādhītaṃ gatāsv etāsu rātriṣu | Hitopadeśa: Hitop, 0, 24 | увы, увы, сынок: ничего не выучено за эти ушедшие ночи |
| vara | топ-100 | 82 | varam eko guṇī putro na ca mūrkhaśatair api | Hitopadeśa: Hitop, 0, 18.2 | лучше один достойный сын — и ни к чему даже сотни глупцов |

*varam eko guṇī putro na ca…* — живой образец конструкции *varaṃ… na* «лучше X, чем Y»
(APT-39); *hā hā putraka* — плач из вступления «Хитопадеши», первого текста, где
учащийся встретит это междометие.

---

_Раздел II методички. Числа полос воспроизводимы скриптом
[scripts/build_corpus_layer.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_corpus_layer.py)
из [corpus_layer/corpus_layer.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/corpus_layer/corpus_layer.tsv);
корпусные данные — Digital Corpus of Sanskrit (О. Хельвиг). Перед печатью —
[/publish-safety-check](https://github.com/gasyoun/claude-config/blob/main/commands/publish-safety-check.md)._

_Dr. Mārcis Gasūns_
