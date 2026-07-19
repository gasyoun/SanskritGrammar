#!/usr/bin/env python3
"""Refresh the Sangram consolidation freeze ledger (H1260).

On 18-07-2026 Dr. Marcis Gasuns ruled a Sangram consolidation freeze: the audit
snapshot had 35 article manifests (9 published + 26 candidates); no new topic /
article manifest may be added until every one of the 26 baseline candidates has
an explicit `published` / `revised` / `rejected` / `kill_gated` disposition.

This script regenerates every NON-JUDGMENTAL field of
sangram/editorial/data/consolidation_ledger.json from the repo's own state and
NEVER touches the human-verdict fields (`disposition`, `blocking_note`,
`source_links`) — those are read from the existing ledger (if any) and written
back byte-identical. `visa_evidence` is a hybrid: mechanically re-derived from
`review/*_decisions.json` sheets (tracked in git since H1273/#455, which
reversed H856's earlier gitignore) when present, else preserved from the prior
ledger untouched (defensive only now that review/ is committed — this branch
still protects a future re-gitignore or a shallow/sparse checkout that omits
review/, never silently downgrading to "unknown" in that case).

The frozen 26-ID baseline itself is a LITERAL, HARDCODED list (FROZEN_BASELINE
below) — it is fixed at the moment the freeze was ruled and must never be
recomputed from the live candidate census, precisely because the live census
changes as candidates get dispositioned (H1257 and others). Re-deriving the
baseline from "whatever is a candidate today" would let the baseline shrink
silently as items are published, defeating the ledger's entire purpose.

Non-judgmental fields refreshed on every run:
  - revision_state       from sangram/articles/<slug>/article.manifest.json revisions[]
  - rederivation_evidence from DCS_DERIVED_NUMBERS_LEDGER_2026.md (H1229), parsed fresh
  - validator_evidence    from importing scripts/article_validate.py and calling validate()
  - last_refresh          repo-wide npm-build status, recorded once per run (human-supplied
                           via --build-status; this script does not itself shell out to npm)

Exit codes:
  0 = ledger refreshed cleanly
  1 = a baseline-integrity violation was found (duplicate / missing / unknown
      frozen-baseline ID) — the ledger is NOT written in this case, so a bad
      run can never silently corrupt the committed baseline.

Usage:
  python scripts/consolidation_ledger_refresh.py                  # refresh + write
  python scripts/consolidation_ledger_refresh.py --check           # refresh, diff, no write (exit 1 on drift)
  python scripts/consolidation_ledger_refresh.py --build-status pass
  python scripts/consolidation_ledger_refresh.py --self-test
"""
from __future__ import annotations

import argparse
import copy
import glob
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LEDGER_PATH = ROOT / "sangram" / "editorial" / "data" / "consolidation_ledger.json"
SCHEMA_PATH = ROOT / "sangram" / "editorial" / "data" / "consolidation_ledger.schema.json"
DCS_LEDGER_PATH = ROOT / "DCS_DERIVED_NUMBERS_LEDGER_2026.md"
ARTICLES_DIR = ROOT / "sangram" / "articles"
REVIEW_DIR = ROOT / "review"

if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import article_validate  # noqa: E402  (sibling script, imported after sys.path fix)

CONTRACT_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# The FROZEN baseline — locked 18-07-2026, the moment MG ruled the freeze.
# Never recompute this list from a live candidate scan. (toc_ref, art slug)
# ---------------------------------------------------------------------------
FROZEN_BASELINE = [
    ("SG-SE-004", "ablative-genitive"),
    ("SG-MO-026", "absolutive"),
    ("SG-MO-019", "aorist-types"),
    ("SG-MO-018", "aorist"),
    ("SG-WF-009", "bahuvrihi"),
    ("SG-SE-001", "case-system-overview"),
    ("SG-WF-006", "compounds-overview"),
    ("SG-MO-012", "conjugation-overview"),
    ("SG-MO-006", "consonant-stems"),
    ("SG-MO-024", "gerundive"),
    ("SG-SE-008", "imperative-optative"),
    ("SG-MO-016", "imperfect"),
    ("SG-MO-025", "infinitive"),
    ("SG-SE-003", "instrumental-dative"),
    ("SG-SE-013", "karaka-case"),
    ("SG-WF-002", "krt-overview"),
    ("SG-SE-005", "locative"),
    ("SG-SE-002", "nominative-accusative"),
    ("SG-MO-027", "passive"),
    ("SG-SE-006", "past-tenses"),
    ("SG-MO-022", "present-perfect-participles"),
    ("SG-WF-011", "preverbs"),
    ("SG-MO-010", "pronouns"),
    ("SG-MO-023", "ta-na-participles"),
    ("SG-SE-009", "voice"),
    ("SG-WF-001", "word-structure-overview"),
]
assert len(FROZEN_BASELINE) == 26, f"FROZEN_BASELINE must carry exactly 26 IDs, has {len(FROZEN_BASELINE)}"

# A handful of published articles carry visa/audit rows too; kept only as the
# `published_context` list so the freeze-reject check sees the full 35-ID
# allowed set. Also a literal, hardcoded 18-07 snapshot — see FROZEN_BASELINE
# docstring above for why.
PUBLISHED_AT_FREEZE = [
    ("SG-MO-002", "a-stems"),
    ("SG-MO-028", "causative"),
    ("SG-MO-001", "declension-overview"),
    ("SG-MO-021", "future"),
    ("SG-WF-003", "krt-suffixes"),
    ("SG-MO-017", "perfect"),
    ("SG-WF-004", "taddhita-overview"),
    ("SG-WF-008", "tatpurusha"),
    ("SG-MO-013", "thematic-present"),
]
assert len(PUBLISHED_AT_FREEZE) == 9, f"PUBLISHED_AT_FREEZE must carry exactly 9 IDs, has {len(PUBLISHED_AT_FREEZE)}"

# The w2-core-11candidates-visa sheet uses a handful of shorthand IDs that do
# not follow the mechanical <DOMAIN><int(number)> pattern derivable from
# toc_ref. Document every exception here instead of silently mis-parsing.
REVIEW_ID_ALIASES = {
    "V": "voice",
}


def manifest_path(slug: str) -> Path:
    return ARTICLES_DIR / slug / "article.manifest.json"


def toc_short_code(toc_ref: str) -> str:
    """SG-MO-012 -> 'MO12' (the shorthand code used by review/*_decisions.json)."""
    m = re.match(r"^SG-([A-Z]{2})-(\d{3})$", toc_ref)
    if not m:
        return toc_ref
    domain, num = m.groups()
    return f"{domain}{int(num):02d}"


def load_prior_ledger() -> dict | None:
    if not LEDGER_PATH.exists():
        return None
    try:
        return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def prior_row_by_toc(prior: dict | None, toc_ref: str) -> dict | None:
    if not prior:
        return None
    for row in prior.get("baseline_ids", []):
        if row.get("toc_ref") == toc_ref:
            return row
    return None


# ---------------------------------------------------------------------------
# 1. revision_state — non-judgmental, from the manifest itself
# ---------------------------------------------------------------------------
def compute_revision_state(slug: str) -> str:
    p = manifest_path(slug)
    if not p.exists():
        return "unknown"
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return "unknown"
    kinds = [r.get("kind") for r in d.get("article", {}).get("revisions", [])]
    return "published" if "published" in kinds else "candidate"


# ---------------------------------------------------------------------------
# 2. rederivation_evidence — parsed fresh from DCS_DERIVED_NUMBERS_LEDGER_2026.md
# ---------------------------------------------------------------------------
_ROW_RE = re.compile(
    r"^\|\s*`([A-Z0-9-]+)`\s*\|\s*(.+?)\s*\|\s*.+?\s*\|\s*.+?\s*\|\s*(CONFIRMED|\*\*REFUTED\*\*|PLAUSIBLE)\s*\|\s*(.+?)\s*\|\s*$"
)
# Anchors reference article slugs as "<slug>:<line>"; several rows share one
# anchor via " + " or " vs "; non-article anchors (checkpoint/manifest/"same"/
# a .mdx doc) contribute no evidence to any single article slug.
_ANCHOR_SLUG_RE = re.compile(r"^([a-z][a-z0-9-]*):\d+")


def _known_slugs() -> set[str]:
    return {p.parent.name for p in ARTICLES_DIR.glob("*/article.manifest.json")}


def parse_dcs_ledger() -> dict[str, list[tuple[str, str, str]]]:
    """slug -> [(check_id, verdict, resolution), ...]."""
    by_slug: dict[str, list[tuple[str, str, str]]] = {}
    if not DCS_LEDGER_PATH.exists():
        return by_slug
    known = _known_slugs()
    text = DCS_LEDGER_PATH.read_text(encoding="utf-8")
    for line in text.splitlines():
        m = _ROW_RE.match(line)
        if not m:
            continue
        check_id, anchor, verdict, resolution = m.groups()
        verdict = "REFUTED" if "REFUTED" in verdict else verdict
        pieces = re.split(r"\s+\+\s+|\s+vs\s+", anchor)
        slugs_in_row = set()
        for piece in pieces:
            am = _ANCHOR_SLUG_RE.match(piece.strip())
            if am and am.group(1) in known:
                slugs_in_row.add(am.group(1))
        for slug in slugs_in_row:
            by_slug.setdefault(slug, []).append((check_id, verdict, resolution))
    return by_slug


def compute_rederivation_evidence(slug: str, dcs_by_slug: dict) -> dict:
    rows = dcs_by_slug.get(slug, [])
    if not rows:
        return {
            "status": "not_audited",
            "confirmed": 0,
            "refuted": 0,
            "checked_ids": [],
            "note": "no article-native published number fell inside H1229's 129-check "
                    "adversarial re-derivation scope; absence of evidence, not evidence of correctness.",
        }
    confirmed = sum(1 for _, v, _ in rows if v == "CONFIRMED")
    refuted = [(cid, res) for cid, v, res in rows if v == "REFUTED"]
    checked_ids = sorted({cid for cid, _, _ in rows})
    if refuted:
        # DCS_DERIVED_NUMBERS_LEDGER_2026.md convention: every per-row REFUTED
        # resolution that starts "corrected: ..." names a value that was already
        # fixed in the same PR (see the doc's "Frozen invariants honoured" section
        # — every REFUTED verdict is backed by a runnable committed script, never
        # left as an open claim). A resolution NOT starting with "corrected:" would
        # mean the number is refuted but no fix has landed yet.
        fixed = all(res.strip().lower().startswith("corrected:") for _, res in refuted)
        status = "refuted_fixed" if fixed else "refuted_open"
        note = "H1229 found " + "; ".join(f"{cid}: {res}" for cid, res in refuted)
    else:
        status = "confirmed"
        note = f"H1229 adversarial re-derivation: {confirmed}/{len(rows)} checks CONFIRMED, 0 REFUTED."
    return {
        "status": status,
        "confirmed": confirmed,
        "refuted": len(refuted),
        "checked_ids": checked_ids,
        "note": note,
    }


# ---------------------------------------------------------------------------
# 3. visa_evidence — mechanically re-derived from local review/*_decisions.json
#    when present on this machine; else PRESERVED from the prior ledger.
# ---------------------------------------------------------------------------
def parse_local_visa_sheets() -> dict[str, dict]:
    """toc_short_code -> {"decision": ..., "note": ..., "sheet": sheet_id}."""
    out: dict[str, dict] = {}
    if not REVIEW_DIR.exists():
        return out
    for fp in sorted(REVIEW_DIR.glob("*_decisions.json")):
        try:
            d = json.loads(fp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        sheet_id = d.get("sheet_id", fp.stem)
        for item in d.get("items", []):
            code = item.get("id")
            if not code:
                continue
            out.setdefault(code, {
                "decision": item.get("decision"),
                "note": item.get("note", ""),
                "sheet": sheet_id,
            })
    return out


def compute_visa_evidence(toc_ref: str, slug: str, local_votes: dict, prior_row: dict | None) -> dict:
    code = toc_short_code(toc_ref)
    aliased_codes = [c for c, s in REVIEW_ID_ALIASES.items() if s == slug]
    candidates = [code] + aliased_codes
    for c in candidates:
        if c in local_votes:
            v = local_votes[c]
            status = "approved" if v["decision"] == "approve" else "pending"
            return {
                "status": status,
                "sheet": v["sheet"],
                "note": f"vote={v['decision']!r} on local review sheet {v['sheet']!r} "
                        f"(short code {c!r}); apply via its owning handoff, never by analogy.",
            }
    if prior_row and "visa_evidence" in prior_row:
        # No local review/ data on this machine (e.g. CI) — preserve, don't downgrade.
        return prior_row["visa_evidence"]
    return {
        "status": "not_submitted",
        "sheet": None,
        "note": "",
    }


# ---------------------------------------------------------------------------
# 4. validator_evidence — import + call the real validator, always fresh.
# ---------------------------------------------------------------------------
def compute_validator_evidence(slug: str, today: str) -> dict:
    p = manifest_path(slug)
    if not p.exists():
        return {"article_validate": "unknown", "checked_at": today}
    try:
        serialized = p.read_text(encoding="utf-8")
        manifest = json.loads(serialized)
        errors, _warnings = article_validate.validate(manifest, serialized)
    except Exception:
        return {"article_validate": "unknown", "checked_at": today}
    return {"article_validate": "pass" if not errors else "fail", "checked_at": today}


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def build_ledger(today: str, build_status: str) -> dict:
    prior = load_prior_ledger()
    dcs_by_slug = parse_dcs_ledger()
    local_votes = parse_local_visa_sheets()

    # -- baseline-integrity gate ------------------------------------------
    live_candidates = {
        p.parent.name for p in ARTICLES_DIR.glob("*/article.manifest.json")
        if compute_revision_state(p.parent.name) == "candidate"
    }
    frozen_slugs = [slug for _, slug in FROZEN_BASELINE]
    dupes = [s for s in set(frozen_slugs) if frozen_slugs.count(s) > 1]
    if dupes:
        raise SystemExit(f"BASELINE INTEGRITY: duplicate frozen-baseline slug(s): {dupes}")
    missing = [(t, s) for t, s in FROZEN_BASELINE if not manifest_path(s).exists()]
    if missing:
        raise SystemExit(f"BASELINE INTEGRITY: frozen-baseline ID(s) with no manifest on disk: {missing}")
    # A frozen-baseline slug is allowed to have since flipped to 'published'
    # (that IS a valid disposition path — H1257 et al.) so we do NOT require
    # it to still be a live candidate. We DO require every *current* live
    # candidate to be a member of the frozen baseline: a live candidate slug
    # outside FROZEN_BASELINE is a freeze violation (a 27th+ topic slipped
    # through under the same rules a pre-freeze candidate would have used).
    unknown = sorted(live_candidates - set(frozen_slugs))
    if unknown:
        raise SystemExit(
            "BASELINE INTEGRITY / FREEZE VIOLATION: candidate article manifest(s) not in the "
            f"frozen 18-07-2026 baseline: {unknown} — the consolidation freeze (H1260) forbids "
            "new candidates while it is active; disposition the 26 baseline IDs first."
        )

    baseline_rows = []
    for toc_ref, slug in FROZEN_BASELINE:
        prior_row = prior_row_by_toc(prior, toc_ref)
        row = {
            "toc_ref": toc_ref,
            "art_id": f"art:{slug}",
            "path": f"sangram/articles/{slug}/article.manifest.json",
            "revision_state": compute_revision_state(slug),
            "rederivation_evidence": compute_rederivation_evidence(slug, dcs_by_slug),
            "visa_evidence": compute_visa_evidence(toc_ref, slug, local_votes, prior_row),
            "validator_evidence": compute_validator_evidence(slug, today),
            # -- human verdict fields: preserved verbatim, defaulted only on first run --
            "disposition": (prior_row or {}).get("disposition", "unknown"),
            "blocking_note": (prior_row or {}).get("blocking_note", ""),
            "source_links": (prior_row or {}).get("source_links", []),
        }
        baseline_rows.append(row)

    published_rows = [
        {"toc_ref": t, "art_id": f"art:{s}", "path": f"sangram/articles/{s}/article.manifest.json"}
        for t, s in PUBLISHED_AT_FREEZE
    ]

    prior_freeze = (prior or {}).get("freeze", {})
    ledger = {
        "$schema": "./consolidation_ledger.schema.json",
        "contract_version": CONTRACT_VERSION,
        "freeze": {
            "active": prior_freeze.get("active", True),
            "ruled_by": "Dr. Marcis Gasuns",
            "ruled_date": "2026-07-18",
            "ruling_handoff": "MG in-chat ruling, 18-07-2026",
            "installing_handoff": "H1260",
            "precedence_rule": "Sangram's 'full cadence' (the general 7C ruling that every research "
                                "track stays at full production cadence) is superseded, for Sangram "
                                "only, by this consolidation freeze: 'full cadence' now means "
                                "consolidation cadence (repair/revise/visa/disposition of the 26 "
                                "baseline candidates), not new-topic production. Other research "
                                "tracks are unaffected.",
            "exit_criterion": "freeze.active flips to false only when every baseline_ids[] row has "
                               "disposition in {published, revised, rejected, kill_gated} — i.e. "
                               "disposition == 'unknown' for zero rows.",
            "baseline_snapshot_date": "2026-07-18",
            "related_handoffs": [
                "H1257 (applies 11 of the 26 baseline candidates' w2-core visa decisions; "
                "consumed here without duplication once it lands)",
                "H1229 (DCS-derived-number adversarial re-derivation; source of rederivation_evidence)",
            ],
            "counts": {"published_at_freeze": 9, "candidate_at_freeze": 26, "total_at_freeze": 35},
        },
        "last_refresh": {
            "date": today,
            "commands": [
                "python scripts/consolidation_ledger_refresh.py",
                "python scripts/article_validate.py --all",
                "python -m pytest",
                "npm run build",
            ],
            "build_status": build_status,
        },
        "published_context": published_rows,
        "baseline_ids": baseline_rows,
    }
    return ledger


def status_totals(ledger: dict) -> dict:
    totals = {"unknown": 0, "published": 0, "revised": 0, "rejected": 0, "kill_gated": 0}
    for row in ledger["baseline_ids"]:
        totals[row["disposition"]] += 1
    return totals


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="refresh in-memory, diff, exit 1 on drift, never write")
    ap.add_argument("--build-status", choices=["pass", "fail", "unknown"], default=None,
                     help="record the last `npm run build` outcome (this script does not run npm itself)")
    ap.add_argument("--today", default=None, help="override the refresh date (tests only)")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    import datetime
    today = args.today or datetime.date.today().isoformat()
    prior = load_prior_ledger()
    build_status = args.build_status or (prior or {}).get("last_refresh", {}).get("build_status", "unknown")

    try:
        ledger = build_ledger(today, build_status)
    except SystemExit as e:
        print(f"ERROR {e}")
        return 1

    totals = status_totals(ledger)
    print(f"baseline: {len(ledger['baseline_ids'])} rows — disposition totals: {totals}")
    serialized = json.dumps(ledger, indent=2, ensure_ascii=False, sort_keys=False) + "\n"

    if args.check:
        current = LEDGER_PATH.read_text(encoding="utf-8") if LEDGER_PATH.exists() else None
        if current == serialized:
            print("PASS  consolidation_ledger.json is up to date")
            return 0
        print("FAIL  consolidation_ledger.json is stale — run without --check to refresh")
        return 1

    LEDGER_PATH.write_text(serialized, encoding="utf-8")
    print(f"wrote {LEDGER_PATH}")
    return 0


def self_test() -> int:
    """Exercise the freeze-integrity gate and the field-preservation contract."""
    failures = []

    # 1. toc_short_code mapping
    cases = {"SG-MO-012": "MO12", "SG-WF-006": "WF06", "SG-SE-013": "SE13", "SG-MO-001": "MO01"}
    for toc, expect in cases.items():
        got = toc_short_code(toc)
        if got != expect:
            failures.append(f"toc_short_code({toc!r}) = {got!r}, expected {expect!r}")

    # 2. FROZEN_BASELINE / PUBLISHED_AT_FREEZE integrity
    if len(FROZEN_BASELINE) != 26:
        failures.append(f"FROZEN_BASELINE has {len(FROZEN_BASELINE)} entries, expected 26")
    if len(PUBLISHED_AT_FREEZE) != 9:
        failures.append(f"PUBLISHED_AT_FREEZE has {len(PUBLISHED_AT_FREEZE)} entries, expected 9")
    if len(set(s for _, s in FROZEN_BASELINE)) != 26:
        failures.append("FROZEN_BASELINE contains duplicate slugs")
    overlap = {s for _, s in FROZEN_BASELINE} & {s for _, s in PUBLISHED_AT_FREEZE}
    if overlap:
        failures.append(f"FROZEN_BASELINE and PUBLISHED_AT_FREEZE overlap: {overlap}")

    # 3. build_ledger against the real repo state must not raise, and must
    #    preserve a synthetic human-verdict field across two runs.
    try:
        today = "2026-07-19"
        first = build_ledger(today, "unknown")
        row0 = first["baseline_ids"][0]
        row0["disposition"] = "revised"
        row0["blocking_note"] = "SELF-TEST SENTINEL"
        row0["source_links"] = ["https://example.org/self-test"]
        LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
        original = LEDGER_PATH.read_text(encoding="utf-8") if LEDGER_PATH.exists() else None
        try:
            LEDGER_PATH.write_text(json.dumps(first, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            second = build_ledger(today, "unknown")
            row0b = next(r for r in second["baseline_ids"] if r["toc_ref"] == row0["toc_ref"])
            if row0b["disposition"] != "revised" or row0b["blocking_note"] != "SELF-TEST SENTINEL":
                failures.append("human-verdict fields were NOT preserved across a refresh run")
        finally:
            if original is not None:
                LEDGER_PATH.write_text(original, encoding="utf-8")
            elif LEDGER_PATH.exists():
                LEDGER_PATH.unlink()
    except SystemExit as e:
        failures.append(f"build_ledger raised on the real repo state: {e}")

    # 4. a synthetic unknown candidate must trip the freeze-violation gate
    sentinel = ARTICLES_DIR / "self-test-sentinel-topic"
    try:
        sentinel.mkdir(exist_ok=True)
        (sentinel / "article.manifest.json").write_text(json.dumps({
            "article": {"id": "art:self-test-sentinel-topic", "revisions": []}
        }), encoding="utf-8")
        try:
            build_ledger("2026-07-19", "unknown")
            failures.append("a synthetic new candidate outside FROZEN_BASELINE did NOT trip the freeze gate")
        except SystemExit:
            pass  # expected
    finally:
        if (sentinel / "article.manifest.json").exists():
            (sentinel / "article.manifest.json").unlink()
        if sentinel.exists():
            sentinel.rmdir()

    for f in failures:
        print(f"SELF-TEST FAIL: {f}")
    n = 4
    print(f"{'PASS' if not failures else 'FAIL'}  self-test: {n - len(failures)}/{n} checks green")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
