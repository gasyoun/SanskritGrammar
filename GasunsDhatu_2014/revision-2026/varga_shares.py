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

Usage:  python varga_shares.py [path-to-varna_freq.csv]
Writes: varga_shares.csv next to this script; prints a summary.
"""
import csv
import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

DEFAULT_SRC = Path(__file__).resolve().parents[3] / 'VisualDCS' / 'derived-data' / 'Fonetika' / 'regen-2026' / 'varna_freq.csv'

# slp1 -> varga for the 25 sparsa varnas (stops + nasals)
VARGAS = {
    'кантхья (гуттуральные)': ['k', 'K', 'g', 'G', 'N'],
    'талавья (палатальные)':  ['c', 'C', 'j', 'J', 'Y'],
    'мурдханья (церебральные)': ['w', 'W', 'q', 'Q', 'R'],
    'дантья (дентальные)':    ['t', 'T', 'd', 'D', 'n'],
    'оштхья (лабиальные)':    ['p', 'P', 'b', 'B', 'm'],
}
SLOTS = ['slot1', 'slot2', 'slot3', 'slot4', 'slot5']
EPOCH_LABELS = ['ведийский', 'эпический', 'классический', 'средневековый', 'поздний']


def main() -> None:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC
    rows = {r['slp1']: r for r in csv.DictReader(src.open(encoding='utf-8'))}

    counts = {}  # varga -> [count per slot]
    for varga, letters in VARGAS.items():
        per_slot = [0] * len(SLOTS)
        for l in letters:
            if l not in rows:
                raise SystemExit(f'varna {l!r} missing from {src}')
            for i, s in enumerate(SLOTS):
                per_slot[i] += int(rows[l][s])
        counts[varga] = per_slot

    slot_totals = [sum(counts[v][i] for v in VARGAS) for i in range(len(SLOTS))]
    grand = sum(slot_totals)

    # Cramer's V over the 5x5 contingency table (varga x epoch)
    chi2 = 0.0
    for v in VARGAS:
        row_total = sum(counts[v])
        for i in range(len(SLOTS)):
            expected = row_total * slot_totals[i] / grand
            chi2 += (counts[v][i] - expected) ** 2 / expected
    k = min(len(VARGAS), len(SLOTS))
    cramers_v = math.sqrt(chi2 / (grand * (k - 1)))

    out = Path(__file__).with_name('varga_shares.csv')
    with out.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['varga'] + [f'{e}_count' for e in EPOCH_LABELS] + [f'{e}_share_pct' for e in EPOCH_LABELS] + ['total_count', 'total_share_pct'])
        for v in VARGAS:
            row_total = sum(counts[v])
            shares = [100 * counts[v][i] / slot_totals[i] for i in range(len(SLOTS))]
            w.writerow([v] + counts[v] + [f'{s:.2f}' for s in shares] + [row_total, f'{100 * row_total / grand:.2f}'])
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
        shares = [100 * counts[v][i] / slot_totals[i] for i in range(len(SLOTS))]
        print(v.ljust(28) + ''.join(f'{s:14.2f}%' for s in shares))
    print()
    print('adjacent-epoch deltas (percentage points):')
    for v in VARGAS:
        shares = [100 * counts[v][i] / slot_totals[i] for i in range(len(SLOTS))]
        deltas = [shares[i + 1] - shares[i] for i in range(len(SLOTS) - 1)]
        print(v.ljust(28) + ''.join(f'{d:+14.2f} ' for d in deltas))


if __name__ == '__main__':
    main()
