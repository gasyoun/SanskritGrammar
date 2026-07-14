#!/usr/bin/env python3
"""varga_shares.py — H246 (GasunsDhatu 2026 print prep), MG decision Q3 of 06-07-2026.

Aggregates the 25 sparsa varnas (stops + nasals) from VisualDCS
derived-data/Fonetika/regen-2026/varna_freq.csv (48 varnas x DCS time slots 1..5)
into the 5 traditional vargas (kanthya/talavya/murdhanya/dantya/oshthya),
computes per-epoch shares (replacing the chi-squared p-value table, defect L7)
and the effect size (Cramer's V) for the varga x epoch contingency table.

Source data: DCS CoNLL-U (Oliver Hellwig), CC BY 4.0; pin 2026-03-05,
4,240,775 words / 31,805,819 varnas. Reproducible via
VisualDCS/derived-data/Fonetika/regen-2026/build_akshara_ligature_freq.py.

Aggregation math lives in the shared VisualDCS `varga_engine.varga_shares()`
(H926) — this file only supplies the RU varga membership/labels and CSV
formatting.

Usage:  python varga_shares.py [path-to-varna_freq.csv]
Writes: varga_shares.csv next to this script; prints a summary.
"""
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

HERE = Path(__file__).resolve().parent
GITHUB_ROOT = HERE.parents[2]
ENGINE_DIR = GITHUB_ROOT / 'VisualDCS' / 'derived-data' / 'Fonetika' / 'varga-series-diachrony'
sys.path.insert(0, str(ENGINE_DIR))
from varga_engine import varga_shares, SLOTS

DEFAULT_SRC = GITHUB_ROOT / 'VisualDCS' / 'derived-data' / 'Fonetika' / 'regen-2026' / 'varna_freq.csv'

# slp1 -> varga for the 25 sparsa varnas (stops + nasals)
VARGAS = {
    'кантхья (гуттуральные)': ['k', 'K', 'g', 'G', 'N'],
    'талавья (палатальные)':  ['c', 'C', 'j', 'J', 'Y'],
    'мурдханья (церебральные)': ['w', 'W', 'q', 'Q', 'R'],
    'дантья (дентальные)':    ['t', 'T', 'd', 'D', 'n'],
    'оштхья (лабиальные)':    ['p', 'P', 'b', 'B', 'm'],
}
EPOCH_LABELS = ['ведийский', 'эпический', 'классический', 'средневековый', 'поздний']


def main() -> None:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC
    counts, shares, chi2, cramers_v = varga_shares(str(src), VARGAS, EPOCH_LABELS)

    slot_totals = [sum(counts[v][i] for v in VARGAS) for i in range(len(SLOTS))]
    grand = sum(slot_totals)

    out = Path(__file__).with_name('varga_shares.csv')
    with out.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['varga'] + [f'{e}_count' for e in EPOCH_LABELS] + [f'{e}_share_pct' for e in EPOCH_LABELS] + ['total_count', 'total_share_pct'])
        for v in VARGAS:
            row_total = sum(counts[v])
            sh = shares[v]
            w.writerow([v] + counts[v] + [f'{s:.2f}' for s in sh] + [row_total, f'{100 * row_total / grand:.2f}'])
        w.writerow(['ИТОГО'] + slot_totals + [''] * len(SLOTS) + [grand, '100.00'])
        w.writerow([])
        w.writerow(['chi2', f'{chi2:.1f}'])
        w.writerow(['cramers_v', f'{cramers_v:.4f}'])

    print(f'sparsa total: {grand:,} of 31,805,819 varnas')
    print(f"chi2 = {chi2:,.1f}   Cramer's V = {cramers_v:.4f}")
    print()
    hdr = 'varga'.ljust(28) + ''.join(e.rjust(15) for e in EPOCH_LABELS)
    print(hdr)
    for v in VARGAS:
        sh = shares[v]
        print(v.ljust(28) + ''.join(f'{s:14.2f}%' for s in sh))
    print()
    print('adjacent-epoch deltas (percentage points):')
    for v in VARGAS:
        sh = shares[v]
        deltas = [sh[i + 1] - sh[i] for i in range(len(SLOTS) - 1)]
        print(v.ljust(28) + ''.join(f'{d:+14.2f} ' for d in deltas))


if __name__ == '__main__':
    main()
