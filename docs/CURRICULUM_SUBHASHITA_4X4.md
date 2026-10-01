# Субхашита 4×4 — 16-урочный план из kosha subhashita-beginner (H2169)

_Created: 16-08-2026 · Last updated: 16-08-2026_

16 lessons in 4 blocks of rising difficulty, built **entirely** from the 106 sayings of
kosha's [subhashita_beginner_pack.json](https://github.com/gasyoun/kosha/blob/main/data/subhashita/subhashita_beginner_pack.json)
(slug `subhashita-beginner`; Böhtlingk, *Indische Sprüche*, 2nd ed. 1870–73, public domain;
difficulty 0.2841–0.4063; 85.3% of tokens carry an RU lemma-layer gloss per
[RU_GLOSS_COVERAGE.md](https://github.com/gasyoun/kosha/blob/main/reading/RU_GLOSS_COVERAGE.md)).
No saying outside the pack is used; no saying is invented. Handoff:
[H2169](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2169-Fable_SanskritGrammar_subhashita-16-lesson-plan_02.08.26.md)
(Fable 5) — Subhāṣita 4×4-block lesson plan. Plan context:
[PLAN_NALOPAKHYANA_SUBHASHITA_COURSES_2026.md](https://github.com/gasyoun/Uprava/blob/main/docs/PLAN_NALOPAKHYANA_SUBHASHITA_COURSES_2026.md)
·
[IMPLEMENTATION_NALOPAKHYANA_SUBHASHITA_COURSES_2026.md](https://github.com/gasyoun/Uprava/blob/main/docs/IMPLEMENTATION_NALOPAKHYANA_SUBHASHITA_COURSES_2026.md)
§2.1. Curation provenance:
[CURATION_NOTES.md](https://github.com/gasyoun/kosha/blob/main/data/subhashita/CURATION_NOTES.md);
raw difficulty table:
[subhashita_difficulty.tsv](https://github.com/gasyoun/kosha/blob/main/data/subhashita/subhashita_difficulty.tsv).

Sayings are cited by their *Indische Sprüche* number — the `num` field of the pack
(e.g. **IS 954**), which is also the stable key for future `Lesson` DB records.

## How the blocks were cut

The 106 sayings were sorted by the pack's `difficulty` score and cut into four
**strictly non-overlapping** quartile bands (26 · 27 · 27 · 26 sayings):

| Block | Sayings | Difficulty band | Character |
|---|---|---|---|
| 1 — Опора (the śloka baseline) | 26 | 0.2841–0.3585 | anuṣṭubh with heavy repetition; present tense; instrumental and locative |
| 2 — Наклонения и обращение | 27 | 0.3591–0.3791 | optative, gerundive, imperative, vocative; the verse starts talking to *you* |
| 3 — Сравнение и производные формы | 27 | 0.3794–0.3955 | simile machinery, gerunds, causatives, negation runs |
| 4 — Свободное чтение | 26 | 0.3956–0.4063 | irony, hard morphology, long metres, capstone gnomes |

**Block boundaries are strict difficulty cuts; within a block, the four lessons are
grouped pedagogically** (by grammar topic and theme), so lesson difficulty ranges
inside one block may interleave — each lesson below states its own measured range as
the rationale. Uneven counts per lesson (6 or 7 sayings) follow the handoff's
autonomy note: difficulty grading naturally produces them. 87 of 106 sayings are
anuṣṭubh (32 syllables); the nine other metres (āryā ×7, upagīti ×6, and one each of
toṭaka, udgīti, rathoddhatā, vaṃśastha, indravajrā, āryāgīti) are deliberately spread
so that each block past the first contains at least one non-śloka verse, with the
long-metre cluster concentrated in Lesson 15.

---

## Block 1 — Опора: the śloka baseline (26 sayings, d 0.2841–0.3585)

### Lesson 1 — One case, four times: repetition as scaffold (7 sayings)

| IS | Incipit | Theme | d |
|---|---|---|---|
| 3128 | dharmeṇa hanyate vyādhir… | dharma destroys disease, demons, enemies | 0.2841 |
| 1249 | udyamena hi sidhyanti kāryāṇi | effort, not wishes, completes work | 0.2893 |
| 1727 | kiṃ kariṣyanti vaktāraḥ | what use are speakers with no hearer | 0.2964 |
| 3071 | dhaneṣu jīvitavyeṣu strīṣu… | no one has enough of wealth, life, food | 0.3076 |
| 6168 | vibhave bhojane dāne | flatterers appear where wealth is | 0.3088 |
| 6847 | samāne śobhate prītī | what befits whom: friendship, service, trade | 0.3103 |
| 291 | anityam iti jānanto | acting despite uncertain outcome | 0.3106 |

**Pedagogical focus.** Present indicative active and passive (`hanyate`, `sidhyanti`,
`śobhate`); instrumental of means (`dharmeṇa` ×4 in IS 3128, `udyamena`); locative
series (`vibhave bhojane dāne`). The signature device is anaphora — the same case
form repeated across all four pādas — so the student meets one inflection many times
before meeting many inflections once.

**Difficulty rationale.** The seven lowest-scored sayings in the pack (0.2841–0.3106),
six of seven in plain 32-syllable metre, sandhi junctions sparse (0–3 per verse),
100% RU gloss coverage. This is the softest possible entry the pack allows.

### Lesson 2 — Lists, questions, and the first gerund (7 sayings)

| IS | Incipit | Theme | d |
|---|---|---|---|
| 133 | atithir bālakaś caiva | guest, child, king, wife ask not whether you have | 0.3125 |
| 894 | ātmanā anarthayuktena | a harmed heart turns to evil | 0.3141 |
| 4669 | madirāmadamatto hi | drunk on wine vs. drunk on power | 0.3247 |
| 1941 | ko 'rthaḥ putreṇa jātena | what use is a son without virtue | 0.3259 |
| 5395 | yasya vānnāni bhuñjīta | repay whose bread you eat | 0.3361 |
| 4166 | pūrṇam induṃ yathā dṛṣṭvā | as the full moon delights the eye | 0.3379 |
| 3197 | na kāṣṭhe vidyate devo | the god is in the heart, not in wood or stone | 0.3386 |

**Pedagogical focus.** Coordination with `ca`/`caiva` in enumerations (IS 133);
the rhetorical `ko 'rthaḥ` + instrumental construction (IS 1941); `yathā … tathā`
comparison and the first absolutive (`dṛṣṭvā`, IS 4166); negated existence
`na … vidyate` (IS 3197); first relative clause with `yasya` + optative (IS 5395).

**Difficulty rationale.** Second-easiest slice (0.3125–0.3386), all anuṣṭubh, but
each verse now carries one *new* construction on top of Lesson 1's baseline —
one step, one novelty.

### Lesson 3 — Future, condition, and the first long metre (6 sayings)

| IS | Incipit | Theme | d |
|---|---|---|---|
| 866 | āgamiṣyanti te bhāvā | what is destined will come | 0.3418 |
| 4703 | mantrabhede hi ye doṣā | the harm of betrayed counsel | 0.3431 |
| 5878 | loke hi puruṣaḥ strī vā | one's own deeds make one dear | 0.3435 |
| 5209 | yadi janmajarāmaraṇaṃ na bhaved… | if there were no birth, ageing, death (toṭaka) | 0.3468 |
| 6192 | viśanti sahasā mūḍhā | fools charge the enemy line unreflecting | 0.3482 |
| 2320 | jaṅgamāni ca bhūtāni | protect moving and unmoving beings as yourself | 0.3486 |

**Pedagogical focus.** Future tense (`āgamiṣyanti`); relative–correlative
`ye … te`; the conditional `yadi` + optative (IS 5209); absolutive of negated
deliberation (`avicārya`, IS 6192). IS 5209 is also the course's first non-32-syllable
verse — toṭaka, 48 syllables — introduced here as a flagged stretch item so metre
variation stops being exotic before Block 4.

**Difficulty rationale.** Tight band 0.3418–0.3486; the lesson is one saying shorter
(6) precisely because IS 5209 costs half again as much reading as a śloka.

### Lesson 4 — Correlative pairs: block capstone (6 sayings)

| IS | Incipit | Theme | d |
|---|---|---|---|
| 584 | arthapatau bhūmipatau | speak fitting words to rich man, king, child, elder | 0.3489 |
| 435 | api śāstreṣu kuśalā | book-learned but ignorant of custom = ridiculous | 0.3501 |
| 2956 | deve tīrthe dvije mantre | as your faith, so your reward | 0.3538 |
| 6601 | ṣaṭkarṇo bhidyate mantraḥ | counsel heard by six ears leaks | 0.3564 |
| 3537 | nākāraṇaruṣāṃ saṅkhyā | countless are those who anger without cause | 0.3567 |
| 6681 | sa jāto yena jātena | truly born is he who raises his family | 0.3585 |

**Pedagogical focus.** The correlative system in full: `yādṛśī … tādṛśī` (IS 2956),
`sa … yena` (IS 6681); concessive `api` (IS 435); bahuvrīhi with numerals
(`ṣaṭkarṇaḥ`, IS 6601); extended locative series as frame (IS 584, udgīti metre —
second controlled metre variation).

**Difficulty rationale.** The top of Block 1 (0.3489–0.3585). Ends the block on
correlatives because Block 2's prescriptive verses lean on them constantly.

---

## Block 2 — Наклонения и обращение (27 sayings, d 0.3591–0.3791)

### Lesson 5 — The grammar of "should": optative and gerundive (6 sayings)

| IS | Incipit | Theme | d |
|---|---|---|---|
| 7058 | sukule yojayet kanyāṃ | place daughter, son, friend, each where they belong | 0.3591 |
| 7215 | strīṣu goṣu na śastrāṇi | never raise a weapon against women, cows, brahmins | 0.3650 |
| 6674 | saṅgaḥ sarvātmanā tyājyaḥ | renounce attachment — or attach to the good | 0.3663 |
| 3532 | nahy avijñātaśīlasya | shelter no one of unknown character | 0.3748 |
| 4065 | pitācāryaḥ suhṛn mātā | no one is beyond punishment | 0.3783 |
| 1653 | kāmaḥ sarvātmanā heyaḥ | renounce desire — or desire your own wife | 0.3786 |

**Pedagogical focus.** The two prescriptive devices of gnomic Sanskrit: optative
(`yojayet`, `pātayet`) and gerundive (`tyājyaḥ`, `heyaḥ`, `pradātavyaḥ`, `adaṇḍyaḥ`).
IS 6674 and IS 1653 are a deliberate minimal pair — identical `sarvātmanā X-yaḥ, sa
cet … na śakyate` frame with different lexical filling — the pack's clearest built-in
substitution drill.

**Difficulty rationale.** Opens Block 2 at its floor (0.3591) and is kept to 6 items
because two new verb categories arrive at once.

### Lesson 6 — The verse speaks to you (7 sayings)

| IS | Incipit | Theme | d |
|---|---|---|---|
| 5201 | yadā satsaṅgarahito bhaviṣyasi | lose good company and you *will* fall in with the bad | 0.3626 |
| 1952 | ko hi nāma kule jātaḥ | who of good birth sells himself for a scrap of comfort | 0.3666 |
| 7583 | paṭha putra kim ālasyam | study, my son — the unlearned carries loads | 0.3686 |
| 1899 | ke khalu nayanavihīnāḥ | who are the truly blind? say, o say! | 0.3699 |
| 1990 | kva nu te 'dya pitā rājan | where now, king, are your fathers? | 0.3706 |
| 975 | ā maraṇād api virutaṃ | crows screeching till death never become peacocks | 0.3735 |
| 1650 | kāma jānāmi te mūlaṃ | o Desire, I know your root | 0.3780 |

**Pedagogical focus.** Second-person address: imperative (`paṭha`, `vada vada`),
vocatives (`putra`, `rājan`, `kāma`), 2nd-person future (`bhaviṣyasi` ×2 as
refrain), interrogatives `ke / kva / kiṃ` in rhetorical volleys, and the ablative
frame `ā maraṇād api`. After two blocks of third-person gnomes, the register shift
to direct address is itself the lesson.

**Difficulty rationale.** Mid-Block-2 band (0.3626–0.3780); the new burden is
pragmatic (speech situation), not morphological, so 7 items are safe.

### Lesson 7 — Parallel worlds: nature mirrors society (7 sayings)

| IS | Incipit | Theme | d |
|---|---|---|---|
| 1584 | kaviḥ karoti kāvyāni | the poet makes, the connoisseur judges | 0.3596 |
| 2128 | guṇāḥ kurvanti dūtatvaṃ | virtues act as messengers, like fragrance to bees | 0.3638 |
| 2087 | gamyate yadi mṛgendramandiraṃ | enter a lion's den, find a pearl; a jackal's, a tail | 0.3650 |
| 1281 | upakāriṣu yaḥ sādhuḥ | goodness toward the harmful is the real goodness | 0.3690 |
| 1277 | upakāraḥ kṛtajñeṣu | service to the grateful earns return | 0.3739 |
| 2089 | garjati śaradi na varṣati | autumn cloud thunders without rain; the base talk | 0.3765 |
| 2366 | jalena jāyate paṅkaṃ | water makes mud and washes it away | 0.3769 |

**Pedagogical focus.** Agent nouns in -tṛ/-aka and abstract `-tva` (`vaktā`,
`dūtatvam`); impersonal passive (`gamyate`, `labhyate`, IS 2087 — rathoddhatā, 44
syllables, this block's metre stretch); strict two-panel parallelism (nature panel ‖
society panel) as the dominant rhetorical form of subhāṣita literature. IS 1281/1277
form a same-root contrast pair (`upakārin`/`upakāra`).

**Difficulty rationale.** Spans 0.3596–0.3769; morphology is familiar from Lessons
1–5, the added load is tracking the two-panel mapping across pādas.

### Lesson 8 — Abstraction: from proverb to philosophy (7 sayings)

| IS | Incipit | Theme | d |
|---|---|---|---|
| 2757 | dānaṃ bhogo nāśas | gift, enjoyment, loss — wealth's three fates | 0.3592 |
| 1714 | kāṣṭhapāṣāṇadhātūnāṃ | worship images with warm heart, gain through faith | 0.3612 |
| 2434 | jīvitaṃ ca śarīreṇa | life and body arise and end together | 0.3622 |
| 5399 | yasya saṃsāriṇī prajñā | wisdom that prefers the useful to the pleasant | 0.3669 |
| 2718 | darśane sparśane vāpi | when seeing, touching, hearing melts the heart — love | 0.3684 |
| 2748 | dātṛtvaṃ priyavaktṛtvaṃ | generosity and tact cannot be drilled | 0.3790 |
| 3247 | na jāyate mriyate vā | nothing is born, nothing dies — Brahman unfolds | 0.3791 |

**Pedagogical focus.** Abstract derivation as a system: `-tva` chains
(`dātṛtvaṃ priyavaktṛtvaṃ dhīratvam`), action-noun locatives (`darśane sparśane
śravaṇe bhāṣaṇe`), `saha` + instrumental, and the philosophical register of IS 3247
(vedāntic negation) as the block's conceptual ceiling. IS 2757 and 2718 are āryā /
upagīti — the moraic metres get normalized here.

**Difficulty rationale.** Closes Block 2 at its top edge (0.3790–0.3791 for the two
hardest items); vocabulary is more abstract than anything earlier, which is exactly
what the score drift within the band reflects.

---

## Block 3 — Сравнение и производные формы (27 sayings, d 0.3794–0.3955)

### Lesson 9 — The simile machine (7 sayings)

| IS | Incipit | Theme | d |
|---|---|---|---|
| 2084 | gandhena gāvaḥ paśyanti | cows see by smell, kings by spies, brahmins by Veda | 0.3794 |
| 1420 | ekeṣāṃ vāci śukavat | parrot-speech vs. mute hearts | 0.3823 |
| 3990 | parjanya iva bhūtānāṃ | the king, like the rain-god, sustains all | 0.3826 |
| 2069 | gatir ātmavatāṃ santaḥ | the good are the refuge of the good | 0.3840 |
| 5125 | yathā bījāṅkuraḥ sūkṣmaḥ | like a tended seedling, service bears fruit in time | 0.3867 |
| 5453 | yādṛg-guṇena bhartrā | as the husband, so the wife — river and ocean | 0.3893 |
| 6365 | śateṣu jāyate śūraḥ | one hero in hundreds, one speaker in hundred thousands | 0.3928 |

**Pedagogical focus.** Every formal device Sanskrit owns for comparison, in one
place: bare instrumental of standard (`gandhena`), suffix `-vat` (`śukavat`),
particle `iva`, full `yathā … tathā` clauses, correlative `yādṛś-/tādṛś-` compounds,
plus chiasmus (IS 2069) and the numeric-climax pattern with locative of population
(IS 6365).

**Difficulty rationale.** Block 3 floor upward (0.3794–0.3928); each verse doubles a
known theme with a new comparison syntax, keeping the novelty purely structural.

### Lesson 10 — Chains of action: gerund, causative, agent (7 sayings)

| IS | Incipit | Theme | d |
|---|---|---|---|
| 3205 | na kṛtasya ca kartuś ca | wronged and wrongdoer never mend friendship | 0.3886 |
| 4814 | mānaṃ hitvā priyo bhavati | drop pride, be loved; drop anger, cease to grieve | 0.3916 |
| 7136 | suvyāhṛtāni dhīrāṇāṃ | weigh the wise's words, then act | 0.3927 |
| 1866 | kṛtasya karaṇaṃ nāsti | the done needs no doing, the dead no dying | 0.3938 |
| 4489 | bodhayanti na yācante | true mendicants remind, not beg | 0.3942 |
| 485 | abhayaṃ sarvabhūtebhyo | give safety to all beings, receive fearlessness | 0.3944 |
| 471 | apriyasya prathamataḥ | who dares say the unpleasant-but-wholesome | 0.3952 |

**Pedagogical focus.** Derived verb morphology as the core: absolutives as sequencers
(`hitvā` ×3 in IS 4814, `paricintya` in IS 7136), the first causative
(`bodhayanti`, IS 4489), agent noun `kartṛ` beside action noun `karaṇa` and
participle `kṛta` from one root (IS 3205 + 1866 — a single-root paradigm lesson),
dative of purpose/recipient (`sarvabhūtebhyaḥ`), adverbial `-tas` (`prathamataḥ`,
`phalataḥ`).

**Difficulty rationale.** The dense upper-middle of Block 3 (0.3886–0.3952); scores
here track exactly the morphological derivation load this lesson teaches.

### Lesson 11 — Seeing and not seeing: negation runs (7 sayings)

| IS | Incipit | Theme | d |
|---|---|---|---|
| 3527 | nahīdṛśaṃ saṃvananaṃ | nothing wins hearts like compassion and friendship | 0.3845 |
| 3336 | na paśyati ca jātyandhaḥ | four kinds of blindness — born, love, pride, greed | 0.3848 |
| 2389 | jātismarāṇi netrāṇi | eyes remember: they melt at the dear, narrow at the foe | 0.3852 |
| 5361 | yasya kṛtyaṃ na jānanti | whose plan is known only from its result | 0.3858 |
| 6414 | śaraṇaṃ kiṃ prapannāni | the miser guards wealth he will never use | 0.3858 |
| 4901 | muner api vanasthasya | even the forest sage has friends and foes | 0.3868 |
| 3371 | na mātā śapate putraṃ | a mother curses not her son; the good harm no one | 0.3912 |

**Pedagogical focus.** Negation as rhetoric: fourfold `na paśyati` anaphora
(IS 3336), the `na X, na Y, na Z` catalogue (IS 3371), `nahi` + `īdṛśa` (IS 3527),
concessive `api` at climax (`muner api`, IS 4901), and perception verbs (`paś`,
`jñā`, `smṛ`) as the unifying lexical field.

**Difficulty rationale.** The tightest difficulty cluster in the whole pack —
five of seven sayings within 0.3845–0.3868 — grouped here so the (real) jump to
Lesson 12's capstone is felt as register, not lexicon.

### Lesson 12 — Staged voices: block capstone (6 sayings)

| IS | Incipit | Theme | d |
|---|---|---|---|
| 2057 | gaccha gacchasi cet kānta | go then, beloved — and be born where I am | 0.3816 |
| 3042 | dhanadhānyaprayogeṣu | in lending, learning, eating — drop shame | 0.3842 |
| 837 | aho bata vicitrāṇi | how strange the ways of the great: Lakṣmī, a straw | 0.3895 |
| 5580 | ye sma kāle sumanasaḥ | honour the old in good time | 0.3925 |
| 2410 | jāyā vā syāj janitrī vā | o ingrates — you owe woman your very existence | 0.3926 |
| 5577 | yeṣu kāryeṣu vidyeta | quick gain, ruinous outcome — the wise refuse | 0.3955 |

**Pedagogical focus.** Dramatized speech inside gnomic frames: the lover's farewell
with doubled imperative + `cet` (IS 2057), exclamation `aho bata` + dative of regard
(`lakṣmīṃ tṛṇāya manyante`, IS 837), vocative rebuke of an addressed group (`he
kṛtaghnāḥ`, IS 2410), optatives `syāt` / `vidyeta` in generalized conditions.

**Difficulty rationale.** Reaches the exact Block 3 ceiling (0.3955, IS 5577); 6
items because two verses (2057, 2410) demand real interpretive discussion — who
speaks, to whom, and why.

---

## Block 4 — Свободное чтение (26 sayings, d 0.3956–0.4063)

### Lesson 13 — Irony and the double edge (7 sayings)

| IS | Incipit | Theme | d |
|---|---|---|---|
| 1892 | kṛpaṇena samo dātā | none so generous as the miser — he leaves all behind | 0.3960 |
| 2436 | jīvitāśā balavatī | go or stay — my longing is for life, not wealth | 0.3963 |
| 2805 | divā paśyati nolūkaḥ | owl blind by day, crow by night — the love-blind always | 0.3975 |
| 4579 | bhāvaśuddhir manuṣyais tu | purity of intent — or you kiss your own kin otherwise | 0.3977 |
| 2420 | jihvā dagdhā parastutyā | tongue burnt by flattery, hands by taking | 0.4008 |
| 2560 | tilamātrasukhārthaṃ hi | a sesame-grain of pleasure against a Meru of loss | 0.4032 |
| 3062 | dhanādhikeṣu khidyante | fools courting the rich: warming at a painted fire | 0.4037 |

**Pedagogical focus.** Reading against the grain: verses whose surface statement is
false or mocking (`kṛpaṇena samo dātā`). Grammar served: `sama` + instrumental,
`-mātra` and `-artham` compounds, past participle runs (`dagdhā` ×3, IS 2420), and
the climactic-comparison template. The comprehension skill is detecting that the
grammar is easy but the meaning is inverted.

**Difficulty rationale.** Block 4 entry band (0.3960–0.4037); scores here are driven
by lexical range and inference, matching the lesson's stated skill.

### Lesson 14 — Hard morphology: r-stems, imperfect, dense sandhi (7 sayings)

| IS | Incipit | Theme | d |
|---|---|---|---|
| 2452 | jñānamantrasadācārair | the teacher earns honour; the pupil must never wound him | 0.3956 |
| 5370 | yasya tasya hi kāryasya | time drinks the juice of the unfinished deed | 0.3973 |
| 2178 | guruśuśrūṣayā vidyā | knowledge: by service, by wealth, or by knowledge | 0.3985 |
| 4809 | mātrā svasrā duhitrā vā | sit not alone even with mother, sister, daughter | 0.4038 |
| 730 | aśvamedhasahasraṃ ca | truth outweighs a thousand horse-sacrifices | 0.4046 |
| 1657 | kāmābhibhūtaḥ krodhād vā | falseness to one's own — the ruined man | 0.4050 |
| 2133 | guṇānām antaraṃ prāyas | only the connoisseur tells jasmine from jasmine | 0.4050 |

**Pedagogical focus.** The pack's concentrated morphology and sandhi tail: irregular
r-stem instrumentals `mātrā svasrā duhitrā` (IS 4809), the one imperfect in the
course (`atyaricyata`, IS 730), `tasmāc chiṣyaḥ` (t + ś assimilation, IS 2452), and
IS 1657 with five labelled sandhi junctions — the pack's maximum. `yasya tasya`
as indefinite idiom.

**Difficulty rationale.** Contains four of the pack's eight hardest scores
(0.4038–0.4050); the difficulty is demonstrably formal (junction counts, rare
inflection), so it is met with explicit tools, not exposure alone.

### Lesson 15 — Beyond the śloka: long metres and allusion (6 sayings)

| IS | Incipit | Theme | d |
|---|---|---|---|
| 7508 | krameṇa bhūmiḥ salilena | step by step: water splits earth, learning is gained (vaṃśastha, 48 syl) | 0.3964 |
| 1286 | upadeśo na dātavyo | advise not just anyone — remember the monkey and the sparrow | 0.3966 |
| 2763 | dānena pāṇir na tu kaṅkaṇena | giving adorns the hand, not bracelets (indravajrā, 44 syl) | 0.3982 |
| 2978 | daivavaśād upapanne sati | wealth arrived, yet no wish to enjoy or give (āryā, 40 syl) | 0.3988 |
| 5938 | vapuḥ śīlaṃ kulaṃ vittaṃ | beauty, character, birth, wealth — the fortunate seven | 0.3989 |
| 7126 | suramandirataru-mūla-nivāsaḥ | the ascetic's inventory: tree-root, earth-bed, deer-skin (āryāgīti, 43 syl) | 0.4027 |

**Pedagogical focus.** The pack's long-metre cluster in one sitting — vaṃśastha,
indravajrā, āryā, āryāgīti — read aloud against the now-automatic anuṣṭubh; the
course's one locative absolute (`upapanne sati vibhave`, IS 2978); and IS 1286 as
the pack's only *allusive* verse, whose point rests on a fable outside the text
(the monkey and the sparrow) — an explicit exercise in recognizing when a verse
presupposes a story.

**Difficulty rationale.** Scores 0.3964–0.4027 despite mostly familiar grammar: the
measured difficulty is metrical length and cultural reference, which is precisely
what the lesson isolates.

### Lesson 16 — Capstone: the summary gnomes (6 sayings)

| IS | Incipit | Theme | d |
|---|---|---|---|
| 2638 | trayaḥ sthānaṃ na muñcanti | three never leave their post: crows, cowards, deer | 0.3996 |
| 5375 | yasya na jñāyate śīlaṃ | befriend no one whose character is unknown | 0.4017 |
| 1606 | kasya doṣaḥ kule nāsti | whose family is flawless? who never ill? | 0.4018 |
| 5772 | rājyaṃ ca saṃpado bhogāḥ | kingdom, wealth, beauty — all fruit of merit | 0.4022 |
| 4897 | muṇḍe muṇḍe matir bhinnā | every head its own opinion, every well its own water | 0.4051 |
| 954 | āpatsu mitraṃ jānīyād | in misfortune know the friend, in battle the hero | 0.4063 |

**Pedagogical focus.** Fully autonomous reading of catalogue gnomes: numeral subjects
(`trayaḥ`), passive `jñāyate` beside optative `jānīyāt` of the same root, question
cascades (IS 1606), and the āmreḍita distributive doubling `muṇḍe muṇḍe … kuṇḍe
kuṇḍe` (IS 4897). The course ends on IS 954 — the pack's single hardest saying
(0.4063) and one of the most-quoted subhāṣitas in the tradition — as the exit
benchmark: read, parse, and translate it unassisted.

**Difficulty rationale.** The pack's terminal difficulty band (0.3996–0.4063),
including its absolute maximum. Nothing in the lesson introduces new grammar; it
certifies accumulated competence.

---

## Coverage check

26 + 27 + 27 + 26 = **106 sayings; every pack item appears in exactly one lesson;
no item appears twice; nothing outside the pack is used.** Per-lesson counts:
7·7·6·6 | 6·7·7·7 | 7·7·7·6 | 7·7·6·6. Anyone re-verifying should diff the IS
numbers above against the `num` fields of
[subhashita_beginner_pack.json](https://github.com/gasyoun/kosha/blob/main/data/subhashita/subhashita_beginner_pack.json).

## Cross-reference: lesson numbering vs. the H2168 reader wiring

[H2168](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2168-Opus_Systema-Sanscriticum_nala-subhashita-reader-wiring_02.08.26.md)
(Opus 5) — Generalize ReadingPackController to multi-course multi-pack — wires the
Subhāṣita course in-cabinet as a **single pack** (`subhashita-beginner`), unlike
Nala's three sequential packs. Consequences for numbering, so students see one
consistent scheme:

1. **In-cabinet, the student sees ONE reading pack**, not sixteen; Lessons 1–16 are
   a curriculum overlay on that single pack. The per-lesson IS-number lists above
   are the canonical slice definition — a lesson *is* its list of `num` values.
2. **`Lesson` DB records** (the human/Filament step of PLAN D12, explicitly out of
   scope here and for H2168) should be created as Lesson 1…16 in this document's
   order, each carrying its IS numbers verbatim; the reader then filters the single
   pack by `num`. No re-numbering layer may be introduced between this document and
   the DB — Lesson N here is Lesson N in-cabinet.
3. **Block boundaries carry no wiring**: unlike Nala's pack-per-stage unlock
   (sequential by default per H2168's autonomy note), Subhāṣita blocks 1–4 are
   pedagogical groupings inside one entitlement; if per-lesson gating is ever
   wanted, it gates on lesson index, not on pack slug.

## Further reading — checked, not used

MG pointed at the samskrtam.ru subhāṣita page
([samskrtam.ru/subhashita/](https://www.samskrtam.ru/subhashita/), "100 prechosen
subhashitas") during planning. It was **checked, and deliberately not used**: the
page is a gateway to two external collections — (a) the **Usha Sanki 95-audio
compilation** distributed via Dropbox, and (b) a **Kochergina-textbook-derived
collection** distributed as Word documents. Both are external audio/Word artifacts,
not machine-fetchable, with no difficulty scores and no RU token glosses. Per
[H2169](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2169-Fable_SanskritGrammar_subhashita-16-lesson-plan_02.08.26.md)'s
context ruling, kosha's own scored and glossed pack is the stronger, self-sufficient
asset; the two collections remain **further reading / future audio prior-art**, and
this curriculum makes no claim that audio recordings exist for any of its 106 items
(none do yet). An Anki export of the same pack already exists:
[subhashita_beginner_anki.apkg](https://github.com/gasyoun/kosha/blob/main/data/subhashita/subhashita_beginner_anki.apkg).

Sibling curriculum in this repo:
[CURRICULUM_START_CHTENIYA_W1_W5.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/CURRICULUM_START_CHTENIYA_W1_W5.md).

_Dr. Mārcis Gasūns_
