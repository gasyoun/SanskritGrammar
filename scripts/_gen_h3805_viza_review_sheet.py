# Generate H3805 review sheet: Apte P4 viza + H3804 Buhler viza addendum.
import sys
sys.stdout.reconfigure(encoding="utf-8")
from csl_pyutil import render_review_sheet

items = []

# ---------------- Apte corpus layer (34 rows) ----------------
apte_corpus_sections = [
    ("Занятие 3 — глаголы движения и падеж цели", [
        ("gam", "топ-100", 25, "tenāsau pañcatvam agamat", "Hitopadeśa: Hitop, 2, 35.3", "оттого он и отошел к пяти началам [умер]"),
        ("yā", "топ-100", 81, "sa eva nidhanaṃ yāti kīlotpāṭīva vānaraḥ", "Hitopadeśa: Hitop, 2, 30.5", "тот и идет к гибели — как обезьяна, выдернувшая клин"),
        ("i", "топ-1000", 307, "āsannataratām eti mṛtyur jantor dine dine", "Hitopadeśa: Hitop, 4, 74", "день за днем смерть подходит к живому все ближе"),
        ("car", "топ-1000", 176, "ajā siṃhaprasādena vane carati nirbhayam", "Hitopadeśa: Hitop, 3, 13.2", "милостью льва коза бесстрашно бродит по лесу"),
        ("vraj", "топ-1000", 642, "sa vināśaṃ vrajaty āśu sūcakāśucir eva ca", "Manusmṛti: ManuS, 4, 71.2", "тот быстро идет к погибели, как и нечистый доносчик"),
        ("sṛ", "редкое", 3640, "tvaramāṇo janasthānaṃ sasārābhimukhas tadā", "Rāmāyaṇa: Rām, Ār, 42, 21.2", "тогда, спеша, он устремился прямо к Джанастхане"),
        ("dhāv", "редкое", 1551, "rājā stenena gantavyo muktakeśena dhāvatā", "Manusmṛti: ManuS, 8, 314", "вор должен бежать к царю с распущенными волосами"),
    ]),
    ("Занятие 7 — глаголы чувства", [
        ("ruc", "редкое", 1463, "yad eva rocate yasmai bhavet tat tasya sundaram", "Hitopadeśa: Hitop, 2, 53.3", "что кому нравится, то для того и прекрасно"),
        ("krudh", "топ-1000", 416, "na jāne kruddhaḥ svāmī kiṃ vidhāsyati", "Hitopadeśa: Hitop, 2, 85.14", "не знаю, что сделает разгневанный господин"),
        ("druh", "редкое", 4237, "sa mātā sa pitā jñeyas taṃ na druhyet kadācana", "Manusmṛti: ManuS, 2, 144.2", "его следует чтить как мать и отца — ему пусть не вредит никогда"),
        ("īrṣy", "редкое", 35949, "idānīm evāhaṃ janaka strīṇām īrṣyāmi no purā", "Āpastambadharmasūtra: ĀpDhS, 2, 13, 6.2", "лишь теперь, о Джанака, я ревную женщин — прежде нет"),
        ("asūy", "редкое", 8823, "asūyanti hi rājāno janān anṛtavādinaḥ", "Mahābhārata: MBh, 4, 4, 13", "ведь цари негодуют на людей лживых"),
    ]),
    ("Занятие 9 — «бросать» и «любить»", [
        ("kṣip", "топ-1000", 264, "gāṃ vipram ajam agniṃ vā prāśayed apsu vā kṣipet", "Manusmṛti: ManuS, 3, 260.2", "пусть скормит корове, брахману, козе, огню — или бросит в воду"),
        ("muc", "топ-1000", 162, "paśya mūṣikamitreṇa kapotā muktabandhanāḥ", "Hitopadeśa: Hitop, 1, 53.4", "смотри: другом-мышью голуби освобождены от пут"),
        ("snih", "редкое", 4166, "tataś cāsyāṃ svayaṃ tasya cakṣuḥ snihyed asaṃśayam", "Kathāsaritsāgara: KSS, 2, 3, 11.2", "и тогда его взгляд, без сомнения, сам потянется к ней с любовью"),
        ("abhilaṣ", "редкое", 4413, "etad bhavatām abhilaṣitam api sampannam", "Hitopadeśa: Hitop, 1, 201.6", "вот и желание ваше исполнилось"),
        ("anurañj", "редкое", 3181, "anuraktaḥ śucir dakṣaḥ smṛtimān deśakālavit", "Manusmṛti: ManuS, 7, 64", "преданный, честный, ловкий, памятливый, знающий место и время"),
    ]),
    ("Занятие 10 — «власть» и «память»", [
        ("īś", "редкое", 2491, "na kaścid īśate brahman svayaṃgrāhasya sattama", "Mahābhārata: MBh, 3, 200, 22", "никто, о брахман, не властен над самовольным захватом"),
        ("prabhū", "редкое", 2142, "kathaṃ mṛtyuḥ prabhavati vedaśāstravidāṃ prabho", "Manusmṛti: ManuS, 5, 2.2", "как смерть имеет власть над знатоками Вед, о владыка?"),
        ("day", "редкое", 9223, "dāmyata datta dayadhvam iti", "Bṛhadāraṇyakopaniṣad: BĀU, 5, 2, 3.8", "«смиряйте себя, давайте, сострадайте»"),
        ("smṛ", "топ-1000", 114, "smarantī taṃ ca bhartāraṃ muktakaṇṭhaṃ ruroda sā", "Kathāsaritsāgara: KSS, 2, 1, 61.2", "вспоминая того мужа [вин.], она рыдала в голос"),
        ("adhī", "редкое", 1275, "mayā ca dharmaśāstrāṇi adhītāni", "Hitopadeśa: Hitop, 1, 11", "и дхармашастры мною изучены"),
    ]),
    ("Занятие 22 — частица uta", [
        ("uta", "топ-1000", 363, "śṛṇu deva kim asmābhir baladarpād durgaṃ bhagnam uta tava pratāpādhiṣṭhitenopāyena", "Hitopadeśa: Hitop, 4, 23", "слушай, государь: нами ли, в гордыне силы, взята крепость — или уловкой, опирающейся на твое величие?"),
        ("kim", "топ-1000", 583, "śvā yadi kriyate rājā tat kiṃ nāśnāty upānaham", "Hitopadeśa: Hitop, 3, 60.23", "если пса сделают царем — разве не станет он грызть сандалию?"),
    ]),
    ("Занятия 29–30 — назначение залога", [
        ("krīḍ", "редкое", 1576, "tatra balavān vānarayūthaḥ krīḍann āgataḥ", "Hitopadeśa: Hitop, 2, 31.5", "туда, резвясь, пришла сильная обезьянья стая"),
        ("ram", "топ-1000", 495, "vaktā śrotā ca yatrāsti ramante tatra sampadaḥ", "Hitopadeśa: Hitop, 2, 135.3", "где есть говорящий и слушающий, там обитают богатства"),
        ("han", "топ-100", 55, "ekaś candramās tamo hanti na ca tārāgaṇair api", "Hitopadeśa: Hitop, 0, 18.3", "одна луна разгоняет тьму — не [сделать этого] и сонмам звезд"),
    ]),
    ("Приложение — словарь частиц", [
        ("punar", "топ-100", 39, "punar na tatra gamiṣyāmi", "Hitopadeśa: Hitop, 3, 17.6", "снова туда не пойду"),
        ("prāyas", "редкое", 2205, "prāyaḥ samāpannavipattikāle dhiyo 'pi puṃsāṃ malinā bhavanti", "Hitopadeśa: Hitop, 1, 28.3", "обычно в час нагрянувшей беды даже разум людей мутнеет"),
        ("muhur", "топ-1000", 652, "suṣeṇaṃ tāḍayāmāsa nanāda ca muhur muhuḥ", "Rāmāyaṇa: Rām, Yu, 33, 35.2", "он ударил Сушену и взревел снова и снова"),
        ("yatas", "топ-1000", 366, "yato rājadharmaś caiṣaḥ", "Hitopadeśa: Hitop, 3, 64", "ибо таков и долг царя"),
        ("yāvat", "топ-1000", 172, "tāvad bhayasya bhetavyaṃ yāvad bhayam anāgatam", "Hitopadeśa: Hitop, 1, 57.9", "бояться беды следует [лишь] до тех пор, пока беда не пришла"),
        ("hā", "топ-1000", 190, "hā hā putraka nādhītaṃ gatāsv etāsu rātriṣu", "Hitopadeśa: Hitop, 0, 24", "увы, увы, сынок: ничего не выучено за эти ушедшие ночи"),
        ("vara", "топ-100", 82, "varam eko guṇī putro na ca mūrkhaśatair api", "Hitopadeśa: Hitop, 0, 18.2", "лучше один достойный сын — и ни к чему даже сотни глупцов"),
    ]),
]

APTE_CORPUS_URL = "https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/METODICHKA_APTE_CORPUS_LAYER_2026.md"
BUHLER_CORPUS_URL = "https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/METODICHKA_BUHLER_CORPUS_LAYER_2026.md"
APTE_UPR_URL = "https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/METODICHKA_APTE_V1_UPRAZHNENIIA_2026.md"
BUHLER_UPR_URL = "https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/METODICHKA_BUHLER_V1_UPRAZHNENIIA_2026.md"

def corpus_items(book, sections, url):
    out = []
    for section, rows in sections:
        for lemma, band, rank, example, locus, translation in rows:
            cid = f"{book}-corpus-{lemma}-{rank}"
            out.append({
                "id": cid,
                "filt": f"{book}-corpus",
                "title": f"{lemma} — {section}",
                "badges": [band, f"ранг {rank}"],
                "question": (
                    f"<p><b>Пример (DCS):</b> {example}</p>"
                    f"<p><b>Локус:</b> {locus}</p>"
                    f"<p><b>Черновой перевод (Fable 5, до визы):</b> «{translation}»</p>"
                ),
                "panels": [("Раздел", f"{section} — <a href=\"{url}\">{url}</a>")],
                "note_placeholder": "правка перевода или причина отклонения",
            })
    return out

items += corpus_items("apte", apte_corpus_sections, APTE_CORPUS_URL)

buhler_corpus_sections = [
    ("Урок XVIII — каузатив: вриддхи конечного гласного и один беглец", [
        ("kāray", "топ-1000", 433, "māṃ rajadarśanaṃ kāraya", "Hitopadeśa: Hitop, 3, 102.5", "дай мне увидеть царя [устрой мне лицезрение царя]"),
        ("darśay", "топ-1000", 594, "tad ahaṃ tvāṃ tatra nītvā darśayāmi", "Hitopadeśa: Hitop, 1, 73.4", "вот я отведу тебя туда и покажу"),
        ("sthāpay", "топ-1000", 632, "jitendriyo hi śaknoti vaśe sthāpayituṃ prajāḥ", "Manusmṛti: ManuS, 7, 44.2", "ведь [лишь] владеющий чувствами способен держать подданных в повиновении"),
        ("śrāvay", "редкое", 2361, "svādhyāyaṃ śrāvayet pitrye dharmaśāstrāṇi caiva hi", "Manusmṛti: ManuS, 3, 232", "на обряде предкам пусть даст услышать [чтение] Веды и дхармашастр"),
        ("pūray", "редкое", 1123, "jalabindunipātena kramaśaḥ pūryate ghaṭaḥ", "Hitopadeśa: Hitop, 2, 10.2", "падением водяных капель постепенно наполняется кувшин"),
    ]),
    ("Урок XXVIII — seṭ и aniṭ причастия: обе половины склеенных пар", [
        ("kup", "редкое", 1398, "tam uvāca tatas tatra kupitā janakātmajā", "Rāmāyaṇa: Rām, Ār, 43, 5", "тогда разгневанная дочь Джанаки сказала ему там"),
        ("krudh", "топ-1000", 416, "ata evāyaṃ daṇḍanāyakaḥ kruddha eva gacchati", "Hitopadeśa: Hitop, 2, 119.10", "потому-то этот начальник стражи и уходит разгневанным"),
        ("jan", "топ-100", 62, "jātasya hi dhruvo mṛtyur dhruvaṃ janma mṛtasya ca", "Hitopadeśa: Hitop, 4, 71.2", "ибо рожденному непреложна смерть, непреложно рождение мертвому"),
        ("khan", "редкое", 3640, "sa khātaṃ pitṛbhir mārgam antarbhaumaṃ mahātmabhiḥ", "Rāmāyaṇa: Rām, Bā, 40, 6", "он [пошел] подземным путем, прорытым великими предками"),
        ("san", "редкое", 3542, "pūṣā vājaṃ sanotu naḥ", "Ṛgveda: ṚV, 6, 54, 5.2", "пусть Пушан добудет нам награду"),
        ("pat", "топ-1000", 211, "atra marusthale patitā yūyaṃ kiṃ kurutha", "Hitopadeśa: Hitop, 3, 4.17", "что вы делаете, попав в эту пустыню?"),
    ]),
    ("Урок XXXIV — samāsānta: rājan → °rāja, sakhi → °sakha, pathin → °patha", [
        ("rājan", "топ-100", 23, "rājovāca katham etat", "Hitopadeśa: Hitop, 3, 6", "царь сказал: как это [было]?"),
        ("yuvarāja", "редкое", 7964, "saṃdhāya yuvarājena yadi vā mukhyamantriṇā", "Hitopadeśa: Hitop, 3, 95", "заключив союз с наследником престола или с первым министром"),
        ("sakhi", "топ-1000", 875, "saṃjīvakenoktaṃ sakhe brūhi kim etat", "Hitopadeśa: Hitop, 2, 154", "Санджнивака сказал: друг, скажи, что это?"),
        ("pathin", "топ-1000", 698, "śivās te santu panthānaḥ", "Hitopadeśa: Hitop, 2, 124.20", "да будут пути твои благосклонны [счастливого пути]"),
        ("apatha", "редкое", 15149, "āpad ety ubhayalokadūṣaṇī vartamānam apathe hi durmatim", "Kirātārjunīya: Kir, 13, 64.2", "ведь к злоумному, стоящему на дурном пути, приходит беда, губящая оба мира"),
    ]),
    ("Урок XXXVIII — корни на u: au перед согласным окончанием", [
        ("stu", "топ-1000", 432, "udgātā cāpi māṃ stauti gītaghoṣair mahādhvare", "Mahābhārata: MBh, 14, 53, 10", "и удгатар славит меня звуками песнопений на великом жертвоприношении"),
        ("ru", "редкое", 5464, "prāk pādayoḥ patati khādati pṛṣṭhamāṃsaṃ karṇe phalaṃ kim api rauti śanair vicitram", "Hitopadeśa: Hitop, 1, 82.2", "сперва падает в ноги, [потом] грызет мясо со спины и тихо, чудно воет что-то на ухо"),
    ]),
    ("Урок XLIII — перфект: не «реже», а нарратив по умолчанию", [
        ("vac", "топ-100", 15, "rājovāca katham etat", "Hitopadeśa: Hitop, 3, 6", "царь сказал: как это [было]?"),
        ("bhū", "топ-100", 13, "dhārāsārair mahatī vṛṣṭir babhūva", "Hitopadeśa: Hitop, 3, 6.6", "потоками ливня пролился великий дождь"),
        ("gam", "топ-100", 25, "avaruhya jagāmāśu velāvanam anuttamam", "Rāmāyaṇa: Rām, Yu, 4, 66", "спустившись, он быстро пошел в несравненный прибрежный лес"),
    ]),
    ("Урок XLIV — будущее: сначала частое", [
        ("yā", "топ-100", 81, "yāsyāmi bhava suprītā vanaṃ cīrajaṭādharaḥ", "Rāmāyaṇa: Rām, Ay, 16, 30.2", "я уйду в лес, нося платье из лыка и косу отшельника, — будь же довольна"),
        ("dṛś", "топ-100", 27, "ito drakṣyāmi vaidehīṃ rāmadarśanalālasām", "Rāmāyaṇa: Rām, Su, 12, 41", "отсюда я увижу Вайдехи, жаждущую увидеть Раму"),
    ]),
    ("Урок XLV — аорист: тематическая парадигма и корневой запрет", [
        ("sic", "редкое", 1563, "toyair jalastham asicann ārabdhajalakelayaḥ", "Kathāsaritsāgara: KSS, 5, 3, 57.2", "затеяв игры в воде, они обливали водой сидевшего в ней"),
        ("muc", "топ-1000", 162, "praśaste tithinakṣatre bohittham amucad vaṇik", "Bṛhatkathāślokasaṃgraha: BKŚS, 18, 251.2", "в благоприятный день, под счастливым созвездием купец отпустил корабль [отчалил]"),
        ("dā", "топ-100", 43, "asūyakāya māṃ mādās tathā syāṃ vīryavattamā", "Manusmṛti: ManuS, 2, 114.2", "не выдавай меня хулителю — тогда стану я наимощнейшей [говорит Веда о себе]"),
    ]),
    ("Управление глаголов — подтвержденные рамки Шерцля вживую", [
        ("hu", "топ-1000", 395, "vātendraguruvahnīnāṃ juhuyāt sarpiṣāhutīḥ", "Manusmṛti: ManuS, 11, 120.2", "Ветру, Индре, Наставнику и Огню пусть принесет возлияния топленого масла"),
        ("ah", "топ-100", 69, "tāv āhatuḥ katham etat", "Hitopadeśa: Hitop, 1, 158", "те двое сказали: как это [было]?"),
        ("grah", "топ-100", 100, "bālād api gṛhītavyaṃ yuktam uktaṃ manīṣibhiḥ", "Hitopadeśa: Hitop, 2, 79.2", "дельное слово следует принять даже от ребенка — так сказали мудрые"),
        ("pā", "топ-1000", 101, "sa caikadā pipāsākulitaḥ pānīyaṃ pātuṃ yamunākaccham agacchat", "Hitopadeśa: Hitop, 2, 20", "и однажды, томимый жаждой, он пошел к берегу Ямуны попить воды"),
        ("dhā", "топ-1000", 283, "cukrodha ca mahākrodho vadhe cāsya mano dadhe", "Rāmāyaṇa: Rām, Yu, 84, 17.2", "вспыхнул он великим гневом и устремил мысль на его убийство"),
    ]),
]

items += corpus_items("buhler", buhler_corpus_sections, BUHLER_CORPUS_URL)

# ---------------- Apte uprazhneniia: keys ----------------
apte_keys = [
    ("3-1", "1 — § 33 (धिग् с винительным); 2 — § 35 (अन्तरेण «без, в отношении» + вин.); 3 — § 32 (वस् с приставкой अधि — винительный места обитания); 4 — § 37 (अनु «вслед за» + вин., karmapravacanīya)."),
    ("3-2", "Дательный цели (grāmāya gacchati) — реальная, но меньшинная альтернатива винительному цели: не ошибка, а та самая «одна из семи» (14,1 %); Апте сам допускает ее в § 71 для физического движения."),
    ("7-1", "सचिवोपदेशाय (дательный при असूय्) и हितवादिने (дательный при कुप्) — § 63: глаголы гнева/злобы управляют дательным лица."),
    ("7-2", "Винительный: он лидирует у krudh/druh и без приставок (подъем дательного 0,91 — ниже фона), а с приставками его требует сам Апте. «Дательный гнева» — книжное правило, винительный — корпусное большинство."),
    ("9-1", "1 — местный (त्वयि, § 94); 2 — родительный (आवयोः при स्निह्, युष्मत्संनिकर्षस्य при उत्कण्ठ्) — живой конкурент местного, которого § 94 не называет; 3 — винительный при अनुरक्ता (примечание Апте к § 94: производные от अनुरञ्ज् с винительным, अनु как karmapravacanīya § 37)."),
    ("9-2", "Винительным объекта — потому что muc чаще значит «освобождать» (मुक्तबन्धनाः «освобожденные от пут»), а не «бросать в»; местный цели при muc в чистом виде редок."),
    ("10-1", "ईश् «владеть, мочь» + родительный गात्राणां — § 113: «не властен над своими членами (не владею телом)»."),
    ("10-2", "«Объект smṛ/adhī стоит в родительном ИЛИ винительном, причем винительный чаще (41 % против 30 %)» — родительный правилен, но не единствен; smarasi godāvarīṃ — не исключение, а большинство."),
    ("19-1", "Пример § 210 показывает лишь то, что аорист *может* стоять при обстоятельстве длительности (यावज्जीवं), но не то, что имперфект там невозможен: по § 207 самого Апте классические авторы употребляют три прошедших «случайным образом», а по Уитни §§ 927–929 аорист несет завершительное значение — прямую противоположность длительности. Запрет «*не* अददात्» — предписание панинийской доктрины, не факт языка (APT-31, FALSE)."),
    ("22-1", "В первом — повторенное uta «или — или» (§ 258 (а)); во втором — одиночное uta сомнения/догадки «столб это или человек?» (§ 259 (1))."),
    ("22-2", "Потому что uta регулярно (23,66 %) открывает предложение — она возглавляет вторую половину разделительного вопроса (kim… uta…), тогда как настоящие постпозитивы (ca/tu/hi — < 1 %) в начале предложения не встречаются; «пользоваться по смыслу, но не как постпозитивной» (виза, зан-22)."),
    ("29-1", "1 — § 337 (yuj с приставкой anu → Ātmanepada: अन्वयुङ्क्त); 2 — § 340 (vi+kṛ «издавать звуки» → Ātmanepada: विकुर्वाणः स्वरान्); 3 — § 317 (b) (upa+yam «брать в жены» → Ātmanepada: उपयेमे); 4 — примечание к § 316: विनी «приручать, дрессировать» → Parasmaipada (विनेष्यन्)."),
    ("29-2", "Подтверждены корпусом и потому заучиваются как факт: § 337 (pra/upa+yuj — но с оговоркой: корпус дает подлинно смешанное 41/59, т. е. Ātmanepada лишь как слабое большинство), § 317 (b) — не входит в проверенные 15; строго подтверждены из разбора — никакие: у № 2 и № 4 (vi+kṛ, vi+nī) корпус либо не дал n ≥ 40, либо показал обратное (nī-группа — 92,6 % Parasmaipada). Как жесткий факт залога из уроков 29–30 учите vi/parā+ji, upa+sthā, bhuj и каузативы § 344; правила kram, nī, pra/upa+yuj и krī-группы — как предписание, которое живой текст соблюдает не всегда (реестр APT-40)."),
]

apte_translations = [
    ("3-1", "Он пришел в крайнее отчаяние."),
    ("3-2", "Странствуй по желанным краям, о облако, обогащенное дождями."),
    ("7-1", "…что нравится вашей светлости."),
    ("7-2", "Так что же ты, словно не понимая, гневаешься на зятя?"),
    ("9-1", "Почему же мое сердце так любит этого ребенка?"),
    ("9-2", "…для желающего пускать стрелы в ланей»; «Стрела не должна поразить тело этой лани."),
    ("10-1", "Ты властен над богатствами — а мы, насколько нужно, властны над словами."),
    ("10-2", "О царица, помнишь ли ты то место…»; «Помнишь ли те дни, помнишь ли Годавари?"),
    ("19-1", "Да не будет помехи обитателям рощи подвижников."),
    ("19-2", "Не поддавайся малодушию, о Партха."),
    ("19-3", "Что я тогда делал, куда ходил, что говорил — ничего этого я не помню (не узнал)."),
    ("22-1", "Не знаю: пристало ли это одеждам из коры, подходит ли к спутанным волосам, согласуется ли с аскезой — или это часть праведных наставлений."),
    ("22-2", "Наставлено ли это учителями, вычитано ли в дхармащастрах, способ ли это достичь освобождения — или некий иной род обета?"),
    ("29-1", "Силы же — совет, мощь и рвение, — поддерживая друг друга, развиваются в делах."),
    ("29-2", "Совершив изгнание Ситы, тот владыка земли владел одной лишь землею, опоясанной океаном."),
]

def key_items(book, keys, url, section_label):
    out = []
    for locus, text in keys:
        out.append({
            "id": f"{book}-key-{locus}",
            "filt": f"{book}-uprazhneniia-keys",
            "title": f"Ключ {locus}",
            "badges": ["⟦MG-viza⟧"],
            "question": f"<p><b>Черновой ключ (до визы):</b> {text}</p>",
            "panels": [("Раздел", f"{section_label} — <a href=\"{url}\">{url}</a>")],
            "note_placeholder": "правка формулировки или причина отклонения",
        })
    return out

def translation_items(book, translations, url, section_label):
    out = []
    for locus, text in translations:
        out.append({
            "id": f"{book}-translation-{locus}",
            "filt": f"{book}-uprazhneniia-translations",
            "title": f"Перевод чтения {locus}",
            "badges": ["⟦MG-viza⟧"],
            "question": f"<p><b>Черновой перевод (до визы):</b> «{text}»</p>",
            "panels": [("Раздел", f"{section_label} — <a href=\"{url}\">{url}</a>")],
            "note_placeholder": "правка перевода или причина отклонения",
        })
    return out

items += key_items("apte", apte_keys, APTE_UPR_URL, "Апте, раздел IV — Ключи ⟦MG-viza⟧")
items += translation_items("apte", apte_translations, APTE_UPR_URL, "Апте, раздел IV — Переводы чтений ⟦MG-viza⟧")

# ---------------- Buhler uprazhneniia: keys + translations ----------------
buhler_keys = [
    ("18-1", "1 — sthāpaya: п. 3г не применим (корень на ā берет paya по п. 2а; sthā → sthāpaya-), простой винительный ratham; 2 — śrāvayeḥ: п. 3г (śru → vṛddhi au → āv), двойной винительный kāvyaṃ… mām «дай мне услышать поэму»; 3 — paridhāpayeyuḥ: п. 2а (dhā → dhāpaya-), двойной винительный bālān… vastrāṇi «пусть оденут мальчиков в новые одежды»; 4 — apātyanta: пассив каузатива по п. 4 (pātaya- → pātya-te) «деревья были повалены силой ветра»."),
    ("18-2", "От pṝ «наполнять»: конечный ṝ после губного дает ūr (pūrayati), а не вриддхи (реестр HB-142; то же правило ūr — заметка OCH-14 линии Зализняка). Каузатив на -ūrayati — всегда сигнал губного корня на ṝ."),
    ("28-1", "Прямо (п. 2–3): labdhāni (labh → labdha, п. 3г — bh → b, t → dh), pṛṣṭaḥ (prach → pṛṣṭa, п. 3в). Через i (п. 3а, список урока): uṣitaiḥ (vas, uṣita — в самом списке), patitaḥ (pat), likhitāt (likh, п. 4 — корень на kh). Через ī (п. 5): gṛhītaḥ (grah)."),
    ("28-2", "Вместо krudh — kup «гневаться» (kupita): krudh кончается на dh, а не на t/p/s, и образует kruddha без i; вместо «sam, sata» — san (ṣaṇ) «давать», причастие sāta с удлинением, как в jāta и khāta строкой выше (Pāṇini 6.4.42); sam вдобавок не корень на n/ṇ. Контраст для памяти: kupita «разгневанный» (с i) — kruddha (без i, с озвончением); реестр HB-211/HB-219."),
    ("34-1", "kopāviṣṭena — тип п. 4а через причастие: kopa āviṣṭo yaṃ saḥ «в кого вошел гнев»; pāṭitodaraḥ — pāṭitam udaraṃ yasya saḥ «у кого распорот живот»; gataprāṇaḥ — gatāḥ prāṇā yasya saḥ «чья жизнь ушла»; bālendudyutinā — п. 4б: bālendor iva dyutir yasya «чей блеск — как у молодого месяца» (согласовано с daṃṣṭrāgreṇa)."),
    ("34-2", "°rāja — обязательная замена rājan в конце всякого tatpuruṣa (п. 3, Pāṇini 5.4.91): aṅgarājaḥ, склоняется как deva. Оговорка о блокировке после a(не) — тенденция, не закон: классическое apatha n. «бездорожье» (тип patha) сосуществует с apathin (реестр HB-269); встретив apatha, фиксируйте вариант, а не ошибку."),
    ("38-1", "П. 4 урока: все корни на u в сильных формах перед согласными окончаниями имеют vṛddhi au — stauti, astaut. Для tu/ru/stu тот же пункт допускает guṇa со вставным ī: stavīti (и stavīmi в парадигме). ūrṇoti — единственный маргинальный контрпример «всех» (производный корень ūrṇu, Pāṇini 7.3.90 vibhāṣā), элементарному курсу не нужный: доверяйте au (реестр HB-296)."),
    ("43-1", "dhā: 3 ед. dadhau, 3 мн. dadhuḥ (сильная основа dadhau по п. 12 — корни на ā в 1/3 ед. на au; слабая dadh-); stu: tuṣṭāva / tuṣṭuvuḥ (сильная tuṣṭāv-, слабая tuṣṭuv-, п. 7); han: jaghāna / jaghnuḥ (сильная jaghān-, слабая jaghn-, п. 11)."),
    ("43-2", "Агрегат DCS тяжел эпосом и пуранами, где перфект — форма повествования; в узком срезе кавьи или шастры направление Бюлера может удерживаться. Поэтому строка — сверхобобщение с неверным для корпуса в целом направлением (OVERSTATED со стратификационной оговоркой), а не фактическая ложь класса опечаток (реестр HB-57). Практический вывод чтения эпоса: uvāca, babhūva, jagāma — норма, имперфект — сосед по строке с тем же значением."),
    ("45-1", "Верно: «как impf. VI кл.» — asicat строится ровно как atudat (тематическое -a-, без носового инфикса); имперфект VII класса (aruṇadham) не похож ни на одну напечатанную форму. Строку опровергает ее же соседняя парадигма — потому это опечатка, а не ошибка Бюлера-грамматиста (реестр HB-60; Whitney §§ 846–847)."),
    ("45-2", "Удваивается конечный согласный (ā-śi-śat, ā-rji-jat, ai-ci-kṣat — эхо согласного с i-вставкой); «эхо» и есть примета каузативного аориста гласного корня (реестр HB-372; Whitney § 865; Очерк § 142 — аорист 3 «обычно аорист каузатива»)."),
]

buhler_translations = [
    ("18-1", "Врагов он отправил на небо, своим возвестил смысл Веды, богов накормил нектаром, Брахму обучил Веде."),
    ("18-2", "Пусть царь заставит вайшьев платить подати."),
    ("28-1", "Глупый осел, обманутый ласковыми речами шакала, пришел в пещеру льва и был им убит."),
    ("28-2", "На полях зерно проросло от вод, пролитых облаками."),
    ("34-1", "Чрезмерной жажды [обладания] иметь не следует — но и жажды вовсе не оставляй: у одержимого чрезмерной жаждой [вырастает] хохол на темени."),
    ("34-2", "А тот вепрь, охваченный яростью, острием клыка, блистающего как молодой месяц, распорол пулинде живот — и тот, бездыханный, упал на землю."),
    ("38-1", "Ты — дочь славящего, просящего, принимающего [дары]; я же — [сын] славимого, дающего, не принимающего."),
    ("38-2", "Восемью гимнами риши восславил Агни-и-Сому, тремя — Индру-и-Варуну."),
    ("38-3", "Лишь тот язык — язык, что славит Будду; лишь то сердце — сердце, что предано Будде."),
    ("45-1", "«не давай»; «не бойся»."),
]

items += key_items("buhler", buhler_keys, BUHLER_UPR_URL, "Бюлер, раздел IV — Ключи ⟦MG-виза⟧")
items += translation_items("buhler", buhler_translations, BUHLER_UPR_URL, "Бюлер, раздел IV — Переводы чтений ⟦MG-виза⟧")

print(f"Total items: {len(items)}", file=sys.stderr)
for k in ("apte-corpus", "apte-uprazhneniia-keys", "apte-uprazhneniia-translations",
          "buhler-corpus", "buhler-uprazhneniia-keys", "buhler-uprazhneniia-translations"):
    n = sum(1 for it in items if it["filt"] == k)
    print(f"  {k}: {n}", file=sys.stderr)

config = {
    "sheet_id": "sanskritgrammar-apte-buhler-viza_p4",
    "title": "Виза P4 — методички Апте и Бюлера (корпусный слой + упражнения)",
    "subtitle": (
        "Черновые русские переводы примеров DCS (раздел II) и черновые ключи/переводы чтений "
        "раздела IV — методички Апте (H3739) и Бюлера (H3804). Каждая карточка — один "
        "черновик ⟦MG-viza⟧/⟦MG-виза⟧ до подписи автора."
    ),
    "footer": (
        "Approve = принять черновик как есть (правку впишите в поле заметки, если требуется точечная замена слова). "
        "Reject = черновик не годится, нужен новый вариант — опишите проблему в заметке. "
        "Defer = отложить на потом."
    ),
    "approve_label": "Принять перевод/ключ",
    "reject_label": "Отклонить",
    "filters": [
        ("apte-corpus", "Апте: корпусный слой (34)"),
        ("apte-uprazhneniia-keys", "Апте: ключи упражнений (13)"),
        ("apte-uprazhneniia-translations", "Апте: переводы чтений (15)"),
        ("buhler-corpus", "Бюлер: корпусный слой (31)"),
        ("buhler-uprazhneniia-keys", "Бюлер: ключи упражнений (11)"),
        ("buhler-uprazhneniia-translations", "Бюлер: переводы чтений (10)"),
    ],
    "generated": "31-08-2026",
    "show_ids": True,
    "note_min_height_px": 88,
    "save_as": "SanskritGrammar/review/sanskritgrammar-apte-buhler-viza_p4_decisions.json",
}

screening = {
    "deterministic": 0,
    "lookup": 0,
    "agent": 0,
    "human": len(items),
    "evidence_path": "review/screening_evidence_sanskritgrammar-apte-buhler-viza_p4.md",
    "rules": ["none"],
}

html = render_review_sheet(items=items, config=config, extras=True, screening=screening)

with open(sys.argv[1], "w", encoding="utf-8") as f:
    f.write(html)
print(f"Wrote {sys.argv[1]}", file=sys.stderr)
