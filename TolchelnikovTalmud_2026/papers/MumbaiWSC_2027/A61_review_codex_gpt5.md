# Hostile referee review: A61

**Date:** 2026-07-18

**Reviewer:** Codex, GPT-5 (OpenAI; the exact serving revision is not exposed in
the session metadata)

**Target:** *How the Cologne Digital Sanskrit Lexicon Endured (1994–2026)*

**Recommendation (updated after evidence pass):** **HOLD FOR FABLE VOICE PASS
AND HUMAN PERMISSIONS — the evidence registry, manuscript-source, legal,
bibliographic, venue, and build gates are complete.**

## Overall assessment

The revision has acquired an argument. Its strongest claim is not that CDSL is
large or old, but that it survived through a series of conversions that made
scholarly labour portable: transcription into structured data, departmental
custody into files, private correction into public version history, and entries
into stable addresses. The counterclaim is equally important: technical
transferability has not deconcentrated maintenance labour.

The paper remains below submission readiness until the H1222 Fable voice pass
and the author's quotation/permission gates are complete. The registry and the
manuscript-level historical, legal, numerical, bibliographic, venue, and build
edits are recorded in `A61_EVIDENCE_GATE_2026-07-18.md`.

## Major findings applied in this revision

1. **The previous title exceeded its evidence cutoff.** The title now ends in
   2026, matching the latest evidence used.
2. **The draft was a catalogue rather than an explanation.** The introduction,
   periodisation, and conclusion now advance and test the serial-infrastructural-
   conversion thesis.
3. **Contributor populations were contradictory.** The revision separates the
   historical roster, 208 release-safe OBS-T labels, sixteen non-bot identities
   in the June Git snapshot, and at most five annual OBS-Q implementers.
4. **Repository totals were contradictory.** The text now distinguishes 78
   repositories returned by the API inventory from 76 represented in transformed
   activity tables.
5. **The public record was treated as complete history.** A dedicated limitations
   section now states the 1994/2014 gap, survival bias, identity limits, mixed
   cutoffs, and the difference between repository evidence and oral history.
6. **Correction totals mixed incompatible categories.** The paper now uses the
   canonical 52,498-event OBS-T release and removes unsupported locus/batch
   totals and the old 76-percent claim.
7. **History was divided by decades rather than mechanisms.** Section 3 is now
   organised around institutional production, collaborative formalisation,
   custody, public versioning, and succession without deconcentration.
8. **A data dump stood in for provenance.** A61 now names the versioned
   `a61-history-v1.1` evidence release, its calendar alias, its per-source cutoffs,
   and its claim/contradiction registers.
9. **A13 and A61 duplicated one another.** A61 is now the canonical synthesis;
   A13 is a complementary analysis of repository visibility and institutional
   transition, not a first-person memoir.

## Evidence-pass disposition

### M10. Unsupported secondary precision removed

Unsupported or stale figures in §§3–7 and §10 have been softened or removed.
Exact values survive only where the evidence audit reproduced them locally. The
remaining machine-readable work is to add claim rows and source hashes for those
retained values; see the csl-observatory additions listed in the evidence-gate
note. A GitHub URL alone is not treated as a frozen source.

### M11. Public locators added; private email remains pending

The 1994 origin, 2008 conventions, funded collaboration, and 2013 DCH transfer
now carry public project or University of Cologne locators. The 2004 start of
collaboration remains explicitly Funderburk's attributed account rather than an
inference from unsupplied mail. The two email-derived milestone slots remain
`evidence_pending` and outside the asserted chronology.

### M12. Legal conclusions narrowed to reported positions and chronology

Section 3.3 now presents database protection only as Malten's stated position in
correspondence, not the paper's legal conclusion. The Apte passage now reports
project access chronology without asserting a jurisdiction-specific public-
domain date.

## Minor findings

- Jachertz and Macdonell bibliographic records are complete at the evidence
  presently available; specific Jachertz-derived claims still need page locators.
- Replace bare URLs in the references with archived or versioned locators where
  possible.
- The future-plans section is still broad. For a conference paper, retain only
  plans that test or follow from the succession thesis; move the rest to a
  project roadmap.
- The official Mumbai WSC page is attached: deadline 1 February 2027; headline
  dates 10–14 December 2027; contradictory footer 10–15 December. No word limit,
  citation style, anonymity rule, or AI-disclosure policy was located.
- Keep testimony visibly attributed. Quotations and participant-role claims
  require author review even when the surrounding prose is rewritten.

## Responsible-research check

- **Limitations:** present and material, not ceremonial.
- **Main claims vs evidence:** the core correction and repository claims are now
  traceable; the secondary exact figures listed under M10 are not.
- **People and privacy:** released identities are pseudonymised or public Git
  identities; the draft should not infer real persons from labels.
- **Human subjects:** the paper uses attributed public testimony and an author
  archive, not an intervention or experiment; consent/status for private email
  quotation remains an author decision.
- **Risks and harms:** the revision avoids national-essentialist explanations
  and states that concentration measures do not measure the value of labour.
- **Reproducibility:** the snapshot builder and clean-source checks exist; a
  time-bounded full reconstruction recipe remains desirable.

## Acceptance gate for the next pass

1. **OPEN (csl lane):** add every retained exact claim to `claim_registry.csv`,
   with population, cutoff, local source/hash, and status.
2. **APPLIED:** M10 figures are frozen or softened.
3. **APPLIED WITH EMAIL HOLD:** M11 milestones have public locators or are
   explicitly attributed testimony; two email rows remain `evidence_pending`.
4. **APPLIED:** M12 language is narrowed to reported historical positions and
   access chronology.
5. **APPLIED:** Jachertz and Macdonell records are complete at current evidence.
6. **PARTIAL:** current official venue dates/deadline are attached; unpublished
   format and policy rules cannot yet be claimed satisfied.
7. **PENDING FINAL TEST RUN:** build, manuscript checks, and stale-claim scan.
