# SIGNOFF — A61 author-voice pass (H1222)

_Created: 18-07-2026 · Last updated: 18-07-2026_

**Paper:** A61 — *How the Cologne Digital Sanskrit Lexicon Endured (1994–2026): From Institutional Project to Shared Infrastructure* ([chapter folder](https://github.com/gasyoun/SanskritGrammar/tree/codex/a61-sol-evidence/TolchelnikovTalmud_2026/papers/MumbaiWSC_2027), [draft PR #403](https://github.com/gasyoun/SanskritGrammar/pull/403))

**Pass:** one authorial voice pass per [H1222](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1222-Fable_SanskritGrammar_a61-author-voice-pass_18.07.26.md), executed 18-07-2026 by Fable 5 (`claude-fable-5`), after the Sol evidence gate ([A61_EVIDENCE_GATE_2026-07-18.md](https://github.com/gasyoun/SanskritGrammar/blob/codex/a61-sol-evidence/TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/A61_EVIDENCE_GATE_2026-07-18.md), Codex GPT-5) and the hostile referee review ([A61_review_codex_gpt5.md](https://github.com/gasyoun/SanskritGrammar/blob/codex/a61-sol-evidence/TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/A61_review_codex_gpt5.md)).

**Overall register verdict:** the post-gate manuscript already reads in the author's voice — first-person scholarly frame, the ICANAS 2004 opening, the measured-honesty idiom. The pass is therefore deliberately light: eleven surgical edits across seven chapter files, itemised below as voice calls the author may veto, plus explicit records of what was left unchanged and why. No number, quotation, citation, claim-registry status, or legal formulation was altered.

## Voice calls made (each vetoable by one revert)

| # | File | Change | Rationale |
|---|---|---|---|
| VC1 | [00-front-matter.mdx](https://github.com/gasyoun/SanskritGrammar/blob/codex/a61-sol-evidence/TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/00-front-matter.mdx) | Venue paragraph restructured: "intended for the Computational Sanskrit and Digital Humanities section" folded into the opening sentence; the footer-discrepancy sentence now reads "this unresolved one-day discrepancy is recorded here rather than silently harmonised" | The old paragraph ended on a dangling fragment ("Intended section: …") and read as an audit log. All three venue facts — deadline **1 February 2027**, headline **10–14 December 2027**, contradictory footer **10–15 December 2027** — plus the "intended"/"unresolved" hedges are retained |
| VC2 | [03-history.mdx](https://github.com/gasyoun/SanskritGrammar/blob/codex/a61-sol-evidence/TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/03-history.mdx) §3.4 | "One negative event should also be recorded" → "One loss should also be recorded" | The passage records Malcolm Hyman's death and the unbuildable transliteration code; "negative event" is process-report jargon, "loss" is the author's register |
| VC3 | [04-data-architecture.mdx](https://github.com/gasyoun/SanskritGrammar/blob/codex/a61-sol-evidence/TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/04-data-architecture.mdx) intro | Added one sentence: "In the argument of this report the architecture is not background but mechanism: stable identifiers and portable line-oriented sources are what made correction addressable and succession technically possible (§1, §3.5)." | H1222 asks for visibility of the causal argument; §4 was the one chapter whose opening did not tie back to the thesis. The sentence restates claims already made in §1, §3.5 and §4.1 — no new claim |
| VC4 | [06-corpus-linking.mdx](https://github.com/gasyoun/SanskritGrammar/blob/codex/a61-sol-evidence/TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/06-corpus-linking.mdx) §6.1 | "its head is dominated by the epics" → "the head of that distribution is dominated by the epics" | Antecedent clarity; "its head" briefly reads as PWG's head |
| VC5 | Typography, five files ([03](https://github.com/gasyoun/SanskritGrammar/blob/codex/a61-sol-evidence/TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/03-history.mdx) ×2, [05](https://github.com/gasyoun/SanskritGrammar/blob/codex/a61-sol-evidence/TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/05-corrections.mdx) ×1, [08](https://github.com/gasyoun/SanskritGrammar/blob/codex/a61-sol-evidence/TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/08-people.mdx) ×1, [11-conclusion](https://github.com/gasyoun/SanskritGrammar/blob/codex/a61-sol-evidence/TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/11-conclusion.mdx) ×1) | Closed em-dashes (`word—word`) normalised to the manuscript's dominant spaced style (`word — word`) | Dash style was mixed between chapters written in different sessions; normalised outside quotations and code blocks only. The em-dash inside the §4.1 data sample (`kuYja—kuwIra`) is quoted source data and was not touched |

`Last updated` headers were bumped to 18-07-2026 on the seven edited files only.

## Left unchanged under an H1222 constraint (per the "note the constraint" clause)

- **The provisional abstract — verbatim.** The evidence gate and the folder [README.mdx](https://github.com/gasyoun/SanskritGrammar/blob/codex/a61-sol-evidence/TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/README.mdx) both record it as a 258-word abstract; any wording change falsifies that recorded figure, so the pass leaves it byte-identical. One authorial suggestion is parked for submission time: "CDSL's durable achievement is therefore not scale alone. It is a corrigible scholarly object…" carries a small antecedent slippage (the achievement is not itself the object); a tighter form would be "…not scale alone but corrigibility: a scholarly object whose sources, identifiers, and procedures a successor can recover." Adopting it changes the word count by −2 and stays inside the 250–300 band — a human decides at submission formatting.
- **§3.3 (copyright episode) and §2.4 (Apte/DDSA, Macdonell) — byte-identical.** Both passages carry legal meaning narrowed by the evidence gate to reported positions and access chronology; no rephrase improves them without risking that meaning.
- **All quotations everywhere** — Kapp–Malten 1997 block quote, all Cologne-call quotations (Funderburk, Patel), Malten's quoted position — byte-identical, verified mechanically against the pre-pass head (see verification record in the PR).
- **§9 Limits of the Evidence** — left in its crisp, enumerated register deliberately; the genre wants exactly that plainness.
- **§10 breadth** — the referee's minor finding that future plans are broad was NOT acted on: trimming §10 is substance, out of a voice pass's scope. Standing referee-lane flag, carried over unresolved.
- **References, abbreviations appendix, milestone statuses** — untouched; the two email milestones remain `evidence_pending` exactly as gated.

## Frozen-invariant confirmation (H1222)

The pass was adversarially verified by three independent read-only agents (Fable 5 `claude-fable-5` subagents) with distinct lenses — semantic drift, legal/venue preservation, register quality — plus the mechanical battery. The register lens flagged the first draft of VC1 (appositive stacking + two dropped hedges); it was revised as recorded above and the mechanical checks re-run green. The legal-lens verifier independently confirmed §3.3/§2.4 hash-identical to the pre-pass head and the abstract at exactly 258 words.

1. No quotation, empirical figure, claim-registry status, or legal meaning altered — confirmed (mechanical checks: quotation-preservation diff, stale-claim scan, `npm run check-claims`).
2. No A13 prose or artifact touched — confirmed (diff touches only `TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/`).
3. The two historical emails not reconstructed; both stay `evidence_pending` — confirmed.
4. Nothing merged, deployed, or submitted; the abstract is still labelled provisional and claims no venue-limit compliance — confirmed; [PR #403](https://github.com/gasyoun/SanskritGrammar/pull/403) remains a draft.
5. Venue ruling preserved: deadline 1 February 2027; headline dates 10–14 December 2027; the contradictory 10–15 December footer stays explicitly logged — confirmed (VC1 rephrases, does not remove).

## What the author must still rule on (read-and-sign, ~30 min)

1. Approve or veto VC1–VC5 above (each is a single revertable edit).
2. Decide the parked abstract sentence (see above) — at submission formatting, not before.
3. The human-permission gates carried over from the evidence gate, unchanged by this pass: quotation timestamps + speaker attributions against the 27 June 2026 recording; archive locator and permission for the Malten correspondence quote; page locator + fair-dealing check for the Kapp–Malten block quote; page locators for any specific Jachertz-derived assertion; participant-role descriptions in §8.1.
4. Byline and affiliation on the title block (including the contact address gasyoun@gmail.com vs the author's other academic addresses) — reserved to the author by H1222; the pass changed nothing there.
5. Final authorial approval. **A61 remains 4/5 until this sign-off is recorded.**

_Dr. Mārcis Gasūns_
