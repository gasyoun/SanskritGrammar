# Методичка к Кочергиной — корпусный слой: частотные полосы и живые примеры

_Created: 21-07-2026 · Last updated: 21-07-2026_

Раздел IV методички-компаньона к В. А. Кочергиной, *Учебник санскрита* (план издания:
[METODICHKA_KOCHERGINA_COMPANION_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_COMPANION_2026.md);
разделы I–III: [комментарий](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_V1_KOMMENTARII_2026.md) ·
[упражнения](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_V1_UPRAZHNENIIA_2026.md) ·
[отсылки](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_V1_OTSYLKI_2026.md)).
Слайс исполнения — [H1297](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1297-Fable_SanskritGrammar_metodichka-corpus-linked-kochergina-apte_19.07.26.md).

## Что это и как читать

Разделы I–III комментируют *правила* Кочергиной. Этот раздел добавляет к ним слой
*слов*: для каждой леммы, на которой держится комментарий раздела I, — ее частотная
полоса в корпусе и одно живое, засвидетельствованное предложение с русским переводом.
Смысл слоя тот же, что у всей методички: показать не «что бывает в грамматике», а что
учащийся реально встретит в текстах.

**Частотные полосы** (по рангу леммы `rank_all` в частотной таблице
[kosha lemma_frequency.tsv](https://github.com/gasyoun/kosha/blob/main/data/frequency/lemma_frequency.tsv),
построенной по Digital Corpus of Sanskrit О. Хельвига):

- **топ-100** — лемма входит в первую сотню корпуса: встретится в первых же текстах;
- **топ-1000** — первая тысяча: надежный актив первого года чтения;
- **редкое** — за пределами первой тысячи: узнавать, но не заучивать первым.

**Примеры** взяты из корпуса DCS-2026 (импорт conllu-разметки О. Хельвига,
[VisualDCS](https://github.com/gasyoun/VisualDCS), коммит источника `04e0778`); каждый
пример несет свой локус DCS (текст, глава, номер предложения) и может быть проверен по
корпусу. Предпочтение отдано текстам, которые русскоязычный учащийся откроет первыми:
«Хитопадеша», «Манусмрити», «Рамаяна», эпос. Русские переводы примеров выполнены
заново для этой методички (Fable 5, `claude-fable-5`; сверка регистра — по публичному
слою глоссария [SanskritRussian](https://github.com/gasyoun/SanskritRussian)) и ждут
визы автора, как и весь текст методички.

**Правовая рамка слоя.** В печать идут только переводы, созданные для методички, либо
взятые из публичного слоя SanskritRussian. Закрытые слои выравнивания при построении
раздела не открывались; если для примера существует лишь закрытый перевод, пример
печатается на санскрите без перевода, с пометой «перевод в закрытом слое» (в текущей
редакции таких строк нет). Данные и сборка: [corpus_layer/](https://github.com/gasyoun/SanskritGrammar/tree/main/KocherginaUchebnik_1998/corpus_layer),
скрипт [scripts/build_corpus_layer.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_corpus_layer.py),
регресс — [tests/test_corpus_layer.py](https://github.com/gasyoun/SanskritGrammar/blob/main/tests/test_corpus_layer.py).

---

## Занятие XII — основы на -ī и -ū

Правило «всегда женского рода» раздел I уже поправил (HK-16); корпус добавляет меру:
производные *nadī* и *vadhū* — обиходные слова, а мужской контрпример *senānī* — редкое,
но вполне живое эпическое слово.

| Лемма | Полоса | Ранг | Пример (форма выделена локусом) | Локус DCS | Перевод |
|---|---|---|---|---|---|
| nadī | топ-1000 | 467 | ṛṇadātā ca vaidyaś ca śrotriyaḥ sajalā nadī | Hitopadeśa: Hitop, 1, 111.3 | [где есть] заимодавец, врач, знаток Вед — и река, полная воды |
| vadhū | редкое | 1636 | sarvalakṣaṇasampannā nārīṇām uttamā vadhūḥ | Rāmāyaṇa: Rām, Bā, 1, 24 | наделенная всеми добрыми знаками, лучшая из женщин невеста |
| senānī | редкое | 10649 | devatānāṃ yathā skandaḥ senānīḥ prabhur avyayaḥ | Mahābhārata: MBh, 8, 6, 29 | как Сканда — полководец богов, владыка нетленный |

*senānīḥ* здесь — именительный падеж мужского рода: то самое склонение, которого
правило «всегда женского» не обещает.

## Занятие XVI — IX класс

Ядро класса — не носовые корни (раздел I, HK-19). Полосы показывают, что ядро это
частотное: *jñā* и *grah* — топ-100, и именно их формы *jānā́ti*, *gṛhṇā́ti* учащийся
встретит первыми.

| Лемма | Полоса | Ранг | Пример | Локус DCS | Перевод |
|---|---|---|---|---|---|
| jñā | топ-100 | 90 | tadaiteṣām upayogo jñāyatām | Hitopadeśa: Hitop, 3, 69.2 | так пусть станет известно, какая от них польза |
| grah | топ-100 | 100 | sa mṛtyur eva gṛhṇāti garbham aśvatarī yathā | Hitopadeśa: Hitop, 2, 148.4 | того смерть и хватает — как мулица собственный плод |
| krī | редкое | 3324 | krīṇīyād yas tv apatyārthaṃ mātāpitror yam antikāt | Manusmṛti: ManuS, 9, 172 | [сын], которого ради потомства покупают у отца и матери |
| pū | топ-1000 | 515 | satyena pūyate sākṣī dharmaḥ satyena vardhate | Manusmṛti: ManuS, 8, 83 | правдой очищается свидетель, правдой возрастает дхарма |
| lū | редкое | 6402 | hataputrabalo dīno lūnapakṣa iva dvijaḥ | Rāmāyaṇa: Rām, Bā, 54, 10 | потерявший сыновей и войско, жалкий, как птица с подрезанными крыльями |
| prī | топ-1000 | 540 | anvādheyaṃ ca yad dattaṃ patyā prītena caiva yat | Manusmṛti: ManuS, 9, 191 | и то [имущество], что подарено довольным мужем |
| bandh | топ-1000 | 296 | ātmanāvagataṃ kṛtvā badhnīyāt pūjayec ca vā | Hitopadeśa: Hitop, 2, 143.3 | убедившись сам, пусть либо свяжет [его], либо почтит |

В *gṛhṇāti* и *badhnīyāt* виден суффикс -nā́-/-nī- в работе — у *bandh* с той самой
утратой носового, которую Кочергина делает портретом всего класса.

## Занятие XVIII — будущее время

Все семь примеров — реальные формы будущего. Три первые показывают -iṣya-норму
(56,8 % различных форм, HK-4b), четыре следующие — лексикализованный рефлекс исхода
корня перед -sya (HK-21): dṛś → *drakṣya-*, dah → *dhakṣya-*, sṛj → *srakṣya-*,
ruh → *rokṣya-*.

| Лемма | Полоса | Ранг | Пример | Локус DCS | Перевод |
|---|---|---|---|---|---|
| kṛ | топ-100 | 12 | locanābhyāṃ vihīnasya darpaṇaḥ kiṃ kariṣyati | Hitopadeśa: Hitop, 3, 121.5 | что сделает зеркало тому, кто лишен глаз? |
| bhū | топ-100 | 13 | anena sadṛśo loke na bhūto na bhaviṣyati | Hitopadeśa: Hitop, 3, 103.13 | равного ему в мире не было и не будет |
| gam | топ-100 | 25 | āyuṣaḥ khaṇḍam ādāya ravir astaṃ gamiṣyati | Hitopadeśa: Hitop, 1, 4.4 | забрав кусок жизни, солнце уйдет за горизонт |
| dṛś | топ-100 | 27 | kadā drakṣyāmahe rāmaṃ jagataḥ śokanāśanam | Rāmāyaṇa: Rām, Ay, 77, 8.2 | когда увидим мы Раму, уносящего скорбь мира? |
| dah | топ-1000 | 329 | imaṃ dhakṣyāmi saumitre hataṃ raudreṇa rakṣasā | Rāmāyaṇa: Rām, Ār, 64, 28.2 | его я сожгу, о сын Сумитры, — сраженного свирепым ракшасом |
| sṛj | топ-1000 | 361 | ekībhūto hi srakṣyāmi śarīrād dvijasattama | Mahābhārata: MBh, 3, 187, 46.2 | став единым, я сотворю [все] из [своего] тела, о лучший из дваждырожденных |
| ruh | редкое | 2079 | sasyāni ca na rokṣyanti yugānte paryupasthite | Mahābhārata: MBh, 3, 188, 76.2 | и посевы не взойдут, когда настанет конец юги |

## Занятие XXI — простой перфект и его беглецы

*vid* и *ās* — те корни, что уходят в перифрастический перфект (HK-25); оба при этом
частотны, так что «исключение» встретится раньше многих «правил». Пример *vid* заодно
показывает перфектное причастие *vidvān*, пример *śru* — императив корня aniṭ (HK-26).

| Лемма | Полоса | Ранг | Пример | Локус DCS | Перевод |
|---|---|---|---|---|---|
| vid | топ-100 | 48 | vidvān evopadeṣṭavyo nāvidvāṃs tu kadācana | Hitopadeśa: Hitop, 3, 5.2 | наставлять следует лишь знающего — и никогда незнающего |
| ās | топ-1000 | 494 | śaśino vyapadeśena śaśakāḥ sukham āsate | Hitopadeśa: Hitop, 3, 14.3 | под покровительством месяца зайцы живут счастливо |
| śru | топ-100 | 47 | viṣṇuśarmovāca śṛṇuta yūyam | Hitopadeśa: Hitop, 1, 2.3 | Вишнушарман сказал: слушайте! |

## Занятие XXII — перифрастический перфект вживую

Раздел I дал распределение (as 91,4 % · kṛ 7,4 % · bhū 0,8 %; SG-MO-017). Вот сам
шаблон °ayām āsa в тексте — оба примера с каузативной основой на -ay, как и обещает
корпусная статистика.

| Лемма | Полоса | Ранг | Пример | Локус DCS | Перевод |
|---|---|---|---|---|---|
| as | топ-100 | 17 | tyājayāmāsa rathyāyāṃ nirapekṣatayā niśi | Kathāsaritsāgara: KSS, 3, 6, 126.2 | ночью, ни на что не глядя, велел бросить [его] на дороге |
| tāḍay | редкое | 1585 | utpatya ca hanūmantaṃ tāḍayāmāsa muṣṭinā | Rāmāyaṇa: Rām, Yu, 58, 38.2 | и, взлетев, ударил Ханумана кулаком |

## Занятие XXX — имена на -as

| Лемма | Полоса | Ранг | Пример | Локус DCS | Перевод |
|---|---|---|---|---|---|
| manas | топ-100 | 74 | netravaktravikāreṇa lakṣyate 'ntargataṃ manaḥ | Hitopadeśa: Hitop, 2, 50.2 | по перемене глаз и лица распознается скрытая мысль |
| tejas | топ-1000 | 143 | tasmād abhibhavaty eṣa sarvabhūtāni tejasā | Manusmṛti: ManuS, 7, 5.2 | потому он превосходит все существа [своим] блеском |
| candramas | редкое | 1812 | ekaś candramās tamo hanti na ca tārāgaṇair api | Hitopadeśa: Hitop, 0, 18.3 | одна луна разгоняет тьму — не [сделать этого] и сонмам звезд |

*candramās* — именительный мужского рода: контрпример HK-32 из первых же строф
«Хитопадеши».

## Занятие XXXII — род bahuvrīhi

| Лемма | Полоса | Ранг | Пример | Локус DCS | Перевод |
|---|---|---|---|---|---|
| mahābāhu | редкое | 11898 | āgantā hi mahābāhur ānṛśaṃsyārtham acyutaḥ | Mahābhārata: MBh, 5, 68, 14.3 | ведь придет мощнорукий Ачьюта ради милосердия |

*mahābāhur* мужского рода при основе *bāhu-* — потому что таков носитель признака
(HK-34); в эпосе это слово — постоянный эпитет героев, так что «редкое» по рангу оно
куда заметнее в текстах, чем обещает счетчик отдельной леммы.

## Занятие XXXVII — корневой аорист

Все четыре корня — за пределами списка «некоторые корни на -ā и bhū» (HK-38); формы
*asthāt*, *adāt*, *dhīmahi*, *akramuḥ* — живые корневые аористы. *dhīmahi* учащийся
уже знает наизусть — из мантры гаятри.

| Лемма | Полоса | Ранг | Пример | Локус DCS | Перевод |
|---|---|---|---|---|---|
| sthā | топ-100 | 57 | dvitīyam apy antarakalpam asthāt | Saddharmapuṇḍarīkasūtra: SDhPS, 7, 27 | он пребыл и вторую промежуточную кальпу |
| dā | топ-100 | 43 | aṅgulīyam abhijñānam adāt tubhyaṃ yaśasvini | Rāmāyaṇa: Rām, Su, 56, 81.2 | он дал тебе перстень как опознавательный знак, о славная |
| dhā | топ-1000 | 283 | viśvā vāmāni dhīmahi | Āpastambaśrautasūtra: ĀpŚS, 6, 23, 1.6 | да обретем мы все блага |
| kram | редкое | 2293 | pra somāsaḥ svādhyaḥ pavamānāso akramuḥ | Ṛgveda: ṚV, 9, 31, 1 | выступили вперед благодатные сомы, очищаясь |

## Занятие XXXIX — два преверба

| Лемма | Полоса | Ранг | Пример | Локус DCS | Перевод |
|---|---|---|---|---|---|
| samāgam | редкое | 1029 | pṛṣṭaś ca kas tvam kutaḥ samāgato 'si | Hitopadeśa: Hitop, 3, 4.11 | и спрошен был: кто ты, откуда пришел? |

*sam-ā-gam* — двухпревербный глагол с контактным ā, ровно по списку занятия; сама
лемма при этом обиходнее своего ранга — прежде всего за счет формулы приветствия
*kutaḥ samāgato 'si*.

---

_Раздел IV методички. Числа полос воспроизводимы скриптом
[scripts/build_corpus_layer.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_corpus_layer.py)
из [corpus_layer/corpus_layer.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/corpus_layer/corpus_layer.tsv);
корпусные данные — Digital Corpus of Sanskrit (О. Хельвиг). Перед печатью —
[/publish-safety-check](https://github.com/gasyoun/claude-config/blob/main/commands/publish-safety-check.md)._

_Dr. Mārcis Gasūns_
