# SIGNOFF A64 — author-voice pass

_Created: 06-09-2026 · Last updated: 06-09-2026_

**Scope.** Manuscript: [DRAFT_compound-type-kappa_A64.md](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/CompoundTypeKappa_A64/DRAFT_compound-type-kappa_A64.md) (English venue-paper draft, readiness 3/5). Handoff: [H3857](https://github.com/gasyoun/Uprava/blob/main/handoffs/H3857-Fable_Uprava_all-articles-author-voice-pass-workflow_01.09.26.md). Pass 1, 06-09-2026, Fable 5.1 (`claude-fable-5-1`). Voice, register and framing only; no number, claim or citation altered; mechanical drift gate (`voice_drift_check.py --git origin/main`) CLEAN: numbers 125 = 125, URLs 15 = 15, citations 4 = 4, IAST tokens 78 = 78, headings 10 = 10. No review memo existed for this paper; no prior signoff.

**Assessment before rewriting.** The draft was already tight on substance and free of most de-AI markers (no fake candour, no filler intensifiers beyond those that carry measured magnitude, no triplet padding). The defects were of four kinds: (1) sole-author paper written in editorial "we"; (2) bold applied to whole sentences for emphasis (abstract caveat, § 1 question, § 2 gap claims, § 3 universe, § 5 caveat); (3) a run of "not X but Y" / "X, not Y" constructions, several stacked with double em-dashes into one sentence (§ 1 question sentence, § 2 gap sentence, § 4 coarse-tier disagreement sentence); (4) em-dash appositions used as copula ("— a finding that", "— a pattern that", "— a documented divergence", "— a genuine open question"). No academic byline block. The question posed in § 1 and the answer in § 6 were already aligned; the title matches what the paper shows.

## 1. Voice calls made — each may be vetoed

| # | Location | Call | Rationale |
|---|---|---|---|
| 1 | Header | `Last updated` 22-07-2026 → 06-09-2026 | Brief rule; `Created` kept (git first-add is 23-07-2026, header says 22-07-2026 — left as authored). |
| 2 | Header, after the status line | Added the academic byline block (Mārcis Gasūns, independent scholar, ORCID, email) | Absent; brief requires it. Closing `_Dr. Mārcis Gasūns_` kept as repo file-closer convention. |
| 3 | Abstract, § 2 (×4), § 3, § 5 | "We"/"our" → "I"/"my", 9 occurrences | Sole-author paper; first-person singular per the voice standard. Venue not yet chosen, so this is reversible if the venue mandates "we". |
| 4 | Abstract | Bold removed from the same-family caveat sentence; "— the lower bound falls under the threshold" → "; the lower bound…" | Whole-sentence bold reads as shouting; the sentence carries itself. Wording otherwise verbatim. |
| 5 | § 1, EM4 sentence | "— evidence-limit **EM4** in…" → ", which is evidence-limit EM4 in…" | Em-dash copula and bold on an identifier. |
| 6 | § 1, research-question sentence | One double-em-dash sentence with a bolded quoted question and an arrow-notation kill-gate → three sentences: the gap requires manual classification; the question is not the distribution but its reliability and grain; reliability is measured as inter-pass κ against the pre-registered kill-gate (κ < 0.70 sends the taxonomy back for revision). | Both halves of the "not X but Y" kept; "→" is not prose. Threshold value and consequence unchanged. |
| 7 | § 1, end | Added one contribution sentence: "The contribution is a positive but qualified answer at the coarse grain and an open question at the fine grain, both figures bounding within-family reproducibility of the classification task rather than independent inter-annotator reliability, since the two passes come from the same LLM family." | Assembled only from the abstract's own claims at the same strength; deliberately contains no numeral so the drift gate and the reader see nothing new. Veto candidate if the intro should end on the question. |
| 8 | § 2, prior-work paragraph | Bold removed from "Neither paper measures…" | Emphasis by bold. |
| 9 | § 2, same paragraph | "This is the gap our study targets — not "can a classifier be built" … but "if two…?"" → "This is the gap my study targets. The question is no longer whether a classifier can be built (both prior works answer yes) but whether two independent passes that classify the same items by the same codebook agree, how often, and whether that agreement survives a finer-grained taxonomy." | Same contrast, declarative form instead of a quoted question inside an em-dash frame. |
| 10 | § 2, LLM-annotator paragraph | "— a finding that generalizes…" and "— a pattern that anticipates…" → new sentences ("That finding generalizes… and it motivates…", "That pattern anticipates…") | Em-dash apposition as copula, twice in one paragraph. |
| 11 | § 2, end | Bold removed from "The verified gap" | Emphasis by bold. |
| 12 | § 3, Universe | Bold removed from "This study's universe is two-member compounds only" | Emphasis by bold; scope word "only" kept. |
| 13 | § 3, Design | "— genuine type ambiguity versus bracketing ambiguity … —" → parentheses | Paired em-dash aside inside an already long sentence. |
| 14 | § 4, Coarse tier | Disagreement sentence reordered: boundary named first ("a single boundary, the endocentric/exocentric one:"), then the karmadhāraya/bahuvrīhi/dvandva reading and the gloss example, then "That boundary is not resolvable from segmentation alone and arguably belongs to external syntax rather than word-formation." | The original stacked two em-dash asides so the referent of "the endocentric/exocentric boundary" arrived after the example. Every clause kept, including "arguably". |
| 15 | § 4, Fine tier | "does not — the case-relation subtype…" → "does not: the case-relation subtype…" | Em-dash as colon. |
| 16 | § 5, same-family caveat | Bold removed; "a genuinely independent — cross-vendor or human — annotator pair" → "a genuinely independent annotator pair, cross-vendor or human," | Bold emphasis and paired em-dash. Rewrapped following lines only. |
| 17 | § 5, Fine κ | "not "recovered" — over-stating this as a clean pass would be a defect" → "not "recovered"; over-stating it as a clean pass…" | Em-dash as semicolon; "this" → "it" for the antecedent. |
| 18 | § 5, Sampling-frame artifact | "— not evidence that avyayībhāva is rare" → "; it is not evidence that avyayībhāva is rare" | Em-dash copula; the negation kept in full. |
| 19 | § 5, registry boundary | "(SG-WF-010) — a documented divergence, not resolved by this pilot." → "(SG-WF-010). The divergence is documented, and this pilot does not resolve it." | Em-dash apposition; both facts kept. |
| 20 | § 6 | "(κ=0.72, lower CI 0.60) — a genuine open question, not a settled result." → "…; that remains a genuine open question, not a settled result." | Em-dash copula; the "X, not Y" here is the hedging claim itself and stays. |

Left untouched on purpose: the four bolded term introductions in § 1 (tatpuruṣa, bahuvrīhi, dvandva, avyayībhāva, kevala-samāsa) and the bold run-in paragraph labels in §§ 2–5 (structural, not emphatic); "markedly lower", "real, if bounded, confidence", "load-bearing next step", "genuinely independent" (magnitude and hedge words attached to claims); the em-dashes that set off Sanskrit glosses in § 1; the "X, not Y" constructions in § 5 headings and § 6 that carry the paper's hedging (claim-strength rule).

## 2. Substance flags carried (not fixed)

1. **"Manual classification" performed by two LLMs.** The abstract ("recovered by manual classification") and § 6 ("by manual classification with high agreement between two same-family LLM passes") call the passes manual while § 3 says both are LLM-generated and model-provisional. A referee will ask what "manual" means here. A human should decide whether to keep "manual" (as "non-automatic, codebook-driven") or replace it with "codebook-driven classification".
2. **Coarse label space is described two ways.** Abstract: "four-way-plus-residual Pāṇinian class". § 3 Codebook: "four coarse classes (…) plus dvigu and an `unclear` residual at the coarse tier" (six labels), while the same paragraph folds dvigu inside tatpuruṣa. Which label set the coarse κ was computed over is ambiguous from the text; `kappa_result.json` will settle it.
3. **The § 4 disagreement example is a gloss, not a token.** "e.g. a compound glossable either as "distinguished qualities" [karmadhāraya] or "one whose qualities are distinguished" [bahuvrīhi]" cites no Sanskrit compound. A venue reader will want the actual item(s) from the sample. Not added: an example is substance.
4. **House-internal identifiers a venue reader cannot resolve.** EM4 / "evidence-limit registry", "Sangram morphology programme", C2, SG-WF-010, P2, P3, "Path B of three candidate designs", "kill-gate", "committed `kappa_result.json`" (committed where?), H989 in Data availability. Each needs either a gloss or a public pointer before submission.
5. **Vendor unnamed.** "Opus 4.8" and "Sonnet 5" are named without the vendor or model family; "the same LLM family" is never identified. A venue reader needs the vendor and, ideally, the dated model IDs already present in § 3 (`claude-opus-4-8`, `claude-sonnet-5`) tied to a vendor name.
6. **Snapshot provenance.** § 3 says the upstream commit is orphaned and that "the binding provenance is the snapshot's own provenance table and checksum". The mirror (`gasyoun/dcs-conllu`) commit or release that carries that provenance table is not cited, so the checksum has no public anchor in the paper.
7. **Relative links.** The header status line and Data availability link the OUTLINE relatively (`OUTLINE_compound-type-kappa_A64.md`). Left as is (URL rule); a human may want them as full blob URLs before the draft leaves the repo.
8. **Coarse-tier percentages** (79.5 / 14.5 / 5.1 / 0.9 of 117) and the fine-tier disagreement split (5 + 4 + 2 + 9 = 20) recompute correctly; 442,649 + 152,372 = 595,021 holds; 2,214 / 841,052 = 0.26% holds. No numeric flag.

## 3. Read-and-sign

- Time to read the diff and this memo: about 30 minutes. Read order: § 1 (calls 6–7 are the only ones that change sentence structure with new material), then § 2 call 9, then § 4 call 14; everything else is punctuation and pronoun.
- Proposed readiness: stay at 3/5 until flags 1, 2 and 4 are ruled; propose 4/5 once they are, since the argument, numbers and hedging are already in final shape. Never 5/5 from this pass.
- Venue: no recommendation from this pass; the OUTLINE § Venue candidates stands. No submission before 2026-11-01.
- Model and date of this pass: Fable 5.1 (`claude-fable-5-1`), 06-09-2026, branch `voice-pass/A64`, no push.

_Dr. Mārcis Gasūns_
