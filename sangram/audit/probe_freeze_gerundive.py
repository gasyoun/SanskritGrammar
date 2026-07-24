"""H1613 freeze-exit probe for SG-MO-024 (art:gerundive).

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
    "toc_ref": "SG-MO-024",
    "art_id": "art:gerundive",
    "slug": "gerundive",
    "programme_slot": "C5 · cluster «Именные формы глагола»; C6 also lists construction slot syn-c-gerundive (not mapped on this C2 id)",
    "matrix_path": "sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md",
    "matrix_url": "https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md",
    "instrument_script": "scripts/sg_mo_024_gerundive.py",
    "kill_gate_criterion": "MISSING — not a C5/C6 pilot.",
    "criterion_status": "MISSING",
    "probe_action": "park_and_skip",
    "disposition_action": "leave_unknown",
    "verdict": "escalated",
    "do_not": "Do not invent a gerundive construction kill-gate from C6 SYN-C without a written programme criterion.",
    "escalate_path": "Human @DECIDE or visa-only path.",
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
