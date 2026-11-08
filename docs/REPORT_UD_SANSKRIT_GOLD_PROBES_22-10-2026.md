# REPORT — UD_Sanskrit-UFAL gold layer landed + claims.yml dependency/lemma probes (H6842)

_Date: 22-10-2026 · Executor: OxAlpha (opencode/z-ai/glm-5.3-flash) · WHEEL9 visa item (b) · Repo: SanskritGrammar_

## Outcome (one line)

UD_Sanskrit-UFAL mirrored as a DATA-ONLY external gold layer (`data/ud_sanskrit/`, licence
facts recorded, CC BY-SA 4.0 — no GPL vendoring) and 4 claims.yml probe rows run against it
with dual verdicts (fact axis + UD-proxy axis): **3 PASS · 1 OVERSTATED**.

## Visa provenance (gate honesty)

The WHEEL9-sandhi-nlp-wave1 @DECIDE row (visa due 18-10-2026) is still open in GTD — no
recorded MG decision. The handoff's structured gate `until:2026-10-18` is authoritative and
"releases itself on expiry" (HANDOFF_LIFECYCLE_MACHINERY_DEEP_MANUAL.md §4.3 step 5); the
window closed without a refusal, the drain claimed the unit 22-10-2026T06:57Z, and the
dossier recommendation for item (b) was ADOPT. Execution proceeded on that basis; if MG
retro-vetoes item (b), the layer is mirror-only and trivially revertible.

## Data landed (mirror-only)

- `data/ud_sanskrit/sa_ufal-ud-test.conllu` — byte-exact mirror of upstream
  [UD_Sanskrit-UFAL](https://github.com/UniversalDependencies/UD_Sanskrit-UFAL) master,
  commit `80f88c8bb3c933deb272bb7a0b7683352134f57e`, fetched 22-10-2026. Last substantive
  annotation change v2.2 (2018). Upstream untouched (no PRs back).
- `data/ud_sanskrit/README.md` — provenance + licence note. Licence facts: GitHub repo-level
  metadata NOASSERTION; treebank data **CC BY-SA 4.0** per upstream README machine-readable
  block and LICENSE.txt. The official LINDAT release bundle was unreachable at fetch time
  (3 retries across endpoints) — recorded in the README; verifier re-fetches the upstream
  blob and diffs.
- Measured size: **230 sentences / 1,843 tokens** (probe count; multi-word tokens and empty
  nodes excluded from the token count).

## Probes (tools/verify_claims_ud.py → data/ud_sanskrit/claims_ud_stats.json)

Register: `data/ud_sanskrit/claims.yml` (new UD-gold probe register; thresholds fixed before
the first run; dual verdicts mirrored back into the rows). Existing-claim replication: UDA-1
re-tests APT-3 (ApteSyntax_1885, `ca` postposition) on the new gold.

| Row | Claim | UD proxy (threshold) | Measured | verdict_fact / verdict_ud |
|---|---|---|---|---|
| UDA-1 | `ca` never sentence-initial (replicates APT-3) | 0 initial / total CCONJ-च | **0/30** | TRUE / PASS |
| UDA-2 | Sanskrit dominantly OV order | obj/iobj before verbal head ≥66.7% | **89.3%** of 103 | TRUE / PASS |
| UDA-3 | Verbless nominal sentences common in prose | non-verbal-root sentences ≥5% | **16.5%** of 230 | TRUE / PASS |
| UDA-4 | Top verb lemma = अस् (as, 'be') | rank 1 → PASS, 2-3 → OVERSTATED | **rank 2** (n=20; कृ 25) | OVERSTATED / OVERSTATED |

First results, honestly: the enclitic-`ca` absolute (APT-3/APT-9 class) replicates clean on a
second, independently annotated gold (0/30); the OV-doctrine and verbless-sentence rows land
where reference grammars put them; and the "most frequent verb is 'be'" folk-claim comes out
OVERSTATED on this gold — कृ (do/make) tops the VERB/AUX lemma census (25 vs 20), with the
caveat that UD lemma counts fold sandhi and mix finite + non-finite uses.

## Schema-mapping caveat (UD label mandatory)

Every number above is a **UD v2** measurement — DEPREL (`root`, `nsubj`, `obj`), UPOS
(VERB/AUX/NOUN/…), UD lemma column (Devanagari). Our claim registers speak
Paninian/karaka-DCST terms; UD `nsubj`/`obj` do NOT carry the karaka distinction, UD lemma
folds sandhi'd surface forms, and non-verbal roots cover what Paninian grammar treats as
copula-omission nominal sentences. These numbers are comparable to other UD treebanks, NOT
directly to the DCS head/deprel slices of `apte_treebank_stats.py` (H1059/H1062) — cross-schema
comparison without the stated scheme is invalid (wheel dossier rule). The full mapping
paragraph lives in the `claims.yml` header.

## Checks

- `python tools/verify_claims_ud.py` → PASS (report + `claims_ud_stats.json` + verdict
  write-back; re-run idempotent; `--check` = report only).
- `ruff check --select=E9,F63,F7,F8` → PASS. `yaml.safe_load` on the register → PASS.
- No GPL files vendored (single conllu mirror, CC BY-SA 4.0); upstream untouched.

## Risks / limits

- LINDAT (official release host) unreachable from the drain box at fetch time — mirror is the
  GitHub master snapshot (content last substantively changed 2018); verifier should re-diff
  against upstream.
- The gold is small (230 sentences, genre fiction) — thresholds were calibrated so "common/
  dominant" claims don't pass on noise; UDA-4's rank claim is census-fact, not inference.
- Probe set is deliberately dependency/lemma-only (no parser built), per handoff scope.

## Inspect (verifier opens first)

1. `data/ud_sanskrit/README.md` (licence + provenance)
2. `data/ud_sanskrit/claims.yml` (schema label + mapping paragraph + dual verdicts)
3. `tools/verify_claims_ud.py` + `data/ud_sanskrit/claims_ud_stats.json` (re-run one row)
