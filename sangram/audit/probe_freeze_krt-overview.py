"""H1613 freeze-exit probe for SG-WF-002 (art:krt-overview).

Park-and-skip record only: C5 programme names no pilot kill-gate for this slot
(H1611 matrix). This script does NOT invent thresholds and does NOT run a
corpus kill-gate. Running it rewrites the sibling .json park artifact.

Matrix: sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md
Programme: sangram/SANGRAM_MORPHOLOGY_PROGRAM_W2.mdx § 7 (pilots only)
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).with_suffix(".json")

RESULT = {
    "handoff": "H1613",
    "executor": "Grok 4.5 (grok-4.5)",
    "date": "2026-07-24",
    "toc_ref": "SG-WF-002",
    "art_id": "art:krt-overview",
    "slug": "krt-overview",
    "programme_slot": "C5 · cluster «Деривация» (overview; script self-labels no kill-gate)",
    "matrix_path": "sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md",
    "matrix_url": "https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md",
    "instrument_script": "scripts/sg_wf_002_krt_overview.py",
    "kill_gate_criterion": "MISSING — overview, not pilot. Related C5 § 7 P5 (SG-WF-003) is a different published article.",
    "criterion_status": "MISSING",
    "probe_action": "park_and_skip",
    "disposition_action": "leave_unknown",
    "verdict": "escalated",
    "do_not": "Do NOT re-fire P5 surface-suffix dictionary-validation gate against the WF-002 overview spine (native VerbForm in {Part,Conv,Gdv,Inf}).",
    "escalate_path": "Visa-only or @DECIDE for an overview-specific freeze rule. Context: C5 EM5.",
    "corpus_probe_run": False,
    "kill_gated": False,
    "survivor_for_visa": True,
    "note": (
        "No fireable C5 § 7 pilot kill-gate for this C2 slot. Per freeze-exit "
        "autonomy, park with ledger blocking_note; route to non-SE visa sheet "
        "or human @DECIDE for a written per-slot gate. Not H1614 (SE-only)."
    ),
}


def main() -> None:
    OUT.write_text(
        json.dumps(RESULT, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"wrote {OUT} verdict={RESULT['verdict']} "
        f"criterion={RESULT['criterion_status']}"
    )


if __name__ == "__main__":
    main()
