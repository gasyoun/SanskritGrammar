# Metadoc — ROADMAP_SANSKRITGRAMMAR_2026H2.md

_Created: 18-07-2026 · Last updated: 18-07-2026_

Companion record for [ROADMAP_SANSKRITGRAMMAR_2026H2.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_SANSKRITGRAMMAR_2026H2.md).
It exists separately from the plan set's own metadoc because the roadmap is registered in
[Uprava/ROADMAP_INDEX.md](https://github.com/gasyoun/Uprava/blob/main/ROADMAP_INDEX.md) and gets read
on its own, by readers who never open
[PLAN_SANGRAM_EDITORIAL_NOTES_AND_CHARTER_2026H2.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANGRAM_EDITORIAL_NOTES_AND_CHARTER_2026H2.md).

## Purpose

Wave order for the Sangram editorial-debt programme in 2026 H2 — applying the author's own visa
notes to the articles and companions they were cast on.

## Audience

A Fable-tier session picking up a note-application wave; and a human checking what Sangram owes
its own review record.

## Provenance

| Field | Value |
|---|---|
| Produced by | [`/ask-batch`](https://github.com/gasyoun/claude-config/blob/main/commands/ask-batch.md) 2026-07 pass 2 (`--resume`, slice 2), 18-07-2026 |
| Control doc | [ASK_BATCH_STAGING_2026-07.md](https://github.com/gasyoun/Uprava/blob/main/ASK_BATCH_STAGING_2026-07.md) |
| Model | Opus 4.8 (`claude-opus-4-8`) — audit, authoring, adversarial verify, patch |
| Rulings | Human, 18-07-2026 |
| Handoffs minted | H1273–H1277 (5), all 🟡 queued. Three drafted waves were **not** minted |

## The one thing to know before reading it

**This roadmap was re-scoped between authoring and minting, and the sections still carry their
original wave names.** Four handoffs minted the same day by concurrent sessions — H1257, H1258,
H1260, H1261 — took over roughly 40% of what it drafted. Sections W1-A, W2-A and W3-A carry
banners recording what actually happened. The plan's §4 disposition table is the authoritative
account; this roadmap's per-wave sections are the working detail behind it.

## Limitations

| # | Limitation |
|---|---|
| L1 | The applied/open split (21 applied / 60 open of 81 applicable) is evidence-graded, not exhaustively hand-verified. It is the gated output of H1273, not an input to it. |
| L2 | Written against `origin/main` at `3b4f9e4`. Numbers moved *during* authoring — the `precative` sheet went 3-open → 0-open mid-pass when [PR #416](https://github.com/gasyoun/SanskritGrammar/pull/416) merged. Re-derive, never re-cite. |
| L3 | Four of the 13 vote sheets have lost their `_review.html`; three of those use positional ids with no external registry, so ~8 open notes have referents that must be reconstructed by text-matching against article prose. That reconstruction may fail for some. |
| L4 | The charter de-calendar ruling is **deferred, not dropped** — it is owned by no handoff right now. If H1260 lands and nobody re-mints it, the charter stays two years out of step with production. This is the most likely thing to be silently lost. |
| L5 | The consolidation freeze ordered 18-07-2026 (H1260) postdates this roadmap's framing. Wave order here does not add new article manifests, so it is compatible — but the governance context is newer than the document. |

## Improvement backlog

| Rank | Item | Why |
|---|---|---|
| 1 | Re-mint the charter de-calendar once H1260 lands (L4) | It is the only ruling from this pass with no owner. Deferred work with no handoff is how a ruling evaporates. |
| 2 | Fold H1257's and H1258's actual outcomes back into the note index | Two of the five sheets are being applied by other sessions; the index is wrong the moment they land unless it is reconciled. |
| 3 | Decide whether the reconstructed-referent notes (L3) are worth the effort | If text-matching cannot place a note confidently, applying it is guesswork; better to mark it unrecoverable than to invent a target. |
| 4 | Re-derive the published/candidate split from article manifests, not the banner | Banner-grep is not a status signal (the string occurs in all 35 articles, including published ones via revision-history rows). H1260 reads 9 published / 26 candidates from manifests. |

## Related

- [PLAN_SANGRAM_EDITORIAL_NOTES_AND_CHARTER_2026H2.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANGRAM_EDITORIAL_NOTES_AND_CHARTER_2026H2.md) — the index, and its `.meta.md`
- [SANGRAM_CHARTER_2026_2031.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_CHARTER_2026_2031.mdx) — the constitution the de-calendar ruling targets
- [ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md) — the portfolio roadmap H1277 re-bases

## Revision history

| Date | Change | Model |
|---|---|---|
| 18-07-2026 | Created alongside the roadmap; records the mint-time re-scope against four concurrent handoffs | Opus 4.8 (`claude-opus-4-8`) |

_Dr. Mārcis Gasūns_
