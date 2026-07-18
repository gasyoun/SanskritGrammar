# A61 manuscript, source, and venue gate

**Date:** 18 July 2026
**Scope:** A61 only; no A13 edits; no Fable voice pass
**Status:** **MANUSCRIPT AND REGISTRY GATES APPLIED; HUMAN-PERMISSION ITEMS REMAIN**

This note records the evidence decisions applied to *How the Cologne Digital
Sanskrit Lexicon Endured (1994–2026)*. The machine-readable companion is
`a61-history-v1.1`, committed in `csl-observatory` as `f300b688`.

## Historical source decisions

| Claim | Disposition | Public locator |
|---|---|---|
| Project initiated by Thomas Malten in 1994 | Verified in the 1997 project report and University of Cologne's 2016 institutional timeline | https://www.sanskrit-lexicon.uni-koeln.de/CDSL.pdf · https://dch.phil-fak.uni-koeln.de/sites/dch/Materialien_Aktivitaeten/2016/The_Cologne_Sanskrit_Lexicon_2016-11-11.pdf |
| Collaboration beginning in 2004 | Retained only as Funderburk's attributed testimony. Public records independently document the Cologne–Brown XML collaboration by 2006–2008, but do not replace the unsupplied correspondence | https://www.sanskrit-lexicon.uni-koeln.de/talkMay2008/markingMonier.html · https://sanskritlibrary.org/nsf2005.html |
| 2008 XML/SLP1 formalisation | Verified by the dated May 2008 project materials and Sanskrit Library project record | https://www.sanskrit-lexicon.uni-koeln.de/talkMay2008/markingMonier.html · https://www.sanskrit-lexicon.uni-koeln.de/talkMay2008/mwtags.html |
| 2009–2013 funded expansion | Verified at project level; exact archive-file counts remain attributed to Scharf's supplied archive until hashed | https://www.sanskritlibrary.org/nehDFG2009.html |
| 2013 DCH responsibility | Verified: Cologne's timeline says Malten retired and DCH became responsible; LAZARUS ran December 2013–January 2015 with CDSL as a named collection | https://dch.phil-fak.uni-koeln.de/sites/dch/Materialien_Aktivitaeten/2016/The_Cologne_Sanskrit_Lexicon_2016-11-11.pdf · https://cceh.uni-koeln.de/portfolio/lazarus/ |
| 2004–2005 scan/database-right episode | Retained only as Malten's stated position in author-held correspondence, not as this paper's legal conclusion | No public primary locator; HUMAN archive/permission gate |
| Apte 1957 rights | Legal conclusion deleted. The manuscript now reports access chronology only and does not infer a jurisdiction-specific public-domain date | https://dsal.uchicago.edu/dictionaries/apte/ · https://www.sanskrit-lexicon.uni-koeln.de/ |

The two email milestones (`HIST-EMAIL-TECH`, `HIST-EMAIL-RIGHTS`) remain
`evidence_pending`. No email text, quotation, or date was reconstructed.

## Bibliographic decisions

- **Jachertz:** recovered from the existing A13/PWK evidence trail as:
  Thomas Jachertz, *Beiträge zu einer bibliographischen Übersicht über die
  textliche Basis unserer europäischen Sanskritwörterbücher, vorzüglich des
  grossen Petersburger Wörterbuches (PW) und des kleinen Petersburger
  Wörterbuches (pw)*, Magisterarbeit, vorgelegt im Sommersemester 1983.
  Public transcription and scan:
  https://github.com/sanskrit-lexicon/PWK/tree/main/pw_ls/pwbib/jachertz .
  The transcription does not identify an awarding institution, so none is
  asserted in the bibliography.
- **Macdonell:** the 1893 Longmans work is the original. The University of
  Chicago DDSA record for the 1929 Oxford issue states that the original was
  reproduced photographically with Longmans' consent. The manuscript now calls
  1929 a photographic reissue under a shortened title, not a revised edition.
  Sources: https://dsal.uchicago.edu/dictionaries/macdonell/ and
  https://upload.wikimedia.org/wikipedia/commons/e/e7/A_Sanskrit-English_dictionary%2C_being_a_practical_handbook_with_transliteration%2C_accentuation%2C_and_etymological_analysis_throughout_%28IA_afr4858.0001.001.umich.edu%29.pdf .

## M10 numerical gate

Retained exact empirical figures are limited to locally reproducible evidence:

- 78 API repositories / 76 transformed-table repositories / 5,413 activity rows;
- 52,498 OBS-T events / 43 dictionaries / 208 release-safe labels;
- sixteen normalized non-bot Git identities;
- five maximum annual OBS-Q implementers and 64–100% annual lead share;
- 323,425 union headwords; 105 pairwise comparisons; BHS 58.7% unique;
  Cappeller 0.6% unique;
- 94,753 MW–PWG common lemmas;
- 828,505 canonicalised citations resolving to 912 texts.

Unsupported or stale precision was removed or softened: the hiatus count; MW
print-change and supplement counts; Apte error percentage; issue-backlog annual
arithmetic; do-not-correct and n-gram totals; detailed citation ranks and link
target subtotals; Mahābhārata notes-apparatus subtotals; DCS and dictionary
alignment percentages; MW/PWG entry-length and citation-overlap block; stale
etymology-oracle and Whitney crosswalk totals; site traffic peak/trend; and
Scharf-archive file-level counts.

## Venue gate

Official page: https://www.hss.iitb.ac.in/wsc2027/

- Abstract deadline: **1 February 2027**.
- Headline and Important Dates conference dates: **10–14 December 2027**.
- Contradiction on the same page: footer says **10–15 December 2027**.
- No abstract word limit, citation style, anonymity rule, or AI-disclosure rule
  was located on the official page as checked on 18 July 2026.
- The manuscript therefore contains a clearly labelled provisional 258-word
  abstract and explicitly makes no claim of venue-limit compliance.

## Completed csl-observatory registry reconciliation

The csl lane completed the following reconciliation in `a61-history-v1.1`
(`f300b688`):

1. Corrected `A61-DATA-03` from the stale four-implementer wording to **five**.
2. Added claim rows for `ORG-ISSUE-PR-ROWS`, `ORG-HUMAN-COMMIT-IDS`,
   `CDSL-DICTIONARIES`, `CDSL-UNION-HW`, and `CDSL-CITATIONS` where retained.
3. Added locked metrics/claim rows for the 105-pair/BHS/Cappeller results and the
   94,753 MW–PWG overlap, including local source paths, hashes, count rules,
   populations, and cutoffs.
4. Updated `HIST-2013-DCH` to `verified` with the two University of Cologne
   locators above; retain `HIST-2004-COLLAB` as `verified-attributed`.
5. Kept both email milestones exactly `evidence_pending`.

## Human gates before submission

- Add timestamps to every quotation from the 27 June 2026 call and review all
  speaker attributions against the recording.
- Confirm archive locator and permission for the Malten correspondence quote;
  otherwise paraphrase or remove it.
- Add a page locator and fair-dealing check for the long Kapp–Malten block
  quotation in §1.
- Add page locators before retaining specific Jachertz-derived historical
  assertions.
- Author-review participant roles, byline/affiliation, and all testimony.
