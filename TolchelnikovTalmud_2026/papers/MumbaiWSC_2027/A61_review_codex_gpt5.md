# Hostile referee review: A61

**Date:** 2026-07-18  
**Reviewer:** Codex, GPT-5 (OpenAI; the exact serving revision is not exposed in
the session metadata)  
**Target:** *How the Cologne Digital Sanskrit Lexicon Endured (1994–2026)*  
**Recommendation:** **HOLD — major revision remains necessary, but the paper is
now structurally viable.**

## Overall assessment

The revision has acquired an argument. Its strongest claim is not that CDSL is
large or old, but that it survived through a series of conversions that made
scholarly labour portable: transcription into structured data, departmental
custody into files, private correction into public version history, and entries
into stable addresses. The counterclaim is equally important: technical
transferability has not deconcentrated maintenance labour.

The paper should remain at readiness 3/5 until the unresolved historical and
legal claims below are locked or softened. The quantitative core is now
substantially better: repository populations are named, bots are excluded by a
curated override, submitter labels are not presented as people, and OBS-T and
OBS-Q are no longer collapsed into one contributor count.

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
   `a61-history-v1.0` evidence release, its calendar alias, its per-source cutoffs,
   and its claim/contradiction registers.
9. **A13 and A61 duplicated one another.** A61 is now the canonical synthesis;
   A13 is a complementary analysis of repository visibility and institutional
   transition, not a first-person memoir.

## Unresolved major findings

### M10. Secondary numerical claims remain outside the frozen release

Several exact figures in §§3–7 and §10 are not yet represented in the A61 claim
registry: the circa-190 worker estimate; 700/4,000 correction examples; detailed
tag/citation subtotals; dictionary-specific lemma, alignment, and character-count
figures; archive-file inventories; and the 482,400 visitor figure. Before
submission, either add each figure to the release with a local, hashed source and
method, or replace it with a non-numerical formulation. Do not treat a GitHub URL
alone as a frozen source.

### M11. The pre-Git historical chain needs primary locators

The 1994 founding, the 2004 collaboration, the 2008 conventions, the 2013 DCH
transfer, and the 2016/2018 format transitions form the causal spine. The current
draft has attributed recollection and project documents, but not a locator for
every link. Attach dated reports, correspondence metadata, archived pages, or
institutional records. The two email-derived milestone slots in the snapshot are
correctly marked `evidence_pending`; they must stay out of asserted chronology
until the author supplies the historical mail.

### M12. Copyright and public-domain language is legally overconfident

Section 3.3 reports an important historical dispute, but the statement about EU
database protection must be presented as Malten's stated position, not the
paper's legal conclusion. Any assertion that a particular edition is public
domain needs jurisdiction and edition-specific legal verification. The present
attribution is an improvement, but legal language should receive a separate
source check.

## Minor findings

- Complete the Jachertz and Macdonell bibliographic records or delete the claims
  that depend on them.
- Replace bare URLs in the references with archived or versioned locators where
  possible.
- The future-plans section is still broad. For a conference paper, retain only
  plans that test or follow from the succession thesis; move the rest to a
  project roadmap.
- Confirm the Mumbai WSC call, word limit, citation style, anonymity rule, and AI
  disclosure policy against the official call before camera-ready preparation.
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

1. Every exact claim retained in A61 is in `claim_registry.csv`, with population,
   cutoff, source, and status.
2. M10 figures are frozen or softened.
3. M11 milestones have primary locators or are explicitly attributed testimony.
4. M12 language is verified or narrowed to reported historical positions.
5. Jachertz and Macdonell records are complete.
6. The venue's current official instructions are attached and satisfied.
7. The manuscript builds cleanly and contains no stale four-implementer, 210-
   contributor, 65-of-76, or 2014-founding formulation.

