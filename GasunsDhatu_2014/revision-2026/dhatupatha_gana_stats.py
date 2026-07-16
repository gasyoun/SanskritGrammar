#!/usr/bin/env python3
"""Структурная статистика цифровой дхатупатхи vidyut для §2.1 Гл. 2 (H1069).

Считает по WhitneyRoots/scratch/vidyut_data/prakriya/dhatupatha.tsv:
  - общее число дхату и распределение по ганам (10 классов);
  - повторные вхождения одной и той же аупадешика-формы (raw SLP1,
    анубандхи НЕ снимаются — см. честный предел в Гл. 5 / PALSULE_AUDIT:
    наивный it-stripped джойн даёт ложные срабатывания);
  - формы, встречающиеся более чем в одной гане.

Выход: печать сводки + dhatupatha_gana_stats_provenance.json рядом со скриптом.
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
DEFAULT_TSV = (
    HERE.parents[2] / "WhitneyRoots" / "scratch" / "vidyut_data" / "prakriya" / "dhatupatha.tsv"
)

GANA_NAMES = {
    "01": "bhvādi", "02": "adādi", "03": "juhotyādi", "04": "divādi",
    "05": "svādi", "06": "tudādi", "07": "rudhādi", "08": "tanādi",
    "09": "kryādi", "10": "curādi",
}


def main() -> None:
    tsv = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_TSV
    rows = []
    with tsv.open(encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        assert header == ["code", "dhatu", "artha"], header
        for line in fh:
            code, dhatu, artha = line.rstrip("\n").split("\t")
            gana = code.split(".")[0]
            rows.append((gana, dhatu, artha))

    total = len(rows)
    per_gana = Counter(g for g, _, _ in rows)

    form_entries = defaultdict(list)
    for gana, dhatu, _ in rows:
        form_entries[dhatu].append(gana)

    distinct_forms = len(form_entries)
    repeated_forms = {f: gs for f, gs in form_entries.items() if len(gs) > 1}
    multi_gana_forms = {f: sorted(set(gs)) for f, gs in form_entries.items() if len(set(gs)) > 1}
    repeat_entries = sum(len(gs) for gs in repeated_forms.values())

    print(f"file: {tsv}")
    print(f"total entries (dhatu): {total}")
    print(f"distinct raw aupadesika forms: {distinct_forms}")
    print(f"forms listed more than once: {len(repeated_forms)} "
          f"(covering {repeat_entries} entries)")
    print(f"forms listed in >1 gana: {len(multi_gana_forms)}")
    print("per-gana counts:")
    for g in sorted(per_gana):
        print(f"  {g} {GANA_NAMES.get(g, '?'):<10} {per_gana[g]}")

    prov = {
        "source": "WhitneyRoots/scratch/vidyut_data/prakriya/dhatupatha.tsv",
        "checked": "17-07-2026",
        "computed_by": "Fable 5 (claude-fable-5), H1069",
        "total_entries": total,
        "distinct_raw_forms": distinct_forms,
        "forms_repeated": len(repeated_forms),
        "entries_in_repeated_forms": repeat_entries,
        "forms_in_multiple_ganas": len(multi_gana_forms),
        "per_gana": {f"{g} {GANA_NAMES.get(g, '?')}": per_gana[g] for g in sorted(per_gana)},
        "note": "raw SLP1 aupadesika strings compared as-is; anubandhas not stripped "
                "(naive it-stripped joins give false positives, see PALSULE_AUDIT / Гл. 5)",
    }
    out = HERE / "dhatupatha_gana_stats_provenance.json"
    out.write_text(json.dumps(prov, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"provenance -> {out.name}")


if __name__ == "__main__":
    main()
