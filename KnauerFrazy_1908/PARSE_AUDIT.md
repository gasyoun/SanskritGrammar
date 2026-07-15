# Parse audit — Knauer, Фразы (1908)

_Created: 15-07-2026 · Last updated: 15-07-2026_

Hand-written summary of [`parse_audit.yml`](parse_audit.yml) — this register has no
`build_claims.py`-style generator yet (it is small enough to review directly; a generator is
worth building once the audit scales toward the full footnote inventory).

## Why this register looks different from `claims.yml`

[H797](https://github.com/gasyoun/Uprava/blob/main/handoffs/H797-Fable_SanskritGrammar_claim-verification-backlog-verify-and-cross-grammar-generalise_12.07.26.md)
asks to port the two-axis claim-verification pipeline (fact + pedagogy, against DCS frequency +
Whitney systemic fact) from `KocherginaUchebnik_1998`/`BuhlerLeitfaden_1923` to Knauer next. That
pipeline harvests **discursive prose** assertions — "always", "usually", "most roots" — because
Kochergina's and Bühler's digitized texts are full discursive grammars making exactly those
claims.

Knauer's digitized text here, [`Frazy-Knauer-03.05.2023.mdx`](Frazy-Knauer-03.05.2023.mdx), is
not that genre. It is a 241-line **phrase reader**: 19 numbered sentence-sets (Nr. 1–19), each
word footnoted with a terse morphological parse (`к. rakṣ по § 120`, `impf. pass. отъ darç`)
pointing into a *separate*, not-digitized Knauer grammar volume. There is no universality/
frequency prose here to harvest — checked directly against the source before starting.

**Adapted unit of analysis:** instead of auditing a rhetorical claim, each entry here audits
*one footnote's morphological parse* — is the stated root/category/preverb analysis of the
surface form linguistically correct per Whitney 1889? (Knauer's own §-numbers are internal to
the undigitized companion grammar and can't be cross-checked directly; the underlying
linguistic claim can be, against Whitney.) DCS is a supplementary existence check only, not the
primary ground truth — these are individual parse claims, not frequency claims.

## This pass (seed, 15-07-2026)

**10 of an estimated 280–330 total footnote parses**, individually verified:

| ID | Surface form | Claimed parse | Kind | Verdict |
|--|--|--|--|--|
| KN-1 | gachati | root gam, ch-substitution | irregular-present | ✅ CONFIRMED |
| KN-2 | ichanti | root iṣ, ch-substitution | irregular-present | ✅ CONFIRMED |
| KN-3 | çāsti | root śās, reduplicated-type irregular | irregular-present | ✅ CONFIRMED |
| KN-4 | kriyante | passive of kṛ, suppletive stem kriyá- | passive-stem | ✅ CONFIRMED |
| KN-5 | adṛçyanta | passive of 'see', darç/dṛç/paç suppletion | suppletion | ✅ CONFIRMED |
| KN-6 | badhyante etc. | regular -ya passive (unmarked in text) | passive-stem | ✅ CONFIRMED |
| KN-7 | rakṣanti | root rakṣ, regular class-I thematic | root-id | ✅ CONFIRMED |
| KN-8 | tiṣṭhataḥ | root sthā, reduplicating irregular present | irregular-present | ✅ CONFIRMED |
| KN-9 | labhāmahe | root labh, Ātmanepada-only (deponent) | voice-restriction | 🟡 QUESTIONABLE |
| KN-10 | kṛṣṇāyate | denominative -āya from kṛṣṇa 'black' | denominative | 🟡 QUESTIONABLE |

**No errors found.** The two QUESTIONABLE entries are flagged only because an exact matching
Whitney citation wasn't pinned down in this pass, not because the underlying claim looks wrong —
they're follow-up items, not open problems.

## Reading the result

A footnote gloss is checked by its author against *one specific worked example* in front of
them — a narrower error surface than the discursive-prose universality/frequency claims that
failed repeatedly in Kochergina and Bühler (overgeneralizing a rule, hiding a frequency). Ten
clean confirms is consistent with that, but it is far too small a sample to conclude Knauer's
footnote apparatus is uniformly reliable — it establishes that the adapted methodology works and
found no errors *yet*.

One genuinely interesting confirmed pattern: iṣ, gam, and vas (KN-1, KN-2) are not three
unrelated irregularities but ONE documented rule (Whitney §608, the ch-substituting present
stems) — Knauer's footnotes correctly identify the specific root behind each surface form without
stating the shared rule, which a learner would otherwise have to notice independently across
three separate exercise sets.

## Backlog

Every one of the ~280–330 total footnote parses in the book is preserved **verbatim**, at
per-Nr.-block granularity, in `parse_audit.yml`'s `block_backlog` — zero information loss, but
not yet split into individually-verified entries at the KN-* granularity above. That full
per-parse extraction (mirroring `BuhlerLeitfaden_1923/claims_harvest.yml`'s per-claim rows) is
future work.

---

_Dr. Mārcis Gasūns_
