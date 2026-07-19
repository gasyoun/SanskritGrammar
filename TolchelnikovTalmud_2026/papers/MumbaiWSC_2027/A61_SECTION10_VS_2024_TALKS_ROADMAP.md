# A61 §10 vs the February 2024 talks — planned road vs actual trajectory

_Created: 19-07-2026 · Last updated: 19-07-2026_

Commissioned by the author in the sign-off ruling on the H1222 voice pass ([SIGNOFF_A61_author_pass.md](https://github.com/gasyoun/SanskritGrammar/blob/codex/a61-sol-evidence/TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/SIGNOFF_A61_author_pass.md)), as the disposition of the referee's "§10 is broad" flag. Prepared by Fable 5 (`claude-fable-5`) under [H1284](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1284-Fable_SanskritGrammar_a61-signoff-ruling-roadmap-compare_19.07.26.md), 19-07-2026.

## Sources compared

- **The two February 2024 talks** — `Cologne-Lexicons-Auroville-2024.pdf` (ISCLS Auroville, 07-02-2024) and `Cologne_Lexicons_Wien_2024.pdf` (Universität Wien, 12-02-2024), both in the local `papers/` folder (untracked). The decks are near-identical (47 slides each); the plan slide "What's Next? 2024–2034" (slide 46) and the "Cologne Code Basic Needs" slide (slide 42) jointly state the initial road.
- **The Cologne roadmap issues the decks themselves cite** — [COLOGNE#325](https://github.com/sanskrit-lexicon/COLOGNE/issues/325) ("todo list in 2021", 36 ranked items) and [COLOGNE#400](https://github.com/sanskrit-lexicon/COLOGNE/issues/400) ("Ideas for 2023"). Both are still **open** as checked 19-07-2026; they remain the org's only standing roadmap documents.
- **A61 §10** — [09-future-plans.mdx](https://github.com/gasyoun/SanskritGrammar/blob/codex/a61-sol-evidence/TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/09-future-plans.mdx) ("Plans That Survive the Audit"), post-evidence-gate state of 18-07-2026.

## Item-by-item: the 2024–2034 road against §10 and against what actually happened

| 2024 plan item (deck slide 46 / 42; roadmap issue) | §10 disposition (2026) | Actual trajectory 2024 → mid-2026 | Verdict |
|---|---|---|---|
| Five Sanskrit–Russian dictionaries ("started") | §10.1 — first-ranked plan | Conversion work began 2025; digitised editions live at samskrtam.ru | **On road** |
| RESTful APIs · JSON output · UI on APIs · simple search with exact ID (slide 42; [#325](https://github.com/sanskrit-lexicon/COLOGNE/issues/325) items 1–2, ranked top since December 2020) | §10.2 — stable entry URLs + API, "highest-return item on the interface side" | Still reviewed prototypes; deployment now conditioned on post-Funderburk maintainer capacity (§3.5). Top-ranked code item for six years without deployment | **On road, stalled** — the single largest plan-vs-actual gap |
| Abbreviation markup · literary-source markup ([#400](https://github.com/sanskrit-lexicon/COLOGNE/issues/400): PWG/PW literary-source refinement, abbreviations for other dictionaries) | §10.5 — "the natural continuing workload for the volunteer model" | Continuous progress in the correction stream; Apte's untagged sources named as the largest unrealised block | **On road** |
| Subheadword/alternate-headword programme (deck slides 8–9; [#325](https://github.com/sanskrit-lexicon/COLOGNE/issues/325) items 6–7 and 26–36) | §10.4 — headword programme, three items ready in design | Normalization pipeline running; feminine-derivative exposure designed; the computed-keys-vs-base-lexicon design question now stated openly | **On road** |
| Amarakosha as a new Sanskrit–Sanskrit dictionary (deck: "still missing"; [#400](https://github.com/sanskrit-lexicon/COLOGNE/issues/400) sketches a lead plan) | **Absent.** §10.6 says no new dictionary is planned except a reverse dictionary | No visible Amarakosha work 2024–2026 | **Silently dropped** — publicly announced in both 2024 talks, unmentioned in §10 |
| "Show corrected print changes" (deck slide 46; slide 7 records print-corrections integrated only in GRA and MW) | **Absent.** The M10 evidence gate also removed the MW print-change counts as unsupported | No integration programme since | **Silently dropped** |
| Cross-reference markup (deck slide 46) | Only obliquely covered by §10.5's citation-markup frame | Partial, inside per-dictionary markup work | **Dropped as a named item** |
| Verb tagging in all dictionaries (deck slide 40; [#325](https://github.com/sanskrit-lexicon/COLOGNE/issues/325) item 15) | Absent from §10 | VCP-centred issues open since 2020 | **Dropped as a named item** |
| Offline usage · mobile PDF visibility ([#325](https://github.com/sanskrit-lexicon/COLOGNE/issues/325) items 4–5) | Absent as a plan; offline-first appears only as Funderburk's historical design preference (§8.2) | No dedicated work | **Dropped as a named item** |
| Volunteer recruitment (both decks close with "let's build a team now"; slide 41: "every other line of code — hiring volunteers") | §10.7 — OED-model crowdsourced verification named the only scaling path, dependent on §10.2 | Volunteer base remains narrow: at most five implementers/year, 64–100% annual lead share (§8) | **On road in intent, unresolved in practice** |
| — (not on the 2024 road) | §10.3 — Scharf archive ingestion, incl. the two Dhātupāṭhas | Archive transmitted during the WSC-2025 review cycle; itemised comparison done | **New since 2024**, review-process windfall |

## Where we are actually heading vs the initial road

1. **The road held better on data than on code.** Everything the project actually advanced 2024–2026 — corrections throughput, Russian line, headword normalization, markup, plus the evidence/measurement infrastructure A61 itself rides on — is the data half of the 2024 road. The code half (API/JSON/UI, the decks' "critical lacking features" and [#325](https://github.com/sanskrit-lexicon/COLOGNE/issues/325)'s rank 1–2 since 2020) is where the six-year stall sits, and §10.2 now honestly re-conditions it on succession capacity. This asymmetry is exactly the decks' own slide-41 diagnosis ("code we can handle… every other line — hiring volunteers"), still true.
2. **§10 is narrower than the 2024 road, not broader.** Against the referee's "future plans are broad" flag: §10 *prunes* the public 2024–2034 programme (drops Amarakosha, print-changes integration, cross-references, verb tagging, offline/mobile) and orders the survivors by evidence-backed readiness. The chapter title's claim — plans that survive the audit — is borne out by this comparison.
3. **The one editorial exposure:** two of the dropped items (Amarakosha, print-changes) were announced at two 2024 conferences by the author. Leaving them silently unmentioned invites a "what happened to…?" question from any listener of those talks who reads A61. One sentence in §10.6 explicitly retiring them (e.g. "the Amarakosha and print-changes programmes announced in 2024 are deferred: neither survives the present capacity audit") would convert the silent drop into the paper's own measured-honesty idiom. Whether to add it is an authorial substance decision — a human decides; it is outside the voice pass and outside this comparison's mandate.

_Dr. Mārcis Gasūns_
