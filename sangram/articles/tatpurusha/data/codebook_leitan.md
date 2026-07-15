# Compound-type codebook (Sangram P4, SG-WF-008) — Leitan / Pāṇinian arrangement

_Created: 15-07-2026 · Last updated: 15-07-2026_

Annotation codebook for the two independent classification passes of pilot P4. Anchored on **Edgar Leitan (Э. З. Лейтан)**, Pāṇinian/Mahābhāṣya arrangement (per author ruling 15-07-2026). Both passes apply this codebook verbatim, blind to each other; Cohen κ over the two label vectors is the C5 §7 P4 kill-gate (κ < 0.7 → revise taxonomy). This is a **machine-annotator** codebook — every label is model-provisional and flagged for scholarly sign-off.

## Task

Each item is a **2-member compound** reconstructed from DCS: `member1` (the `Case=Cpd` non-final member) + `head` (the inflected final member). You are given both members' unsandhied forms and lemmas, the head's external case (this is how the *whole compound* is used in the sentence — **not** its internal type), the head's dictionary grammar, and the sentence context.

Assign **two labels** per compound:
- **`coarse`** — one of the five Mahābhāṣya classes (or `unclear`).
- **`fine`** — if and only if `coarse = tatpuruṣa`, the Leitan tatpuruṣa subtype; otherwise `n/a`.

Rules:
1. **Parse right-to-left**: the `head` (right member) is the semantic head for tatpuruṣa; classify by the relation of `member1` to the `head`.
2. Determine the class by the implied **vigraha** (analytic paraphrase): mentally expand the compound and see which member dominates.
3. The head's *external* case is a distractor — ignore it for the internal type; the vibhakti that matters is `member1`'s relation to the head.
4. Keep Sanskrit in IAST. Give a one-line rationale + the vigraha you assumed.

## Tier 1 — coarse (5 classes + unclear)

| label | Pāṇinian defn | test | example |
|---|---|---|---|
| `tatpuruṣa` | uttarapadārtha­pradhāna — right member dominant (determinative). **Includes karmadhāraya and dvigu** per Leitan. | member1 qualifies/depends on head; the whole *is a kind of* head | `rāja-sevaka` (servant of the king) |
| `bahuvrīhi` | anyapadārtha­pradhāna — an **external** referent dominates (possessive/exocentric) | the compound denotes something *other than* either member: "one whose … is …" | `pīta-ambara` (he whose garment is yellow = Viṣṇu) |
| `dvandva` | ubhayapadārtha­pradhāna — both members equal (copulative) | vigraha joins with "and": "X and Y" | `rāma-kṛṣṇau` (Rāma and Kṛṣṇa) |
| `avyayībhāva` | pūrvapadārtha­pradhāna — left member dominant, result indeclinable/adverbial | left is usually a preposition/particle (upa-, yathā-, prati-, anu-, nir-, su-); whole is adverbial | `yathā-śakti` (according to capacity) |
| `kevala-samāsa` | idiomatic, not resolvable by standard rules (Pān. 2.1.4) | meaning is lexicalized, vigraha does not recover it | `ā-janma-śuddha` (pure from birth) |
| `unclear` | evidence insufficient to decide | — | — |

## Tier 2 — fine (Leitan's tatpuruṣa subtypes; only when coarse = tatpuruṣa)

**Vibhakti-tatpuruṣa (vyadhikaraṇa)** — by the case of member1 in the vigraha:

| label | case of member1 | vigraha pattern | Leitan example |
|---|---|---|---|
| `tat-prathamā` | nominative (rare) | pūrvaṃ X-sya | `pūrva-kāya` (front of body) |
| `tat-dvitīyā` | accusative | X-am [p.p.p. / kṛt] | `grāma-gata` (gone to the village) |
| `tat-tṛtīyā` | instrumental | X-ena | `dhānya-artha` (wealth by grain) |
| `tat-caturthī` | dative | X-āya (with artha, bali, hita, sukha, rakṣita) | `yūpa-dāru` (wood for the sacrificial post) |
| `tat-pañcamī` | ablative | X-āt (with bhaya, bhīta) | `caura-bhaya` (fear of/from a thief) |
| `tat-ṣaṣṭhī` | genitive | X-sya | `rāja-sevaka` (servant of the king) |
| `tat-saptamī` | locative | X-i (with śauṇḍa, dhūrta, nipuṇa, siddha) | `akṣa-śauṇḍa` (skilled at dice) |

**Samānādhikaraṇa & special:**

| label | defn | test | Leitan example |
|---|---|---|---|
| `karmadhāraya` | samānādhikaraṇa-tatpuruṣa — both members in the **same** case in vigraha (adj+noun, apposition, simile) | "X which is [also] Y", "Y like X" | `tuṅga-vṛkṣa` (tall tree); `megha-śyāma` (dark as a cloud) |
| `dvigu` | numeral-initial karmadhāraya (saṃkhyā-pūrva) | member1 is a numeral, collective/taddhita sense | `pañca-gava` (five cows [as a set]) |
| `nañ` | negation (a-/an-/na-) | member1 = negating a-/an- | `a-brāhmaṇa` (non-brahmin) |
| `prādi` | prefixal (pra-, parā-, apa-, vi-, ni-, ā- …), often elided verb | member1 = pra-class prefix | `pra-ācārya` → prācārya (eminent teacher) |
| `gati` | special non-verbal prefix (puras-, tiras-, …) | member1 = gati particle | `puras-kāra` (honouring) |
| `upapada` | head is a **kṛt** (primary verbal derivative) needing member1 as its object/complement | head lemma is deverbal (-a, -in, -jit, -kara, -ga …); member1 is its argument | `kumbha-kāra` (potter); `prameha-jit` (conqueror of prameha) |
| `tat-other` | aluk (case-ending retained), madhyamapadalopin (middle elided), or otherwise tatpuruṣa but none above | — | `vane-cara` (forest-wanderer, aluk) |

## Output (per compound)

`{cpd_token_id, coarse, fine, vigraha, rationale}` — `fine="n/a"` unless `coarse="tatpuruṣa"`.

_Dr. Mārcis Gasūns_
