# SanskritGrammar OxAlpha code-review implementation

_Created: 29-08-2026 · Last updated: 29-08-2026_

1. Start from fresh origin/main (worktree `SanskritGrammar-h3550-drain`); read CLAUDE.md, state, README, changelog, CI, and relevant plans.
2. Add canonical files under [docs/agents](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/agents), append the `## Agent skills` block to CLAUDE.md, keep PR intake OFF, create only missing labels, and merge separately.
3. Census ~130 merged PRs in 26-07-2026..25-08-2026; retain at most ten executable-risk slices: #600 (+#865/#866/#868 re-merges), #578 (+#577 duplicate merge), #599, #589, #529, #848, #849, #592, #882, #590. Replace out-of-window or non-executable candidates without exceeding ten.
4. Fetch PR body, files, base SHA, and head SHA; resolve spec evidence in the ruled order.
5. Run independent bounded passes focused on the pre-push guard family, CI validator gates, offline-search patches, data readers, the compound splitter, the uv workspace seam, same-SHA Pages gating, the cross-repo claims gate, the lessonpack generator, and the visa-sheet screening wire.
6. Publish [the report](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/reviews/OXALPHA_RETROSPECTIVE_CODE_REVIEW_26-08-2026.md) with explicit exclusions and no-spec outcomes.
7. For every proven P0/P1, add adjacent regression proof, implement the smallest fix, run focused and repository gates, and merge a minimal green PR.
8. Write [the design](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/OXALPHA_STATUS_GATE_DESIGN_2026.md) without altering workflows/protection.
9. Update changelog/state; close only after adapter, report, applicable fixes, and design exist.

_Dr. Mārcis Gasūns_
