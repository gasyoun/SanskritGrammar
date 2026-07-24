"""H1613 freeze-exit probe for SG-MO-019 (art:aorist-types).

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
    "toc_ref": "SG-MO-019",
    "art_id": "art:aorist-types",
    "slug": "aorist-types",
    "programme_slot": "C5 · cluster «Перфект, аорист, будущее» (beyond-quota partition of SG-MO-018)",
    "matrix_path": "sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md",
    "matrix_url": "https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md",
    "instrument_script": "scripts/sg_mo_019_aorist_types.py",
    "kill_gate_criterion": "MISSING — C5 § 7 pilots are only MO-002 / MO-013 / MO-017 / WF-008 / WF-003. Nearest related pilot text is C5 P3 (SG-MO-017 perfect), which does NOT transfer.",
    "criterion_status": "MISSING",
    "probe_action": "park_and_skip",
    "disposition_action": "leave_unknown",
    "verdict": "escalated",
    "do_not": "Do not transfer C5 P3 form-class 95% gate from perfect to aorist-types.",
    "escalate_path": "Human @DECIDE for a per-slot MO-019 gate, or visa-only path. Context: C5 EM2.",
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
