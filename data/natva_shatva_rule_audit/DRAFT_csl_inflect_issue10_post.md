# DRAFT comment for csl-inflect #10 — DO NOT POST (MG posts; kosha RELATIONS.md §2/§7 diplomacy gate)

_Status: draft v2 (H6054, 06-10-2026). Updates the H185 draft with the
rule-vs-fact cell audit: exact per-cell matrix, śaṭva contrast row, and DCS
attestation counts. Single on-its-merits comment, no bot framing._

---

Following the Cologne-vs-Huet comparison here, I ran an independent
**vidyut-prakriya** comparison over 10,000 entry-bearing nominal stems
(~240k case×number cells) as a third data point, then audited every
ṇatva-divergent cell against the shipped MWinflect `calc_tables.txt`
(sha256-pinned) and against DCS corpus attestation. Agreement with the
Cologne tables is **90.5 %**; the divergences group cleanly.

**The systematic class is n↔ṇ only.** In the top-10k sample the retroflexion
gap is **326 cells over 89 stems (55 lemmas)**; re-checking each cell, mapping
ṇ→n makes the two engines' form sets equal in **326/326** cases — every other
character, ś included, is identical. Two rule contexts produce the gap:

- **Monosyllabic final compound member** (121 cells, 27 of the 89 paradigms) —
  `nṛ-pa`, `tura-ga`, `ura-ga`, `śatru-ghna`…: the tables emit
  `-ena`/`-ānām`/`-āni` where the 8.4.12 antaraṅga rule (as drdhaval2785 set
  out in [MWinflect#6](https://github.com/sanskrit-lexicon/MWinflect/issues/6))
  retroflexes across the member boundary. This is the known #6 class; the
  blast radius is larger than the 69 enumerated there — 57 of these 89
  paradigms (36 distinct key2 stems) already sit in the 2019
  `diff_nopada_m_a.txt` list.
- **key2 hyphen splits with polysyllabic finals** (205 cells, 62 paradigms) —
  `pra-Bu`, `nir-Baya`, `cakravAka`, `antaryAmin`…: declining the key2 final
  pada in isolation suppresses ṇ where the single-pada analysis of
  upasarga/kṛt/secondary-suffix formations applies it. This subclass is a
  genuine analytical fork rather than a clear bug — flagged, not asserted.

**The same paradigms apply śaṭva correctly**: all 89 stems' loc.pl forms in
the shipped tables carry ṣ (`nṛpeṣu`, `prabhuṣu`, `śatrughneṣu`), so the gap
is specific to triggers sitting before the key2 hyphen — the final-pada scope
cannot see them.

**Corpus weight** (DCS form→lemma): for the 326 cells, the retroflexed
spelling has attestation rows in 217 cells vs 74 for the unretroflexed one
(166 ṇ-only · 51 both · 23 n-only · 86 unattested either way) — e.g.
`cakravākeṇa`'s ṇ spelling is attested while the plain-n one is not, though
`śatru-ghna`'s is not, in the other direction.

Happy to share the per-cell divergence table (326 rows: rule form, table form,
key2 stem, rule class, attestation counts) if useful for the Huet comparison
programs.
