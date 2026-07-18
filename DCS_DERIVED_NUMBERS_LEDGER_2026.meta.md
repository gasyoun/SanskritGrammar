# Metadoc — DCS_DERIVED_NUMBERS_LEDGER_2026.md

_Created: 18-07-2026 · Last updated: 18-07-2026_

**Subject:** [DCS_DERIVED_NUMBERS_LEDGER_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/DCS_DERIVED_NUMBERS_LEDGER_2026.md)

## Purpose

The audit-of-record for every DCS-derived number published in the Sangram series:
129 checks, each CONFIRMED or REFUTED against the pinned corpus, with committed
re-derivation scripts. Answers "can the published statistics be trusted" once,
so no future session re-audits from scratch.

## Audience

Future sessions editing Sangram articles (check here before doubting a number);
referees of the Sangram-derived papers; the author when citing counts externally.

## Provenance

- Handoff: [H1229](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1229-Fable_SanskritGrammar_dcs-derived-numbers-adversarial-rederivation_18.07.26.md)
- Model: Fable 5 (`claude-fable-5`), 18-07-2026
- Corpus: `dcs_full.sqlite` pin `04e0778d3dc971030229179e25eea043d06ff397`
- Scripts: [sangram/audit/](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/audit) (rounds 1–3 + machine-readable JSON results)

## Limitations

- Audits only *mechanically re-derivable* numbers; qualitative grammatical claims
  are H1228's territory, not covered here.
- Sample-based figures (kappa adjudications, seeded validation samples) are audited
  at the universe/predicate level, not by re-drawing samples.
- The ledger is frozen to the 18-07-2026 article set; numbers published after that
  date are unaudited until a new round runs.

## Ranked improvement backlog

1. Wire the round-1 script into CI as a regression gate when the DCS pin changes
   (currently manual).
2. Extend to the SG-* CHANGELOG report numbers not repeated in articles (partial
   coverage today — articles + manifests + W2 checkpoint).
3. After the -tṛ draft PR is ruled on, re-run the krt-suffixes pilot with the IAST
   `%tṛ` universe (771 lemmas) and ledger the resulting numbers.

## Revision history

| Date | Change | Actor |
|---|---|---|
| 18-07-2026 | Created with the full 129-row ledger (97 exact + 29 definitional + 3 refuted) | Fable 5 (`claude-fable-5`), H1229 |
| 18-07-2026 | REFUTED #3 (-tṛ) resolved: MG ruled merge of [PR #414](https://github.com/gasyoun/SanskritGrammar/pull/414); ledger cell updated | Fable 5 (`claude-fable-5`) |

_Dr. Mārcis Gasūns_
