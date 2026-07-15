#!/usr/bin/env python
"""verify_claims_dcs.py — reproducible corpus statistics behind the Zaliznyak
Konspekt claim register (H797 Phase 2).

Both of this book's seed claims cite ground truth already computed elsewhere in this
cross-grammar program rather than needing a fresh query:
  - KZ-1 reuses Kochergina's HK-4 future-stem seṭ/aniṭ share (56.8%), already reproduced by
    KocherginaUchebnik_1998/verify_claims_dcs.py.
  - KZ-2 reuses the periphrastic-future tense-code table already built for
    BuhlerLeitfaden_1923/verify_claims_dcs.py (DCS-2021 timws.csv has no separate medium-voice
    periphrastic-future code).

This script exists for consistency with the other books' per-book verify script convention, and
to make the reuse explicit and re-runnable rather than just cited in prose. It recomputes the one
number this book's synthesis states independently: the periphrastic-future codebook check.

Ground-truth source: Digital Corpus of Sanskrit (Oliver Hellwig, DCS-2021, CC BY),
    ../../VisualDCS/src/DCS-data-2021/timws.csv  (tense/mood code -> label -> token count)

Usage:  python verify_claims_dcs.py            # report + rewrite claims_dcs_stats.json
        python verify_claims_dcs.py --check     # report only, no file write
"""
import sys, json, re
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
VDCS = REPO.parent / "VisualDCS"
DCS = VDCS / "src" / "DCS-data-2021"


def periphrastic_future_codebook_check():
    """KZ-2: does DCS-2021's tense/mood codebook (timws.csv) carry a separate medium-voice
    periphrastic-future code alongside the active one? Same code table BuhlerLeitfaden_1923's
    verify script reads."""
    rows = []
    for ln in (DCS / "timws.csv").read_text(encoding="utf-8").splitlines()[1:]:
        m = re.match(r"\s*(\d+):(.*):(\d+)\s*$", ln)
        if m:
            rows.append((int(m.group(1)), m.group(2).strip(), int(m.group(3))))
    periph = [(c, lbl, n) for c, lbl, n in rows if "ppf" in lbl.lower() or "periph" in lbl.lower()]
    return {
        "periphrastic_future_codes_found": periph,
        "has_separate_medium_code": any("med" in lbl.lower() for _, lbl, _ in periph),
    }


def analyze():
    return {
        "_source": "DCS-2021 (Oliver Hellwig, CC BY) via VisualDCS/src/DCS-data-2021/timws.csv",
        "_note": "KZ-1 reuses KocherginaUchebnik_1998's HK-4 (-iṣya 56.8%) verbatim — not recomputed here.",
        "KZ2_periphrastic_future_codebook": periphrastic_future_codebook_check(),
    }


def report(s):
    p = s["KZ2_periphrastic_future_codebook"]
    print(f"KZ-2 PERIPHRASTIC FUTURE CODEBOOK: {p['periphrastic_future_codes_found']} "
          f"-> separate medium-voice code exists: {p['has_separate_medium_code']}")


def main():
    stats = analyze()
    report(stats)
    if "--check" not in sys.argv:
        out = HERE / "claims_dcs_stats.json"
        out.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n-> wrote {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
