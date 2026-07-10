# -*- coding: utf-8 -*-
"""H385 — generate RWS_SKIPPED.md from the triage + agent skips.

Documents every RWS finding NOT internalised into the book prose, grouped by
Д-cluster with the reason, per handoff DO #1 ("спорные и вкусовые или требующие
фактов, которых нет — не внедрять, копить с причиной"). Sources:
  * triage SKIP  (Д4 sources/sutra, Д5 tradition/apparatus) — need a fact not on hand
  * triage SOFTEN (Д3 unsupported claims) — deferred hedges
  * agent-reported per-finding skips inside apply-paragraphs
Stdlib only.
"""
import json, sys, io, csv
from collections import defaultdict, Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
REV = r'C:\Users\user\Documents\GitHub\SanskritGrammar-h385\GasunsDhatu_2014\revision-2026'

CLUSTER_TITLE = {
    'Д3': 'Д3 — недоказанные утверждения (смягчение отложено)',
    'Д4': 'Д4 — нет источника / сутры / страницы / стиха',
    'Д5': 'Д5 — требуется добавить научный слой (традиция, комментарий, аппарат)',
}
CLUSTER_REASON = {
    'Д3': 'Находка просит подкрепить утверждение доказательством. Лёгкое смягчение '
          '(«по-видимому», «как принято считать») внедрялось только внутри уже '
          'переработанных абзацев; отдельный проход смягчений отложен, чтобы не менять '
          'регистр всей книги одним махом.',
    'Д4': 'Находка требует конкретной ссылки — номера сутры Панини, ведийского стиха, '
          'страницы издания или вторичной литературы, — которых нет на руках. Внедрять '
          'ссылку «на память» нельзя (референт-видимый дефект), поэтому находка отложена '
          'до прохода с источниками.',
    'Д5': 'Находка просит дописать содержательный научный слой (традицию комментария, '
          'цепочку авторитетов, аппарат разночтений). Это не стилистическая правка, а '
          'исследовательская работа с источниками — вне задачи H385.',
}

def main():
    tri = json.load(open(REV + r'\rws_triage.json', encoding='utf-8'))
    try:
        agent_skips = json.load(open(REV + r'\rws_agent_skips.json', encoding='utf-8'))
    except FileNotFoundError:
        agent_skips = []

    # gather skipped/soften findings from triage
    buckets = defaultdict(list)  # cluster -> list of (file,line,style,type,finding)
    typecount = defaultdict(Counter)
    for p in tri['paragraphs']:
        for f in p['findings']:
            if f['disposition'] in ('SKIP', 'SOFTEN'):
                buckets[f['cluster']].append((p['file'], p['line'], f['style'], f['type'], f['finding']))
                typecount[f['cluster']][f['type']] += 1

    lines = []
    lines.append('# RWS-находки, не внедрённые в прозу (H385)')
    lines.append('')
    lines.append('_Created: 10-07-2026 · Last updated: 10-07-2026_')
    lines.append('')
    lines.append('Список RWS-находок, **не** внедрённых в текст книги при задаче '
                 '[H385](https://github.com/gasyoun/Uprava/blob/main/handoffs/H385-Opus_SanskritGrammar_gasuns-dhatu-rws-apply-highlight_08.07.26.md), '
                 'с причиной по кластерам. Внедрённые находки — в '
                 '[`rws_edits.jsonl`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/rws_edits.jsonl); '
                 'сводка — в '
                 '[`RWS_APPLY_MEMO.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/RWS_APPLY_MEMO.md).')
    lines.append('')
    total = sum(len(v) for v in buckets.values())
    lines.append(f'**Итого отложено:** {total} находок '
                 + ', '.join(f'{c} — {len(buckets[c])}' for c in sorted(buckets)) + '.')
    lines.append('')

    for c in ['Д4', 'Д5', 'Д3']:
        if c not in buckets:
            continue
        lines.append(f'## {CLUSTER_TITLE[c]} — {len(buckets[c])} находок')
        lines.append('')
        lines.append('_' + CLUSTER_REASON[c] + '_')
        lines.append('')
        lines.append('Распределение по типу находки:')
        lines.append('')
        for t, n in typecount[c].most_common():
            lines.append(f'- `{t}` — {n}')
        lines.append('')

    if agent_skips:
        lines.append('## Точечные пропуски внутри переработанных абзацев')
        lines.append('')
        lines.append('Находки, помеченные исполнителем к внедрению, но при переработке '
                     'абзаца отклонённые (обычно — требовали ссылки):')
        lines.append('')
        rc = Counter(s.get('reason', '') for s in agent_skips)
        for r, n in rc.most_common():
            lines.append(f'- {n}× — {r}')
        lines.append('')

    lines.append('_Dr. Mārcis Gasūns_')
    open(REV + r'\RWS_SKIPPED.md', 'w', encoding='utf-8', newline='').write('\n'.join(lines) + '\n')
    print('wrote RWS_SKIPPED.md — skipped/soften findings:', total,
          '| agent point-skips:', len(agent_skips))

if __name__ == '__main__':
    main()
