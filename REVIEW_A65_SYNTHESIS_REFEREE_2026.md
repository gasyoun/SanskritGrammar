# Referee review of A65 (hostile pass) + disposition — 16-07-2026

_Created: 16-07-2026 · Last updated: 16-07-2026_

Hostile referee pass over
[REPORT_GRAMMAR_CLAIM_VERIFICATION_SYNTHESIS_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/REPORT_GRAMMAR_CLAIM_VERIFICATION_SYNTHESIS_2026.md)
(the merged A65 full draft), performed by a fresh-context reviewer agent
(general-purpose subagent on the session model, Fable 5 `claude-fable-5`),
instructed to check number consistency, overclaiming, logical gaps, method
honesty, genre residue, Russian prose, and reference hygiene. **10 Major +
16 Minor findings; verdict: empirical core sound (all headline arithmetic
verified independently), draft not submittable without the Major fixes — all
mechanical, none threatening the results.** Fixes applied same pass (below);
submission-conversion items deferred to the author-pass checklist.

## Major findings and disposition

| # | Finding (compressed) | Disposition |
|--:|---|---|
| 1 | §9 «96–100 %» arithmetically false vs the §4 table (true range 94.6–100 % among testable) | ✅ APPLIED — denominator stated, range corrected |
| 2 | «первый содержательный FALSE программы» contradicts HK-16 (§5.2), which is substantive and earlier | ✅ APPLIED — restricted to «первый FALSE очерка», HK-16 credited as chronologically first |
| 3 | Four-class typology silently extrapolated to Бюлер/Зализняк; Бюлер's 7 OVERSTATED never characterized | ✅ APPLIED — extrapolation demoted to hypothesis; Бюлер's 7 OVERSTATED characterized with three named examples; formal cross-book classification named as future work |
| 4 | «728 по двум осям» documented only for Кочергина; +24/12 disjointness unstated | ✅ APPLIED — pedagogy-axis counts given for Кочергина (36/234, disjoint sets stated), Бюлер (8/403), Зализняк (3 MISLEADING) |
| 5 | Overclaiming: «впервые» (ACL-only check), «считавшиеся непроверяемыми» (own registry), «ПРЕДСКАЗАННОЕ» (same-pipeline, not preregistered) | ✅ APPLIED — novelty scoped to CL literature with named unindexed venues; «не имевшие корпусных чисел»; prediction downgraded to internal marking, non-preregistered |
| 6 | «Три диахронических утверждения» — the third (purāṇas) is the programme's own finding, not Зализняк's claim | ✅ APPLIED — recounted as two Зализняк claims + the purāṇa signature as the programme's own control measurement |
| 7 | Vedic-skew caveat arrives in §8 while §4.3 issues word-order verdicts from the skewed slice | ✅ APPLIED — per-genre breakdowns (classical subset 86.5 % / 37.6 %; Arthaśāstra 51.4 %) inlined into §4.3 |
| 8 | Genre residue: status banner, H###/A## IDs, session dates, status glyphs, ⬜-slot bibliography, GitHub-only evidence links | ◐ PARTIAL — main-text IDs and session-date findings neutralized; ⬜ slot converted to «в подготовке»; **deferred to author-pass/submission: banner removal, appendix provenance notation, Zenodo/OSF archival deposit of evidence** |
| 9 | Broken word «аллом орфов»; systematic calques (конфлирует, флагуется, бейджирующий, вердиктованные, пиннованный, коммитнутый, дрен, бэклог, блокер, кроссволк, стайл-гайд, аудированы) | ✅ APPLIED — word repaired; all listed calques replaced; «treebank-срез» defined at first use; «адъюдикация» kept in the title, glossed at first use in §1 |
| 10 | Bibliography below venue standard (missing places/translators; Зализняк-1975 title unverified; no GOST; zero Russian-language related work) | ◐ PARTIAL — Кнауэр place added, Бюлер translator noted, Зализняк-1975 marked for verification against the first edition; **deferred to author-pass: GOST formatting, Russian-scholarship ring in §2** |

## Minor findings

All 16 applied except: №3 (three-in-one table split — kept for now, flagged for
typesetting at submission) and №10 (related-work thinness — folded into the
deferred Russian-scholarship ring). Notables: «втрое» → «в 2,6 раза»; «ровно
порядок величины» → «в 5,6–16 раз»; Fisher exact p = 0,42 (Бюлер vs Кочергина)
inserted for the «статистически незначимы» sentence; «Уитни-930» glossed;
print-vs-digitization status of Бюлер's FALSE set stated (checked against the
2008 e-text; 1923 print collation is a future step); Конспект's Rigveda
fractions given their one-sentence explanation; journalistic headings toned
down.

## Collision note (H214-class, resolved by merit-merge)

While this referee pass was being applied, a concurrent session (H1033,
[PR #277](https://github.com/gasyoun/SanskritGrammar/pull/277)) landed its own
A60→A65 4/5 merge and cut v0.34.0. Merit comparison: H1033's version PERFORMED
the five-book typology classification (Зализняк's 3 syntax flags placed in
classes 1/2/4; Бюлер's misprint-FALSE set correctly excluded; classified total
9/4/2/0 of 15) and fixed two register defects (HK-10's Whitney §§ 592/595;
HK-38's exception-inventory reading) — stronger than this branch's
hypothesis-demotion on those points. This branch's referee findings, absent
from H1033's text, were re-applied onto the H1033 base (PR #278 closed as
superseded; the re-application PR carries both). Disposition above reads
against the merged result; Major 3 is closed by H1033's classification rather
than by softening.

## Deferred to the author-pass / submission conversion (the 4/5 → 5/5 gate)

1. Remove the working status banner; convert repo links to an archived deposit
   (Zenodo/OSF DOI) — a journal cannot cite live blob URLs.
2. GOST bibliography + verify Зализняк-1975 against the first edition.
3. Russian-language scholarship ring in §2 (зеро сейчас — named referee
   concern for a российская-индология venue).
4. Split the §5.3 triple table for typesetting.
5. The standing human gates: авторская виза and the human verdict-validation
   sample (κ template) — both named in the draft itself.

_Reviewer: fresh-context subagent (Fable 5 `claude-fable-5`); fixes applied by
the same session, H1015. Full referee text preserved in the session transcript;
this file records findings + disposition._

_Dr. Mārcis Gasūns_
